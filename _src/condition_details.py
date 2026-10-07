"""Researched condition detail pages, rendered from _src/conditions/{slug}.json.

The 14 hand-written pages in pages/cond-*.html are the practice's core conditions.
These detail pages cover the specific foot and ankle problems that had no page at
all (ingrown toenails, hammertoes, Morton's neuroma, gout, ...), each written for
a patient in Jupiter or Palm Beach Gardens rather than a national reader. That is
deliberate: the old vendor's 100+ national "how to" articles drew traffic that
never booked. These answer the search AND make the case for an exam here.

Content was researched from ACFAS, APMA, AAOS, AAD, NIH, Mayo Clinic and
Cleveland Clinic, then fact-checked claim by claim by a separate pass
(_dev/condition-pages-factcheck-log.md). Every page lists its sources.

THE REVIEW GATE. A page is built either way, but until its slug is in
CONDITION_REVIEW it is noindex, left out of sitemap.xml, and not linked from
/conditions/. Adding the doctor's name and date here is the single switch that
publishes it: indexable, in the sitemap, carded on the conditions hub, with a
visible "Reviewed by" line and reviewedBy/lastReviewed schema. That line is a
public statement that the doctor read the page, so only add it when they have.
The unlisted /conditions/review/ page lists every page with its open questions.
"""

import html
import json
from pathlib import Path

SRC = Path(__file__).resolve().parent
DATA = SRC / "conditions"
BASE = "https://jupiterlaser.com"

DOCTORS = {
    "cedeno": ("Dr. Orlando Cedeno, DPM", "/meet-dr-cedeno/"),
    "mustafa": ("Dr. Isin A. Mustafa, DPM", "/meet-dr-mustafa/"),
}

# slug -> (doctor key, "YYYY-MM-DD"). Empty until a doctor has read the page.
CONDITION_REVIEW = {
    # "ingrown-toenail": ("cedeno", "2026-10-20"),
}

# Existing pages each detail page should link to.
RELATED = {
    "hammertoes": [("/how-to-use-custom-orthotics-to-manage-hammer-toe-pain/", "Using Custom Orthotics to Manage Hammertoe Pain"),
                   ("/conditions/bunions/", "Bunions")],
    "posterior-tibial-tendon-dysfunction": [("/conditions/flat-feet/", "Flat Feet")],
    "haglunds-deformity": [("/conditions/achilles-tendonitis/", "Achilles Tendonitis"), ("/conditions/heel-pain/", "Heel Pain")],
    "stress-fractures": [("/conditions/sports-injuries/", "Sports Injuries")],
    "peroneal-tendonitis": [("/conditions/sprains-strains/", "Ankle Sprains and Strains")],
    "gout": [("/conditions/arthritis/", "Foot and Ankle Arthritis")],
    "sesamoiditis": [("/conditions/sports-injuries/", "Sports Injuries")],
    "metatarsalgia": [("/services/foot-bbl/", "Foot BBL fat pad restoration")],
    "corns-calluses": [("/conditions/diabetic-foot-care/", "Diabetic Foot Care")],
    "toenail-fungus": [("/conditions/diabetic-foot-care/", "Diabetic Foot Care")],
    "ingrown-toenail": [("/conditions/diabetic-foot-care/", "Diabetic Foot Care")],
    "mortons-neuroma": [("/conditions/neuropathy/", "Peripheral Neuropathy")],
}

e = html.escape


