import json
import logging

from .session import sessionaware
from .utils import jsearch
from .constants import QUERY_HASHES, JSPATHS
from .constants import URLS, GRAPHQL_URL

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
    shortcode = post['shortcode'] if isinstance(post, dict) else post

    url = URLS['post_info'](shortcode=shortcode)

    params = {'__a': '1'}
    response = session.query(url, params=params)

    return jsearch(JSPATHS['post_info'], response)


@sessionaware
def followers(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    variables = {'id': user_id}

    yield from _iterate(session, variables)


@sessionaware
def following(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    variables = {'id': user_id}

    yield from _iterate(session, variables)


@sessionaware
def posts(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    variables = {'id': user_id}

    yield from _iterate(session, variables)


@sessionaware
def likes(session, post):
    shortcode = post['shortcode'] if isinstance(post, dict) else post
    variables =  {'shortcode': shortcode}

    yield from _iterate(session, variables)


@sessionaware
def comments(session, post):
    shortcode = post['shortcode'] if isinstance(post, dict) else post
    variables = {'shortcode': shortcode}

    yield from _iterate(session, variables)


@sessionaware
def feed(session):
    yield from _iterate(session, chunk_key='fetch_media_item_count',
                                 cursor_key='fetch_media_item_cursor')

@sessionaware
def explore(session):
    yield from _iterate(session)


def _iterate(session, variables={}, chunk_key='first', cursor_key='after'):
    # TODO [romeira]: make it prettier {09/03/18 00:03}
    query = session.current_function.__name__

    chunks = session.settings['QUERY_CHUNKS'][query]()
    jspath = JSPATHS[query]
    params = {'query_hash': QUERY_HASHES[query]}

    variables[chunk_key] = next(chunks)
    params['variables'] = json.dumps(variables)

    response = session.query(GRAPHQL_URL, params=params)
    data = jsearch(jspath, response)
    yield from jsearch(JSPATHS['_nodes'], data)

    page_info = data['page_info']

    while page_info['has_next_page']:
        variables[chunk_key] = next(chunks)
        variables[cursor_key] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(GRAPHQL_URL, params=params)
        data = jsearch(jspath, response)
        yield from jsearch(JSPATHS['_nodes'], data)

        page_info = data['page_info']

