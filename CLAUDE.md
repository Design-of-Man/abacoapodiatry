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

Pages, `sitemap.xml`, and every redirect surface are generated. CSS, JS, images and video
under `assets/` are static and edited in place.

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

**Redirects come from `_src/redirect-map.tsv` and nowhere else.** Add a line there and
rebuild. `build.py` writes all four surfaces from it: the `redirects` array in `vercel.json`
(the only one that runs on Vercel), `_redirects` (Netlify), `.htaccess` (Apache), and
meta-refresh stubs for the handful of short paths listed in `STUB_PATHS`.

Do not hand-edit those four. `build.py` overwrites them, which is exactly how the map got
out of sync before: `_redirects` and `.htaccess` were regenerated from a 19-entry dict in
`build.py` on every build, so anything written into them by hand vanished at the next
build, silently, in the two files nobody opens.

The build refuses to write a map that redirects to a missing page, chains one redirect into
another, points at `/` in bulk, duplicates a source, or drops a trailing slash. The `/`
rule is not style: Google reads a mass redirect to the homepage as a soft 404 and discards
the link equity, so a "safe" catch-all to `/` is worse than the 404 it replaces. Send it to
the section hub.

**Sources carry a trailing slash, and that is load-bearing.** `vercel.json` sets
`trailingSlash: true`, so Vercel 308s `/foo` to `/foo/` *before* it matches the redirect
table — a slash-less source is never reached. Every source was slash-less until
2026-08-14, which made the whole array inert while reading perfectly in the file:
`/veins/` and `/venous-insufficiency/` returned a hard 404 in production. `build.py` emits
both forms now. Don't "tidy" the slash away.

Two checks, and they answer different questions:

```
python3 _dev/crawl-old-site.py --coverage      # is anything on the old site unmapped?
python3 _dev/verify-redirects.py <origin>      # does every one actually resolve, live?
```

The second is the one that matters. Reading `vercel.json` tells you nothing about what the
deployment does — that is exactly how an entirely non-functional redirect table survived,
since the only legacy URLs anyone spot-checked were the handful with a meta-refresh stub
behind them. Both need `jupiterlaser.com` reachable. Run both before cutover.

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

## The contact form is the only lead path, and it can fail silently

`_src/pages/contact.html` posts to FormSubmit. The floating "Jupiter Laser Assistant" is
*not* a second path — `assets/js/assistant.js` is keyword-matched canned answers, entirely
client-side, and routes people to the phone or `/contact/`.

Two things about FormSubmit are worth knowing before you touch that form.

**It does not deliver to an address until someone clicks a confirmation link**, sent on the
first submission to that address. Until then submissions are accepted and dropped.
`_dev/client-form-activation.md` is the note to send the practice.

**A 2xx does not mean delivered.** FormSubmit answers `200` with `{"success":"false"}` in
exactly that unactivated case, so the handler in `assets/js/main.js` reads the JSON body
and requires `success` to be `"true"` — note the *string*, not a boolean. Checking `r.ok`
alone would thank the patient, fire a lead event, and drop the request, all at once. It
did, until 2026-08-14. Anything unexpected deliberately falls to the error path and shows
the phone number: a wasted call costs less than a lead that evaporates.

`_dev/formtest/run-formtest.sh` drives headless Chrome against a fake FormSubmit that
returns all three replies (delivered / accepted-then-dropped / 500) and asserts what the
patient sees and whether a lead event fires. Run it after any change to that handler.
It needs no network — everything is local.

**On the condition dropdown:** "What can we help with?" collects condition detail
alongside name and phone and sends it through a service with no BAA. Reviewed and kept
deliberately on 2026-08-14 — the field earns its place in triage, and the on-form
disclaimer asking patients not to add medical detail is the mitigation. If that trade
ever gets revisited, the options are neutral labels or dropping the field.

Lead events go to **Vercel Web Analytics** (`window.va`), not Google Analytics. `track()`
no-ops when the script isn't present, which is always the case on localhost — so a local
form test will never show an event unless you stub `window.va` the way the test harness
does.

## Conventions

- Match the surrounding code. The CSS is one design system in `assets/css/main.css`; the JS
  is vanilla with no dependencies in `assets/js/main.js`. Don't introduce a framework or a
  package manager to solve a small problem.
- Placeholder content is marked `LAUNCH TODO`. Don't treat those strings as real copy, and
  don't quietly ship them as final.
- The pre-launch checklist in `README.md` is live. If you complete an item, tick it there.
