# Search Console deep dive, 2026-10-14

Property: `sc-domain:jupiterlaser.com` (the domain property; it is the one `gsc.py sites`
lists for this site). Pulled 2026-10-14 with `gsc.py`. Data lags about three days, so the
current 28-day window ends 2026-10-11. Raw pulls (query, page, query+page, date) stayed in
the session scratchpad; nothing patient-related is in Search Console data.

## 1. The numbers that matter

| | Previous 28 days (2026-08-17 to 2026-09-13) | Current 28 days (2026-09-14 to 2026-10-11) | Change |
|---|---|---|---|
| Clicks | 566 | 837 | +48% |
| Impressions | 66,271 | 125,493 | +89% |
| CTR | 0.85% | 0.67% | down 0.19 pp |
| Average position | 20.5 | 10.1 | better (lower is better) |

Totals are zero-dimension reads (the true total). The query and page tables below are
truncated by Google and are used only for shares and examples, never for totals.

90-day view, for context: 2,184 clicks and 308,602 impressions (2026-07-14 to 2026-10-11)
against 2,483 and 476,252 in the 90 days before. The earlier window starts 2026-04-15 and
the property holds no data before 2026-04-18 (see `MIGRATION.md`), so it is three days
short; the decline it shows is real and was already documented in August.

### The headline impressions jump is mostly noise

The +89% impressions and the average position "improving" from 20.5 to 10.1 are not the
practice getting found more. Split the (truncated) query table into segments:

| Segment, share of table impressions | Previous 28 d | Current 28 d |
|---|---|---|
| Brand (Abacoa, Cedeno, Mustafa, misspellings) | 1.4% (454) | 1.3% (710) |
| Local medical (a town or "near me" plus a foot, ankle, vein or doctor term) | 18.2% (5,977) | 9.5% (5,203) |
| National commercial ("podiatrist", "doctor", "clinic" with no place) | 0.8% (276) | 1.4% (775) |
| National informational (how-to, what-is, symptoms) | 78.3% (25,647) | 73.0% (39,957) |
| **Local non-medical noise** ("jupiter fl hotels", "houses for sale jupiter", "planet jupiter") | 1.3% (415) | **14.8% (8,076)** |

The homepage started ranking around position 9 to 10 for hundreds of "Jupiter" real-estate,
astronomy and town-hall queries in October (804 such queries, 1 click). Those impressions
can never become patients and they drag CTR down while making average position look
better. **Report clicks, not impressions, until this settles,** and read average position
per page, not sitewide.

Clicks did rise for real: the cortisone-shot article (124 to 257), the homepage (41 to 103,
mostly brand and "podiatrist jupiter"), the Achilles articles and both physician pages
(Dr. Mustafa 12 to 32).

### Local is still about 5% of clicks

The August audit found 95% of impressions national and informational. It is the same
picture now: in the current 28 days local medical queries are 9.5% of table impressions
and **5.7% of clicks (11 of 192 table clicks)**; national informational is 73% of
impressions and 59% of clicks. One article, `/plantar-fasciitis-steroid-injection-when-to-consider-it/`,
earns 31% of all clicks (257 of 837) at position 6, almost entirely from people who are not
in Palm Beach County.

## 2. Striking distance

Definition: non-brand query, average position 4 to 20, at least 10 impressions in the
current 28 days.

- **653 striking-distance queries** (34,235 impressions).
- **69 of them are local medical** (2,697 impressions). The rest are national
  informational (most), plus 119 local non-medical noise queries.

### The local commercial set, and the page that owns each

