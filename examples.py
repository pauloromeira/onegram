#!/usr/bin/env python

from operator import itemgetter
from itertools import islice
from collections import defaultdict

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


# Top likers
def likes_rank(user=None):
    rank = defaultdict(int)

    for post in posts(user):
        for like in likes(post):
            username = like['username']
            rank[username] += 1

    return sorted(rank.items(), key=itemgetter(1), reverse=True)


with Login():
    rank = likes_rank()
