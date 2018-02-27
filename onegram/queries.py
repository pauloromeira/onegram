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
    return jsearch('user', response)

# TODO [romeira]: Refactor followers/following (almost the same) {27/02/18 20:27}
@sessionaware
def followers(session, username=None):
    username = username or session.username

    user = user_info(session, username)
    url = URLS['graphql']

    variables = {
        'id': user['id'],
        'first': 20,
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
        variables['first'] = 10
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

    variables = {
        'id': user['id'],
        'first': 20,
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
        variables['first'] = 10
        variables['after'] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(url, params=params)
        data = jsearch('data.user.edge_follow', response)
        yield from jsearch('edges[].node', data)

        page_info = data['page_info']

