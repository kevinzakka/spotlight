from typing import Any

import regex

from spotlight import evaluators


class Parser:
    """An async parser."""

    LETTERS_ONLY = "^[A-Za-z ]+$"
    MATH_ONLY = "^[0-9+\-*/\^ ]+$"

    def __init__(self):
        self.de = evaluators.DictClientEvaluator()

    def parse(self, expression: str) -> str:
        expression = expression.lower()
        ret = ""

        if regex.match(self.LETTERS_ONLY, expression):
            pass
            # ret = evaluators.DictClientEvaluator()(expression)
            # ret = self.de(expression)
        else:
            ret = evaluators.ArithmeticEvaluator()(expression)

        return ret
