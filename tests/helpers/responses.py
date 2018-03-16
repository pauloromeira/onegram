from onegram.constants import URLS
from . import hash_id


def login_responses(responses):
    responses.get(URLS['start'], cookies={'csrftoken': 'token'})
    data = {
        'authenticated': True,
        'status': 'ok',
        'user': True
    }
    responses.post(URLS['login'], 
                   cookies={'ds_user_id': hash_id('username')},
                   json=data)

def user_info_responses(responses, username):
    data = {'graphql': {'user': {'id': hash_id(username)} }}
    responses.get(URLS['user_info'](username=username), json=data)

def follow_responses(responses, username):
    user_id = hash_id(username)
    data = {
        'result': 'following',
        'status': 'ok'
    }
    responses.post(URLS['follow'](user_id=user_id), json=data)
