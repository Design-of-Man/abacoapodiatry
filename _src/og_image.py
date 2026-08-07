#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph share image (assets/img/og-image.png)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), (12, 11, 8))
d = ImageDraw.Draw(img)

# Vertical navy gradient
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

# Laser beam sweep
for off, col in [(-3, (232, 199, 120)), (0, (211, 172, 87)), (3, (138, 106, 42))]:
    d.line([(0, 470 + off), (W, 380 + off)], fill=col, width=2)

def font(size, bold=True):
    for name in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

# Planet mark
mx, my, mr = 140, 150, 58
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(211, 172, 87), outline=(232, 199, 120), width=3)
for band in (-22, 0, 22):
    d.arc([mx - mr + 12, my + band - 12, mx + mr - 12, my + band + 12], 200, 340, fill=(250, 246, 235), width=4)
d.ellipse([mx - mr - 34, my - 16, mx + mr + 34, my + 16], outline=(232, 199, 120), width=3)

d.text((230, 105), "ABACOA PODIATRY", font=font(54), fill=(255, 255, 255))
d.text((233, 172), "& LEG VEIN CENTER  •  JUPITER LASER", font=font(27), fill=(232, 199, 120))

d.text((80, 300), "Heal Faster. Hurt Less.", font=font(58), fill=(255, 255, 255))
d.text((80, 375), "Without Surgery or Drugs.", font=font(58), fill=(232, 199, 120))

d.text((80, 490), "FDA-Cleared MLS Laser Therapy  •  Shockwave  •  Regenerative Medicine",
       font=font(26, bold=False), fill=(202, 195, 179))
d.text((80, 540), "Jupiter, FL   •   (561) 915-1934   •   jupiterlaser.com",
       font=font(26), fill=(255, 255, 255))

img.save("assets/img/og-image.png", optimize=True)
print("Wrote assets/img/og-image.png")
