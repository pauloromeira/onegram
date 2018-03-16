from onegram.constants import URLS
from . import hash_id


def login_responses(responses):
    resps = []
    resps.append(responses.get(URLS['start'], cookies={'csrftoken': 'token'}))
    data = {
        'authenticated': True,
        'status': 'ok',
        'user': True
    }
    resps.append(responses.post(URLS['login'],
                                cookies={'ds_user_id': hash_id('username')},
                                json=data))
    return resps

def user_info_responses(responses, username):
    data = {'graphql': {'user': {'id': hash_id(username)} }}
    return [responses.get(URLS['user_info'](username=username), json=data)]

def follow_responses(responses, username):
    user_id = hash_id(username)
    data = {
        'result': 'following',
        'status': 'ok'
    }
    return [responses.post(URLS['follow'](user_id=user_id), json=data)]

def unfollow_responses(responses, username):
    user_id = hash_id(username)
    data = {
        'status': 'ok'
    }
    return [responses.post(URLS['unfollow'](user_id=user_id), json=data)]
