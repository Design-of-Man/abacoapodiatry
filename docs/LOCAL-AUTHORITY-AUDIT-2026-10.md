# Local authority audit, 2026-10-14

Why the practice is not winning more local searches, and what fixes it. Evidence for the
competitor points is in `docs/seo-kit/competitor-teardown-2026-10.md`; the search data is in
`docs/GSC-DEEP-DIVE-2026-10.md`; the browser prompt that makes the listing fixes is
`docs/COWORK-LOCAL-FIXES.md`.

## 0. Canonical facts (use exactly these everywhere)

| Field | Value |
|---|---|
| Public name | Abacoa Podiatry & Leg Vein Center (former brand "Jupiter Laser & Regenerative Medicine" is an alternate name only) |
| Phone (both offices) | **(561) 915-1934**. (561) 624-4800 is the old, dead number |
| Fax | (561) 624-5206 (from Dr. Cedeno's credentialing card, added 2026-08-18; it shares the old exchange, so confirm it still rings, see questions) |
| Jupiter | 4601 Military Trail, Suite 202, Jupiter, FL 33458. Mon–Thu 8 AM–5 PM, Fri 8 AM–2 PM, Sat concierge appointments only, Sun closed |
| Palm Beach Gardens | 11380 Prosperity Farms Rd, Suite 204, Palm Beach Gardens, FL 33410. Mon, Tue, Wed 8 AM–4:30 PM, Fri 8 AM–2 PM, **Thu closed**, Sat concierge appointments only, Sun closed |
| Website | https://jupiterlaser.com (Palm Beach Gardens listings: https://jupiterlaser.com/locations/palm-beach-gardens/) |
| Physicians | Dr. Orlando Cedeno, DPM (NPI 1700076437, board certified); Dr. Isin A. Mustafa, DPM, MSHS, DABPM, DACFAS (NPI 1639585177) |

Hours source: `_src/hours.py`. Both Google Business Profiles matched these on 2026-10-14.

## 1. Why competitors outrank us (short version)

Not schema, and not word count (teardown). Every competitor that shows up has an office in
the town searched, and so do we, twice. What we lack is on three fronts:

1. **Citations carry a dead phone.** NPPES (all four records tied to the practice), Healthgrades
   and the directories that copy them still say (561) 624-4800. NPPES feeds insurer
   directories, Healthgrades, WebMD, Doximity and AI answers.
2. **The Palm Beach Gardens listing is thin.** Zero Google reviews, no secondary category,
   website pointing at the homepage, a description copied from Jupiter that says "in Jupiter,
   Florida" and names one doctor.
3. **The brand is spread across four names.** Abacoa Podiatry & Leg Vein Center (public),
   Jupiter Laser & Regenerative Medicine (old brand, still the Yelp listing name), Podiatry
   Associates of Palm Beach Gardens Inc (legal entity on NPPES and Healthgrades), and Ortho
   Florida, LLC doing business as "Podiatry Associates of Palm Beach Gardens" (a record the
   practice does not control).

## 2. Citation error table

One row per error. "Verified" means read on 2026-10-14 in this session; "per notes" means
reported in earlier notes and not re-readable from the sandbox (login wall or bot block), so
Cowork must confirm before changing anything.

| # | Where | What is wrong | Fix | Who |
|---|---|---|---|---|
| 1 | NPPES, Dr. Cedeno, NPI 1700076437 (verified) | Location and mailing phone 561-624-4800; Jupiter only (no Palm Beach Gardens practice location); last updated 2021-10-19; primary Florida taxonomy row has no description | Phone to 561-915-1934; add 11380 Prosperity Farms Rd Ste 204 as a practice location; set the primary taxonomy to the podiatry code he practices under | Dr. Cedeno (his own NPPES login; he certifies) |
| 2 | NPPES, Dr. Mustafa, NPI 1639585177 (verified) | Phone 561-624-4800; Jupiter only; credential field empty (should read DPM); updated 2026-06-16 | Phone; add the Palm Beach Gardens practice location if she sees patients there; credential "DPM" | Dr. Mustafa (her own login) |
| 3 | NPPES org, Podiatry Associates of Palm Beach Gardens Inc, NPI 1598726986 (verified) | Phone 561-624-4800, fax 561-624-5206; Jupiter only; authorized official Orlando Cedeno; updated 2021-10-18 | Phone; add the Palm Beach Gardens location. **First ask Nick which entity bills**; this legal name differs from the public brand | Dr. Cedeno as authorized official |
| 4 | NPPES org, Jupiter Laser and Regenerative Medicine LLC, NPI 1831779834 (verified, newly found) | Phone 561-624-4800; taxonomy "Clinic/Center, Primary Care" (a podiatry practice is not primary care); authorized official Orlando Cedeno; updated 2021-04-26 | If the LLC is still in use: phone and taxonomy. If not: ask whether to deactivate. Do not change without Nick's answer | Dr. Cedeno |
| 5 | NPPES org, Ortho Florida, LLC, NPI 1174289045, DBA "Podiatry Associates of Palm Beach Gardens" (verified) | Location 4601 Military Trl Ste 202 with 561-624-4800; mailing address Boca Raton; authorized official is Ortho Florida's CEO; updated 2021-11-15 | **Only Ortho Florida can change it.** Flag for Nick; never attempt | Ortho Florida (via Nick) |
| 6 | Healthgrades, Dr. Cedeno (verified) | (561) 624-4800 on both office entries; practice shown as "Podiatry Associates of Palm Beach Gardens Inc"; no board certification shown; 28 ratings averaging 4.1 | Claim via Healthgrades for Providers; phone 915-1934 on both locations; practice name; add board certification | Cowork, then Dr. Cedeno for identity checks |
| 7 | Healthline FindCare, Dr. Cedeno (verified) | (561) 624-4800 on both offices, same group name | Mirrors Healthgrades data; fix Healthgrades first, then use Healthline's correction link | Cowork |
| 8 | Healthgrades, Dr. Mustafa | No profile found by search on 2026-10-14 | Check whether one exists under "Isin Mustafa"; claim or create | Cowork, Dr. Mustafa |
| 9 | Facebook, facebook.com/AbacoaPodiatry (per notes) | Old 624-4800 number reported | Phone, hours for both offices, website | Cowork (Nick's login) |
| 10 | Yelp, "Jupiter Laser and Regenerative Medicine" (per notes; Yelp blocks the sandbox) | Old phone reported; listing under the old brand name; check for Suite 202 | Phone, name to Abacoa Podiatry & Leg Vein Center if Yelp allows, suite, hours. Apple Maps ingests Yelp | Cowork |
| 11 | WebMD Care (per notes) | Old phone reported | Correction request | Cowork |
| 12 | SEAK expert-witness directory, Dr. Cedeno (search snippet) | (561) 624-4800 | Ask SEAK to update (Dr. Cedeno's own account) | Dr. Cedeno |
| 13 | Manta, "Abacoa Podiatry & Leg Vein Center" (search snippet; Manta blocks the sandbox) | Listing is claimed and shows a bio for a "Dr. Raj Prabhakar", who is not on the practice's roster | Find who claimed it; correct roster, phone, both offices. Question for Nick | Cowork, Nick |
| 14 | Google Business Profile, Jupiter (verified via API) | Secondary category "Foot care" carries the service type "Foot massages"; "Medical Center" category; description names only Dr. Cedeno and contains an em dash; review replies on 12 of the last 34 reviews | Remove the "Foot massages" service type; ask Nick about dropping "Medical Center"; new description (below); reply to every review | Cowork (approved changes only) |
| 15 | Google Business Profile, Palm Beach Gardens (verified via API) | No secondary categories; website is the homepage; description copied from Jupiter ("in Jupiter, Florida"); 0 reviews | Website to /locations/palm-beach-gardens/; add "Medical clinic"; own description; review plan (section 5) | Cowork, front desk |
| 16 | Apple Business Connect, Bing Places (not checked) | Unknown; two listings needed | Claim/verify both offices with the facts above | Cowork |
| 17 | Doximity, Zocdoc, Vitals, US News, Medicare Care Compare (blocked or not found) | Unknown | Read each; record phone and offices; fix where claimable | Cowork |
| 18 | Insurer directories (Aetna, BCBS, Cigna, UHC) | Pull from NPPES and CAQH | After NPPES, update CAQH ProView for both doctors with the new phone and both offices | Practice billing staff |
| 19 | `abacoapodiatry.com` (verified) | Not the practice's domain: 302 to a HugeDomains "for sale" page; NameBright registrar; changed 2026-10-03 | Any listing, card or email signature that uses it sends patients to a sale page. Remove it everywhere; decide whether to buy it back | Nick / owner |
| 20 | `jupiterveincenter.com` (verified) | 302 (temporary) to `http://www.jupiterlaser.com/`, then two more hops | Registrar forwarding: one 301 to `https://jupiterlaser.com/services/vein-treatment/` | Owner (GoDaddy) |

The site itself carries no trace of 624-4800 (checked across every source and built file on
2026-10-14), so nothing on the website needs purging; every remaining instance is off-site.

## 3. Two offices, two listings, everywhere

Every platform that allows locations needs two: Google, Apple, Bing, Yelp, Facebook (one
page with both addresses in About is acceptable there), Healthgrades (both doctors, both
locations), and NPPES practice locations for both doctors. Name, address and phone must
match section 0 character for character, suite numbers included. `_dev/listings-nap.md` has
the per-field values and was corrected to these hours on 2026-10-14.

## 4. Google Business Profile

Read through the API on 2026-10-14.

| | Jupiter | Palm Beach Gardens |
|---|---|---|
| Primary category | Podiatrist | Podiatrist |
| Secondary | Foot care (with "Foot massages" service type), Medical Center, Medical clinic | none |
| Reviews | **193, average 4.9**; 34 in the last 12 months; newest 2026-10-13 | **0** |
| Impressions, 28 d (2026-09-14 to 10-11) | 1,014 (previous 28 d: 1,100) | 141 (131) |
| Calls / website clicks / directions | 60 / 64 / 88 (prev 71 / 61 / 83) | 1 / 5 / 29 (prev 0 / 4 / 62) |
| Website | https://jupiterlaser.com/ | https://jupiterlaser.com/ (should be the office page) |
| Services listed | 10 (no MLS laser) | 11 (includes MLS laser) |

Recommended changes (Cowork asks Nick before each category change):

- **Jupiter:** remove the "Foot massages" service type (it tells Google this is a spa). Keep
  Podiatrist primary. "Medical Center" usually means a hospital-type facility; propose
  removing it and keeping "Medical clinic". Add a UTM to the website link
  (`?utm_source=google&utm_medium=gbp&utm_campaign=jupiter`) so GA4 can separate profile
  traffic.
- **Palm Beach Gardens:** website `https://jupiterlaser.com/locations/palm-beach-gardens/?utm_source=google&utm_medium=gbp&utm_campaign=pbg`;
  add "Medical clinic" as secondary. **Do not add "Orthopedic surgeon" or a regenerative
  category**: the same suite houses ELITE Sports Medicine (owns "Orthopedic surgeon") and
  RegenOrtho Palm Beach, and listings at one address compete in Maps when categories
  overlap. Podiatry is this listing's lane.
- **Descriptions** (no em dashes; each under 750 characters):
  - Jupiter: "Abacoa Podiatry & Leg Vein Center is a podiatry practice on Military Trail in
    Jupiter. Board-certified foot and ankle surgeons Dr. Orlando Cedeno, DPM and Dr. Isin A.
    Mustafa, DPM treat heel pain and plantar fasciitis, bunions (including minimally invasive
    bunion surgery), neuropathy, diabetic foot problems, wounds, sports injuries and leg veins.
    Treatments include shockwave (EPAT), PRP and regenerative medicine, plus surgery when it is
    needed. Medicare and most major plans accepted. Our second office is on Prosperity Farms
    Road in Palm Beach Gardens."
  - Palm Beach Gardens: "Abacoa Podiatry & Leg Vein Center's Palm Beach Gardens office, Suite
    204 at 11380 Prosperity Farms Road, is home to our MLS laser, EPAT shockwave and
    regenerative medicine suites. Board-certified foot and ankle surgeons Dr. Orlando Cedeno,
    DPM and Dr. Isin A. Mustafa, DPM see patients for heel pain, bunions, neuropathy, diabetic
    feet, wounds and leg veins. Open Monday to Wednesday and Friday; closed Thursday. Medicare
    and most major plans accepted. Our main office is on Military Trail in Jupiter."
- **Photos:** the two the site still waits for (office exterior, MLS laser unit) belong on the
  Palm Beach Gardens listing first. One new real photo a month per listing; no AI images of
  the practice (STATUS.md).
- **Posts:** one a month per listing, linking the matching service page; Cowork drafts, Nick
  approves.

## 5. Review-request plan

Facts: Jupiter has 193 Google reviews (4.9) and about 2.8 new reviews a month over the last
12 months; Palm Beach Gardens has none. The August note "zero reviews" was the Gardens
listing. Target: **Palm Beach Gardens to 25 reviews in 90 days; Jupiter at 4+ a month.**

How (ask every patient, the same way, never selectively):

1. **QR card at each front desk**, one per office, each pointing at that office's own review
   link (a Jupiter patient reviewing the Gardens listing helps nobody):
   - Jupiter: `https://search.google.com/local/writereview?placeid=ChIJE3bekovV3ogRs7AajChyqKQ`
   - Palm Beach Gardens: `https://search.google.com/local/writereview?placeid=ChIJ42alBA8r34gR7G3gik_7tL0`
   Card text: "Did we take good care of you today? A short Google review helps neighbors find
   us. Scan to leave one for our <office> office."
2. **Text after the visit**, same day, only to patients who agreed to receive texts from the
   practice, from the practice's own patient-messaging system: "Thank you for visiting
   Abacoa Podiatry in <office> today. If you have a minute, a Google review helps others find
   us: <office link>. Reply STOP to opt out." No condition, procedure or doctor detail in the
   message.
3. **Reply to every review within a week**, thanking the reviewer without confirming they are
   a patient or mentioning any condition (HIPAA). 12 of the last 34 got a reply.

Never: offer anything for a review (discounts, gift cards, raffles), ask only patients who
seem happy ("review gating"), write or edit a review for a patient, have staff review the
practice, or ask in a way that pressures. Never post the review text on the site as schema.

Reviews already on the site are the nine verified quotes on `/reviews/`, now also reused
verbatim on five service and condition pages (checked by `_dev/verify-testimonials.py`).
The live Google count appears on the homepage as dated text ("193 Google reviews with a 4.9
average, as of October 14, 2026") from `_src/reviews.py`; refresh it when GBP is next pulled.

## 6. Specialty directories and earned links

Only memberships the site already states are listed; the practice confirms before any
listing is created.

- **ABFAS** board-certified surgeon search (both doctors are ABFAS certified per their pages).
- **ACFAS** "Find a Foot & Ankle Surgeon" on FootHealthFacts.org (Dr. Cedeno FACFAS,
  Dr. Mustafa DACFAS).
- **American Board of Podiatric Medicine** directory (Dr. Mustafa, DABPM).
- **AVLS** (American Vein & Lymphatic Society) find-a-specialist, for the vein half of the
  brand (Dr. Cedeno is a member).
- **APWCA** (wound care certification, Dr. Cedeno) and **FPMA** (Florida Podiatric Medical
  Association) member directories.
- **Jupiter Medical Center** find-a-doctor profile (Dr. Cedeno's privileges): confirm it shows
  the new phone and links the site.
- **Sister practices.** ELITE Sports Medicine and RegenOrtho Palm Beach link here from their
  footers and this site links back from its footer, at Dr. Cedeno's request. Sitewide
  reciprocal footer links between related sites are the pattern Google's link-scheme policy
  describes; a contextual link from each About or physician page is the safer form. Raised
  as a question for Nick, not changed.

## 7. Brand plan

No collision with another practice was found (NPPES and search, 2026-10-14). The problem is
self-inflicted name sprawl. Use "Abacoa Podiatry & Leg Vein Center" on every listing; keep
"Jupiter Laser & Regenerative Medicine" only as `alternateName` in the site schema and as an
"also known as" where a directory supports it; never use the legal entity names publicly.
`abacoapodiatry.com` must not appear anywhere until the practice owns it again.
