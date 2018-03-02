#!/usr/bin/env python

from itertools import islice

from onegram import Login

from onegram.queries import user_info, post_info
from onegram.queries import followers, following
from onegram.queries import posts, explore

from onegram.actions import follow, unfollow
from onegram.actions import like, unlike
from onegram.actions import comment, uncomment
from onegram.actions import save, unsave

with Login():
    p = next(posts())
    p_info = post_info(p)
