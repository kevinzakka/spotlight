from dictionary_client import DictionaryClient

from .base import Evaluator


class DictClientEvaluator(Evaluator):
    """Looks up an expression using a dictionary client."""

    HOSTNAME = "dict.org"

    def evaluate(self, expression: str) -> str:
        raise NotImplementedError
