from .constants import URLS
from .session import sessionaware
from .queries import _user_id, _post_id


@sessionaware
def follow(session, user):
    return _user_action(session, user)

@sessionaware
def unfollow(session, user):
    return _user_action(session, user)

@sessionaware
def like(session, post):
    return _post_action(session, post)

@sessionaware
def unlike(session, post):
    return _post_action(session, post)

@sessionaware
def comment(session, commentary, post=None):
    comment_text = (commentary['text'] if 
                    isinstance(commentary, dict) else commentary)
    payload = {'comment_text': comment_text}
    return _post_action(session, post or commentary, payload=payload)

@sessionaware
def uncomment(session, commentary, post=None):
    comment_id = (commentary['id'] if 
                  isinstance(commentary, dict) else commentary)
    return _post_action(session, post or commentary, comment_id=comment_id)

@sessionaware
def save(session, post):
    return _post_action(session, post)

@sessionaware
def unsave(session, post):
    return _post_action(session, post)


#######################################################################
#                               HELPERS                               #
#######################################################################

def _user_action(session, user, **kw):
    user_id = _user_id(session, user)
    data = _action(session, user_id=user_id, **kw)
    data['user_id'] = user_id
    return data

def _post_action(session, post, **kw):
    post_id = _post_id(post)
    data = _action(session, post_id=post_id, **kw)
    data['post_id'] = post_id
    return data

def _action(session, payload={}, **kw):
    action = session.current_function_name
    url = URLS[action](**kw)
    return session.action(url, data=payload)
