# Zero-Lost-Leads Migration Plan

The owner's worry — "if we replace the site, my leads disappear" — is legitimate: botched
migrations lose rankings when old URLs die, tracking breaks, or Google Business Profile
links go stale. This plan removes each of those risks. Follow it in order.

**Context worth knowing:** Search Console already shows a steady decline since April.
That means the *current* site is bleeding visibility — the risk of a careful migration is
lower than the risk of standing still. And at ~$5,500/mo in Google Ads, every organic
ranking this site wins is directly reducing paid spend.

---

## Why this redesign is migration-safe by construction

### 1. Every URL the old site publishes is kept or 301-mapped

Checked against a crawl rather than asserted. `_dev/crawl-old-site.py` pulls all four Yoast
sitemaps from `jupiterlaser.com`; `--coverage` reports anything with no redirect and no
matching page.

| | |
|---|---|
| Live URLs on the old site | **157** |
| Kept identical, no redirect needed | 8 |
| 301-redirected | 149 |
| **Uncovered** | **0** |

**This was 132 uncovered until 2026-08-14.** The original map was 27 redirects written from
search research rather than a crawl, and it covered 17 of the 157. The other 132 — 101
pages and posts, 30 category archives, 1 author archive — resolved on the old site and
would have returned 404 the moment DNS moved. That is the difference between a migration
and starting from zero, and it was invisible while `jupiterlaser.com` was blocked at the
egress proxy.

**Kept identical (zero risk):** `/`, `/blog/`, `/contact/`, `/services/`, `/telehealth/`,
`/meet-dr-cedeno/`, `/how-mls-laser-therapy-relieves-foot-and-ankle-pain/`,
`/innovative-treatments-for-heel-pain-exploring-mls-laser-therapy/`.

**The other 149** are in `_src/redirect-map.tsv`, one line each with the reason for the
target. `build.py` generates `vercel.json` (the only one Vercel reads), `_redirects`,
`.htaccess` and the meta-refresh stubs from it, so the four cannot disagree.

Every target is the closest real equivalent; **nothing redirects to `/`**, and the build
refuses a map that does. A bulk redirect to the homepage is read as a soft 404 and the link
equity is discarded, which would waste the whole exercise.

**Re-run `python3 _dev/crawl-old-site.py --coverage` immediately before cutover.** The old
site is still live and still being edited; a post published after 2026-08-14 will not be in
the map.

### 2. The phone number is the lead pipeline — it's everywhere and unchanged
(561) 915-1934 appears in the header, footer, every CTA, the mobile sticky call bar, and
all structured data. **Do not add a call-tracking number that differs from the Google
Business Profile number** without using a proper NAP-safe setup — number consistency is a
local-ranking factor.

### 3. NAP consistency
Name / Address / Phone are identical on every page and in schema:
`Jupiter Laser & Regenerative Medicine · 4601 Military Trail, Suite 202, Jupiter, FL 33458 · (561) 915-1934`.
This must match the Google Business Profile exactly.

---

## Cutover steps (one afternoon)

1. **Crawl the old site first.** Before DNS changes, run a crawler (Screaming Frog free
   tier, or `wget --spider -r`) against the live jupiterlaser.com and export every URL
   that returns 200. Compare against the table above; add a 301 for anything indexed
   that isn't already covered (edit `REDIRECTS` in `_src/build.py`, rebuild). The list
   above came from search-engine research; the crawl is the belt-and-suspenders check.
2. **Keep Search Console access.** Do NOT delete or re-create the property. The existing
   property follows the domain, not the old site. If the current SEO vendor owns the
   only verification, add owner verification now (DNS TXT record) *before* the switch.
