#!/usr/bin/env python

from onegram import Insta

from onegram.queries import user_info
from onegram.queries import followers, following
from onegram.queries import posts

from onegram.actions import follow, unfollow
from onegram.actions import like, unlike
from onegram.actions import comment, uncomment
from onegram.actions import save, unsave


with Insta():
    post = next(posts())
    save(post)
    unsave(post)
