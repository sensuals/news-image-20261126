#!/usr/bin/env python3
"""Build the entry image for news-image-20261126.

Draws a one-page broadsheet, "THE WORLD IN ONE DAY", summing up the world
news of Thursday 26 November 2026: 40 stories, all of which happened or were
first reported on that day, verified against the day's reporting (One Turn's
26 Nov digest of 123 stories, BBC, Reuters, AP, Guardian, FIDE and others).

Everything is drawn with Pillow from the STORIES data below: flat scenes,
a world map with pins, a UTC timeline and a date check that keeps older
events out of the day. No network, no randomness, no timestamps in the
output, so two runs write identical bytes.

Run:  python3 generate_image.py [output.png]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
NAVY = (22, 50, 79)
RED = (176, 30, 30)
TEAL = (15, 91, 77)
GOLD = (201, 162, 39)
GREY = (90, 86, 76)
LIGHT = (232, 226, 208)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(d, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def badge(d, x, y, num, fill=RED):
    r = 11
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=fill)
    t = str(num)
    f = font(SANS_B, 12)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + 3), t, font=f, fill=(255, 255, 255))


def status_tag(d, x, y, label):
    f = font(SANS_B, 9)
    w = int(d.textlength(label, font=f)) + 10
    d.rectangle([x, y, x + w, y + 14], outline=TEAL, width=1)
    d.text((x + 5, y + 2), label, font=f, fill=TEAL)
    return w


# ---------------------------------------------------------------- scenes
def scene_macy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 48, 84))
    for bx, bh in [(0, 70), (38, 95), (86, 60), (140, 88), (196, 66), (248, 92)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 34, y + h], fill=(12, 24, 48))
        for wy in range(y + h - bh + 8, y + h - 4, 14):
            d.rectangle([x + bx + 6, wy, x + bx + 12, wy + 7], fill=GOLD)
            d.rectangle([x + bx + 20, wy, x + bx + 26, wy + 7], fill=GOLD)
    d.ellipse([x + w // 2 - 52, y + 12, x + w // 2 + 52, y + 62], fill=(214, 48, 49))
    d.ellipse([x + w // 2 - 38, y + 16, x + w // 2 + 2, y + 30], fill=(232, 232, 232))
    d.ellipse([x + w // 2 - 14, y + 38, x + w // 2 - 4, y + 48], fill=INK)
    d.ellipse([x + w // 2 + 4, y + 38, x + w // 2 + 14, y + 48], fill=INK)
    for rx in range(x + 10, x + w - 10, 26):
        d.line([rx, y + 6, rx - 8, y + 26], fill=(160, 190, 220), width=2)
    d.rectangle([x + 8, y + h - 24, x + 168, y + h - 6], fill=RED)
    d.text((x + 14, y + h - 22), "POSTPONED TO SATURDAY",
           font=font(SANS_B, 11), fill=(255, 255, 255))
    d.ellipse([x + w - 46, y + h - 44, x + w - 8, y + h - 6], fill=GOLD)
    d.text((x + w - 36, y + h - 36), "100", font=font(SANS_B, 15), fill=INK)


def scene_mumbai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 148, 52))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 62, 20))
    d.rectangle([x + 30, y + h - 52, x + w - 30, y + h - 34], fill=(150, 84, 32))
    for cx in (70, 160, 250):
        d.pieslice([x + cx - 20, y + h - 72, x + cx + 20, y + h - 32], 180, 360,
                   fill=(150, 84, 32))
        d.rectangle([x + cx - 3, y + h - 78, x + cx + 3, y + h - 70], fill=(150, 84, 32))
    for cx in range(x + 24, x + w - 20, 30):
        d.rectangle([x + cx, y + h - 22, x + cx + 7, y + h - 8], fill=(245, 240, 220))
        d.ellipse([x + cx - 1, y + h - 30, x + cx + 8, y + h - 20], fill=(255, 190, 60))
    d.rectangle([x + w - 118, y + 10, x + w - 10, y + 34], fill=(20, 20, 20))
    d.text((x + w - 108, y + 14), "18 YEARS", font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x + 10, y + 10, x + 74, y + 34], fill=(255, 153, 51))
    d.rectangle([x + 10, y + 18, x + 74, y + 26], fill=(255, 255, 255))
    d.rectangle([x + 10, y + 26, x + 74, y + 34], fill=(19, 136, 8))


def scene_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 44))
    s_ = 12
    ox, oy = x + 16, y + 10
    for r in range(6):
        for c in range(8):
            col = (240, 230, 200) if (r + c) % 2 == 0 else (60, 40, 20)
            d.rectangle([ox + c * s_, oy + r * s_, ox + (c + 1) * s_, oy + (r + 1) * s_], fill=col)
    d.ellipse([ox + 2 * s_ + 2, oy + 2 * s_ + 2, ox + 3 * s_ - 2, oy + 3 * s_ - 2], fill=INK)
    d.ellipse([ox + 5 * s_ + 2, oy + 1 * s_ + 2, ox + 6 * s_ - 2, oy + 2 * s_ - 2], fill=(240, 240, 240))
    for i, t in enumerate(("1:32", "1:32")):
        bx, by = x + 140, y + 10 + i * 38
        d.rectangle([bx, by, bx + 58, by + 30], fill=(245, 240, 220))
        d.rectangle([bx, by, bx + 58, by + 10], fill=RED)
        d.text((bx + 8, by + 13), t, font=font(SANS_B, 13), fill=INK)
    d.rectangle([x + 216, y + 10, x + w - 12, y + 32], fill=RED)
    d.text((x + 224, y + 14), "GAME 3", font=font(SANS_B, 12), fill=(255, 255, 255))
    d.rectangle([x + 16, y + 84, x + w - 16, y + h - 2], fill=(245, 240, 220))
    d.text((x + 26, y + 87), "GUKESH  1.5 - 1.5  SINDAROV",
           font=font(SANS_B, 14), fill=INK)


def scene_generic(d, x, y, w, h, sky, fn):
    d.rectangle([x, y, x + w, y + h], fill=sky)
    fn(d, x, y, w, h)


def sc_drone(d, x, y, w, h):
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(194, 164, 110))
    cx, cy = x + w // 2, y + 34
    d.line([cx - 34, cy - 14, cx + 34, cy + 14], fill=INK, width=4)
    d.line([cx - 34, cy + 14, cx + 34, cy - 14], fill=INK, width=4)
    d.ellipse([cx - 12, cy - 9, cx + 12, cy + 9], fill=(60, 60, 60))
    for px, py in [(cx - 52, cy - 8), (cx + 40, cy + 4)]:
        d.ellipse([px, py, px + 26, py + 26], fill=(255, 170, 40))
        d.ellipse([px + 8, py + 8, px + 18, py + 18], fill=(255, 220, 120))


def sc_tariff(d, x, y, w, h):
    vals = [30, 55, 40, 70, 48, 62, 36, 58, 44, 66, 52, 38, 60, 46]
    bw = w // len(vals)
    for i, v in enumerate(vals):
        bh = int(v * h / 90)
        d.rectangle([x + i * bw + 2, y + h - 8 - bh, x + (i + 1) * bw - 2, y + h - 8],
                    fill=RED if i == 3 else NAVY)
    d.rectangle([x + 8, y + 6, x + 96, y + 26], fill=(255, 255, 255))
    d.text((x + 12, y + 9), "14 PARTNERS", font=font(SANS_B, 11), fill=RED)


def sc_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 2], fill=(70, 130, 200))
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(240, 200, 60))
    d.line([x + 10, y + 12, x + w - 30, y + h - 20], fill=(255, 255, 255), width=3)
    d.ellipse([x + w - 40, y + h - 30, x + w - 16, y + h - 6], fill=(255, 120, 40))
    d.ellipse([x + w - 34, y + h - 24, x + w - 22, y + h - 12], fill=(255, 200, 80))


def sc_refinery(d, x, y, w, h):
    g = y + h - 10
    for bx in (16, 62, 108):
        d.rectangle([x + bx, g - int(0.55 * h), x + bx + 30, g], fill=(120, 120, 120))
        d.rectangle([x + bx + 4, g - int(0.72 * h), x + bx + 12, g - int(0.55 * h)],
                    fill=(120, 120, 120))
    for fx, fy, s_ in [(x + 152, g - int(0.62 * h), 22), (x + 130, g - int(0.45 * h), 15),
                       (x + 168, g - int(0.42 * h), 12)]:
        d.polygon([(fx, fy - s_), (fx - s_ // 2, fy), (fx + s_ // 2, fy)], fill=(255, 120, 20))
        d.polygon([(fx, fy - s_ // 2), (fx - s_ // 3, fy), (fx + s_ // 3, fy)], fill=(255, 200, 60))
    d.ellipse([x + 20, y + 4, x + 52, y + 18], fill=(200, 200, 200))


def sc_gaza(d, x, y, w, h):
    g = y + h - 8
    for bx, bh in [(10, 0.62), (52, 0.78), (100, 0.5), (140, 0.7)]:
        bh = int(bh * h)
        d.rectangle([x + bx, g - bh, x + bx + 36, g], fill=(150, 140, 120))
    d.polygon([(x + 52, g - int(0.78 * h)), (x + 70, g - int(0.95 * h)),
               (x + 88, g - int(0.78 * h))], fill=(150, 140, 120))
    d.ellipse([x + 120, y + 4, x + 168, y + 26], fill=(180, 180, 180))


def sc_hiv(d, x, y, w, h):
    cx, cy, r = x + w // 2 - 30, y + h // 2, min(22, h // 2 - 4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    d.rectangle([cx - r + 4, cy - 5, cx + r - 4, cy + 5], fill=TEAL)
    d.rectangle([cx - 5, cy - r + 4, cx + 5, cy + r - 4], fill=TEAL)
    d.text((x + w // 2 + 2, y + h // 2 - 9), "2x", font=font(SANS_B, 18), fill=TEAL)
    d.text((x + w // 2 + 2, y + h // 2 + 10), "A YEAR", font=font(SANS_B, 10), fill=TEAL)


def sc_ebola(d, x, y, w, h):
    import math
    for fx, fy, fr in [(0.26, 0.42, 0.20), (0.62, 0.68, 0.24), (0.48, 0.85, 0.14), (0.84, 0.38, 0.13)]:
        cx, cy, r = x + int(fx * w), y + int(fy * h), int(fr * h)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        for a in range(6):
            x2 = cx + int((r + 7) * math.cos(a))
            y2 = cy + int((r + 7) * math.sin(a))
            d.line([cx, cy, x2, y2], fill=RED, width=2)


def sc_ecb(d, x, y, w, h):
    import math
    g = y + h - 10
    for bx in range(5):
        d.rectangle([x + 18 + bx * 34, g - int(0.42 * h), x + 32 + bx * 34, g],
                    fill=(240, 235, 220))
    d.polygon([(x + 10, g - int(0.42 * h)), (x + w // 2, y + 4),
               (x + w - 10, g - int(0.42 * h))], fill=(240, 235, 220))
    d.text((x + w // 2 - 11, g - int(0.42 * h) + 2), "€",
           font=font(SANS_B, 22), fill=NAVY)
    for i in range(12):
        a = i * math.pi / 6
        sx = x + w // 2 + int(78 * math.cos(a))
        sy = y + int(0.45 * h) + int(12 * math.sin(a))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)


def sc_cairo(d, x, y, w, h):
    g = y + h - 8
    d.rectangle([x, g, x + w, y + h], fill=(80, 80, 80))
    d.rectangle([x + 18, g - 22, x + 110, g - 2], fill=(220, 220, 220))
    d.ellipse([x + 36, g - 6, x + 56, g + 6], fill=INK)
    d.ellipse([x + 86, g - 6, x + 106, g + 6], fill=INK)
    d.rectangle([x + 110, g - 14, x + 140, g - 2], fill=(180, 60, 40))
    for fx, fy, s_ in [(x + 152, g - 34, 20), (x + 134, g - 22, 13), (x + 168, g - 24, 10)]:
        d.polygon([(fx, fy - s_), (fx - s_ // 2, fy), (fx + s_ // 2, fy)], fill=(255, 120, 20))
        d.polygon([(fx, fy - s_ // 2), (fx - s_ // 3, fy), (fx + s_ // 3, fy)], fill=(255, 200, 60))


def sc_ibiza(d, x, y, w, h):
    d.rectangle([x, y + h // 2, x + w, y + h], fill=(40, 110, 170))
    for wy in range(y + h // 2 + 8, y + h - 6, 14):
        d.arc([x + 8, wy, x + 60, wy + 12], 0, 180, fill=(255, 255, 255), width=2)
        d.arc([x + 100, wy, x + 152, wy + 12], 0, 180, fill=(255, 255, 255), width=2)
    d.polygon([(x + 50, y + 18), (x + 150, y + 30), (x + 140, y + 52), (x + 60, y + 44)],
              fill=(40, 40, 40))
    d.rectangle([x + 88, y + 30, x + 96, y + 52], fill=(200, 60, 40))


SCENES = {
    1: scene_macy, 2: scene_mumbai, 3: scene_chess,
    4: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (222, 196, 150), sc_drone),
    5: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (235, 230, 215), sc_tariff),
    6: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (240, 200, 60), sc_ukraine),
    7: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (230, 210, 180), sc_refinery),
    8: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (210, 200, 180), sc_gaza),
    9: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (200, 230, 215), sc_hiv),
    10: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (245, 225, 215), sc_ebola),
    11: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (30, 60, 110), sc_ecb),
    12: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (235, 220, 190), sc_cairo),
    13: lambda d, x, y, w, h: scene_generic(d, x, y, w, h, (180, 210, 235), sc_ibiza),
}

# ---------------------------------------------------------------- data
LEADS = [
    (1, "USA · THANKSGIVING", "Macy's 100th Thanksgiving parade postponed",
     "A nor'easter brings 60 mph gusts to New York; the parade moves to Saturday, a first in 100 years.",
     "AP", "CONFIRMED"),
    (2, "INDIA · MUMBAI", "India marks 18 years since the 26/11 attacks",
     "Tributes across India on the anniversary, as the nation also marks 77 years of its Constitution.",
     "PTI", "CONFIRMED"),
    (3, "CHESS · GENEVA", "Gukesh meets Sindarov in Game 3",
     "A 60-move Berlin draw in Geneva leaves the world title match level at 1.5-1.5.",
     "FIDE", "CONFIRMED"),
]

MID = [
    (4, "KUWAIT", "Drone attack in Kuwait kills two Italians",
     "Two technicians die at a military site; Iran denies any role.", "BBC", "REPORTED"),
    (5, "TARIFFS", "US proposes tariffs on 14 trading partners",
     "Levies up to 40% on China; the EU, Japan and China push back.", "Reuters", "CONFIRMED"),
    (6, "UKRAINE WAR", "Russia and Ukraine trade strikes",
     "Trump urges Putin to pull back; Kyiv says 87 missiles downed.", "BBC", "REPORTED"),
    (7, "SAUDI ARABIA", "Houthis hit Saudi Jazan refinery",
     "A Nepali worker is killed; Saudi Arabia strikes Yemen in reply.", "Al Jazeera", "REPORTED"),
    (8, "GAZA", "Israeli strikes in Gaza kill Hamas officials",
     "About nine die, including a Hamas deputy minister, amid a fragile ceasefire.", "BBC", "REPORTED"),
    (9, "HEALTH", "Cheaper HIV prevention jab reaches Africa",
     "A twice-yearly injection arrives at lower cost; nearly 100% effective.", "BBC", "CONFIRMED"),
    (10, "DR CONGO", "DR Congo Ebola cases pass 12,000",
     "About 5,900 have died in the second-largest outbreak on record.", "AP", "CONFIRMED"),
    (11, "EUROPE", "Spain's Hernandez de Cos picked to lead the ECB",
     "The former Bank of Spain chief succeeds Lagarde in February 2027.", "Guardian", "CONFIRMED"),
    (12, "EGYPT", "Cairo tanker fire kills 31",
     "A tanker crash on the Ring Road leaves 31 dead and 21 hurt; the driver is held.", "BBC", "CONFIRMED"),
    (13, "SPAIN", "Diesel tanker capsizes off Ibiza",
     "One crew member dies and 17 are rescued; Spain activates an emergency plan.", "BBC", "REPORTED"),
]

MORE = [
    ("Brussels", "EU budget summit, no deal", "Guardian"),
    ("Jerusalem", "Netanyahu bribery charge may go", "Euronews"),
    ("New York", "Nasdaq nears bear market", "CNBC"),
    ("Brooklyn", "Huawei guilty of trade-secret theft", "BBC"),
    ("Pyongyang", "Kim vows more nuclear weapons", "NPR"),
    ("Tiangong", "First Pakistani astronaut in orbit", "AFP"),
    ("Washington", "FCC backs 1m-satellite SpaceX plan", "BBC"),
    ("Dimorphos", "Hera shows crater from NASA impact", "Guardian"),
    ("USA", "Pig kidney patient a year off dialysis", "CBC"),
    ("Erbil", "Iraq takes control of Kurdistan oil", "DW"),
    ("London", "UK net migration falls to 77,000", "Guardian"),
    ("Madrid", "Spain votes Sunday, right favoured", "France 24"),
    ("Brasilia", "Brazil recalls envoy to Argentina", "MercoPress"),
    ("Caracas", "Venezuela to lift opponents' ban", "La Nacion"),
    ("Washington", "Judge blocks birthright limits", "Al Jazeera"),
    ("Naypyidaw", "Myanmar defies ICJ genocide ruling", "BBC"),
    ("Moscow", "Iran oil revenue falls under blockade", "OilPrice"),
    ("Hong Kong", "City marks year since fire killed 168", "BBC"),
    ("Honiara", "Solomons sign Australia security pact", "NBC"),
    ("Gazipur", "Garment workers protest minimum wage", "Al Jazeera"),
    ("Sudan", "WFP warns of severe food shortage", "Asharq Al-Awsat"),
    ("Shanghai", "China probes party chief Chen Jining", "SCMP"),
    ("Cape Town", "Ramaphosa impeachment report void", "AllAfrica"),
    ("Liverpool", "Liverpool beat Club Brugge 3-0", "UEFA"),
    ("Lille", "Lille beat Bayern Munich 2-1", "UEFA"),
    ("Paris", "PSG and Roma draw 2-2", "UEFA"),
    ("Finland", "Wright, first US biathlon Cup winner", "IBU"),
]

TIMELINE = [
    ("02:18", "Gaza airstrike"),
    ("09:33", "Kyiv missile strike"),
    ("14:00", "Chess Game 3, Geneva"),
    ("17:57", "Gaza airstrike"),
    ("21:20", "Yemen missile strike"),
]

DATE_CHECK = [
    "Gukesh draws Game 2 vs Sindarov — 25 Nov",
    "Ukraine drones hit Russian ships off Libya — 22 Nov",
    "Mumbai attacks killed 166 people — 26 Nov 2008",
    "Hong Kong fire killed 168 — 26 Nov 2025",
    "Gukesh draws Game 1 vs Sindarov — 24 Nov",
    "NASA's DART probe hit Dimorphos — 2022",
]

CONTINENTS = [
    [(22, 28), (92, 14), (122, 34), (112, 70), (72, 86), (36, 70), (16, 48)],
    [(96, 108), (126, 104), (142, 140), (116, 182), (100, 150)],
    [(212, 24), (262, 18), (278, 44), (252, 60), (222, 54)],
    [(216, 74), (272, 70), (288, 110), (262, 162), (232, 150), (210, 108)],
    [(282, 18), (402, 14), (442, 40), (432, 92), (382, 112), (332, 96), (302, 60), (282, 40)],
    [(392, 150), (432, 144), (442, 166), (412, 176), (392, 166)],
]
PINS = {1: (58, 56), 2: (336, 86), 3: (246, 48), 4: (306, 70), 5: (62, 64),
        6: (266, 38), 7: (300, 94), 8: (278, 60), 9: (238, 108), 10: (262, 138),
        11: (220, 32), 12: (260, 82), 13: (228, 58)}


def build(out_path):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 10], fill=NAVY)
    d.rectangle([0, 1014, W, H], fill=NAVY)

    # masthead
    f_mast = font(SERIF_B, 56)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 16), t, font=f_mast, fill=INK)
    d.line([24, 82, W - 24, 82], fill=INK, width=2)
    f_date = font(SANS_B, 25)
    t = "THURSDAY 26 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 88), t, font=f_date, fill=RED)
    y = text_block(d, 60, 118, "A nor'easter grounds New York's 100th Thanksgiving parade, "
                   "India marks 18 years since the 26/11 Mumbai attacks, and Gukesh "
                   "meets Sindarov in Game 3 of the world title match in Geneva.",
                   font(SERIF_I, 15), W - 120, 19, fill=(40, 40, 40))
    d.line([24, 158, W - 24, 158], fill=INK, width=1)

    # stat strip
    stats = [("40", "STORIES"), ("9", "REGIONS"), ("123", "HEADLINES CHECKED")]
    xs = [24, 356, 688]
    for (num, lab), x in zip(stats, xs):
        d.rectangle([x, 164, x + 312, 188], outline=INK, width=1)
        f_n = font(SANS_B, 17)
        d.text((x + 10, 168), num, font=f_n, fill=RED)
        f_l = font(SANS_B, 12)
        d.text((x + 10 + d.textlength(num + " ", font=f_n), 171), lab, font=f_l, fill=INK)
    d.text((24, 192), "North America  ·  South Asia  ·  Europe  ·  Middle East  ·  Africa  ·  "
           "East Asia  ·  Oceania  ·  South America  ·  Space",
           font=font(SANS, 11), fill=GREY)

    # lead row
    y0 = 206
    for (num, region, head, deck, src, status), x in zip(LEADS, [24, 356, 688]):
        SCENES[num](d, x, y0, 312, 104)
        badge(d, x + 6, y0 + 6, num)
        hy = y0 + 112
        d.text((x, hy), region, font=font(SANS_B, 10), fill=RED)
        hy = text_block(d, x, hy + 14, head, font(SANS_B, 18), 312, 21, max_lines=2)
        hy = text_block(d, x, hy + 2, deck, font(SANS, 12), 312, 15, max_lines=2)
        src_y = hy + 4
        d.text((x, src_y), "SOURCE: " + src, font=font(SANS_B, 9), fill=GREY)
        status_tag(d, x + 240, src_y - 2, status)
        d.line([x, src_y + 14, x + 312, src_y + 14], fill=LIGHT, width=1)

    # mid rows: 10 scenes, 5 per row
    for row in range(2):
        y0 = 428 + row * 136
        for col in range(5):
            num, region, head, deck, src, status = MID[row * 5 + col]
            x = 24 + col * 200
            SCENES[num](d, x, y0, 190, 72)
            badge(d, x + 4, y0 + 4, num)
            hy = y0 + 76
            d.text((x, hy), region, font=font(SANS_B, 9), fill=RED)
            hy = text_block(d, x, hy + 12, head, font(SANS_B, 11), 190, 13, max_lines=2)
            hy = text_block(d, x, hy + 1, deck, font(SANS, 9), 190, 11, max_lines=2)

    # UTC timeline
    d.rectangle([24, 702, W - 24, 728], fill=NAVY)
    d.text((34, 709), "THE DAY IN UTC", font=font(SANS_B, 12), fill=(255, 255, 255))
    tx = 170
    for tm, ev in TIMELINE:
        d.text((tx, 709), tm, font=font(SANS_B, 10), fill=GOLD)
        d.text((tx + 52, 709), ev, font=font(SANS, 10), fill=(255, 255, 255))
        tx += 52 + int(d.textlength(ev, font=font(SANS, 10))) + 10

    # map + also list
    y0 = 734
    d.rectangle([24, y0, 454, 904], outline=INK, width=1)
    d.text((34, y0 + 6), "WHERE IT HAPPENED — PINS 1-13", font=font(SANS_B, 11), fill=INK)
    mx, my = 34, y0 + 28
    for poly in CONTINENTS:
        d.polygon([(mx + int(px * 0.92), my + int(py * 0.78)) for px, py in poly],
                  fill=(205, 198, 170), outline=(120, 112, 96))
    for num, (px, py) in PINS.items():
        cx, cy = mx + int(px * 0.92), my + int(py * 0.78)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
        t = str(num)
        f = font(SANS_B, 9)
        d.text((cx - d.textlength(t, font=f) / 2, cy - 6), t, font=f, fill=(255, 255, 255))

    d.rectangle([466, y0, W - 24, 904], outline=INK, width=1)
    d.text((476, y0 + 6), "AND ALSO — STORIES 14-40", font=font(SANS_B, 11), fill=INK)
    f_item = font(SANS, 8)
    f_num = font(SANS_B, 9)
    for i, (place, head, src) in enumerate(MORE):
        col = 0 if i < 14 else 1
        r = i % 14
        x = 476 + col * 262
        yy = y0 + 22 + r * 10
        d.text((x, yy), str(14 + i) + ".", font=f_num, fill=RED)
        line = place + " — " + head
        while d.textlength(line, font=f_item) > 228 and " " in line:
            line = line.rsplit(" ", 1)[0] + " …"
        d.text((x + 24, yy), line, font=f_item, fill=INK)

    # date check
    d.rectangle([24, 912, W - 24, 970], outline=RED, width=2)
    d.text((34, 917), "DATE CHECK — THESE ARE NOT 26 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    for i, item in enumerate(DATE_CHECK):
        col = 0 if i < 3 else 1
        r = i % 3
        x = 34 + col * 490
        yy = 938 + r * 11
        d.text((x, yy), "×  " + item, font=font(SANS, 10), fill=INK)

    # footer
    d.text((24, 978), "Sources: AP · Reuters · BBC · Guardian · PTI · FIDE · Al Jazeera · AFP · "
           "NPR · CBC · DW · Euronews · SCMP · UEFA · IBU. Every story here happened or was "
           "first reported on Thursday 26 November 2026.",
           font=font(SANS, 9), fill=GREY)
    d.text((24, 992), "Scenes are drawn illustrations, not photographs. HOW SURE: CONFIRMED = "
           "two or more outlets · REPORTED = one outlet · CLAIM = as claimed.",
           font=font(SANS, 9), fill=GREY)

    im.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    build(out)
    print(out, out.stat().st_size, "bytes")
