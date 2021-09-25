import abc

import time
import threading

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GObject


class Parser(abc.ABC):
    """Base parser abstraction."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""


class AsyncParser(GObject):
    """Base async parser abstraction."""

    def __init__(self):
        self._cond = threading.Condition()
        self._query = None

        thread = threading.Thread(target=self.run, args=(), daemon=True)
        thread.start()

    @GObject.Signal(
        flags=GObject.SignalFlags.RUN_LAST,
        return_type=bool,
        arg_types=(str, str),
        accumulator=GObject.signal_accumulator_true_handled,
    )
    def query_result(query: str, value: str):
        pass

    def run_query(self, query: str):
        with self._cond:
            self._query = query
            self._cond.notify_all()

    def _run(self):
        while True:
            with self._cond:
                if self._query is None:
                    self._cond.wait()
                query = self._query
            result = self.parse(query)
            with self.cond:
                # Don't trigger signal if query changed.
                if self.query == query:
                    self.emit_async("query_result", query, result)
                    self.query = None

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""


class SleepyParrotParser(AsyncParser):
    """A parser that sleeps then repeats what it was fed."""

    def parse(self, string: str) -> str:
        self.string = string
        return "Looking up term..."

    def _parse(self):
        time.sleep(0.1)
        self.ret = self.string
        self.string = None
