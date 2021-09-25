"""Command line interface."""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from spotlight.spotlight import Spotlight


def main():
    app = Spotlight()
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
