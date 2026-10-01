# New-patient Search campaign — October 2026

The campaign, its reasoning, and the order to switch it on. `campaign.py` is the
single source of truth for what goes into Google Ads; this file explains why.
Regenerate the import files after any edit:

```
python3 _dev/ads/2026-10-new-patients/campaign.py
```

It refuses to write anything if a headline, description, path, callout or
sitelink is over Google's limit, or if a negative keyword would block a keyword
the campaign is buying.

Account: Google Ads `924-500-5023` ("Dr. Cedeno"). Audit windows are stated in
real dates below; the full audit with charts is the client report artifact.

## What the audit found (Google Ads, 2026-07-03 to 2026-09-30)

$12,468 spent. The search-terms report shows the query behind $7,386 of it, and
that visible spend splits like this:

| who was searching | spend | share |
|---|---|---|
| a competitor practice or a named doctor | $2,010 | 27% |
| a hospital or unrelated clinic (top term: "jupiter medical center", $885) | $1,831 | 25% |
| a podiatrist, generically ("podiatrist jupiter", "foot doctor near me") | $1,457 | 20% |
| Abacoa, Dr. Cedeno or Dr. Mustafa by name | $626 | 8% |
| an orthopedic group or other specialty | $478 | 6% |
| a foot condition, with intent to treat | $469 | 6% |
| physical therapy | $204 | 3% |
| a foot condition, researching ("what kills toenail fungus instantly") | $180 | 2% |
| other | $131 | 2% |

So about a quarter of the visible spend reached someone looking for a
podiatrist or naming a foot problem. About 60% reached someone looking for a
different provider.

