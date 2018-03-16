from onegram.session import Login
from onegram.constants import DEFAULT_COOKIES


def test_session_attrs(session):
    cookies = {'csrftoken': 'token'}
    cookies.update(DEFAULT_COOKIES)
    assert cookies == session.cookies
    assert session.username == 'username'
    assert session.user_id == '1'


def test_login_request(responses, session):
    request = responses.last_request
    assert request.text == 'username=username&password=password'
    assert request.headers['X-CSRFToken'] == 'token'


def test_current_session(session):
    assert session == Login.current()
