import json
import logging
import jmespath

from itertools import chain
from itertools import repeat as iter_repeat
from functools import partial
from collections import deque
from time import monotonic as now
from time import sleep

from random import uniform
from random import choice
from requests import Response

logger = logging.getLogger(__name__)


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


class RateLimiter:
    def __init__(self, session):
        self.session = session
        rate_limits = session.settings.get('RATE_LIMITS', {})
        self.rates = {}
        for key, limits in rate_limits.items():
            self.rates[key] = _RateController(limits)

    def __enter__(self):
        self._current_keys = ('*', self.session.current_module_name,
                              self.session.current_function_name)
        self.wait(self._current_keys)

    def __exit__(self, *exc_info):
        self.done(self._current_keys)

    def wait(self, keys):
        for key in keys:
            if key in self.rates:
                self.rates[key].wait()

    def done(self, keys):
        end = now()
        for key in keys:
            if key in self.rates:
                self.rates[key].done(end)


class _RateController:
    def __init__(self, limits):
        self.windows = [(deque(maxlen=times), secs) for times, secs in limits]

    def wait(self):
        for queue, secs in self.windows:
            if len(queue) == queue.maxlen:
                sleep(max(queue[0] + secs - now(), 0))

    def done(self, end):
        for queue, _ in self.windows:
            queue.append(end)
