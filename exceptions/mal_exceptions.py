class MalLoginException(Exception):
    value = "Something goes wrong"


class MalAuthorizationException(Exception):
    value = "Refresh token expired"
