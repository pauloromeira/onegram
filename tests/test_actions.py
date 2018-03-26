from onegram.actions import follow, unfollow
from onegram.actions import like, unlike
from onegram.actions import comment, uncomment
from onegram.actions import save, unsave


def test_follow(session, user):
    response = follow(user)
    assert response == {'result': 'following',
                        'status': 'ok',
                        'user_id': user['id']}

    response = unfollow(user)
    assert response == {'status': 'ok', 'user_id': user['id']}


def test_like(session, post):
    response = like(post)
    assert response == {'status': 'ok', 'post_id': post['id']}

    response = unlike(post)
    assert response == {'status': 'ok', 'post_id': post['id']}


def test_comment(session, post):
    text = 'awesome!'
    commentary = comment(text, post)
    assert commentary['id']
    assert commentary['from']['username'] == session.username
    assert commentary['text'] == text
    assert commentary['status'] == 'ok'
    assert commentary['post_id'] == post['id']

    response = uncomment(commentary)
    assert response == {'status': 'ok', 'post_id': post['id']}


def test_save(session, post):
    response = save(post)
    assert response == {'status': 'ok', 'post_id': post['id']}

    response = unsave(post)
    assert response == {'status': 'ok', 'post_id': post['id']}
