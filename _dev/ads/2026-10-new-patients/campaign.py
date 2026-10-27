#!/usr/bin/env python3
"""The October 2026 new-patient Search campaign, stated once.

Everything the campaign is made of lives in this file: settings, ad groups,
keywords, ads, assets and negatives. Running it checks every Google Ads limit
(30-character headlines, 90-character descriptions, 25-character callouts and
so on) and writes the files that get it into the account:

    python3 _dev/ads/2026-10-new-patients/campaign.py

    campaign.json    the whole spec, for pushing through the Windsor connector
    keywords.csv     Google Ads Editor import: positive keywords
    negatives.csv    Google Ads Editor import: campaign-level negatives
    ads.csv          Google Ads Editor import: responsive search ads
    assets.csv       sitelinks, callouts, structured snippets, call asset

Why it looks the way it does is in README.md next to this file. The short
version: in the 90 days to 2026-09-30, most of the account's visible spend went
to people searching for a different provider (a hospital, a competitor, a
physical therapist, an orthopedic group that takes Medicaid). This campaign
only buys searches from people looking for a podiatrist or naming a foot
problem, sends each to the page that answers it, and sells the practice as a
whole: two board-certified foot & ankle surgeons, Dr. Orlando Cedeno and
Dr. Isin Mustafa, who can usually see a new patient within the week.

Every claim in the ad copy is one the site already makes, on the landing page
the ad points at. If the site changes, check the copy here against it.
"""

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "https://jupiterlaser.com"
PHONE = "(561) 915-1934"

CAMPAIGN = {
    "name": "NP | Search | New Patients | N. Palm Beach",
    "channel": "search",
    "networks": "Google Search only (no Search Partners, no Display)",
    "status": "paused",
    "daily_budget": 85.00,
    # Maximize Clicks with a ceiling until the account counts website leads.
    # Today the only primary conversion is a tap on the ad's call button, and
    # over half of those came from people looking for someone else. Switching
    # to Maximize Conversions before that is fixed teaches the bidder to chase
    # "jupiter medical center" again. See README.md, "Bidding".
    "bidding": {"strategy": "target_spend", "cpc_bid_ceiling": 9.00,
                "switch_to": "maximize_conversions",
                "switch_when": "30+ conversions from the cleaned set (website "
                               "call_click + form_submit imported from GA4, "
                               "ad calls of 90s or longer)"},
    # Presence only. The account currently also pays for people out of state
    # (New York, Philadelphia and others: $245 in 90 days).
    "location_option": "PRESENCE",
    # Named places rather than a radius. The areas that produced calls at
    # $30-39 each run north to Stuart and Palm City (~23 mi from the Jupiter
    # office), while Wellington and Greenacres, which cost $52-53, sit ~18 mi
    # south-west -- no single circle takes one without the other.
    # IDs are Google Ads geo target constants from geotargets-2026-08-12.csv.
    "geo": {
        "targets": [
            (1015072, "Jupiter"), (9052966, "Tequesta"),
            (9190942, "Jupiter Island"), (9052212, "Juno Beach"),
            (9052625, "Palm Beach Gardens"), (1015139, "North Palm Beach"),
            (9194272, "Lake Park"), (9052756, "Riviera Beach"),
            (9052626, "Palm Beach Shores"), (1015052, "Hobe Sound"),
            (9052702, "Port Salerno"), (1015208, "Stuart"),
            (1015159, "Palm City"), (9192318, "Sewall's Point"),
            (1015229, "West Palm Beach"), (1015158, "Palm Beach"),
            # Jupiter ZIPs, for unincorporated Jupiter Farms and the edges of
            # Tequesta that the city targets don't cover.
            (9012031, "33458"), (9012038, "33469"),
            (9012044, "33477"), (9012045, "33478"),
        ],
        "excluded": [],
    },
    "languages": ["en"],
    # Office hours from _src/hours.py: Jupiter Mon-Thu 8-5, Fri 8-2. Starting an
    # hour early catches people searching before they call at 8. Weekends are
    # off: $1,002 of weekend spend produced 9 calls ($111 each) against $36 on
    # weekdays, because nobody answers the phone.
    "ad_schedule": [
        {"day": d, "start": "07:00", "end": "17:00"}
        for d in ("MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY")
    ] + [{"day": "FRIDAY", "start": "07:00", "end": "14:00"}],
}

