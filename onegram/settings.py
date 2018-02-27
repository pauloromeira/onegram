import logging

from decouple import config


USERNAME = config('INSTA_USERNAME', default=None)
PASSWORD = config('INSTA_PASSWORD', default=None)

SSL_INSECURE = True

# USER_AGENT = 'fake-useragent'

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s:%(funcName)s:%(message)s',
    'level': logging.INFO,
}
