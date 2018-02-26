# onegram

A simplistic api-like instagram bot.

#### Example:
```py
from onegram import Insta
from onegram.actions import followers, follow


with Insta(username='user', password='pswd'):
    user_followers = followers()
    print(user_followers)

    follow('<me>') # Follow me :)
```
