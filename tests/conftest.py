import pytest
import requests_mock

from onegram import login, logout
from helpers.responses import login_responses


@pytest.fixture
def responses():
    with requests_mock.mock() as mocker:
        yield mocker

@pytest.fixture
def session(responses):
    settings = {
        'USER_AGENT': 'user-agent',
        'RATE_LIMITS': None,
    }
    login_responses(responses)
    sess = login(custom_settings=settings)
    yield sess
    logout()