Three broad-match keywords did most of the drifting, $4,650 between them:
`podiatrist jupiter` ($2,129, matched "jupiter medical center"),
`dr cedeno jupiter` ($1,365, matched other podiatrists' names), and
`orthopedic that takes medicaid near me` ($1,156). The practice's insurance list
(`/insurance/`) has no Medicaid plan.

**The conversion numbers can't be trusted as they stand.** The only primary
conversion is "Calls from ads": a tap on the call button in the ad itself. 55%
of the conversions on visible search terms came from people searching for a
hospital, competitor, PT clinic or orthopedic group, which reads as people
calling the number in the ad thinking it was the place they searched for.
Meanwhile every call and form that happens *on the website* is invisible to
Google Ads: GA4 has been receiving `call_click`, `form_submit` and
`appointment_cta` since 2026-09-03, but they were never imported. In September
GA4 attributes 18 website call taps and 3 form submissions to paid search that
Google Ads did not count. Smart bidding has been optimising toward the
wrong-number calls.

Other numbers that shaped the settings:

- 97% of spend is on mobile.
- Weekend: $1,002 for 9 calls ($111 each). Weekdays: $36 each.
- Spend by area: north Palm Beach County and Martin County $33 per call;
  Wellington / Greenacres / Lake Worth $52; out of state (New York,
  Philadelphia, Midland TX) $255 for 3 calls.
- Clinic, Doctor and Brand each lose 44–59% of impression share to budget,
  but on broad keywords that spend the budget on the queries above.
- September CPC rose to $7.12 from $4.73 in August (Treatment campaign paused,
  budgets raised, two Bunion Boss campaigns at $24 a click).

## What this campaign changes

1. **Only phrase and exact match.** 88 keywords across six intents: local
   podiatrist searches, bunions, heel pain, ingrown toenails, ankle and sports
   injuries, diabetic foot and neuropathy.
2. **Each ad group lands on the page that answers it**, not the homepage
   (which took 899 ad clicks in 90 days). Generic podiatrist searches and
   ingrown toenails go to the new `/see-a-podiatrist-this-week/`.
3. **Dr. Isin Mustafa is the face of it.** Every ad group carries her name and
   "Accepting New Patients"; the landing page leads with her; its booking links
   open the contact form with her preselected (`/contact/?doctor=mustafa`), so
   the office sees "Preferred doctor: Dr. Isin Mustafa" on the email. Patients
   who already know her name get their own ad group in the Brand campaign.
4. **185 negatives**, grouped by the audit row they come from (see `NEGATIVES`
   in `campaign.py`). The non-competitor groups also go on Clinic, Doctor and
   Brand on day one.
5. **Presence-only location targeting**, 18 miles around the Jupiter office.
6. **Office hours only**: Mon–Thu 7am–5pm, Fri 7am–2pm. No weekends.

## Switch-on order

Do these in order. Step 1 matters most: without it nothing after it can be
judged.

**1. Measurement (day 1, ~20 minutes in Google Ads + GA4)**
- Link GA4 property `391066165` (jupiterlaser.com) to Google Ads `924-500-5023`.
- Import `call_click` and `form_submit` as **primary** conversions, category
  Lead. Import `appointment_cta` as **secondary** (a click toward the form,
  not a lead).
- On "Abacoa Podiatry - Calls from ads", raise the minimum call length to
  **90 seconds**. A misdial asking for Jupiter Medical Center ends sooner.
- Ask the front desk to note, for each new patient, how they found the
  practice and which doctor they booked with. That is the only source for the
  number that matters: new patients seen.

**2. Stop the leak in the running campaigns (day 1)**
- Add the shared negatives (`negatives.csv`, rows for Clinic, Doctor, Brand).
- Pause the Brand campaign's **Competitors** ad group ($788 in the 90 days on
  competitor names; can't be judged until step 1 is done).
- In Doctor, pause `orthopedic that takes medicaid near me`,
  `walk in orthopedic near me` and `orthopedic west palm beach`.
- Change `podiatrist jupiter` (Clinic) and `dr cedeno jupiter` (Brand) from
  broad to phrase.
- Set every campaign's location option to **presence only**.

**3. Launch (day 2–3)**
- Create the campaign from `campaign.json` (or import the CSVs in Google Ads
  Editor). It is created **paused**. Review, then enable.
- Add the Dr. Mustafa ad group to Brand.

**4. Budget, first three weeks**

| campaign | daily | ~monthly |
|---|---|---|
| NP – New Patients (new) | $85 | $2,585 |
| Brand (tightened) | $15 | $455 |
| Doctor (with negatives) | $25 | $760 |
| Clinic (with negatives) | $25 | $760 |
| **total** | **$150** | **~$4,560** |

September spent $4,913 on Google, so this is roughly level. Clinic and Doctor
keep running at reduced budget as a comparison, not out of sentiment.

**Day 21 decision:** compare cost per lead (website call tap + form + ad call
of 90s or more) between NP and Clinic/Doctor. Pause whichever is worse and move
its budget. If NP is limited by budget with more than 20% impression share
lost to budget, raise it.

## Bidding

Maximize Clicks with a $9 CPC ceiling to start. Switch NP to Maximize
Conversions once it has 30+ conversions from the cleaned set (step 1). Doing it
sooner points the bidder back at the wrong-number calls it learned from.

## What to check weekly

- **Search terms report** for NP. Anything naming another provider, a
  hospital, a body part we don't treat, or asking a research question goes
  into `NEGATIVES` here, then into the account.
- Impression share and lost-to-budget on NP.
- Calls of 90s+, website call taps and forms, by ad group.
- From the office: new patients from Google, and how many booked with
  Dr. Mustafa.

## Targets for the first 60 days

These are starting targets from the account's own history, not forecasts.

- NP search impression share **60%+** on its keywords.
- Cost per lead (cleaned set) **under $60**. Generic podiatrist searches in
  this account turned 15% of clicks into ad calls at ~$6.25 a click, about $42
  a call, before website leads were counted at all.
- **40+ leads a month** from NP by month two.
- Dr. Mustafa's new-patient bookings: needs a baseline from the office first.

## Open questions for the practice

- Which office(s) and days does Dr. Mustafa see patients? If she is at Palm
  Beach Gardens, that office gets its own location-targeted ad group.
- How many new-patient slots does she have open per week? That sets the
  ceiling on how hard to push.
- Confirm ingrown toenail treatment is a service you want advertised (it has
  no page on the site yet).
- Does anyone on staff speak Spanish? "podiatras cerca de mi" and similar
  queries convert, but the ads are English-only.
- The Palm Beach Gardens Google Business listing has 0 calls since it was
  created, no reviews, and no map coordinates in the API. Is it verified?
