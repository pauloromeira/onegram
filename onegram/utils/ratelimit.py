import json

from collections import deque
from time import monotonic as now
from time import sleep
from pathlib import Path


class RateLimiter:
    def __init__(self, session):
        self.session = session

        rate_limits = session.settings.get('RATE_LIMITS')
        self.cache_enabled = session.settings.get('RATE_CACHE_ENABLED', False)
        self.rates = {}
        if rate_limits:
            for key, limits in rate_limits.items():
                self.rates[key] = _RateController(limits)

            if self.cache_enabled:
                cache_dir = session.settings.get('RATE_CACHE_DIR', Path('.cache'))
                self.cache_path = cache_dir / f'{self.session.username}'
                self.load()


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
        encoded = _json_encoder(self)
        if encoded:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(encoded))

    def load(self):
        if self.cache_path.exists():
            _json_decoder(self, json.loads(self.cache_path.read_text()))


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


def _json_encoder(manager):
    encoded = {}
    for key, control in manager.rates.items():
        window = max(control.windows, key=lambda w: len(w[0]))
        queue = window[0]
        if queue:
            encoded[key] = list(queue)
    return encoded


def _json_decoder(manager, encoded):
    for key, queue in encoded.items():
        if key in manager.rates:
            control = manager.rates[key]
            for window_queue, _ in control.windows:
                window_queue.extend(queue)
