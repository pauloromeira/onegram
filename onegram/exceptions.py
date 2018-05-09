class OnegramException(Exception):
    pass

# TODO [romeira]: Login exceptions {06/03/18 23:07}
class AuthException(OnegramException):
    pass

class AuthFailed(AuthException):
    pass

class AuthUserError(AuthException):
    pass

class NotSupportedError(OnegramException):
    pass

class RequestFailed(OnegramException):
    pass

class RateLimitedError(RequestFailed):
    pass


# TODO [romeira]: Query/action exceptions {06/03/18 23:08}
# TODO [romeira]: Session expired exception {06/03/18 23:08}
# TODO [romeira]: Private user exception/warning {06/03/18 23:09}
# TODO [romeira]: Not found exception {06/03/18 23:12}
# TODO [romeira]: Already following/liked/commented? warnings {06/03/18 23:12}
# TODO [romeira]: Timeout exception {06/03/18 23:12}
