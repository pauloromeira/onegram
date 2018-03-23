from onegram.actions import follow, unfollow


def test_follow(session):
    follow('<me>')

def test_unfollow(session):
    unfollow('<me>')
