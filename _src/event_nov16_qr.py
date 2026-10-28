#!/usr/bin/env python3
"""Generate the source-tagged QR codes for the Nov 16 evening talk (/rsvp/).

One QR per printed channel, each carrying its own ?src= tag so the RSVP email
says where the guest came from (see EVENT-NOV-16-TALK.md):

  nov-16-qr-card.png     invite cards handed out at check-out and in exam rooms
  nov-16-qr-flyer.png    the event flyer
  nov-16-qr-hotworx.png  the HotWorx sign-up table on Oct 29

All 900px square, under assets/img/events/. The domain is cut over, so they
point at jupiterlaser.com. Override only to aim a test print somewhere else:

    EVENT_URL=https://abacoapodiatry.vercel.app/rsvp/ python3 _src/event_nov16_qr.py

Requires: Pillow, segno.
"""
import os
from pathlib import Path

import segno
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/img/events"
URL = os.environ.get("EVENT_URL", "https://jupiterlaser.com/rsvp/")
CHANNELS = ["card", "flyer", "hotworx"]


def qr_image(url, px):
    """QR at roughly `px` square. Error correction H so it still scans with a
    corner obscured, same as the HOTWORX flyer."""
    tmp = OUT / ".qr-tmp.png"
    # scale 1 + nearest-neighbour upscale keeps module edges perfectly crisp.
    segno.make(url, error="h").save(tmp, scale=1, border=2)
    img = Image.open(tmp).convert("RGB")
    tmp.unlink()
    mult = max(1, round(px / img.width))
    return img.resize((img.width * mult, img.height * mult), Image.NEAREST)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for src in CHANNELS:
        name = f"nov-16-qr-{src}.png"
        qr_image(f"{URL}?src={src}", 900).save(OUT / name, optimize=True)
        print(f"Wrote assets/img/events/{name} -> {URL}?src={src}")


if __name__ == "__main__":
    main()
