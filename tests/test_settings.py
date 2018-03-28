import random
import pytest
from itertools import islice

from onegram.settings import load_settings


@pytest.fixture(scope='module')
def settings():
    random.seed(0)
    return load_settings()


@pytest.mark.parametrize('key,expected', [
    ('following', [20, 10, 10]),
    ('followers', [20, 10, 10]),
    ('posts', [12, 12, 12]),
    ('feed', [12, 12, 12]),
    ('likes', [20, 10, 10]),
    ('comments', [32, 33, 21]),
    ('explore', [24, 24, 24]),
])
def test_query_chunks(settings, key, expected):
    query_chunks = settings['query_chunks']
    chunks = query_chunks[key]()
    result = list(islice(chunks, 3))
    assert result == expected
