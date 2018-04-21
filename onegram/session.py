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
from tenacity import retry, retry_if_exception_type
from tenacity import wait_chain, wait_fixed
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url

from . import settings as settings_module
from .constants import DEFAULT_HEADERS, QUERY_HEADERS, ACTION_HEADERS
from .constants import URLS
from .constants import REGEXES
from .exceptions import AuthException
from .utils.ratelimit import RateLimiter
from .utils.validation import check_auth


class Login(Session):

    @classmethod
    def current(cls):
        return Session.current() or login()

    @property
    def current_module_name(self):
        return (self.current_function.__module__.split('.', 1)[-1]
                if self.current_function else None)

    @property
    def current_function_name(self):
        return (self.current_function.__name__
                if self.current_function else None)

    @property
    def cookies(self):
        return self._requests.cookies


    def __init__(self, username=None, password=None, custom_settings={}):
        if username:
            custom_settings['USERNAME'] = username
        if password:
            custom_settings['PASSWORD'] = password

        self.settings = _load_settings(custom_settings)

        log_settings = self.settings.get('LOG_SETTINGS')
        if log_settings:
            logging.basicConfig(**log_settings)

        self.username = self.settings.get('USERNAME')


    def enter_contexts(self):
        self._requests = yield requests.Session()

        # Security config
        verify_ssl = self.settings.get('VERIFY_SSL', True)
        self._requests.verify = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(InsecureRequestWarning)

        # Init headers
        self._requests.headers.update(DEFAULT_HEADERS)
        user_agent = self.settings.get('USER_AGENT')
        if user_agent is not None:
            self._requests.headers['User-Agent'] = user_agent
        else:
            self._requests.headers.pop('User-Agent', None)

        try:
            self._login()
        except AuthException as e:
            self.logger.error(e)
            self.close()
            raise e

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
        def _after_request_attempt(func, trial_number, *a, **kw):
            self.logger.warning(f'RETRY {trial_number} attempt(s) ...')

        @retry(wait=wait_chain(wait_fixed(60), wait_fixed(15)),
               retry=retry_if_exception_type(HTTPError),
               after=_after_request_attempt)
        def _request():
            with self.rate_limiter:
                self.logger.info(f'{method} "{url}"')
                response = None
                try:
                    response = self._requests.request(method, url, *a, **kw)
                    response.raise_for_status()
                    return json.loads(response.text)
                except Exception:
                    if response:
                        self.logger.error(response.text)
                    raise
        return _request()


    def _login(self):
        start_url, login_url = URLS['start'], URLS['login']
        response = self._requests.get(start_url)
        response.raise_for_status()
        self.rhx_gis = self._get_rhx_gis(response)

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

        response = self._requests.post(login_url, **kw)
        response.raise_for_status()
        check_auth(json.loads(response.text))
        self.user_id = self.cookies.get('ds_user_id')


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


    def __str__(self):
        return f'({self.username})'


sessionaware = _sessionaware(cls=Login)


def login(*args, **kwargs):
    return Login(*args, **kwargs).open()


@_sessionaware
def logout(session):
    session.close()


def _load_settings(custom_settings={}):
    settings = {k:getattr(settings_module, k)
                for k in dir(settings_module) if k.isupper()}
    settings.update(custom_settings)
    return settings
