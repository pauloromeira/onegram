#!/usr/bin/env python

from itertools import islice

from onegram import Insta
from onegram.queries import user_info, followers, following
from onegram.actions import follow, unfollow


with Insta():
    some_following = list(islice(following(), 30))
