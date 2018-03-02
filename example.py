#!/usr/bin/env python

from itertools import islice

from onegram import Login

# Queries
from onegram import user_info, post_info
from onegram import followers, following
from onegram import posts, likes, comments
from onegram import explore

# Actions
from onegram import follow, unfollow
from onegram import like, unlike
from onegram import comment, uncomment
from onegram import save, unsave


with Login():
    p = next(posts())
    for comment in comments(p):
        print(comment['text'])
