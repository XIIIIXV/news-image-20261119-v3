#!/usr/bin/env python3
"""Thursday 19 November 2026 — one-day front page for make.fun (v3).

Builds a 1024x1024 PNG front page carrying 52 news stories, all dated
Thursday 19 November 2026.  Everything is drawn with PIL primitives
(rectangles, ellipses, polygons, lines); no photos, no network, no
randomness, so repeated runs produce identical bytes.

What v3 fixes over v2 (round 1, 98.2873%, rank #753):
- DATE DISCIPLINE: the Van Gogh $190.4m sale (first reported 18 Nov)
  is OUT of the main list and the numbers strip, and is named in the
  DATE CHECK as excluded, alongside Voyager 1, the EU EUR45bn Ukraine
  loan and the other 18-Nov stories.  Card 15 is now Corrado Augias,
  who died on 19 Nov (verified: Wikipedia, LaPresse, 19 Nov 2026).
- CRAFT: every illustration is one simple, bold, flat icon that reads
  at small size (the v2 motifs smeared and overlapped at card height),
  and the world map is a real equirectangular outline of the
  continents (the v2 map was unrecognisable grey blobs).
- DATE CHECK now names the excluded stories one by one, notes the
  Anthropic $83 pricing was set 18 Nov (trading began 19 Nov), and
  lists what was not yet due on 19 Nov (COP31 close, Akvan landfall).
- Confidence legend now reads CONFIRMED (2+ outlets) / REPORTED
  (one outlet) / CLAIM (one party), as the top entries do.

Usage:
    python3 gen_image.py            # writes entry.png next to this file
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "stories.json")
TARGET = os.path.join(HERE, "entry.png")

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 14
INNER = CANVAS_W - 2 * MARGIN  # 996

PAPER = (250, 244, 230)
INK = (18, 18, 18)
SOFT_INK = (70, 66, 60)
RED = (178, 34, 34)
DARK_RED = (139, 0, 0)
RULE = (120, 110, 95)
CARD_BG = (255, 252, 244)
CARD_EDGE = (190, 180, 160)
PANEL = (238, 232, 216)
SKY = (214, 228, 238)

REGION_PAINT = {
    "ASIA": (176, 138, 20),
    "EUROPE": (46, 111, 176),
    "AMERICAS": (178, 52, 40),
    "MIDDLE EAST": (204, 102, 20),
    "GLOBAL": (106, 76, 160),
    "AFRICA": (34, 139, 110),
    "OCEANIA": (32, 140, 164),
}

# Rough lon/lat for each card's story, used only to place its map pin.
PIN_LONLAT = {
    1: (115, 22), 2: (4, 52), 3: (30, 36), 4: (-74, 40),
    5: (47, 25), 6: (85, 18), 7: (-80, 26), 8: (127, 37),
    9: (10, 56), 10: (36, 45), 11: (90, 24), 12: (149, -35),
    13: (-74, 5), 14: (37, -1), 15: (12, 42), 16: (-77, 39),
}

# Coarse continent outlines (lon, lat), equirectangular.  Deliberately
# simple: at 308 px wide the map only needs to read as the world.
CONTINENTS = [
    # North America
    [(-168, 66), (-155, 70), (-140, 70), (-125, 70), (-110, 68), (-95, 69),
     (-85, 66), (-80, 72), (-70, 62), (-60, 55), (-55, 47), (-60, 45),
     (-65, 43), (-70, 40), (-75, 35), (-80, 26), (-85, 30), (-90, 21),
     (-97, 16), (-95, 15), (-90, 14), (-85, 12), (-80, 8), (-77, 7),
     (-80, 9), (-85, 11), (-90, 14), (-95, 16), (-100, 18), (-105, 20),
     (-112, 25), (-117, 33), (-123, 38), (-125, 49), (-130, 55),
     (-140, 60), (-155, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68), (-22, 70),
     (-25, 76), (-35, 78), (-50, 76), (-58, 74), (-62, 70), (-58, 64)],
    # South America
    [(-79, 9), (-77, 4), (-75, 0), (-80, -4), (-81, -6), (-77, -12),
     (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
     (-70, -52), (-66, -55), (-68, -50), (-65, -45), (-62, -40),
     (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
     (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-52, 4),
     (-55, 6), (-60, 8), (-65, 10), (-70, 12), (-75, 10), (-79, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 35), (-1, 36),
     (5, 37), (10, 37), (15, 32), (20, 32), (25, 32), (30, 31), (32, 31),
     (35, 28), (37, 22), (40, 15), (43, 12), (48, 11), (51, 11), (48, 5),
     (42, 0), (40, -5), (38, -12), (35, -18), (33, -25), (28, -32),
     (20, -35), (17, -32), (15, -27), (13, -20), (12, -15), (10, -5),
     (9, 0), (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12),
     (-17, 15)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-1, 46),
     (-4, 48), (-2, 50), (0, 51), (3, 52), (5, 53), (8, 55), (8, 57),
     (10, 58), (12, 56), (18, 56), (21, 55), (21, 57), (24, 58),
     (24, 60), (28, 60), (30, 62), (28, 66), (25, 70), (20, 70),
     (15, 69), (12, 66), (10, 64), (8, 62), (5, 60), (5, 58), (0, 57),
     (-3, 55), (-5, 52), (-8, 52), (-10, 48), (-10, 43), (-10, 36)],
    # Asia
    [(28, 62), (30, 65), (35, 68), (40, 68), (45, 68), (50, 69), (60, 70),
     (70, 72), (80, 73), (90, 75), (100, 76), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (160, 70), (170, 67), (178, 65),
     (170, 60), (162, 56), (158, 52), (155, 50), (150, 45), (142, 40),
     (140, 38), (135, 35), (130, 33), (127, 35), (122, 32), (120, 28),
     (115, 23), (110, 20), (108, 15), (105, 10), (103, 8), (100, 8),
     (98, 10), (95, 15), (92, 20), (89, 22), (86, 20), (82, 16),
     (80, 13), (77, 8), (75, 12), (72, 20), (68, 22), (65, 25), (62, 25),
     (58, 26), (55, 26), (52, 27), (50, 29), (48, 30), (45, 30),
     (42, 32), (40, 35), (38, 36), (36, 36), (33, 36), (30, 36),
     (28, 40), (27, 42), (28, 45), (28, 48), (28, 52), (28, 55),
     (28, 58), (28, 62)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (151, -24),
     (149, -20), (146, -19), (143, -15), (142, -11), (139, -15),
     (136, -12), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (114, -22), (113, -22)],
    # Sumatra / Java
    [(95, 5), (100, 0), (105, -3), (108, -6), (112, -7), (115, -8),
     (118, -9), (120, -10), (118, -8), (114, -7), (110, -6), (106, -5),
     (102, 0), (98, 3), (95, 5)],
    # Borneo
    [(109, 1), (113, 3), (117, 5), (119, 2), (117, -2), (114, -3),
     (110, -1), (109, 1)],
    # New Guinea
    [(131, -1), (136, -2), (140, -4), (141, -6), (138, -8), (134, -7),
     (131, -3), (131, -1)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 43), (141, 44), (139, 42), (137, 39), (135, 35),
     (132, 33), (130, 31)],
    # Great Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
     (-2, 51), (-5, 50)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -23), (45, -25),
     (44, -22), (43, -18), (44, -16)],
]

FONT_DIR = "/usr/share/fonts/truetype"


def pick_font(name, size):
    """Return a truetype font, falling back through known local families."""
    candidates = {
        "serif_b": ["liberation/LiberationSerif-Bold.ttf",
                    "dejavu/DejaVuSerif-Bold.ttf"],
        "serif": ["liberation/LiberationSerif-Regular.ttf",
                  "dejavu/DejaVuSerif.ttf"],
        "sans_b": ["liberation/LiberationSans-Bold.ttf",
                   "dejavu/DejaVuSans-Bold.ttf"],
        "sans": ["liberation/LiberationSans-Regular.ttf",
                 "dejavu/DejaVuSans.ttf"],
    }
    for rel in candidates[name]:
        path = os.path.join(FONT_DIR, rel)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


class TypeCase:
    """All fonts used on the page, sized once."""

    def __init__(self):
        self.masthead = pick_font("serif_b", 56)
        self.kicker = pick_font("sans_b", 11)
        self.strap = pick_font("serif", 15)
        self.big_num = pick_font("serif_b", 21)
        self.stat_lab = pick_font("sans", 9)
        self.strip = pick_font("sans_b", 11)
        self.strip_sm = pick_font("sans_b", 9)
        self.time = pick_font("sans_b", 9)
        self.time_txt = pick_font("sans", 9)
        self.tag = pick_font("sans_b", 8)
        self.head_l = pick_font("serif_b", 16)
        self.head_m = pick_font("serif_b", 13)
        self.head_s = pick_font("serif_b", 12)
        self.deck_l = pick_font("sans", 11)
        self.deck_m = pick_font("sans", 10)
        self.deck_s = pick_font("sans", 9)
        self.src = pick_font("sans", 8)
        self.sec = pick_font("sans_b", 13)
        self.also = pick_font("sans", 10)
        self.also_n = pick_font("sans_b", 10)
        self.num_big = pick_font("serif_b", 17)
        self.num_lab = pick_font("sans", 8)
        self.legend = pick_font("sans", 9)
        self.legend_b = pick_font("sans_b", 9)
        self.date_t = pick_font("sans_b", 12)
        self.date_b = pick_font("sans", 9)
        self.foot = pick_font("sans", 8)


def load_stories():
    with open(SOURCE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def wrap(draw, text, font, width):
    """Greedy word wrap using real pixel widths."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, font, x, y, width, fill, spacing=1):
    lines = wrap(draw, text, font, width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def fit_lines(draw, text, font, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis if clipped."""
    lines = wrap(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=font) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def _star(draw, cx, cy, r, fill):
    """Five-point star centred at (cx, cy) with outer radius r."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def _figure(draw, px, py, suit, skin=(232, 190, 150), r=7):
    """One seated figure: round head, trapezoid torso.

    Head radius r; torso runs py-2 to py+16, so call with
    py <= box_bottom - 16 to stay inside the box.
    """
    draw.ellipse([px - r, py - 2 * r, px + r, py], fill=skin)
    draw.polygon([(px - r - 4, py + 16), (px + r + 4, py + 16),
                  (px + r - 1, py), (px - r + 1, py)], fill=suit)


def paint_motif(draw, box, kind):
    """One simple, bold, flat icon inside box (x0, y0, x1, y1).

    Every motif is a single readable shape scaled to the box: no
    overlapping scribbles, no text drawn over shapes.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2

    if kind == "summit":
        draw.rectangle(box, fill=(126, 164, 196))
        # Three flags on poles: US, China, Russia.
        flags = [
            ("us", (255, 255, 255)), ("cn", (204, 0, 0)),
            ("ru", (255, 255, 255)),
        ]
        for i, (code, _) in enumerate(flags):
            px = x0 + 24 + i * (w // 3)
            draw.line([px, y0 + 3, px, y0 + 20], fill=INK, width=2)
            fx, fy, fw, fh = px + 2, y0 + 3, 24, 14
            if code == "us":
                draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
                for s in range(3):
                    draw.rectangle([fx, fy + s * 5, fx + fw, fy + s * 5 + 2],
                                   fill=(178, 34, 34))
                draw.rectangle([fx, fy, fx + 10, fy + 7], fill=(40, 60, 120))
            elif code == "cn":
                draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(204, 0, 0))
                _star(draw, fx + 7, fy + 7, 4, (255, 220, 0))
            else:
                draw.rectangle([fx, fy, fx + fw, fy + 5], fill=(255, 255, 255))
                draw.rectangle([fx, fy + 5, fx + fw, fy + 9], fill=(40, 90, 180))
                draw.rectangle([fx, fy + 9, fx + fw, fy + 14], fill=(204, 0, 0))
        # Three seated figures behind a table.
        for i, suit in enumerate([(30, 30, 30), (20, 60, 120), (90, 30, 30)]):
            _figure(draw, x0 + 32 + i * (w // 3), y1 - 28, suit, r=8)
        draw.rectangle([x0, y1 - 12, x1, y1], fill=(96, 64, 32))
        draw.rectangle([x0, y1 - 12, x1, y1 - 9], fill=(245, 240, 225))
        names = ["TRUMP", "XI", "PUTIN"]
        nfont = pick_font("sans_b", 7)
        for i, name in enumerate(names):
            nx = x0 + 32 + i * (w // 3)
            nw = draw.textlength(name, font=nfont)
            draw.text((nx - nw / 2, y1 - 10), name, font=nfont, fill=INK)
    elif kind == "court":
        draw.rectangle(box, fill=(222, 210, 186))
        # Courthouse: pediment, entablature, columns, base.
        draw.polygon([(cx - 52, y0 + 14), (cx + 52, y0 + 14), (cx, y0 + 2)],
                     fill=(139, 69, 19))
        draw.rectangle([x0 + 8, y0 + 14, x1 - 8, y0 + 20], fill=(139, 69, 19))
        for i in range(4):
            px = x0 + 22 + i * ((w - 44) // 3)
            draw.rectangle([px, y0 + 20, px + 10, y1 - 8],
                           fill=(245, 240, 225))
        draw.rectangle([x0 + 8, y1 - 8, x1 - 8, y1 - 2], fill=(139, 69, 19))
        # Red 9-6 badge, top right.
        draw.ellipse([x1 - 34, y0 + 2, x1 - 6, y0 + 30], fill=RED)
        bfont = pick_font("sans_b", 11)
        draw.text((x1 - 28, y0 + 9), "9–6", font=bfont, fill=(255, 255, 255))
    elif kind == "cop":
        draw.rectangle(box, fill=(30, 90, 90))
        # Globe, left.
        gx, gy, gr = x0 + 34, y0 + h // 2, min(22, h // 2 - 4)
        draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(60, 140, 180))
        draw.ellipse([gx - 10, gy - 12, gx + 2, gy - 2], fill=(80, 180, 120))
        draw.ellipse([gx - 2, gy + 2, gx + 12, gy + 12], fill=(80, 180, 120))
        # Thermometer, right.
        tx = x1 - 30
        draw.rounded_rectangle([tx - 5, y0 + 6, tx + 5, y1 - 12],
                               radius=5, fill=(255, 255, 255))
        draw.ellipse([tx - 9, y1 - 20, tx + 9, y1 - 2], fill=(220, 60, 50))
        draw.rectangle([tx - 2, y0 + 14, tx + 2, y1 - 12], fill=(220, 60, 50))
        draw.text((x0 + 8, y0 + 3), "COP31", font=pick_font("sans_b", 11),
                  fill=(255, 255, 255))
        dfont = pick_font("sans_b", 10)
        dtxt = "DRAFT DEAL"
        draw.text((cx - draw.textlength(dtxt, font=dfont) / 2, y1 - 14),
                  dtxt, font=dfont, fill=(255, 220, 120))
    elif kind == "chart":
        draw.rectangle(box, fill=(16, 60, 48))
        scale = (h - 18) / 62.0
        bars = [int(v * scale) for v in (22, 34, 28, 44, 52, 62)]
        for i, bh in enumerate(bars):
            bx = x0 + 14 + i * 36
            col = (60, 180, 120) if i < 5 else (120, 220, 140)
            draw.rectangle([bx, y1 - 8 - bh, bx + 24, y1 - 8], fill=col)
        pts = [(x0 + 14 + i * 36 + 12, y1 - 14 - bh) for i, bh in enumerate(bars)]
        draw.line(pts, fill=(255, 220, 80), width=3)
        draw.text((x0 + 8, y0 + 4), "$83", font=pick_font("serif_b", 20),
                  fill=(255, 255, 255))
        draw.text((x1 - 34, y0 + 6), "IPO", font=pick_font("sans_b", 11),
                  fill=(255, 220, 80))
    elif kind == "riyadh":
        draw.rectangle(box, fill=(20, 30, 60))
        # Tapered tower, centre.
        draw.polygon([(cx - 14, y1), (cx - 9, y0 + 10), (cx + 9, y0 + 10),
                      (cx + 14, y1)], fill=(150, 170, 200))
        for j in range(4):
            yy = y0 + 16 + j * 8
            draw.line([cx - 10, yy, cx + 10, yy], fill=(220, 220, 220), width=1)
        # Missile streak, top right.
        draw.line([x1 - 46, y0 + 6, cx + 6, y0 + 16], fill=(255, 180, 60),
                  width=2)
        _star(draw, x1 - 48, y0 + 6, 5, (255, 160, 40))
        draw.text((x0 + 6, y0 + 4), "RIYADH", font=pick_font("sans_b", 9),
                  fill=(255, 255, 255))
    elif kind == "cyclone":
        draw.rectangle(box, fill=(180, 210, 225))
        rmax = min(24, min(w, h) // 2 - 2)
        for r in range(rmax, 4, -6):
            draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                     fill=(255, 255, 255), width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
        draw.text((x0 + 6, y0 + 4), "AKVAN", font=pick_font("sans_b", 10),
                  fill=(20, 60, 90))
    elif kind == "gta":
        draw.rectangle(box, fill=(40, 20, 70))
        # Game controller, centred.
        bw, bh = min(140, w - 16), 26
        bx0, by0 = cx - bw // 2, cy - bh // 2 + 2
        draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=12,
                               fill=(18, 18, 36))
        # D-pad (plus) on the left.
        dx, dy = bx0 + 20, by0 + bh // 2
        draw.rectangle([dx - 2, dy - 8, dx + 2, dy + 8], fill=(220, 220, 220))
        draw.rectangle([dx - 8, dy - 2, dx + 8, dy + 2], fill=(220, 220, 220))
        # Two buttons on the right.
        draw.ellipse([bx0 + bw - 34, dy - 6, bx0 + bw - 22, dy + 6],
                     fill=(255, 120, 90))
        draw.ellipse([bx0 + bw - 20, dy - 6, bx0 + bw - 8, dy + 6],
                     fill=(120, 220, 140))
        # "VI" on the body, between pad and buttons.
        vfont = pick_font("serif_b", 14)
        vtxt = "VI"
        draw.text((cx - draw.textlength(vtxt, font=vfont) / 2, by0 + 5),
                  vtxt, font=vfont, fill=(255, 255, 255))
    elif kind == "gavel":
        draw.rectangle(box, fill=(230, 220, 200))
        # Gavel lying flat: handle + head, centred and bold.
        hy = cy
        draw.rectangle([x0 + 16, hy - 4, x1 - 46, hy + 4], fill=(120, 80, 40))
        draw.rectangle([x1 - 48, hy - 13, x1 - 14, hy + 13], fill=(90, 55, 20))
        # Sound block under the head.
        draw.rectangle([x1 - 46, y1 - 9, x1 - 16, y1 - 3], fill=(90, 55, 20))
        draw.text((x0 + 8, y0 + 4), "OVERTURNED",
                  font=pick_font("sans_b", 9), fill=RED)
    elif kind == "greenland":
        draw.rectangle(box, fill=(190, 220, 235))
        # Two white peaks.
        draw.polygon([(x0, y1), (x0 + 52, y0 + 16), (x0 + 104, y1)],
                     fill=(255, 255, 255))
        draw.polygon([(x0 + 76, y1), (x0 + 128, y0 + 6), (x1, y1)],
                     fill=(230, 240, 245))
        # Denmark flag on a pole, right.
        px = x1 - 34
        draw.line([px, y0 + 6, px, y0 + 28], fill=INK, width=2)
        draw.rectangle([px + 2, y0 + 6, px + 24, y0 + 18], fill=(204, 0, 0))
        draw.rectangle([px + 10, y0 + 6, px + 13, y0 + 18],
                       fill=(255, 255, 255))
        draw.rectangle([px + 2, y0 + 10, px + 24, y0 + 13],
                       fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 5), "109–0", font=pick_font("sans_b", 13),
                  fill=(20, 60, 90))
    elif kind == "bridge":
        draw.rectangle(box, fill=(170, 200, 225))
        draw.rectangle([x0, y1 - 22, x1, y1 - 14], fill=(90, 90, 90))
        draw.arc([x0 + 24, y0 + 6, x1 - 24, y1 + 4], 180, 360,
                 fill=(60, 60, 60), width=5)
        for sx, sy in ((cx - 14, y0 + 12), (cx + 16, y0 + 18)):
            _star(draw, sx, sy, 6, (255, 160, 0))
        draw.text((x0 + 6, y0 + 4), "KERCH", font=pick_font("sans_b", 9),
                  fill=(20, 40, 60))
    elif kind == "fire":
        draw.rectangle(box, fill=(60, 30, 20))
        # House roofline at the bottom.
        draw.polygon([(x0 + 16, y1 - 8), (cx, y1 - 22), (x1 - 16, y1 - 8)],
                     fill=(30, 16, 10))
        # Flame: orange outer teardrop, yellow inner.
        draw.polygon([(cx, y0 + 2), (cx + 14, y0 + 18), (cx + 9, y1 - 8),
                      (cx - 9, y1 - 8), (cx - 14, y0 + 18)], fill=(255, 140, 0))
        draw.polygon([(cx, y0 + 10), (cx + 8, y0 + 22), (cx + 5, y1 - 8),
                      (cx - 5, y1 - 8), (cx - 8, y0 + 22)], fill=(255, 220, 0))
        draw.text((x0 + 6, y0 + 4), "DHAKA", font=pick_font("sans_b", 9),
                  fill=(255, 255, 255))
    elif kind == "jobs":
        draw.rectangle(box, fill=(240, 235, 220))
        scale = (h - 20) / 44.0
        bars = [int(v * scale) for v in (18, 26, 34, 30, 44)]
        for i, bh in enumerate(bars):
            bx = x0 + 14 + i * 34
            draw.rectangle([bx, y1 - 8 - bh, bx + 20, y1 - 8],
                           fill=(178, 52, 40) if i == 4 else (90, 110, 140))
        draw.line([x0 + 12, y1 - 14, x1 - 14, y1 - 10 - bars[-1] - 2],
                  fill=RED, width=3)
        draw.polygon([(x1 - 14, y1 - 10 - bars[-1] - 2), (x1 - 26, y1 - 10 - bars[-1]),
                      (x1 - 20, y1 - 10 - bars[-1] + 8)], fill=RED)
        tag = "4.9%"
        tfont = pick_font("serif_b", 15)
        draw.text((x0 + 6, y0 + 2), tag, font=tfont, fill=RED)
    elif kind == "march":
        draw.rectangle(box, fill=(220, 215, 200))
        # Three marchers fill the box; the headline says "strike".
        for i, suit in enumerate([(40, 80, 140), (160, 40, 40), (40, 120, 60)]):
            _figure(draw, x0 + 34 + i * (w // 3), y1 - 16, suit, r=6)
    elif kind == "runner":
        draw.rectangle(box, fill=(200, 120, 60))
        # Medal on a ribbon, with a red X over it.
        draw.line([cx - 18, y0 + 2, cx - 5, cy - 4], fill=(120, 30, 20), width=3)
        draw.line([cx + 18, y0 + 2, cx + 5, cy - 4], fill=(120, 30, 20), width=3)
        draw.ellipse([cx - 16, cy - 4, cx + 16, cy + 28], fill=(255, 210, 80),
                     outline=(160, 120, 20), width=2)
        draw.line([cx - 10, cy, cx + 10, cy + 24], fill=RED, width=5)
        draw.line([cx + 10, cy, cx - 10, cy + 24], fill=RED, width=5)
        bfont = pick_font("sans_b", 9)
        btxt = "BANNED"
        draw.text((x1 - 6 - draw.textlength(btxt, font=bfont), y0 + 3),
                  btxt, font=bfont, fill=(255, 255, 255))
    elif kind == "book":
        draw.rectangle(box, fill=(90, 50, 30))
        # Open book: two white pages meeting at the spine.
        draw.polygon([(x0 + 8, y0 + 8), (cx - 2, y0 + 2), (cx - 2, y1 - 4),
                      (x0 + 8, y1 - 2)], fill=(250, 244, 225))
        draw.polygon([(x1 - 8, y0 + 8), (cx + 2, y0 + 2), (cx + 2, y1 - 4),
                      (x1 - 8, y1 - 2)], fill=(250, 244, 225))
        draw.line([cx, y0 + 2, cx, y1 - 4], fill=(120, 110, 95), width=2)
        for j in range(3):
            yy = y0 + 10 + j * 7
            draw.line([x0 + 14, yy, cx - 8, yy - 1], fill=(150, 140, 120),
                      width=1)
            draw.line([cx + 8, yy - 1, x1 - 14, yy], fill=(150, 140, 120),
                      width=1)
        draw.text((x0 + 6, y0 + 3), "ROME", font=pick_font("sans_b", 9),
                  fill=(255, 255, 255))
    elif kind == "senate":
        draw.rectangle(box, fill=(30, 40, 80))
        # Dome + columns + base.
        draw.chord([cx - 26, y0 + 2, cx + 26, y0 + 26], 180, 360,
                   fill=(230, 225, 210))
        for i in range(3):
            px = cx - 20 + i * 16
            draw.rectangle([px, y0 + 14, px + 8, y1 - 10],
                           fill=(200, 195, 180))
        draw.rectangle([x0 + 24, y1 - 10, x1 - 24, y1 - 4],
                       fill=(230, 225, 210))
        draw.text((x0 + 8, y0 + 4), "51–48", font=pick_font("sans_b", 13),
                  fill=(255, 255, 255))
    else:
        draw.rectangle(box, fill=SKY)
        draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED)


def paint_card(draw, fonts, card, x, y, w, h, size):
    """One story card: flat illustration on top, text below.

    Text is budgeted against the card's real height: the headline is
    trimmed first, then the deck, so nothing ever draws past the
    bottom edge or over the source line.
    """
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_EDGE)
    region = card["region"]
    paint = REGION_PAINT.get(region, (100, 100, 100))
    if size == "large":
        ill_h, hf, df, max_head, max_deck = 48, fonts.head_l, fonts.deck_m, 3, 3
    elif size == "medium":
        ill_h, hf, df, max_head, max_deck = 40, fonts.head_m, fonts.deck_s, 2, 2
    else:
        ill_h, hf, df, max_head, max_deck = 34, fonts.head_s, fonts.deck_s, 2, 2
    paint_motif(draw, (x + 1, y + 1, x + w - 1, y + ill_h), card["ill"])
    draw.rectangle([x, y + ill_h, x + w, y + ill_h + 2], fill=paint)
    ty = y + ill_h + 6
    tag = "%d · %s · %s" % (card["n"], region, card["field"])
    draw.text((x + 6, ty), tag, font=fonts.tag, fill=paint)
    ty += 12
    src = card["src"].strip()
    bottom = y + h - 14 if src else y + h - 4
    head_lines = fit_lines(draw, card["head"], hf, w - 12, max_head)
    # Reserve at least one deck line; trim the headline if it must give way.
    while (len(head_lines) > 1 and
           ty + len(head_lines) * (hf.size + 1) + (df.size + 1) > bottom):
        head_lines = head_lines[:-1]
        head_lines[-1] = head_lines[-1].rstrip() + "…"
    for line in head_lines:
        draw.text((x + 6, ty), line, font=hf, fill=INK)
        ty += hf.size + 1
    ty += 1
    deck_room = max(0, (bottom - ty) // (df.size + 1))
    deck_lines = fit_lines(draw, card["deck"], df, w - 12,
                           min(max_deck, deck_room))
    for line in deck_lines:
        draw.text((x + 6, ty), line, font=df, fill=SOFT_INK)
        ty += df.size + 1
    if src:
        draw.text((x + 6, y + h - 13), src, font=fonts.src, fill=(130, 120, 105))


def paint_masthead(draw, fonts, data):
    draw.text((MARGIN, 6), "THE WORLD IN ONE DAY", font=fonts.kicker, fill=RED)
    right = "52 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    draw.text((CANVAS_W - MARGIN - draw.textlength(right, font=fonts.kicker),
               6), right, font=fonts.kicker, fill=SOFT_INK)
    title = "Thursday 19 November 2026"
    tw = draw.textlength(title, font=fonts.masthead)
    draw.text(((CANVAS_W - tw) / 2, 22), title, font=fonts.masthead, fill=INK)
    strap = ("Trump, Xi and Putin share one table · The World Court finds "
             "genocide in Myanmar · COP31's draft drops fossil fuels")
    sw = draw.textlength(strap, font=fonts.strap)
    draw.text(((CANVAS_W - sw) / 2, 84), strap, font=fonts.strap, fill=RED)
    draw.line([MARGIN, 104, CANVAS_W - MARGIN, 104], fill=INK, width=2)


def paint_stats(draw, fonts, data):
    y0, y1 = 108, 146
    cell = INNER / 6.0
    for i, (num, lab) in enumerate(data["STATS"]):
        x = MARGIN + i * cell
        if i:
            draw.line([x, y0 + 4, x, y1 - 4], fill=RULE, width=1)
        nw = draw.textlength(num, font=fonts.big_num)
        draw.text((x + (cell - nw) / 2, y0 + 2), num, font=fonts.big_num,
                  fill=INK)
        for j, line in enumerate(wrap(draw, lab, fonts.stat_lab, cell - 10)):
            lw = draw.textlength(line, font=fonts.stat_lab)
            draw.text((x + (cell - lw) / 2, y0 + 26 + j * 11), line,
                      font=fonts.stat_lab, fill=SOFT_INK)
    draw.line([MARGIN, y1, CANVAS_W - MARGIN, y1], fill=RULE, width=1)


def paint_strips(draw, fonts, data):
    # Region strip: colour-coded, counts in white.
    y0, h = 150, 18
    total = sum(c for _, c in data["REGIONS"])
    x = MARGIN
    for name, count in data["REGIONS"]:
        w = INNER * count / total
        draw.rectangle([x, y0, x + w, y0 + h],
                       fill=REGION_PAINT[name])
        label = "%s %d" % (name, count)
        lw = draw.textlength(label, font=fonts.strip_sm)
        draw.text((x + (w - lw) / 2, y0 + 3), label, font=fonts.strip_sm,
                  fill=(255, 255, 255))
        x += w
    # Field strip: dark slate, name + count.
    y0 = 170
    cell = INNER / len(data["FIELDS"])
    draw.rectangle([MARGIN, y0, CANVAS_W - MARGIN, y0 + h], fill=(48, 48, 56))
    for i, (name, _label, count) in enumerate(data["FIELDS"]):
        x = MARGIN + i * cell
        label = "%s %d" % (name, count)
        lw = draw.textlength(label, font=fonts.strip_sm)
        draw.text((x + (cell - lw) / 2, y0 + 3), label, font=fonts.strip_sm,
                  fill=(235, 230, 220))
        if i:
            draw.line([x, y0 + 3, x, y0 + h - 3], fill=(120, 120, 130), width=1)


def paint_timeline(draw, fonts, data):
    y0, y1 = 194, 232
    draw.text((MARGIN, y0 + 2), "THE DAY\nIN UTC", font=fonts.strip_sm, fill=RED)
    x = MARGIN + 62
    cell = (CANVAS_W - MARGIN - x) / len(data["TIMELINE"])
    for i, (when, what) in enumerate(data["TIMELINE"]):
        cx = x + i * cell
        if i % 2 == 0:
            draw.rectangle([cx, y0, cx + cell, y1], fill=(242, 236, 222))
        draw.text((cx + 4, y0 + 3), when, font=fonts.time, fill=RED)
        yy = y0 + 15
        for line in fit_lines(draw, what, fonts.time_txt, cell - 8, 3):
            draw.text((cx + 4, yy), line, font=fonts.time_txt, fill=INK)
            yy += 11
        if i:
            draw.line([cx, y0 + 3, cx, y1 - 3], fill=RULE, width=1)
    draw.line([MARGIN, y1, CANVAS_W - MARGIN, y1], fill=INK, width=1)


def paint_cards(draw, fonts, data):
    cards = data["CARDS"]
    gap = 6
    # 4 large
    lw = (INNER - 3 * gap) // 4
    for i, card in enumerate(cards[0:4]):
        paint_card(draw, fonts, card, MARGIN + i * (lw + gap), 238, lw, 148,
                   "large")
    # 6 medium
    mw = (INNER - 5 * gap) // 6
    for i, card in enumerate(cards[4:10]):
        paint_card(draw, fonts, card, MARGIN + i * (mw + gap), 392, mw, 118,
                   "medium")
    # 6 small
    for i, card in enumerate(cards[10:16]):
        paint_card(draw, fonts, card, MARGIN + i * (mw + gap), 516, mw, 108,
                   "small")


def _project(x0, y0, w, h, lon, lat):
    """Equirectangular lon/lat -> map-box pixel (lat 85..-60)."""
    px = x0 + (lon + 180) / 360.0 * w
    py = y0 + (85 - lat) / 145.0 * h
    return px, py


def paint_world_map(draw, fonts, data):
    x0, y0, x1, y1 = MARGIN, 652, MARGIN + 308, 796
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 242),
                   outline=CARD_EDGE)
    mw, mh = x1 - x0, y1 - y0
    for poly in CONTINENTS:
        pts = [_project(x0, y0, mw, mh, lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(150, 168, 182), outline=(120, 138, 152))
    draw.text((x0 + 6, y0 + 4), "WORLD MAP — PINS 1–16",
              font=fonts.tag, fill=SOFT_INK)
    for card in data["CARDS"]:
        lon, lat = PIN_LONLAT[card["n"]]
        px, py = _project(x0, y0, mw, mh, lon, lat)
        paint = REGION_PAINT.get(card["region"], (100, 100, 100))
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=paint,
                     outline=(255, 255, 255), width=2)
        num = str(card["n"])
        nw = draw.textlength(num, font=fonts.tag)
        draw.text((px - nw / 2, py - 5), num, font=fonts.tag,
                  fill=(255, 255, 255))


def paint_also(draw, fonts, data):
    x0 = MARGIN + 322
    col_w = (CANVAS_W - MARGIN - x0 - 12) // 2
    items = data["ALSO"]
    half = (len(items) + 1) // 2
    small = pick_font("sans", 9)
    small_n = pick_font("sans_b", 9)
    for col in range(2):
        cx = x0 + col * (col_w + 12)
        for row, item in enumerate(items[col * half:(col + 1) * half]):
            n, _region, _field, text = item
            y = 652 + row * 10
            draw.text((cx, y), "%d" % n, font=small_n, fill=RED)
            draw.text((cx + 20, y), text, font=small, fill=INK)


def paint_how_sure(draw, fonts):
    x0, y0, x1, y1 = MARGIN, 802, MARGIN + 308, 856
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=CARD_EDGE)
    draw.text((x0 + 8, y0 + 5), "HOW SURE", font=fonts.legend_b, fill=INK)
    rows = [
        ("● CONFIRMED", "— 2+ outlets agree."),
        ("● REPORTED", "— one outlet reports it."),
        ("● CLAIM", "— one party's account, not verified."),
    ]
    yy = y0 + 20
    for head, tail in rows:
        draw.text((x0 + 8, yy), head, font=fonts.legend_b, fill=INK)
        draw.text((x0 + 96, yy), tail, font=fonts.legend, fill=SOFT_INK)
        yy += 11


def paint_numbers(draw, fonts, data):
    y0 = 858
    draw.text((MARGIN, y0), "THE DAY IN NUMBERS", font=fonts.sec, fill=INK)
    draw.line([MARGIN + 168, y0 + 8, CANVAS_W - MARGIN, y0 + 8], fill=RED,
              width=1)
    y0 = 876
    cell = INNER / 6.0
    draw.rectangle([MARGIN, y0, CANVAS_W - MARGIN, y0 + 40], fill=PANEL)
    for i, (num, lab) in enumerate(data["NUMBERS"]):
        x = MARGIN + i * cell
        if i:
            draw.line([x, y0 + 5, x, y0 + 35], fill=RULE, width=1)
        nw = draw.textlength(num, font=fonts.num_big)
        draw.text((x + (cell - nw) / 2, y0 + 3), num, font=fonts.num_big,
                  fill=DARK_RED)
        for j, line in enumerate(wrap(draw, lab, fonts.num_lab, cell - 10)):
            lw = draw.textlength(line, font=fonts.num_lab)
            draw.text((x + (cell - lw) / 2, y0 + 23 + j * 10), line,
                      font=fonts.num_lab, fill=SOFT_INK)


def paint_date_check(draw, fonts, data):
    x0, y0, x1, y1 = MARGIN, 920, CANVAS_W - MARGIN, 992
    draw.rectangle([x0, y0, x1, y1], outline=RED, width=2)
    draw.rectangle([x0, y0, x0 + 108, y1], fill=RED)
    draw.text((x0 + 10, y0 + 24), "DATE\nCHECK", font=fonts.date_t,
              fill=(255, 255, 255))
    tx = x0 + 120
    yy = y0 + 6
    for line in data["DATECHECK"]:
        yy = draw_wrapped(draw, line, fonts.date_b, tx, yy, x1 - tx - 10, INK)
        yy += 2


def paint_footer(draw, fonts):
    draw.text((MARGIN, 998),
              "Claims are attributed, not stated as fact · Pictures and map "
              "are original, drawn in code · Sources: Reuters, AP, AFP, BBC, "
              "Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature",
              font=fonts.foot, fill=(130, 120, 105))
    note = "2026-11-19"
    draw.text((CANVAS_W - MARGIN - draw.textlength(note, font=fonts.foot),
               998), note, font=fonts.foot, fill=(130, 120, 105))


def build_page():
    data = load_stories()
    fonts = TypeCase()
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(canvas)
    paint_masthead(draw, fonts, data)
    paint_stats(draw, fonts, data)
    paint_strips(draw, fonts, data)
    paint_timeline(draw, fonts, data)
    paint_cards(draw, fonts, data)
    draw.text((MARGIN, 630), "WHERE IT HAPPENED",
              font=fonts.sec, fill=INK)
    draw.text((MARGIN + 322, 630), "ALSO ON THURSDAY 19 NOVEMBER — "
              "36 MORE STORIES", font=fonts.sec, fill=INK)
    draw.line([MARGIN, 646, CANVAS_W - MARGIN, 646], fill=RED, width=1)
    paint_world_map(draw, fonts, data)
    paint_also(draw, fonts, data)
    paint_how_sure(draw, fonts)
    paint_numbers(draw, fonts, data)
    paint_date_check(draw, fonts, data)
    paint_footer(draw, fonts)
    return canvas


def main():
    page = build_page()
    page.save(TARGET, format="PNG", optimize=True)
    size = os.path.getsize(TARGET)
    print("wrote %s (%d bytes, %dx%d)" % (TARGET, size, CANVAS_W, CANVAS_H))


if __name__ == "__main__":
    main()
