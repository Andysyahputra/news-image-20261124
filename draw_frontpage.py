#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: THE WORLD TODAY.

Own work, drawn in this session with Pillow. Five real stories, verified
against news reports published on 24 November 2026:

  1. Russian strikes kill 12 in Kyiv region (Reuters / Ukrainian officials)
  2. Indonesia candy factory fire: 24 dead, ~30 missing (Reuters)
  3. Jensen Huang reinstated as Nvidia CEO; shares +31% (Times of India)
  4. FIFA names 2031 Women's World Cup hosts (FIFA)
  5. Oxfam/CEOBS: Gaza's air, soil and water poisoned for decades
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (150, 144, 130)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---- pictograms (simple flat shapes, drawn, not copied) -------------------

def pic_skyline(draw, x, y, s, ink=INK):
    """City skyline with smoke columns (war strikes)."""
    draw.rectangle([x, y + 55 * s, x + 130 * s, y + 130 * s], fill=ink)
    draw.rectangle([x + 20 * s, y + 30 * s, x + 55 * s, y + 130 * s], fill=ink)
    draw.rectangle([x + 75 * s, y + 15 * s, x + 110 * s, y + 130 * s], fill=ink)
    for bx in (x + 28 * s, x + 45 * s, x + 84 * s, x + 100 * s):
        draw.rectangle([bx, y + 65 * s, bx + 8 * s, y + 75 * s], fill=PAPER)
        draw.rectangle([bx, y + 90 * s, bx + 8 * s, y + 100 * s], fill=PAPER)
    # smoke
    for cx, cy, r in ((x + 30 * s, y + 12 * s, 9 * s),
                      (x + 95 * s, y + 2 * s, 8 * s),
                      (x + 118 * s, y + 22 * s, 7 * s)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREY)


def pic_flame(draw, x, y, s):
    """Flame over a factory roof (factory fire)."""
    draw.rectangle([x, y + 95 * s, x + 130 * s, y + 130 * s], fill=INK)
    draw.polygon([(x + 10 * s, y + 95 * s), (x + 10 * s, y + 70 * s),
                  (x + 35 * s, y + 70 * s), (x + 35 * s, y + 95 * s)], fill=INK)
    draw.polygon([(x + 95 * s, y + 95 * s), (x + 95 * s, y + 60 * s),
                  (x + 120 * s, y + 60 * s), (x + 120 * s, y + 95 * s)], fill=INK)
    draw.polygon([(x + 65 * s, y + 5 * s), (x + 95 * s, y + 55 * s),
                  (x + 80 * s, y + 85 * s), (x + 65 * s, y + 60 * s),
                  (x + 50 * s, y + 85 * s), (x + 35 * s, y + 55 * s)],
                 fill=(214, 90, 20))


def pic_chip(draw, x, y, s):
    """Microchip (Nvidia)."""
    draw.rectangle([x + 20 * s, y + 20 * s, x + 110 * s, y + 110 * s],
                   fill=(20, 90, 60))
    draw.rectangle([x + 45 * s, y + 45 * s, x + 85 * s, y + 85 * s],
                   fill=PAPER)
    draw.text((x + 58 * s, y + 52 * s), "N", font=font(SANS_B, int(28 * s)),
              fill=(20, 90, 60))
    for i in range(4):
        px = x + 35 * s + i * 20 * s
        draw.line([(px, y + 5 * s), (px, y + 20 * s)], fill=INK, width=4)
        draw.line([(px, y + 110 * s), (px, y + 125 * s)], fill=INK, width=4)
        py = y + 35 * s + i * 20 * s
        draw.line([(x + 5 * s, py), (x + 20 * s, py)], fill=INK, width=4)
        draw.line([(x + 110 * s, py), (x + 125 * s, py)], fill=INK, width=4)


def pic_ball(draw, x, y, s):
    """Football (World Cup)."""
    cx, cy, r = x + 65 * s, y + 65 * s, 55 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=4)
    pts = []
    import math
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        pts.append((cx + 18 * s * math.cos(a), cy + 18 * s * math.sin(a)))
    draw.polygon(pts, fill=INK)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        x1, y1 = cx + 18 * s * math.cos(a), cy + 18 * s * math.sin(a)
        x2, y2 = cx + 55 * s * math.cos(a), cy + 55 * s * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=INK, width=3)


