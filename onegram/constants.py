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
}
