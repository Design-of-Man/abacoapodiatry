#!/usr/bin/env python3
"""Generate the Instagram/Facebook reminder graphics for the Sept 15 event.

The poster carries the launch post. These are the follow-ups — reposting one
image four times in four days reads as spam, so each reminder gets its own
card in the poster's language: near-black ground, ember glow, serif headline,
gradient detail bar.

1080x1350 (4:5), the tallest ratio Instagram shows uncropped in feed.

    python3 _src/event_hotworx_reminders.py

Requires: Pillow.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/events"

W, H = 1080, 1350
INK = (10, 10, 12)
GOLD = (232, 199, 120)
EMBER = (233, 110, 50)
WHITE = (255, 255, 255)
MUTED = (150, 143, 130)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (filename, kicker, headline lines, supporting line)
CARDS = [
    ("hotworx-sept-15-reminder-free.jpg", "THIS TUESDAY",
     ["Free.", "Tuesday.", "4 PM."],
     "Bring us the foot question you've been putting off."),
    ("hotworx-sept-15-reminder-tomorrow.jpg", "ONE MORE SLEEP",
     ["Tomorrow."],
     "Dr. Cedeno is answering foot and ankle questions. No appointment."),
    ("hotworx-sept-15-reminder-today.jpg", "HAPPENING TODAY",
     ["Today.", "4 PM."],
     "Walk in whenever. Snacks are on us."),
]


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit(draw, text, path, start, max_w):
    """Largest size at which `text` still fits `max_w`."""
    size = start
    while size > 12:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, 12)


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build(filename, kicker, headline, support):
    img = Image.new("RGB", (W, H), INK)

    # Ember glow rising from the lower right, echoing the poster's gradient bar.
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, r = 900, 1320, 760
    for i in range(r, 0, -4):
        gd.ellipse([cx - i, cy - i, cx + i, cy + i], fill=int(80 * (1 - i / r)))
    img = Image.composite(Image.new("RGB", (W, H), EMBER), img, glow)
    d = ImageDraw.Draw(img)

    M = 84                      # side margin
    TW = W - M * 2              # text width

    d.text((M, 150), kicker, font=font(SANS_B, 30), fill=EMBER)
    d.line([(M, 205), (M + 190, 205)], fill=EMBER, width=3)

    y = 270
    for line in headline:
        f = fit(d, line, SERIF, 132, TW)
        d.text((M, y), line, font=f, fill=WHITE if line != headline[-1] else GOLD)
        y += f.size + 22

    y += 30
    fs = font(SANS, 36)
    for line in wrap(d, support, fs, TW):
        d.text((M, y), line, font=fs, fill=MUTED)
        y += 52

    # Detail bar: the poster's orange-to-gold sweep, same role on the card.
    bar_top, bar_h = H - 330, 250
    bar = Image.new("RGB", (W - M * 2, bar_h))
    bd = ImageDraw.Draw(bar)
    for x in range(bar.width):
        t = x / bar.width
        bd.line([(x, 0), (x, bar_h)], fill=(
            int(214 + (247 - 214) * t),
            int(74 + (183 - 74) * t),
            int(40 + (77 - 40) * t)))
    img.paste(bar, (M, bar_top))

    bx, by = M + 44, bar_top + 38
    d.text((bx, by), "TUESDAY, SEPT 15", font=font(SANS_B, 38), fill=(40, 14, 4))
    d.text((bx, by + 52), "4:00 PM", font=font(SANS_B, 66), fill=(24, 10, 3))
    d.text((bx, by + 132), "HOTWORX Palm Beach Gardens",
           font=font(SANS_B, 27), fill=(52, 20, 6))
    d.text((bx, by + 166), "3980 Northlake Blvd  ·  (561) 915-1934",
           font=font(SANS_B, 27), fill=(52, 20, 6))

    img.save(OUT / filename, quality=92, optimize=True)
    print(f"Wrote assets/img/events/{filename}")


if __name__ == "__main__":
    for card in CARDS:
        build(*card)
