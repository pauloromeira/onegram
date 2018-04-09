from itertools import islice

from onegram import followers, following
from onegram import posts, likes, comments, feed
from onegram import explore

# TODO [romeira]:
#                 posts
#                 posts_self
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
    count = follows_count(session, user, 'followers')
    assert_follows(session, followers(user), count)


def test_followers_self(session, self, cassette):
    count = follows_count(session, self, 'followers')
    assert_follows(session, followers(), count)


def test_following(session, user, cassette):
    count = follows_count(session, user, 'following')
    assert_follows(session, following(user), count)


def test_following_self(session, self, cassette):
    count = follows_count(session, self, 'following')
    flwgs = assert_follows(session, following(), count)
    assert all(f['followed_by_viewer'] for f in flwgs)


#######################################################################
#                               HELPERS                               #
#######################################################################

def assert_follows(session, follows, count):
    follows = list(islice(follows, count))
    assert len(follows) == count

    for f in follows:
        assert f['id']
        assert f['username']

    return follows


def follows_count(session, user, query, pages=3):
    chunks = session.settings['QUERY_CHUNKS'][query]()
    result_count = sum(islice(chunks, pages))
    edge = 'edge_follow' if query == 'following' else 'edge_followed_by'
    follows_count = user[edge]['count']
    return min(result_count, follows_count)
