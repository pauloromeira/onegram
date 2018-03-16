from onegram.constants import URLS
from . import hash_id


def login_responses(responses):
    responses.get(URLS['start'], cookies={'csrftoken': 'token'})
    responses.post(URLS['login'], cookies={'ds_user_id': hash_id('username')})


def user_info_responses(session, responses, username=None):
    username = username or session.username
    json = {'graphql': {'user': {'id': hash_id(username)} }}
    responses.get(URLS['user_info'](username=username), json=json)
