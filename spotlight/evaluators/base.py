import abc


class Evaluator(abc.ABC):
    """Base evaluator abstraction."""

    def __init__(self):
        pass

    def __call__(self, expression: str) -> str:
        return self.evaluate(expression)

    @abc.abstractmethod
    def evaluate(self, expression: str) -> str:
        """Evaluate the expression."""
