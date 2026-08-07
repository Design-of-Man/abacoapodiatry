#!/usr/bin/env python3
"""Generate the hero poster (assets/img/hero-poster.jpg).

Shown before the lighthouse video loads, if the video is absent, and for
visitors who ask for reduced motion — so it has to stand on its own.
A Jupiter-inlet dusk: warm black sky, gold horizon, lighthouse silhouette.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
img = Image.new("RGB", (W, H), (12, 11, 8))
d = ImageDraw.Draw(img)

HORIZON = int(H * 0.72)

# Sky: deep warm black at top easing into gold near the horizon
for y in range(HORIZON):
    t = (y / HORIZON) ** 2.4
    r = int(12 + (196 - 12) * t)
    g = int(11 + (150 - 11) * t)
    b = int(8 + (74 - 8) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Sun glow just above the horizon
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.66), HORIZON - 20
for i in range(460, 0, -3):
    gd.ellipse([cx - i, cy - int(i * 0.55), cx + i, cy + int(i * 0.55)],
               fill=int(120 * (1 - i / 460) ** 1.7))
glow = glow.filter(ImageFilter.GaussianBlur(28))
img = Image.composite(Image.new("RGB", (W, H), (255, 214, 138)), img, glow)
d = ImageDraw.Draw(img)

# Water: darker, with a gold sun column and horizontal ripple banding
for y in range(HORIZON, H):
    t = (y - HORIZON) / (H - HORIZON)
    r = int(74 - 62 * t)
    g = int(58 - 48 * t)
    b = int(30 - 23 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Ripples are drawn onto their own layer and blurred, so the sun column reads
# as shimmering water rather than scan lines.
ripple = Image.new("L", (W, H), 0)
rd = ImageDraw.Draw(ripple)
for y in range(HORIZON, H, 3):
    t = (y - HORIZON) / (H - HORIZON)
    spread = 40 + t * 420
    amp = int(230 * (1 - t) ** 1.4)
    if amp <= 0:
        continue
    wob = math.sin(y * 0.35) * spread * 0.35
    rd.line([(cx - spread + wob, y), (cx + spread + wob, y)], fill=amp, width=2)
ripple = ripple.filter(ImageFilter.GaussianBlur(5))
img = Image.composite(Image.new("RGB", (W, H), (255, 208, 122)), img, ripple)
d = ImageDraw.Draw(img)

# Distant land strip
d.rectangle([0, HORIZON - 4, W, HORIZON + 2], fill=(30, 25, 15))

# --- Lighthouse silhouette (left third, classic tapered tower) ---
bx, by = int(W * 0.235), HORIZON + 8
tower_h = int(H * 0.46)
base_w, top_w = 118, 66
top_y = by - tower_h

d.polygon([(bx - base_w // 2, by), (bx + base_w // 2, by),
           (bx + top_w // 2, top_y), (bx - top_w // 2, top_y)], fill=(16, 14, 10))
# gallery deck
d.rectangle([bx - top_w // 2 - 16, top_y - 16, bx + top_w // 2 + 16, top_y], fill=(16, 14, 10))
# lantern room
lr_h = 64
d.rectangle([bx - 30, top_y - 16 - lr_h, bx + 30, top_y - 16], fill=(16, 14, 10))
# lit lamp
d.rectangle([bx - 19, top_y - 12 - lr_h, bx + 19, top_y - 26], fill=(255, 226, 158))
# roof + finial
d.polygon([(bx - 38, top_y - 16 - lr_h), (bx + 38, top_y - 16 - lr_h),
           (bx, top_y - 16 - lr_h - 52)], fill=(16, 14, 10))
d.line([(bx, top_y - 16 - lr_h - 52), (bx, top_y - 16 - lr_h - 74)], fill=(16, 14, 10), width=5)
# keeper's house
d.rectangle([bx + 62, by - 88, bx + 210, by], fill=(16, 14, 10))
d.polygon([(bx + 52, by - 88), (bx + 220, by - 88), (bx + 136, by - 140)], fill=(16, 14, 10))

# Beam sweeping right from the lamp
beam = Image.new("L", (W, H), 0)
bd = ImageDraw.Draw(beam)
lamp = (bx, top_y - 22 - lr_h // 2)
bd.polygon([lamp, (W, lamp[1] - 190), (W, lamp[1] + 250)], fill=46)
bd.polygon([lamp, (W, lamp[1] - 60), (W, lamp[1] + 110)], fill=34)
beam = beam.filter(ImageFilter.GaussianBlur(46))
img = Image.composite(Image.new("RGB", (W, H), (255, 226, 158)), img, beam)
d = ImageDraw.Draw(img)

# Lamp bloom
bloom = Image.new("L", (W, H), 0)
bld = ImageDraw.Draw(bloom)
for i in range(90, 0, -2):
    bld.ellipse([lamp[0] - i, lamp[1] - i, lamp[0] + i, lamp[1] + i],
                fill=int(190 * (1 - i / 90) ** 1.5))
bloom = bloom.filter(ImageFilter.GaussianBlur(16))
img = Image.composite(Image.new("RGB", (W, H), (255, 240, 200)), img, bloom)

# Vignette so hero text stays readable at the edges
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(W * 0.35), -int(H * 0.5), int(W * 1.35), int(H * 1.5)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(240))
img = Image.composite(img, Image.new("RGB", (W, H), (8, 7, 5)), vig)

img.save("assets/img/hero-poster.jpg", quality=82, optimize=True, progressive=True)
print("Wrote assets/img/hero-poster.jpg")
