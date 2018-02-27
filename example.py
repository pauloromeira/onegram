#!/usr/bin/env python

from onegram import Insta
from onegram.queries import user_info
from onegram.actions import follow


with Insta():
    follow('other')
    # me = user_info()
    # other = user_info('other')
