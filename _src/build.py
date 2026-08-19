#!/usr/bin/env python3
"""Static site builder for jupiterlaser.com.

Each file in _src/pages/ starts with a JSON meta block:

    <!--META
    { "path": "services/mls-laser-therapy/", "title": "...", ... }
    META-->
    ...page HTML...

Run `python3 _src/build.py` from the repo root (or anywhere). It wraps every
page in _src/template.html, writes it to the site root, and regenerates
sitemap.xml. Nothing else on the site is generated — CSS/JS/images are static.
"""
import functools
import hashlib
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path


def _git(*args):
    """Run a git command from the repo root, returning stdout or "" on any failure."""
    try:
        r = subprocess.run(("git",) + args, cwd=str(ROOT), capture_output=True,
                           text=True, timeout=15)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


@functools.lru_cache(maxsize=1)
def modified_dates():
    """Map repo-relative path -> the date its content actually last changed.

    Answer engines weight recency, which is exactly why this must not be the
    build date: stamping today onto all 54 pages every rebuild would assert a
    freshness that isn't real, the same way a blanket sitemap lastmod does. So
    the date comes from the last commit that touched the file, and a file with
    uncommitted edits is dated today because it genuinely is being changed now.
    Outside a git checkout this returns nothing and callers omit the field --
    an absent dateModified beats a wrong one.
    """
    dates, cur = {}, None
    for line in _git("log", "--name-only", "--format=%cs", "--", "_src").splitlines():
        line = line.strip()
        if not line:
            continue
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", line):
            cur = line
        elif cur and line not in dates:
            dates[line] = cur          # log is newest-first, so first hit wins
    today = date.today().isoformat()
    for line in _git("status", "--porcelain", "--", "_src").splitlines():
        path = line[3:].strip().strip('"')
        if path:
            dates[path] = today
    return dates


def esc(value):
    """HTML-escape a meta value before it goes into markup.

    Titles and descriptions land in two hostile places: inside <title>, which is
    RCDATA where a bare `&` starts an entity reference, and inside
    content="..." attributes, where a literal `"` closes the attribute early and
    silently truncates the value. Both occur in real page metadata -- an
    apostrophe-free quote in a description is enough to destroy it.
    """
    return html.escape(str(value), quote=True)

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
PAGES = SRC / "pages"
# Canonical domain for canonicals, schema @ids, and sitemap URLs.
# The site is branded Abacoa Podiatry & Leg Vein Center but currently targets
# the jupiterlaser.com domain (the site being replaced, which holds the existing
# rankings). To launch on a different domain instead, set SITE_ORIGIN:
#     SITE_ORIGIN=https://abacoapodiatry.com python3 _src/build.py
import os
BASE_URL = os.environ.get("SITE_ORIGIN", "https://jupiterlaser.com").rstrip("/")

# Social preview images must resolve on the host actually SERVING the page.
#
# Before the 2026-08-18 cutover this defaulted to the *.vercel.app host,
# because jupiterlaser.com still served the client's old site: an og:image
# there 404'd and scrapers fell back to whatever in-page image they could
# find, which is the transparent logo, and iMessage paints transparency on
# grey. That is no longer true -- the domain now serves this site, so the
# default is the real domain and a plain `python3 _src/build.py` no longer
# silently reverts the cutover.
#
# Override only to preview on a host that is not the canonical domain:
#     IMAGE_ORIGIN=https://abacoapodiatry.vercel.app python3 _src/build.py
IMAGE_ORIGIN = os.environ.get("IMAGE_ORIGIN", BASE_URL).rstrip("/")

sys.path.insert(0, str(SRC))
from locations import location_pages  # noqa: E402
import instagram  # noqa: E402
import hours  # noqa: E402

META_RE = re.compile(r"^<!--META\s*(\{.*?\})\s*META-->\s*", re.DOTALL)

