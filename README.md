# onegram

A simplistic api-like instagram bot powered by [requests](https://github.com/requests/requests).

#### Example:
```py
from onegram import Insta
from onegram.actions import follow
from onegram.queries import followers


with Insta(username='user', password='pswd'):
    user_followers = list(followers())
    print(user_followers)

    follow('<me>') # Follow me :)
```
