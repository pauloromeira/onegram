import json
from ..exceptions import AuthFailed, AuthUserError
from ..exceptions import RequestFailed, RateLimitedError


def validate_response(session, response, auth=False):
    try:
        try:
            js_response = json.loads(response.text)
        except:
            response.raise_for_status()
            if auth:
                raise AuthFailed('Authentication failed')
        else:
            if auth:
                _check_auth(js_response)
            _check_status(js_response)
            response.raise_for_status()
            return js_response
    except:
        if response:
            session.logger.error(response.text)
        raise


def _check_auth(response):
    if not response.get('user', False):
        raise AuthUserError('Please check your username')
    if not response.get('authenticated', False):
        raise AuthFailed('Authentication failed')


def _check_status(response):
    message = response.get('message', '').lower()
    status = response.get('status', '').lower()

    msg = ''
    if status:
        msg = status
    if message:
        msg += f': {message}'

    if 'rate limit' in message:
        raise RateLimitedError(msg)
    if 'fail' in status:
        raise RequestFailed(msg)
