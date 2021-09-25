# spotlight

A spotlight-equivalent for Linux.

## Todos

* [x] Arithmetic
* [ ] Definitions
* [ ] Currency conversion (e.g. 1 BTC to USD)
* [ ] [Bangs](https://help.duckduckgo.com/duckduckgo-help-pages/features/bangs/)
    * [ ] `!g`: google
    * [ ] `!a`: amazon
    * [ ] `!a`: youtube
* [ ] ArXiv / google scholar search
* [ ] Spotify search

## Quickstart

First install GTK dependencies:

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

Then install in editable mode:

```bash
git clone git@github.com:kevinzakka/spotlight.git
cd spotlight
pip install -e .
```

You can now run `spotlight` to launch the app.

Once this is ready to launch, we'll want to have instructions for binding the
entry point to a key stroke that way say `ctrl + space` can launch the app.
