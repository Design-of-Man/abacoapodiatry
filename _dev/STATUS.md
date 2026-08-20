# Where this stands — 14 Aug 2026

Handoff note. `CLAUDE.md` covers how the repo works; this covers what has happened and
what is still open, so a new session does not have to reconstruct it.

## The tooling that now exists

These were built across this pipeline. A new session should know they are there before
reinventing any of them.

| | |
|---|---|
| `_dev/preflight.py` | Hard-failing launch gate. Placeholders, missing assets, empty or duplicate meta, invalid JSON-LD, broken internal links, missing `alt`, `<h1>` count, redirect destinations. **Exits non-zero. Currently passes — nothing blocking.** |
| `_dev/verify-testimonials.py` | Refetches the practice's testimonials page and Dr. Cedeno's Healthgrades profile and string-matches every quoted span on `/reviews/` against them. Exits non-zero on any drift. Run it after touching that page. |
| `_dev/crawl-old-site.py` | Rebuilds the old-site inventory from all four Yoast sitemaps, with titles, into `_dev/old-site-urls.tsv`. `--coverage` reports any live URL with no redirect and no matching page. Needs `jupiterlaser.com` reachable. |
| `_dev/verify-redirects.py` | Requests all 156 old URLs against a **deployed** build and follows each to the end. Exits non-zero on anything that is not a 200. Checking `vercel.json` is not the same as checking the deployment, which is how a completely inert redirect table survived. |
| `_src/redirect-map.tsv` | The redirect source of truth, 159 entries. `build.py` writes `vercel.json`, `_redirects`, `.htaccess` and the stubs from it. Not a dev tool, a build input. |
| `_dev/formtest/run-formtest.sh` | Drives headless Chrome through the contact form against a fake `/api/contact` returning stored / accepted-then-dropped / 400 / 502. Asserts what the patient sees and whether a lead event fires. Run after any change to that handler. |
| `_dev/measure/measure.sh` | Lighthouse mobile + axe across five representative pages. `measure.sh <label>` writes to `results/<label>/`. Run the same command before and after or the delta means nothing. |
| `_dev/image-prompts*.md`, `_dev/optimise-images.py` | 42 image prompts, one per page with no image, and the resize/WebP pipeline for the results. |
| `_dev/atmos-manifest.tsv`, `_dev/fetch-atmos.sh` | index -> slug -> model -> job id -> URL -> QC verdict for all 42, and the script that refetches them. Regenerate one image and update its row. |
| `_dev/client-photo-brief.md` | Client-ready note for the photography only the practice can supply. |

Needs `pip install Pillow imageio-ffmpeg` and `cd _dev/measure && npm install --ignore-scripts lighthouse axe-core`. Both work: pypi and the npm registry are among the few hosts this environment's proxy allows.

## Measured state

| | |
|---|---|
| Lighthouse mobile | perf 80-84, **a11y 100, SEO 100**, CLS **0.000** across measured pages |
| axe | **0 violations** |
| Homepage payload | 5,582KB → 1,761KB after fixing the hero video (−68%) |
| Em dashes | 495 → 1, from 19.4 per 1,000 words to 0.04 |
| Pages with a diagram | 6, hand-built inline SVG |
| Pages with no image | **0** — all 42 generated, checked and wired on 2026-08-14 |
| Atmos image payload | 2,193KB for 42 images (4% of the 54MB of raws) |
| Preflight | **passes** — 0 blocking items |
| Testimonials | **9/9 verbatim** against their two sources, checked mechanically |
| Redirect coverage | **157/157** of the old site's live URLs, from 25 before |
| Redirects verified live | **156/156** resolve to 200 on a deployed build, tested over the wire |

## Blocked on someone else

Nothing here is code. All of it gates launch.

1. **Search Console** — get the vendor to grant Owner *before* terminating them. GSC does not backfill, so the decline since April only exists in their property. Separately, verify a Domain property by DNS TXT today; it cannot be revoked and the clock starts when it is verified.
2. **The contact form needs its environment variables set on Vercel** (Production, Preview *and* Development): `SUPABASE_URL=https://iiabylugbnmcdzqjenus.supabase.co`, `SUPABASE_SERVICE_ROLE_KEY` (Supabase → Settings → API), `LEAD_TO` (the four office addresses, comma-separated), and — optionally, for email — `LEAD_FROM` plus `RESEND_API_KEY`. Adding a variable requires a redeploy to take effect. Until the Supabase pair is set the function returns 502 and the page tells patients to call, which is honest but is not a lead path. **Until `RESEND_API_KEY` exists nobody is emailed and someone must watch the `leads` table.** ~~FormSubmit activation~~ is moot: FormSubmit was removed on 2026-08-15 precisely because that activation click never happened and it had therefore delivered nothing.
3. **Vercel Web Analytics is off**, so `track()` no-ops and no lead events are being recorded at all. `/_vercel/insights/script.js` 404s in production until it is enabled.
4. **Default branch is still `claude/jupiter-laser-redesign-55fr8l`.** Should be `main`. The stale branch has 0 commits not already in `main`, so it can be deleted after. No MCP tool can change this and the REST API is blocked here; it is a manual settings change.
5. ~~**The redirect map is unverified against a crawl.**~~ Done 2026-08-14. Crawled all four Yoast sitemaps: 157 live URLs, of which **132 had no redirect and no matching page** and would have 404'd at cutover. Now 157/157, from `_src/redirect-map.tsv`. Recheck with `_dev/crawl-old-site.py --coverage` before cutover in case the old site changed.
6. **Two photos still owed**: `office.jpg` for `/contact/`, `mls-laser.jpg` for `/technology/`. The `<img>` tags were removed because they requested an asset that 404s on every page load; the PHOTO SLOT comments, monogram tiles and captions remain, so re-adding a real photo is one line. Does not block preflight or launch. See `_dev/photo-shotlist.md`.
7. **The invoice** separating media spend from management fee. Google Ads shows ~$15.5k paid to Google across the period; what the vendor charged on top only exists on their invoice.

