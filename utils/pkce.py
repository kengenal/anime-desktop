import random
import string
from typing import Tuple


class PKCE:
    @staticmethod
    def code_verifier(self) -> Tuple[str, int]:
        rand = random.SystemRandom()
        code_verifier = "".join(
            rand.choices(string.ascii_letters + string.digits, k=90)
        )

        return str(code_verifier), len(code_verifier)
