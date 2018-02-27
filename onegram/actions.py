import json
import logging

from sessionlib import sessionaware

from .queries import user_info
from .constants import URLS

logger = logging.getLogger(__name__)


@sessionaware
def follow(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    url = URLS['follow'](user_id=user['id'])

    response = session.action(url)

    logger.debug(response.text)
    return response
