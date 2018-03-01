# onegram

A simplistic api-like instagram bot powered by [requests](https://github.com/requests/requests).

#### Example:
```py
from onegram import Login
from onegram import follow, followers


with Login(username='user', password='pswd'):
    my_followers = list(followers())
    print(my_followers)

    follow('<me>') # Follow me :)
```

#### Also possible:
```py
from onegram import login, logout
from onegram import posts

login(username='user', password='pswd')

my_posts = list(posts())

logout()
```
