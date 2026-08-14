# Where this stands — 14 Aug 2026

Handoff note. `CLAUDE.md` covers how the repo works; this covers what has happened and
what is still open, so a new session does not have to reconstruct it.

## The tooling that now exists

Four things were built this session. A new session should know they are there before
reinventing any of them.

| | |
|---|---|
| `_dev/preflight.py` | Hard-failing launch gate. Placeholders, missing assets, empty or duplicate meta, invalid JSON-LD, broken internal links, missing `alt`, `<h1>` count, redirect destinations. **Exits non-zero.** Currently fails on 4 real items, which is correct. |
| `_dev/formtest/run-formtest.sh` | Drives headless Chrome through the contact form against a fake FormSubmit returning delivered / accepted-then-dropped / 500. Asserts what the patient sees and whether a lead event fires. Run after any change to that handler. |
| `_dev/measure/measure.sh` | Lighthouse mobile + axe across five representative pages. `measure.sh <label>` writes to `results/<label>/`. Run the same command before and after or the delta means nothing. |
| `_dev/image-prompts*.md`, `_dev/optimise-images.py` | 42 image prompts, one per page with no image, and the resize/WebP pipeline for the results. |

Needs `pip install Pillow imageio-ffmpeg` and `cd _dev/measure && npm install --ignore-scripts lighthouse axe-core`. Both work: pypi and the npm registry are among the few hosts this environment's proxy allows.

## Measured state

| | |
|---|---|
| Lighthouse mobile | perf 80-84, **a11y 100, SEO 100**, CLS **0.000** across measured pages |
| axe | **0 violations** |
| Homepage payload | 5,582KB → 1,761KB after fixing the hero video (−68%) |
| Em dashes | 495 → 1, from 19.4 per 1,000 words to 0.04 |
| Pages with a diagram | 6, hand-built inline SVG |
| Pages still with no image | 42, prompts written and waiting on generation |

## Blocked on someone else

Nothing here is code. All of it gates launch.

1. **Search Console** — get the vendor to grant Owner *before* terminating them. GSC does not backfill, so the decline since April only exists in their property. Separately, verify a Domain property by DNS TXT today; it cannot be revoked and the clock starts when it is verified.
2. **The contact form delivers to nobody** until someone clicks FormSubmit's activation link on `AbacoaPodiatry@gmail.com`. Note to forward: `_dev/client-form-activation.md`. Then confirm a live submission reaches all four recipients, spam included.
3. **`/reviews/` carries 8 unverified testimonials** on a medical site. Gates cutover. Real Google reviews are the replacement, which is why the GBP work matters.
4. **Vercel Web Analytics is off**, so `track()` no-ops and no lead events are being recorded at all. `/_vercel/insights/script.js` 404s in production until it is enabled.
5. **Default branch is still `claude/jupiter-laser-redesign-55fr8l`.** Should be `main`. The stale branch has 0 commits not already in `main`, so it can be deleted after. No MCP tool can change this and the REST API is blocked here; it is a manual settings change.
6. **`jupiterlaser.com` is 403 at this environment's egress proxy.** That blocks the old-site crawl, so the redirect map is still open, and it blocked fetching an SVG the client wanted used. Allow-listing the host fixes both.
7. **Two photos** referenced but never committed: `office.jpg` on `/contact/`, `mls-laser.jpg` on `/technology/`. Preflight blocks on them. Both pages degrade gracefully via `onerror`, so nothing looks broken meanwhile.
8. **The invoice** separating media spend from management fee. Google Ads shows ~$15.5k paid to Google across the period; what the vendor charged on top only exists on their invoice.

## Decisions worth not relitigating

- **No AI-generated people, and nothing depicting the practice.** Office, treatment rooms, equipment, staff and patients are camera work, listed in `_dev/photo-shotlist.md`. A generated photo of "our treatment room" is a false claim on a medical site.
- **Anatomy stays on the SVG diagrams**, not AI raster. These models garble structure and any baked-in text, and the diagrams are accurate, weightless, screen-reader readable and CLS-free.
- **The condition dropdown on the contact form stays**, carrying condition detail through a non-BAA service with an on-form disclaimer as the mitigation. Reviewed deliberately.
- **Speculation Rules are `conservative`, not `moderate`.** A prerender fires the page's load scripts, and Web Analytics records a pageview on load; hover-triggered prerendering would inflate the numbers this site is judged on.
- **The hero poster is frame zero of the hero video.** It cannot simply be deleted: it is the LCP element and the entire hero for reduced-motion, Save-Data, 2g and non-H.264 visitors.

## Immediate next step

Generate the 42 images. `_dev/image-prompts-paste.md` has them as self-contained blocks.
Copilot works but is one-per-turn and entirely manual. A connected image MCP (ViewMax is
$14/mo yearly, 1 credit per image) would let a session generate, check, optimise and wire
them in without a human in the loop — worth weighing against the other client sites in the
same pipeline, not just this one.

Conditions and services first. Those are the pages patients reach from a search; the
fifteen location pages are local-SEO surface.
