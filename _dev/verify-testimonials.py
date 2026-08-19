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
"""
import html
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "_src" / "pages" / "reviews.html"

SOURCES = {
    "practice testimonials page": "https://jupiterlaser.com/testimonials/",
    "Healthgrades profile": "https://www.healthgrades.com/physician/dr-orlando-cedeno-xq8jf",
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

    print(f"verify-testimonials: {len(quotes)} quote(s) against {len(sources)} source(s)\n")
    bad = []
    for i, quote in enumerate(quotes, 1):
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

    print(f"\n  OK -- all {len(quotes)} quotes are verbatim")


if __name__ == "__main__":
    main()