LP = "/see-a-podiatrist-this-week/"

# Each ad group: one intent, one landing page that answers it, phrase and exact
# match only. No broad match anywhere -- the three broad keywords in the current
# account ("podiatrist jupiter", "dr cedeno jupiter", "orthopedic that takes
# medicaid near me") spent $4,650 in 90 days, 37% of the whole account.
AD_GROUPS = [
    {
        "name": "Podiatrist - Local",
        "final_url": SITE + LP,
        "path": ("Podiatrist", "This-Week"),
        "max_cpc": 8.00,
        "keywords": {
            "phrase": [
                "podiatrist jupiter", "podiatrist in jupiter", "jupiter podiatrist",
                "podiatrist palm beach gardens", "podiatrist in palm beach gardens",
                "podiatrist north palm beach", "podiatrist tequesta",
                "podiatrist juno beach", "podiatrist hobe sound",
                "foot doctor jupiter", "foot doctor palm beach gardens",
                "foot and ankle doctor jupiter", "foot and ankle specialist jupiter",
                "podiatrist accepting new patients", "female podiatrist",
                "woman podiatrist", "podiatrist that takes medicare",
                "medicare podiatrist",
            ],
            "exact": [
                "podiatrist near me", "foot doctor near me", "podiatry near me",
                "foot specialist near me", "foot and ankle specialist near me",
                "podiatrist jupiter fl", "podiatrist jupiter florida",
                "best podiatrist near me",
            ],
        },
        "headlines": [
            "Podiatrist in Jupiter, FL", "Foot & Ankle Doctor Near You",
            "Abacoa Podiatry & Vein", "Two Board-Certified Surgeons",
            "Dr. Cedeno & Dr. Mustafa", "Most Seen Within the Week",
            "Accepting New Patients", "Medicare & Most Major Plans",
            "Jupiter & Palm Beach Gardens", "Rated 4.9 on Google",
            "Call " + PHONE, "Book Your Foot Exam Today",
            "Most Need No Referral", "Heel, Bunion & Ankle Care",
            "Laser & Regenerative Options",
        ],
        "descriptions": [
            "Board-certified foot & ankle surgeons Dr. Orlando Cedeno and Dr. Isin Mustafa.",
            "Most new patients are seen within the week. Heel pain, bunions, injuries & more.",
            "Medicare, Aetna, BCBS, Cigna & UHC. We verify your plan before your first visit.",
            "Offices in Jupiter on Military Trail and Palm Beach Gardens. Call or book online.",
        ],
    },
    {
        "name": "Bunions - MIS",
        "final_url": SITE + "/minimally-invasive-bunion-surgery/",
        "path": ("Bunion", "Surgery"),
        "max_cpc": 9.00,
        "keywords": {
            "phrase": [
                "bunion surgery", "minimally invasive bunion surgery",
                "mis bunion surgery", "keyhole bunion surgery", "bunion surgeon",
                "bunion doctor", "bunion specialist", "bunion treatment near me",
                "bunion removal", "bunionectomy", "tailors bunion surgery",
                "hallux valgus surgery", "bunion correction",
            ],
            "exact": ["bunion doctor near me", "bunion surgeon near me"],
        },
        "headlines": [
            "Minimally Invasive Bunions", "Bunion Surgery in Jupiter",
            "Smaller Incisions", "Two Board-Certified Surgeons",
            "Dr. Cedeno & Dr. Mustafa", "Reconstructive Foot Surgeons",
            "Book a Bunion Evaluation", "Every Option Under One Roof",
            "Least Invasive Option First", "Medicare & Most Major Plans",
            "Jupiter & Palm Beach Gardens", "Rated 4.9 on Google",
            "Lapidus & Revision Options", "Call " + PHONE,
            "Bunion Pain Treatment",
        ],
        "descriptions": [
            "Minimally invasive bunion surgery uses far smaller incisions than traditional surgery.",
            "Two board-certified surgeons: Dr. Cedeno (FACFAS) and Dr. Mustafa, who focuses on MIS.",
            "We review your X-rays and recommend the least invasive operation that will hold.",
            "Conservative care, MIS, Lapidus & revision surgery. Book your bunion evaluation.",
        ],
    },
    {
        "name": "Heel Pain - Plantar Fasciitis",
        "final_url": SITE + "/conditions/plantar-fasciitis/",
        "path": ("Heel-Pain", "Treatment"),
        "max_cpc": 8.00,
        "keywords": {
            "phrase": [
                "plantar fasciitis doctor", "plantar fasciitis specialist",
                "plantar fasciitis treatment near me", "heel pain doctor",
                "heel pain specialist", "heel pain treatment near me",
                "heel spur doctor", "heel spur treatment",
                "plantar fasciitis podiatrist", "shockwave therapy plantar fasciitis",
                "prp for plantar fasciitis", "plantar fasciitis injection near me",
            ],
            "exact": ["plantar fasciitis doctor near me", "heel pain doctor near me"],
        },
        "headlines": [
            "Plantar Fasciitis Treatment", "Heel Pain Doctor in Jupiter",
            "Heel Pain Specialists", "Most Seen Within the Week",
            "Board-Certified Foot Surgeons", "Shockwave, Laser & PRP",
            "Orthotics When You Need Them", "Medicare & Most Major Plans",
            "Jupiter & Palm Beach Gardens", "Rated 4.9 on Google",
            "Call " + PHONE, "Diagnosis at Your First Visit",
            "Dr. Cedeno & Dr. Mustafa", "Heel Spur Treatment",
            "Laser & Regenerative Care",
        ],
        "descriptions": [
            "Heel pain that won't quit? Get a diagnosis and a treatment plan at your first visit.",
            "From stretching plans & orthotics to shockwave, laser and PRP when you need more.",
            "Board-certified foot & ankle surgeons. Most new patients are seen within the week.",
            "Medicare, Aetna, BCBS, Cigna & UHC accepted. Jupiter & Palm Beach Gardens offices.",
        ],
    },
    {
        "name": "Ingrown Toenails",
        "final_url": SITE + LP,
        "path": ("Podiatrist", "Ingrown-Nail"),
        "max_cpc": 7.00,
        "keywords": {
            "phrase": [
                "ingrown toenail doctor", "ingrown toenail removal",
                "ingrown toenail podiatrist", "ingrown toenail treatment near me",
                "podiatrist for ingrown toenail", "infected ingrown toenail doctor",
                "toenail removal near me",
            ],
            "exact": ["ingrown toenail doctor near me", "ingrown toenail removal near me"],
        },
        "headlines": [
            "Ingrown Toenail Treatment", "Ingrown Toenail Doctor",
            "Podiatrist in Jupiter, FL", "Most Seen Within the Week",
            "Board-Certified Podiatrists", "Medicare & Most Major Plans",
            "Jupiter & Palm Beach Gardens", "Rated 4.9 on Google",
            "Call " + PHONE, "Dr. Cedeno & Dr. Mustafa",
            "Toenail Problems Treated", "Accepting New Patients",
            "Book Online or Call Today", "Abacoa Podiatry & Vein",
            "Most Need No Referral",
        ],
        "descriptions": [
            "Painful ingrown toenail? Board-certified podiatrists in Jupiter & Palm Beach Gardens.",
            "Most new patients are seen within the week. Call or request an appointment online.",
            "Medicare, Aetna, BCBS, Cigna & UHC accepted. We verify your plan before you come.",
            "Abacoa Podiatry & Leg Vein Center: two board-certified foot & ankle surgeons.",
        ],
    },
    {
        "name": "Injuries - Ankle & Sports",
        "final_url": SITE + "/conditions/sprains-strains/",
        "path": ("Ankle", "Injury"),
        "max_cpc": 8.00,
        "keywords": {
            "phrase": [
                "ankle sprain doctor", "sprained ankle doctor", "ankle injury doctor",
                "foot injury doctor", "sprained ankle treatment near me",
                "achilles tendonitis doctor", "achilles tendon specialist",
                "sports podiatrist", "broken toe doctor", "foot fracture doctor",
            ],
            "exact": ["ankle doctor near me", "sprained ankle doctor near me"],
        },
        "headlines": [
            "Ankle Sprain Treatment", "Foot & Ankle Injury Doctor",
            "Sports Foot & Ankle Care", "Acute Injuries Prioritized",
            "Two Board-Certified Surgeons", "Trauma-Trained Foot Surgeon",
            "Achilles & Tendon Injuries", "Same-Day Imaging if Needed",
            "Medicare & Most Major Plans", "Jupiter & Palm Beach Gardens",
            "Rated 4.9 on Google", "Call " + PHONE,
            "Accepting New Patients", "Rule Out Hidden Fractures",
            "Heal It Right the First Time",
        ],
        "descriptions": [
            "Rolled your ankle or hurt your foot? Acute injuries get priority scheduling.",
            "Board-certified foot & ankle surgeons. Same-day imaging when the exam calls for it.",
            "Sprains, tendon injuries & sports injuries treated in Jupiter & Palm Beach Gardens.",
            "Medicare, Aetna, BCBS, Cigna & UHC accepted. Call or request an appointment online.",
        ],
    },
    {
        "name": "Diabetic Foot & Neuropathy",
        "final_url": SITE + "/conditions/diabetic-foot-care/",
        "path": ("Diabetic", "Foot-Care"),
        "max_cpc": 7.00,
        "keywords": {
            "phrase": [
                "diabetic foot doctor", "diabetic podiatrist", "diabetic foot care",
                "diabetic foot exam", "diabetic foot ulcer treatment",
                "foot wound care", "wound care podiatrist",
                "neuropathy foot doctor", "foot neuropathy treatment",
                "peripheral neuropathy podiatrist",
            ],
            "exact": ["diabetic foot doctor near me", "neuropathy doctor near me"],
        },
        "headlines": [
            "Diabetic Foot Care", "Diabetic Foot Doctor",
            "Wound Care Podiatrist", "Neuropathy Foot Treatment",
            "Medicare Accepted", "Most Seen Within the Week",
            "Board-Certified Podiatrists", "Board-Certified in Wound Care",
            "Jupiter & Palm Beach Gardens", "Rated 4.9 on Google",
            "Call " + PHONE, "Diabetic Foot Exams",
            "Foot Ulcer & Wound Care", "Accepting New Patients",
            "Drug-Free Laser for Neuropathy",
        ],
        "descriptions": [
            "Diabetic foot exams, wound care and neuropathy care from board-certified podiatrists.",
            "Dr. Cedeno is board certified in wound care and focuses on diabetic limb preservation.",
            "Medicare & most major plans accepted. We verify your benefits before your first visit.",
            "Offices in Jupiter and Palm Beach Gardens. Call " + PHONE + " or book online.",
        ],
    },
]

