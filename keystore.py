from getpass import getpass

from utils import sha256


class Keystore:

    def __init__(self, source=False):
        if not source:
            source = getpass(prompt="Enter your password: ", stream=None)
        self._base_key = sha256(source)
        self._encoded_key = sha256(source).encode('ISO-8859-1')
        self._key = self._encoded_key[0:32]
        self._leftover_key = self._encoded_key[32:]

    @property
    def base_key(self):
        return self._base_key

    @property
    def encoded_key(self):
        return self._encoded_key

    @property
    def key(self):
        return self._key

    @property
    def leftover_key(self):
        return self._encoded_key[32:]
