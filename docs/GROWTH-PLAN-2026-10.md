# Abacoa Podiatry growth audit and plan, October 2026

Written 2026-10-14 for jupiterlaser.com. Evidence: `docs/GSC-DEEP-DIVE-2026-10.md` (search),
`docs/LOCAL-AUTHORITY-AUDIT-2026-10.md` (listings, GBP, reviews),
`docs/seo-kit/competitor-teardown-2026-10.md` (competitors). Paste-ready browser work:
`docs/COWORK-LOCAL-FIXES.md`. Index of everything: `docs/seo-kit/README.md`.

## 1. Bottom line: the levers, ranked

1. **Fix the dead phone off-site.** (561) 624-4800 is on all four NPPES records tied to the
   practice, Healthgrades and the directories that copy them. NPPES feeds insurer
   directories and AI answers; a patient who calls that number reaches nothing. Owner and
   Cowork work, no code. Biggest leak per hour of effort.
2. **Make the Palm Beach Gardens listing a real competitor.** Zero Google reviews against 193
   in Jupiter; 1 call in 28 days against 60. The QR-card and after-visit-text plan (audit
   section 5) targets 25 reviews in 90 days; the listing also needs its own website link,
   description and a secondary category.
3. **Local pages that already rank, made deeper (shipped).** Homepage, Palm Beach Gardens office,
   vein, heel pain, bunions, neuropathy, diabetic foot, wound care and MLS pages now answer
   "where, who, what does insurance cover" in their own words, with both offices, both doctors
   and verified credentials.
4. **Trustworthy schema (shipped).** Sitewide AggregateRating removed; FAQ markup rebuilt from
   what each page shows (69 of the 72 pages carrying it listed questions the page does not show); physician NPIs added; glossary
   DefinedTermSet. Not a ranking lever by itself (teardown), but it removes a penalty risk.
5. **Coverage content that brings local patients (shipped).** The Medicare and podiatry guide on
   `/insurance/` and the patient glossary. Medicare beneficiaries are the core of a Jupiter
   podiatry practice; a dated, sourced guide is something an assistant can cite.

Not on the list, on purpose: more national blog posts (95% of impressions are already
national informational and earn almost no patients) and more city pages (13 exist; they
earn almost nothing, city intent is a GBP lever).

## 2. What the data says

- **Search Console, 28 days to 2026-10-11:** 837 clicks (previous 28 days 566, +48%),
  125,493 impressions (66,271, +89%), CTR 0.67% (0.85%), average position 10.1 (20.5).
  The impressions jump is mostly the homepage ranking for Jupiter real estate, astronomy and
  town-hall searches (8,076 impressions, 1 click); clicks rose for real, led by the cortisone
  article and brand searches.
- **Local is about 5% of clicks.** Local medical queries are 9.5% of impressions and 5.7% of
  clicks; national informational is 73% and 59%. The August finding stands.
- **Striking distance:** 653 non-brand queries at positions 4 to 20 with 10+ impressions; 69
  are local medical. Several "jupiter + vein/stem cell term" rows look like a rank tracker,
  not patients (zero clicks ever, flat positions).
- **GBP, same 28 days:** Jupiter 1,014 impressions, 60 calls, 64 website clicks, 88
  direction requests; Palm Beach Gardens 141 impressions, 1 call, 5 website clicks, 29
  directions. Jupiter: 193 reviews, 4.9, 34 in the last 12 months, newest 2026-10-13, 12
  of those 34 answered. Palm Beach Gardens: 0 reviews.
- **GA4 (property 391066165), same window:** 2,922 sessions; Direct 1,248, Organic 1,185,
  Paid Search 343, Referral 99, Organic Social 36. Events: call_click 79, appointment_cta 65,
  form_start 27, form_submit 20 (confirmed deliveries). Key-event counts in GA4 are lower
  than event counts (call_click 17, appointment_cta 14, form_submit 7), which suggests the
  key-event flags were set partway through the window; check the settings.
- **Old URLs:** three paths landed GA4 visitors on a 404 (29 sessions in 28 days) and 42
  garbled URLs earned impressions while 404ing; the ones that matter now 301.
- **Domains:** `www` 308s to the apex (good). `abacoapodiatry.com` belongs to a domain
  broker. `jupiterveincenter.com` 302s through three hops.
- **The August content failures are fixed.** `/conditions/diabetic-foot-care/` is about
  diabetic feet (no knee or ligament content anywhere in the diabetic pages) and returns
  200; `/diabetic-foot-care/` 308s to it. `/how-to-take-care-of-surgical-wounds-at-home-to-prevent-infection/`
  returns 200 with a 482-word article and `/services/wound-care/` is populated. Both were
  checked live on 2026-10-14.

## 3. Shipped in this PR

