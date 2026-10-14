"""Patient glossary: podiatry and vein terms, stated once.

The /glossary/ page and its DefinedTermSet JSON-LD are both rendered from TERMS,
so the structured data can never describe a term the page does not show
(Google's rule for every kind of markup, and the agency's).

Each entry: (term, plain-language definition, related page path or None,
             alternate names).

Rules for adding a term:
  * Define it in plain English a patient can act on. General medical meaning
    only; nothing here is a claim about this practice (no outcomes, no numbers
    that are not on the linked page or from an official source).
  * Link it to the page on this site that covers it, or None.
  * No em dashes. preflight.py checks the built page.
"""
import html
import re

TERMS = [
    ("Achilles tendinitis",
     "Irritation and pain in the Achilles tendon, the thick cord that joins the calf muscles to the back of the heel. It is usually caused by overuse and is often worst with the first steps of the day.",
     "/conditions/achilles-tendonitis/", ["Achilles tendonitis"]),
    ("Achilles tendinosis",
     "Long-standing wear inside the Achilles tendon, where the tissue has started to break down rather than heal. It tends to need treatment that restarts healing, not just rest.",
     "/is-your-achilles-tendon-pain-due-to-tendonitis-or-tendinosis/", []),
    ("Ankle sprain",
     "A stretch or tear of the ligaments that hold the ankle bones together, usually from rolling the foot inward. A sprain that keeps giving way or swelling weeks later should be examined.",
     "/conditions/sprains-strains/", []),
    ("Board certified (podiatry)",
     "A podiatrist who has passed the examinations of a recognized specialty board, such as the American Board of Foot and Ankle Surgery (ABFAS) or the American Board of Podiatric Medicine (ABPM).",
     "/about/", []),
    ("Bunion",
     "A bony bump at the base of the big toe that forms when the big toe drifts toward the second toe and the joint behind it pushes outward. The medical name is hallux valgus.",
     "/conditions/bunions/", ["Hallux valgus"]),
    ("Bunionectomy",
     "Surgery to correct a bunion. Most modern procedures realign the bone behind the big toe rather than only shaving the bump.",
     "/types-of-bunion-surgery-which-procedure-is-right-for-you/", ["Bunion surgery"]),
    ("Chronic venous insufficiency",
     "A condition in which the one-way valves inside the leg veins stop closing properly, so blood pools in the lower leg. It causes swelling, aching, varicose veins and skin changes near the ankle.",
     "/conditions/venous-insufficiency/", ["Venous insufficiency", "CVI"]),
    ("Compression stockings",
     "Elastic stockings that squeeze the leg most at the ankle and less higher up, helping blood move back toward the heart. They are often prescribed with or after vein treatment.",
     "/services/vein-treatment/", []),
    ("Custom orthotics",
     "Shoe inserts made from a mold or scan of your own feet to support or redistribute pressure. They differ from store-bought insoles, which are made to fit an average foot.",
     "/conditions/flat-feet/", ["Orthotics"]),
    ("Debridement",
     "Removing dead or unhealthy tissue from a wound so the healthy tissue underneath can heal.",
     "/services/wound-care/", []),
    ("Deep vein thrombosis (DVT)",
     "A blood clot in a deep vein, usually in the leg. A painful, swollen, warm leg, especially on one side, needs urgent medical care, because a clot can travel to the lungs.",
     None, ["DVT"]),
    ("Diabetic foot ulcer",
     "An open sore on the foot of a person with diabetes, often on the sole, that can go unnoticed when nerve damage has dulled sensation. Any wound on a diabetic foot should be seen promptly.",
     "/conditions/diabetic-foot-care/", []),
    ("DPM (Doctor of Podiatric Medicine)",
     "The medical degree held by podiatrists, who diagnose and treat conditions of the foot, ankle and lower leg, both with and without surgery.",
     "/about/", ["Podiatrist", "Doctor of Podiatric Medicine"]),
    ("Duplex ultrasound",
     "A painless scan that shows the veins and the direction blood is flowing in them. It is the standard test for mapping which veins are leaking before vein treatment.",
     "/conditions/venous-insufficiency/", []),
    ("Endovenous laser treatment (EVLT)",
     "A minimally invasive vein procedure in which a thin laser fiber is placed inside a faulty vein through a needle puncture and used to seal it closed. Blood then reroutes through healthy veins.",
     "/how-endovenous-laser-therapy-evlt-works-a-comprehensive-overview/", ["EVLT", "Endovenous laser ablation"]),
    ("Fat pad atrophy",
     "Thinning of the natural cushions under the heel and the ball of the foot, which can make standing on hard floors feel like walking on bone.",
     "/services/foot-bbl/", []),
    ("First MTP joint",
     "The joint at the base of the big toe, where the first metatarsal meets the toe. It is the joint involved in bunions and in big toe arthritis (hallux rigidus).",
     "/best-guide-to-first-metatarsophalangeal-joint-arthritis/", ["First metatarsophalangeal joint", "Big toe joint"]),
    ("Flatfoot",
     "A foot whose arch is low or collapses when standing. Many flat feet cause no trouble; some cause arch, ankle or Achilles pain and benefit from support or treatment.",
     "/conditions/flat-feet/", ["Flat feet", "Pes planus"]),
    ("Hallux rigidus",
     "Arthritis of the big toe joint that makes the toe stiff and painful to bend, especially when pushing off to walk.",
     "/best-guide-to-first-metatarsophalangeal-joint-arthritis/", ["Big toe arthritis"]),
    ("Hammertoe",
     "A toe that bends downward at the middle joint, so the top of the toe rubs on shoes. It can be flexible early on and become rigid over time.",
     "/how-to-use-custom-orthotics-to-manage-hammer-toe-pain/", ["Hammer toe"]),
    ("Heel spur",
     "A small calcium deposit on the underside of the heel bone, seen on X-ray. Many people have one without pain; heel pain usually comes from the soft tissue around it.",
     "/conditions/heel-pain/", []),
    ("High ankle sprain",
     "An injury to the ligaments that hold the two lower leg bones together just above the ankle. It usually takes longer to recover from than a common ankle sprain.",
     "/high-ankle-injury-symptoms-what-to-watch-for-early/", ["Syndesmotic sprain"]),
    ("Loss of protective sensation",
     "Reduced feeling in the feet, usually from nerve damage, to the point where a person may not notice a blister, cut or pressure sore. It is checked with a simple monofilament test.",
     "/conditions/diabetic-foot-care/", ["LOPS"]),
    ("Microphlebectomy",
     "Removal of bulging surface varicose veins through tiny skin nicks, usually under local anesthetic.",
     None, ["Ambulatory phlebectomy"]),
    ("Minimally invasive bunion surgery",
     "Bunion correction performed through several small incisions with guidance from live X-ray, instead of one long incision.",
     "/minimally-invasive-bunion-surgery/", ["MIS bunion surgery"]),
    ("MLS laser therapy",
     "A treatment that uses a robotic, dual-wavelength laser on the skin over an injured area to reduce pain and inflammation. Sessions are short and painless.",
     "/services/mls-laser-therapy/", ["Multiwave Locked System laser"]),
    ("Monofilament test",
     "A quick foot exam in which a thin nylon filament is pressed against several spots on the sole to check whether protective sensation is still present.",
     "/conditions/diabetic-foot-care/", []),
    ("Morton's neuroma",
     "A thickened, irritated nerve between two toes, most often the third and fourth, causing burning or the feeling of a pebble in the shoe.",
     None, ["Neuroma"]),
    ("Offloading",
     "Taking pressure off a wound or injured area of the foot with special boots, padding, casts or footwear so it can heal.",
     "/services/wound-care/", []),
    ("Peripheral neuropathy",
     "Damage to the nerves outside the brain and spinal cord, which in the feet causes burning, tingling, numbness or pain. Diabetes is the most common cause.",
     "/conditions/neuropathy/", ["Neuropathy", "Diabetic neuropathy"]),
    ("Plantar fascia",
     "The thick band of tissue under the foot that runs from the heel to the toes and supports the arch.",
     "/conditions/plantar-fasciitis/", []),
    ("Plantar fasciitis",
     "Pain where the plantar fascia attaches to the heel, classically sharpest with the first steps in the morning or after sitting. It is the most common cause of heel pain.",
     "/conditions/plantar-fasciitis/", []),
    ("Plantar wart",
     "A wart on the sole of the foot caused by a virus (HPV). Pressure from walking pushes it inward, which is why it can hurt like a stone in the shoe.",
     "/conditions/plantar-warts/", ["Verruca plantaris", "Verruca"]),
    ("Platelet-rich plasma (PRP)",
     "A concentrate made from a small sample of your own blood, spun to collect the platelets, and injected into an injured tendon, ligament or fascia to support healing.",
     "/services/prp-therapy/", ["PRP"]),
    ("Radiofrequency ablation (RFA)",
     "A minimally invasive vein procedure that uses radiofrequency heat delivered through a thin catheter to seal a leaking vein closed.",
     "/services/vein-treatment/", ["RFA", "Radiofrequency vein ablation"]),
    ("Regenerative medicine",
     "Treatments aimed at helping damaged tissue repair itself, rather than only masking pain. In foot and ankle care this includes laser, shockwave and PRP.",
     "/services/regenerative-medicine/", []),
    ("Routine foot care (Medicare)",
     "Medicare's term for nail trimming, corn and callus removal, and hygienic care. Medicare usually does not cover it, with exceptions for certain medical conditions.",
     "/insurance/#medicare", []),
    ("Sclerotherapy",
     "Injection of a medicine into spider veins or small varicose veins that makes them close and fade over the following weeks.",
     "/services/vein-treatment/", []),
    ("Shockwave therapy (EPAT)",
     "A non-invasive treatment that sends acoustic pressure waves into a chronically injured tendon or fascia to restart the body's healing response.",
     "/services/shockwave-therapy/", ["EPAT", "ESWT", "Extracorporeal shockwave therapy"]),
    ("Spider veins",
     "Small red, blue or purple veins that sit flat under the skin in web-like clusters. They are usually painless; sometimes they signal a leaking vein underneath.",
     "/services/vein-treatment/", ["Telangiectasia"]),
    ("Therapeutic shoes (Medicare)",
     "Extra-depth or custom-molded shoes and inserts that Medicare Part B can cover once a year for people with diabetes and severe diabetic foot disease, when the required doctors certify and order them.",
     "/insurance/#medicare", ["Diabetic shoes"]),
    ("Varicose veins",
     "Enlarged, twisted veins that bulge above the skin, usually on the legs. They often ache or throb and are a common sign of venous insufficiency.",
     "/services/vein-treatment/", []),
    ("Vein ligation",
     "A surgical procedure that ties off a faulty vein so blood reroutes through healthy veins.",
     "/the-role-of-vein-ligation-in-treating-severe-varicose-veins/", []),
]

