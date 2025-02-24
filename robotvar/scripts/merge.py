"""Font merger for RoboTvar.

Merges Roboto font variants with TossFace emoji font.
"""

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from pathlib import Path
from typing import Optional


def otf_to_ttf_glyph(font: TTFont, glyph_name: str) -> Optional[TTGlyphPen]:
    """Convert a CFF glyph to TTF format.

    Args:
        font: Source OTF font
        glyph_name: Name of the glyph to convert

    Returns:
        Converted TTF glyph or None if conversion failed
    """
    cff = font["CFF "].cff
    td = cff[cff.fontNames[0]]
    char_strings = td.CharStrings

    if glyph_name not in char_strings:
        return None

    pen = TTGlyphPen(None)
    char_strings[glyph_name].draw(pen)
    return pen.glyph()


def merge_fonts(base_font_path: Path, emoji_font_path: Path, output_path: Path) -> None:
    """Merge a Roboto font variant with TossFace emoji font.

    Args:
        base_font_path: Path to the Roboto font variant
        emoji_font_path: Path to the TossFace emoji font
        output_path: Where to save the merged font
    """
    print(f"Loading base font: {base_font_path.name}")
    base_font = TTFont(base_font_path)
    print(f"Loading emoji font: {emoji_font_path.name}")
    emoji_font = TTFont(emoji_font_path)

    # Get glyph sets
    base_glyphs = set(base_font.getGlyphOrder())
    emoji_glyphs = set(emoji_font.getGlyphOrder())
    new_glyphs = emoji_glyphs - base_glyphs
    print(f"Found {len(new_glyphs)} new glyphs to add")

    # Copy required tables for emoji support
    required_tables = ["GSUB", "GPOS", "GDEF", "COLR", "CPAL"]
    for table_tag in required_tables:
        if table_tag in emoji_font:
            if table_tag in base_font:
                del base_font[table_tag]
            base_font[table_tag] = emoji_font[table_tag]

    # Update glyph order
    current_glyph_order = base_font.getGlyphOrder()
    new_glyph_order = current_glyph_order + list(new_glyphs)
    base_font.setGlyphOrder(new_glyph_order)

    # Convert and copy new glyphs
    print("Converting and copying glyphs...")
    converted_count = 0
    for glyph_name in new_glyphs:
        ttf_glyph = otf_to_ttf_glyph(emoji_font, glyph_name)
        if ttf_glyph:
            base_font["glyf"][glyph_name] = ttf_glyph
            converted_count += 1

            # Copy metrics
            if "hmtx" in emoji_font and glyph_name in emoji_font["hmtx"].metrics:
                base_font["hmtx"][glyph_name] = emoji_font["hmtx"].metrics[glyph_name]

    print(f"Successfully converted {converted_count} glyphs from OTF to TTF format")

    # Update character mapping
    new_cmap = newTable("cmap")
    new_cmap.tableVersion = 0

    format12 = CmapSubtable.newSubtable(12)
    format12.platformID = 3
    format12.platEncID = 10
    format12.language = 0
    format12.cmap = {}

    # Copy base font mappings
    for table in base_font["cmap"].tables:
        if table.isUnicode():
            format12.cmap.update(table.cmap)

    # Add emoji font mappings
    for table in emoji_font["cmap"].tables:
        if table.isUnicode():
            for code, name in table.cmap.items():
                if name in new_glyphs:
                    format12.cmap[code] = name

    new_cmap.tables = [format12]
    base_font["cmap"] = new_cmap

    # Update maxp table
    if "maxp" in base_font:
        base_font["maxp"].numGlyphs = len(new_glyph_order)

    # Verify consistency
    assert len(base_font.getGlyphOrder()) == len(base_font["glyf"].glyphs)

    # Save merged font
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving merged font to: {output_path}")
    base_font.save(output_path)
    print("Font merge completed successfully!")


def merge_all_fonts(output_dir: Optional[Path] = None) -> None:
    """Merge all Roboto font variants with TossFace emoji font.

    Args:
        output_dir: Optional custom output directory, defaults to robotvar/merged
    """
    package_dir = Path(__file__).parent.parent
    roboto_dir = package_dir / "fonts" / "roboto"
    tossface_dir = package_dir / "fonts" / "tossface"
    output_dir = output_dir or (package_dir / "merged")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all Roboto variants
    roboto_fonts = list(roboto_dir.glob("Roboto-*.ttf"))
    if not roboto_fonts:
        raise FileNotFoundError(
            "No Roboto font variants found. Please run download first."
        )

    # Find TossFace font
    tossface_font = next(tossface_dir.glob("*.otf"), None)
    if not tossface_font:
        raise FileNotFoundError("TossFace font not found. Please run download first.")

    print(f"Found {len(roboto_fonts)} Roboto variants to process")

    # Process each Roboto variant
    for roboto_font in roboto_fonts:
        variant_name = roboto_font.stem  # e.g., "Roboto-Bold"
        output_name = f"RoboTvar-{variant_name[7:]}.ttf"  # e.g., "RoboTvar-Bold.ttf"
        output_path = output_dir / output_name

        print(f"\nProcessing {variant_name}...")
        merge_fonts(roboto_font, tossface_font, output_path)
