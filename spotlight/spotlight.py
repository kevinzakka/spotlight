import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


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

    def on_key_press(self, widget, event):
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        if event.keyval == Gdk.KEY_Escape:
            if self._entry.props.text != "":
                self.clear_text()
            else:
                self.close()
        elif ctrl and event.keyval == Gdk.KEY_c:
            self.copy_to_clipboard()
        else:
            return False

    def on_entry_changed(self, event) -> None:
        if self._entry.props.text == "":
            self.auto_shrink()
            return
        self._answer.set_text(self._entry.props.text)

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
