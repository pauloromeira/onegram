# onegram

A simplistic api-like instagram bot powered by [requests](https://github.com/requests/requests).

#### Example:
```py
from onegram import follow

follow('<me>') # Follow me :)
```

#### Explicit login:
```py
from onegram import Login
from onegram import posts

with Login(username='user', password='pass'):
  my_posts = list(posts())
  other_posts = list(posts('other'))
```

#### Also possible:
```py
from onegram import login, logout
from onegram import posts, likes

login()

first_post = next(posts())
post_likes = list(likes(first_post))

logout()
```