# Brand campaign changes, applied to the existing "Brand" campaign rather than
# the new one. Brand already has a "Dr. Cedeno" ad group (its broad keyword is
# tightened in README step 2); patients who search Dr. Mustafa by name have no
# ad group of their own today ("isin mustafa dpm" gets organic clicks at 44%
# CTR), so she gets one alongside it.
BRAND_MUSTAFA_AD_GROUP = {
    "campaign": "Brand",
    "name": "Dr. Mustafa",
    "final_url": SITE + "/meet-dr-mustafa/",
    "path": ("Dr-Mustafa", None),
    "max_cpc": 3.00,
    "keywords": {
        "phrase": ["isin mustafa", "dr isin mustafa", "mustafa podiatrist",
                   "dr mustafa podiatrist", "mustafa dpm", "dr mustafa jupiter"],
        "exact": ["dr mustafa", "isin mustafa dpm"],
    },
    "headlines": [
        "Dr. Isin Mustafa, DPM", "Board-Certified Foot Surgeon",
        "Accepting New Patients", "Most Seen Within the Week",
        "Minimally Invasive Surgeon", "Abacoa Podiatry & Vein",
        "Jupiter & Palm Beach Gardens", "Medicare & Most Major Plans",
        "Call " + PHONE, "Book With Dr. Mustafa",
        "Rated 4.9 on Google", "Former Chief Resident",
    ],
    "descriptions": [
        "Foot & ankle surgeon focused on minimally invasive surgery and regenerative medicine.",
        "Board certified by the American Board of Foot and Ankle Surgery. Accepting new patients.",
        "Bunions, wound care, sports injuries & orthotics. Most new patients seen within the week.",
    ],
}

