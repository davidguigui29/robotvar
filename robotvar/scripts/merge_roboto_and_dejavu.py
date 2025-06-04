"""
Font merger for RoboTvar with DejaVu support.

Merges Roboto font variants with DejaVuSans and Twemoji emoji fonts,
scaling both CFF and glyf glyphs using TransformPen.
"""

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


def merge_fonts(base_font: TTFont, addon_font: TTFont, protect_existing=True) -> TTFont:
    scale = base_font["head"].unitsPerEm / addon_font["head"].unitsPerEm
    base_glyphs = set(base_font.getGlyphOrder())
    addon_glyphs = set(addon_font.getGlyphOrder())
    new_glyphs = addon_glyphs - base_glyphs

    added_glyphs = []

    for glyph_name in new_glyphs:
        if "CFF " in addon_font:
            glyph = otf_to_ttf_glyph_scaled(addon_font, glyph_name, scale)
        else:
            glyph = scale_glyf_glyph(addon_font.getGlyphSet(), glyph_name, scale)

        if glyph:
            base_font["glyf"][glyph_name] = glyph
            added_glyphs.append(glyph_name)
            if "hmtx" in addon_font and glyph_name in addon_font["hmtx"].metrics:
                aw, lsb = addon_font["hmtx"].metrics[glyph_name]
                base_font["hmtx"][glyph_name] = (int(aw * scale), int(lsb * scale))

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

    for table in addon_font["cmap"].tables:
        if table.isUnicode():
            for code, name in table.cmap.items():
                if name in added_glyphs and (not protect_existing or code not in format12.cmap):
                    format12.cmap[code] = name

    new_cmap.tables = [format12]
    base_font["cmap"] = new_cmap

    # Only keep glyphs that exist in glyf table
    final_glyphs = base_font.getGlyphOrder() + [g for g in added_glyphs if g in base_font["glyf"].glyphs]
    final_glyphs = list(dict.fromkeys(final_glyphs))  # remove duplicates

    # Sync glyph order for both font and 'glyf' table
    base_font.setGlyphOrder(final_glyphs)
    base_font["glyf"].glyphOrder = final_glyphs
    base_font["glyf"].glyphs = {g: base_font["glyf"].glyphs[g] for g in final_glyphs if g in base_font["glyf"].glyphs}

    if "maxp" in base_font:
        base_font["maxp"].numGlyphs = len(base_font.getGlyphOrder())

    return base_font


def merge_roboto_dejavu_fonts(output_dir: Optional[Path] = None) -> None:
    package_dir = Path(__file__).parent.parent
    roboto_dir = package_dir / "fonts" / "roboto"
    dejavu_dir = package_dir / "fonts" / "dejavu"

    output_dir = (package_dir / "fonts" / "roboto_dejavu")

    output_dir.mkdir(parents=True, exist_ok=True)

    roboto_fonts = list(roboto_dir.glob("Roboto-*.ttf"))
    dejavu_font = next(dejavu_dir.glob("*.ttf"), None)


    if not roboto_fonts:
        raise FileNotFoundError("Roboto fonts missing.")
    if not dejavu_font:
        raise FileNotFoundError("DejaVuSans font missing.")


    for roboto_font in roboto_fonts:
        variant_name = roboto_font.stem
        print(f"Here is the variant_name: {variant_name}")
        print(f"🔧 Merging: {roboto_font.name}")
        base_font = TTFont(roboto_font)

        base_font = merge_fonts(base_font, TTFont(dejavu_font))


        output_name = f"RoboTvar-{variant_name[7:]}.ttf"


        output_path = output_dir / output_name
        base_font.save(output_path)
        print(f"✅ Saved: {output_name}")
    


