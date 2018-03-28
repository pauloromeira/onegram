import json
import logging
import jmespath

from functools import partial
from itertools import chain
from itertools import repeat
from random import choice

from requests import Response


def jsearch(jspath, content):
    if isinstance(content, dict):
        dct = content
    else:
        if isinstance(content, Response):
            text = content.text
        elif isinstance(content, str):
            text = content
        else:
            raise TypeError()
        dct = json.loads(text)

    return jmespath.search(jspath, dct)


def choices(values):
    def _choices():
        while True:
            yield choice(values)
    return _choices


def repeat_last(values):
    if not isinstance(values, (list, tuple)):
        values = [values]
    return partial(chain, values, repeat(values[-1]))
