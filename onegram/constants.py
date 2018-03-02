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

_graphql = 'https://www.instagram.com/graphql/query/'
URLS = {
    'start': 'https://www.instagram.com/',
    'login': 'https://www.instagram.com/accounts/login/ajax/',
    'user_info': 'https://www.instagram.com/{username}/'.format,
    'followers': _graphql,
    'following': _graphql,
    'posts': _graphql,
    'explore': _graphql,
    'follow': ('https://www.instagram.com/web/'
               'friendships/{user_id}/follow/').format,
    'unfollow': ('https://www.instagram.com/web/'
                 'friendships/{user_id}/unfollow/').format,
    'like': 'https://www.instagram.com/web/likes/{post_id}/like/'.format,
    'unlike': 'https://www.instagram.com/web/likes/{post_id}/unlike/'.format,
    'comment': 'https://www.instagram.com/web/comments/{post_id}/add/'.format,
    'uncomment': ('https://www.instagram.com/web/comments/'
                  '{post_id}/delete/{commentary_id}/'.format),
    'save': 'https://www.instagram.com/web/save/{post_id}/save/'.format,
    'unsave': 'https://www.instagram.com/web/save/{post_id}/unsave/'.format,
    'post_info': 'https://www.instagram.com/p/{shortcode}/'.format,
}

# TODO [romeira]: get from Consumer.js {27/02/18 19:52}
QUERY_HASHES = {
    'followers': '37479f2b8209594dde7facb0d904896a',
    'following': '58712303d941c6855d4e888c5f0cd22f',
    'posts': '472f257a40c653c64c666ce877d59d2b',
    'explore': 'df0dcc250c2b18d9fd27c5581ef33c7c',
}

JSPATHS = {
    '_nodes': 'edges[].node',
    'posts': 'data.user.edge_owner_to_timeline_media',
    'following': 'data.user.edge_follow',
    'followers': 'data.user.edge_followed_by',
    'user_info': 'graphql.user',
    'explore': 'data.user.edge_web_discover_media',
    'post_info': 'graphql.shortcode_media',
}
