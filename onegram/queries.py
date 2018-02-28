import json
import logging

from sessionlib import sessionaware

from .constants import URLS, QUERY_HASHES
from .utils import jsearch

logger = logging.getLogger(__name__)


@sessionaware
def user_info(session, username=None):
    username = username or session.username

    url = URLS['user_info'](username=username)
    params = {'__a': '1'}
    response = session.query(url, params=params)

    logger.debug(response.text)
    return jsearch('graphql.user', response)


# TODO [romeira]: username -> user (can be a dict) {27/02/18 23:14}
# TODO [romeira]: Refactor followers/following (almost the same) {27/02/18 20:27}
@sessionaware
def followers(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    url = URLS['graphql']

    chunks = session.settings['QUERY_CHUNKS']

    variables = {
        'id': user['id'],
        'first': chunks['follow_head'],
    }
    params = {
        'query_hash': QUERY_HASHES['followers'],
        'variables': json.dumps(variables),
    }

    response = session.query(url, params=params)
    data = jsearch('data.user.edge_followed_by', response)
    yield from jsearch('edges[].node', data)

    page_info = data['page_info']
    while page_info['has_next_page']:
        variables['first'] = chunks['follow_tail']
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(url, params=params)
        data = jsearch('data.user.edge_followed_by', response)
        yield from jsearch('edges[].node', data)

        page_info = data['page_info']


@sessionaware
def following(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    url = URLS['graphql']

    chunks = session.settings['QUERY_CHUNKS']

    variables = {
        'id': user['id'],
        'first': chunks['follow_head'],
    }
    params = {
        'query_hash': QUERY_HASHES['following'],
        'variables': json.dumps(variables),
    }

    response = session.query(url, params=params)
    data = jsearch('data.user.edge_follow', response)
    yield from jsearch('edges[].node', data)

    page_info = data['page_info']
    while page_info['has_next_page']:
        variables['first'] = chunks['follow_tail']
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(url, params=params)
        data = jsearch('data.user.edge_follow', response)
        yield from jsearch('edges[].node', data)

        page_info = data['page_info']


# TODO [romeira]: username -> user (can be a dict) {27/02/18 23:14}
@sessionaware
def posts(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    url = URLS['graphql']

    data = user['edge_owner_to_timeline_media']
    yield from jsearch('edges[].node', data)

    page_info = data['page_info']
    if not page_info['has_next_page']:
        return

    chunks = session.settings['QUERY_CHUNKS']

    variables = {
        'id': user['id'],
        'first': chunks['posts'],
    }
    params = {
        'query_hash': QUERY_HASHES['posts'],
    }

    while page_info['has_next_page']:
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(url, params=params)
        data = jsearch('data.user.edge_owner_to_timeline_media', response)
        yield from jsearch('edges[].node', data)

        page_info = data['page_info']
