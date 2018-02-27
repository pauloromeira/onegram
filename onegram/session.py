import logging

import requests
from sessionlib import Session
from fake_useragent import UserAgent

from .utils import load_settings

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
        self.requests.headers.update(self.settings['DEFAULT_HEADERS'])
        user_agent = self.settings.get('USER_AGENT')
        if not user_agent:
            user_agent = UserAgent().random
        self.requests.headers.update({'User-Agent': user_agent})

        self.cookies = {}
        self._login()


    def action(self, *a, **kw):
        if 'verify' not in kw:
            kw['verify'] = not self.settings.get('SSL_INSECURE', False)

        headers = settings.get('ACTION_HEADERS', {})
        if 'headers' in kw:
            headers.update(kw['headers'])
        headers['X-CSRFToken'] = self.cookies['csrftoken']
        kw['headers'] = headers

        self.requests.post(*a, **kw)


    def query(self, *a, **kw):
        if 'verify' not in kw:
            kw['verify'] = not self.settings.get('SSL_INSECURE', False)

        headers = settings.get('QUERY_HEADERS', {})
        if 'headers' in kw:
            headers.update(kw['headers'])
        kw['headers'] = headers

        self.requests.get(*a, **kw)


    def _login(self):
        verify = self.settings.get('SSL_INSECURE', False)
        response = self.requests.get('https://www.instagram.com/',
                                     verify=verify)

        # TODO [romeira]: como colocar direto na sessao? {26/02/18 21:44}
        # self.cookies.update({
        #     'ig_vw': '1440',
        #     'ig_pr': '2',
        #     'ig_vh': '800',
        #     'ig_or': 'landscape-primary',
        # })


    def __str__(self):
        return f'({self.username})'
