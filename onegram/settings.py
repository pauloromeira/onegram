import yaml

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__)


def load_settings(file=None, custom={}):
    settings = _load_yaml(BASE_DIR / 'default-settings.yaml')
    if file:
        settings.update(_load_yaml(Path(file)))
    settings.update(custom)
    return settings


def _load_yaml(path):
    return yaml.load(path.open()) if path.exists() else {}


## DEPRECATED

# USERNAME = config('INSTA_USERNAME', default=None)
# PASSWORD = config('INSTA_PASSWORD', default=None)

# # Leave it commented to fetch a random User-Agent
# # USER_AGENT = None

# DEBUG = config('INSTA_DEBUG', default=False, cast=bool)
# VERIFY_SSL = config('VERIFY_SSL', default=True, cast=bool)

# # Limits requests per second
# RATE_LIMITS = {
#     'all': [(1, 1)],
#     'actions': [(1, 2)],
# }

# RATE_PERSIST = {
#     'enabled': True,
#     'directory': CURRENT_DIR / '.onegram/rates'
# }

# LOG_SETTINGS = {
#     'format': '%(levelname)s:%(name)s: %(message)s',
#     'level': logging.DEBUG if DEBUG else logging.INFO,
# }

# QUERY_CHUNKS = {
#     'following': (20, 10),
#     'followers': (20, 10),
#     'posts': 12,
#     'feed': 12,
#     'likes': (20, 10),
#     'comments': choices(range(20, 40)),
#     'explore': 24,
# }
