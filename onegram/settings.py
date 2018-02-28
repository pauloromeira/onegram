import logging

from decouple import config


USERNAME = config('INSTA_USERNAME', default=None)
PASSWORD = config('INSTA_PASSWORD', default=None)

DEBUG = config('INSTA_DEBUG', default=False, cast=bool)

VERIFY_SSL = DEBUG is False

# Leave it commented to get a random User-Agent
# USER_AGENT = ''

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s:%(funcName)s:%(message)s',
    'level': logging.DEBUG if DEBUG else logging.INFO,
}

QUERY_CHUNKS = {
    'follow_head': 20,
    'follow_tail': 10,
    'posts': 12,
}
