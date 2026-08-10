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

## Domains are not cut over yet

`jupiterlaser.com` and `abacoapodiatry.com` are **not attached to the Vercel project** — it
serves only `*.vercel.app` hostnames. `jupiterlaser.com` still serves the client's old site.
Read `MIGRATION.md` before doing anything that touches DNS or URLs.

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
