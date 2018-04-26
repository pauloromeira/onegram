import random

from itertools import islice

from onegram.utils import jsearch

from onegram import followers, following
from onegram import posts, likes, comments, feed
from onegram import explore

# TODO [romeira]: feed {02/04/18 23:09}


def test_user_info(user, test_username):
    assert user['id']
    assert user['username'] == test_username
    assert user['edge_followed_by']['count'] is not None
    assert user['edge_follow']['count'] is not None


def test_self_info(session, self):
    assert self['id'] == session.user_id
    # TODO [romeira]: betamax placeholders issue {05/04/18 02:48}
    # assert self['username'] == session.username
    assert self['username']
    assert self['edge_followed_by']['count'] is not None
    assert self['edge_follow']['count'] is not None


def test_post_info(post, user):
    assert post['id']
    assert post['shortcode']
    assert post['display_url']

    owner = post['owner']
    assert owner['id'] == user['id']
    assert owner['username'] == user['username']


def test_followers(session, user, cassette):
    assert_followers(session, followers(user), user)


def test_following(session, user, cassette):
    assert_following(session, following(user), user)


def test_self_followers(session, self, cassette):
    assert_followers(session, followers(), self)


def test_self_following(session, self, cassette):
    flwgs = assert_following(session, following(), self)
    assert all(f['followed_by_viewer'] for f in flwgs)


def test_posts(session, user, cassette):
    assert_posts(session, posts(user), user)


def test_self_posts(session, self, cassette):
    assert_posts(session, posts(), self)


def test_explore(session, self, cassette):
    assert_posts(session, explore(), self)


def test_likes(session, post, cassette):
    assert_likes(session, likes(post), post)


def test_comments(session, post, cassette):
    assert_comments(session, comments(post), post)


#######################################################################
#                               HELPERS                               #
#######################################################################

def assert_following(session, following, user):
    total = jsearch('edge_follow.count', user)
    following = assert_iter(session, following, total)
    for f in following:
        assert f['id']
        assert f['username']
    return following


def assert_followers(session, followers, user):
    total = jsearch('edge_followed_by.count', user)
    followers = assert_iter(session, followers, total)
    for f in followers:
        assert f['id']
        assert f['username']
    return followers


def assert_posts(session, posts, user):
    total = jsearch('edge_owner_to_timeline_media.count', user)
    posts = assert_iter(session, posts, total)
    for p in posts:
        assert p['id']
        assert p['shortcode']
        assert p['display_url']
        assert p['owner']['id']
    return posts


def assert_likes(session, likes, post):
    total = jsearch('edge_media_preview_like.count', post)
    likes = assert_iter(session, likes, total)
    for l in likes:
        assert l['id']
        assert l['username']
    return likes


def assert_comments(session, comments, post):
    total = jsearch('edge_media_to_comment.count', post)
    comments = assert_iter(session, comments, total)
    for c in comments:
        assert c['id']
        assert c['text']
        assert c['created_at']
        assert c['owner']['id']
        assert c['owner']['username']
    return comments


def assert_iter(session, iter_query, total=None, pages=3):
    random.seed(0)
    count = iter_count(session, iter_query, pages, total)
    random.seed(0)
    items = list(islice(iter_query, count))
    assert len(items) == count
    return items


def iter_count(session, iter_query, pages, total=None):
    query = iter_query.__name__
    chunks = session.settings['QUERY_CHUNKS'][query]()
    result_count = sum(islice(chunks, pages))

    if total is not None:
        return min(result_count, total)
    else:
        return result_count
