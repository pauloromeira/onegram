import json
import logging
import requests
import urllib3

from fake_useragent import UserAgent
from getpass import getpass
from requests import HTTPError
from sessionlib import Session, sessionaware
from tenacity import retry, retry_if_exception_type, after_log
from tenacity import wait_chain, wait_fixed
from urllib3.exceptions import InsecureRequestWarning
from urllib3.util import parse_url

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

        # Security config
        verify_ssl = self.settings.get('VERIFY_SSL', True)
        self._requests.verify = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(InsecureRequestWarning)

        # Init headers
        self._requests.headers.update(DEFAULT_HEADERS)
        user_agent = self.settings.get('USER_AGENT')
        if user_agent is None:
            user_agent = UserAgent(verify_ssl=verify_ssl).random
        self._requests.headers.update({'User-Agent': user_agent})

        # Init cookies
        self._requests.get(URLS['start'])
        self._requests.cookies.update(COOKIES)

        self._login()


    def action(self, url, *a, **kw):
        sleep(self.settings.get('ACTION_DELAY', 0))
        return self.request('POST', url, *a, **kw)

    def query(self, url, *a, **kw):
        sleep(self.settings.get('QUERY_DELAY', 0))
        return self.request('GET', url, *a, **kw)


    @retry(wait=wait_chain(wait_fixed(60), wait_fixed(15)),
           retry=retry_if_exception_type(HTTPError),
           after=after_log(logger, logging.INFO))
    def request(self, method, url, *a, **kw):
        if kw.pop('no_proxy', False):
            kw['proxies'] = {'no_proxy': parse_url(url).host}

        if method == 'POST':
            headers = ACTION_HEADERS
            headers['X-CSRFToken'] = self._requests.cookies['csrftoken']
        else:
            headers = QUERY_HEADERS

        if 'headers' in kw:
            kw['headers'].update(headers)
        else:
            kw['headers'] = headers

        try:
            response = self._requests.request(method, url, *a, **kw)
            response.raise_for_status()
            return json.loads(response.text)
        except Exception:
            logger.error(response.text)
            raise


    def _login(self):
        self.username = self.username or input('Username: ')
        payload = {
            'username': self.username,
            'password': self.settings.get('PASSWORD') or getpass()
        }
        no_proxy = self.settings.get('DISABLE_LOGIN_PROXY', False)
        self.action(URLS['login'], data=payload, no_proxy=no_proxy)


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
