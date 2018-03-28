import logging
import yaml

from pathlib import Path
from decouple import config

from .utils import repeat_last, choices

BASE_DIR = Path(__file__).parent


def load_settings(file=None, custom={}):
    settings = _load_yaml(BASE_DIR / 'default-settings.yml')
    settings.update(_load_env())
    if file:
        settings.update(_load_yaml(Path(file)))
    if custom:
        settings.update(custom)
    _parse(settings)
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


def _parse(settings):
    _parse_log(settings)
    _parse_query_chunks(settings)


def _parse_log(settings):
    log_settings = settings.get('log')
    if log_settings and 'level' not in log_settings:
        debug = settings.get('debug')
        log_settings['level'] = logging.DEBUG if debug else logging.INFO


_chunk_functions = {
    'choices': choices,
    'range': lambda values: range(*values),
    'repeat_last': repeat_last,
    'repeat': repeat_last,
}


def _parse_query_chunks(settings):
    query_chunks = settings.get('query_chunks', {})
    for key, value in query_chunks.items():
        if isinstance(value, dict):
            try:
                query_chunks[key] = _complex_chunk(value)
            except:
                raise ValueError(f'Invalid "{key}" query chunk value')
        else:
            query_chunks[key] = repeat_last(value)


def _complex_chunk(value):
    if not isinstance(value, dict):
        return value

    if len(value) == 1:
        fn, args = value.popitem()
        return _chunk_functions[fn](_complex_chunk(args))
    else:
        raise ValueError
