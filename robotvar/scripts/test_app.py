"""Kivy test application for RoboTvar fonts.

Tests the combined font's ability to display text and emojis in various styles.
"""

import os

os.environ["KIVY_NO_ARGS"] = "1"

from datetime import datetime
from pathlib import Path
from typing import Optional

from kivy.core.window import Window
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder


# Set window size
Window.size = (1024, 768)

# KV language string for the UI
KV = """
<RootWidget@BoxLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.05, 1
        Rectangle:
            size: self.size
            pos: self.pos
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.2
        
        Label:
            text: "RoboTvar Fonts Showcase"
            font_size: 64
            font_name: "RoboTvar"
            color: 0.6, 0.2, 0.8, 1
    
    GridLayout:
        cols: 2
        spacing: 20
        padding: 10
        
        # Regular style tests
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.07, 0.07, 0.07, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
            
            Label:
                text: "Regular"
                font_size: 32
                font_name: "RoboTvar"
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\u2714 Hello World! 👋 🌍 1234"
                font_size: 48
                font_name: "RoboTvar"
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\u2714 Crown 👑 and clutch bag 👝"
                font_size: 24
                font_name: "RoboTvar"
                color: 1, 0.6, 0.2, 1
                
        # Bold style tests
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.1, 0.07, 0.04, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            Label:
                text: "Bold"
                font_size: 32
                font_name: "RoboTvar"
                bold: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: "RoboTvar"
                bold: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: " \u2714 Lab coat 🥼 and flat shoe 🥿"
                font_size: 24
                font_name: "RoboTvar"
                bold: True
                color: 1, 0.6, 0.2, 1
                
        # Italic style tests
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.07, 0.04, 0.1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            Label:
                text: "Italic"
                font_size: 32
                font_name: "RoboTvar"
                italic: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: "RoboTvar"
                italic: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\u2714 Rocket ship 🚀 and flexed biceps 💪"
                font_size: 24
                font_name: "RoboTvar"
                italic: True
                color: 1, 0.6, 0.2, 1
                
        # BoldItalic style tests
        BoxLayout:
            orientation: 'vertical'
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.09, 0.02, 0.09, 1
                Rectangle:
                    size: self.size
                    pos: self.pos
            
            Label:
                text: "Bold Italic"
                font_size: 32
                font_name: "RoboTvar"
                bold: True
                italic: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: "RoboTvar"
                bold: True
                italic: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\u2714 Bouquet 💐 and butterfly 🦋"
                font_size: 24
                font_name: "RoboTvar"
                bold: True
                italic: True
                color: 1, 0.6, 0.2, 1

RootWidget
"""


class RoboTvarTestApp(App):
    """Test application for RoboTvar fonts."""

    def __init__(self, font_dir: Optional[Path] = None, **kwargs):
        """Initialize the test app.

        Args:
            font_dir: Directory containing RoboTvar fonts, defaults to robotvar/merged
            **kwargs: Additional arguments passed to App
        """
        super().__init__(**kwargs)
        self.font_dir = font_dir or (Path(__file__).parent.parent / "merged")

    def build(self):
        """Build and return the root widget."""
        self._register_fonts()
        return Builder.load_string(KV)

    def _register_fonts(self) -> None:
        """Register all RoboTvar font variants with Kivy."""

        variants = ["Regular", "Bold", "BoldItalic", "Italic"]

        kwargs = {}
        for variant in variants:
            font_path = self.font_dir / f"RoboTvar-{variant}.ttf"
            if not font_path.exists():
                raise FileNotFoundError(
                    f"Font {font_path.name} not found. "
                    "Please run font merging first with: python -m robotvar"
                )

            kwargs[f"fn_{variant.lower()}"] = str(font_path)
        print(kwargs)
        LabelBase.register(name="RoboTvar", **kwargs)

    def on_stop(self):
        """Save a screenshot when the app is closed."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.font_dir.parent / "screenshots"
        screenshot_path.mkdir(exist_ok=True)
        self.root.export_to_png(str(screenshot_path / f"test_app_{timestamp}.png"))


def run_test_app(font_dir: Optional[Path] = None) -> None:
    """Run the RoboTvar test application.

    Args:
        font_dir: Optional custom directory containing RoboTvar fonts
    """
    RoboTvarTestApp(font_dir=font_dir).run()
