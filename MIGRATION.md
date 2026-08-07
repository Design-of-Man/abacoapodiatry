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

### 1. URLs that already rank were kept or 301-mapped

**Kept identical (no redirect needed — zero risk):**

| Legacy URL | Status |
|---|---|
| `/meet-dr-cedeno/` | same URL on new site |
| `/telehealth/` | same URL on new site |
| `/how-mls-laser-therapy-relieves-foot-and-ankle-pain/` | same URL on new site |
| `/innovative-treatments-for-heel-pain-exploring-mls-laser-therapy/` | same URL on new site |

**301-redirected (both `_redirects` for Netlify and `.htaccess` for Apache are pre-built,
plus meta-refresh fallback stubs for any other host):**

| Legacy URL | New URL |
|---|---|
| `/mls/` | `/services/mls-laser-therapy/` |
| `/about-us/` | `/about/` |
| `/regenerative-medicine/` | `/services/regenerative-medicine/` |
| `/neuropathy-solutions/` | `/conditions/neuropathy/` |
| `/plantar-fasciitis/` | `/conditions/plantar-fasciitis/` |
| `/stem-cell-therapy/` | `/services/stem-cell-therapy/` |

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
4. **Point DNS** at the new host. TLS certificate auto-provisions on Netlify/Vercel.
5. **Same day:** in Search Console, submit `https://jupiterlaser.com/sitemap.xml`; in
   Bing Webmaster Tools (free, imports from GSC in two clicks), do the same.
6. **Test the 301s** — hit each legacy URL and confirm it lands on the right new page.
7. **Google Business Profile:** confirm the website link still points to
   jupiterlaser.com, and use "Website" appointment link → `/contact/`.
8. **Google Ads:** update any ad final URLs pointing at old deep pages to the new URLs
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
