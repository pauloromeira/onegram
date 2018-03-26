from onegram.actions import follow, unfollow


def test_follow(session, user):
    response = follow(user)
    assert response == {'result': 'following',
                        'status': 'ok',
                        'user_id': user['id']}

    response = unfollow(user)
    assert response == {'status': 'ok',
                        'user_id': user['id']}
