# spotlight

An open-source Spotlight for Linux, for researchers.

## Todos

* [x] Arithmetic
* [x] Definitions
* [ ] Currency conversion (e.g. 1 BTC to USD)
* [ ] Latex preview
* [ ] [Bangs](https://help.duckduckgo.com/duckduckgo-help-pages/features/bangs/)
    * [ ] `!g`: google
    * [ ] `!a`: amazon
    * [ ] `!a`: youtube
* [ ] ArXiv / google scholar search
* [ ] Spotify search
* [ ] Autocomplete with GPT

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

Alternatively, you can create a custom keyboard shortcut. Just make sure you
are using the correct environment python binary (use `which python`).

* Name: `spotlight`
* Command: `/home/kevin/anaconda3/envs/spotlight/bin/python /home/kevin/repos/spotlight/main.py`
* Shortcut: `ctrl + space`
