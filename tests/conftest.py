import pytest
import requests_mock

from onegram import login, logout
from onegram.constants import URLS


@pytest.fixture
def responses():
    with requests_mock.mock() as mocker:
        yield mocker

@pytest.fixture
def session(responses):
    custom_settings = {'USER_AGENT': 'user-agent'}
    cookies = {'csrftoken': 'token'}
    responses.get(URLS['start'], cookies=cookies)
    responses.post(URLS['login'])

    sess = login(custom_settings=custom_settings)
    sess.user_id = '1'
    yield sess

    logout()


