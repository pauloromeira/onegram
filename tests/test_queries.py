import pytest

from onegram.queries import user_info, post_info
from onegram.queries import followers, following
from onegram.queries import posts, likes, comments, feed
from onegram.queries import explore

# TODO [romeira]: followers
#                 following
#                 posts
#                 likes
#                 comments
#                 feed
#                 explore
# {02/04/18 23:09}


@pytest.mark.usefixtures('cassette')
def test_user_info(username):
    u_info = user_info(username)
    assert u_info['id']
    assert u_info['username'] == username
    assert u_info['edge_followed_by']['count'] is not None
    assert u_info['edge_follow']['count'] is not None


@pytest.mark.usefixtures('cassette')
def test_user_info_self(session):
    u_info = user_info()
    assert u_info['id'] == session.user_id
    # TODO [romeira]: fix betamax placeholder issue: 
    #                 replace encoded body {03/04/18 02:10}
    # assert u_info['username'] == session.username
    assert u_info['edge_followed_by']['count'] is not None
    assert u_info['edge_follow']['count'] is not None


@pytest.mark.usefixtures('cassette')
def test_post_info(post, user):
    p_info = post_info(post)
    assert p_info['id'] == post['id']
    assert p_info['shortcode'] == post['shortcode']
    assert p_info['display_url']

    owner = p_info['owner']
    assert owner['id'] == user['id']
    assert owner['username'] == user['username']
