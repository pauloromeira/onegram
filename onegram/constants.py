DEFAULT_HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US',
}

QUERY_HEADERS = {
    'Host': 'www.instagram.com',
    'Referer': 'https://www.instagram.com/',
    'X-Requested-With': 'XMLHttpRequest'
}

ACTION_HEADERS = {
    'Host': 'www.instagram.com',
    'Referer': 'https://www.instagram.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.instagram.com',
    'X-Instagram-AJAX': '1',
    'X-Requested-With': 'XMLHttpRequest'
}

COOKIES = {
    'ig_vw': '1440',
    'ig_pr': '2',
    'ig_vh': '800',
    'ig_or': 'landscape-primary',
}

URLS = {
    'start': 'https://www.instagram.com/',
    'login': 'https://www.instagram.com/accounts/login/ajax/',
    'user_info': 'https://www.instagram.com/{username}/'.format,
    'follow': ('https://www.instagram.com/web/'
               'friendships/{user_id}/follow/').format,
    'unfollow': ('https://www.instagram.com/web/'
                 'friendships/{user_id}/unfollow/').format,
    'graphql': 'https://www.instagram.com/graphql/query/',
    'like': 'https://www.instagram.com/web/likes/{post_id}/like/'.format,
    'unlike': 'https://www.instagram.com/web/likes/{post_id}/unlike/'.format,
    'comment': 'https://www.instagram.com/web/comments/{post_id}/add/'.format,
    'uncomment': ('https://www.instagram.com/web/comments/'
                  '{post_id}/delete/{commentary_id}/'.format),
    'save': 'https://www.instagram.com/web/save/{post_id}/save/'.format,
    'unsave': 'https://www.instagram.com/web/save/{post_id}/unsave/'.format,
}

# TODO [romeira]: get from Consumer.js {27/02/18 19:52}
QUERY_HASHES = {
    'followers': '37479f2b8209594dde7facb0d904896a',
    'following': '58712303d941c6855d4e888c5f0cd22f',
    'posts': '472f257a40c653c64c666ce877d59d2b',

    # TODO [romeira]: Implement {27/02/18 23:26}
    'feed': '885c6a457b80f0e329bbc9389cf21f0b',
    'explore': 'df0dcc250c2b18d9fd27c5581ef33c7c',
    'suggested_users': '58fef9d690135e575980c97d9abe776a',
}
