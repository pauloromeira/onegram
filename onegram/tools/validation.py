from ..exceptions import AuthFailed, AuthUserError


def check_auth(response):
    if not response.get('user', False):
        raise AuthUserError('Please check your username')
    if not response.get('authenticated', False):
        raise AuthFailed('Authentication failed')
