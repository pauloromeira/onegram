#!/usr/bin/env python

from itertools import islice

from onegram import Insta
from onegram.queries import user_info, followers, following, posts
from onegram.actions import follow, unfollow, like, unlike


with Insta():
    post = next(posts())
    unlike(post)
