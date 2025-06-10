from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from pathlib import Path
from typing import Optional

def scale_glyf_glyph(glyph_set, glyph_name, scale) -> Optional[TTGlyphPen]:
    if glyph_name not in glyph_set:
        return None
    glyph = glyph_set[glyph_name]
    pen = TTGlyphPen(glyph_set)
    tpen = TransformPen(pen, (scale, 0, 0, scale, 0, 0))
    glyph.draw(tpen)
    return pen.glyph()

def otf_to_ttf_glyph_scaled(font: TTFont, glyph_name: str, scale: float = 1.0) -> Optional[TTGlyphPen]:
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
    print(f"Loading base font: {base_font_path.name}")
    base_font = TTFont(base_font_path)
    print(f"Loading emoji font: {emoji_font_path.name}")
    emoji_font = TTFont(emoji_font_path)

    scale = base_font["head"].unitsPerEm / emoji_font["head"].unitsPerEm
    print(f"Scaling emoji glyphs by: {scale:.3f}")

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
    for table in emoji_font["cmap"].tables:
        if table.isUnicode():
            for code, name in table.cmap.items():
                if name in new_glyphs and code not in format12.cmap:
                    format12.cmap[code] = name

    new_cmap.tables = [format12]
    base_font["cmap"] = new_cmap

    if "maxp" in base_font:
        base_font["maxp"].numGlyphs = len(new_glyph_order)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Saving merged font to: {output_path}")
    base_font.save(output_path)
    print("✅ Font merge completed!")

def merge_all_fonts(output_dir: Optional[Path] = None) -> None:
    """Merge all DejaVuSans font variants with Twemoji into RoboTvar-compatible fonts."""
    package_dir = Path(__file__).parent.parent
    dejavu_dir = package_dir / "fonts" / "dejavu"
    twemoji_dir = package_dir / "fonts" / "twemoji"
    output_dir = output_dir or (package_dir / "merged")
    output_dir.mkdir(parents=True, exist_ok=True)

    emoji_font = next(twemoji_dir.glob("*.ttf"))
    dejavu_fonts = list(dejavu_dir.glob("*.ttf"))
    if not dejavu_fonts:
        raise FileNotFoundError("No DejaVuSans font variants found in fonts/dejavu/")

    # Mapping from DejaVuSans variant to RoboTvar output name
    variant_map = {
        "DejaVuSans.ttf": "RoboTvar-Regular.ttf",
        "DejaVuSans-Bold.ttf": "RoboTvar-Bold.ttf",
        "DejaVuSans-Oblique.ttf": "RoboTvar-Italic.ttf",
        "DejaVuSans-BoldOblique.ttf": "RoboTvar-BoldItalic.ttf",
    }

    print(f"Merging {len(dejavu_fonts)} DejaVuSans variants with {emoji_font.name}")

    for dejavu_font in dejavu_fonts:
        variant_name = dejavu_font.name
        output_name = variant_map.get(dejavu_font.name, f"RoboTvar-{dejavu_font.stem}.ttf")
        output_path = output_dir / output_name

        print(f"\n📦 Processing {variant_name} -> {output_name} ...")
        merge_fonts(dejavu_font, emoji_font, output_path)