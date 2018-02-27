import logging

from decouple import config


USERNAME = config('USERNAME', default=None)
PASSWORD = config('PASSWORD', default=None)

SSL_INSECURE = True

# USER_AGENT = 'fake-useragent'

DEFAULT_HEADERS = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US',
}

QUERY_HEADERS = {
    'Host': 'www.instagram.com',
    'X-Requested-With': 'XMLHttpRequest'
}

ACTION_HEADERS = {
    'Host': 'www.instagram.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.instagram.com',
    'X-CSRFToken': 'csrftoken', # Fill with cookie
    'X-Instagram-AJAX': '1',
    'X-Requested-With': 'XMLHttpRequest'
}

LOG_SETTINGS = {
    'format': '%(levelname)s:%(name)s:%(funcName)s:%(message)s',
    'level': logging.INFO,
}