3. **Deploy to a temporary URL** (e.g. Netlify's `*.netlify.app`) and click through it.
3a. **Rebuild with the production image origin.** Social preview images (`og:image`,
   `twitter:image`, schema `image`/`logo`/`thumbnailUrl`) point at the deployment host
   rather than the canonical domain, because before cutover `jupiterlaser.com` still
   serves the old site — an `og:image` there 404s and scrapers fall back to whatever
   in-page image they find, which is the transparent logo (iMessage paints it on grey).
   Canonical URLs already point at `jupiterlaser.com`, so only the image origin needs
   flipping:

   ```bash
   IMAGE_ORIGIN=https://jupiterlaser.com python3 _src/build.py
   ```

   Then re-scrape the card so caches update: Facebook Sharing Debugger, LinkedIn Post
   Inspector, and for iMessage just send the link to yourself from a different thread
   (Apple caches per-URL). Leaving this step undone is cosmetic, not an SEO problem —
   the images still resolve, just from the Vercel host.
4. **Point DNS** at the new host. TLS certificate auto-provisions on Netlify/Vercel.
5. **Confirm the staging block lifted.** Until cutover the site is reachable at
   `abacoapodiatry.vercel.app`, which is public (no deployment protection) and serves
   pages whose canonical points at `jupiterlaser.com` — a domain that still returns the
   *old* site. A canonical whose target doesn't match gets ignored, so Google is free to
   index the `.vercel.app` copies and have them compete with the real domain later.
   `vercel.json` therefore sends `X-Robots-Tag: noindex, nofollow` on any `*.vercel.app`
   host. The rule keys on hostname, so attaching the real domain lifts it automatically —
   nothing to remember to remove. **Verify once after DNS lands:**

   ```bash
   curl -sI https://jupiterlaser.com/ | grep -i x-robots-tag   # expect: no output
   curl -sI https://abacoapodiatry.vercel.app/ | grep -i x-robots-tag   # expect: noindex
   ```

   If the first command prints a noindex, stop and fix it before submitting the sitemap —
   that would deindex the live site.
6. **Same day:** in Search Console, submit `https://jupiterlaser.com/sitemap.xml`; in
   Bing Webmaster Tools (free, imports from GSC in two clicks), do the same. Bing also
   supports **IndexNow** for near-instant recrawls — worth wiring up once the domain is
   live, since it needs a key file served from the real origin.
7. **Test the 301s** — hit each legacy URL and confirm it lands on the right new page.
8. **Google Business Profile:** confirm the website link still points to
   jupiterlaser.com, and use "Website" appointment link → `/contact/`.
9. **Google Ads:** update any ad final URLs pointing at old deep pages to the new URLs
   (or rely on the 301s, but direct links preserve Quality Score better). The new
   condition pages (`/conditions/plantar-fasciitis/` etc.) make far better ad landing
   pages than a homepage — expect Quality Score and cost-per-lead to improve.

## The first 30 days

- Watch GSC "Pages" report for 404s; add redirects for any stragglers and rebuild.
- Expect a small ranking wobble for 1–3 weeks — normal for any migration. The decline
  since April is the baseline to beat, not pre-April.
- Ask 3–5 happy patients for Google reviews (the reviews page links directly to the
  review flow). Review velocity + this site's local schema is the fastest local-pack lever.
- Confirm the practice's categories on GBP include "Podiatrist" and add services
  (MLS laser therapy, shockwave, etc.) with links to the matching service pages.

## What this site does that the old one didn't

- **Answer-first content + FAQPage/MedicalCondition/Physician schema** on every relevant
  page — built for Google/Bing rich results and AI-generated answers (llms.txt included).
- **A page per condition and per service** — each one a landing page for a search intent
  ("plantar fasciitis treatment jupiter fl", "shockwave therapy near me", …). The old
  site had a handful of pages competing for everything.
- **Local signals**: geo meta, areaServed schema, service-area page, embedded map, NAP
  in the footer of all 33 pages.
- **Conversion pressure everywhere**: click-to-call in the sticky header, mobile call
  bar, CTA band on every page — leads have a shorter path than on the old site.
- **Speed**: no page builder, no jQuery stack — one CSS file, one deferred JS file,
  static HTML. Core Web Vitals are a ranking input; this site will score dramatically
  better than a WordPress builder site.
