import re

from spotlight import evaluators


class Parser:
    """An async parser."""

    LETTERS_ONLY = "^[A-Za-z ]+$"
    MATH_ONLY = "^[0-9+\-*/\^ ]+$"

    def parse(self, expression: str) -> str:
        expression = expression.lower()
        ret = ""

        if re.match(self.LETTERS_ONLY, expression):
            ret = evaluators.DictClientEvaluator()(expression)
        else:
            ret = evaluators.ArithmeticEvaluator()(expression)

        return ret
