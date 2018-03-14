import logging

from .session import sessionaware
from .utils import jsearch
from ._utils import shortcode, user_id, iter_query
from .constants import JSPATHS, URLS

logger = logging.getLogger(__name__)


@sessionaware
def user_info(session, username=None):
    username = username or session.username

    url = URLS['user_info'](username=username)
    params = {'__a': '1'}
    response = session.query(url, params=params)

    return jsearch(JSPATHS['user_info'], response)


@sessionaware
def post_info(session, post=None):
    url = URLS['post_info'](shortcode=shortcode(post))
    params = {'__a': '1'}
    response = session.query(url, params=params)

    return jsearch(JSPATHS['post_info'], response)


@sessionaware
def followers(session, user=None):
    variables = {'id': user_id(session, user)}
    yield from iter_query(session, variables)


@sessionaware
def following(session, user=None):
    variables = {'id': user_id(session, user)}
    yield from iter_query(session, variables)


@sessionaware
def posts(session, user=None):
    variables = {'id': user_id(session, user)}
    yield from iter_query(session, variables)


@sessionaware
def likes(session, post):
    variables =  {'shortcode': shortcode(post)}
    yield from iter_query(session, variables)


@sessionaware
def comments(session, post):
    variables = {'shortcode': shortcode(post)}

    yield from iter_query(session, variables)


@sessionaware
def feed(session):
    yield from iter_query(session, chunk_key='fetch_media_item_count',
                                 cursor_key='fetch_media_item_cursor')


@sessionaware
def explore(session):
    yield from iter_query(session)

