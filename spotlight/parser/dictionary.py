from dictionary_client import DictionaryClient

from .base import Parser


class DictClientParser(Parser):
    """Performs a dictionary lookup of the input."""

    HOSTNAME = "dict.org"

    def __init__(self):
        pass

    def parse(self, parse: str) -> str:
        raise NotImplementedError

    def lookup(self, word: str):
        client = DictionaryClient(self.HOSTNAME)
        return client.define(word)
