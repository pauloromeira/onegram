from onegram.actions import follow, unfollow
from onegram.constants import URLS

from helpers.responses import user_info_responses
from helpers.responses import follow_responses
from helpers.responses import unfollow_responses


def assert_action(session, responses, resps):
    request = responses.last_request
    assert request.headers['X-CSRFToken'] == 'token'
    assert all(r.called_once for r in resps)

def test_follow(session, responses):
    username = 'other'
    resps = user_info_responses(responses, username)
    resps += follow_responses(responses, username)
    follow(username)
    assert_action(session, responses, resps)

def test_unfollow(session, responses):
    username = 'other'
    resps = user_info_responses(responses, username)
    resps += unfollow_responses(responses, username)
    unfollow(username)
    assert_action(session, responses, resps)
