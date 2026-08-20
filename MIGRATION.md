# Zero-Lost-Leads Migration Plan

The owner's worry — "if we replace the site, my leads disappear" — is legitimate: botched
migrations lose rankings when old URLs die, tracking breaks, or Google Business Profile
links go stale. This plan removes each of those risks. Follow it in order.

**Context worth knowing:** the domain property in Search Console (`sc-domain:jupiterlaser.com`,
verified 2026-08-17) shows the opposite of a decline — clicks and impressions both roughly
2.5x'd over the last two 90-day windows. The "steady decline since April" this section used
to claim came from the previous vendor's reporting and does not hold up against the real
account; don't repeat it. The migration is still the right call, just not for that reason —
see the redirect coverage and the content-parity work in `_dev/STATUS.md` instead.

Google Ads spend is **$3k–3.9k/mo** per the owner's actual billing (confirmed 2026-08-18),
not the ~$5,500/mo this section used to state. Every organic ranking this site wins still
directly reduces paid spend — that logic holds regardless of the exact figure.

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

**Verified on a live deployment, not just in the config.** `python3 _dev/verify-redirects.py
<origin>` requests all 156 old URLs against a real build and follows each to the end:

```
  156/156 resolve to 200
  OK -- every URL the old site publishes lands on a real page
```

That distinction earned its keep. `vercel.json` sets `trailingSlash: true`, so Vercel 308s
`/foo` to `/foo/` **before** matching the redirect table — and every source was written
slash-less, so the whole array was inert. `/veins/` and `/venous-insufficiency/` returned a
hard 404 in production while the config file looked perfectly correct. The only legacy URLs
that resolved did so through a meta-refresh stub, which is why hand-checking never caught
it: the paths a person thinks to try are exactly the ones with a stub behind them.
WordPress publishes every URL with a trailing slash, so the broken form was the only form
real traffic would have used.

**Before cutover, run both:**

```
python3 _dev/crawl-old-site.py --coverage        # anything new on the old site?
python3 _dev/verify-redirects.py <origin>        # does every one actually resolve?
```

The old site is still live and still being edited; a post published after 2026-08-14 will
not be in the map.

### 2. The phone number is the lead pipeline — it's everywhere and unchanged
(561) 624-4800 appears in the header, footer, every CTA, the mobile sticky call bar, and
all structured data. **Do not add a call-tracking number that differs from the Google
Business Profile number** without using a proper NAP-safe setup — number consistency is a
local-ranking factor.

### 3. NAP consistency
Name / Address / Phone are identical on every page and in schema:
`Jupiter Laser & Regenerative Medicine · 4601 Military Trail, Suite 202, Jupiter, FL 33458 · (561) 624-4800`.
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
3a. ~~**Rebuild with the production image origin.**~~ Done 2026-08-18. Social preview
   images (`og:image`, `twitter:image`, schema `image`/`logo`/`thumbnailUrl`) used to
   point at the deployment host, because before cutover `jupiterlaser.com` still served
   the old site — an `og:image` there 404s and scrapers fall back to whatever in-page
   image they find, which is the transparent logo (iMessage paints it on grey).
   `IMAGE_ORIGIN` now defaults to `SITE_ORIGIN`, so a plain build produces the real
   domain and this cannot silently revert.

   **Merge that rebuild only once DNS resolves**, not before — until then those image
   URLs point at a domain still serving the old site.

   After DNS lands, re-scrape the card so caches update: Facebook Sharing Debugger,
   LinkedIn Post Inspector, and for iMessage send the link to yourself from a different
   thread (Apple caches per-URL).
3b. **Set the apex as production in Vercel, and redirect `www` to it.** Adding both
   domains makes Vercel offer `www` as primary with the apex 308ing to it, which is
   backwards here: canonicals, all 101 sitemap URLs, `robots.txt` and schema `@id`s all
   use the apex, and the old site 301'd `www` to the apex too. Left the default way,
   every URL Google has indexed redirects to a host whose canonical points back at the
   URL it came from.
4. **Point DNS** at the new host. TLS certificate auto-provisions on Netlify/Vercel.
   **Change only the A record and the `www` record — do not move the nameservers.** DNS
   is at GoDaddy (`ns59/ns60.domaincontrol.com`) and email is Microsoft 365
   (`MX → jupiterlaser-com.mail.protection.outlook.com`); repointing nameservers at
   Vercel drops the MX records and takes the practice's email down with them.

   | Type | Name | Value |
   |---|---|---|
   | A | `@` | `76.76.21.21` |
   | CNAME | `www` | `cname.vercel-dns.com` |
4a. **Re-activate FormSubmit on the new domain.** The contact form posts to FormSubmit
   (`_src/pages/contact.html`, see that file's comment for why and the full history).
   FormSubmit ties its one-time activation to the exact domain a submission comes from —
   the Vercel preview URL and `jupiterlaser.com` are different domains as far as it's
   concerned, so the preview being activated does **not** carry over. The first real
   submission from `jupiterlaser.com` will silently fail exactly like the original bug
   this file exists to prevent, until someone clicks the new activation email. **Submit one
   test entry through the live `jupiterlaser.com/contact/` form immediately after DNS
   lands, before announcing the site is live**, and click the activation link that
   arrives at the current recipient. Do not skip this — it is the same failure mode,
   reintroduced by the domain change itself.
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
