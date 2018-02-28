import json
import logging

from sessionlib import sessionaware

from .queries import user_info
from .constants import URLS

logger = logging.getLogger(__name__)


@sessionaware
def follow(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    url = URLS['follow'](user_id=user_id)
    return session.action(url)


@sessionaware
def unfollow(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    url = URLS['unfollow'](user_id=user_id)
    return session.action(url)


@sessionaware
def like(session, post):
    post_id = post['id'] if isinstance(post, dict) else post

    url = URLS['like'](post_id=post_id)
    return session.action(url)

@sessionaware
def unlike(session, post):
    post_id = post['id'] if isinstance(post, dict) else post

    url = URLS['unlike'](post_id=post_id)
    return session.action(url)
