#!/usr/bin/env python3
"""
MTG Card Renderer — generates realistic Magic: The Gathering card images from JSON data.

Uses real Beleren Bold (card names) and MPlantin (rules text) fonts plus
mana symbols from the andrewgioia/mana project.

All dimensions are computed from a target DPI so the output matches
the physical size of a real MTG card (63 × 88 mm / 2.48 × 3.46 in).

Usage:
    python render_cards.py cards.json --output-dir ./output --dpi 300
    python render_cards.py --single --name "Ember Archon" --mana-cost "{3}{R}{R}" ...
"""

import argparse
import json
import os
import re
import sys
import textwrap
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter, PngImagePlugin

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SYMBOLS_DIR = ASSETS_DIR / "symbols"
FRAMES_DIR = ASSETS_DIR / "frames"
PT_DIR = FRAMES_DIR / "pt"

# ---------------------------------------------------------------------------
# Physical card size
# A real MTG card is 63 × 88 mm (2.48 × 3.46 in).
# ---------------------------------------------------------------------------
CARD_WIDTH_MM = 63.0
CARD_HEIGHT_MM = 88.0
CARD_WIDTH_IN = CARD_WIDTH_MM / 25.4
CARD_HEIGHT_IN = CARD_HEIGHT_MM / 25.4

# ---------------------------------------------------------------------------
# Layout defined in MILLIMETRES — sourced from real MTG card measurements.
#
#   Card:     63 × 88 mm
#   Border:   ~3 mm top/sides, ~5 mm bottom (collector info area)
#   Art box:  53 × 39 mm  (modern M15+ frame)
#   Text box: 53 × 24 mm
#   Type line: ~4.5 mm tall
#   Title bar: ~5 mm tall
#
# References:
#   - Arcmage wiki template references (53 × 39 mm art, 53 × 24 mm text)
#   - Draftsim / Cardboard Keeper card measurement guides
#   - MTG Wiki illustration dimensions
# ---------------------------------------------------------------------------
_LAYOUT_MM = {
    # Structural
    "border_top":      3.0,    # black border, top
    "border_side":     3.0,    # black border, left & right
    "border_bottom":   5.0,    # black border, bottom (collector info)
    "inner_pad":       1.5,    # coloured frame visible around content elements
    "corner_radius":   2.0,

    # Title bar
    "title_bar_offset": 1.0,   # gap from inner frame top to title bar
    "title_bar_h":      5.0,

    # Art box (modern M15+ frame)
    "art_gap":          0.8,   # gap between title bar → art, art → type line
    "art_h":           39.0,   # ← the key measurement: real art window height

    # Type line
    "type_bar_h":       4.5,

    # Text box
    "text_box_gap":     0.8,   # gap between type line and text box
    # text box height is computed: fills remaining space above footer

    # Power / toughness box
    "pt_box_w":        10.0,
    "pt_box_h":         6.0,

    # Footer (collector number line)
    "footer_h":         3.5,   # space for collector info at card bottom

    # Rarity gem
    "gem_hw":           1.4,   # half-width
    "gem_hh":           1.6,   # half-height
}

# Font sizes in POINTS (at 300 DPI, 1 pt ≈ 1/72 in ≈ 4.17 px).
# Real MTG uses ~9 pt rules text; title is larger.
_FONT_PT = {
    "title":        10.0,   # Beleren Bold, card name
    "type":          7.5,   # Beleren Bold, type line
    "rules":         7.5,   # MPlantin, rules text  (real cards ~9pt but we need room)
    "rules_italic":  7.0,   # MPlantin, flavor text
    "pt":            9.5,   # Beleren Bold, power/toughness
    "small":         5.0,   # MPlantin, collector info
}

# Symbol sizes in mm
_SYM_MM = {
    "mana_cost":     3.0,   # mana cost circles in title bar
    "inline":        2.2,   # inline mana symbols in rules text
    "mana_gap":      0.3,   # gap between mana cost symbols
}

# Line heights in mm
_LINE_MM = {
    "rules":   3.0,
    "flavor":  2.8,
}

# Outline widths in mm
_OUTLINE_MM = {
    "thin":  0.2,
    "thick": 0.3,
}


def _mm2px(mm: float, dpi: int) -> int:
    """Convert millimetres to pixels at the given DPI."""
    return max(1, round(mm / 25.4 * dpi))


def _pt2px(pt: float, dpi: int) -> int:
    """Convert typographic points to pixels at the given DPI."""
    return max(1, round(pt / 72.0 * dpi))


# ---------------------------------------------------------------------------
# Colour palette (DPI-independent)
# ---------------------------------------------------------------------------
COLOR_FRAMES = {
    "W": (248, 231, 185),
    "U": (14, 104, 171),
    "B": (21, 11, 0),
    "R": (211, 32, 42),
    "G": (0, 115, 62),
}
GOLD_FRAME = (201, 175, 103)
COLORLESS_FRAME = (194, 192, 189)
BLACK_FRAME_TEXT = (240, 240, 240)

MANA_CIRCLE_COLORS = {
    "W": (255, 251, 213),
    "U": (170, 224, 250),
    "B": (166, 159, 157),
    "R": (249, 170, 143),
    "G": (155, 211, 174),
    "C": (204, 194, 183),
    "T": (204, 194, 183),
    "Q": (204, 194, 183),
    "X": (204, 194, 183),
    "S": (204, 194, 183),
    "E": (204, 194, 183),
}

