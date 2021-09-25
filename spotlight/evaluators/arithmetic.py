"""Evaluate arithmetic expressions."""

from lark import Lark, Transformer, v_args

from .base import Evaluator

ALIASES = {
    "ln": "log",
    "log": "log10",
}


GRAMMAR = """
    ?start: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: pow
        | product "*" pow  -> mul
        | product "/" pow  -> div
    
    ?pow: atom
        | pow "**" atom  -> pow
        | pow "^" atom   -> pow

    ?atom: NUMBER                       -> number
        | NAME "(" sum ")"              -> func
        | NAME "(" sum ("," sum)+ ")"   -> func
        |   "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)
class ArithmeticTransformer(Transformer):
    from operator import add, eq, ge, gt, le, lt, mul, ne, neg, pow, sub
    from operator import truediv as div

    def number(self, x):
        if x.isdigit():
            return int(x)
        return float(x)

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        return self.vars[name]

    def func(self, name, *args) -> float:
        import math

        name = str(name)
        if name in ALIASES:
            name = ALIASES[name]
        return getattr(math, name)(*args)


class ArithmeticEvaluator(Evaluator):
    """Performs an arithmetic evaluation of the expression."""

    def __init__(self):
        self.calc_parser = Lark(
            GRAMMAR, parser="lalr", transformer=ArithmeticTransformer()
        )
        self.calc = self.calc_parser.parse

    def evaluate(self, expression: str) -> str:
        try:
            return str(self.calc(expression))
        except:
            return ""
