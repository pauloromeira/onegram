import os
import pytest
import requests

from betamax import Betamax
from betamax.fixtures.pytest import _casette_name as _cassette_name
from betamax_serializers import pretty_json
from pathlib import Path

from onegram import Login, Unlogged
from onegram import post_info, user_info
from onegram import posts


@pytest.fixture(scope='session')
def username():
    return os.environ['INSTA_USERNAME']

@pytest.fixture(scope='session')
def password():
    return os.environ['INSTA_PASSWORD']

@pytest.fixture(scope='session')
def test_username():
    return os.environ['ONEGRAM_TEST_USERNAME']

@pytest.fixture(scope='session')
def record_mode():
    return os.environ['ONEGRAM_TEST_RECORD_MODE']

@pytest.fixture
def settings(record_mode):
    return {'RATE_LIMITS': None} if record_mode == 'none' else {}

def _logged_id(param):
    return 'logged' if param else 'unlogged'

@pytest.fixture(params=[True, False], ids=_logged_id)
def logged(request):
    return request.param



@pytest.fixture
def recorder(logged, monkeypatch, username, password, record_mode):
    Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    cassete_dir = Path(f'tests/cassettes/')
    cassete_dir.mkdir(parents=True, exist_ok=True)

    placeholders = [
        {'placeholder': 'INSTA_USERNAME', 'replace': username},
        {'placeholder': 'INSTA_PASSWORD', 'replace': password},
    ]

    options = {
        'serialize_with': 'prettyjson',
        'placeholders': placeholders,
        'record_mode': record_mode,
    }

    with Betamax(requests.Session(), cassette_library_dir=cassete_dir,
                 default_cassette_options=options) as recorder:
        monkeypatch.setattr(requests, 'Session', lambda: recorder.session)
        yield recorder


@pytest.fixture
def session(logged, recorder, settings):
    recorder.use_cassette(f'fixture_session[{_logged_id(logged)}]')
    if logged:
        session = Login(custom_settings=settings)
    else:
        session = Unlogged(custom_settings=settings)

    with session:
        recorder.current_cassette.eject()
        yield session


@pytest.fixture
def user(session, logged, recorder, test_username):
    recorder.use_cassette(f'fixture_user[{_logged_id(logged)}]')
    try:
        return user_info(test_username)
    finally:
        recorder.current_cassette.eject()


@pytest.fixture
def self(session, logged, recorder):
    if not logged:
        return None

    recorder.use_cassette(f'fixture_self[{_logged_id(logged)}]')
    try:
        return user_info()
    finally:
        recorder.current_cassette.eject()


@pytest.fixture
def post(recorder, logged, user):
    recorder.use_cassette(f'fixture_post[{_logged_id(logged)}]')
    try:
        return post_info(next(posts(user)))
    finally:
        recorder.current_cassette.eject()


@pytest.fixture
def cassette(recorder, request):
    cassette_name = _cassette_name(request, True)
    recorder.use_cassette(cassette_name)
    cassette = recorder.current_cassette
    yield cassette
    cassette.eject()
