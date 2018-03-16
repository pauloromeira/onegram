from onegram.constants import DEFAULT_COOKIES


def test_session(session):
    cookies = {'csrftoken': 'token'}
    cookies.update(DEFAULT_COOKIES)
    assert cookies == session.cookies
    assert session.username == 'username'
    assert session.user_id == '1'

