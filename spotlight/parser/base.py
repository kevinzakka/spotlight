import abc

import time
import threading
from typing import Optional, Tuple

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GObject, GLib


class Parser(abc.ABC):
    """Base parser abstraction."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, string: str) -> str:
        """Parse a string."""


class AsyncParser(GObject.Object):
    """Base async parser abstraction."""

    def __init__(self):
        super().__init__()
        self._cond = threading.Condition()
        self._query = None

        thread = threading.Thread(target=self._run, args=(), daemon=True)
        thread.start()

    @GObject.Signal(
        flags=GObject.SignalFlags.RUN_LAST,
        return_type=bool,
        arg_types=(object,),
        accumulator=GObject.signal_accumulator_true_handled,
    )
    def query_result(
        self, query_value_exception: Tuple[str, Optional[str], Optional[Exception]]
    ):
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
            try:
                result = self.parse_sync(query)
                exception = None
            except Exception as exc:
                result = None
                exception = exc
            with self._cond:
                # Don't trigger signal if query changed.
                if self._query == query:
                    ev = GLib.Idle()
                    ev.set_callback(
                        lambda *args: self.emit(
                            "query_result", (query, result, exception)
                        )
                    )
                    ev.attach(GLib.MainContext.default())
                    self._query = None

    @abc.abstractmethod
    def parse_sync(self, string: str) -> str:
        """Parse a string."""


class SleepyParrotParser(AsyncParser):
    """A parser that sleeps then repeats what it was fed."""

    def parse_sync(self, string: str) -> str:
        time.sleep(0.1)
        raise ValueError("hi")
        return "hello " + string
