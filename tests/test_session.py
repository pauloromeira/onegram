import pytest

from sessionlib import Session

from onegram import login, logout
from onegram.exceptions import AuthUserError, AuthFailed


def test_invalid_user(settings, cassette):
    invalid_user = 'xxx'
    with pytest.raises(AuthUserError):
        login(username=invalid_user, custom_settings=settings)

    assert Session.current() is None


def test_invalid_password(settings, password, cassette):
    wrong_password = 'wrong' + password
    with pytest.raises(AuthFailed):
        login(password=wrong_password, custom_settings=settings)

    assert Session.current() is None


def test_session_functions(settings, cassette):
    assert Session.current() is None
    login(custom_settings=settings)
    assert Session.current()
    logout()
    assert Session.current() is None
