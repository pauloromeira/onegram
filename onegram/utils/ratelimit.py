import json

from collections import deque, defaultdict
from json import JSONEncoder, JSONDecoder
from time import monotonic as now
from time import sleep
from pathlib import Path


class RateLimiter:
    def __init__(self, session):
        self.session = session
        self.cache_enabled = session.settings.get('RATE_CACHE_ENABLED', False)
        self.cache_dir = session.settings.get('RATE_CACHE_DIR', Path('.cache'))

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

        if self.cache_enabled:
            self.dump()

    def dump(self):
        path = self.cache_dir / f'{self.session.username}'
        path.parent.mkdir(parents=True, exist_ok=True)
        open(path, 'w').write(json.dumps(self, cls=_RateLimiterJSONEncoder))


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


class _RateLimiterJSONEncoder(JSONEncoder):
    def default(self, o):
        rates = defaultdict(dict)
        for key, controller in o.rates.items():
            for queue, secs in controller.windows:
                if queue:
                    rates[key][f'{queue.maxlen}/{secs}'] = list(queue)
        return rates
