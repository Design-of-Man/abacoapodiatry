"""City data + page generator for /locations/<city>/ local-SEO pages.

Every city between West Palm Beach and Stuart gets its own page with real
driving directions to the Jupiter office, unique copy, and LocalBusiness
schema. Imported by build.py.
"""

DEST = "4601 Military Trail, Suite 202, Jupiter, FL 33458"
DEST_Q = "4601+Military+Trail+Suite+202+Jupiter+FL+33458"

# name, slug, county, drive, route (HTML), angle (unique local copy, HTML), alt (image alt)
CITIES = [
    ("West Palm Beach", "west-palm-beach", "Palm Beach County", "25–30 minutes",
     "Take <strong>I-95 North</strong> to Exit 83 (Donald Ross Road). Head east to Military Trail, turn north, and we're at 4601 on the right — Suite 202, with free parking at the building.",
     "Plenty of West Palm patients pass a dozen podiatry offices to reach us — usually because robotic MLS laser therapy and surgeon-supervised regenerative care aren't offered closer to home. Twice-weekly laser visits pair easily with a commute up I-95.",
     "People crossing a palm-lined waterfront promenade with the city across the water"),
    ("Riviera Beach", "riviera-beach", "Palm Beach County", "about 20 minutes",
     "Take <strong>I-95 North</strong> to Exit 83 (Donald Ross Road), head east to Military Trail, then north to 4601, Suite 202.",
     "From Riviera Beach and the Port district, we're one straight run up I-95. Patients come to us for heel pain, neuropathy, and diabetic foot care they can schedule around work shifts — sessions take 10–15 minutes.",
     "Walking a concrete marina walkway with moored boats on either side"),
    ("Singer Island", "singer-island", "Palm Beach County", "about 25 minutes",
     "Cross <strong>Blue Heron Boulevard</strong> to the mainland, take I-95 North to Donald Ross Road, head east to Military Trail, then north to 4601, Suite 202.",
     "Beach walking on Singer Island is glorious — until plantar fasciitis or Achilles pain takes it away. We help island residents get back to barefoot sand miles with laser-accelerated healing.",
     "Crossing pale sand past sea oats with a towel over one shoulder"),
    ("Lake Park", "lake-park", "Palm Beach County", "15–20 minutes",
     "Head north on <strong>Military Trail</strong> or take I-95 North to Donald Ross Road; we're just north of Donald Ross at 4601, Suite 202.",
     "Lake Park patients often just drive Military Trail straight north to our door. That convenience matters when a laser plan calls for two to three short visits a week.",
     "Crouched at the edge of a wooden marina dock beside a coiled mooring line"),
    ("North Palm Beach", "north-palm-beach", "Palm Beach County", "15–18 minutes",
     "Take <strong>US-1 North</strong> to Donald Ross Road, head west to Military Trail, then north to 4601, Suite 202. Or take I-95 to the Donald Ross exit.",
     "Golfers and tennis players from North Palm Beach keep us busy with Achilles tendonitis, plantar fasciitis, and big-toe arthritis. We get you back on course without cortisone roulette.",
     "A golfer walking a mown fairway at dawn with a bag over one shoulder"),
# Palm Beach Gardens is deliberately NOT in this list. It is not a city we drive
# to -- it is an office we have, so /locations/palm-beach-gardens/ is a
# hand-written page at _src/pages/loc-palm-beach-gardens.html carrying that
# office's own address, hours and schema. Adding it back here would build the
# same path twice and the generated version would win, silently replacing the
# office page with a drive-times page.
    ("Juno Beach", "juno-beach", "Palm Beach County", "about 12 minutes",
     "Take <strong>Donald Ross Road</strong> west from US-1 to Military Trail, then turn north to 4601, Suite 202.",
     "Juno Beach's pier walkers and beach runners know heel pain well. We're one straight shot down Donald Ross Road — most patients make it door to door in about twelve minutes.",
     "Walking barefoot along the waterline past weathered pier pilings"),
    ("Jupiter", "jupiter", "Palm Beach County", "5–10 minutes",
     "We're on <strong>Military Trail</strong> between Donald Ross Road and Frederick Small Road — 4601, Suite 202, with free parking on site.",
     "This is home. From Abacoa to the Inlet, Jupiter patients can be in and out of a laser session on a lunch break — and many are.",
     "A runner crossing a wooden boardwalk above turquoise inlet water"),
    ("Abacoa", "abacoa", "Palm Beach County", "3–5 minutes",
     "From Abacoa Town Center, take <strong>Frederick Small Road</strong> west to Military Trail, turn south, and we're immediately on the left at 4601, Suite 202.",
     "We're practically inside the neighborhood — our parent practice is Abacoa Podiatry &amp; Leg Vein Center for a reason. Walk the dog, drop the kids at Lighthouse Elementary, get your laser session, done.",
     "Two people walking a paved town-centre walkway past flowering planters"),
    ("Tequesta", "tequesta", "Palm Beach County", "12–15 minutes",
     "Take <strong>US-1 or Alternate A1A South</strong> across the Loxahatchee River, turn west on Indiantown Road, then south on Military Trail to 4601, Suite 202.",
     "Tequesta patients cross the river for treatments unavailable in the village — robotic MLS laser, EPAT shockwave, and regenerative injections, all under one board-certified surgeon.",
     "Walking a dog along a residential sidewalk shaded by live oaks"),
    ("Hobe Sound", "hobe-sound", "Martin County", "about 20 minutes",
     "Take <strong>US-1 South</strong> or I-95 South to Indiantown Road (Exit 87), head east, then south on Military Trail to 4601, Suite 202.",
     "Hobe Sound sits in a care gap — big-city medicine is 40 minutes in either direction. We close that gap: advanced laser and regenerative foot care twenty minutes from Bridge Road.",
     "A hiker on a sandy trail through tall slash pines"),
    ("Port Salerno", "port-salerno", "Martin County", "about 30 minutes",
     "Take <strong>US-1 South</strong> through Hobe Sound, or I-95 South to Indiantown Road, east to Military Trail, then south to 4601, Suite 202.",
     "Watermen and dock workers from Port Salerno spend brutal hours on their feet. When plantar fasciitis or tendonitis threatens a livelihood, an evidence-based healing plan beats toughing it out.",
     "Coiling rope on a wet working fishing dock at dusk"),
    ("Palm City", "palm-city", "Martin County", "25–30 minutes",
     "Take <strong>I-95 South</strong> to Exit 87A (Indiantown Road East), head east to Military Trail, then south to 4601, Suite 202.",
     "Palm City patients hop on I-95 at Martin Highway and are here in under half an hour — worth it for technologies no closer practice offers, and same-week new-patient visits.",
     "A rider on horseback crossing a sandy paddock in low evening light"),
    ("Stuart", "stuart", "Martin County", "about 30 minutes",
     "Take <strong>US-1 South</strong> or I-95 South to Indiantown Road (Exit 87), east to Military Trail, then south to 4601, Suite 202.",
     "Our farthest regulars — and they'll tell you the drive is worth it. Stuart patients typically combine twice-weekly laser visits with errands in the northern Palm Beaches.",
     "Walking a brick sidewalk past striped shopfront awnings in a historic downtown"),
]

