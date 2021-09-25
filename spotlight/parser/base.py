import abc


class Parser(abc.ABC):
    """Base parser abstraction."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""