TERMS = sorted(TERMS, key=lambda t: t[0].lower())


def slug(term):
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def html_list():
    """The visible glossary: A-Z jump links, then one <dl> per letter."""
    letters = []
    for term, *_ in TERMS:
        ch = term[0].upper()
        if ch not in letters:
            letters.append(ch)
    out = ['<nav class="glossary-az" aria-label="Glossary letters"><ul class="city-links">']
    out += [f'<li><a href="#letter-{c.lower()}">{c}</a></li>' for c in letters]
    out.append("</ul></nav>")
    for c in letters:
        out.append(f'<h2 id="letter-{c.lower()}">{c}</h2>')
        out.append('<dl class="glossary">')
        for term, definition, link, alts in TERMS:
            if term[0].upper() != c:
                continue
            aka = (f' <span class="glossary-aka">Also called: {html.escape(", ".join(alts))}.</span>'
                   if alts else "")
            more = (f' <a href="{html.escape(link)}">Read more</a>' if link else "")
            out.append(f'<dt id="{slug(term)}">{html.escape(term)}</dt>')
            out.append(f'<dd>{html.escape(definition)}{aka}{more}</dd>')
        out.append("</dl>")
    return "\n          ".join(out)


def ld(page_url):
    """DefinedTermSet JSON-LD object from the same TERMS list."""
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "@id": page_url + "#glossary",
        "name": "Podiatry and leg vein glossary",
        "url": page_url,
        "inLanguage": "en-US",
        "publisher": {"@id": "https://jupiterlaser.com/#clinic"},
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "@id": page_url + "#" + slug(term),
                "name": term,
                **({"alternateName": alts} if alts else {}),
                "description": definition,
                "url": page_url + "#" + slug(term),
                "inDefinedTermSet": {"@id": page_url + "#glossary"},
            }
            for term, definition, link, alts in TERMS
        ],
    }
