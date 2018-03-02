import logging

from decouple import config

from .utils import head_tail, choice_repeat, repeat


USERNAME = config('INSTA_USERNAME', default=None)
PASSWORD = config('INSTA_PASSWORD', default=None)

DEBUG = config('INSTA_DEBUG', default=False, cast=bool)

# Leave it commented to get a random User-Agent
# USER_AGENT = ''

VERIFY_SSL = config('VERIFY_SSL', default=True, cast=bool)

ACTION_DELAY = 0
QUERY_DELAY = 0

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s:%(funcName)s:%(message)s',
    'level': logging.DEBUG if DEBUG else logging.INFO,
}

QUERY_CHUNKS = {
    'following': head_tail(20, 10),
    'followers': head_tail(20, 10),
    'posts': repeat(12),
    'likes': head_tail(20, 10),
    'comments': choice_repeat(33, 28, 26, 23),
    'explore': repeat(24),
}




_default_settings = {k:v for k, v in locals().items() if k.isupper()}
def load_settings(custom_settings={}):
    settings = _default_settings.copy()
    settings.update(custom_settings)
    return settings
