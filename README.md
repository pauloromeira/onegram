# onegram
[![Travis](https://travis-ci.org/pauloromeira/onegram.svg?branch=master)](https://travis-ci.org/pauloromeira/onegram)
[![Pypi](https://img.shields.io/pypi/v/onegram.svg)](https://pypi.python.org/pypi/onegram)

A simplistic api-like instagram **bot** powered by [requests](https://github.com/requests/requests).

### *Warnings!*
* If not working, make sure you have the last version installed. Things often change!
* Default rate limits are not configured properly, so [adjust them](#rate-limits) to not get banned!

## Installation
```sh
pip install onegram
```

### Dependencies
Python 3.6

## Examples
#### Follow me :wink:
```py
from onegram import follow

follow('<me>')
```

#### Like all my posts :joy:

```py
from onegram import like, posts

for post in posts('<me>'):
  like(post)
```

#### Who likes you most? :open_mouth:
```py
from collections import defaultdict
from operator import itemgetter

from onegram import posts, likes

rank = defaultdict(int)
for post in posts():
    for like_info in likes(post):
        username = like_info['username']
        rank[username] += 1

rank = sorted(rank.items(), key=itemgetter(1), reverse=True)

print(rank[:10]) # TOP 10!
```

#### Explicit login (optional)
```py
from onegram import Login, posts

with Login(username='user', password='pass'):
  user_posts = list(posts())
  other_posts = list(posts('other'))
```

##### Also possible
```py
from onegram import *

login()

last_post = next(posts())
post_likes = list(likes(last_post))

logout()
```

## Cheatsheet
The set of functions are divided into queries and actions. For some queries
the user is optional, with default set to the logged user.

|Query|Argument(s)||Action|Argument(s)|
|-|-|-|-|-|
|`user_info`|`[user]`||`follow`|`user`|
|`followers`|`[user]`||`unfollow`|`user`|
|`following`|`[user]`||`like`|`post`|
|`posts`|`[user]`||`unlike`|`post`|
|`post_info`|`post`||`comment`|`comment[, post]`|
|`likes`|`post`||`uncomment`|`comment[, post]`|
|`comments`|`post`||`save`|`post`|
|`feed`|||`unsave`|`post`|
|`explore`|||||

## Rate Limits
Settings can be overridden if you use one of the [explicit login](#explicit-login-optional) forms (defaults: `onegram/settings.py`). It's possible to define a fixed `User-Agent`, for example.
Overall, the most userful setting is `RATE_LIMITS`, where you can set rate limits for:
1. Each query or action
2. All queries or all actions
3. All queries and actions

#### Example
```py
from onegram import login

minute = 60
hour = minute * 60
day = hour * 24

rate_limits = {
  'queries': [(1, 1)], # One query per second
  'actions': [(1, 3)], # One action per 3 seconds
  'like': [
    (5, minute), # A maximum of 5 likes in a minute
    (100, day)   # A maximum of 100 likes in a day
  ],
  'comment': [(1, 5)], # One comment per 5 seconds
}
# You can use '*' to set limits for all queries and actions.

settings = {
  'RATE_LIMITS': rate_limits,
  'RATE_CACHE_ENABLED': True, # enabled by default
  'RATE_CACHE_DIR': '~/.onegram/rate'
}

login(custom_settings=settings)
# ...
```

Notice that you can specify a greedy or patient behaviour, or both. This is possible because you can have different rates for different time intervals.

For example, both `(10, 10)` and `(1, 1)` will do 10 requests in 10 seconds, but the first
one is greedy. It will make 10 requests and wait 10 seconds to continue, whereas the second one will make one request at each second.

As general rule:

Greedy = `(times, seconds)`  
Patient = `(1, seconds/times)`

## Tips
  * Export your credentials so you don't have to type it:
    ```sh
    export INSTA_USERNAME=username
    export INSTA_PASSWORD=password
    ```
