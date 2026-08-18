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
# 1280x720 rather than full size: this sits behind the hero's dark glass
# panel and is replaced by video within a second, so pixel-peeping detail
# buys nothing while the bytes come straight off the LCP.
WIDTH, HEIGHT = 1280, 720
# The old drawn poster was 47KB. Drone footage of foliage and water will not
# compress that far without visible blocking -- at 1920x1080 JPEG it needed
# quality 43 and 152KB. WebP at 1280x720 lands near 88KB and still looks right,
# which is the trade worth making to stop shipping a cartoon.
TARGET_BYTES = 95_000


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
