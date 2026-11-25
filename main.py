#!/usr/bin/env python3
"""Draw a 2x3 infographic summarising world news of 24 November 2026.

Run:  python3 main.py
Output: output/world-news-24-nov-2026.png
Only the Python standard library and Pillow are needed.
"""

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- layout ---------------------------------------------------------------
W, H = 1240, 1754
BG = (245, 243, 238)          # warm off-white
NAVY = (27, 47, 80)           # deep blue header
NAVY_DARK = (20, 36, 62)
INK = (22, 28, 43)            # body text
MUTED = (90, 96, 110)
CARD = (255, 255, 255)
BORDER = (200, 203, 210)
ACCENTS = [
    (46, 111, 180),   # NVIDIA  blue
    (178, 62, 48),    # IRAN     red
    (120, 86, 40),    # UKRAINE  ochre
    (150, 48, 48),    # GAZA     dark red
    (46, 125, 84),    # CLIMATE  green
    (146, 110, 52),   # MYANMAR  bronze
]

HEADER_H = 250
MARGIN = 48
GAP = 28
COLS, ROWS = 2, 3

ITEMS = [
    ("NVIDIA",
     "Huang returns as CEO, shares jump 30%",
     "Jensen Huang was reinstated as Nvidia CEO, less than "
     "two weeks after resigning. The stock jumped about 30%."),
    ("IRAN",
     "Hormuz tankers hit mines, blockade standoff",
     "Three oil tankers hit mines and caught fire in the "
     "Strait of Hormuz. Iran vowed to confront the US naval "
     "blockade and refused talks."),
    ("UKRAINE",
     "Zaporizhzhia strike kills 2, wounds 40",
     "An overnight Russian attack hit an apartment building "
     "in Zaporizhzhia, killing two and wounding about 40, "
     "including four children."),
    ("GAZA",
     "Israeli strike kills Hamas security chief",
     "Israeli airstrikes killed Naeem Abu Nahel, director of "
     "Hamas' internal security apparatus in Gaza, and six "
     "others."),
    ("CLIMATE",
     "COP31 ends with no fossil-fuel deal",
     "The COP31 climate summit collapsed without an agreement "
     "on fossil fuels, ending in deadlock."),
    ("MYANMAR",
     "Court rules genocide against Rohingya",
     "The International Court of Justice ruled that Myanmar "
     "committed genocide against the Rohingya people."),
]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Wrap text to fit `width` pixels, using the real font metrics."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, cx, cy, color, s=34):
    """A small line icon, drawn with plain PIL shapes."""
    if kind == 0:  # chip
        draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                       outline=color, width=4)
        draw.rectangle([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4],
                       outline=color, width=3)
        for dx in (-s // 4, 0, s // 4):
            draw.line([cx + dx, cy - s // 2 - 10, cx + dx, cy - s // 2], fill=color, width=3)
            draw.line([cx + dx, cy + s // 2, cx + dx, cy + s // 2 + 10], fill=color, width=3)
    elif kind == 1:  # tanker + warning
        draw.polygon([(cx - s, cy + 8), (cx + s, cy + 8), (cx + s - 8, cy + s // 2),
                      (cx - s + 8, cy + s // 2)], outline=color, width=4)
        draw.rectangle([cx - s // 3, cy - s // 2, cx + s // 3, cy + 6], outline=color, width=3)
        draw.line([cx - s // 3, cy - s // 2 - 8, cx - s // 3, cy - s // 2], fill=color, width=3)
    elif kind == 2:  # damaged building
        draw.rectangle([cx - s // 2, cy - s // 2, cx - 4, cy + s // 2], outline=color, width=3)
        draw.rectangle([cx + 4, cy - s // 4, cx + s // 2, cy + s // 2], outline=color, width=3)
        draw.line([cx - 4, cy - s // 2, cx + 6, cy - s // 4, cx - 2, cy + 2, cx + 8, cy + s // 4],
                  fill=color, width=3)
    elif kind == 3:  # map pin: ring, dot, point
        draw.ellipse([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 8],
                     outline=color, width=4)
        draw.ellipse([cx - 7, cy - s // 2 + 13, cx + 7, cy - s // 2 + 27],
                     fill=color)
        draw.polygon([(cx - 9, cy + s // 8 - 2), (cx + 9, cy + s // 8 - 2),
                      (cx, cy + s // 2)], fill=color)
    elif kind == 4:  # globe: circle, equator arc, small leaf
        draw.ellipse([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                     outline=color, width=4)
        draw.arc([cx - s // 2, cy - s // 4, cx + s // 2, cy + s // 4],
                 start=0, end=360, fill=color, width=3)
        draw.arc([cx - s // 4, cy - s // 2, cx + s // 4, cy + s // 2],
                 start=0, end=360, fill=color, width=3)
    else:  # scales of justice
        draw.line([cx, cy - s // 2, cx, cy + s // 2], fill=color, width=4)
        draw.line([cx - s // 2, cy - s // 2 + 6, cx + s // 2, cy - s // 2 + 6],
                  fill=color, width=4)
        draw.arc([cx - s // 2 - 4, cy - 2, cx - 6, cy + s // 2 - 6], start=0, end=180,
                 fill=color, width=3)
        draw.arc([cx + 6, cy - 2, cx + s // 2 + 4, cy + s // 2 - 6], start=0, end=180,
                 fill=color, width=3)
        draw.line([cx - s // 2, cy + s // 2, cx + s // 2, cy + s // 2], fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # --- header -----------------------------------------------------------
    draw.rectangle([0, 0, W, HEADER_H], fill=NAVY)
    draw.rectangle([0, HEADER_H - 6, W, HEADER_H], fill=NAVY_DARK)
    title_font = font("DejaVuSans-Bold.ttf", 52)
    sub_font = font("DejaVuSans.ttf", 30)
    title = "WORLD NEWS — 24 NOVEMBER 2026"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 72), title, font=title_font, fill=(255, 255, 255))
    sub = "Six stories that defined the day"
    sw = draw.textlength(sub, font=sub_font)
    draw.text(((W - sw) / 2, 158), sub, font=sub_font, fill=(170, 185, 210))

    # --- grid -------------------------------------------------------------
    grid_top = HEADER_H + MARGIN
    grid_w = W - 2 * MARGIN
    cell_w = (grid_w - GAP) // COLS
    cell_h = (H - grid_top - MARGIN - (ROWS - 1) * GAP) // ROWS

    head_font = font("DejaVuSans-Bold.ttf", 34)
    body_font = font("DejaVuSans.ttf", 26)

    for i, (head, lead, body) in enumerate(ITEMS):
        r, c = divmod(i, COLS)
        x0 = MARGIN + c * (cell_w + GAP)
        y0 = grid_top + r * (cell_h + GAP)
        x1, y1 = x0 + cell_w, y0 + cell_h
        color = ACCENTS[i]

        draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                               outline=BORDER, width=2)
        draw.line([x0 + 24, y0 + 6, x0 + 24, y1 - 6], fill=color, width=6)

        # icon, larger and centred on the heading block
        draw_icon(draw, i, x0 + 80, y0 + 84, color, s=46)

        # heading (two lines: name, then lead)
        tx = x0 + 148
        twrap = cell_w - 148 - 28
        draw.text((tx, y0 + 30), head + " —", font=head_font, fill=INK)
        lead_lines = wrap(draw, lead, head_font, twrap)
        ly = y0 + 76
        for ln in lead_lines[:3]:
            draw.text((tx, ly), ln, font=head_font, fill=INK)
            ly += 42

        # body, clear of the accent stripe on the left
        body_lines = wrap(draw, body, body_font, cell_w - 88)
        by = y0 + 216
        for ln in body_lines[:4]:
            draw.text((x0 + 44, by), ln, font=body_font, fill=MUTED)
            by += 36

    # --- footer -----------------------------------------------------------
    foot_font = font("DejaVuSans.ttf", 22)
    foot = "Sources: Just Security, Reuters, The Global Eye, CWEB — 24 November 2026"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, H - 34), foot, font=foot_font, fill=MUTED)

    os.makedirs("output", exist_ok=True)
    out = os.path.join("output", "world-news-24-nov-2026.png")
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
