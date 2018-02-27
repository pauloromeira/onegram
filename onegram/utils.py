import time
import .settings as settings_module
from random import uniform


def load_settings(custom_settings={}):
    settings = {k:getattr(settings_module, k)
                for k in dir(settings_module) if k.isupper()}
    settings.update(custom_settings)
    return settings


def sleep(t, var=.5):
    time.sleep(uniform((1-var)*t, (1+var)*t))
