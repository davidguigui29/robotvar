# RoboTvar

RoboTvar is a Python project that creates custom fonts by merging Roboto font variants with  
**Twemoji emoji font** or **TossFace emoji font**. The resulting fonts combine the elegance of Roboto typography with expressive emoji support.

![image](screenshot.gif)

## Motivation

This project addresses a problem which might arise when attempting to display text with emojis in a  
single `Label` widget. Typically, mixing regular text with emojis in a `kivy.uix.label.Label`'s  
`text` attribute might require more complex markup workarounds or multiple widgets. RoboTvar solves  
this by creating unified fonts that contain both text and emoji glyphs, allowing you to:

```python
from kivy.uix.label import Label

# Now you can simply do this:
label = Label(
    text="Hello World! 👋 🌍",
    font_name="RoboTvar"
)
```

The merged fonts ensure that both text and emojis render correctly within a single Label widget,  
maintaining proper alignment, spacing, and style consistency across your Kivy application.

## Features

- Seamless text and emoji display in Kivy Label widgets
- Multiple font styles for flexible typography:
  - [RoboTvar-Regular.ttf](https://github.com/patrikflorek/robotvar/blob/main/robotvar/merged/RoboTvar-Regular.ttf)
  - [RoboTvar-Bold.ttf](https://github.com/patrikflorek/robotvar/blob/main/robotvar/merged/RoboTvar-Bold.ttf)
  - [RoboTvar-Italic.ttf](https://github.com/patrikflorek/robotvar/blob/main/robotvar/merged/RoboTvar-Italic.ttf)
  - [RoboTvar-BoldItalic.ttf](https://github.com/patrikflorek/robotvar/blob/main/robotvar/merged/RoboTvar-BoldItalic.ttf)
- **Supports both Twemoji and TossFace emoji fonts**  
  - Default merge uses TossFace for backward compatibility  
  - Use `--merge-twemoji` to merge with Twemoji instead
- Automatic downloading of Roboto, TossFace, DejaVuSans, and Twemoji fonts from their official GitHub sources
- Retry logic and redirect handling for more robust font downloading
- Font merging with proper glyph conversion, scaling, and metrics preservation
- Unicode and symbol support via **DejaVuSans** integration
- Interactive Kivy-based test application for font preview and screenshot capture
- Font analysis tools for comparing character sets between fonts
- **New reset options:**  
  - `--delete` deletes the merged fonts folder  
  - `--delete-all` deletes all font folders in the fonts directory  
  - Both options clean up generated or downloaded files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/patrikflorek/robotvar.git
cd robotvar
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

RoboTvar provides a command-line interface with several operations:

### Download Fonts

Download required fonts from GitHub repositories (Roboto, TossFace, DejaVuSans, and Twemoji):
```bash
python -m robotvar --download-only
```

> ✅ Downloads now support automatic redirect handling and retry on failure.

### Merge Fonts

Merge downloaded fonts to create RoboTvar variants (default: TossFace):
```bash
python -m robotvar --merge-only
```

Merge with Twemoji instead:
```bash
python -m robotvar --merge-twemoji
```

Merge with Twemoji with the --showcase argument to create the showcase fonts DejaVuTwemoji-*.ttf. That way you can see a second tab in the test application with DejaVuSans and Twemoji fonts. This is useful if you want to see how the DejaVuSans font looks with Twemoji emojis and how Roboto fonts look with TossFace emojis:
```bash
python -m robotvar --merge-twemoji --showcase

You can specify a custom output directory:
```bash
python -m robotvar --merge-only --output-dir /path/to/output
```

### Reset/Cleanup

Delete the merged fonts folder:
```bash
python -m robotvar --delete
```

Delete all font folders in the fonts directory (full cleanup):
```bash
python -m robotvar --delete-all
```

### Test Application

Launch the interactive test application to preview the fonts:
```bash
python -m robotvar --test-app   
```

The test application automatically saves screenshots to `robotvar/screenshots/` when closed.  
Screenshots include samples of text and emojis in all four created font variants with different  
sizes and colors.

### Compare Fonts

Compare character sets between two font files:
```bash
python -m robotvar --compare-fonts --font1 /path/to/first/font.ttf --font2 /path/to/second/font.ttf
```

This will display a list of characters (glyphs) that are present in both fonts. Useful for:
- Analyzing font compatibility before merging
- Verifying contents of merged fonts
- Checking for potential character conflicts or overlaps

### Full Process

Run the complete process (download and merge) in one command:
```bash
python -m robotvar
```

## Project Structure

```
robotvar/
├── .venv/                     # Python virtual environment
├── requirements.txt           # Python dependencies
├── robotvar/                  # Main package directory
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # CLI entry point
│   ├── fonts/                 # Downloaded font files
│   │   ├── roboto/            # Roboto font variants
│   │   ├── dejavu/            # DejaVuSans font (for Unicode/symbol support)
│   │   ├── tossface/          # TossFace emoji font
│   │   └── twemoji/           # Twemoji emoji font
│   ├── merged/                # Output directory for merged fonts
│   ├── screenshots            # Output directory for screenshots taken when you close test_app
│   └── scripts/               # Package scripts
│       ├── __init__.py                    # Scripts initialization
│       ├── compare_sources.py             # Compare two fonts
│       ├── download.py                    # Font downloading with redirect support
│       ├── merge.py                       # Font merging(Roboto with TossFace emoji font)
│       ├── merge_dejavu_and_twemoji.py    # Font merging(DejaVuSans with Twemoji font)
│       ├── reset.py                       # Delete generated folders/files
│       └── test_app.py                    # Kivy test application
└── README.md
```

## Dependencies

- Python 3.8+
- fonttools==4.56.0
- Kivy==2.3.1
- httpx==0.28.1

## Development

This project was primarily developed through AI-assisted pair programming using Claude 3.5 Sonnet, 
an AI coding agent by Anthropic. The AI agent helped with:

- Project structure and organization
- Implementation of font downloading and merging functionality
- Creation of the Kivy test application
- Documentation, README, and license generation

The development focused on achieving the first fully functional version of the package. While the 
current implementation successfully accomplishes its core objectives, there is plenty of room for 
code improvements, optimizations, and additional features in future iterations.



## Contributing

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request 🚀

## Contributors

We gratefully acknowledge the contributions of:

- [David Guigui](https://github.com/davidguigui29) - Twemoji integration, font merging improvements, GUI and CLI enhancements
- [Patrik Florek](https://github.com/patrikflorek) - Project creator and maintainer


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Fonts](https://github.com/googlefonts/roboto-2) — Roboto font family  
- [Mozilla Twemoji](https://github.com/mozilla/twemoji-colr) — Twemoji emoji font  
- [Toss](https://github.com/toss/tossface) — TossFace emoji font  
- [DejaVu Fonts](https://dejavu-fonts.github.io/) — DejaVuSans font for wide Unicode coverage
