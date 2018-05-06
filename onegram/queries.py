import json

from .session import sessionaware
from .utils import jsearch
from .constants import URLS, GRAPHQL_URL
from .constants import QUERY_HASHES, JSPATHS
from .exceptions import NotSupportedError


@sessionaware
def user_info(session, username=None):
    if session.unlogged and not username:
        raise NotSupportedError('You must provide an user at Unlogged state')
    return _info(session, username=username or session.username)

@sessionaware
def post_info(session, post):
    return _info(session, shortcode=_shortcode(post))

@sessionaware
def followers(session, user=None):
    if session.unlogged and not user:
        raise NotSupportedError('You must provide an user at Unlogged state')
    yield from _iter_user(session, user)

@sessionaware
def following(session, user=None):
    if session.unlogged and not user:
        raise NotSupportedError('You must provide an user at Unlogged state')
    yield from _iter_user(session, user)

@sessionaware
def posts(session, user=None):
    if session.unlogged and not user:
        raise NotSupportedError('You must provide an user at Unlogged state')
    yield from _iter_user(session, user)

@sessionaware
def likes(session, post):
    yield from _iter_post(session, post)

@sessionaware
def comments(session, post):
    yield from _iter_post(session, post)

@sessionaware
def feed(session):
    yield from _iter_query(session, chunk_key='fetch_media_item_count',
                                    cursor_key='fetch_media_item_cursor')

@sessionaware
def explore(session, tag=None):
    if tag:
        yield from explore_tag(session, tag)
    else:
        yield from _iter_query(session)

@sessionaware
def explore_tag(session, tag):
    variables = {'tag_name': tag}
    yield from _iter_query(session, variables)


#######################################################################
#                               HELPERS                               #
#######################################################################

def _user_id(session, user):
    if user is None:
        user_id = getattr(session, 'user_id', None)
        if user_id:
            return user_id
        else:
            user = session.username
    if isinstance(user, dict):
        user_id = user.get('user_id', user.get('id'))
        if user_id:
            return user_id
        else:
            user = user.get('username')
    if user is None:
        raise ValueError('Invalid user')

    return user_info(session, user)['id']

def _post_id(post):
    if isinstance(post, dict):
        return post.get('post_id', post.get('id'))
    else:
        return post

def _shortcode(post):
    return post['shortcode'] if isinstance(post, dict) else post


def _info(session, **kw):
    query = session.current_function_name
    url = URLS[query](**kw)
    params = {'__a': '1'}
    response = session.query(url, params=params)
    return jsearch(JSPATHS[query], response)

def _iter_user(session, user, *a, **kw):
    variables = {'id': _user_id(session, user)}
    yield from _iter_query(session, variables, *a, **kw)

def _iter_post(session, post, *a, **kw):
    variables =  {'shortcode': _shortcode(post)}
    yield from _iter_query(session, variables, *a, **kw)

def _iter_query(session, variables={}, chunk_key='first', cursor_key='after'):
    query = session.current_function_name
    progress = {'count': 0}

    chunks = session.settings['QUERY_CHUNKS'][query]()
    jspath = JSPATHS[query]
    params = {'query_hash': QUERY_HASHES[query]}

    variables[chunk_key] = next(chunks)
    params['variables'] = json.dumps(variables)

    response = session.query(GRAPHQL_URL, params=params)
    data = jsearch(jspath, response)
    _iter_progress(session, data, progress)
    yield from jsearch(JSPATHS['_nodes'], data)

    page_info = data['page_info']

    while page_info['has_next_page']:
        variables[chunk_key] = next(chunks)
        variables[cursor_key] = page_info['end_cursor']
        params['variables'] = json.dumps(variables)

        response = session.query(GRAPHQL_URL, params=params)
        data = jsearch(jspath, response)
        _iter_progress(session, data, progress)
        yield from jsearch(JSPATHS['_nodes'], data)

        page_info = data['page_info']

def _iter_progress(session, data, progress):
    total = progress.setdefault('total', data.get('count', 0))
    fetched = len(data.get('edges', []))
    count = progress['count'] + fetched

    if count < total and not fetched:
        query = session.current_function_name
        session.logger.warning(f'STOP :: No {query} available')
        raise StopIteration

    progress['fetched'] = fetched
    progress['count'] = count

    msg = f'FETCH {fetched} :: [{count}/{total}] - {count/(total or 1):.0%}'
    session.logger.info(msg)
