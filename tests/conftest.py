import os
import pytest
import requests

from _pytest.monkeypatch import MonkeyPatch
from betamax import Betamax
from betamax.fixtures.pytest import _casette_name as _cassette_name
from betamax_serializers import pretty_json
from pathlib import Path

from onegram import Login
from onegram import post_info, user_info
from onegram import posts


@pytest.fixture(scope='session')
def monkeypatch_session():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope='session')
def betamax(monkeypatch_session):
    Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    cassete_dir = Path('tests/cassettes/')
    cassete_dir.mkdir(parents=True, exist_ok=True)
    username = os.environ['INSTA_USERNAME']
    password = os.environ['INSTA_PASSWORD']
    record_mode = os.environ.get('ONEGRAM_TEST_RECORD_MODE', 'none')

    placeholders = [
        {'placeholder': 'INSTA_USERNAME', 'replace': username},
        {'placeholder': 'INSTA_PASSWORD', 'replace': password},
    ]

    options = {
        'serialize_with': 'prettyjson',
        'placeholders': placeholders,
        'record_mode': record_mode,
    }

    with Betamax(requests.Session(),
                 cassette_library_dir=cassete_dir,
                 default_cassette_options=options) as recorder:
        monkeypatch_session.setattr(requests,
                                    'Session',
                                    lambda: recorder.session)
        yield recorder


@pytest.fixture(scope='session', autouse=True)
def session(request, betamax):
    settings = {'RATE_LIMITS': None, 'USER_AGENT': None}
    betamax.use_cassette('fixture_session')
    with Login(custom_settings=settings) as session:
        betamax.current_cassette.eject()
        yield session


@pytest.fixture(scope='session')
def username():
    return os.environ['ONEGRAM_TEST_USERNAME']


@pytest.fixture(scope='session')
def user(betamax, username):
    betamax.use_cassette('fixture_user')
    try:
        return user_info(username)
    finally:
        betamax.current_cassette.eject()


@pytest.fixture(scope='session')
def self(betamax):
    betamax.use_cassette('fixture_self')
    try:
        return user_info()
    finally:
        betamax.current_cassette.eject()


@pytest.fixture(scope='session')
def post(betamax, user):
    betamax.use_cassette('fixture_post')
    try:
        return post_info(next(posts(user)))
    finally:
        betamax.current_cassette.eject()


@pytest.fixture
def cassette(betamax, request):
    cassette_name = _cassette_name(request, True)
    betamax.use_cassette(cassette_name)
    cassette = betamax.current_cassette
    yield cassette
    cassette.eject()
