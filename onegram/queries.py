import json
import logging

from sessionlib import sessionaware

from .constants import URLS

logger = logging.getLogger(__name__)


@sessionaware
def user(session, username=None):
    username = username or session.username

    url = URLS['user'](username)
    params = {'__a': '1'}
    response = session.query(url, params=params)

    return json.loads(response.text)
