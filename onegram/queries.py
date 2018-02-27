import json
import logging

from sessionlib import sessionaware

from .constants import URLS
from .utils import jsearch

logger = logging.getLogger(__name__)


@sessionaware
def user_info(session, username=None):
    username = username or session.username

    url = URLS['user_info'](username=username)
    params = {'__a': '1'}
    response = session.query(url, params=params)

    logger.debug(response.text)
    return jsearch('user', response)