| Query | Impr. | Clicks | Pos. | Ranking page |
|---|---|---|---|---|
| podiatrist jupiter | 147 | 4 | 5.8 | `/` |
| podiatrist near me | 110 | 1 | 17.7 | `/` |
| jupiter foot and ankle | 99 | 0 | 9.0 | `/` |
| jupiter pad treatment | 73 | 0 | 6.0 | `/diabetic-foot-care/` (old URL, 301 to the condition page) |
| jupiter spider vein | 70 | 0 | 8.2 | `/services/vein-treatment/` |
| jupiter wound care | 68 | 0 | 7.9 | `/services/wound-care/` |
| stem cell therapy jupiter fl | 68 | 0 | 7.4 | `/stem-cell-therapy/` (withdrawn page, now a redirect stub) |
| jupiter chronic venous insufficiency | 67 | 0 | 6.2 | `/services/vein-treatment/` |
| jupiter cosmetic vein care | 64 | 0 | 7.8 | `/services/vein-treatment/` |
| jupiter varicose vein | 64 | 0 | 8.7 | `/services/vein-treatment/` |
| jupiter sclerotherapy | 63 | 0 | 9.6 | `/services/vein-treatment/` |
| palm city vein treatment | 60 | 0 | 12.9 | `/services/vein-treatment/` |
| achilles tendon treatment jupiter | 59 | 0 | 4.6 | `/achilles-tendon-treatment-jupiter/` (old URL) |
| ankle pain treatment jupiter | 58 | 0 | 11.3 | `/` |
| bunion treatment palm beach | 50 | 0 | 18.2 | `/conditions/bunions/` |
| jupiter endovenous ablation | 50 | 0 | 4.4 | `/services/vein-treatment/` |
| jupiter microphlebectomy | 42 | 0 | 8.3 | `/services/vein-treatment/` |
| platlet rich plasma jupiter | 42 | 0 | 17.1 | `/services/prp-therapy/` |
| podiatrist jupiter fl | 41 | 1 | 4.7 | `/` |
| peripheral nerve specialist jupiter, fl | 21 | 0 | 6.2 | `/conditions/neuropathy/` |

**Caution on the "jupiter + vein term" rows.** Seven near-identical queries ("jupiter
spider vein", "jupiter varicose vein", "jupiter cosmetic vein care", "jupiter sclerotherapy",
"jupiter endovenous ablation", "jupiter chronic venous insufficiency", "jupiter
microphlebectomy") each show 60 to 115 impressions over 90 days, at steady positions, with
zero clicks ever. Several "stem cell therapy for <body part> jupiter" and "bmac injection
jupiter" / "radial shockwave therapy jupiter" rows (position 1.0, hundreds of impressions,
0 clicks) look the same. That pattern is typical of a rank-tracking tool checking a keyword
list every day, not of patients. Treat those rows as a rank tracker's view of us, useful for
position, worthless as demand. Ask Nick whether the previous vendor or anyone else still
runs one (questions list).

The real local demand signal is Google Business Profile search terms (September 2026,
Jupiter listing): "podiatrist near me" 25, "podiatrist" 22, "podiatrist jupiter" 19,
"abacoa podiatry" 17, "dr cedeno" 16, "jupiter medical center" 16, "podiatrist jupiter
military trail" 16, plus under-15 terms including "podiatrist palm beach gardens", "dr
mustafa podiatrist in palm beach gardens fl", "vein doctor jupiter", "foot doctor jupiter",
"ingrown toenail" and "fungal toe clinic".

## 3. Cannibalization

122 non-brand queries had two or more pages each earning 10+ impressions over 90 days.
Most of it is the July to August overlap of old WordPress URLs and their new equivalents,
which the 301s are now consolidating. The two live cases:

- **"bunion surgery" / "types of bunion surgery"**: the merged article
  `/types-of-bunion-surgery-which-procedure-is-right-for-you/` (merge shipped 2026-09-28)
  and the new `/minimally-invasive-bunion-surgery/` page. `/conditions/bunions/` now links
  both in its local section. Re-read in November.
- **"podiatrist jupiter" / "jupiter foot and ankle"**: the homepage plus `/about/`, `/faq/`,
  `/services/`, `/conditions/`. The homepage is the right owner and now says "Podiatrist in
  Jupiter and Palm Beach Gardens" in an H2 with both addresses and both doctors.

## 4. CTR far below position

Pages with 1,000+ impressions at position 12 or better and CTR under 1% (current 28 days):

| Page | Impr. | Clicks | CTR | Pos. |
|---|---|---|---|---|
| `/plantar-fasciitis-steroid-injection-when-to-consider-it/` | 29,073 | 257 | 0.88% | 6.0 |
| `/` (noise-inflated, see 1) | 15,352 | 103 | 0.67% | 11.3 |
| `/best-guide-to-first-metatarsophalangeal-joint-arthritis/` | 11,780 | 16 | 0.14% | 8.1 |
| `/cold-vs-warm-therapy-for-foot-pain-which-one-works-best/` | 5,286 | 7 | 0.13% | 9.1 |
| `/how-laser-therapy-can-improve-wound-healing-and-reduce-scarring/` | 3,833 | 18 | 0.47% | 8.2 |
| `/how-advanced-diagnostic-tools-help-in-accurate-assessment-of-achilles-tendonitis/` | 2,694 | 3 | 0.11% | 7.2 |

