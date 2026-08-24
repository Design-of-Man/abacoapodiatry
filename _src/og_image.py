#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph share image (assets/img/og-image.png).

Flat RGB, no alpha: iMessage, Slack and Facebook all paint transparency onto
their own backdrop (grey in iMessage), so a share card must carry its own
background rather than borrowing one.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), (12, 11, 8))
d = ImageDraw.Draw(img)

# Vertical gradient
top, bottom = (12, 11, 8), (24, 21, 14)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))

# Radial glow, upper right
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
cx, cy, r = 1050, 60, 640
for i in range(r, 0, -4):
    gd.ellipse([cx - i, cy - i, cx + i, cy + i], fill=int(70 * (1 - i / r)))
img = Image.composite(Image.new("RGB", (W, H), (140, 108, 44)), img, glow)
d = ImageDraw.Draw(img)

# Dot grid
for gx in range(0, W, 34):
    for gy in range(0, H, 34):
        d.ellipse([gx, gy, gx + 2, gy + 2], fill=(96, 86, 58))

# Gold sweep
for off, col in [(-3, (232, 199, 120)), (0, (211, 172, 87)), (3, (138, 106, 42))]:
    d.line([(0, 470 + off), (W, 380 + off)], fill=col, width=2)


def font(size, bold=True):
    path = ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def fit(text, start, max_w, bold=True):
    """Largest size at which `text` still fits `max_w`. The headline changed
    once already; measuring beats guessing a size that silently overflows."""
    size = start
    while size > 12:
        f = font(size, bold)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(12, bold)


# Practice logo
logo = Image.open("assets/img/logo-abacoa.png").convert("RGBA")
lw = 430
logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
img.paste(logo, (78, 74), logo)

d.text((548, 128), "FOOT & ANKLE", font=font(26), fill=(232, 199, 120))
d.text((548, 166), "SPECIALISTS", font=font(26), fill=(232, 199, 120))

MAXW = W - 160
l1, l2 = "Walk Without Pain Again.", "Jupiter's Foot & Ankle Specialists."
d.text((80, 300), l1, font=fit(l1, 58, MAXW), fill=(255, 255, 255))
d.text((80, 375), l2, font=fit(l2, 58, MAXW), fill=(232, 199, 120))

sub = "MLS Laser  •  Shockwave  •  Regenerative Medicine  •  Bunions  •  Surgery"
d.text((80, 490), sub, font=fit(sub, 26, MAXW, bold=False), fill=(202, 195, 179))

# No domain here on purpose: the site is mid-migration between hosts, and a
# baked-in URL is the one thing on this card that can silently go stale.
foot = "Jupiter & Palm Beach Gardens, FL   •   (561) 915-1934"
d.text((80, 540), foot, font=fit(foot, 26, MAXW), fill=(255, 255, 255))

img.save("assets/img/og-image.png", optimize=True)
print("Wrote assets/img/og-image.png")
