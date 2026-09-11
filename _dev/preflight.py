#!/usr/bin/env python3
"""Hard-failing pre-launch gate for the built site.

Run it on the generated output, not the sources:

    python3 _src/build.py && python3 _dev/preflight.py

Exits non-zero on any failure. That is the whole point — a check that only
prints is a suggestion, and suggestions do not stop a bad deploy.

Every check here exists because this repo actually shipped the thing it
catches: an empty meta description (a quoted phrase closed the attribute
early), images referenced but never committed, unverified patient
testimonials left behind a LAUNCH TODO marker on a public medical site.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_src", "_dev", "assets", ".git", "node_modules"}

# Markers that mean "not finished", wherever they appear in source or output.
PLACEHOLDER_RE = re.compile(r"LAUNCH TODO|REPLACE_[A-Z_]+|YOUR_FORM_ID|lorem ipsum", re.I)

failures = []
notes = []


def fail(category, detail):
    failures.append((category, detail))


def pages():
    """Built, indexable pages. Redirect stubs are generated and exempt."""
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        html = p.read_text(encoding="utf-8", errors="replace")
        if 'http-equiv="refresh"' in html.lower():
            continue
        yield p, html


def rel(p):
    return str(p.relative_to(ROOT))


def main():
    titles, descs = Counter(), Counter()
    seen_pages = []

    for path, html in pages():
        r = rel(path)
        seen_pages.append(path)

        # --- title / description -------------------------------------------
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        if not m or not m.group(1).strip():
            fail("meta", f"{r}: missing or empty <title>")
        else:
            titles[m.group(1).strip()] += 1

        m = re.search(r'<meta name="description" content="(.*?)"\s*/?>', html, re.S)
        if not m:
            fail("meta", f"{r}: no meta description")
        elif not m.group(1).strip():
            # The exact failure cond-sprains.html shipped: an unescaped quote
            # closed content="" on its first character.
            fail("meta", f"{r}: meta description is EMPTY (unescaped quote in the value?)")
        else:
            descs[m.group(1).strip()] += 1

        # --- structure ------------------------------------------------------
        h1s = re.findall(r"<h1[^>]*>", html, re.I)
        if len(h1s) != 1:
            fail("structure", f"{r}: {len(h1s)} <h1> elements, expected exactly 1")

        for img in re.findall(r"<img\b[^>]*>", html, re.I):
            if not re.search(r"\balt\s*=", img, re.I):
                fail("a11y", f"{r}: <img> without alt — {img[:70]}")

        # --- structured data -------------------------------------------------
        for block in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        ):
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                fail("schema", f"{r}: invalid JSON-LD — {e}")

        # --- placeholders ----------------------------------------------------
        for hit in set(PLACEHOLDER_RE.findall(html)):
            fail("placeholder", f"{r}: contains {hit!r}")

        # --- referenced local assets exist -----------------------------------
        for url in set(re.findall(r'(?:src|href)="(/assets/[^"?#]+)"', html)):
            if not (ROOT / url.lstrip("/")).exists():
                fail("assets", f"{r}: references missing {url}")

        # --- internal links resolve ------------------------------------------
        for url in set(re.findall(r'href="(/[^"#?]*)"', html)):
            target = url.strip("/")
            if not target:
                continue
            candidate = ROOT / target
            if candidate.is_file() or (candidate / "index.html").exists():
                continue
            fail("links", f"{r}: internal link 404s — {url}")

    # --- placeholders in the sources too -------------------------------------
    for src in sorted((ROOT / "_src" / "pages").glob("*.html")):
        text = src.read_text(encoding="utf-8", errors="replace")
        for hit in set(PLACEHOLDER_RE.findall(text)):
            fail("placeholder", f"_src/pages/{src.name}: contains {hit!r}")

    # --- uniqueness -----------------------------------------------------------
    for t, n in titles.items():
        if n > 1:
            fail("meta", f"duplicate <title> on {n} pages: {t[:70]!r}")
    for d, n in descs.items():
        if n > 1:
            fail("meta", f"duplicate description on {n} pages: {d[:60]!r}")

    # --- redirects land somewhere real ----------------------------------------
    vercel = ROOT / "vercel.json"
    if vercel.exists():
        conf = json.loads(vercel.read_text(encoding="utf-8"))
        for rule in conf.get("redirects", []):
            dest = rule["destination"].strip("/")
            if dest and not (
                (ROOT / dest).is_file() or (ROOT / dest / "index.html").exists()
            ):
                fail("redirects", f"301 {rule['source']} -> {rule['destination']} (missing)")
        if not any(h.get("has") for h in conf.get("headers", [])):
            notes.append(
                "vercel.json has no host-scoped header rule — the *.vercel.app "
                "noindex guard may have been removed."
            )
    else:
        fail("config", "vercel.json is missing — redirects and headers are not configured")

    if not (ROOT / ".vercelignore").exists():
        fail("config", ".vercelignore missing — _src/ and internal .md files would be served")

    # --- opening hours, in the two files the build cannot reach ---------------
    # _src/hours.py is the single source of truth and build.py renders it into
    # every generated page. assets/js/assistant.js and llms.txt are hand-written
    # and regenerate from nothing, so they are exactly where hours drift back
    # out of step -- which is how the Palm Beach Gardens schema ended up
    # asserting Jupiter's Mon-Thu 8-5 for an office open Monday and Wednesday.
    # Matching on the distinctive closing time rather than a whole rendered
    # string keeps this from failing on ordinary copy edits.
    sys.path.insert(0, str(ROOT / "_src"))
    try:
        import hours as _hours
    except Exception as e:                                  # pragma: no cover
        fail("hours", f"cannot import _src/hours.py — {e}")
    else:
        pbg_close = _hours.PALM_BEACH_GARDENS.days["Wednesday"][1]   # "16:30"
        pbg_12h = _hours._h12(pbg_close)                             # "4:30 PM"
        for rel_path in ("assets/js/assistant.js", "llms.txt"):
            f = ROOT / rel_path
            if not f.exists():
                fail("hours", f"{rel_path} is missing")
                continue
            text = f.read_text(encoding="utf-8")
            if "Palm Beach Gardens" not in text:
                fail("hours", f"{rel_path}: no mention of the Palm Beach Gardens office")
            elif pbg_12h not in text and pbg_close not in text:
                fail("hours", f"{rel_path}: Palm Beach Gardens hours are stale — "
                              f"expected {pbg_12h} from _src/hours.py")

    # --- report ---------------------------------------------------------------
    print(f"preflight: {len(seen_pages)} pages checked\n")
    if notes:
        for n in notes:
            print(f"  note: {n}")
        print()
    if not failures:
        print("  PASS — nothing blocking launch")
        return 0

    by_cat = {}
    for cat, detail in failures:
        by_cat.setdefault(cat, []).append(detail)
    for cat in sorted(by_cat):
        items = by_cat[cat]
        print(f"  {cat.upper()} ({len(items)})")
        for d in items[:12]:
            print(f"    - {d}")
        if len(items) > 12:
            print(f"    ... and {len(items) - 12} more")
        print()
    print(f"  FAIL — {len(failures)} blocking issue(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
