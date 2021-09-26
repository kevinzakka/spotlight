"""Command line interface."""

import argparse

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from spotlight.spotlight import Spotlight


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force-mutter-center",
        action="store_true",
        help="Force the mutter window manager to center the window",
    )
    args = parser.parse_args()

    app = Spotlight(force_mutter_center=args.force_mutter_center)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
