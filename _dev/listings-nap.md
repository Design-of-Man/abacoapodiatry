# Listings and NAP — the canonical values

Every directory must carry **identical** name, address and phone. Inconsistent NAP is
one of the few local-SEO problems that actively costs rankings rather than merely
failing to help, and it is the easiest to create by accident — four people filling in
four forms from memory.

Everything below is taken from the site's own structured data, which is what search
engines already read. Enter it verbatim. Where a field is a judgement call it says so.

---

## The two locations

The practice runs two. The schema models this correctly — the main `#clinic` node is
Jupiter, with Palm Beach Gardens as a `department` and a child entity carrying
`parentOrganization`. **That means two listings on every platform, not one.**

### Main — Jupiter

| Field | Value |
|---|---|
| Name | `Abacoa Podiatry & Leg Vein Center` |
| Street | `4601 Military Trail, Suite 202` |
| City / State / ZIP | `Jupiter`, `FL`, `33458` |
| Phone | `(561) 915-1934` |
| Website | `https://jupiterlaser.com` *(after cutover — see MIGRATION.md)* |
| Geo | `26.8934, -80.1096` |

### Branch — Palm Beach Gardens

| Field | Value |
|---|---|
| Name | `Abacoa Podiatry & Leg Vein Center — Palm Beach Gardens` |
| Street | `11380 Prosperity Farms Rd, Suite 204` |
| City / State / ZIP | `Palm Beach Gardens`, `FL`, `33410` |
| Phone | `(561) 915-1934` *(same line)* |
| Website | `https://jupiterlaser.com/locations/palm-beach-gardens/` |
| Geo | `26.8412, -80.0714` |

### Both

| Field | Value |
|---|---|
| Hours | Mon–Thu `08:00–17:00`, Fri `08:00–14:00`, Sat–Sun closed |
| Price range | `$$` |
| Practitioners | Dr. Orlando Cedeno, DPM · Dr. Isin A. Mustafa, DPM, MSHS |

**The suite numbers are the thing to watch.** They are the field most often dropped, and
dropping one is what sends a patient to the right building and the wrong floor.

---

## Google Business Profile

The one account already accessible, and the highest-leverage work available — it is also
**the unlock for `/reviews/`**, which currently carries eight unverified testimonials and
cannot go live as-is. Real Google reviews are what replace them.

- **Primary category:** `Podiatrist`
- **Secondary:** `Foot care`, `Medical clinic`, and something vein-related — the
  business is a *Leg Vein Center* and the current listing almost certainly does not say
  so anywhere. That half of the name is invisible to search without it.
- **Services:** MLS laser therapy · Shockwave therapy (EPAT) · PRP · Regenerative /
  stem cell therapy · Foot BBL™ · Bunion correction · Diabetic foot care · Wound care ·
  Flat feet · Custom orthotics · Minimally invasive surgery
- **Photos:** the two the site is still waiting on do double duty here — the building
  exterior (`/contact/`) and the MLS laser unit (`/technology/`). Worth requesting once
  and using in both places.
- **Q&A:** seed it from `/faq/`. The answers are already written and already marked up
  as `FAQPage`.

## Apple Maps — Apple Business Connect

`businessconnect.apple.com`, free, and where the missing Suite 202 gets fixed. Worth
doing properly because Apple Maps is the iPhone default and feeds Siri's "podiatrist
near me".

**Fix Yelp at the same time.** Apple ingests business data partly from third parties
including Yelp, and this practice has a Yelp listing already
(`yelp.com/biz/jupiter-laser-and-regenerative-medicine-jupiter`). If Yelp is missing the
suite number, that is the likely upstream source — correcting Apple alone risks it
drifting back on the next sync.

## Bing Places

Free, imports directly from Google Business Profile in a couple of clicks, and feeds
Copilot and DuckDuckGo. Do it after GBP is correct so the import carries good data.

---

## Closing the loop back into the site

`_src/template.html` currently lists only two `sameAs` URLs — Yelp and YouTube. That is
thin for a medical practice. Once the listings are claimed, add the real profile URLs
(Google, Apple, Facebook, Instagram, Healthgrades) to the `sameAs` array. It is how a
search engine confirms that the entity on the site and the entity in the directory are
the same business, and it is a two-minute edit that nothing else substitutes for.
