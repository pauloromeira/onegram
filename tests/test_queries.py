from itertools import islice

from onegram.constants import JSPATHS

from onegram import followers, following
from onegram import posts, likes, comments, feed
from onegram import explore

# TODO [romeira]:
#                 likes
#                 comments
#                 feed
#                 explore
# {02/04/18 23:09}


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
    assert_follows(session, followers(user), user)


def test_following(session, user, cassette):
    assert_follows(session, following(user), user)


def test_self_followers(session, self, cassette):
    assert_follows(session, followers(), self)


def test_self_following(session, self, cassette):
    flwgs = assert_follows(session, following(), self)
    assert all(f['followed_by_viewer'] for f in flwgs)


def test_posts(session, user, cassette):
    assert_posts(session, posts(user), user)


def test_self_posts(session, self, cassette):
    assert_posts(session, posts(), self)


#######################################################################
#                               HELPERS                               #
#######################################################################

def assert_follows(session, follows, user):
    follows = assert_iter(session, follows, user)
    for f in follows:
        assert f['id']
        assert f['username']
    return follows


def assert_posts(session, posts, user):
    posts = assert_iter(session, posts, user)
    for p in posts:
        assert p['id']
        assert p['shortcode']
        assert p['display_url']
        assert p['owner']['id']
    return posts


def assert_iter(session, iter_query, target, pages=3):
    count = iter_count(session, iter_query, target, pages)
    items = list(islice(iter_query, count))
    assert len(items) == count
    return items


def iter_count(session, iter_query, target, pages):
    query = iter_query.__name__
    chunks = session.settings['QUERY_CHUNKS'][query]()
    result_count = sum(islice(chunks, pages))
    edge = JSPATHS[query].split('.')[-1]
    count = target[edge]['count']
    return min(result_count, count)
