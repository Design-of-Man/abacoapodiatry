#!/usr/bin/env python3
"""Generate the hero poster from the hero video's own opening frame.

    python3 _src/poster.py

This used to draw a lighthouse with gradients and polygons, and it looked like
it: a black triangle and a blocky hut over an orange gradient. On load you saw
that cartoon, then it was replaced by drone footage of the actual Jupiter Inlet
Lighthouse, and the swap was the first thing a visitor noticed about the site.

Taking the poster from frame zero of the video makes the swap invisible, which
is the point. The poster is not decoration:

  - it is the LCP element, preloaded with fetchpriority="high"
  - it is the whole hero for anyone with prefers-reduced-motion, where no video
    is ever attached
  - same for Save-Data and 2g connections, and for browsers without H.264

So it cannot simply be deleted, and it should look like what it stands in for.

Needs ffmpeg. imageio-ffmpeg ships a static build and installs from pypi, which
is reachable through the agent proxy:  pip install imageio-ffmpeg Pillow
"""
import io
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VIDEO = ROOT / "assets" / "video" / "lighthouse-hd.mp4"
OUT = ROOT / "assets" / "img" / "hero-poster.webp"
# Full source resolution (1920x1080), not the 1280x720 this used to write.
#
# The old reasoning was that the poster "is replaced by video within a second,
# so pixel-peeping detail buys nothing". That holds for the common case and
# ignores the three cases listed at the top of this file: under
# prefers-reduced-motion, under Save-Data or 2g, and in a browser that cannot
# play the sources, no video is ever attached and this image IS the hero,
# permanently. At 1280 wide it was being upscaled 2.25x across a 1440px hero on
# a 2x display, and the client reported the hero as blurry -- correctly.
#
# 1920x1080 is the source ceiling; the video itself is 1080p, so anything
# larger would be invented detail, not recovered detail.
WIDTH, HEIGHT = 1920, 1080
# Drone footage of foliage and water does not compress cheaply. WebP at
# 1920x1080 lands near 165KB at a quality that holds up on a 2x display; the
# 1280x720 version was 85KB. ~80KB more on the LCP is the cost of a hero that
# is not visibly soft, and it is still a smaller payload than the hero video
# it sits in front of by more than an order of magnitude.
TARGET_BYTES = 180_000


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("imageio-ffmpeg not installed:  pip install imageio-ffmpeg Pillow")


def main() -> None:
    from PIL import Image

    if not VIDEO.exists():
        sys.exit(f"missing {VIDEO}")

    # Frame zero, full resolution, straight to stdout as PNG so nothing is
    # re-encoded twice.
    raw = subprocess.run(
        [ffmpeg(), "-hide_banner", "-loglevel", "error", "-i", str(VIDEO),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout

    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)

    # Walk the quality down until it fits. Reported so a regression in the
    # source video's compressibility is visible rather than silent.
    for q in range(82, 40, -3):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= TARGET_BYTES:
            break
    OUT.write_bytes(buf.getvalue())
    print(f"Wrote {OUT.relative_to(ROOT)}  {WIDTH}x{HEIGHT}  "
          f"{buf.tell()/1024:.0f}KB at quality {q}")


if __name__ == "__main__":
    main()