ASSETS = {
    "callouts": [
        "Most Seen Within a Week", "Medicare & Major Plans",
        "Most Need No Referral", "Board-Certified Surgeons",
        "Free On-Site Parking", "Jupiter & PBG Offices",
        "Rated 4.9 on Google", "Accepting New Patients",
    ],
    "sitelinks": [
        ("Meet Dr. Cedeno", "/meet-dr-cedeno/",
         "Board-certified foot surgeon", "Laser, regenerative & wound care"),
        ("Meet Dr. Mustafa", "/meet-dr-mustafa/",
         "Board-certified foot surgeon", "Minimally invasive & regenerative"),
        ("Insurance We Accept", "/insurance/",
         "Medicare, Aetna, BCBS, Cigna, UHC", "We verify your plan before you come"),
        ("MIS Bunion Surgery", "/minimally-invasive-bunion-surgery/",
         "Smaller incisions", "Two board-certified surgeons"),
        ("Heel Pain Treatment", "/conditions/plantar-fasciitis/",
         "Plantar fasciitis & heel spurs", "Shockwave, laser, PRP & orthotics"),
        ("Your First Visit", "/new-patients/",
         "What to bring, what to expect", "Plan about 45 to 60 minutes"),
        ("Request an Appointment", "/contact/",
         "Send a request in a minute", "We call you back to schedule"),
    ],
    "structured_snippet": {
        "header": "Services",
        "values": ["Bunion Surgery", "Heel Pain", "Ingrown Toenails",
                   "Sports Injuries", "Diabetic Foot Care", "Wound Care",
                   "Neuropathy"],
    },
    "call": {"phone": PHONE, "country": "US",
             "schedule": "match campaign ad schedule"},
}

