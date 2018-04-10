import json
import logging
import jmespath

from itertools import chain
from itertools import repeat as iter_repeat
from functools import partial

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

def repeat(*a, **kw):
    return partial(iter_repeat, *a, **kw)
    
def choices(seq):
    def _choices():
        while True:
            yield choice(seq)
    return _choices

def head_tail(head, tail):
    return partial(chain, [head], iter_repeat(tail))
