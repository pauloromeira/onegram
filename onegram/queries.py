import json
import logging

from sessionlib import sessionaware

from .constants import URLS, QUERY_HASHES, JSPATH
from .utils import jsearch

logger = logging.getLogger(__name__)


@sessionaware
def user_info(session, username=None):
    username = username or session.username

    url = URLS['user_info'](username=username)
    params = {'__a': '1'}
    response = session.query(url, params=params)

    return jsearch(JSPATH['user_info'], response)


# TODO [romeira]: username -> user (can be a dict) {27/02/18 23:14}
# TODO [romeira]: Refactor followers/following (almost the same) {27/02/18 20:27}
@sessionaware
def followers(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    variables = {'id': user['id']}

    yield from _iterate(session, 'followers', variables)


@sessionaware
def following(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    variables = {'id': user['id']}

    yield from _iterate(session, 'following', variables)


# TODO [romeira]: username -> user (can be a dict) {27/02/18 23:14}
@sessionaware
def posts(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    data = user['edge_owner_to_timeline_media']
    variables = {'id': user['id']}

    yield from _iterate(session, 'posts', variables, data)


def _iterate(session, query, variables, data=None):
    url = URLS[query]
    chunks = session.settings['QUERY_CHUNKS']
    chunks_head = chunks.get(query + '_head') or chunks.get(query)
    chunks_tail = chunks.get(query)

    variables['first'] = chunks_head
    params = {'query_hash': QUERY_HASHES[query]}
    jspath = JSPATH[query]

    if not data:
        params['variables'] = json.dumps(variables)
        response = session.query(url, params=params)
        data = jsearch(jspath, response)

    yield from jsearch(JSPATH['_nodes'], data)
    page_info = data['page_info']

    if not page_info['has_next_page']:
        return

    variables['first'] = chunks_tail
    while page_info['has_next_page']:
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(url, params=params)
        data = jsearch(jspath, response)
        yield from jsearch(JSPATH['_nodes'], data)

        page_info = data['page_info']

