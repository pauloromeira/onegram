import pytest

from onegram.exceptions import NotSupportedError

from onegram import follow, unfollow
from onegram import like, unlike
from onegram import comment, uncomment
from onegram import save, unsave


def test_follow(logged, user, cassette):
    if logged:
        response = follow(user)
        assert response == {'result': 'following',
                            'status': 'ok',
                            'user_id': user['id']}

        response = unfollow(user)
        assert response == {'status': 'ok', 'user_id': user['id']}
    else:
        with pytest.raises(NotSupportedError):
            follow(user)
        with pytest.raises(NotSupportedError):
            unfollow(user)


def test_like(logged, post, cassette):
    if logged:
        response = like(post)
        assert response == {'status': 'ok', 'post_id': post['id']}

        response = unlike(post)
        assert response == {'status': 'ok', 'post_id': post['id']}
    else:
        with pytest.raises(NotSupportedError):
            like(post)
        with pytest.raises(NotSupportedError):
            unlike(post)


def test_comment(logged, post, cassette):
    text = 'awesome!'
    if logged:
        commentary = comment(text, post)
        assert commentary['id']
        assert commentary['text'] == text
        assert commentary['status'] == 'ok'
        assert commentary['post_id'] == post['id']

        response = uncomment(commentary)
        assert response == {'status': 'ok', 'post_id': post['id']}
    else:
        with pytest.raises(NotSupportedError):
            comment(text, post)
        with pytest.raises(NotSupportedError):
            fake_comment = {'id': '1', 'post_id': '2'}
            uncomment(fake_comment)



def test_save(logged, post, cassette):
    if logged:
        response = save(post)
        assert response == {'status': 'ok', 'post_id': post['id']}

        response = unsave(post)
        assert response == {'status': 'ok', 'post_id': post['id']}
    else:
        with pytest.raises(NotSupportedError):
            save(post)
        with pytest.raises(NotSupportedError):
            unsave(post)
