# Disabled pages

`build.py` only globs `_src/pages/*.html`, so anything parked here is kept in
the repo, kept in git history, and simply not built or published.

## The stem cell pages

All three were pulled from the live site on 2026-08-18 at Dr. Cedeno's request
-- the service page first, then both articles once he confirmed. His stated
reason was that the content "pushes the site down on Google"; the sharper
reasons to keep it down are that stem-cell clinic marketing is an active
FDA/FTC enforcement area, and that Google Ads restricts unproven cellular
therapies, which matters because running ads is on the roadmap. Google does not
demote for the phrase itself, but weakly-substantiated YMYL medical content can
drag sitewide quality assessment, which is the closest real mechanism to what
he described.

They are parked rather than deleted because he asked for them back "on standby"
for when he wants them edited.

| file | was served at |
|---|---|
| `services-stemcell.html` | `/services/stem-cell-therapy/` |
| `post-stem-cell-foot-ankle.html` | `/the-role-of-stem-cell-therapy-in-foot-and-ankle-injuries/` |
| `post-stem-cell-leg-injuries.html` | `/how-can-stem-cell-therapy-benefit-leg-injuries/` |

All three URLs now 301 to `/services/regenerative-medicine/`. The two article
URLs are old-site URLs that had been ported back onto their original paths
precisely because they earned traffic, so they are worth restoring if the
content is ever reworked rather than abandoned.

### Putting one back

1. `git mv _src/pages-disabled/<file> _src/pages/`
2. Remove that page's row from `_src/redirect-map.tsv`. `build.py` hard-fails if
   a redirect source is also a built page -- the check that stops a page
   shipping to a URL that 301s away from it. It caught exactly this during the
   withdrawal.
3. For the service page only: repoint the inbound links currently aimed at
   `/services/regenerative-medicine/`, if wanted -- `home.html`, `faq.html`,
   `technology.html`, `services-index.html`, `services-regen.html`,
   `template.html` (two nav entries were removed as duplicates),
   `assets/js/assistant.js`, `llms.txt`.
4. Rebuild, run `_dev/preflight.py`, and **commit `sitemap.xml`** -- restoring a
   page is a content change, so the usual "revert the sitemap" rule does not
   apply. Getting that backwards is what left a redirecting URL in the sitemap
   during the withdrawal.

## The plain-English bunion surgery guide

`blog-types-of-bunion-surgery-a-plain-english-guide-to-your-options.html` was
parked on 2026-09-28. It covered the same ground as the older
`post-bunion-surgery-types.html` (`/types-of-bunion-surgery-which-procedure-is-right-for-you/`),
which carries the ranking history (about 4,300 Search Console impressions in its
last 28 days, against 34 for this one), so the two were splitting the same
searches. Its two details the older article lacked (distal vs proximal
osteotomy names, and "bunionectomy" as an umbrella term) were folded in. Its URL
301s to the older article.

## The heel pain / plantar fasciitis articles

Parked on 2026-11-03. Six pages targeted Jupiter heel pain and plantar fasciitis,
and Google was ranking an article instead of the condition page ("plantar fasciitis
treatment jupiter" and "heel pain treatment near me" both landed on
`/innovative-treatments-for-plantar-fasciitis-beyond-traditional-methods/`). Their
unique material was folded into the two survivors, and each URL 301s there:

| file | was served at | now 301s to |
|---|---|---|
| `post-plantar-fasciitis-advanced-treatments.html` | `/innovative-treatments-for-plantar-fasciitis-beyond-traditional-methods/` | `/conditions/plantar-fasciitis/` |
| `post-plantar-fasciitis-laser-shockwave-prp.html` | `/plantar-fasciitis-treatment-laser-shockwave-prp-jupiter/` | `/conditions/plantar-fasciitis/` |
| `post-heel-pain-jupiter-causes-treatment.html` | `/heel-pain-jupiter-fl-causes-treatment/` | `/conditions/plantar-fasciitis/` |
| `post-heel-pain-other-causes.html` | `/heel-pain-causes-not-plantar-fasciitis/` | `/conditions/heel-pain/` |

`/conditions/plantar-fasciitis/` is the plantar fasciitis diagnosis and treatment
page; `/conditions/heel-pain/` is the "heel pain that isn't plantar fasciitis" page.
Unsourced figures in the parked articles (shockwave success rates, the share of
chronic heel pain from Baxter's nerve, the share needing surgery, PRP-vs-cortisone
study results) were deliberately not carried over.