| Change | Why |
|---|---|
| Removed the sitewide `AggregateRating` (193/4.9 snapshot) from JSON-LD; review count now shown as dated, linked text on the homepage; preflight fails on AggregateRating, Review or reviewedBy | Self-serving review markup, banned by the agency rule and ineligible under Google's rules |
| FAQPage JSON-LD built from each page's visible `<details class="faq">`; dropped where a page shows no FAQ | 69 of the 72 pages with FAQ markup carried questions the page does not show; 111 of 111 pages now pass the schema/visible check |
| Medicare and podiatry guide on `/insurance/` (#medicare) with 2026 figures and five CMS/Medicare.gov sources; three new visible FAQs | Coverage questions on the page that already gets insurance queries |
| `/glossary/`: 43 podiatry and vein terms, DefinedTermSet from the same list (`_src/glossary.py`) | Patient education, AI-citable definitions, internal links into every service |
| Local depth on 10 pages (section 6 of the deep dive) | Striking-distance local queries |
| Verbatim patient reviews on vein, wound care, MLS, surgery and bunion pages | Proof on the money pages; quotes are identical to the verified `/reviews/` set |
| `_dev/verify-testimonials.py` no longer "verifies" against our own page | `/testimonials/` has redirected to `/reviews/` since the cutover, so the check compared the page with itself; the six practice quotes are now frozen as verified on 2026-08-14 and Healthgrades is still checked live |
| Physician NPIs as `identifier` and NPPES `sameAs`, shown visibly on each physician page | Verified identity, matched to the page |
| 9 new 301s | GA4 404 landings and 404 URLs earning impressions |
| Footer "Jupiter Vein Center" now links `/services/vein-treatment/`; footer adds Insurance & Medicare and Glossary | The old link looped through a 302 on another domain; insurance was not linked from any money page |
| Mobile call bar steps aside while a form's submit button is on screen; call-bar click placement fixed (`.callbar`) | At 393px "Call Now" covered "Request Appointment"; "Book Online" taps were recorded as "body" |
| 321 em dashes removed from page sources and JS strings; preflight now fails on any | House rule; STATUS.md's "1 em dash" counted literal characters only, not `&mdash;` |
| CLAUDE.md and `_dev/listings-nap.md` hours corrected to `hours.py`; stale "domains not cut over" section replaced | Both described a schedule the office does not keep |
| `_dev/measure/measure.sh` accepts `MEASURE_PAGES` | Measure the pages a change touched |

## 4. Owner actions (no code), in order

1. Run the Cowork prompt (`docs/COWORK-LOCAL-FIXES.md`), tasks 1 and 2 first (GBP), then
   NPPES with each doctor signed in.
2. Dr. Cedeno and Dr. Mustafa certify their NPPES updates; billing staff then update CAQH
   ProView for both, so Aetna, BCBS, Cigna, UHC and Medicare directories follow.
3. Print the two office QR review cards and turn on the after-visit text (audit section 5).
4. GoDaddy: make `jupiterveincenter.com` a single 301 to
   `https://jupiterlaser.com/services/vein-treatment/`.
5. Decide whether to buy back `abacoapodiatry.com` from the broker; until then it must
   appear nowhere.
6. GA4: confirm `call_click`, `appointment_cta` and `form_submit` are key events for the
   whole period (counts suggest they were flagged mid-window).
7. Merge this PR, then ping IndexNow for the changed URLs (README, IndexNow section) and
   request indexing for `/insurance/`, `/glossary/` and `/locations/palm-beach-gardens/` in
   Search Console.
8. Every January: update the Medicare figures on `/insurance/` (Part B deductible, premium)
   from the new CMS fact sheet and re-date the "Checked" line.

## 5. Decisions for Nick (also in the PR's questions)

See the PR body. The ones that block work: which legal entity bills (NPPES 1598726986 vs
1831779834), whether Ortho Florida's NPI 1174289045 should be updated or deactivated, and
whether the sitewide sister-practice footer links should become contextual links.

## 6. Next 90 days and how we will know

Re-read Search Console on or after 2026-11-15 (first full 28 days after merge) and again in
mid-January.

| Measure | Now (28 d to 2026-10-11) | 90-day target |
|---|---|---|
| Non-brand local medical clicks (query table) | 11 | 30 |
| "podiatrist jupiter" position / clicks | 5.8 / 4 | top 3 / 12 |
| Palm Beach Gardens Google reviews | 0 | 25 |
| Palm Beach Gardens GBP calls | 1 | 10 |
| Jupiter new Google reviews per month | about 2.8 | 4+ |
| Records still showing 624-4800 (audit table rows 1 to 12) | 11 | 0 controllable (Ortho Florida's record excepted) |
| Confirmed form submissions (GA4 form_submit) | 20 | 30 |
| Pages failing schema/visible match | 0 of 111 | 0 |

## 7. Guardrails

No invented facts, reviews, prices or drive times. No AggregateRating or Review schema. No
"medically reviewed by" without a recorded sign-off. No new city or doorway pages. No
national informational posts. No analytics on any form that collects clinical history.
Testimonials verbatim. Never name or disparage another practice. Never touch DNS, Google
Ads, GBP settings or NPPES from a session.
