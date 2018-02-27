#!/usr/bin/env python

from itertools import islice

from onegram import Insta
from onegram.queries import user_info, followers
from onegram.actions import follow, unfollow


with Insta():
    some_followers = list(islice(followers(), 30))
