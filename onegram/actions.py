import json
import logging

from .queries import user_info
from .session import sessionaware
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


@sessionaware
def comment(session, commentary, post=None):
    post_id = post['id'] if isinstance(post, dict) else post
    comment_text = (commentary['text'] if 
                     isinstance(commentary, dict) else commentary)

    if post_id is None:
        try:
            post_id = commentary['post_id']
        except (TypeError, KeyError):
            raise ValueError('Post id is missing')

    url = URLS['comment'](post_id=post_id)
    payload = {'comment_text': comment_text}

    data = session.action(url, data=payload)
    data['post_id'] = post_id
    return data


@sessionaware
def uncomment(session, commentary, post=None):
    post_id = post['id'] if isinstance(post, dict) else post
    commentary_id = (commentary['id'] if 
                     isinstance(commentary, dict) else commentary)

    if post_id is None:
        try:
            post_id = commentary['post_id']
        except (TypeError, KeyError):
            raise ValueError('Post id is missing')

    url = URLS['uncomment'](post_id=post_id, commentary_id=commentary_id)
    return session.action(url)


@sessionaware
def save(session, post):
    post_id = post['id'] if isinstance(post, dict) else post

    url = URLS['save'](post_id=post_id)
    return session.action(url)


@sessionaware
def unsave(session, post):
    post_id = post['id'] if isinstance(post, dict) else post

    url = URLS['unsave'](post_id=post_id)
    return session.action(url)
