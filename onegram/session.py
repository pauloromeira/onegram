import logging

import requests
from sessionlib import Session
from fake_useragent import UserAgent

from .utils import load_settings
from .constants import DEFAULT_HEADERS, QUERY_HEADERS, ACTION_HEADERS
from .constants import URLS, COOKIES

logger = logging.getLogger(__name__)


class Insta(Session):

    def __init__(self, username=None, password=None, custom_settings={}):
        if username:
            custom_settings['USERNAME'] = username
        if password:
            custom_settings['PASSWORD'] = password

        self.settings = load_settings(custom_settings)

        log_settings = self.settings.get('LOG_SETTINGS')
        if log_settings:
            logging.basicConfig(**log_settings)

        self.username = self.settings.get('USERNAME')


    def enter_contexts(self):
        self.requests = yield requests.Session()
        self.requests.headers.update(DEFAULT_HEADERS)

        user_agent = self.settings.get('USER_AGENT')
        if not user_agent:
            user_agent = UserAgent().random
        self.requests.headers.update({'User-Agent': user_agent})

        self._login()


    def action(self, *a, **kw):
        kw.setdefault('verify', not self.settings.get('SSL_INSECURE', False))

        headers = ACTION_HEADERS
        headers['X-CSRFToken'] = self.requests.cookies['csrftoken']
        if 'headers' in kw:
            headers = headers.copy()
            headers.update(kw['headers'])
        kw['headers'] = headers

        return self.requests.post(*a, **kw)


    def query(self, *a, **kw):
        kw.setdefault('verify', not self.settings.get('SSL_INSECURE', False))

        headers = QUERY_HEADERS
        if 'headers' in kw:
            headers = headers.copy()
            headers.update(kw['headers'])
        kw['headers'] = headers

        return self.requests.get(*a, **kw)


    def _login(self):
        verify = not self.settings.get('SSL_INSECURE', False)
        response = self.requests.get(URLS['start'], verify=verify)

        self.requests.cookies.update(COOKIES)

        payload = {
            'username': self.settings['USERNAME'],
            'password': self.settings['PASSWORD']
        }

        response = self.action(URLS['login'], data=payload)

        logger.debug(response.text)


    def __str__(self):
        return f'({self.username})'
