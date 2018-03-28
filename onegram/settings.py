import yaml

from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).parent


def load_settings(file=None, custom={}):
    import ipdb; ipdb.set_trace()
    settings = _load_yaml(BASE_DIR / 'default-settings.yml')
    _merge(settings, _load_env())
    if file:
        _merge(settings, _load_yaml(Path(file)))
    if custom:
        _merge(settings, custom)
    return settings


def _load_yaml(path):
    for p in (path, path.with_suffix('.yml'), path.with_suffix('.yaml')):
        if p.exists():
            return yaml.load(p.open())
    return {}


def _load_env():
    settings = {
        'username': config('INSTA_USERNAME', default=None),
        'password': config('INSTA_PASSWORD', default=None),
        'debug': config('ONEGRAM_DEBUG', default=False, cast=bool),
        'verify_ssl': config('VERIFY_SSL', default=True, cast=bool),
    }
    return settings


def _merge(settings, other):
    if other:
        settings.update({k:v for k, v in other.items() if v is not None})





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
