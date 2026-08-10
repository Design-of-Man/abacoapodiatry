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
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path


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

# Social preview images must resolve on the host actually SERVING the page, not
# on the canonical domain. Until the cutover, jupiterlaser.com still points at
# the old site, so an og:image there 404s and scrapers fall back to whatever
# in-page image they can find -- which is the transparent logo, and iMessage
# paints transparency on grey. Canonical stays on the real domain so launch SEO
# is right; only the image URLs follow the deployment.
# At cutover: rebuild with IMAGE_ORIGIN=https://jupiterlaser.com (see MIGRATION.md).
IMAGE_ORIGIN = os.environ.get(
    "IMAGE_ORIGIN", "https://abacoapodiatry.vercel.app"
).rstrip("/")

sys.path.insert(0, str(SRC))
from locations import location_pages  # noqa: E402

META_RE = re.compile(r"^<!--META\s*(\{.*?\})\s*META-->\s*", re.DOTALL)

# Legacy jupiterlaser.com URLs -> new locations. Old URLs that we preserved
# exactly (/meet-dr-cedeno/, /telehealth/, and both legacy blog-post slugs)
# don't appear here because they never moved.
REDIRECTS = {
    "mls/": "/services/mls-laser-therapy/",
    "about-us/": "/about/",
    "regenerative-medicine/": "/services/regenerative-medicine/",
    "neuropathy-solutions/": "/conditions/neuropathy/",
    "plantar-fasciitis/": "/conditions/plantar-fasciitis/",
    "stem-cell-therapy/": "/services/stem-cell-therapy/",
    "testimonials/": "/reviews/",
    "what-we-do/": "/services/",
    # superseded by /locations/
    "service-areas/": "/locations/",
    "bbl/": "/services/foot-bbl/",
    "bunion/": "/conditions/bunions/",
    "flat-feet/": "/conditions/flat-feet/",
    "wound-care/": "/services/wound-care/",
    "foot-ankle-surgery/": "/services/foot-ankle-surgery/",
    "providers/": "/about/",
    "request-an-appointment/": "/contact/",
    "videos/": "/media/",
    "flat-feet-flatfoot-types-causes-treatment/": "/conditions/flat-feet/",
    "physical-therapy-and-rehabilitation-after-flat-foot-surgery/": "/conditions/flat-feet/",
}

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
    """Fallback meta-refresh stubs for plain static hosts, plus host-level
    301 config for Netlify (_redirects) and Apache (.htaccess)."""
    for old, new in REDIRECTS.items():
        out = ROOT / old / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(REDIRECT_HTML.format(target=new, base=BASE_URL), encoding="utf-8")

    netlify = "".join(f"/{old.rstrip('/')} {new} 301!\n/{old} {new} 301!\n"
                      for old, new in REDIRECTS.items())
    (ROOT / "_redirects").write_text(netlify, encoding="utf-8")

    htaccess = ["# 301 redirects from legacy jupiterlaser.com URLs",
                "RewriteEngine On"]
    for old, new in REDIRECTS.items():
        htaccess.append(f"RewriteRule ^{old.rstrip('/')}/?$ {new} [R=301,L]")
    htaccess += [
        "",
        "# Serve custom 404",
        "ErrorDocument 404 /404.html",
    ]
    (ROOT / ".htaccess").write_text("\n".join(htaccess) + "\n", encoding="utf-8")


def build_page(template: str, raw: str, name: str):
    m = META_RE.match(raw)
    if not m:
        sys.exit(f"ERROR: {name} is missing its <!--META ... META--> block")
    try:
        meta = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: bad JSON meta in {name}: {e}")
    content = raw[m.end():]

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

    def ld_json(obj):
        # Escape `<` so a value containing `</script>` cannot terminate the block
        # and spill schema into the document. < is valid JSON and parses back
        # to `<`, so Google and every other consumer still read the original text.
        body = json.dumps(obj, indent=2, ensure_ascii=False).replace("<", "\\u003c")
        return ('  <script type="application/ld+json">\n  %s\n  </script>\n'
                % body.replace("\n", "\n  "))

    schema_html = "".join(ld_json(s) for s in schemas)

    path = meta["path"]
    canon = BASE_URL + "/" + path
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
        .replace("{{BODY_CLASS}}", f' class="{meta["bodyclass"]}"' if meta.get("bodyclass") else "")
        .replace("{{SCHEMA}}", schema_html)
        .replace("{{CONTENT}}", content)
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
    build_redirects()
    print(f"Built {len(sources)} pages + {len(REDIRECTS)} redirect stubs "
          f"+ sitemap.xml ({len(sitemap_rows)} URLs)")


if __name__ == "__main__":
    main()
