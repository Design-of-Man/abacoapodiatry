#!/usr/bin/env python3
"""The rolling Instagram strip on the homepage.

Data-driven, the same way locations.py is: this reads POSTS below and the
matching files in assets/img/instagram/. If a post's image is not on disk the
post is skipped, and if none are on disk the whole section returns "" and the
homepage simply does not have the band. That is deliberate -- preflight hard
fails on an <img> whose file is missing, so the section must never render ahead
of its assets.

There is no runtime JavaScript and no external request. Instagram retired the
old embed API in 2024, so a live feed now needs a Business account, a Facebook
Page and a token that expires every 60 days -- the feed would silently freeze
when it lapsed. Curated and self-hosted keeps the page fast, keeps a medical
site free of third-party tracking, and cannot break on someone else's schedule.

To add a post: optimise the image into assets/img/instagram/<slug>.opt.webp
(python3 _dev/optimise-images.py handles the conversion), then add a row here.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "img" / "instagram"

HANDLE = "@abacoapodiatry"
PROFILE_URL = "https://www.instagram.com/abacoapodiatry/"

# slug, width, height, alt (for a screen reader), caption (visible label)
#
# Dimensions are recorded here rather than read from the file so the build stays
# dependency-free -- build.py must not need Pillow. They are printed by
# `python3 _dev/optimise-images.py instagram`; copy them across when adding a
# post. Getting one wrong costs layout shift, so `python3 _src/instagram.py`
# checks every row against the real file.
#
# The strip holds a uniform height and lets width follow the image, so nothing
# is cropped. These posts are a mix of near-square before/after collages and
# tall portraits; forcing them all into one aspect ratio sliced the "After" half
# off the collages.
POSTS = [
    ("bunion-xray-before-after", 640, 588,
     "Before and after X-rays of a bunion correction, the realigned bones held with surgical screws",
     "Bunion correction, before &amp; after"),
    ("mis-bunion-before", 640, 787,
     "A foot photographed before minimally invasive bunion surgery, showing the bump at the base of the big toe",
     "Before minimally invasive bunion surgery"),
    ("mis-bunion-3-weeks", 640, 788,
     "The same foot three weeks after minimally invasive bunion surgery, with small healed incision marks",
     "Three weeks after surgery"),
    ("toenail-before-after", 640, 583,
     "Before and after photographs of toenail treatment, showing clearer nail growing in",
     "Toenail restoration progress"),
    ("dr-cedeno-surgery", 640, 669,
     "Dr. Cedeno in the operating room during a foot reconstruction, an external fixation frame in place",
     "Dr. Cedeno in reconstruction surgery"),
    ("dr-cedeno-imaging", 640, 723,
     "Dr. Cedeno positioning a mobile imaging arm in the operating room",
     "Imaging during a procedure"),
    ("dr-cedeno-profile", 640, 787,
     "A profile card introducing Dr. Cedeno, podiatrist and foot and ankle surgeon",
     "Meet Dr. Cedeno"),
    ("dr-mustafa-regenerative", 640, 787,
     "A profile card for Dr. Isin A. Mustafa introducing regenerative care for ankles and feet",
     "Regenerative care with Dr. Mustafa"),
]


def _available():
    """POSTS whose image is actually on disk, in order."""
    return [p for p in POSTS if (IMG_DIR / f"{p[0]}.opt.webp").is_file()]


def _tile(slug, w, h, alt, caption, duplicate=False):
    # The duplicated half of the track is decorative: it exists only so the
    # animation can loop seamlessly. Hiding it from assistive tech stops every
    # post being announced twice.
    hide = ' aria-hidden="true"' if duplicate else ""
    # aspect-ratio on the <li> reserves the tile's width from its fixed height
    # before the image decodes, so a variable-width strip still shifts nothing.
    return (
        f'          <li class="ig-item" style="aspect-ratio:{w}/{h}"{hide}>\n'
        f'            <img src="/assets/img/instagram/{slug}.opt.webp" alt="{html.escape(alt, quote=True)}"\n'
        f'                 width="{w}" height="{h}" loading="lazy" decoding="async">\n'
        f'            <span class="ig-cap">{caption}</span>\n'
        f'          </li>\n'
    )


def feed_html():
    """The homepage Instagram band, or "" when no images are present."""
    posts = _available()
    if not posts:
        return ""

    # The track is rendered twice back to back. The animation translates it by
    # exactly -50%, so the second copy lands where the first began and the loop
    # has no visible seam. Duration scales with the number of posts so the strip
    # always travels at the same speed regardless of how many are in it.
    tiles = "".join(_tile(*p) for p in posts)
    tiles += "".join(_tile(*p, duplicate=True) for p in posts)
    seconds = len(posts) * 7

    return f"""
    <!-- ================= INSTAGRAM ================= -->
    <section class="section section-mist ig-section">
      <div class="wrap">
        <div class="ig-head" data-reveal>
          <div>
            <span class="kicker">From the practice</span>
            <h2>Recent work, straight from our feed</h2>
          </div>
          <a class="btn btn-ghost" href="{PROFILE_URL}" rel="noopener">Follow {HANDLE}</a>
        </div>
      </div>

      <div class="ig-viewport" tabindex="0" role="region"
           aria-label="Recent posts from our Instagram feed, scrollable">
        <ul class="ig-track" style="--ig-duration:{seconds}s">
{tiles}        </ul>
      </div>

      <div class="wrap">
        <p class="ig-note">Individual results may vary. Clinical images are shared with
        patient permission and are not a promise of any particular outcome.</p>
      </div>
    </section>
"""


if __name__ == "__main__":
    have = _available()
    print(f"{len(have)}/{len(POSTS)} post images present in {IMG_DIR.relative_to(ROOT)}/")
    bad = 0
    for slug, w, h, _, _ in POSTS:
        f = IMG_DIR / f"{slug}.opt.webp"
        if not f.is_file():
            print(f"  MISSING {slug}.opt.webp")
            continue
        note = ""
        try:  # Pillow is a dev-time convenience here, never needed by the build.
            from PIL import Image
            rw, rh = Image.open(f).size
            if (rw, rh) != (w, h):
                note = f"  <-- WRONG, file is {rw}x{rh}; layout will shift"
                bad += 1
        except ImportError:
            note = "  (install Pillow to verify dimensions)"
        print(f"  ok      {slug}.opt.webp  {w}x{h}{note}")
    if bad:
        raise SystemExit(f"\n{bad} row(s) disagree with the file on disk.")
