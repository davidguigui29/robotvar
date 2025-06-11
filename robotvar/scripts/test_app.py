"""Kivy test application for RoboTvar fonts.

Tests the combined font's ability to display text and emojis in various styles.
"""

import os

os.environ["KIVY_NO_ARGS"] = "1"

from datetime import datetime
from fontTools.ttLib import TTFont
from pathlib import Path
from typing import Optional

from kivy.core.window import Window
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.lang import Builder

# Set window size
# Window.size = (1024, 768)

# Maximize the window (works on most platforms)
Window.maximize()

class RoboTvarTestApp(App):
    """Test application for RoboTvar fonts."""

    def __init__(self, font_dir: Optional[Path] = None, **kwargs):
        """Initialize the test app.

        Args:
            font_dir: Directory containing merged fonts, defaults to robotvar/merged
            **kwargs: Additional arguments passed to App
        """
        super().__init__(**kwargs)
        self.font_dir = font_dir or (Path(__file__).parent.parent / "merged")
        self.available_families = []

    def build(self):
        self._register_fonts()
        # Determine the RoboTvar tab label based on the font family name
        robovar_tab_label = "RoboTvar"
        if "RoboTvar" in self.available_families:
            robovar_regular = self.font_dir / "RoboTvar-Regular.ttf"
            if robovar_regular.exists():
                family_name = self.get_font_name(robovar_regular)
                if family_name == "Roboto":
                    robovar_tab_label = "Roboto+TossFace"
                else:
                    robovar_tab_label = "DejaVu+Twemoji"
        # Dynamically build the KV string based on available families
        # tabs = ""
        # if "RoboTvar" in self.available_families:
        #     tabs += f"    TabbedPanelItem:\n"
        #     tabs += f"        text: \"{robovar_tab_label}\"\n"
        #     tabs += "        background_color: 0.6, 0.2, 0.8, 1\n"
        #     tabs += "        FontShowcase:\n"
        #     tabs += "            font_name: \"RoboTvar\"\n"
        # if "DejaVuTwemoji" in self.available_families:
        #     tabs += "    TabbedPanelItem:\n"
        #     tabs += "        text: \"DejaVu+Twemoji\"\n"
        #     tabs += "        background_color: 0.6, 0.2, 0.8, 1\n"
        #     tabs += "        FontShowcase:\n"
        #     tabs += "            font_name: \"DejaVuTwemoji\"\n"

        tabs = ""
        if "RoboTvar" in self.available_families:
            robovar_regular = self.font_dir / "RoboTvar-Regular.ttf"
            robovar_family = self.get_font_name(robovar_regular) if robovar_regular.exists() else ""
            robovar_tab_label = "Roboto+TossFace" if robovar_family == "Roboto" else "DejaVu+Twemoji"
            robovar_title = "Roboto and TossFace Showcase" if robovar_family == "Roboto" else "DejaVu and Twemoji Showcase"
            tabs += f"    TabbedPanelItem:\n"
            tabs += f"        text: \"{robovar_tab_label}\"\n"
            tabs += "        background_color: 0.6, 0.2, 0.8, 1\n"
            tabs += "        FontShowcase:\n"
            tabs += "            font_name: \"RoboTvar\"\n"
            tabs += f"            title: \"{robovar_title}\"\n"
        
        # If DejaVuTwemoji is available, add its tab
        if "DejaVuTwemoji" in self.available_families:
            tabs += f"    TabbedPanelItem:\n"
            tabs += f"        text: \"DejaVu+Twemoji\"\n"
            tabs += "        background_color: 0.6, 0.2, 0.8, 1\n"
            tabs += "        FontShowcase:\n"
            tabs += "            font_name: \"DejaVuTwemoji\"\n"
            tabs += f"            title: \"DejaVu and Twemoji Showcase\"\n"

        kv = f"""
<FontShowcase@BoxLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    font_name: ''
    title: ''
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
            id: title_label
            text: root.title
            # text: "Roboto and TossFace Showcase" if root.font_name=="RoboTvar" else "DejaVu and Twemoji Showcase"
            font_size: 64
            font_name: root.font_name
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
                font_name: root.font_name
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\\u2714 Hello World! 👋 🌍 12"
                font_size: 48
                font_name: root.font_name
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\\u2714 Crown 👑 and clutch bag 👝"
                font_size: 24
                font_name: root.font_name
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
                font_name: root.font_name
                bold: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: root.font_name
                bold: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: " \\u2714 Lab coat 🥼 and flat shoe 🥿"
                font_size: 24
                font_name: root.font_name
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
                font_name: root.font_name
                italic: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: root.font_name
                italic: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\\u2714 Rocket ship 🚀 and flexed biceps 💪"
                font_size: 24
                font_name: root.font_name
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
                font_name: root.font_name
                bold: True
                italic: True
                color: 0.2, 0.6, 1, 1

            Label:
                text: "\\u2714 Hello World! 👋 🌍"
                font_size: 48
                font_name: root.font_name
                bold: True
                italic: True
                color: 0.2, 1, 0.4, 1

            Label:
                text: "\\u2714 Bouquet 💐 and butterfly 🦋"
                font_size: 24
                font_name: root.font_name
                bold: True
                italic: True
                color: 1, 0.6, 0.2, 1

TabbedPanel:
    do_default_tab: False
    # tab_height: 64
    tab_width: 300  # set a fixed width for each tab
{tabs}
"""
        return Builder.load_string(kv)

    def _register_fonts(self) -> None:
        """Register all RoboTvar(Roboto and TossFaceFontWeb) and DejaVuTwemoji(DejaVuSans and Twemoji) font variants with Kivy."""

        variants = ["Regular", "Bold", "BoldItalic", "Italic"]
        robovar_kwargs = {}
        robovar_family_name = None
        for variant in variants:
            font_path = self.font_dir / f"RoboTvar-{variant}.ttf"
            if not font_path.exists():
                raise FileNotFoundError(
                    f"Font {font_path.name} not found. "
                    "Please run font merging first with: python -m robotvar"
                )
            if variant == "Regular":
                robovar_family_name = self.get_font_name(font_path)
            robovar_kwargs[f"fn_{variant.lower()}"] = str(font_path)
        # Set the showcase title based on the family name
        if robovar_family_name == "Roboto":
            self.title = "Roboto and TossFace Showcase"
        else:
            self.title = "DejaVu and Twemoji Showcase"
        LabelBase.register(name="RoboTvar", **robovar_kwargs)
        self.available_families.append("RoboTvar")

        # Optionally register DejaVuTwemoji if all variants exist
        dejavu_kwargs = {}
        all_dejavu_exist = True
        for variant in variants:
            font_path = self.font_dir / f"DejaVuTwemoji-{variant}.ttf"
            if not font_path.exists():
                all_dejavu_exist = False
                break
            dejavu_kwargs[f"fn_{variant.lower()}"] = str(font_path)
        if all_dejavu_exist:
            
            LabelBase.register(name="DejaVuTwemoji", **dejavu_kwargs)
            self.available_families.append("DejaVuTwemoji")

    def on_stop(self):
        """Save a screenshot when the app is closed."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.font_dir.parent / "screenshots"
        screenshot_path.mkdir(exist_ok=True)
        self.root.export_to_png(str(screenshot_path / f"test_app_{timestamp}.png"))


    def get_font_name(self, ttf_path):
        font = TTFont(ttf_path)
        name = font['name']
        for record in name.names:
            if record.nameID == 1:  # 1 is the nameID for the font family name
                return record.toUnicode()
        return None

    


def run_test_app(font_dir: Optional[Path] = None) -> None:
    """Run the RoboTvar test application.

    Args:
        font_dir: Optional custom directory containing merged fonts
    """
    RoboTvarTestApp(font_dir=font_dir).run()