SYMBOL_FILE_MAP = {
    "T": "tap", "Q": "untap",
    "W": "w", "U": "u", "B": "b", "R": "r", "G": "g", "C": "c",
    "S": "s", "X": "x", "E": "e",
    "W/U": "wu", "U/B": "ub", "B/R": "br", "R/G": "rg", "G/W": "gw",
    "W/B": "wb", "U/R": "ur", "B/G": "bg", "R/W": "rw", "G/U": "gu",
    "W/P": "wp", "U/P": "up", "B/P": "bp", "R/P": "rp", "G/P": "gp",
}

RARITY_COLORS = {
    "common":   (20, 20, 20),
    "uncommon": (140, 152, 161),
    "rare":     (206, 172, 0),
    "mythic":   (213, 51, 0),
}

# ---------------------------------------------------------------------------
# Enhanced frame styling — M15+ realistic card frame
# ---------------------------------------------------------------------------

# Pinline colors: thin decorative borders between card elements
PINLINE_COLORS = {
    "W": (194, 172, 110),
    "U": (8, 72, 130),
    "B": (90, 80, 78),
    "R": (155, 18, 28),
    "G": (0, 82, 40),
}
GOLD_PINLINE = (160, 135, 55)
COLORLESS_PINLINE = (135, 133, 130)

# Frame gradient: (light, mid, dark) for vignette effect
FRAME_GRADIENTS = {
    "W": ((255, 245, 215), (248, 231, 185), (218, 198, 145)),
    "U": ((28, 132, 202), (14, 104, 171), (5, 72, 128)),
    "B": ((72, 62, 76), (45, 37, 50), (20, 14, 24)),
    "R": ((238, 58, 62), (211, 32, 42), (158, 14, 24)),
    "G": ((18, 150, 85), (0, 115, 62), (0, 82, 40)),
}
GOLD_FRAME_GRADIENT = ((228, 204, 135), (201, 175, 103), (165, 140, 72))
COLORLESS_FRAME_GRADIENT = ((218, 216, 213), (194, 192, 189), (162, 160, 157))

# Title / type bar gradient: (top, bottom) for vertical gradient fill
BAR_GRADIENTS = {
    "W": ((255, 250, 228), (242, 225, 178)),
    "U": ((35, 142, 215), (10, 90, 158)),
    "B": ((82, 72, 86), (40, 32, 45)),
    "R": ((245, 72, 72), (198, 28, 38)),
    "G": ((25, 158, 92), (0, 102, 52)),
}
GOLD_BAR_GRADIENT = ((235, 215, 150), (195, 168, 98))
COLORLESS_BAR_GRADIENT = ((225, 223, 220), (185, 183, 180))

# Parchment text box gradient
TEXTBOX_TOP = (255, 253, 245)
TEXTBOX_BOTTOM = (245, 238, 218)

# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

def _load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


# Synthetic italic: shear regular text when no italic font file is available.
_ITALIC_SHEAR = 0.2   # ~12° slant, close to typical italic

