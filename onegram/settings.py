import logging

from pathlib import Path
from decouple import config

from tenacity import retry_if_exception_type
from tenacity import wait_chain, wait_fixed, wait_random
from tenacity import stop_after_delay

from .utils import head_tail, choices, repeat
from .exceptions import RateLimitedError


CURRENT_DIR = Path.cwd()

USERNAME = config('INSTA_USERNAME', default=None)
PASSWORD = config('INSTA_PASSWORD', default=None)

DEBUG = config('INSTA_DEBUG', default=False, cast=bool)

# Uncomment to set a custom User-Agent
# USER_AGENT = None

# Uncomment to set proxies
# PROXIES = {'http': '<proxy>', 'https': '<proxy>'}

VERIFY_SSL = config('VERIFY_SSL', default=True, cast=bool)

# Limits requests per second
RATE_LIMITS = {
    '*': [(1, 1)],
    'actions': [(1, 2)],
}

RATE_PERSIST_ENABLED = True
RATE_PERSIST_DIR = CURRENT_DIR / '.onegram/rates'

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s: %(message)s',
    'level': logging.DEBUG if DEBUG else logging.INFO,
}

QUERY_CHUNKS = {
    'following': head_tail(20, 10),
    'followers': head_tail(20, 10),
    'posts': repeat(12),
    'feed': repeat(12),
    'likes': head_tail(20, 10),
    'comments': choices(range(20, 40)),
    'explore': repeat(24),
    'explore_tag': choices(range(1, 13)),
}

RETRY_ENABLED = True
RETRY_SETTINGS = {
    'wait': wait_chain(wait_fixed(50) + wait_random(0, 10),
                       wait_fixed(15) + wait_random(0, 5)),
    'retry': retry_if_exception_type(RateLimitedError),
    'stop': stop_after_delay(20 * 60),
}