def load():
    out = {}
    for p in sorted(DATA.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out[d["slug"]] = d
    return out


DETAILS = load()


def live(slug):
    return slug in CONDITION_REVIEW


def _ul(items, cls="check-list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def _schema(d, url, review):
    sch = d.get("schema", {})
    cond = {
        "@type": "MedicalCondition", "@id": url + "#condition", "name": d["name"],
        "alternateName": d.get("also_called", []), "description": d["lede"],
        "signOrSymptom": [{"@type": "MedicalSignOrSymptom", "name": s} for s in sch.get("signOrSymptom", [])],
        "riskFactor": [{"@type": "MedicalRiskFactor", "name": s} for s in sch.get("riskFactor", [])],
        "possibleTreatment": [{"@type": "MedicalTherapy", "name": t} for t in sch.get("possibleTreatment", [])],
    }
    if sch.get("associatedAnatomy"):
        cond["associatedAnatomy"] = {"@type": "AnatomicalStructure", "name": sch["associatedAnatomy"]}
    if sch.get("icd10"):
        cond["code"] = {"@type": "MedicalCode", "codeValue": sch["icd10"], "codingSystem": "ICD-10"}
    page = {
        "@context": "https://schema.org", "@type": "MedicalWebPage", "@id": url + "#webpage",
        "url": url, "name": d["seo_title"], "description": d["seo_desc"],
        "about": cond, "audience": {"@type": "Patient"}, "specialty": "Podiatric",
        "isPartOf": {"@id": BASE + "/#website"}, "provider": {"@id": BASE + "/#clinic"},
        "inLanguage": "en-US",
        "citation": [{"@type": "CreativeWork", "name": s["title"], "url": s["url"]} for s in d.get("sources", [])],
    }
    if review:
        doc, when = review
        page["reviewedBy"] = {"@id": BASE + DOCTORS[doc][1] + "#physician"}
        page["lastReviewed"] = when
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": f["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in d["faqs"]]}
    return [page, faq]


def _page(d):
    slug = d["slug"]
    path = f"conditions/{slug}/"
    url = f"{BASE}/{path}"
    review = CONDITION_REVIEW.get(slug)
    meta = {
        "path": path, "title": d["seo_title"], "desc": d["seo_desc"], "nav": "conditions",
        "priority": 0.7, "crumbs": [["Conditions", "/conditions/"], [d["name"], None]],
        "schema": _schema(d, url, review),
    }
    if not review:
        meta["robots"] = "noindex, follow"
        meta["sitemap"] = False

    reviewed = ""
    if review:
        name, href = DOCTORS[review[0]]
        reviewed = f'<p class="med-note">Medically reviewed by <a href="{href}">{e(name)}</a> on {e(review[1])}.</p>'
    aka = f'<p class="med-note">Also called: {e(", ".join(d["also_called"]))}</p>' if d.get("also_called") else ""
    methods = "".join(f"<h3>{e(a)}</h3><p>{e(b)}</p>" for a, b in d["how_therapy_helps"]["methods"])
    faqs = "".join(f'<details class="faq"><summary>{e(f["q"])}</summary><div class="faq-a"><p>{e(f["a"])}</p></div></details>'
                   for f in d["faqs"])
    sources = "".join(f'<li><a href="{e(s["url"])}" rel="noopener">{e(s["title"])}</a>, {e(s.get("publisher", ""))}</li>'
                      for s in d["sources"])
    rel = RELATED.get(slug, []) + [(f"/conditions/{s}/", DETAILS[s]["name"]) for s in DETAILS
                                   if s != slug and live(s)][:3]
    rel_html = ""
    if rel:
        rel_html = ('<section class="section-tight"><div class="wrap-narrow" data-reveal>'
                    '<h2 style="font-size:1.1rem;margin-bottom:0.6rem">Related</h2><ul class="check-list">'
                    + "".join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in rel) + "</ul></div></section>")
    body = f"""
    <section class="page-hero">
      <div class="wrap">
        <ol class="crumbs">
          <li><a href="/">Home</a></li>
          <li><a href="/conditions/">Conditions</a></li>
          <li>{e(d["name"])}</li>
        </ol>
        <span class="kicker">Jupiter &amp; Palm Beach Gardens</span>
        <h1>{e(d["name"])}</h1>
        <p class="lede">{e(d["lede"])}</p>
        <div class="btn-row">
          <a class="btn btn-primary btn-lg" href="/contact/">Book Appointment</a>
          <a class="btn btn-ghost btn-lg" href="tel:+15619151934">(561) 915-1934</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap-narrow prose" data-reveal>
        {reviewed}{aka}
        <h2>{e(d["name"])}, explained</h2>
        {"".join(f"<p>{e(p)}</p>" for p in d["what_it_is"])}
        <h2>Common symptoms</h2>
        {_ul(d["symptoms"])}
        <h2>Causes and risk factors</h2>
        {_ul(d["causes"])}
        <h2>How we treat it</h2>
        <p>{e(d["how_therapy_helps"]["intro"])}</p>
        {methods}
        <h2>Your first visit</h2>
        <p>{e(d["first_visit"])}</p>
        <h2>Recovery</h2>
        <p>{e(d["recovery"])}</p>
        <h2>What you can do at home</h2>
        {_ul(d["self_care"])}
        <h2>When to get care right away</h2>
        {_ul(d["see_a_doctor"])}
      </div>
    </section>

    <section class="section section-mist">
      <div class="wrap-narrow" data-reveal>
        <h2>{e(d["name"])}: common questions</h2>
        <div class="faq-list">
          {faqs}
        </div>
      </div>
    </section>
{rel_html}
    <section class="section-tight">
      <div class="wrap-narrow prose" data-reveal>
        <h2 style="font-size:1.1rem">Sources</h2>
        <ol>{sources}</ol>
        <p class="med-note">This page is general information, not medical advice. Please see a podiatrist or your physician about your own symptoms.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="wrap">
        <div class="cta-band" data-reveal>
          <div>
            <h2>Get it looked at in Jupiter or Palm Beach Gardens</h2>
            <p>Two offices, two foot and ankle physicians. Tell us what is going on and we will find you a time.</p>
          </div>
          <div class="btn-row">
            <a class="btn btn-primary btn-lg" href="/contact/">Book Appointment</a>
            <a class="btn btn-ghost btn-lg" href="tel:+15619151934">(561) 915-1934</a>
          </div>
        </div>
      </div>
    </section>
"""
    return "<!--META\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\nMETA-->" + body


