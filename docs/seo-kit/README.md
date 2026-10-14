# SEO and local growth kit: START HERE

Everything from the October 2026 takeover audit of jupiterlaser.com (Abacoa Podiatry & Leg
Vein Center). This page says what each file is, whether it is current, and which file wins
when two disagree.

**Order of authority.** When two documents disagree, follow the first one on this list:

1. `CLAUDE.md` (repo rules and standing decisions)
2. `_src/build.py`, `_src/hours.py`, `_src/reviews.py`, `_src/glossary.py` (what the site ships)
3. The dated audits in `docs/` listed below
4. This kit (`docs/seo-kit/`), which is evidence and tooling

## The current plan and evidence (read these first)

| File | Status | What it is |
|---|---|---|
| `docs/GROWTH-PLAN-2026-10.md` | Current, 2026-10-14 | The levers ranked, what the data says, what shipped, owner actions in order, decisions for Nick, 90-day targets |
| `docs/GSC-DEEP-DIVE-2026-10.md` | Current, 2026-10-14; re-read after 2026-11-15 | Search Console: the four numbers, the noise in the impressions jump, local vs national split, 653 striking-distance queries (69 local), cannibalization, CTR outliers, 404s, and every title and page change with its date |
| `docs/LOCAL-AUTHORITY-AUDIT-2026-10.md` | Current, 2026-10-14 | Canonical facts, the citation error table (NPPES x5, Healthgrades, Healthline, Facebook, Yelp, WebMD, SEAK, Manta, both GBPs, domains), two-listings rule, GBP changes with ready descriptions, the review-request plan, specialty directories, brand plan |
| `docs/COWORK-LOCAL-FIXES.md` | Current, ready to paste | Browser prompt that makes the listing fixes, with stop rules. Owner-run, not Code |
| `docs/seo-kit/competitor-teardown-2026-10.md` | Current, 2026-10-14 | Per-site evidence (anonymized): title, H1, schema types, word count. Conclusion: not schema, not word count |
| `_dev/listings-nap.md` | Corrected 2026-10-14 | Field-by-field NAP values for both offices |

## Tools

| File | Use |
|---|---|
| `docs/seo-kit/scripts/check_schema_visible_match.py` | Checks a built page's JSON-LD against its visible text (FAQ, DefinedTerm, review markup, duplicate @ids). Run on any page whose schema changes: `python3 docs/seo-kit/scripts/check_schema_visible_match.py glossary/index.html`. All 111 pages passed on 2026-10-14 |
| `_dev/preflight.py` | Launch gate. Since 2026-10-14 it also fails on AggregateRating/Review schema, reviewedBy/lastReviewed, and any em dash in page text |
| `_dev/verify-testimonials.py` | Verbatim check for every quote on `/reviews/` and every reuse on other pages |
| `_dev/measure/measure.sh` | Lighthouse mobile + axe. `MEASURE_PAGES="/ /insurance/" bash _dev/measure/measure.sh <label>` |

## Things that recur every year

- **January:** update the Medicare figures on `/insurance/#medicare` (Part B deductible and
  premium) from the new CMS fact sheet, re-check the three Medicare.gov coverage pages, and
  change the "Checked against Medicare.gov and CMS on ..." date.
- **When GBP is pulled:** refresh `_src/reviews.py` (count, average, date) and rebuild.

## Questions that keep coming up

**Should we add review stars to the schema?** No. Self-serving review markup is not eligible
and the agency rule bans it; preflight now fails the build. The count is shown as dated text.

**Should we add FAQ schema to a page?** Only by adding visible `<details class="faq">`
questions. `build.py` builds FAQPage from them; the hand-written lists still sitting in old
META blocks are ignored.

**More city pages or national posts?** No. City intent is a GBP lever; national posts bring
readers who cannot become patients. Depth goes into the pages that already rank locally.

**Is `abacoapodiatry.com` ours?** Not since at least 2026-10-03: it is held by a domain
broker. Do not use it anywhere.