def _draw_italic_text(img: Image.Image, xy: tuple[int, int], text: str,
                      font: ImageFont.FreeTypeFont, fill, is_synthetic: bool):
    """Draw text with italic styling.  Uses the font directly if it is a true
    italic face; otherwise renders into a temp image and applies an affine shear."""
    if not is_synthetic:
        draw = ImageDraw.Draw(img)
        draw.text(xy, text, fill=fill, font=font)
        return
    # Measure text
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    # Shear leans the top rightward; pad only by the shear amount at the
    # baseline so the bottom-left of the text lands exactly at xy (no indent).
    shear_off = int(_ITALIC_SHEAR * th) + 2
    tmp = Image.new("RGBA", (tw + shear_off + 2, th + 4), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((-bbox[0], -bbox[1]), text, fill=fill, font=font)
    tmp = tmp.transform(tmp.size, Image.AFFINE,
                        (1, _ITALIC_SHEAR, -shear_off, 0, 1, 0),
                        resample=Image.BICUBIC)
    img.paste(tmp, xy, tmp)


# Font cache keyed by (name, size)
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def _get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = _load_font(name, size)
    return _font_cache[key]


def _fit_font_to_width(
    font_name: str,
    text: str,
    max_w: int,
    base_pt: float,
    dpi: int,
    min_pt: float = 4.5,
) -> tuple[ImageFont.FreeTypeFont, int]:
    """Return (font, size_px) for `text` shrunk to fit within `max_w` pixels.

    Starts at `base_pt` and steps down by 0.25 pt until the rendered width
    is ≤ `max_w` or `min_pt` is reached. Real MTG cards do the same thing —
    the title font shrinks substantially for long names ("Borborygmos
    Enraged," "Our Market Research Shows That Players Like Really Long
    Card Names...") and Beleren is legible down to ~4.5 pt at print DPI.
    """
    pt = float(base_pt)
    while pt > min_pt:
        size_px = _pt2px(pt, dpi)
        font = _get_font(font_name, size_px)
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        if text_w <= max_w:
            return font, size_px
        pt -= 0.25
    # Floor: return the smallest size even if it still overflows.
    size_px = _pt2px(min_pt, dpi)
    return _get_font(font_name, size_px), size_px


# ---------------------------------------------------------------------------
# Mana symbol rendering
# ---------------------------------------------------------------------------

_MANA_RE = re.compile(r"\{([^}]+)\}")


def _parse_mana_cost(cost: str) -> list[str]:
    if not cost:
        return []
    return _MANA_RE.findall(cost)


def _render_mana_symbol(symbol: str, size: int = 32) -> Image.Image:
    """Render a single mana symbol as a circular image."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    sym_upper = symbol.upper()
    if sym_upper in MANA_CIRCLE_COLORS:
        bg = MANA_CIRCLE_COLORS[sym_upper]
    elif "/" in sym_upper:
        first = sym_upper.split("/")[0]
        bg = MANA_CIRCLE_COLORS.get(first, (204, 194, 183))
    else:
        bg = (204, 194, 183)

    ow = max(1, size // 16)  # outline scales with symbol size
    draw.ellipse([1, 1, size - 2, size - 2], fill=bg, outline=(0, 0, 0), width=ow)

    # Try SVG
    svg_name = SYMBOL_FILE_MAP.get(sym_upper, symbol.lower())
    svg_path = SYMBOLS_DIR / f"{svg_name}.svg"
    if not svg_path.exists():
        svg_path = SYMBOLS_DIR / f"{symbol.lower()}.svg"
    if svg_path.exists():
        try:
            import cairosvg
            inner_size = int(size * 0.55)
            png_data = cairosvg.svg2png(url=str(svg_path), output_width=inner_size, output_height=inner_size)
            sym_img = Image.open(BytesIO(png_data)).convert("RGBA")
            offset = (size - inner_size) // 2
            img.paste(sym_img, (offset, offset), sym_img)
            return img
        except Exception:
            pass

    # Fallback: text
    font = _get_font("Beleren-Bold.ttf", int(size * 0.55))
    text = sym_upper
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) // 2, (size - th) // 2 - 2), text, fill=(0, 0, 0), font=font)
    return img


def _draw_mana_cost(img: Image.Image, symbols: list[str], right_x: int, y: int,
                    sym_size: int = 32, gap: int = 3):
    """Draw mana symbols right-aligned ending at right_x."""
    total_w = len(symbols) * sym_size + max(0, len(symbols) - 1) * gap
    x = right_x - total_w
    for s in symbols:
        sym_img = _render_mana_symbol(s, sym_size)
        img.paste(sym_img, (x, y), sym_img)
        x += sym_size + gap


# ---------------------------------------------------------------------------
# Colour logic
# ---------------------------------------------------------------------------

def _infer_colors(card: dict) -> list[str]:
    colors = card.get("color") or card.get("colors") or []
    if isinstance(colors, str):
        colors = [colors]
    if not colors and card.get("mana_cost"):
        found = set()
        for sym in _parse_mana_cost(card["mana_cost"]):
            if sym.upper() in "WUBRG":
                found.add(sym.upper())
        colors = sorted(found, key="WUBRG".index)
    return colors


def _frame_color(colors: list[str]) -> tuple:
    if not colors:
        return COLORLESS_FRAME
    if len(colors) == 1:
        return COLOR_FRAMES.get(colors[0], COLORLESS_FRAME)
    return GOLD_FRAME


def _text_color_for_frame(frame_color: tuple) -> tuple:
    brightness = 0.299 * frame_color[0] + 0.587 * frame_color[1] + 0.114 * frame_color[2]
    return (0, 0, 0) if brightness > 128 else BLACK_FRAME_TEXT


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _measure_text_with_symbols(draw, text, font, sym_size=22):
    parts = re.split(r"(\{[^}]+\})", text)
    total = 0
    for part in parts:
        if _MANA_RE.match(part):
            total += sym_size + 2
        else:
            bbox = draw.textbbox((0, 0), part, font=font)
            total += bbox[2] - bbox[0]
    return total


def _wrap_text(draw, text, font, max_width, sym_size=22):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            test = current + " " + word
            if _measure_text_with_symbols(draw, test, font, sym_size) <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _draw_rules_line(img, draw, line, x, y, font, fill, sym_size):
    parts = re.split(r"(\{[^}]+\})", line)
    cx = x
    for part in parts:
        m = _MANA_RE.match(part)
        if m:
            sym = m.group(1)
            sym_img = _render_mana_symbol(sym, sym_size)
            img.paste(sym_img, (cx, y + 2), sym_img)
            cx += sym_size + 2
        else:
            draw.text((cx, y), part, fill=fill, font=font)
            bbox = draw.textbbox((0, 0), part, font=font)
            cx += bbox[2] - bbox[0]


# ---------------------------------------------------------------------------
# Art: load external image or fall back to procedural gradient
# ---------------------------------------------------------------------------

def _load_and_crop_art(image_path: str, target_w: int, target_h: int) -> Image.Image | None:
    """Load an image from disk and crop/resize it to fill the art box.

    Uses a centre-crop strategy: scale the image so it fully covers the
    target dimensions, then crop the excess from the centre.  This avoids
    distortion and guarantees the art box is completely filled.
    """
    try:
        src = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"  Warning: could not load art image '{image_path}': {e}")
        return None

    src_w, src_h = src.size
    # Scale so the smaller axis matches the target
    scale = max(target_w / src_w, target_h / src_h)
    new_w = round(src_w * scale)
    new_h = round(src_h * scale)
    src = src.resize((new_w, new_h), Image.LANCZOS)

    # Centre-crop to exact target size
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return src.crop((left, top, left + target_w, top + target_h))


def _generate_art_fallback(colors, width, height, texture_gap=12):
    """Procedural gradient placeholder when no art image is available."""
    img = Image.new("RGB", (width, height), (40, 40, 40))
    draw = ImageDraw.Draw(img)

    if not colors:
        c1, c2 = (100, 100, 110), (60, 60, 70)
    elif len(colors) == 1:
        base = COLOR_FRAMES.get(colors[0], (100, 100, 100))
        c1 = tuple(min(255, c + 60) for c in base)
        c2 = tuple(max(0, c - 40) for c in base)
    else:
        c1 = COLOR_FRAMES.get(colors[0], (100, 100, 100))
        c2 = COLOR_FRAMES.get(colors[-1], (100, 100, 100))

    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    for i in range(0, width, texture_gap):
        draw.line([(i, 0), (i + height // 3, height)], fill=(255, 255, 255), width=1)

    return img


def _get_art_image(card: dict, target_w: int, target_h: int, colors: list,
                   texture_gap: int = 12) -> Image.Image:
    """Return the art image for a card.

    Priority:
      1. card["art_image"] — path to a local image file (pre-fetched or generated)
      2. Procedural gradient fallback based on card colours
    """
    art_path = card.get("art_image") or card.get("art_path")
    if art_path and os.path.isfile(art_path):
        cropped = _load_and_crop_art(art_path, target_w, target_h)
        if cropped is not None:
            return cropped

    return _generate_art_fallback(colors, target_w, target_h, texture_gap)


# ---------------------------------------------------------------------------
# Frame drawing helpers — gradients, pinlines, texture
# ---------------------------------------------------------------------------


def _pinline_color(colors: list[str]) -> tuple:
    """Get pinline color for a card's colour identity."""
    if not colors:
        return COLORLESS_PINLINE
    if len(colors) == 1:
        return PINLINE_COLORS.get(colors[0], COLORLESS_PINLINE)
    return GOLD_PINLINE


def _frame_gradient(colors: list[str]) -> tuple:
    """Get (light, mid, dark) gradient for the frame background."""
    if not colors:
        return COLORLESS_FRAME_GRADIENT
    if len(colors) == 1:
        return FRAME_GRADIENTS.get(colors[0], COLORLESS_FRAME_GRADIENT)
    return GOLD_FRAME_GRADIENT


def _bar_gradient(colors: list[str]) -> tuple:
    """Get (top, bottom) gradient for title / type bars."""
    if not colors:
        return COLORLESS_BAR_GRADIENT
    if len(colors) == 1:
        return BAR_GRADIENTS.get(colors[0], COLORLESS_BAR_GRADIENT)
    return GOLD_BAR_GRADIENT


def _draw_vgradient(img: Image.Image, x0: int, y0: int, x1: int, y1: int,
                    top_color: tuple, bottom_color: tuple, radius: int = 0):
    """Draw a rectangle with vertical gradient fill, optionally rounded."""
    w = x1 - x0 + 1
    h = y1 - y0 + 1
    if w <= 0 or h <= 0:
        return
    bar = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(bar)
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        d.line([(0, y), (w - 1, y)], fill=(r, g, b))
    if radius > 0:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1),
                                               radius=radius, fill=255)
        img.paste(bar, (x0, y0), mask)
    else:
        img.paste(bar, (x0, y0))


