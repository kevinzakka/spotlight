from dictionary_client import DictionaryClient

from .base import AsyncParser


class DictClientParser(AsyncParser):
    """Performs a dictionary lookup of the input."""

    HOSTNAME = "dict.org"
    DATABASE = "wn"  # Should this be user changeable?

    def __init__(self):
        super().__init__()

        self.client = None

    def run_query(self, query: str):
        super().run_query(query)

        return "Searching definition..."

    def parse_sync(self, string: str) -> str:
        if self.client is None:
            self.client = DictionaryClient(self.HOSTNAME)

        definition = self.client.define(string, db=self.DATABASE).content
        if not definition:
            matches = self.client.match(string, db=self.DATABASE).content
            if matches is None:
                definition = None
            else:
                if len(matches) > 0:
                    definition = self.client.define(
                        matches[self.DATABASE][0], self.DATABASE
                    ).content

        if definition is None:
            answer = f"No match found for {string}."
        else:
            answer = self._format_answer(definition)

        return answer

    def _format_answer(self, definition) -> str:
        assert len(definition) == 1
        return f"{definition[0]['definition']}"