## Decisions worth not relitigating

- **No AI-generated people, and nothing depicting the practice.** Office, treatment rooms, equipment, staff and patients are camera work, listed in `_dev/photo-shotlist.md`. A generated photo of "our treatment room" is a false claim on a medical site.
- **Anatomy stays on the SVG diagrams**, not AI raster. These models garble structure and any baked-in text, and the diagrams are accurate, weightless, screen-reader readable and CLS-free.
- **The condition dropdown on the contact form stays**, carrying condition detail through a non-BAA service with an on-form disclaimer as the mitigation. Reviewed deliberately.
- **Speculation Rules are `conservative`, not `moderate`.** A prerender fires the page's load scripts, and Web Analytics records a pageview on load; hover-triggered prerendering would inflate the numbers this site is judged on.
- **The hero poster is frame zero of the hero video.** It cannot simply be deleted: it is the LCP element and the entire hero for reduced-motion, Save-Data, 2g and non-H.264 visitors.
- **Redirect sources carry a trailing slash, and that is load-bearing.** `vercel.json` sets `trailingSlash: true`, so Vercel 308s `/foo` to `/foo/` *before* matching the redirect table. A slash-less source is never reached. Every source was slash-less until 2026-08-14, which made the entire array inert while looking perfectly correct in the file. `build.py` emits both forms now. Verify over the wire with `_dev/verify-redirects.py`, never by reading the JSON.
- **Testimonials are quoted, never tidied.** Every quote on `/reviews/` is a contiguous span copied exactly, with `…` at every trim or join. Two sources contain typos and those sentences are quoted around rather than corrected, because correcting a patient's grammar is still putting words in their mouth. `_dev/verify-testimonials.py` enforces it mechanically; a careful human proofread does not, which is how the summarised versions survived as long as they did.
- **No `aggregateRating` or `Review` schema on `/reviews/`.** The quotes are real but they are a curated selection from two sources, and marking them up as an aggregate would assert a rating this site did not compute. The stars are presentational.

## The images are done. Two lessons from doing them

**Use Higgsfield, not ViewMax.** The account already holds ~870 credits on a paid Plus
plan; ViewMax has none. Higgsfield's image roster is a superset and it has a batch API,
so all 42 submit in four calls. FLUX.2 won a bake-off against Nano Banana 2 and Seedream
4.5 at roughly 1 credit an image.

**Generating blind is the expensive failure.** The first full run of 42 shipped a foot in
a high-heeled shoe, because `heel` is ambiguous in an image prompt and because nothing in
the negative list forbade footwear. Neither was visible to the session until the CDN was
allow-listed and the files could actually be opened. Once they could, a visual pass caught
a Nike swoosh and a set of garbled brand stripes too. **Allow-list the image host before
generating anything, and look at every file before wiring it.**

Note on that swoosh: negative-prompting it away just produced a New Balance N. Changing the
camera angle so the shoe's side panel leaves the frame worked where the word "unbranded"
did not.

## Immediate next step

**Preflight passes. Nothing in the repo blocks launch.** What is left is account work and
one crawl, in the order that matters:

1. **The contact form's Vercel environment variables** (item 2 above). The code path is
   done and tested; without `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` the function
   answers 502 and the site still has no working lead path. Nothing here depends on
   anyone clicking a link in an inbox any more, which was the previous design's fatal
   flaw.
2. **Search Console**, before the vendor is terminated. GSC does not backfill.
3. **Web Analytics on**, so there is a pre-cutover baseline rather than a cliff.
4. **The redirect crawl.** `jupiterlaser.com` is reachable now, so the 27 redirects can
   finally be checked against the old site's real URL list instead of inferred.
5. **The photography.** `_dev/client-photo-brief.md` is written and ready to forward. No
   longer gates preflight, and every shot on the list also fills the thin Google Business
   Profile.
