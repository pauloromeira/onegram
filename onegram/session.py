import logging

import requests
from sessionlib import Session

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
        self._login()


    def _login(self):
        pass


    def __str__(self):
        return f'({self.username})'
