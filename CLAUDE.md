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

## Opening hours

Both offices' hours live in `_src/hours.py` and nowhere else. `build.py` renders them
into `{{HOURS_JUP_LD}}`, `{{HOURS_PBG_LD}}`, `{{HOURS_JUP_LINE}}`, `{{HOURS_PBG_LINE}}`,
`{{HOURS_PBG_CLOSED}}` and `{{HOURS_FOOTER}}`. Change the schedule there and rebuild;
do not edit hours in a page or in `template.html`.

Jupiter is Mon–Thu 8–5, Fri 8–2 with a 12:30–1:30 lunch closure. Palm Beach Gardens is
**Monday and Wednesday only, 8–4:30**. They were identical in the JSON-LD until
2026-08-15 because PBG's `openingHoursSpecification` had been copied from Jupiter's,
while the visible copy on `/locations/` said "call for availability" — the schema and the
page disagreed and both were wrong.

Two consumers are outside the build and must be hand-edited: `assets/js/assistant.js`
and `llms.txt`. `_dev/preflight.py` imports `hours.plain()` and fails if either drifts.

## The contact form is the only lead path, and it can fail silently

`_src/pages/contact.html` posts to FormSubmit (`https://formsubmit.co/ajax/...`) again as
of 2026-08-18, by explicit, informed client request — see below. The assistant's own lead
capture (`assets/js/assistant.js`) still posts to `/api/contact/` (Supabase), unchanged.

**It used to be FormSubmit, and it delivered nothing — read this before touching the form
again.** FormSubmit requires a one-time activation link to be clicked in the recipient's
inbox before it forwards anything; until then it accepts every submission and drops it,
answering `200` with `{"success":"false"}`. Nobody ever clicked it, and the site looked
like it was taking bookings while taking none. Replaced with `api/contact.js` (Supabase)
on 2026-08-15 for exactly that reason.

**It's back on 2026-08-18, deliberately.** The client asked for FormSubmit specifically,
was told this history first, and confirmed anyway. Recipient is temporarily
`nicholasbkashuba@gmail.com` so he can click the activation link himself; it gets
repointed at Dr. Cedeno's and the rest of the office's addresses once that's done.
`api/contact.js` is untouched and still in the repo for a future revert. **Do not silently
switch the form back to `/api/contact/` citing this file** — that decision is the client's
to make, not a bug to fix.

**The response means "stored", and nothing weaker.** `api/contact.js` writes to Supabase
FIRST and only answers `success: "true"` if that insert succeeded; a failed write returns
`502` and an incomplete request `400`. Email is sent afterwards, best-effort, and can never
change the response — a broken inbox must not tell a patient their request vanished when
the row is already safe. The handler in `assets/js/main.js` reads the JSON body and
requires `success` to be `"true"` — note the *string*, not a boolean, kept deliberately so
the browser logic did not have to change. Anything unexpected falls to the error path and
shows the phone number: a wasted call costs less than a lead that evaporates.

**Secrets live in the Vercel environment, never here.** `SUPABASE_SERVICE_ROLE_KEY`
bypasses row-level security. `LEAD_TO` holds the office recipients, which used to be four
staff addresses sitting in the page source. `RESEND_API_KEY` is optional: without it
capture still works and the office reads the Supabase table.

`_dev/formtest/run-formtest.sh` drives headless Chrome against a fake `/api/contact` that
returns each outcome (stored / accepted-then-dropped / 400 / 502) and asserts what the
patient sees and whether a lead event fires. Run it after any change to that handler.
It needs no network — everything is local. It proves the *browser* half; the function
itself needs a real POST against a deployment.

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
