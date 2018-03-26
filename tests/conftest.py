import os
import pytest
import betamax
import onegram

from betamax_serializers import pretty_json
from pathlib import Path


@pytest.fixture(scope='session')
def username():
    return os.environ.get('INSTA_USERNAME')

@pytest.fixture(scope='session')
def password():
    return os.environ.get('INSTA_PASSWORD')


@pytest.fixture(scope="session", autouse=True)
def init_betamax(username, password):
    betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    with betamax.Betamax.configure() as config:
        cassete_dir = Path('tests/cassettes/')
        cassete_dir.mkdir(parents=True, exist_ok=True)
        config.cassette_library_dir = cassete_dir

        record_mode = os.environ.get('ONEGRAM_TEST_RECORD_MODE')
        config.default_cassette_options['record_mode'] = record_mode
        config.default_cassette_options['serialize_with'] = 'prettyjson'

        config.define_cassette_placeholder('<INSTA_USERNAME>', username)
        config.define_cassette_placeholder('<INSTA_PASSWORD>', password)


@pytest.fixture
def session(betamax_session, monkeypatch, username, password):
    monkeypatch.setattr(onegram.session.requests,
                        'Session', lambda: betamax_session)
    settings = {
        'RATE_LIMITS': None,
        'USERNAME': username,
        'PASSWORD': password,
    }
    with onegram.Login(custom_settings=settings) as session:
        yield session


@pytest.fixture
def user(session):
    username = os.environ.get('ONEGRAM_TEST_USERNAME')
    return onegram.user_info(username)
