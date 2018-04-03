import pytest

from onegram.queries import user_info, post_info
from onegram.queries import followers, following
from onegram.queries import posts, likes, comments, feed
from onegram.queries import explore

# TODO [romeira]: post_info
#                 followers
#                 following
#                 posts
#                 likes
#                 comments
#                 feed
#                 explore
# {02/04/18 23:09}


@pytest.mark.usefixtures('cassette')
def test_user_info(username):
    user = user_info(username)
    assert user['id']
    assert user['username'] == username
    assert user['edge_followed_by']['count'] is not None
    assert user['edge_follow']['count'] is not None


@pytest.mark.usefixtures('cassette')
def test_user_info_self(session):
    user = user_info()
    assert user['id'] == session.user_id
    assert user['username'] == session.username
    assert user['edge_followed_by']['count'] is not None
    assert user['edge_follow']['count'] is not None
