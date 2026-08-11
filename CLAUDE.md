# Working in this repo

Static marketing site for **Abacoa Podiatry & Leg Vein Center**, currently targeting the
`jupiterlaser.com` domain. No framework, no dependencies at runtime. `README.md` covers
what the site contains and how to author pages; this file covers the things that are easy
to get wrong.

## The build output is committed

`_src/build.py` runs **on your machine**, not on the host. It wraps each `_src/pages/*.html`
in `_src/template.html` and writes finished pages to the repo root, then regenerates
`sitemap.xml`.

Vercel has **no build command** — it serves the committed repo root as static files. So:

```
edit _src/pages/foo.html  →  python3 _src/build.py  →  commit BOTH the source and the
                                                        regenerated root pages
```

Committing only the `_src/` change ships nothing. The old generated page stays live and the
diff looks fine, which is why this is worth stating twice.

Only pages and `sitemap.xml` are generated. CSS, JS, images and video under `assets/` are
static and edited in place.

One wrinkle: the build stamps **today's date** into every `<lastmod>` in `sitemap.xml`,
whether or not the page changed. So a rebuild always dirties the sitemap. If your change
didn't touch page content, `git checkout sitemap.xml` before committing — otherwise you are
telling search engines all 53 URLs changed when none did.

## Meta values are escaped at build time

`build.py` runs `title`, `desc` and the canonical through `esc()` before substituting them.
This is load-bearing, not decoration: those values land in `<title>` (RCDATA, where a bare
`&` starts an entity) and in `content="..."` attributes (where a literal `"` closes the
attribute and silently truncates the value to nothing). A description in
`_src/pages/cond-sprains.html` opens with a quoted phrase and shipped an **empty** meta
description for exactly that reason. Write `title`/`desc` in the META block as plain text —
real `&`, real quotes — and let the build escape them. Don't pre-escape by hand, or you get
`&amp;amp;`.

JSON-LD is emitted with `<` escaped as `<` so a schema value containing a closing
script tag can't break out of the block.

## Two schema fields the build adds for you

Don't hand-author these in a page's META block; `build.py` fills them in.

- **A `WebPage` entity**, on any page whose META declares no page-level schema of its
  own (`*Page`, `Article`, `BlogPosting`). Built from `title`, `desc` and the canonical,
  linked to the sitewide `#website` and `#clinic` nodes. Declare your own `MedicalWebPage`
  and the build leaves it alone.
- **`dateModified`**, from the last git commit that touched the page's source — or today
  if that source has uncommitted edits. Deliberately *not* the build date: answer engines
  weight recency, so stamping today onto all 54 pages every rebuild would assert a
  freshness that isn't real. Outside a git checkout the field is omitted rather than
  guessed. If you ever see all 54 pages sharing one date, that's the bug.

## Deploy pipeline

| | |
|---|---|
| Remote | `Design-of-Man/abacoapodiatry` |
| Vercel project | `abacoapodiatry`, team `thedesignofman` |
| Production branch | **`main`** — pinned by name |
| Any other branch | preview deployment, production alias untouched |
| Config | `vercel.json` — 301s, security headers, cache policy |

Verified working end to end on 2026-08-10: push → webhook → build, ~10s to READY.

**The repo's default branch is `claude/jupiter-laser-redesign-55fr8l`, not `main`.** This
does not affect production (Vercel targets `main` by name), but it means a new PR defaults
to the wrong base and a fresh clone checks out the wrong branch. **Always set a PR's base to
`main` explicitly** until someone fixes the repo setting.

`_redirects` (Netlify) and `.htaccess` (Apache) are maintained for portability but are inert
on Vercel. If you add a redirect, add it to `vercel.json` or it will not take effect.

`vercel.json` also sends `X-Robots-Tag: noindex, nofollow` on any `*.vercel.app` host. That
is deliberate — see the next section. Don't widen that rule to `/(.*)` unconditionally, and
don't delete it before the domain is attached.

## Domains are not cut over yet

`jupiterlaser.com` and `abacoapodiatry.com` are **not attached to the Vercel project** — it
serves only `*.vercel.app` hostnames. `jupiterlaser.com` still serves the client's old site.
Read `MIGRATION.md` before doing anything that touches DNS or URLs.

Because of that split the live `*.vercel.app` host serves pages canonicalised to a domain
that returns different content. Search engines ignore a canonical whose target doesn't
match and index the staging copy instead, so the host is blocked with `X-Robots-Tag` in
`vercel.json`. The rule keys on hostname, so attaching the real domain lifts it with no
cleanup step. `MIGRATION.md` step 5 has the two curls that verify it landed the right way
round.

Two build-time origins encode this split:

- `SITE_ORIGIN` (default `https://jupiterlaser.com`) drives canonicals, schema `@id`s and the
  sitemap — the real future domain, so launch SEO is correct now.
- `IMAGE_ORIGIN` (default `https://abacoapodiatry.vercel.app`) drives only OpenGraph/Twitter
  images, which must resolve on the host actually serving the page. Pointing these at the
  canonical domain before cutover makes link previews fall back to the transparent logo.

At cutover, rebuild with `IMAGE_ORIGIN=https://jupiterlaser.com`.

## Known dead code

`_src/vercel-build.sh` and its `HERO_VIDEO_URL` variable are leftovers from when the hero
video was fetched from Dropbox at deploy time. Nothing runs the script (no build command)
and nothing reads the variable. The video encodes are committed under `assets/video/`
(desktop + mobile, MP4 + WebM). Safe to delete; left in place only because removing it
wasn't in scope for the change that found it.

## Conventions

- Match the surrounding code. The CSS is one design system in `assets/css/main.css`; the JS
  is vanilla with no dependencies in `assets/js/main.js`. Don't introduce a framework or a
  package manager to solve a small problem.
- Placeholder content is marked `LAUNCH TODO`. Don't treat those strings as real copy, and
  don't quietly ship them as final.
- The pre-launch checklist in `README.md` is live. If you complete an item, tick it there.
