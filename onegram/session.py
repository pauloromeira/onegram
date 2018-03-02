import json
import logging

import requests
from sessionlib import Session, sessionaware
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .settings import load_settings
from .constants import DEFAULT_HEADERS, QUERY_HEADERS, ACTION_HEADERS
from .constants import URLS, COOKIES
from .utils import sleep

logger = logging.getLogger(__name__)


class Login(Session):

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
        self._requests = yield requests.Session()
        self._requests.headers.update(DEFAULT_HEADERS)

        verify_ssl = self.settings.get('VERIFY_SSL', True)
        self._requests.verify = verify_ssl
        if not verify_ssl:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        user_agent = self.settings.get('USER_AGENT')
        if user_agent is None:
            user_agent = UserAgent(verify_ssl=verify_ssl).random

        self._requests.headers.update({'User-Agent': user_agent})

        self._login()


    # TODO [romeira]: handle 'wait few minutes' - jd/tenacity {01/03/18 21:13}
    def action(self, *a, **kw):
        headers = ACTION_HEADERS
        headers['X-CSRFToken'] = self._requests.cookies['csrftoken']
        if 'headers' in kw:
            headers = headers.copy()
            headers.update(kw['headers'])
        kw['headers'] = headers

        # TODO [romeira]: calculate from the last time a request was made  {28/02/18 17:40}
        sleep(self.settings.get('ACTION_DELAY', 0))
        response = self._requests.post(*a, **kw)
        return json.loads(response.text)


    def query(self, *a, **kw):
        headers = QUERY_HEADERS
        if 'headers' in kw:
            headers = headers.copy()
            headers.update(kw['headers'])
        kw['headers'] = headers

        sleep(self.settings.get('QUERY_DELAY', 0))
        response = self._requests.get(*a, **kw)
        return json.loads(response.text)


    def _login(self):
        response = self._requests.get(URLS['start'])

        self._requests.cookies.update(COOKIES)

        payload = {
            'username': self.settings['USERNAME'],
            'password': self.settings['PASSWORD']
        }

        response = self.action(URLS['login'], data=payload)


    def __str__(self):
        return f'({self.username})'



def login(*args, **kwargs):
    insta = Login(*args, **kwargs)
    return insta.open()


@sessionaware
def logout(session):
    try:
        session.close()
    except:
        pass
