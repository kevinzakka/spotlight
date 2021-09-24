import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk


class Spotlight(Gtk.Window):
    """An open-source Spotlight for Linux."""

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

        self.connect("key-press-event", self.on_key_press_event)
        self.connect("delete-event", Gtk.main_quit)

    def on_key_press_event(self, widget, event):
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

    def style_entry(self):
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

    def auto_shrink(self):
        self.resize(10, 10)

    def clear_text(self):
        self._answer.set_text("")
        self._entry.set_text("")
        self.auto_shrink()

    def copy_to_clipboard(self):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = self._answer.get_text()
        clip.set_text(text, len(text))


if __name__ == "__main__":
    spotlight = Spotlight()
    spotlight.show_all()
    Gtk.main()