"""A basic arithmetic parser."""

from lark import Lark, Transformer, v_args

from .base import AsyncParser

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
        | "pi"                          -> pi
        | "e"                           -> e
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
    from operator import add, mul, pow, sub
    from operator import truediv as div

    # TODO(kevin): Figure out non-hacky way to return ints if the string can be
    # coerced to one. This will make for prettier printing in the spotlight
    # answer box.
    number = float

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        return self.vars[name]

    def pi(self) -> float:
        import math

        return math.pi

    def e(self) -> float:
        import math

        return math.e

    def func(self, name, *args) -> float:
        import math

        name = str(name)
        if name in ALIASES:
            name = ALIASES[name]
        return getattr(math, name)(*args)


class ArithmeticParser(AsyncParser):
    """Performs an arithmetic parse of the input."""

    def __init__(self):
        super().__init__()

        parser = Lark(GRAMMAR, parser="lalr", transformer=ArithmeticTransformer())
        self.parser = parser.parse

    def parse_sync(self, string: str) -> str:
        try:
            return str(self.parser(string))
        except:
            return ""
