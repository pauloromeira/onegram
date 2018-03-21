from onegram.session import Login

from helpers import hash_id


def test_session_attrs(session):
    assert session.cookies['csrftoken'] == 'token'
    assert session.username == 'username'
    assert session.user_id == hash_id(session.username)

def test_login_request(session, responses):
    request = responses.last_request
    assert request.text == 'username=username&password=password&next=%2F'
    assert request.headers['X-CSRFToken'] == 'token'

def test_current_session(session):
    assert session == Login.current()
