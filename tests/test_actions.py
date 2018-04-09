from onegram import follow, unfollow
from onegram import like, unlike
from onegram import comment, uncomment
from onegram import save, unsave


def test_follow(user, cassette):
    response = follow(user)
    assert response == {'result': 'following',
                        'status': 'ok',
                        'user_id': user['id']}

    response = unfollow(user)
    assert response == {'status': 'ok', 'user_id': user['id']}


def test_like(post, cassette):
    response = like(post)
    assert response == {'status': 'ok', 'post_id': post['id']}

    response = unlike(post)
    assert response == {'status': 'ok', 'post_id': post['id']}


def test_comment(post, cassette):
    text = 'awesome!'
    commentary = comment(text, post)
    assert commentary['id']
    assert commentary['text'] == text
    assert commentary['status'] == 'ok'
    assert commentary['post_id'] == post['id']

    response = uncomment(commentary)
    assert response == {'status': 'ok', 'post_id': post['id']}


def test_save(post, cassette):
    response = save(post)
    assert response == {'status': 'ok', 'post_id': post['id']}

    response = unsave(post)
    assert response == {'status': 'ok', 'post_id': post['id']}