def _review_page():
    rows = []
    for slug, d in DETAILS.items():
        status = (f"Reviewed by {e(DOCTORS[CONDITION_REVIEW[slug][0]][0])} on {e(CONDITION_REVIEW[slug][1])}"
                  if live(slug) else "Waiting for a doctor (hidden from Google)")
        notes = "".join(f"<li>{e(n)}</li>" for n in d.get("notes_for_reviewer", []))
        rows.append(f'<details class="faq"><summary>{e(d["name"])} &middot; {status}</summary><div class="faq-a">'
                    f'<p><a href="/conditions/{slug}/">Open the page</a> &middot; {len(d["sources"])} sources</p>'
                    f'<p><strong>Please confirm:</strong></p><ul>{notes}</ul></div></details>')
    meta = {"path": "conditions/review/", "title": "Condition Page Review | Abacoa Podiatry",
            "desc": "Internal review list for condition pages.", "nav": "conditions",
            "robots": "noindex, nofollow", "sitemap": False}
    pending = sum(1 for s in DETAILS if not live(s))
    body = f"""
    <section class="section">
      <div class="wrap-narrow prose">
        <h1>Condition pages: doctor review</h1>
        <p>{len(DETAILS)} new condition pages are built. {pending} are waiting for review. A page stays hidden from Google and off the Conditions page until a doctor has read it.</p>
        <p>Open each page, read it as a patient handout, and check the list under its name. Send corrections to Nick. When a page is right, tell Nick which doctor reviewed it and the date; one line in the build publishes it with "Medically reviewed by" and your name.</p>
        <div class="faq-list">{"".join(rows)}</div>
      </div>
    </section>
"""
    return "<!--META\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\nMETA-->" + body


def condition_detail_pages():
    """Yield (virtual_filename, page_source) like locations.location_pages()."""
    for slug, d in DETAILS.items():
        yield f"cond-detail-{slug}.html", _page(d)
    yield "cond-detail-review.html", _review_page()


def hub_cards():
    """Cards for /conditions/, reviewed pages only."""
    cards = "".join(
        f'<article class="card card-glow" data-reveal><h3><a href="/conditions/{s}/">{e(d["name"])}</a></h3>'
        f'<p>{e(d["lede"])}</p><span class="link-arrow">Learn more</span></article>'
        for s, d in DETAILS.items() if live(s))
    return f'<div class="grid grid-2" style="margin-top:1.6rem">{cards}</div>' if cards else ""