def _draw_frame_bg(img: Image.Image, x0: int, y0: int, x1: int, y1: int,
                   gradient: tuple, radius: int = 0):
    """Draw the coloured frame background with a subtle vignette gradient.

    *gradient* is (light, mid, dark) — centre row is brightest, edges darker.
    """
    light, mid, dark = gradient
    w = x1 - x0 + 1
    h = y1 - y0 + 1
    if w <= 0 or h <= 0:
        return
    frame = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(frame)
    cy = h // 2
    for y in range(h):
        t = abs(y - cy) / max(cy, 1)
        t = min(1.0, t)
        r = int(mid[0] + (light[0] - mid[0]) * (1 - t) * 0.3
                + (dark[0] - mid[0]) * t * 0.5)
        g = int(mid[1] + (light[1] - mid[1]) * (1 - t) * 0.3
                + (dark[1] - mid[1]) * t * 0.5)
        b = int(mid[2] + (light[2] - mid[2]) * (1 - t) * 0.3
                + (dark[2] - mid[2]) * t * 0.5)
        d.line([(0, y), (w - 1, y)],
               fill=(max(0, min(255, r)), max(0, min(255, g)),
                     max(0, min(255, b))))
    if radius > 0:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1),
                                               radius=radius, fill=255)
        img.paste(frame, (x0, y0), mask)
    else:
        img.paste(frame, (x0, y0))