# Negatives, by the reason they exist. Each group is one row of the audit:
# the search terms that cost money in the 90 days to 2026-09-30 while looking
# for something this practice is not. Phrase match unless noted.
NEGATIVES = {
    "hospitals_and_other_clinics": [
        "jupiter medical center", "jupiter medical", "jfk hospital", "jfk medical",
        "good samaritan", "good sam", "st marys", "st mary's",
        "palm beach gardens medical center", "palm beach garden hospital",
        "cleveland clinic", "mount sinai", "wellington regional", "hhs hospital",
        "hospital", "conviva", "cano health", "mycare", "my care medical",
        "la medical", "my clinic", "health care district", "jupiter west medical",
        "evolve health", "urgent care center", "walk in clinic", "primary care",
    ],
    "physical_therapy": [
        "physical therapy", "physical therapist", "physiotherapy", "saylor",
        "bend physical", "gold coast physical", "action physical",
        "elite physical", "life motion",
    ],
    "orthopedic_groups_and_other_specialties": [
        "pboi", "palm beach orthopedic", "palm beach orthopaedic",
        "orthopedic institute", "paley", "bone and joint", "bone & joint",
        "southflaortho", "coastal orthopedics", "knee", "hip", "shoulder",
        "spine", "back pain", "hand surgeon", "wrist",
    ],
    # The practice's insurance list (/insurance/) has no Medicaid plan.
    # "orthopedic that takes medicaid near me" alone spent $1,156.
    "insurance_not_accepted": ["medicaid", "sunshine health", "simply healthcare"],
    "competitor_practices": [
        "south florida foot", "palm beach foot and ankle", "pga foot",
        "shoppe foot", "schoppe", "taub podiatry", "dr taub", "luxe podiatry",
        "family foot center", "hall podiatry", "treasure coast podiatry",
        "signature foot", "la podiatry", "certified foot and ankle specialists",
        "ankle and foot center of florida", "advanced foot and ankle",
        "modern foot and ankle", "mattison podiatry", "florida foot and ankle center",
    ],
    "competitor_doctors": [
        "dr fried", "dr vena", "dr lamm", "dr prager", "dr perkins", "dr pan",
        "dr spinner", "dr selbst", "dr hartstein", "alan hartstein", "nemeroff",
        "ostapchuk", "dr daly", "joshua daly", "elgut", "lapoff", "lepoff",
        "montijo", "gerszberg", "breslauer", "harlis", "jonathan cutler",
        "nina solomon", "michael sturm", "matthew wolfson", "khoa pham",
        "gary ackerman", "dr sater", "dr yee", "fishman", "wexler",
        "andrew noble", "paul weiner", "andrew lerner", "dana desser",
        "christopher boyes", "lopez viego", "garrett nguyen", "ashley bowles",
        "tiffany cerda", "desiree garzon", "taylor tendrich", "craig paul",
    ],
    "do_it_yourself_and_research": [
        "how to", "what is", "what causes", "why does", "why do", "home remedy",
        "home remedies", "cure", "instantly", "overnight", "cream", "ointment",
        "over the counter", "otc", "essential oil", "apple cider vinegar",
        "vicks", "epsom", "exercises", "stretches", "taping", "insoles",
        "shoes", "sandals", "socks", "pedicure", "nail salon", "reddit",
        "youtube", "pictures", "images", "icd 10", "cpt code", "symptoms",
    ],
    "jobs_and_education": [
        "jobs", "job", "career", "salary", "hiring", "school", "residency",
        "assistant", "technician",
    ],
    "animals": ["dog", "cat", "vet", "horse", "hoof", "farrier"],
    "outside_service_area": [
        "port st lucie", "boca raton", "boynton", "delray", "lake worth",
        "wellington", "royal palm beach", "greenacres", "fort lauderdale",
        "miami", "orlando fl", "tampa",
    ],
    # The practice treats veins, but under its own campaign and page. Vein
    # searches matched to a podiatry ad group land on the wrong page.
    "veins_belong_elsewhere": [
        "vein", "veins", "varicose", "spider vein", "sclerotherapy",
        "lymphedema", "vascular",
    ],
}