PAGE_TMPL = """<!--META
{{
  "path": "locations/{slug}/",
  "title": "Podiatrist for {name}, FL | Abacoa Podiatry",
  "desc": "Foot & ankle care for {name}, FL — {drive} from our Jupiter office. MLS laser, shockwave & regenerative medicine. Call (561) 915-1934.",
  "nav": "about",
  "priority": 0.6,
  "crumbs": [["Locations", "/locations/"], ["{name}", null]],
  "schema": [
    {{
      "@context": "https://schema.org",
      "@type": "MedicalWebPage",
      "name": "Podiatry & Laser Therapy for {name}, FL",
      "url": "https://jupiterlaser.com/locations/{slug}/",
      "about": {{ "@id": "https://jupiterlaser.com/#clinic" }},
      "audience": {{
        "@type": "PeopleAudience",
        "geographicArea": {{ "@type": "City", "name": "{name}", "containedInPlace": {{ "@type": "AdministrativeArea", "name": "{county}, Florida" }} }}
      }}
    }}
  ]
}}
META-->
    <section class="page-hero">
      <div class="wrap">
        <ol class="crumbs">
          <li><a href="/">Home</a></li>
          <li><a href="/locations/">Locations</a></li>
          <li>{name}</li>
        </ol>
        <span class="kicker">{county} &middot; {drive} from our Jupiter office</span>
        <h1>Advanced Foot &amp; Ankle Care for {name}</h1>
        <p class="lede">FDA-cleared MLS laser therapy, shockwave, and regenerative medicine — the treatments {name} residents can't find around the corner, {drive} away on Military Trail in Jupiter.</p>
        <div class="btn-row">
          <a class="btn btn-primary btn-lg" href="/contact/">Book Your Evaluation</a>
          <a class="btn btn-ghost btn-lg" href="tel:+15619151934">(561) 915-1934</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="split">
          <div class="prose" data-reveal>
            <h2>Why {name} patients make the trip</h2>
            <p>{angle}</p>
            <p>Every treatment plan is designed by <a href="/meet-dr-cedeno/">Dr. Orlando Cedeno, DPM</a>, a board-certified foot and ankle surgeon — which means an honest read on every option from stretching to surgery, and advanced treatment only when it genuinely fits your case.</p>
            <h3>Most requested by {name} patients</h3>
            <ul class="check-list">
              <li><a href="/services/mls-laser-therapy/">MLS laser therapy</a> for <a href="/conditions/plantar-fasciitis/">plantar fasciitis</a> &amp; <a href="/conditions/heel-pain/">heel pain</a></li>
              <li>Drug-free <a href="/conditions/neuropathy/">neuropathy</a> symptom relief</li>
              <li><a href="/services/shockwave-therapy/">Shockwave (EPAT)</a> for chronic <a href="/conditions/achilles-tendonitis/">Achilles tendonitis</a></li>
              <li><a href="/conditions/arthritis/">Arthritis</a> care that keeps you active</li>
              <li><a href="/conditions/diabetic-foot-care/">Diabetic foot exams</a> &amp; prevention</li>
            </ul>
          </div>
          <div class="split-aside" data-reveal style="--rd:0.1s">
            <div class="card card-glow" style="position:sticky;top:100px">
              <h3>Directions from {name}</h3>
              <p style="font-size:0.97rem">{route}</p>
              <div class="btn-row" style="margin-top:0.8rem">
                <a class="btn btn-primary btn-sm" href="https://www.google.com/maps/dir/?api=1&amp;origin={origin_q}&amp;destination={dest_q}" rel="noopener">Turn-by-Turn Directions</a>
              </div>
              <hr>
              <p style="font-size:0.92rem;margin:0"><strong>Abacoa Podiatry &amp; Leg Vein Center</strong><br>{dest}<br><a href="tel:+15619151934">(561) 915-1934</a><br>{{{{HOURS_JUP_LINE}}}}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="wrap">
        <figure class="photo-frame photo-atmos" style="margin:0">
          <span class="monogram" aria-hidden="true">JL</span>
          <img src="/assets/img/atmos/locations-{slug}.opt.webp" alt="{alt}"
               width="1200" height="675" loading="lazy" decoding="async" onerror="this.remove()">
        </figure>
      </div>
    </section>

    <section class="section-tight">
      <div class="wrap">
        <div class="cta-band" data-reveal>
          <div>
            <h2>{drive} to a foot that finally feels better.</h2>
            <p>Most new patients from {name} are seen within the week. One call starts it.</p>
          </div>
          <div class="btn-row">
            <a class="btn btn-primary btn-lg" href="/contact/">Book Appointment</a>
            <a class="btn btn-ghost btn-lg" href="tel:+15619151934">(561) 915-1934</a>
          </div>
        </div>
      </div>
    </section>
"""


def location_pages():
    """Yield (virtual_filename, page_source) for each city."""
    for name, slug, county, drive, route, angle, alt in CITIES:
        yield f"loc-{slug}.html", PAGE_TMPL.format(
            name=name, slug=slug, county=county, drive=drive, route=route,
            angle=angle, alt=alt, dest=DEST, dest_q=DEST_Q,
            origin_q=name.replace(" ", "+") + ",+FL",
        )
