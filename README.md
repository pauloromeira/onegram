# onegram

A simplistic api-like instagram bot.

#### Example:
```py
from onegram import Insta
from onegram import follow, followers


with Insta(username='user', password='pswd'):
    user_followers = list(followers())
    print(user_followers)

    follow('<me>') # Follow me :)
```
