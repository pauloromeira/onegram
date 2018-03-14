import logging

from pathlib import Path
from decouple import config

from .utils import head_tail, choices, repeat

BASE_DIR = Path(__file__).parent


USERNAME = config('INSTA_USERNAME', default=None)
PASSWORD = config('INSTA_PASSWORD', default=None)

DEBUG = config('INSTA_DEBUG', default=False, cast=bool)

# Leave it commented to get a random User-Agent
# USER_AGENT = ''

VERIFY_SSL = config('VERIFY_SSL', default=True, cast=bool)

DISABLE_LOGIN_PROXY = False

# Limits requests per second
RATE_LIMITS = {
    'queries': [(2, 10)],
    'posts': [(30, 60), (100, 200)],
}

RATE_CACHE_ENABLED = True
RATE_CACHE_DIR = BASE_DIR / '.onegram/rate'

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s:%(funcName)s:%(message)s',
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
}
