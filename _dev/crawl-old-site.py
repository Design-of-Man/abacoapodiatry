#!/usr/bin/env python3
"""Inventory every URL on the old WordPress site, with enough content to map it.

    python3 _dev/crawl-old-site.py            # crawl and cache
    python3 _dev/crawl-old-site.py --coverage # report gaps against vercel.json

Writes _dev/old-site-urls.tsv: path, sitemap, title, h1, words.

Why the titles matter. Redirecting a 100-post back-catalogue by reading slugs is how you
end up sending "best-running-shoes-2026-jupiter-podiatrist" to /services/ because it
contains the word "podiatrist". The mapping is a judgment about what a page is *about*,
and that needs its title and heading, so this fetches them once and caches them.

Why every URL needs a target. 132 of the old site's 157 URLs had neither a redirect nor a
matching path on the new site, so at cutover they 404 and drop whatever ranking history
they carry. That is the whole risk this file exists to close.

Redirect to the closest equivalent, never to the homepage in bulk: Google treats a mass
redirect to / as a soft 404 and discards the link equity, which defeats the point.

Needs network. jupiterlaser.com must be reachable from wherever this runs -- it was 403
at this environment's egress proxy until 2026-08-14.
"""
import argparse
import concurrent.futures as cf
import html
import json
import pathlib
import re
import sys
import urllib.parse as up
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_dev" / "old-site-urls.tsv"
INDEX = "https://jupiterlaser.com/sitemap_index.xml"
UA = {"User-Agent": "Mozilla/5.0 (compatible; site-migration-audit)"}


def get(url: str, timeout: int = 40) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def locs(xml: str) -> list:
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S)


def text_of(markup: str, pattern: str) -> str:
    m = re.search(pattern, markup, re.I | re.S)
    if not m:
        return ""
    inner = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", html.unescape(inner)).strip()


def probe(url: str) -> dict:
    path = up.urlparse(url).path.rstrip("/") or "/"
    try:
        body = get(url)
    except Exception as exc:
        return {"path": path, "title": f"<fetch failed: {exc}>", "h1": "", "words": 0}
    title = text_of(body, r"<title[^>]*>(.*?)</title>")
    # Yoast appends a site suffix to nearly every title; it is noise for mapping.
    title = re.sub(r"\s*[|\-–—]\s*Jupiter Laser.*$", "", title).strip()
    h1 = text_of(body, r"<h1[^>]*>(.*?)</h1>")
    stripped = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", body)
    words = len(re.sub(r"<[^>]+>", " ", stripped).split())
    return {"path": path, "title": title, "h1": h1, "words": words}


def crawl() -> list:
    print(f"reading {INDEX}")
    children = locs(get(INDEX))
    print(f"  {len(children)} child sitemap(s)")

    seen, rows = set(), []
    for child in children:
        kind = re.sub(r"-sitemap\.xml$", "", child.rsplit("/", 1)[-1])
        urls = [u for u in locs(get(child)) if u not in seen]
        seen.update(urls)
        print(f"  {kind:<10} {len(urls):>3} URL(s)")
        for u in urls:
            rows.append({"url": u, "sitemap": kind})

    print(f"\nfetching {len(rows)} page(s) for titles")
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda r: probe(r["url"]), rows))
    for row, res in zip(rows, results):
        row.update(res)

    rows.sort(key=lambda r: r["path"])
    with OUT.open("w") as fh:
        fh.write("path\tsitemap\ttitle\th1\twords\n")
        for r in rows:
            fh.write(f"{r['path']}\t{r['sitemap']}\t{r['title']}\t{r['h1']}\t{r['words']}\n")
    failed = [r for r in rows if r["title"].startswith("<fetch failed")]
    print(f"\nwrote {OUT.relative_to(ROOT)} ({len(rows)} rows"
          + (f", {len(failed)} fetch failures)" if failed else ")"))
    for r in failed:
        print("  FAILED", r["path"])
    return rows


def new_site_paths() -> set:
    paths = set()
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in {"_src", "_dev", "node_modules"}:
            continue
        d = "/" + "/".join(rel.parts[:-1])
        paths.add(d.rstrip("/") or "/")
    return paths


def coverage() -> int:
    if not OUT.exists():
        sys.exit(f"{OUT.relative_to(ROOT)} missing -- run without --coverage first")
    rows = [l.split("\t") for l in OUT.read_text().splitlines()[1:] if l.strip()]
    old = [(r[0], r[1], r[2]) for r in rows]

    vercel = json.loads((ROOT / "vercel.json").read_text())
    sources = {r["source"].rstrip("/") or "/" for r in vercel.get("redirects", [])}
    pages = new_site_paths()

    gaps = [(p, kind, title) for p, kind, title in old
            if p not in sources and p not in pages]
    print(f"old URLs {len(old)} | redirected {sum(1 for p,_,_ in old if p in sources)}"
          f" | unchanged path {sum(1 for p,_,_ in old if p not in sources and p in pages)}"
          f" | UNCOVERED {len(gaps)}")
    for p, kind, title in gaps:
        print(f"  [{kind}] {p}\n        {title}")
    return 1 if gaps else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--coverage", action="store_true",
                    help="report old URLs with no redirect and no matching page")
    args = ap.parse_args()
    sys.exit(coverage() if args.coverage else (crawl() and 0))
