"""Font merger for RoboTvar with proper scaling for glyf glyphs.

Merges Roboto font variants with Twemoji Mozilla or similar emoji fonts,
scaling both CFF and glyf glyphs using TransformPen. This script works
great with Twemoji Mozilla, which uses COLR/CPAL layered color outlines.

- Roboto fonts are expected in: fonts/roboto/
- Emoji font (e.g., TwemojiMozilla.ttf) should be placed in: fonts/twemoji/
- Output will be written to: merged/
- Handles both CFF (OTF) and glyf (TTF) emoji glyphs.

Note: Scaling boost is disabled for Twemoji as it renders well without it.
"""

from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from pathlib import Path
from typing import Optional
from .merge_roboto_and_dejavu import merge_roboto_dejavu_fonts


def scale_glyf_glyph(glyph_set, glyph_name, scale) -> Optional[TTGlyphPen]:
    """Scale a TTF glyf-based glyph using TransformPen."""
    if glyph_name not in glyph_set:
        return None
    glyph = glyph_set[glyph_name]
    pen = TTGlyphPen(glyph_set)
    tpen = TransformPen(pen, (scale, 0, 0, scale, 0, 0))
    glyph.draw(tpen)
    return pen.glyph()


def otf_to_ttf_glyph_scaled(font: TTFont, glyph_name: str, scale: float = 1.0) -> Optional[TTGlyphPen]:
    """Convert and scale a CFF glyph to TTF format using TransformPen."""
    if "CFF " not in font:
        return None
    cff = font["CFF "].cff
    td = cff[cff.fontNames[0]]
    char_strings = td.CharStrings

    if glyph_name not in char_strings:
        return None

    pen = TTGlyphPen(None)
    tpen = TransformPen(pen, (scale, 0, 0, scale, 0, 0))
    char_strings[glyph_name].draw(tpen)
    return pen.glyph()


def merge_fonts(base_font_path: Path, emoji_font_path: Path, output_path: Path) -> None:
    """Merge one Roboto variant with an emoji font into a new font file."""
    print(f"Loading base font: {base_font_path.name}")
    base_font = TTFont(base_font_path)
    print(f"Loading emoji font: {emoji_font_path.name}")
    emoji_font = TTFont(emoji_font_path)

    # Compute scaling ratio between base and emoji UPM (Units per Em)
    scale = base_font["head"].unitsPerEm / emoji_font["head"].unitsPerEm
    SCALE_BOOST = 1.8  # Adjust to taste
    # scale *= SCALE_BOOST
    print(f"Scaling emoji glyphs by: {scale:.3f} (Twemoji renders well without boost)")

    base_glyphs = set(base_font.getGlyphOrder())
    emoji_glyphs = set(emoji_font.getGlyphOrder())
    new_glyphs = emoji_glyphs - base_glyphs
    print(f"Found {len(new_glyphs)} new glyphs to add")

    # Copy emoji color tables if present
    for table_tag in ["GSUB", "GPOS", "GDEF", "COLR", "CPAL"]:
        if table_tag in emoji_font:
            if table_tag in base_font:
                del base_font[table_tag]
            base_font[table_tag] = emoji_font[table_tag]

    # Merge glyph order
    new_glyph_order = base_font.getGlyphOrder() + list(new_glyphs)
    base_font.setGlyphOrder(new_glyph_order)

    print("Converting and copying emoji glyphs...")
    converted_count = 0
    for glyph_name in new_glyphs:
        if "CFF " in emoji_font:
            ttf_glyph = otf_to_ttf_glyph_scaled(emoji_font, glyph_name, scale)
        else:
            ttf_glyph = scale_glyf_glyph(emoji_font.getGlyphSet(), glyph_name, scale)

        if ttf_glyph:
            base_font["glyf"][glyph_name] = ttf_glyph
            converted_count += 1

            if "hmtx" in emoji_font and glyph_name in emoji_font["hmtx"].metrics:
                aw, lsb = emoji_font["hmtx"].metrics[glyph_name]
                base_font["hmtx"][glyph_name] = (int(aw * scale), int(lsb * scale))

    print(f"✅ Successfully added {converted_count} emoji glyphs")

    # Merge character maps
    new_cmap = newTable("cmap")
    new_cmap.tableVersion = 0

    format12 = CmapSubtable.newSubtable(12)
    format12.platformID = 3
    format12.platEncID = 10
    format12.language = 0
    format12.cmap = {}

    for table in base_font["cmap"].tables:
        if table.isUnicode():
            format12.cmap.update(table.cmap)

    # Add emoji font mappings ONLY if code point is not already mapped
    for table in emoji_font["cmap"].tables:
        if table.isUnicode():
            for code, name in table.cmap.items():
                if name in new_glyphs and code not in format12.cmap:
                    format12.cmap[code] = name


    new_cmap.tables = [format12]
    base_font["cmap"] = new_cmap

    if "maxp" in base_font:
        base_font["maxp"].numGlyphs = len(new_glyph_order)

    assert len(base_font.getGlyphOrder()) == len(base_font["glyf"].glyphs)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving merged font to: {output_path}")
    base_font.save(output_path)
    print("✅ Font merge completed!")


def merge_all_fonts(output_dir: Optional[Path] = None) -> None:
    merge_roboto_dejavu_fonts()
    
    """Merge all Roboto font variants with a Twemoji-style emoji font."""
    package_dir = Path(__file__).parent.parent
    roboto_dir = package_dir / "fonts" / "roboto_dejavu"
    emoji_dir = package_dir / "fonts" / "twemoji"
    output_dir = output_dir or (package_dir / "merged")

    output_dir.mkdir(parents=True, exist_ok=True)

    roboto_fonts = list(roboto_dir.glob("*.ttf"))
    if not roboto_fonts:
        raise FileNotFoundError("No Roboto font variants found in fonts/roboto/")

    emoji_font = next(emoji_dir.glob("*.ttf"), None)
    if not emoji_font:
        raise FileNotFoundError("Emoji font not found in fonts/twemoji/")

    print(f"Merging {len(roboto_fonts)} Roboto variants with {emoji_font.name}")

    for roboto_font in roboto_fonts:
        variant_name = roboto_font.stem
        output_name = f"RoboTvar-{variant_name[9:]}.ttf"
        output_path = output_dir / output_name

        print(f"\n📦 Processing {variant_name}...")
        merge_fonts(roboto_font, emoji_font, output_path)
