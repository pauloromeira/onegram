from onegram.actions import follow, unfollow

from helpers.responses import user_info_responses
from helpers.responses import follow_responses
from helpers.responses import unfollow_responses


def test_follow_username(session, responses):
    username = 'other'
    user_info_responses(responses, username)
    follow_responses(responses, username)
    follow(username)

def test_unfollow_username(session, responses):
    username = 'other'
    user_info_responses(responses, username)
    unfollow_responses(responses, username)
    unfollow(username)
