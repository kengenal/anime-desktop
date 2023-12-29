import keyring


class SecureStore:
    def __init__(self):
        self.keyname = "anime"

    def set(self, key: str, value: str) -> None:
        keyring.set_password(self.keyname, key, value)

    def get(self, key: str) -> str:
        return keyring.get_password(self.keyname, key)

    def delete(self, key: str) -> None:
        keyring.delete_password(self.keyname, key)

    def exists(self, key: str) -> bool:
        get = keyring.get_password(self.keyname, key)
        if get:
            return True
        return False
