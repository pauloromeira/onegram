import hashlib
import json
import logging
import re
import requests
import urllib3

from getpass import getpass
from requests import HTTPError
from sessionlib import Session
from sessionlib import sessionaware as _sessionaware
from tenacity import retry, retry_never
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url

from . import settings as settings_module
from .constants import DEFAULT_HEADERS, QUERY_HEADERS, ACTION_HEADERS
from .constants import URLS
from .constants import REGEXES
from .exceptions import AuthException, NotSupportedError
from .utils.ratelimit import RateLimiter
from .utils.validation import validate_response
from .utils import humanize_interval


class _BaseSession(Session):


    @classmethod
    def current(cls):
        return Session.current() or login()


    @property
    def current_function_name(self):
        return (self.current_function.__name__
                if self.current_function else None)

    @property
    def current_module_name(self):
        return (self.current_function.__module__.split('.', 1)[-1]
                if self.current_function else None)

    @property
    def cookies(self):
        return self._requests.cookies


    @property
    def unlogged(self):
        return isinstance(self, Unlogged)


    def __init__(self, custom_settings={}):
        self.settings = _load_settings(custom_settings)

        log_settings = self.settings.get('LOG_SETTINGS')
        if log_settings:
            logging.basicConfig(**log_settings)


    def enter_contexts(self):
        self._requests = yield requests.Session()

        proxies = self.settings.get('PROXIES')
        if proxies:
            self._requests.proxies = proxies

        verify_ssl = self.settings.get('VERIFY_SSL', True)
        self._requests.verify = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(InsecureRequestWarning)

        self._requests.headers.update(DEFAULT_HEADERS)
        user_agent = self.settings.get('USER_AGENT')
        if user_agent is not None:
            self._requests.headers['User-Agent'] = user_agent
        else:
            self._requests.headers.pop('User-Agent', None)

        response = self._requests.get(URLS['start'])
        response.raise_for_status()
        self.rhx_gis = self._get_rhx_gis(response)

        self.rate_limiter = RateLimiter(self)


    def action(self, url, *a, **kw):
        headers = kw.setdefault('headers', ACTION_HEADERS)
        headers['X-CSRFToken'] = self.cookies['csrftoken']
        return self.request('POST', url, *a, **kw)


    def query(self, url, *a, **kw):
        headers = kw.setdefault('headers', QUERY_HEADERS)
        signature = self._build_signature(url, kw.get('params'))
        headers['X-Instagram-GIS'] = signature
        return self.request('GET', url, *a, **kw)


    def request(self, method, url, *a, **kw):
        def _after_request_attempt(func, tries, secs):
            msg = f'RETRY {tries} attempt(s)'
            if tries > 1:
                interval = humanize_interval(secs)
                msg += f'. Time spent: {interval}'
            msg += ' ...'
            self.logger.warning(msg)

        if self.settings.get('RETRY_ENABLED'):
            retry_kw = {'after': _after_request_attempt}
            retry_kw.update(self.settings.get('RETRY_SETTINGS', {}))
        else:
            retry_kw = {'retry': retry_never}

        @retry(**retry_kw)
        def _request():
            with self.rate_limiter:
                self.logger.info(f'{method} "{url}"')
                response = self._requests.request(method, url, *a, **kw)
                return validate_response(self, response)

        return _request()


    def _get_rhx_gis(self, response):
        match = re.search(REGEXES['rhx_gis'], response.text)
        return match.group(1) if match else None


    def _build_signature(self, url, params):
        if self.current_function_name in ('post_info', 'user_info'):
            var = parse_url(url).path
        else:
            var = params.get('variables')

        payload = f'{self.rhx_gis}:{var}'
        return hashlib.md5(payload.encode('utf-8')).hexdigest()


    @property
    def logger(self):
        name = f'{__name__}:{self}'
        if self.current_function:
            name += f' {self.current_module_name}.{self.current_function_name}'
        return logging.getLogger(name)


class Login(_BaseSession):


    def __init__(self, username=None, password=None, custom_settings={}):
        if username:
            custom_settings['USERNAME'] = username
        if password:
            custom_settings['PASSWORD'] = password

        super(Login, self).__init__(custom_settings)

        self.username = self.settings.get('USERNAME')
        # TODO [romeira]: fix sessionlib {06/05/18 04:41}
        # self.on_open.subscribe(self._login)


    def enter_contexts(self):
        yield from super(Login, self).enter_contexts()
        try:
            self._login()
        except AuthException as e:
            self.logger.error(e)
            self.close()
            raise e


    def _login(self):
        kw = {}
        self.username = self.username or input('Username: ')
        kw['data'] = {
            'username': self.username,
            'password': self.settings.get('PASSWORD') or getpass(),
            'queryParams': '{}',
        }

        headers = ACTION_HEADERS
        headers['X-CSRFToken'] = self.cookies['csrftoken']
        kw['headers'] = headers
        response = self._requests.post(URLS['login'], **kw)
        self.user_id = self.cookies.get('ds_user_id', None)
        return validate_response(self, response, auth=True)


    def __str__(self):
        return f'({self.username})'


class Unlogged(_BaseSession):

    supported = ['user_info', 'post_info', 'posts', 'comments', 'explore_tag']

    def __init__(self, custom_settings={}):
        super(Unlogged, self).__init__(custom_settings)


    def request(self, *a, **kw):
        fn = self.current_function_name 
        if fn not in Unlogged.supported:
            msg = f'"{fn}" is not supported at Unlogged state'
            raise NotSupportedError(msg)

        return super(Unlogged, self).request(*a, **kw)


    def __str__(self):
        return f'(Unlogged[{id(self)}])'


sessionaware = _sessionaware(cls=_BaseSession)


def login(*args, **kwargs):
    return Login(*args, **kwargs).open()


@_sessionaware
def close(session):
    session.close()


logout = close


def unlogged(*args, **kwargs):
    return Unlogged(*args, **kwargs).open()


def _load_settings(custom_settings={}):
    settings = {k:getattr(settings_module, k)
                for k in dir(settings_module) if k.isupper()}
    settings.update(custom_settings)
    return settings
