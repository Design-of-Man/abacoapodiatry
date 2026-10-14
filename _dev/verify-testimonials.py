#!/usr/bin/env python3
"""Prove every quote on /reviews/ is copied verbatim from a real source.

    python3 _dev/verify-testimonials.py

Refetches jupiterlaser.com/testimonials/ and Dr. Cedeno's Healthgrades profile,
strips both to plain text, and asserts that every contiguous span of every quote
on the reviews page appears in one of them character for character.

Why this exists rather than a one-time read-through: the quotes originally on
that page came through a search summarizer and had been lightly normalised --
a patient's "kind, caring and through" had become "thorough", and one quote
spliced two non-adjacent sentences into what read as a single sentence. Both
are the kind of thing that survives a careful human proofread and does not
survive a string match. Misquoting a real patient on a medical site is the risk
this page carries, so the check is mechanical.

How quotes are built, and what this enforces:

  * A quote is one or more contiguous spans copied exactly from a source.
  * A horizontal ellipsis marks every place a span was trimmed or joined.
    Anything else between two spans is a splice, and this script fails on it.
  * Spans are chosen so nothing needs editing to read cleanly. Two sources
    contain typos ("kind, caring and through", "saw me o a regular basis");
    those sentences are quoted around, never silently corrected.
  * Curly apostrophes and quotes are folded to straight, matching the rest of
    the site. That is the only permitted difference, and it is applied to the
    source side too, so it can never hide a wording change.

Exits non-zero on any mismatch, so it can gate a launch the same way
preflight.py does. Needs network: both hosts must be reachable.

CHANGED 2026-10-14: the practice testimonials page is no longer a source.
Since the 2026-08-18 cutover, jupiterlaser.com/testimonials/ 301s to this
site's own /reviews/, so "verifying" against it compared the page with itself
and passed every quote, including the Healthgrades ones. The six practice
testimonials were verified against the real old page on 2026-08-14 (commit
e4890f95); they are now frozen below, byte for byte, and any edit to one fails.
Healthgrades is still fetched live and is still a real, independent source.

Quotes reused on service and condition pages (any <figure class="testi">
outside /reviews/) must be identical to a quote on /reviews/, so the
verification above covers them too.
"""
import html
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "_src" / "pages" / "reviews.html"

SOURCES = {
    "Healthgrades profile": "https://www.healthgrades.com/physician/dr-orlando-cedeno-xq8jf",
}

# Verified 2026-08-14 against the pre-cutover jupiterlaser.com/testimonials/
# (commit e4890f95). That page no longer exists independently; see docstring.
FROZEN_PRACTICE_TESTIMONIALS = {
    "I can't say enough about Dr. Cedeno and his staff! I was very nervous about my vein procedure… He and his staff put me at ease and the procedure was truly easier than I had thought! I'm so happy with the relief I have gotten after my 1st treatment!",
    "My appointment with Dr. Cedeno couldn't have gone better! I live in New Jersey and injured my foot while on vacation. I called the office and they were super accommodating and scheduled me the next day for an evaluation.",
    "Dr Orlando Cedeno is beyond a 5 star doctor! … I had to go to wound care with him and I am so glad my doctor recommended him … Best experience ever in a doctors office! Everyone treats you like family!!",
    "Dr. Cedeno was great before, during and after the surgery. … The laser treatments definitely helped. The staff at the office was very professional and caring especially the two nurse assistants!!",
    "Dr. Cedeno was knowledgeable and very thorough. … His staff was friendly and efficient. I loved the fact that I did not have to wait a long time for my appt. I highly recommend him!",
    "From the minute I walked in til I left everyone was so fantastic. Dr Cedeno explained so simply what I needed to get better quick!",
}

# Curly to straight, and both dashes to a hyphen. Applied to page and source
# alike, so a fold can never mask a difference in wording.
FOLD = [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
        ("–", "-"), ("—", "-")]
ELLIPSIS = "…"


def plain(markup: str) -> str:
    """Markup to a single normalised line of text."""
    markup = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", markup)
    markup = re.sub(r"(?s)<!--.*?-->", " ", markup)
    markup = re.sub(r"<[^>]+>", " ", markup)
    markup = html.unescape(markup)
    for a, b in FOLD:
        markup = markup.replace(a, b)
    return re.sub(r"\s+", " ", markup)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def main() -> None:
    sources = {}
    for name, url in SOURCES.items():
        try:
            sources[name] = plain(fetch(url))
        except Exception as exc:
            sys.exit(f"could not fetch {name} ({url}): {exc}\n"
                     f"Both hosts must be reachable for this check to mean anything.")

    page = re.sub(r"(?s)<!--.*?-->", " ", REVIEWS.read_text())
    quotes = re.findall(r"&ldquo;(.*?)&rdquo;", page, re.S)
    if not quotes:
        sys.exit(f"no quotes found in {REVIEWS.relative_to(ROOT)} -- has the markup changed?")

    print(f"verify-testimonials: {len(quotes)} quote(s) against {len(sources)} live source(s)"
          f" + {len(FROZEN_PRACTICE_TESTIMONIALS)} frozen 2026-08-14 testimonials\n")
    frozen = {plain(q).strip() for q in FROZEN_PRACTICE_TESTIMONIALS}
    bad = []
    for i, quote in enumerate(quotes, 1):
        if plain(quote).strip() in frozen:
            print(f"  {i:>2}. verbatim   frozen      practice testimonial (verified 2026-08-14)")
            continue
        spans = [s.strip() for s in plain(quote).split(ELLIPSIS) if s.strip()]
        hits = [[n for n, text in sources.items() if s in text] for s in spans]
        if all(hits):
            found = ", ".join(dict.fromkeys(h[0] for h in hits))
            print(f"  {i:>2}. verbatim   {len(spans)} span(s)  {found}")
        else:
            bad.append(i)
            print(f"  {i:>2}. MISMATCH   {len(spans)} span(s)")
            for span, hit in zip(spans, hits):
                if not hit:
                    print(f"        not in either source: {span[:150]}")

    if bad:
        print(f"\n  FAIL -- {len(bad)} quote(s) are not verbatim: {bad}")
        print("  Re-copy from the source. Do not tidy a patient's grammar, and use")
        print(f"  '{ELLIPSIS}' wherever you trim or join, or the join is a splice.")
        sys.exit(1)

    # Reused quotes elsewhere must be identical to a /reviews/ quote.
    on_reviews = {plain(q).strip() for q in quotes}
    reuse_bad = []
    for src in sorted((ROOT / "_src" / "pages").glob("*.html")):
        if src.name == REVIEWS.name:
            continue
        text = re.sub(r"(?s)<!--.*?-->", " ", src.read_text())
        for fig in re.findall(r'(?s)<figure class="testi".*?</figure>', text):
            for q in re.findall(r"&ldquo;(.*?)&rdquo;", fig, re.S):
                if plain(q).strip() not in on_reviews:
                    reuse_bad.append(f"{src.name}: {plain(q)[:90]}")
                else:
                    print(f"      reused verbatim on {src.name}")
    if reuse_bad:
        print("\n  FAIL -- quote(s) outside /reviews/ that are not identical to a /reviews/ quote:")
        for b in reuse_bad:
            print(f"    - {b}")
        sys.exit(1)

    print(f"\n  OK -- all {len(quotes)} quotes are verbatim")


if __name__ == "__main__":
    main()
