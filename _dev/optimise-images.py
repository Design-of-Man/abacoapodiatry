#!/usr/bin/env python3
"""Turn raw generated images into something safe to ship.

    python3 _dev/optimise-images.py

Drop the raw downloads into assets/img/atmos/ with the filenames from
_dev/image-prompts.md, then run this. Each one is resized, converted to WebP
under a size budget, and the original is moved to _dev/atmos-raw/ so it is kept
but never deployed (.vercelignore excludes _dev/).

Why the budget is not negotiable: PR #12 cut the mobile payload 68% by fixing
the hero video, and thirty-odd unoptimised 1K rasters would hand all of that
straight back. Anything that cannot get under budget while still looking right
is reported rather than silently shipped heavy -- drop it instead.

Needs Pillow, which installs from pypi (one of the few hosts the agent proxy
allows):  pip install Pillow
"""
import io
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATMOS = ROOT / "assets" / "img" / "atmos"
KEEP = ROOT / "_dev" / "atmos-raw"

# These display at roughly 700-860px inside .wrap-narrow, so 1200 covers a 1.5x
# screen without paying for detail nobody sees.
MAX_WIDTH = 1200
TARGET_BYTES = 90_000
SOURCES = {".png", ".jpg", ".jpeg", ".webp", ".avif"}


def main() -> None:
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow missing:  pip install Pillow")

    if not ATMOS.is_dir():
        sys.exit(f"nothing to do, {ATMOS.relative_to(ROOT)} does not exist")

    raw = [p for p in sorted(ATMOS.iterdir())
           if p.is_file() and p.suffix.lower() in SOURCES
           and not p.name.endswith(".opt.webp")]
    if not raw:
        print("  no raw images found")
        return

    KEEP.mkdir(parents=True, exist_ok=True)
    total_before = total_after = 0
    over = []

    for src in raw:
        before = src.stat().st_size
        img = Image.open(src).convert("RGB")
        if img.width > MAX_WIDTH:
            img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)),
                             Image.LANCZOS)

        for q in range(82, 40, -3):
            buf = io.BytesIO()
            img.save(buf, "WEBP", quality=q, method=6)
            if buf.tell() <= TARGET_BYTES:
                break

        out = ATMOS / f"{src.stem}.opt.webp"
        out.write_bytes(buf.getvalue())
        shutil.move(str(src), KEEP / src.name)

        total_before += before
        total_after += buf.tell()
        flag = ""
        if buf.tell() > TARGET_BYTES:
            over.append(src.stem)
            flag = "  OVER BUDGET"
        print(f"  {src.stem:<28} {before/1024:6.0f}KB -> {buf.tell()/1024:5.0f}KB  "
              f"q{q} {img.width}x{img.height}{flag}")

    print(f"\n  {len(raw)} image(s): {total_before/1024:.0f}KB -> {total_after/1024:.0f}KB "
          f"({total_after/total_before*100:.0f}% of original)")
    print(f"  originals kept in {KEEP.relative_to(ROOT)}/ (not deployed)")
    if over:
        print(f"\n  {len(over)} could not reach {TARGET_BYTES//1024}KB even at low quality:")
        for n in over:
            print(f"    {n}")
        print("  Regenerate these simpler, or drop them. Do not ship them heavy.")


if __name__ == "__main__":
    main()
