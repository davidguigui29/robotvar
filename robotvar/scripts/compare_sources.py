"""Font comparison utilities for RoboTvar.

Provides functionality to compare character sets between fonts.
"""

import sys
import argparse
from fontTools.ttLib import TTFont
from pathlib import Path
from typing import Set


def get_font_characters(font_path: Path) -> Set[str]:
    """Get a set of character names present in the font.

    Args:
        font_path: Path to the font file

    Returns:
        Set of character names in the font
    """
    font = TTFont(font_path)
    return set(font.getGlyphOrder())


def get_overlapping_characters(font1_path: Path, font2_path: Path) -> Set[str]:
    """Get character names that are present in both fonts.

    Args:
        font1_path: Path to the first font
        font2_path: Path to the second font

    Returns:
        Set of character names present in both fonts
    """
    chars1 = get_font_characters(font1_path)
    chars2 = get_font_characters(font2_path)
    return chars1.intersection(chars2)


def compare_fonts(font1_path: Path, font2_path: Path) -> None:
    """Compare two fonts and print overlapping characters.

    Args:
        font1_path: Path to the first font
        font2_path: Path to the second font
    """
    if not font1_path.exists():
        print(f"Error: Font file not found: {font1_path}", file=sys.stderr)
        sys.exit(1)
    if not font2_path.exists():
        print(f"Error: Font file not found: {font2_path}", file=sys.stderr)
        sys.exit(1)

    overlapping = get_overlapping_characters(font1_path, font2_path)
    print(f"\nFound {len(overlapping)} overlapping characters between:")
    print(f"1: {font1_path.name}")
    print(f"2: {font2_path.name}")
    print("\nOverlapping characters:")
    for char in sorted(overlapping):
        print(f"- {char}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare character sets between fonts."
    )
    parser.add_argument("font1", type=Path, help="Path to the first font")
    parser.add_argument("font2", type=Path, help="Path to the second font")
    args = parser.parse_args()
    compare_fonts(args.font1, args.font2)


if __name__ == "__main__":
    main()
