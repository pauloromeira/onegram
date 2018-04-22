# onegram
[![pypi](https://img.shields.io/pypi/v/onegram.svg?style=flat-square)](https://pypi.python.org/pypi/onegram)
[![pyversions](https://img.shields.io/pypi/pyversions/onegram.svg?style=flat-square)](https://pypi.python.org/pypi/onegram)
[![travis](https://img.shields.io/travis/pauloromeira/onegram/master.svg?style=flat-square&logo=travis)](https://travis-ci.org/pauloromeira/onegram)
[![codecov](https://img.shields.io/codecov/c/github/pauloromeira/onegram/master.svg?style=flat-square)](https://codecov.io/gh/pauloromeira/onegram)
[![gitter](https://img.shields.io/gitter/room/pauloromeira/onegram.svg?style=flat-square&logo=gitter-white&colorB=ed1965&logoWidth=10)](https://gitter.im/pauloromeira/onegram)
[![license](https://img.shields.io/github/license/pauloromeira/onegram.svg?style=flat-square)](https://github.com/pauloromeira/onegram/blob/master/LICENSE)

A simplistic api-like instagram **bot** powered by [requests](https://github.com/requests/requests).

### *Warnings!*
* This isn't an official api. Use at your own risk. 
* Make sure you have the latest version installed. To update: `pip install -U onegram`.
* Default rate limits are not configured properly, so [adjust them](#rate-limits) to not get banned!

## Installation
```sh
pip install onegram
```

### Dependencies
Python 3.6

## Examples
#### Follow someone
```py
from onegram import follow

follow('<someone>')
```

#### Like all someone posts

```py
from onegram import like, posts

for post in posts('<someone>'):
  like(post)
```

#### Who likes you most?
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
  'RATE_PERSIST_ENABLED': True, # enabled by default
  'RATE_PERSIST_DIR': '.onegram/rates' # default directory
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