# Legacy jupiterlaser.com URLs -> new locations, read from _src/redirect-map.tsv.
#
# That file is the single source of truth and this is its only reader. It used to
# be a dict here covering 19 URLs, which was 19 of the 157 the old site actually
# publishes -- the other 138 would have 404'd at cutover. The map was rebuilt from
# a real crawl of all four Yoast sitemaps (_dev/crawl-old-site.py).
#
# Everything downstream is generated from it: vercel.json (the only one that takes
# effect on Vercel), _redirects, .htaccess, and the meta-refresh stubs. Anything
# hand-maintained alongside it drifts, and the two files nobody looks at drift
# first.
REDIRECT_MAP = ROOT / "_src" / "redirect-map.tsv"

# The subset that also gets a meta-refresh stub committed into the repo. Short,
# guessable paths someone might type or have printed on something -- worth a
# fallback if the site is ever served somewhere with no redirect config. The
# other ~140 are long article slugs where a stub earns nothing, and 140 extra
# directories of generated HTML costs more than it saves. Must be a subset of
# the map; the build checks.
STUB_PATHS = {
    "/mls", "/about-us", "/regenerative-medicine", "/neuropathy-solutions",
    "/plantar-fasciitis", "/stem-cell-therapy", "/testimonials", "/what-we-do",
    "/service-areas", "/bbl", "/bunion", "/flat-feet", "/wound-care",
    "/foot-ankle-surgery", "/providers", "/request-an-appointment", "/videos",
    "/flat-feet-flatfoot-types-causes-treatment",
}