def _add_frame_texture(img: Image.Image, x0: int, y0: int, x1: int, y1: int,
                       intensity: int = 8):
    """Add subtle organic noise texture to a frame region.

    Generates noise at 1/8 resolution, upscales and blurs for an organic
    feel, then applies as brightness modulation via ImageChops.add.
    """
    w, h = x1 - x0, y1 - y0
    if w <= 4 or h <= 4:
        return
    crop = img.crop((x0, y0, x1, y1))
    nw, nh = max(2, w // 8), max(2, h // 8)
    noise = Image.frombytes("L", (nw, nh), os.urandom(nw * nh))
    noise = noise.resize((w, h), Image.BILINEAR)
    noise = noise.filter(ImageFilter.GaussianBlur(max(1, w // 80)))
    # Normalize to 128 ± intensity
    nmin, nmax = noise.getextrema()
    if nmax <= nmin:
        return
    scale = 2.0 * intensity / (nmax - nmin)
    centre = (nmin + nmax) / 2.0
    noise = noise.point(
        lambda p: max(0, min(255, int(128 + (p - centre) * scale))))
    noise_rgb = Image.merge("RGB", [noise, noise, noise])
    # Brightness modulation: result = crop + (noise − 128)
    result = ImageChops.add(crop, noise_rgb, 1, -128)
    img.paste(result, (x0, y0))


# ---------------------------------------------------------------------------
# Frame image loading — real M15+ card frame overlays
# ---------------------------------------------------------------------------

# Map card colour identity to frame image filename
_FRAME_FILE_MAP = {
    "W": "w", "U": "u", "B": "b", "R": "r", "G": "g",
}

# Cache: (color_key, w, h) → Image or None
_frame_cache: dict[tuple, Image.Image | None] = {}
_pt_cache: dict[tuple, Image.Image | None] = {}


def _frame_file_key(colors: list[str]) -> str:
    """Map card colours to frame filename (without extension)."""
    if not colors:
        return "c"       # colorless
    if len(colors) == 1:
        return _FRAME_FILE_MAP.get(colors[0], "c")
    return "m"           # multicolor / gold


def _load_frame_image(colors: list[str], card_w: int,
                      card_h: int) -> Image.Image | None:
    """Load and resize the real card frame overlay for the given colours.

    Returns an RGBA image at (card_w, card_h) with transparent art window,
    or None if the frame image file is not available (triggers procedural
    fallback).
    """
    key = (_frame_file_key(colors), card_w, card_h)
    if key in _frame_cache:
        return _frame_cache[key]

    path = FRAMES_DIR / f"{key[0]}.png"
    if not path.exists():
        print(f"  WARNING: frame PNG not found at '{path}' — "
              f"falling back to procedural gradient for '{key[0]}' cards. "
              f"Expected files: w.png, u.png, b.png, r.png, g.png, m.png, c.png in {FRAMES_DIR}")
        _frame_cache[key] = None
        return None

    try:
        frame = Image.open(path).convert("RGBA")
        if frame.size != (card_w, card_h):
            frame = frame.resize((card_w, card_h), Image.LANCZOS)
        _frame_cache[key] = frame
        return frame
    except Exception as e:
        print(f"  WARNING: could not load frame '{path}': {e} — falling back to procedural gradient")
        _frame_cache[key] = None
        return None


def _load_pt_image(colors: list[str], target_w: int,
                   target_h: int) -> Image.Image | None:
    """Load and resize the P/T box overlay for creatures."""
    fk = _frame_file_key(colors).upper()
    key = (fk, target_w, target_h)
    if key in _pt_cache:
        return _pt_cache[key]

    path = PT_DIR / f"m15PT{fk}.png"
    if not path.exists():
        print(f"  WARNING: P/T overlay not found at '{path}' — "
              f"falling back to procedural P/T box for '{fk}' creatures")
        _pt_cache[key] = None
        return None

    try:
        pt = Image.open(path).convert("RGBA")
        if pt.size != (target_w, target_h):
            pt = pt.resize((target_w, target_h), Image.LANCZOS)
        _pt_cache[key] = pt
        return pt
    except Exception as e:
        print(f"  WARNING: could not load PT image '{path}': {e} — falling back to procedural P/T box")
        _pt_cache[key] = None
        return None


# ---------------------------------------------------------------------------
# Main card renderer
# ---------------------------------------------------------------------------

def render_card(card: dict, dpi: int = 300) -> Image.Image:
    """Render a single MTG card to a PIL Image at the given DPI.

    At 300 DPI the output is 744 × 1039 px — the exact physical size of
    a real MTG card (63 × 88 mm) at print resolution.  Every element is
    positioned using real-world millimetre measurements taken from actual
    MTG cards (M15+ frame).
    """
    mm = lambda v: _mm2px(v, dpi)  # shorthand

    # --- Pixel dimensions for this DPI ---
    card_w = round(CARD_WIDTH_IN * dpi)
    card_h = round(CARD_HEIGHT_IN * dpi)

    # Layout values (all from mm)
    L = _LAYOUT_MM
    border_top   = mm(L["border_top"])
    border_side  = mm(L["border_side"])
    border_bot   = mm(L["border_bottom"])
    inner_pad    = mm(L["inner_pad"])
    corner_r     = mm(L["corner_radius"])
    tb_offset    = mm(L["title_bar_offset"])
    tb_h         = mm(L["title_bar_h"])
    art_gap      = mm(L["art_gap"])
    art_h        = mm(L["art_h"])
    type_h       = mm(L["type_bar_h"])
    text_gap     = mm(L["text_box_gap"])
    footer_h     = mm(L["footer_h"])
    pt_w         = mm(L["pt_box_w"])
    pt_h         = mm(L["pt_box_h"])
    gem_hw       = mm(L["gem_hw"])
    gem_hh       = mm(L["gem_hh"])

    mana_sym     = mm(_SYM_MM["mana_cost"])
    inline_sym   = mm(_SYM_MM["inline"])
    mana_gap     = mm(_SYM_MM["mana_gap"])

    rules_lh     = mm(_LINE_MM["rules"])
    flavor_lh    = mm(_LINE_MM["flavor"])

    ow_thin      = mm(_OUTLINE_MM["thin"])
    ow_thick     = mm(_OUTLINE_MM["thick"])
    texture_gap  = max(4, mm(1.0))

    # Fonts (point sizes → pixels)
    F = _FONT_PT
    f_title    = _get_font("Beleren-Bold.ttf", _pt2px(F["title"], dpi))
    f_type     = _get_font("Beleren-Bold.ttf", _pt2px(F["type"], dpi))
    f_rules    = _get_font("MPlantin.ttf",     _pt2px(F["rules"], dpi))
    # Prefer true italic font; fall back to regular + synthetic shear
    _italic_font_name = "MPlantin-Italic.ttf"
    _synthetic_italic = not (FONTS_DIR / _italic_font_name).exists()
    if _synthetic_italic:
        _italic_font_name = "MPlantin.ttf"
    f_rules_it = _get_font(_italic_font_name,  _pt2px(F["rules_italic"], dpi))
    f_pt       = _get_font("Beleren-Bold.ttf", _pt2px(F["pt"], dpi))
    f_small    = _get_font("MPlantin.ttf",     _pt2px(F["small"], dpi))

    # --- Card data ---
    colors     = _infer_colors(card)
    frame_col  = _frame_color(colors)
    text_col   = _text_color_for_frame(frame_col)

    name        = card.get("name", "Unnamed")
    mana_cost   = card.get("mana_cost", "")
    card_type   = card.get("type", card.get("type_line", ""))
    rules_text  = card.get("rules_text", card.get("oracle_text", ""))
    flavor_text = card.get("flavor_text", "")
    power       = card.get("power")
    toughness   = card.get("toughness")
    rarity      = card.get("rarity", "common").lower()
    is_creature = power is not None and toughness is not None

    # --- Create image ---
    img = Image.new("RGB", (card_w, card_h), (0, 0, 0))
    px = lambda v: _mm2px(v, dpi)

    # --- Layout positions (shared by both frame paths) ---
    ix0 = border_side
    iy0 = border_top
    ix1 = card_w - border_side
    iy1 = card_h - border_bot
    cx0 = ix0 + inner_pad
    cx1 = ix1 - inner_pad

    tb_y0 = iy0 + tb_offset
    tb_y1 = tb_y0 + tb_h
    art_y0 = tb_y1 + art_gap
    art_y1 = art_y0 + art_h
    art_w = cx1 - cx0
    tp_y0 = art_y1 + art_gap
    tp_y1 = tp_y0 + type_h
    tx_y0 = tp_y1 + text_gap
    tx_y1 = iy1 - footer_h

    pt_x1 = cx1 - px(0.4)
    pt_x0 = pt_x1 - pt_w
    pt_y1_ = tx_y1 + px(0.4)
    pt_y0_ = pt_y1_ - pt_h

    # =====================================================================
    # Phase 1 — Art
    # =====================================================================
    art_img = _get_art_image(card, art_w, art_h, colors, texture_gap)

    # =====================================================================
    # Phase 2 — Frame (real image overlay, or procedural fallback)
    # =====================================================================
    frame_overlay = _load_frame_image(colors, card_w, card_h)

    if frame_overlay is not None:
        # --- Real card frame image ---
        # Place art first; frame overlay has transparent art window
        img.paste(art_img, (cx0, art_y0))
        img.paste(frame_overlay, (0, 0), frame_overlay)
        # P/T box overlay for creatures
        if is_creature:
            pt_overlay = _load_pt_image(colors, pt_w, pt_h)
            if pt_overlay is not None:
                img.paste(pt_overlay, (pt_x0, pt_y0_), pt_overlay)
    else:
        # --- Procedural frame (gradient + pinline fallback) ---
        draw = ImageDraw.Draw(img)
        pin_w = max(1, px(0.15))
        pin_col = _pinline_color(colors)
        frame_grad = _frame_gradient(colors)
        bar_grad = _bar_gradient(colors)
        bevel_hl = tuple(min(255, c + 40) for c in bar_grad[0])
        bevel_sh = tuple(max(0, c - 30) for c in bar_grad[1])

        # Black border
        draw.rounded_rectangle((0, 0, card_w - 1, card_h - 1),
                               radius=corner_r, fill=(0, 0, 0))
        # Frame background with gradient + texture
        frame_r = max(1, corner_r - px(0.5))
        _draw_frame_bg(img, ix0, iy0, ix1, iy1, frame_grad, radius=frame_r)
        _add_frame_texture(img, ix0, iy0, ix1, iy1, intensity=8)
        draw = ImageDraw.Draw(img)

        # Title bar
        bar_r = max(1, px(0.8))
        draw.rounded_rectangle(
            (cx0 - pin_w, tb_y0 - pin_w, cx1 + pin_w, tb_y1 + pin_w),
            radius=bar_r + pin_w, fill=pin_col)
        _draw_vgradient(img, cx0, tb_y0, cx1, tb_y1,
                        bar_grad[0], bar_grad[1], radius=bar_r)
        draw = ImageDraw.Draw(img)
        draw.line([(cx0 + bar_r, tb_y0 + 1), (cx1 - bar_r, tb_y0 + 1)],
                  fill=bevel_hl, width=max(1, px(0.08)))
        draw.line([(cx0 + bar_r, tb_y1 - 1), (cx1 - bar_r, tb_y1 - 1)],
                  fill=bevel_sh, width=max(1, px(0.08)))

        # Art pinline + art
        draw.rectangle(
            (cx0 - pin_w, art_y0 - pin_w, cx1 + pin_w, art_y1 + pin_w),
            fill=pin_col)
        img.paste(art_img, (cx0, art_y0))
        draw = ImageDraw.Draw(img)

        # Type line
        type_r = max(1, px(0.6))
        draw.rounded_rectangle(
            (cx0 - pin_w, tp_y0 - pin_w, cx1 + pin_w, tp_y1 + pin_w),
            radius=type_r + pin_w, fill=pin_col)
        _draw_vgradient(img, cx0, tp_y0, cx1, tp_y1,
                        bar_grad[0], bar_grad[1], radius=type_r)
        draw = ImageDraw.Draw(img)
        draw.line([(cx0 + type_r, tp_y0 + 1), (cx1 - type_r, tp_y0 + 1)],
                  fill=bevel_hl, width=max(1, px(0.08)))
        draw.line([(cx0 + type_r, tp_y1 - 1), (cx1 - type_r, tp_y1 - 1)],
                  fill=bevel_sh, width=max(1, px(0.08)))

        # Text box
        text_r = max(1, px(0.6))
        draw.rounded_rectangle(
            (cx0 - pin_w, tx_y0 - pin_w, cx1 + pin_w, tx_y1 + pin_w),
            radius=text_r + pin_w, fill=pin_col)
        _draw_vgradient(img, cx0, tx_y0, cx1, tx_y1,
                        TEXTBOX_TOP, TEXTBOX_BOTTOM, radius=text_r)
        draw = ImageDraw.Draw(img)

        # P/T box (procedural)
        if is_creature:
            pt_r = max(1, px(0.8))
            draw.rounded_rectangle(
                (pt_x0 - pin_w, pt_y0_ - pin_w, pt_x1 + pin_w, pt_y1_ + pin_w),
                radius=pt_r + pin_w, fill=pin_col)
            _draw_vgradient(img, pt_x0, pt_y0_, pt_x1, pt_y1_,
                            bar_grad[0], bar_grad[1], radius=pt_r)
            draw = ImageDraw.Draw(img)
            draw.line([(pt_x0 + pt_r, pt_y0_ + 1), (pt_x1 - pt_r, pt_y0_ + 1)],
                      fill=bevel_hl, width=max(1, px(0.08)))

    # =====================================================================
    # Phase 3 — Text rendering (same for both frame paths)
    # =====================================================================
    draw = ImageDraw.Draw(img)

    # Mana cost symbols — measured first so the title knows how much space it has
    mana_symbols = _parse_mana_cost(mana_cost)
    mana_total_w = 0
    if mana_symbols:
        mana_total_w = (len(mana_symbols) * mana_sym
                        + max(0, len(mana_symbols) - 1) * mana_gap)

    # Card name — fit font to the horizontal space left of the mana cost.
    name_left = cx0 + px(1.2)
    if mana_symbols:
        # Mana cost is right-aligned at (cx1 - px(0.8)) and extends left by
        # mana_total_w. Reserve px(1.0) of breathing room between title and cost.
        name_right = cx1 - px(0.8) - mana_total_w - px(1.0)
    else:
        name_right = cx1 - px(0.8)
    name_max_w = max(px(1.0), name_right - name_left)
    f_title_fitted, name_size_px = _fit_font_to_width(
        "Beleren-Bold.ttf", name, name_max_w, F["title"], dpi)
    name_y = tb_y0 + (tb_h - name_size_px) // 2
    draw.text((name_left, name_y), name, fill=(0, 0, 0), font=f_title_fitted)

    if mana_symbols:
        sym_y = tb_y0 + (tb_h - mana_sym) // 2
        _draw_mana_cost(img, mana_symbols, cx1 - px(0.8), sym_y,
                        sym_size=mana_sym, gap=mana_gap)

    # Type line text — always black
    type_text_y = tp_y0 + (type_h - _pt2px(F["type"], dpi)) // 2
    draw.text((cx0 + px(1.0), type_text_y), card_type, fill=(0, 0, 0), font=f_type)

    # Rarity gem — diamond shape, right side of type line
    rar_col = RARITY_COLORS.get(rarity, RARITY_COLORS["common"])
    rar_cx = cx1 - px(2.2)
    rar_cy = tp_y0 + type_h // 2
    gem_pts = [
        (rar_cx, rar_cy - gem_hh),
        (rar_cx + gem_hw, rar_cy),
        (rar_cx, rar_cy + gem_hh),
        (rar_cx - gem_hw, rar_cy),
    ]
    draw.polygon(gem_pts, fill=rar_col, outline=(0, 0, 0), width=ow_thin)
    hl = tuple(min(255, c + 80) for c in rar_col)
    draw.polygon([
        (rar_cx, rar_cy - gem_hh + px(0.3)),
        (rar_cx + gem_hw - px(0.4), rar_cy - px(0.2)),
        (rar_cx, rar_cy + px(0.2)),
        (rar_cx - px(0.2), rar_cy - px(0.4)),
    ], fill=hl)

    # Rules text
    text_left = cx0 + px(1.2)
    text_max_w = (cx1 - cx0) - px(2.4)
    cursor_y = tx_y0 + px(1.0)

    if rules_text:
        lines = _wrap_text(draw, rules_text, f_rules, text_max_w, inline_sym)
        for line in lines:
            if cursor_y + rules_lh > tx_y1 - px(1.0):
                break
            _draw_rules_line(img, draw, line, text_left, cursor_y,
                             f_rules, (0, 0, 0), inline_sym)
            cursor_y += rules_lh

    # Flavor text
    if flavor_text:
        cursor_y += px(0.8)
        if cursor_y + px(0.4) < tx_y1 - px(3.0):
            draw.line([(text_left + px(2.0), cursor_y),
                       (cx1 - px(3.2), cursor_y)],
                      fill=(160, 150, 140), width=max(1, px(0.1)))
            cursor_y += px(0.8)
            fl_lines = _wrap_text(draw, flavor_text, f_rules_it,
                                  text_max_w, inline_sym)
            for line in fl_lines:
                if cursor_y + flavor_lh > tx_y1 - px(0.8):
                    break
                _draw_italic_text(img, (text_left, cursor_y), line,
                                  f_rules_it, fill=(80, 70, 60),
                                  is_synthetic=_synthetic_italic)
                cursor_y += flavor_lh

    # Power / Toughness text
    if is_creature:
        pt_text = f"{power}/{toughness}"
        draw.text((pt_x0 + pt_w / 2 + px(0.8), pt_y0_ + pt_h / 2),
                  pt_text, fill=(0, 0, 0), font=f_pt, anchor="mm")

    # Footer (collector info)
    footer_y = iy1 - footer_h + px(0.5)
    card_id = card.get("id", "")
    footer_text = f"{card_id}  •  {rarity.upper()}" if card_id else rarity.upper()
    draw.text((cx0 + px(1.0), footer_y), footer_text, fill=text_col, font=f_small)

    return img


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def load_cards(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "cards" in data:
            return data["cards"]
        return [data]
    return []


def _save_png_with_dpi(img: Image.Image, path: str, dpi: int):
    """Save a PNG with DPI metadata so print software knows the intended size."""
    # PPI → pixels per metre (PNG pHYs chunk)
    ppm = round(dpi / 0.0254)
    info = PngImagePlugin.PngInfo()
    # Pillow uses the 'dpi' key in info for saving
    img.save(path, "PNG", dpi=(dpi, dpi), pnginfo=info)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Render MTG cards as PNG images at exact physical card dimensions.")
    parser.add_argument("input", nargs="?", help="Path to JSON file with card data")
    parser.add_argument("--output-dir", default="./card_images", help="Output directory")
    parser.add_argument("--dpi", type=int, default=300,
                        help="Target DPI (300 = standard print, 600 = high-res). "
                             "At 300 DPI output is 744×1039 px = exact MTG card size.")
    parser.add_argument("--filter-rarity", help="Only render cards of this rarity")
    parser.add_argument("--filter-color", help="Only render cards of this color (W/U/B/R/G)")

    # Single-card mode
    parser.add_argument("--single", action="store_true", help="Render one card from CLI args")
    parser.add_argument("--name", help="Card name")
    parser.add_argument("--mana-cost", help="Mana cost, e.g. {3}{R}{R}")
    parser.add_argument("--type", dest="card_type", help="Type line")
    parser.add_argument("--rules", help="Rules text")
    parser.add_argument("--flavor", help="Flavor text")
    parser.add_argument("--power", help="Power")
    parser.add_argument("--toughness", help="Toughness")
    parser.add_argument("--rarity", default="common", help="Rarity")
    parser.add_argument("--color", help="Color(s), e.g. R or WU")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    dpi = args.dpi
    card_w = round(CARD_WIDTH_IN * dpi)
    card_h = round(CARD_HEIGHT_IN * dpi)
    print(f"Target DPI: {dpi}  →  {card_w} × {card_h} px  "
          f"({CARD_WIDTH_IN * 25.4:.0f} × {CARD_HEIGHT_IN * 25.4:.0f} mm)")

    if args.single:
        card = {
            "name": args.name or "Unnamed Card",
            "mana_cost": args.mana_cost or "",
            "type": args.card_type or "Unknown Type",
            "rules_text": args.rules or "",
            "flavor_text": args.flavor or "",
            "rarity": args.rarity,
        }
        if args.power is not None:
            card["power"] = args.power
        if args.toughness is not None:
            card["toughness"] = args.toughness
        if args.color:
            card["color"] = list(args.color.upper())
        cards = [card]
    elif args.input:
        cards = load_cards(args.input)
    else:
        parser.error("Provide a JSON file path or use --single mode")
        return

    if args.filter_rarity:
        cards = [c for c in cards if c.get("rarity", "").lower() == args.filter_rarity.lower()]
    if args.filter_color:
        fc = args.filter_color.upper()
        cards = [c for c in cards if fc in _infer_colors(c)]

    if not cards:
        print("No cards to render after filtering.")
        return

    print(f"Rendering {len(cards)} card(s)...")
    saved = 0
    for i, card in enumerate(cards):
        img = render_card(card, dpi=dpi)
        safe_name = re.sub(r'[^\w\-]', '_', card.get("name", f"card_{i}").lower().strip())
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')
        out_path = os.path.join(args.output_dir, f"{safe_name}.png")
        _save_png_with_dpi(img, out_path, dpi)
        saved += 1
        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(cards)} done...")

    print(f"Saved {saved} card image(s) to {args.output_dir}/")


if __name__ == "__main__":
    main()
