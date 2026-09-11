#!/usr/bin/env python3
"""Generate the print flyer, QR code, and share card for the Sept 15 HOTWORX event.

Three outputs, all under assets/img/events/:
  hotworx-sept-15-qr.png     standalone QR, for dropping into someone else's design
  hotworx-sept-15-flyer.png  letter-size print flyer: the poster + a scan-me band
  hotworx-sept-15-og.png     1200x630 link-preview card for Facebook/iMessage/SMS

The QR target is an env var because the site is mid-migration. Until DNS cuts
over, jupiterlaser.com still serves the OLD site, so a QR pointing there would
land on a 404 in front of a room full of people. It points at the live Vercel
host instead. After cutover, rerun with:

    EVENT_URL=https://jupiterlaser.com/hotworx/ python3 _src/event_hotworx.py

Requires: Pillow, segno.
"""
import os
from pathlib import Path

import segno
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/events"
POSTER = OUT / "hotworx-sept-15.jpg"

URL = os.environ.get("EVENT_URL", "https://abacoapodiatry.vercel.app/hotworx/")

INK = (10, 10, 12)
GOLD = (232, 199, 120)
EMBER = (233, 110, 50)
WHITE = (255, 255, 255)
MUTED = (176, 168, 154)

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"


def font(size, weight="-Bold"):
    try:
        return ImageFont.truetype(DEJAVU % weight, size)
    except OSError:
        return ImageFont.load_default()


def fit(draw, text, start, max_w, weight="-Bold"):
    """Largest size at which `text` still fits `max_w`."""
    size = start
    while size > 10:
        f = font(size, weight)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(10, weight)


def qr_image(px, dark=INK, light=WHITE):
    """QR at roughly `px` square. Error correction H so it still scans with the
    corner obscured — printed flyers get thumbtacked and coffee-ringed."""
    qr = segno.make(URL, error="h")
    tmp = OUT / ".qr-tmp.png"
    # scale 1 + nearest-neighbour upscale keeps module edges perfectly crisp;
    # letting segno scale directly can land on a non-integer module size.
    qr.save(tmp, scale=1, border=2, dark="#%02x%02x%02x" % dark,
            light="#%02x%02x%02x" % light)
    img = Image.open(tmp).convert("RGB")
    tmp.unlink()
    mult = max(1, round(px / img.width))
    return img.resize((img.width * mult, img.height * mult), Image.NEAREST)


def build_qr():
    qr_image(900).save(OUT / "hotworx-sept-15-qr.png", optimize=True)
    print("Wrote assets/img/events/hotworx-sept-15-qr.png")


def build_flyer():
    """Letter portrait at 150 DPI (1275x1650) — prints clean on any office
    printer and still reads on a phone screen at the front desk."""
    W, H = 1275, 1650
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    poster = Image.open(POSTER).convert("RGB")
    pw = 1080
    ph = round(poster.height * pw / poster.width)
    poster = poster.resize((pw, ph), Image.LANCZOS)
    px, py = (W - pw) // 2, 28
    img.paste(poster, (px, py))

    band_top = py + ph + 26
    d.line([(px, band_top - 13), (px + pw, band_top - 13)], fill=(58, 50, 38), width=2)

    qr = qr_image(200)
    qx, qy = px, band_top + 14
    # White quiet-zone plate: scanners need the light margin, and the poster
    # background is near-black.
    d.rectangle([qx - 10, qy - 10, qx + qr.width + 10, qy + qr.height + 10], fill=WHITE)
    img.paste(qr, (qx, qy))

    tx = qx + qr.width + 42
    tw = px + pw - tx
    # Deliberately no typed-out URL beside the QR: the site is mid-migration and
    # the host the QR can reach today is not a domain anyone would type. The QR
    # carries the link; the phone number carries everyone else.
    d.text((tx, qy + 6), "SCAN FOR EVENT DETAILS",
           font=fit(d, "SCAN FOR EVENT DETAILS", 40, tw), fill=GOLD)
    l2 = "Questions, or to save a spot for IV night:"
    d.text((tx, qy + 74), l2, font=fit(d, l2, 27, tw, ""), fill=MUTED)
    d.text((tx, qy + 116), "(561) 915-1934",
           font=fit(d, "(561) 915-1934", 60, tw), fill=EMBER)

    img.save(OUT / "hotworx-sept-15-flyer.png", optimize=True)
    print("Wrote assets/img/events/hotworx-sept-15-flyer.png")


def build_og():
    """1200x630 flat RGB — iMessage and Slack paint transparency onto their own
    backdrop, so the card has to carry its own background."""
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # Ember glow behind the poster edge, echoing the poster's own gradient bar.
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, r = 980, 680, 620
    for i in range(r, 0, -4):
        gd.ellipse([cx - i, cy - i, cx + i, cy + i], fill=int(90 * (1 - i / r)))
    img = Image.composite(Image.new("RGB", (W, H), EMBER), img, glow)
    d = ImageDraw.Draw(img)

    poster = Image.open(POSTER).convert("RGB")
    ph = H - 72
    pw = round(poster.width * ph / poster.height)
    poster = poster.resize((pw, ph), Image.LANCZOS)
    img.paste(poster, (W - pw - 48, 36))

    tw = W - pw - 48 - 64 - 48
    x = 64
    d.text((x, 92), "EVENT  ·  TUESDAY, SEPT 15", font=fit(d, "EVENT  ·  TUESDAY, SEPT 15", 26, tw), fill=GOLD)
    for i, line in enumerate(["Sweat.", "Recover.", "Stand."]):
        d.text((x, 150 + i * 78), line, font=fit(d, line, 68, tw),
               fill=GOLD if line == "Stand." else WHITE)
    sub = "Foot & ankle Q&A with Dr. Cedeno"
    d.text((x, 410), sub, font=fit(d, sub, 27, tw, ""), fill=MUTED)
    d.text((x, 452), "4:00 PM · HOTWORX Palm Beach Gardens",
           font=fit(d, "4:00 PM · HOTWORX Palm Beach Gardens", 24, tw, ""), fill=MUTED)
    d.text((x, 500), "3980 Northlake Blvd",
           font=fit(d, "3980 Northlake Blvd", 24, tw, ""), fill=MUTED)
    d.text((x, 548), "(561) 915-1934", font=fit(d, "(561) 915-1934", 34, tw), fill=WHITE)

    img.save(OUT / "hotworx-sept-15-og.png", optimize=True)
    print("Wrote assets/img/events/hotworx-sept-15-og.png")


if __name__ == "__main__":
    print(f"QR target: {URL}")
    build_qr()
    build_flyer()
    build_og()
