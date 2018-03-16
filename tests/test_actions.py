from onegram.actions import follow

from helpers.responses import user_info_responses
from helpers.responses import follow_responses


def test_follow_username(session, responses):
    username = 'other'
    user_info_responses(responses, username)
    follow_responses(responses, username)
    follow(username)