# Which negative groups also go on the existing campaigns right away, before
# the new campaign launches. These are the ones with no plausible patient on
# the other side. Competitor names are excluded here because Brand has a
# deliberate "Competitors" ad group -- pause that ad group instead (README).
SHARED_NEGATIVE_GROUPS = [
    "hospitals_and_other_clinics", "physical_therapy",
    "orthopedic_groups_and_other_specialties", "insurance_not_accepted",
    "do_it_yourself_and_research", "jobs_and_education", "animals",
    "outside_service_area",
]

LIMITS = {"headline": 30, "description": 90, "path": 15, "callout": 25,
          "sitelink_text": 25, "sitelink_desc": 35, "snippet_value": 25}


def check():
    errors = []

    def lim(kind, text, where):
        if len(text) > LIMITS[kind]:
            errors.append(f"{where}: {kind} is {len(text)} chars (max "
                          f"{LIMITS[kind]}): {text!r}")

    for ag in AD_GROUPS + [BRAND_MUSTAFA_AD_GROUP]:
        where = ag["name"]
        hs, ds = ag["headlines"], ag["descriptions"]
        if not 3 <= len(hs) <= 15:
            errors.append(f"{where}: {len(hs)} headlines (3-15)")
        if not 2 <= len(ds) <= 4:
            errors.append(f"{where}: {len(ds)} descriptions (2-4)")
        if len(set(h.lower() for h in hs)) != len(hs):
            errors.append(f"{where}: duplicate headline")
        for h in hs:
            lim("headline", h, where)
        for d in ds:
            lim("description", d, where)
        for p in ag["path"]:
            if p:
                lim("path", p, where)
        kws = ag["keywords"]["phrase"] + ag["keywords"]["exact"]
        if len(set(kws)) != len(kws):
            errors.append(f"{where}: duplicate keyword")
    for c in ASSETS["callouts"]:
        lim("callout", c, "callout")
    for text, _, d1, d2 in ASSETS["sitelinks"]:
        lim("sitelink_text", text, "sitelink")
        lim("sitelink_desc", d1, f"sitelink {text}")
        lim("sitelink_desc", d2, f"sitelink {text}")
    for v in ASSETS["structured_snippet"]["values"]:
        lim("snippet_value", v, "snippet")

    # A negative must never block a keyword we are buying.
    positives = [k for ag in AD_GROUPS
                 for k in ag["keywords"]["phrase"] + ag["keywords"]["exact"]]
    for group, words in NEGATIVES.items():
        for n in words:
            for p in positives:
                if f" {n} " in f" {p} ":
                    errors.append(f"negative {n!r} ({group}) blocks keyword {p!r}")
    return errors