def load_redirects():
    """Parse _src/redirect-map.tsv into an ordered [(source, destination)] list."""
    pairs, seen = [], {}
    for lineno, raw in enumerate(
            REDIRECT_MAP.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("old\t"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            sys.exit(f"ERROR: {REDIRECT_MAP.name}:{lineno}: expected tab-separated "
                     f"source and destination, got {line!r}")
        src = "/" + parts[0].strip().strip("/")
        dst = parts[1].strip()
        if src in seen:
            sys.exit(f"ERROR: {REDIRECT_MAP.name}:{lineno}: duplicate source {src} "
                     f"(already at line {seen[src]})")
        if not dst.startswith("/") or not dst.endswith("/"):
            sys.exit(f"ERROR: {REDIRECT_MAP.name}:{lineno}: destination {dst!r} must "
                     f"start and end with /")
        seen[src] = lineno
        pairs.append((src, dst))

    sources = {s for s, _ in pairs}
    # A destination that is itself redirected means two hops, which loses PageRank
    # and trips "redirect chain" in every audit tool.
    for src, dst in pairs:
        if (dst.rstrip("/") or "/") in sources:
            sys.exit(f"ERROR: {REDIRECT_MAP.name}: {src} -> {dst}, but {dst} is itself "
                     f"a redirect source (chain)")
    # Bulk redirects to / are read as soft 404s and the link equity is discarded,
    # which defeats the point of redirecting at all. Use the section hub instead.
    for src, dst in pairs:
        if dst == "/":
            sys.exit(f"ERROR: {REDIRECT_MAP.name}: {src} targets the homepage; "
                     f"redirect to the closest section hub instead")
    missing = STUB_PATHS - sources
    if missing:
        sys.exit(f"ERROR: STUB_PATHS entries not in {REDIRECT_MAP.name}: "
                 f"{sorted(missing)}")
    return pairs

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved: {target} | Abacoa Podiatry</title>
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{base}{target}">
  <meta name="robots" content="noindex">
</head>
<body>
  <p>This page has moved to <a href="{target}">{base}{target}</a>.</p>
</body>
</html>
"""


def build_redirects():
    """Write every redirect surface from _src/redirect-map.tsv.

    vercel.json is the one that actually runs in production; _redirects and
    .htaccess are kept for portability; the stubs are a last-resort fallback for
    a host with no redirect config at all. All four come from the same list so
    they cannot disagree.
    """
    pairs = load_redirects()
    dests = {d for _, d in pairs}

    # Destinations must be real pages. Runs after build_page() so the directories
    # exist -- a typo'd destination would otherwise ship as a 301 into a 404.
    for dest in sorted(dests):
        if not (ROOT / dest.strip("/") / "index.html").exists() and dest != "/":
            sys.exit(f"ERROR: redirect destination {dest} is not a page on this site")

    # ...and a source must NOT be a real page. Vercel matches the redirect table
    # before serving a static file, so a URL that is both ships as a page nobody
    # can reach: the file is right there in the repo and every request to it 301s
    # away. Nothing else in this build would notice -- the page renders, the
    # redirect resolves, and both checks above pass.
    #
    # This is the failure mode of porting an old post back onto its original URL
    # (which is the point of keeping the URL: no redirect, no lost ranking) while
    # leaving its row in the map. STUB_PATHS are the deliberate exception -- the
    # loop below writes a meta-refresh stub *at* the source path on purpose.
    for src, dst in pairs:
        if src in STUB_PATHS:
            continue
        if (ROOT / src.strip("/") / "index.html").exists():
            sys.exit(
                f"ERROR: {src} is both a redirect source and a built page.\n"
                f"  The redirect wins, so the page is unreachable and its {dst} target\n"
                f"  gets the traffic. Either delete the {src} row from\n"
                f"  {REDIRECT_MAP.name}, or delete the page that builds to {src}."
            )

    for old, new in pairs:
        if old not in STUB_PATHS:
            continue
        out = ROOT / old.strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(REDIRECT_HTML.format(target=new, base=BASE_URL), encoding="utf-8")

    netlify = ["# Netlify 301s from legacy jupiterlaser.com URLs. Inert on Vercel,",
               "# which reads vercel.json. GENERATED from _src/redirect-map.tsv.", ""]
    for old, new in pairs:
        netlify.append(f"{old} {new} 301!")
        netlify.append(f"{old}/ {new} 301!")
    (ROOT / "_redirects").write_text("\n".join(netlify) + "\n", encoding="utf-8")

    htaccess = ["# Apache 301s from legacy jupiterlaser.com URLs. Inert on Vercel,",
                "# which reads vercel.json. GENERATED from _src/redirect-map.tsv.",
                "RewriteEngine On"]
    for old, new in pairs:
        htaccess.append(f"RewriteRule ^{old.lstrip('/')}/?$ {new} [R=301,L]")
    htaccess += ["", "# Serve custom 404", "ErrorDocument 404 /404.html"]
    (ROOT / ".htaccess").write_text("\n".join(htaccess) + "\n", encoding="utf-8")

    # vercel.json carries hand-maintained headers and trailingSlash alongside the
    # redirects, so replace only the one key and leave the file otherwise intact.
    #
    # BOTH forms of every source, and the trailing-slash one is the one that
    # works. vercel.json sets "trailingSlash": true, so Vercel 308s /foo to /foo/
    # BEFORE it matches the redirect table. A source written as /foo is therefore
    # never reached: the request arrives as /foo, gets normalised to /foo/, and
    # /foo/ matches nothing. That is not theoretical -- every redirect in this
    # file was slash-less until 2026-08-14, so /veins/, /varicose-veins/ and
    # /venous-insufficiency/ all returned a hard 404 in production, and the only
    # legacy URLs that resolved at all were the 19 with a meta-refresh stub, via
    # the stub rather than via a 301. WordPress publishes every URL with a
    # trailing slash, so the broken form was the only form real traffic used.
    #
    # The slash-less entries are kept because they cost nothing and catch a
    # hand-typed or hand-written link if Vercel's normalisation order ever
    # changes.
    vercel_path = ROOT / "vercel.json"
    vercel = json.loads(vercel_path.read_text(encoding="utf-8"))
    sources = []
    for old, new in pairs:
        sources.append({"source": old + "/", "destination": new, "permanent": True})
        sources.append({"source": old, "destination": new, "permanent": True})
    vercel["redirects"] = sources
    vercel_path.write_text(json.dumps(vercel, indent=2) + "\n", encoding="utf-8")
    return len(pairs)


def build_page(template: str, raw: str, name: str):
    m = META_RE.match(raw)
    if not m:
        sys.exit(f"ERROR: {name} is missing its <!--META ... META--> block")
    try:
        meta = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: bad JSON meta in {name}: {e}")
    content = raw[m.end():]

    path = meta["path"]
    canon = BASE_URL + "/" + path

    schemas = list(meta.get("schema", []))
    crumbs = meta.get("crumbs")
    if crumbs:
        items = [{
            "@type": "ListItem", "position": 1, "name": "Home",
            "item": BASE_URL + "/",
        }]
        for i, (label, url) in enumerate(crumbs, start=2):
            item = {"@type": "ListItem", "position": i, "name": label}
            if url:
                item["item"] = BASE_URL + url
            items.append(item)
        schemas.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items,
        })

    # Fifteen pages -- the homepage, both physician pages, the services and
    # conditions hubs among them -- described the practice and the website but
    # never the document itself. Nothing tied the title, description and URL
    # together as one addressable thing, so there was no node for a physician or
    # a condition to hang off. Give any page that still lacks a page-level entity
    # a plain WebPage built only from metadata it already declares.
    def is_page_entity(s):
        t = s.get("@type")
        return any(str(k).endswith("Page") or k in ("Article", "BlogPosting")
                   for k in (t if isinstance(t, list) else [t]))

    if not any(is_page_entity(s) for s in schemas):
        schemas.insert(0, {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "@id": canon + "#webpage",
            "url": canon,
            "name": meta["title"],
            "description": meta["desc"],
            "inLanguage": "en-US",
            "isPartOf": {"@id": BASE_URL + "/#website"},
            "about": {"@id": BASE_URL + "/#clinic"},
        })

    # Freshness. 50 of the 54 pages carried no date at all, and every answer
    # engine weights recency when picking what to cite. Only page-level entities
    # get one: the clinic and website schemas describe the practice, not this
    # document, and BreadcrumbList is navigation. Location pages have no file of
    # their own -- they are generated from locations.py, so that is genuinely
    # when their content last changed.
    dates = modified_dates()
    modified = dates.get(f"_src/pages/{name}") or dates.get("_src/locations.py")
    if modified:
        for s in schemas:
            t = s.get("@type")
            for kind in (t if isinstance(t, list) else [t]):
                if str(kind).endswith("Page") or kind in ("Article", "BlogPosting"):
                    s.setdefault("dateModified", modified)
                    break

    def ld_json(obj):
        # Escape `<` so a value containing `</script>` cannot terminate the block
        # and spill schema into the document. < is valid JSON and parses back
        # to `<`, so Google and every other consumer still read the original text.
        body = json.dumps(obj, indent=2, ensure_ascii=False).replace("<", "\\u003c")
        return ('  <script type="application/ld+json">\n  %s\n  </script>\n'
                % body.replace("\n", "\n  "))

    schema_html = "".join(ld_json(s) for s in schemas)
    geo_pos = meta.get("geopos", "26.8934;-80.1096")

    if path.endswith(".html"):  # e.g. 404.html
        out_file = ROOT / path
    else:
        out_file = ROOT / path / "index.html" if path else ROOT / "index.html"

    html = (
        template
        .replace("{{TITLE}}", esc(meta["title"]))
        .replace("{{DESC}}", esc(meta["desc"]))
        .replace("{{CANON}}", esc(canon))
        .replace("{{ROBOTS}}", meta.get("robots", "index, follow"))
        .replace("{{OG_TYPE}}", meta.get("ogtype", "website"))
        .replace("{{NAV}}", meta.get("nav", ""))
        # Geo meta defaults to the Jupiter office. The Palm Beach Gardens
        # office page overrides both, so the one page that is genuinely about
        # a different address stops claiming Jupiter's coordinates.
        .replace("{{GEO_PLACE}}", esc(meta.get("geoplace", "Jupiter, Florida")))
        .replace("{{GEO_POS}}", esc(geo_pos))
        .replace("{{GEO_ICBM}}", esc(geo_pos.replace(";", ", ")))
        .replace("{{BODY_CLASS}}", f' class="{meta["bodyclass"]}"' if meta.get("bodyclass") else "")
        .replace("{{SCHEMA}}", schema_html)
        .replace("{{CONTENT}}", content)
        # After CONTENT, since the token lives in a page body. Returns "" when
        # assets/img/instagram/ is empty, so the band never renders ahead of
        # its images and preflight never sees a missing <img>.
        .replace("{{INSTAGRAM_FEED}}", instagram.feed_html())
        # Opening hours, from _src/hours.py. Rendered here rather than written
        # into each file because they appeared in eleven places and had already
        # drifted: the Palm Beach Gardens JSON-LD asserted Jupiter's Mon-Thu
        # 8-5 for an office that opens Monday and Wednesday. One source, so
        # the schema and the page copy cannot disagree again.
        .replace("{{HOURS_JUP_LD}}", hours.ld(hours.JUPITER))
        .replace("{{HOURS_PBG_LD}}", hours.ld(hours.PALM_BEACH_GARDENS))
        .replace("{{HOURS_JUP_LINE}}", hours.line(hours.JUPITER))
        .replace("{{HOURS_PBG_LINE}}", hours.line(hours.PALM_BEACH_GARDENS))
        .replace("{{HOURS_PBG_CLOSED}}", hours.closed_note(hours.PALM_BEACH_GARDENS))
        .replace("{{HOURS_FOOTER}}", hours.footer_html())
        # Last, so it also reaches placeholders inside page-level schema and
        # page bodies -- not just the shared template.
        .replace("{{IMAGE_ORIGIN}}", IMAGE_ORIGIN)
    )

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    return meta


def asset_versions():
    """Map asset URL -> URL?v=<content hash>. Busts long-lived CDN/browser
    caches the moment a file's content changes — without this, visitors can
    get new HTML with months-old CSS."""
    out = {}
    for rel in ["assets/css/main.css", "assets/js/main.js",
                "assets/js/assistant.js", "assets/js/media.js"]:
        f = ROOT / rel
        if f.exists():
            h = hashlib.md5(f.read_bytes()).hexdigest()[:10]
            out["/" + rel] = f"/{rel}?v={h}"
    return out


def main():
    template = (SRC / "template.html").read_text(encoding="utf-8")
    versions = asset_versions()
    for src, versioned in versions.items():
        template = template.replace(f'"{src}"', f'"{versioned}"')
    pages = sorted(PAGES.glob("*.html"))
    if not pages:
        sys.exit("ERROR: no pages found in _src/pages/")

    sitemap_rows = []
    today = date.today().isoformat()
    sources = [(p.name, p.read_text(encoding="utf-8")) for p in pages]
    sources += list(location_pages())
    for name, raw in sources:
        for src, versioned in versions.items():
            raw = raw.replace(f'"{src}"', f'"{versioned}"')
        meta = build_page(template, raw, name)
        if meta.get("sitemap", True) and not meta["path"].endswith(".html"):
            sitemap_rows.append((
                BASE_URL + "/" + meta["path"],
                meta.get("priority", 0.7),
                meta.get("changefreq", "monthly"),
            ))

    sitemap_rows.sort(key=lambda r: (-r[1], r[0]))
    urls = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{pri:.1f}</priority>\n  </url>"
        for loc, pri, freq in sitemap_rows
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    n_redirects = build_redirects()
    print(f"Built {len(sources)} pages + {len(STUB_PATHS)} redirect stubs "
          f"+ sitemap.xml ({len(sitemap_rows)} URLs) "
          f"+ {n_redirects} redirects")


if __name__ == "__main__":
    main()
