"""Command line interface."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .spotlight import Spotlight


def main():
    from .parser.base import SleepyParrotParser

    parser = SleepyParrotParser()
    parser.connect("query_result", handle_result)
    parser.run_query("hi")
    # app = Spotlight()
    # app.show_all()
    Gtk.main()


def handle_result(_, query_output):
    print("hi", query_output)