def write_outputs():
    camp = CAMPAIGN["name"]
    with open(HERE / "keywords.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Ad Group", "Keyword", "Criterion Type",
                    "Max CPC", "Final URL"])
        for ag in AD_GROUPS:
            for mt in ("phrase", "exact"):
                for k in ag["keywords"][mt]:
                    w.writerow([camp, ag["name"], k, mt.title(),
                                f"{ag['max_cpc']:.2f}", ag["final_url"]])
        b = BRAND_MUSTAFA_AD_GROUP
        for mt in ("phrase", "exact"):
            for k in b["keywords"][mt]:
                w.writerow([b["campaign"], b["name"], k, mt.title(),
                            f"{b['max_cpc']:.2f}", b["final_url"]])

    with open(HERE / "negatives.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Keyword", "Criterion Type", "Reason"])
        for group, words in NEGATIVES.items():
            for n in words:
                w.writerow([camp, n, "Campaign Negative Phrase", group])
        for existing in ("Clinic", "Doctor", "Brand"):
            for group in SHARED_NEGATIVE_GROUPS:
                for n in NEGATIVES[group]:
                    w.writerow([existing, n, "Campaign Negative Phrase", group])

    with open(HERE / "ads.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Ad Group", "Ad type"]
                   + [f"Headline {i}" for i in range(1, 16)]
                   + [f"Description {i}" for i in range(1, 5)]
                   + ["Final URL", "Path 1", "Path 2"])
        for ag in AD_GROUPS + [BRAND_MUSTAFA_AD_GROUP]:
            c = ag.get("campaign", camp)
            hs = ag["headlines"] + [""] * (15 - len(ag["headlines"]))
            ds = ag["descriptions"] + [""] * (4 - len(ag["descriptions"]))
            w.writerow([c, ag["name"], "Responsive search ad"] + hs + ds
                       + [ag["final_url"], ag["path"][0] or "", ag["path"][1] or ""])

    with open(HERE / "assets.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Campaign", "Asset type", "Text", "Final URL",
                    "Description 1", "Description 2"])
        for c in ASSETS["callouts"]:
            w.writerow([camp, "Callout", c, "", "", ""])
        for text, path, d1, d2 in ASSETS["sitelinks"]:
            w.writerow([camp, "Sitelink", text, SITE + path, d1, d2])
        sn = ASSETS["structured_snippet"]
        w.writerow([camp, "Structured snippet", sn["header"] + ": "
                    + "; ".join(sn["values"]), "", "", ""])
        w.writerow([camp, "Call", PHONE, "", "Office hours only", ""])

    spec = {"campaign": CAMPAIGN, "ad_groups": AD_GROUPS,
            "brand_mustafa_ad_group": BRAND_MUSTAFA_AD_GROUP,
            "assets": ASSETS, "negatives": NEGATIVES,
            "shared_negative_groups": SHARED_NEGATIVE_GROUPS}
    (HERE / "campaign.json").write_text(json.dumps(spec, indent=2) + "\n")


def main():
    errors = check()
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s); nothing written.")
    write_outputs()
    n_kw = sum(len(ag["keywords"]["phrase"]) + len(ag["keywords"]["exact"])
               for ag in AD_GROUPS)
    n_neg = sum(len(v) for v in NEGATIVES.values())
    print(f"OK: {len(AD_GROUPS)} ad groups, {n_kw} keywords, "
          f"{n_neg} campaign negatives, all limits pass. Files written.")


if __name__ == "__main__":
    main()
