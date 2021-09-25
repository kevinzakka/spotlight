import enum
import re
from typing import Dict

import gi

gi.require_version("Gtk", "3.0")
import threading

from gi.repository import Gdk, Gtk

from spotlight import parser


class Expression(enum.Enum):
    """The types of expressions we understand and support."""

    ARITHMETIC = "arithmetic"
    DICTIONARY_LOOKUP = "dictionary"
    CURRENCY_CONVERSION = "currency_conversion"
    BANG_SEARCH = "bang_search"
    SPOTIFY_SEARCH = "spotify_search"
    ARXIV_SEARCH = "arxiv_search"
    GOOGLE_SCHOLAR_SEARCH = "google_scholar_search"


class Linker:
    """The linker reads raw user text and links it to an Expression."""

    PATTERN_TO_EXPRESSION: Dict[str, Expression] = {
        "^[A-Za-z ]+$": Expression.DICTIONARY_LOOKUP,
        "[0-9a-z()+\-\*/]": Expression.ARITHMETIC,
        "^[!]": Expression.BANG_SEARCH,
    }

    def __call__(self, text: str) -> Expression:

        for pattern in self.PATTERN_TO_EXPRESSION.keys():
            if re.match(pattern, text) is not None:
                return self.PATTERN_TO_EXPRESSION[pattern]

        return "Invalid expression."


EXPRESSION_TO_PARSER = {
    Expression.ARITHMETIC: parser.ArithmeticParser,
    Expression.DICTIONARY_LOOKUP: parser.DictClientParser,
}


class Spotlight(Gtk.Window):
    """An open-source Spotlight for Linux."""

    MIN_HEIGHT = 10
    MIN_WIDTH = 10
    WIDTH = 400

    def __init__(self):
        super().__init__()

        container = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )

        self._entry = Gtk.Entry()
        self._entry.set_size_request(self.WIDTH, 0)
        self.style_entry()
        container.add(self._entry)

        self._answer = Gtk.Label(label="")
        self._answer.xalign = 0
        container.add(self._answer)

        self.add(container)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(True)
        self.set_decorated(False)

        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self._entry.connect("changed", self.on_entry_changed)

        self._linker = Linker()
        self._parsers: Dict[Expression, parser.AsyncParser] = {}

    def on_key_press(self, widget, event):
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        if event.keyval == Gdk.KEY_Escape:
            if self.text_entry != "":
                self.clear_text()
            else:
                self.close()
        elif ctrl and event.keyval == Gdk.KEY_c:
            self.copy_to_clipboard()
        else:
            return False

    def on_entry_changed(self, event) -> None:
        if self.text_entry == "":
            self.clear_text()
            return

        expression = self._linker(self.text_entry)
        if expression in self._parsers:
            parser = self._parsers[expression]
        else:
            parser = EXPRESSION_TO_PARSER[expression]()
            self._parsers[expression] = parser

            def _handle_result(_, query_output_exc):
                query, output, exc = query_output_exc
                if query == self.text_entry and exc is None:
                    self._answer.set_text(output)
                    self.auto_shrink()

            parser.connect("query_result", _handle_result)

        answer = parser.run_query(self.text_entry)
        if answer is not None:
            self._answer.set_text(answer)

    def style_entry(self) -> None:
        css = Gtk.CssProvider()
        data = """
                GtkEntry, entry {
                    border: none; font-size: 30px; padding: 15px 10px; box-shadow: none;
                }
                GtkLabel, label {
                    padding: 10px 10px 10px 10px; font-size: 20px;
                }
                """
        css.load_from_data(data.encode())
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        Gtk.StyleContext.add_provider_for_screen(screen, css, 600)
        self._entry.has_frame = False

    def auto_shrink(self) -> None:
        self.resize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)

    def clear_text(self) -> None:
        """Clears the text in the entry and answer boxes."""
        self._answer.set_text("")
        self._entry.set_text("")
        self.auto_shrink()

    def copy_to_clipboard(self) -> None:
        """Copies the answer to the user clipboard."""
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = self._answer.get_text()
        clip.set_text(text, len(text))

    @property
    def text_entry(self) -> str:
        return self._entry.props.text
