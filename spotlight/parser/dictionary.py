from dictionary_client import DictionaryClient

from .base import AsyncParser


class DictClientParser(AsyncParser):
    """Performs a dictionary lookup of the input."""

    HOSTNAME = "dict.org"

    def __init__(self):
        super().__init__()

    def parse_sync(self, string: str) -> str:
        client = DictionaryClient(self.HOSTNAME)
        definition = client.define(string).content
        if definition is None:
            return f"No definitions found for {string}."
        ret = ""
        for defin in definition:
            ret += f"""
            From {client.databases[defin['db']]}:

            {defin['definition']}
            """
        client.disconnect()
        return ret