All of these are national informational articles, and three of them were retitled on
2026-09-28 (`e90c6fef`). They were left alone on purpose: the brief for this run is local
over national, a second retitle inside three weeks would make both changes unmeasurable,
and the clicks they could gain are not patients. The local fix is to route their readers to
a local page, which the heel pain page now does for the cortisone article (and the article
already links back).

## 5. Old and broken URLs

- 42 URLs earned impressions while returning 404 in the last 90 days. Almost all are
  garbled copies of real slugs (typos and paraphrases, the pattern AI answer engines produce
  when they quote a URL from memory). The ones with 2+ impressions now 301 to the real page
  (`_src/redirect-map.tsv`, 2026-10-14 block): `/plantar-fascia-steroid-injection-when-to-consider-it/`
  (29 impressions), `/is-and-ankle-surgery-worth-it-...` (12), two "top 5 myths" variants,
  `/best-guide-to-first-mtp-joint-arthritis/` and `/plantar-fascitis-steroid-...`.
- GA4 showed three more landing on a 404 in the same 28 days: `/plantar-plate-injuries`
  (11 sessions), `/provider/orlando-cedeno-dpm` (10) and
  `/when-is-ankle-replacement-surgery-necessary-signs-you-shouldnt-ignore` (8). All three
  now 301 (the first to the conditions hub, since no plantar plate page exists).
- `www.jupiterlaser.com` returns 308 to the apex (checked 2026-10-14). Search Console
  still shows 3,096 impressions and 72 clicks on www URLs over 90 days; that is the tail
  of the pre-cutover index and should fade.

## 6. Changes made from this data (dated, for the next read)

Shipped in the 2026-10-14 PR; re-read on or after **2026-11-15** (28 full days after merge
plus the 3-day lag):

| Page | Change |
|---|---|
| `/services/vein-treatment/` | Title "Varicose & Spider Vein Treatment in Jupiter, FL \| Sclerotherapy, EVLT, Ablation" (79 chars, truncated) to "Vein Treatment in Jupiter, FL \| Varicose & Spider Veins" (55). New description. Question-shaped H2s, a "where to get vein care" section with both offices and hours, verbatim patient review |
| `/locations/palm-beach-gardens/` | Title "Podiatrist in Palm Beach Gardens, FL \| Abacoa Podiatry & Leg Vein Center" (72) to "Podiatrist in Palm Beach Gardens, FL \| Abacoa Podiatry" (54). New description with "foot doctor". Who you will see (both doctors), bunion line, visible FAQ (hours, insurance, phone, suite) |
| `/insurance/` | Title "Insurance & Coverage \| Jupiter Podiatry Costs Explained" to "Insurance & Medicare Podiatry Coverage \| Jupiter, FL". Medicare and podiatry guide (2026 figures, CMS and Medicare.gov sources), three new visible FAQs |
| `/` | Description now leads "Podiatrist in Jupiter and Palm Beach Gardens, FL". H2 "Podiatrist in Jupiter and Palm Beach Gardens" with both addresses, both doctors, conditions and insurance; dated Google review count as text |
| `/conditions/heel-pain/` | Question H2s; "should I get a cortisone shot", "when to see a podiatrist", "where in Jupiter or Palm Beach Gardens" sections; links to the 29k-impression cortisone article |
| `/conditions/bunions/` | Description; "where can I have bunion surgery near Jupiter or Palm Beach Gardens" section; verbatim review |
| `/conditions/neuropathy/`, `/conditions/diabetic-foot-care/`, `/services/wound-care/`, `/services/mls-laser-therapy/` | Local "where" sections with both offices, verified credentials (APWCA wound care, AENS) and Medicare rules where they apply |
| `/glossary/` | New: 43-term patient glossary with DefinedTermSet built from the same list |

What to look for in November: clicks and position for "podiatrist jupiter", "podiatrist
palm beach gardens", "foot doctor palm beach gardens", "jupiter wound care", "bunion
surgery west palm beach" and the vein queries (position only, see the caution in 2), and
impressions for Medicare queries on `/insurance/`.
