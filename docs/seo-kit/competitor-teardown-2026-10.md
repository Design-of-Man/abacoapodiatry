# Competitor teardown, 2026-10-14

Raw HTML of each page below was fetched on 2026-10-14 and parsed for title, H1, JSON-LD
types and visible word count (`<script>`, `<style>`, `<svg>` stripped). The raw HTML is
third-party content and is not committed. Conclusions and actions are in
`docs/LOCAL-AUTHORITY-AUDIT-2026-10.md`.

**Competitors are not named in this repo.** The agency rule is never to name, report or
disparage another practice, so each one is a letter. The mapping from letter to practice
is in the session report to Nick, not here.

## How the list was built

Firecrawl (the usual SERP tool) was out of credits on 2026-10-14, so the organic sample
comes from the session's web search for six money queries, and the map pack could not be
pulled at all. Treat the "who ranks" column as indicative, not a rank tracker reading. The
map-pack comparison is the first job for the next session with a SERP tool (see the growth
plan, lever 1).

Queries: `podiatrist Jupiter FL`, `podiatrist Palm Beach Gardens FL`, `bunion surgery
Jupiter FL`, `varicose vein treatment Jupiter FL`, `heel pain treatment Jupiter FL
podiatrist`, `neuropathy treatment Jupiter FL foot`.

## Per page

| Site / page | Office in the searched town? | Title pattern | H1 | JSON-LD types (deduplicated) | Words |
|---|---|---|---|---|---|
| A, Jupiter location page (multi-office podiatry group) | Yes, Military Trail, Jupiter | "<Group> Jupiter \| Podiatry & Foot Care" | "<Group> Jupiter" | Organization, WebPage, WebSite, BreadcrumbList, FAQPage, SearchAction | ~2,350 |
| B, home page (multi-office foot and ankle group, Jupiter clinic) | Yes, Jupiter Lakes Blvd | "Foot and Ankle Specialists \| Best Podiatrist in South Florida" | "Why choose <group>" | Organization, WebPage, WebSite, BreadcrumbList, SearchAction | ~2,560 |
| C, home page (single podiatrist, Palm Beach Gardens) | Yes, Prosperity Farms Rd | "<Brand> - Foot Doctor, Podiatrist Jupiter, Florida" | none | LocalBusiness, Organization, WebSite | ~400 |
| D, Jupiter location page (dermatology group with a vein center) | Yes, Jupiter | "Dermatologist Jupiter FL \| <Brand>" | "<Brand> \| Jupiter" | MedicalClinic, MedicalBusiness, MedicalOrganization, MedicalProcedure, MedicalTherapy, Physician, FAQPage, ReserveAction, GeoCoordinates | ~770 |
| E, podiatry page (orthopedic institute, West Palm Beach) | No (West Palm Beach) | "Podiatrists in West Palm Beach, FL \| <Institute>" | "Expert Podiatrists in West Palm Beach, FL" | MedicalClinic, MedicalBusiness, Physician, Service, MedicalProcedure, OpeningHoursSpecification, NewsArticle | ~1,590 |
| F, Palm Beach Gardens podiatry group | Yes, Burns Rd | n/a (site timed out, HTTP 522) | | | |
| **Us, home page** | Yes, Jupiter and Palm Beach Gardens | "Jupiter Podiatrist \| Abacoa Podiatry & Leg Vein Center" | "Walk Without Pain Again. Jupiter's Foot & Ankle Specialists." | MedicalClinic + LocalBusiness ×2 (both offices), Physician, WebPage, WebSite, OpeningHoursSpecification, SpeakableSpecification (AggregateRating removed 2026-10-14) | ~1,900 |

Directories that answered the same searches: Healthline FindCare (mirrors Healthgrades),
Healthgrades, a Palm Beach health network directory, MediFind, Top4 and Manta. Healthline
and Healthgrades both show Dr. Cedeno with the dead (561) 624-4800 number on both offices.

## Reading it

1. **Schema is not the gap.** Only D and E carry a medical node richer than ours, and A
   (the one that appears for "podiatrist Jupiter" and "heel pain Jupiter" alike) ships
   Yoast defaults. Keep our markup accurate and matched to the page; do not spend more
   time on it to win rankings.
2. **Word count is not the gap.** A and B run about 2,400 words on a location or home page;
   our home page is about 1,900, and the service and condition pages deepened in this PR
   are now in the same range or above. Depth went into pages that already rank, not into
   new pages.
3. **Every one of them has an office in the searched town.** So do we, twice. Our map
   problem is not proximity in Jupiter; it is the Palm Beach Gardens listing (zero
   reviews, no secondary category, generic website link) and directory data that still
   carries a dead phone number.
4. **Review volume.** Our Jupiter Google profile (193 reviews, 4.9) is strong. Palm Beach
   Gardens has none, which is the one place a competitor with an office on the same road
   (C) can out-review us cheaply. That is the review plan's first target.
5. **Do not copy E's "Podiatrists in West Palm Beach" pattern.** We have no office there;
   a page claiming one would be a doorway page.
