import json
import logging

from sessionlib import sessionaware

from .constants import URLS, GRAPHQL_URL
from .constants import QUERY_HASHES, JSPATHS
from .utils import jsearch

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
    shortcode = post['shortcode'] if isinstance(post, dict) else shortcode

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

    yield from _iterate(session, 'followers', variables)


@sessionaware
def following(session, user=None):
    user = user or session.username
    if isinstance(user, dict):
        user_id = user['id']
    else:
        user_id = user_info(session, user)['id']

    variables = {'id': user_id}

    yield from _iterate(session, 'following', variables)


@sessionaware
def posts(session, user=None):
    user = user or session.username
    if not isinstance(user, dict):
        user = user_info(session, user)

    data = user['edge_owner_to_timeline_media']
    variables = {'id': user['id']}

    yield from _iterate(session, 'posts', variables, data)


@sessionaware
def likes(session, post):
    shortcode = post['shortcode'] if isinstance(post, dict) else shortcode
    variables =  {'shortcode': shortcode}

    yield from _iterate(session, 'likes', variables)


@sessionaware
def comments(session, post):
    shortcode = post['shortcode'] if isinstance(post, dict) else shortcode
    variables = {'shortcode': shortcode}

    yield from _iterate(session, 'comments', variables)


@sessionaware
def explore(session):
    yield from _iterate(session, 'explore')



def _iterate(session, query, variables={}, data=None):
    chunks = session.settings['QUERY_CHUNKS'][query]()

    variables['first'] = next(chunks)
    params = {'query_hash': QUERY_HASHES[query]}
    jspath = JSPATHS[query]

    if not data:
        params['variables'] = json.dumps(variables)
        response = session.query(GRAPHQL_URL, params=params)
        data = jsearch(jspath, response)

    yield from jsearch(JSPATHS['_nodes'], data)
    page_info = data['page_info']

    if not page_info['has_next_page']:
        return

    while page_info['has_next_page']:
        variables['first'] = next(chunks)
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(GRAPHQL_URL, params=params)
        data = jsearch(jspath, response)
        yield from jsearch(JSPATHS['_nodes'], data)

        page_info = data['page_info']

