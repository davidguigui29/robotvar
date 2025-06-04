# RoboTvar

**RoboTvar** is a Python project that creates custom fonts by merging Roboto font variants with  
the **Twemoji emoji font**. The resulting fonts combine the elegance of Roboto typography with  
the expressive and visually balanced Twemoji emojis.

> 🧠 Why? Because mixing emojis with text in a single `Label` in Kivy is otherwise tricky, often requiring workarounds or custom rendering. RoboTvar solves this with seamless, merged fonts.

```python
from kivy.uix.label import Label

label = Label(
    text="Hello World! 👋 🌍",
    font_name="RoboTvar"
)
```

This lets both text and emojis render correctly and cleanly — no more hacks or broken layouts.

---

## ✨ Features

- ✅ Seamless emoji + text rendering in Kivy Labels
- ✅ Includes four font variants:
  - RoboTvar-Regular.ttf
  - RoboTvar-Bold.ttf
  - RoboTvar-Italic.ttf
  - RoboTvar-BoldItalic.ttf
- ✅ Auto-downloads Roboto + Twemoji from GitHub
- ✅ Retries downloads with backoff
- ✅ Handles COLR/CPAL emoji rendering (color!)
- ✅ Kivy test app with screenshot capture
- ✅ Command-line interface for full workflow
- ✅ Font comparison tools for debugging/analysis

---

## 🛠 Installation

```bash
git clone https://github.com/patrikflorek/robotvar.git
cd robotvar

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt
```

---

## 🚀 Usage

### 🔹 Download Fonts

```bash
python -m robotvar --download-only
```

> Automatically fetches Roboto from Google Fonts and Twemoji from Mozilla's GitHub releases.

---

### 🔹 Merge Fonts

```bash
python -m robotvar --merge-only
```

To customize output location:

```bash
python -m robotvar --merge-only --output-dir ./my_fonts
```

---

### 🔹 Launch Test App

```bash
python -m robotvar --test-app
```

Renders samples and automatically saves screenshots in `robotvar/screenshots/`.

---

### 🔹 Compare Fonts

```bash
python -m robotvar --compare-fonts --font1 path/to/font1.ttf --font2 path/to/font2.ttf
```

Use this to check:
- Which characters differ
- Whether emoji glyphs were properly merged

---

### 🔹 Full Pipeline

```bash
python -m robotvar
```

This downloads and merges everything in one go.

---

## 📁 Project Structure

```
robotvar/
├── .venv/                     # Python virtual environment
├── requirements.txt           # Python dependencies
├── robotvar/                  # Main package directory
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # CLI entry point and argument parser
│   ├── fonts/                 # Downloaded font files
│   │   ├── roboto/            # Roboto font variants (Regular, Bold, etc.)
│   │   └── twemoji/           # Twemoji emoji font from Mozilla
│   ├── merged/                # Output directory for merged font files
│   └── scripts/               # Python scripts for internal operations
│       ├── __init__.py        # Script package initializer
│       ├── download.py        # Downloads Roboto and Twemoji fonts
│       ├── merge.py           # Merges glyphs and color layers into unified fonts
│       └── test_app.py        # Kivy app for rendering preview and screenshots
└── README.md                  # Project documentation

```

---

## 📦 Dependencies

- Python 3.8+
- `fonttools==4.56.0`
- `httpx==0.28.1`
- `kivy==2.3.1`

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

We welcome your contributions!

1. Fork this repo
2. Create your feature branch: `git checkout -b feat/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push it: `git push origin feat/my-feature`
5. Open a Pull Request 🚀

---

## 📜 License

Apache 2.0 — see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- [Google Fonts](https://github.com/googlefonts/roboto-2) — Roboto
- [Mozilla Twemoji](https://github.com/mozilla/twemoji-colr) — Twemoji color font
- ❤️ Thanks to [Anthropic Claude 3.5 Sonnet](https://www.anthropic.com) and [OpenAI GPT-4](https://openai.com) for co-development support

---

This README reflects all recent updates:  
✅ TossFace removed · ✅ Twemoji added · ✅ Font merging improved · ✅ CLI updated.
