#!/usr/bin/env python

from onegram import Insta
from onegram.queries import user


with Insta():
    me = user()
    other = user('other')
