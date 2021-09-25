"""A basic arithmetic parser."""

from lark import Lark, Transformer, v_args

from .base import Parser

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


class ArithmeticParser(Parser):
    """Performs an arithmetic parse of the input."""

    def __init__(self):
        parser = Lark(GRAMMAR, parser="lalr", transformer=ArithmeticTransformer())
        self.parser = parser.parse

    def parse(self, string: str) -> str:
        try:
            return str(self.parser(string))
        except:
            return ""