def pic_drop(draw, x, y, s):
    """Water drop with warning mark (Gaza contamination)."""
    cx = x + 65 * s
    draw.polygon([(cx, y + 5 * s), (cx + 48 * s, y + 75 * s),
                  (cx - 48 * s, y + 75 * s)], fill=(200, 160, 30))
    draw.ellipse([cx - 48 * s, y + 45 * s, cx + 48 * s, y + 125 * s],
                 fill=(40, 110, 160))
    draw.ellipse([cx - 48 * s, y + 45 * s, cx + 48 * s, y + 125 * s],
                 outline=INK, width=3)
    draw.rectangle([cx - 4 * s, y + 55 * s, cx + 4 * s, y + 88 * s], fill=(255, 255, 255))
    draw.ellipse([cx - 5 * s, y + 95 * s, cx + 5 * s, y + 105 * s],
                 fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead ------------------------------------------------------
    d.text((W // 2, 30), "THE WORLD TODAY", font=font(SERIF, 66),
           fill=INK, anchor="ma")
    rule(d, M, 112, W - M, 3)
    d.text((W // 2, 122), "TUESDAY, 24 NOVEMBER 2026",
           font=font(SANS_B, 26), fill=RED, anchor="ma")
    d.text((W // 2, 156), "FIVE STORIES  ·  ONE DAY  ·  THE WORLD IN ONE PAGE",
           font=font(SANS, 17), fill=GREY, anchor="ma")
    rule(d, M, 188, W - M, 2)

    # ---- lead story ----------------------------------------------------
    y = 204
    d.text((M, y), "WAR IN EUROPE", font=font(SANS_B, 19), fill=RED)
    y += 28
    y = draw_wrapped(d, M, y, "RUSSIAN STRIKES KILL 12 IN KYIV REGION",
                     font(SERIF, 42), 620, leading=1.08)
    y += 8
    y = draw_wrapped(
        d, M, y,
        "Russian drone and missile attacks struck homes in the Kyiv region, "
        "killing at least 12 people, Ukrainian officials said. A residential "
        "building in the village of Dymer was hit.",
        font(SANS, 21), 620, leading=1.3)
    d.text((M, y + 10), "Source: Reuters / Ukrainian officials",
           font=font(SANS, 15), fill=GREY)
    pic_skyline(d, 700, 212, 1.7)
    rule(d, M, 452, W - M, 2)

    # ---- 2x2 grid ------------------------------------------------------
    stories = [
        ("DISASTER IN ASIA",
         "FACTORY FIRE: 24 DEAD, 30 MISSING",
         "Rescuers kept searching the burned-out candy factory in Banten, "
         "Indonesia. Officials confirmed 24 dead; about 30 workers remain "
         "missing.",
         "Source: Reuters", pic_flame),
        ("TECH & BUSINESS",
         "HUANG BACK AT NVIDIA; SHARES SOAR 31%",
         "Jensen Huang returned as Nvidia's chief executive after a board "
         "inquiry cleared his return, and the chipmaker's shares surged "
         "more than 31% in a day.",
         "Source: Times of India", pic_chip),
        ("SPORT",
         "2031 WOMEN'S WORLD CUP FOR FOUR HOSTS",
         "FIFA confirmed the 2031 Women's World Cup will be staged in the "
         "United States, Mexico, Costa Rica and Jamaica, with the 2035 "
         "edition in the United Kingdom.",
         "Source: FIFA", pic_ball),
        ("MIDDLE EAST",
         "GAZA 'POISONED FOR DECADES', REPORT WARNS",
         "Oxfam and the Conflict and Environment Observatory warn that "
         "explosive and incendiary weapons have left toxic contamination "
         "across almost the whole Gaza Strip.",
         "Source: Oxfam / CEOBS", pic_drop),
    ]
    cell_w = (W - 2 * M - 24) // 2
    cell_h = 240
    gx, gy = M, 470
    for i, (kicker, head, body, src, pic) in enumerate(stories):
        cx = gx + (i % 2) * (cell_w + 24)
        cy = gy + (i // 2) * (cell_h + 8)
        if i % 2 == 1:
            d.line([(cx - 12, cy + 6), (cx - 12, cy + cell_h - 12)],
                   fill=RULE, width=1)
        pic(d, cx + cell_w - 100, cy + 8, 0.7)
        d.text((cx, cy), kicker, font=font(SANS_B, 16), fill=RED)
        yy = draw_wrapped(d, cx, cy + 26, head, font(SERIF, 25),
                          cell_w - 110, leading=1.1)
        # Body starts below the pictogram so text never runs under it.
        body_y = max(yy + 8, cy + 104)
        draw_wrapped(d, cx, body_y, body, font(SANS, 18),
                     cell_w - 12, leading=1.28)
        d.text((cx, cy + cell_h - 28), src, font=font(SANS, 14), fill=GREY)
        if i == 1:
            rule(d, M, gy + cell_h + 2, W - M, 1, RULE)

    # ---- footer --------------------------------------------------------
    rule(d, M, 978, W - M, 2)
    d.text((W // 2, 988),
           "Drawn from reports published on 24 November 2026  ·  THE WORLD TODAY",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
