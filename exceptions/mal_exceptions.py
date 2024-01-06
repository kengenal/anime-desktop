class MalLoginException(Exception):
    value = "Something goes wrong"


class MalAuthorizationException(Exception):
    value = "Refresh token expired"


class MalApiException(Exception):
    def __init__(self, status_code: int):
        self.value = f"Something goes wrong api raise exception with {str(status_code)} status code"
