import json
import jmespath

from functools import partial
from itertools import chain
from itertools import repeat
from random import randint

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


# TODO [romeira]: move to chunks module {28/03/18 02:00}
def repeat_last(values):
    if not isinstance(values, (list, tuple)):
        values = [values]
    return partial(chain, values, repeat(values[-1]))


def random_int(values):
    def _randint():
        while True:
            yield randint(*values)
    return _randint
