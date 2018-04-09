from itertools import islice

from onegram import followers, following
from onegram import posts, likes, comments, feed
from onegram import explore

# TODO [romeira]:
#                 following
#                 following_self
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
    assert_followers(session, user, followers(user))


def test_followers_self(session, self, cassette):
    assert_followers(session, self, followers())


def assert_followers(session, user, followers):
    count = followers_count(session.settings, user)
    followers = list(islice(followers, count))
    assert len(followers) == count

    for follower in followers:
        assert follower['id']
        assert follower['username']


def followers_count(settings, user, pages=3):
    chunks = settings['QUERY_CHUNKS']['followers']()
    result_count = sum(islice(chunks, pages))
    followers_count = user['edge_followed_by']['count']
    return min(result_count, followers_count)
