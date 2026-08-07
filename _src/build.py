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
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
PAGES = SRC / "pages"
BASE_URL = "https://jupiterlaser.com"

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
}

REDIRECT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Moved: Jupiter Laser &amp; Regenerative Medicine</title>
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

    schema_html = "".join(
        '  <script type="application/ld+json">\n  %s\n  </script>\n'
        % json.dumps(s, indent=2, ensure_ascii=False).replace("\n", "\n  ")
        for s in schemas
    )

    path = meta["path"]
    canon = BASE_URL + "/" + path
    if path.endswith(".html"):  # e.g. 404.html
        out_file = ROOT / path
    else:
        out_file = ROOT / path / "index.html" if path else ROOT / "index.html"

    html = (
        template
        .replace("{{TITLE}}", meta["title"])
        .replace("{{DESC}}", meta["desc"])
        .replace("{{CANON}}", canon)
        .replace("{{ROBOTS}}", meta.get("robots", "index, follow"))
        .replace("{{OG_TYPE}}", meta.get("ogtype", "website"))
        .replace("{{NAV}}", meta.get("nav", ""))
        .replace("{{BODY_CLASS}}", f' class="{meta["bodyclass"]}"' if meta.get("bodyclass") else "")
        .replace("{{SCHEMA}}", schema_html)
        .replace("{{CONTENT}}", content)
    )

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    return meta


def main():
    template = (SRC / "template.html").read_text(encoding="utf-8")
    pages = sorted(PAGES.glob("*.html"))
    if not pages:
        sys.exit("ERROR: no pages found in _src/pages/")

    sitemap_rows = []
    today = date.today().isoformat()
    for p in pages:
        meta = build_page(template, p.read_text(encoding="utf-8"), p.name)
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
    print(f"Built {len(pages)} pages + {len(REDIRECTS)} redirect stubs "
          f"+ sitemap.xml ({len(sitemap_rows)} URLs)")


if __name__ == "__main__":
    main()
