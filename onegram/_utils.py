import json
from .utils import jsearch
from .constants import QUERY_HASHES, JSPATHS
from .constants import GRAPHQL_URL


def shortcode(post):
    return post['shortcode'] if isinstance(post, dict) else post


def user_id(session, user=None):
    if user is None:
        user_id = getattr(session, 'user_id', None)
        if user_id:
            return user_id
        else:
            user = session.username
    if isinstance(user, dict):
        return user['id']
    else:
        return user_info(session, user)['id']


def iter_query(session, variables={}, chunk_key='first', cursor_key='after'):
    query = session.current_function_name

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

