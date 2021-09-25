import abc

import time
import threading


class Parser(abc.ABC):
    """Base parser abstraction."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""


class AsyncParser(abc.ABC):
    """Base async parser abstraction."""

    def __init__(self):
        self.string = None
        self.ret = None

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            if self.string is not None:
                self._parse()
            time.sleep(0.05)

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""

    def _parse(self):
        pass


class SleepyParrotParser(AsyncParser):
    """A parser that sleeps then repeats what it was fed."""

    def parse(self, string: str) -> str:
        self.string = string
        return "Looking up term..."

    def _parse(self):
        time.sleep(0.1)
        self.ret = self.string
        self.string = None
