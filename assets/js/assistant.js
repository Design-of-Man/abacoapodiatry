/* Abacoa Podiatry virtual assistant.

   Two jobs in one panel, both set answers only: no AI, no external service
   beyond the site's own /api/contact/ endpoint, no medical advice.

   1. Questions. TOPICS below are keyword-matched answers grounded in the
      site's own pages. Anything they cannot answer is passed to the front
      desk as a message, never guessed at.
   2. Booking. A one-question-per-bubble appointment request (the First Rehab
      intake pattern): topic, office, preferred doctor, a sentence about what's
      going on, name, phone, optional email, best time to call, optional
      insurance, then a summary to confirm. It posts JSON to /api/contact/ with
      source "assistant", the same endpoint and contract as the contact form.

   Facts and where they come from (change them there first, then here):
     hours        _src/hours.py (plain()); _dev/preflight.py fails if HOURS
                  below stops matching it
     topics       "What can we help with?" in _src/pages/contact.html, plus
                  the vein and wound care service pages
     doctors      "Preferred doctor" in _src/pages/contact.html
     insurance    "Insurance plans we're credentialed with", insurance.html
     addresses    _src/pages/loc-palm-beach-gardens.html, contact.html

   Delivery: success means HTTP 200 AND {"success":"true"} (the string), which
   api/contact.js only answers once the lead is stored. Anything else keeps the
   request in localStorage (QUEUE_KEY) and retries on the next page load; the
   visitor is told to call. Every answer is drafted to localStorage as it is
   given (DRAFT_KEY) so a reload can pick up where it left off.

   Analytics: one form_submit {form: "assistant"} after a confirmed send, the
   same event and payload shape main.js fires for the contact form. Never a
   field value, never the topic. */
(function () {
  "use strict";

  var PHONE_HTML = '<a href="tel:+15619151934">(561) 915-1934</a>';

  /* Each topic: match terms (any hit scores), answer HTML, follow-up chips. */
  var TOPICS = [
    {
      id: "laser",
      match: ["laser", "mls", "photobiomodulation", "light therapy", "cold laser"],
      a: "<strong>MLS laser therapy</strong> is our flagship treatment — an FDA-cleared laser that uses two synchronized wavelengths to calm pain and inflammation and speed tissue healing. Sessions are <strong>painless</strong>, take <strong>10–15 minutes</strong>, and have no downtime. Most plans run 6–12 sessions.<ul><li><a href='/services/mls-laser-therapy/'>MLS laser therapy in depth</a></li></ul>",
      chips: ["Does it hurt?", "How much does it cost?", "Book an appointment"]
    },
    {
      id: "hurt",
      match: ["hurt", "painful", "pain during", "does it feel", "needles"],
      a: "No — laser therapy is <strong>completely painless</strong>. Most patients feel nothing at all, or a mild soothing warmth. No needles, no incisions, no recovery time. Shockwave therapy feels like a firm rhythmic tapping — very tolerable, and we adjust intensity to your comfort.",
      chips: ["How many sessions?", "What conditions do you treat?", "Book an appointment"]
    },
    {
      id: "sessions",
      match: ["how many sessions", "how long", "how fast", "how quickly", "results", "how soon"],
      a: "Most conditions respond within <strong>6–12 laser sessions</strong>, scheduled 2–3 times per week — many patients feel improvement in the first 1–3 visits. Shockwave typically runs 3–5 weekly sessions. You'll get a specific plan at your evaluation, adjusted as you progress.",
      chips: ["Does it hurt?", "How much does it cost?", "Book an appointment"]
    },
    {
      id: "cost",
      match: ["cost", "price", "how much", "insurance", "coverage", "covered", "medicare", "pay", "hsa", "fsa", "payment"],
      a: "Your <strong>evaluation and standard podiatric care are typically covered by insurance</strong>. Laser, shockwave, and regenerative therapies are usually elective (out-of-pocket) — we quote transparent package pricing <em>before</em> you commit, and HSA/FSA funds generally apply. Call " + PHONE_HTML + " and our team will verify your benefits.<ul><li><a href='/faq/'>Cost &amp; insurance FAQ</a></li></ul>",
      chips: ["Do you offer payment plans?", "Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "financing",
      match: ["payment plan", "payment plans", "financing", "carecredit", "care credit", "installment", "package pricing"],
      a: "Ask our front desk about current packages and payment options when you call " + PHONE_HTML + " — we work to keep effective treatment within reach. For the Foot BBL&trade;, financing is available through CareCredit and similar programs, with transparent pricing given at consultation.<ul><li><a href='/faq/'>Cost &amp; insurance FAQ</a></li><li><a href='/services/foot-bbl/'>Foot BBL&trade; pricing</a></li></ul>",
      chips: ["Book an appointment", "How much does it cost?"]
    },
    {
      id: "book",
      match: ["book", "appointment", "schedule", "visit", "come in", "see the doctor", "consultation", "availab"],
      a: "The fastest way to book is to call " + PHONE_HTML + " — most new patients are seen <strong>within the week</strong>. You can also <a href='/contact/'>request an appointment online</a> and our team will call you back to confirm.",
      chips: ["Leave your info, we'll call you back", "What should I bring?", "Where are you located?", "What are your hours?"]
    },
    {
      id: "reschedule",
      match: ["cancel", "reschedul", "change my appointment", "move my appointment", "running late"],
      a: "No problem — call " + PHONE_HTML + " as soon as you know and our front desk will get you rebooked or adjusted. It's the fastest way to change or cancel a visit.",
      chips: ["Book an appointment", "Where are you located?"]
    },
    {
      id: "location",
      match: ["where", "located", "location", "address", "directions", "parking", "office"],
      a: "We have two offices.<br><strong>Jupiter:</strong> 4601 Military Trail, Suite 202, Jupiter, FL 33458 — minutes from Abacoa and I-95, free on-site parking. Open Mon–Thu 8 AM–5 PM · Fri 8 AM–2 PM.<br><strong>Palm Beach Gardens:</strong> 11380 Prosperity Farms Rd, Suite 204, FL 33410 — our laser center. Open Mon–Wed 8 AM–4:30 PM · Fri 8 AM–2 PM · Sat by concierge appointment only.<ul><li><a href='/locations/palm-beach-gardens/'>Palm Beach Gardens office</a></li><li><a href='/contact/'>Map &amp; directions</a></li><li><a href='/locations/'>All areas we serve</a></li></ul>",
      chips: ["What are your hours?", "Book an appointment"]
    },
    {
      id: "hours",
      match: ["hours", "open", "close", "weekend", "saturday", "sunday", "lunch"],
      // Two offices on different schedules. Kept in step with _src/hours.py by
      // a check in _dev/preflight.py -- this file is not generated by build.py,
      // so nothing else would catch it drifting.
      a: "<strong>Jupiter</strong> (4601 Military Trail): Mon–Thu 8 AM–5 PM · Fri 8 AM–2 PM — closed Sunday. Saturday is by concierge appointment only.<br><strong>Palm Beach Gardens</strong> (11380 Prosperity Farms Rd): Mon–Wed 8 AM–4:30 PM · Fri 8 AM–2 PM — closed Thursday and Sunday. Saturday is by concierge appointment only.<br>Call " + PHONE_HTML + " to schedule at either office.",
      chips: ["Book an appointment", "Where are you located?"]
    },
    {
      id: "heel",
      match: ["heel", "plantar", "fasciitis", "morning pain", "first steps", "spur"],
      a: "Sharp heel pain with your first steps in the morning is the signature of <strong>plantar fasciitis</strong> — the most common condition we treat, and one that responds very well to laser and shockwave therapy, even after failed injections.<ul><li><a href='/conditions/plantar-fasciitis/'>Plantar fasciitis treatment</a></li><li><a href='/conditions/heel-pain/'>All causes of heel pain</a></li></ul>",
      chips: ["How many sessions?", "Book an appointment"]
    },
    {
      id: "neuropathy",
      match: ["neuropathy", "burning", "tingling", "numb", "pins and needles", "diabetic nerve"],
      a: "Burning, tingling, or numb feet usually point to <strong>peripheral neuropathy</strong>. We offer drug-free MLS laser therapy that improves the microcirculation feeding your nerves — many patients report less burning and better sleep.<ul><li><a href='/conditions/neuropathy/'>Neuropathy treatment</a></li><li><a href='/conditions/diabetic-foot-care/'>Diabetic foot care</a></li></ul>",
      chips: ["How many sessions?", "Book an appointment"]
    },
    {
      id: "achilles",
      match: ["achilles", "tendon", "tendonitis", "tendinitis", "back of ankle", "calf"],
      a: "Pain in the cord above your heel is usually <strong>Achilles tendonitis</strong>. We treat it with loading rehab plus laser and shockwave — and we never inject cortisone into the Achilles (it raises rupture risk).<ul><li><a href='/conditions/achilles-tendonitis/'>Achilles treatment</a></li></ul>",
      chips: ["How many sessions?", "Book an appointment"]
    },
    {
      id: "ankle",
      match: ["sprain", "twisted", "rolled", "unstable", "ankle"],
      a: "Ankle sprains that aren't rehabbed properly become chronic instability — up to 40% leave lingering symptoms. We grade the injury, rule out fracture, accelerate healing with laser, and rebuild strength and balance.<ul><li><a href='/conditions/sprains-strains/'>Sprains &amp; strains</a></li></ul>",
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "bunion",
      match: ["bunion", "bony bump", "big toe bump", "hallux valgus", "toe leaning"],
      a: "A <strong>bunion</strong> is a progressive joint deformity — a bony bulge at the base of the big toe that worsens over time. First-line care is nonsurgical: taping, padding, custom orthotics, footwear changes, and anti-inflammatories. Large or stubbornly painful bunions may need surgical correction, which our board-certified surgeons perform — including minimally invasive techniques.<ul><li><a href='/conditions/bunions/'>Bunion treatment</a></li></ul>",
      chips: ["Book an appointment", "Do I need surgery?"]
    },
    {
      id: "bbl",
      match: ["bbl", "fat pad", "cushion", "walking on marbles", "walking on bones", "ball of foot", "heels hurt", "liposana", "sculptra"],
      a: "The <strong>Foot BBL&trade;</strong> is our signature fat-pad restoration procedure — it rebuilds the natural cushion under your heel and forefoot using Liposana&trade; (an adipose allograft) or Sculptra (a collagen stimulator). In-office, under local anesthesia, no liposuction, walk out same day. If it feels like you're walking on marbles or heels have become unbearable, this addresses the actual cause.<ul><li><a href='/services/foot-bbl/'>Foot BBL&trade; in depth</a></li></ul>",
      chips: ["What's Foot BBL recovery like?", "How much does it cost?", "Book an appointment"]
    },
    {
      id: "bbl-recovery",
      match: ["bbl recovery", "foot bbl recovery", "how long is recovery", "after the bbl", "bbl downtime"],
      a: "Foot BBL&trade; recovery is gentle: <strong>days 1–3</strong> walking with offloading (a post-op shoe or soft dressing) and mild tenderness, <strong>week 1</strong> back to most daily activities, <strong>weeks 2–4</strong> back to normal footwear and full activity, and the cushion keeps settling through <strong>weeks 4–12</strong>. There's no donor site, so there's nothing else to heal from.<ul><li><a href='/services/foot-bbl/'>Foot BBL&trade; in depth</a></li></ul>",
      chips: ["How much does it cost?", "Book an appointment"]
    },
    {
      id: "flatfeet",
      match: ["flat feet", "flat foot", "flatfoot", "fallen arch", "arches", "pttd"],
      a: "Flat feet that ache, tire quickly, or roll inward deserve evaluation — especially if the arch is newly lowering (often a failing posterior tibial tendon). Care runs from custom orthotics and bracing to full flatfoot reconstruction by our surgeons.<ul><li><a href='/conditions/flat-feet/'>Flat feet treatment</a></li></ul>",
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "wound",
      match: ["wound", "ulcer", "sore that won't heal", "not healing", "open sore", "slow healing", "stitches won't close"],
      a: "Any wound that hasn't clearly improved in two weeks — or <strong>any wound on a diabetic foot</strong> — should be seen promptly. Healthy healing needs blood supply, pressure relief, infection control, and cooperative body chemistry; a wound that lingers is usually missing one of those. Our advanced wound care program covers debridement, offloading, advanced dressings, infection management, circulation assessment, biologics, and limb preservation, plus surgery in-house when structure demands it. Please call " + PHONE_HTML + " today rather than waiting.<ul><li><a href='/services/wound-care/'>Wound care program</a></li></ul>",
      chips: ["Book an appointment", "Where are you located?"]
    },
    {
      id: "diabetic",
      match: ["diabetic", "diabetes", "diabetic foot", "blood sugar", "a1c"],
      a: "Diabetes threatens feet two ways: nerve damage that silences pain, and slowed circulation that delays healing — a blister you never felt can become an ulcer before anyone notices. See a podiatrist <strong>at least annually</strong>, or every 3–6 months with neuropathy, circulation problems, deformity, or a prior ulcer. Your visit includes sensation testing, circulation assessment, skin/nail evaluation, and pressure-point mapping. Check both feet daily for redness, blisters, cracks, or color changes, and call promptly about anything new.<ul><li><a href='/conditions/diabetic-foot-care/'>Diabetic foot care</a></li><li><a href='/services/wound-care/'>Wound care program</a></li></ul>",
      chips: ["Book an appointment", "Where are you located?"]
    },
    {
      id: "arthritis",
      match: ["arthritis", "joint", "stiff", "big toe", "bunion", "hallux"],
      a: "Foot and ankle <strong>arthritis</strong> is very treatable: laser therapy reduces joint inflammation drug-free, and offloading strategies keep you active. Big-toe stiffness (hallux rigidus) is one of our most common presentations.<ul><li><a href='/conditions/arthritis/'>Arthritis treatment</a></li></ul>",
      chips: ["How many sessions?", "Book an appointment"]
    },
    {
      id: "shockwave",
      match: ["shockwave", "epat", "eswt", "acoustic"],
      a: "<strong>Shockwave (EPAT)</strong> sends acoustic pressure waves into chronically injured tissue to break down scar tissue and restart stalled healing — one of the best-evidenced treatments for stubborn plantar fasciitis and Achilles problems. 3–5 weekly sessions, no downtime.<ul><li><a href='/services/shockwave-therapy/'>Shockwave in depth</a></li></ul>",
      chips: ["Does it hurt?", "Book an appointment"]
    },
    {
      id: "regen",
      match: ["prp", "platelet", "stem cell", "regenerative", "injection", "biologic"],
      a: "We offer <strong>PRP</strong> (your own concentrated growth factors) and <strong>regenerative cell therapies</strong> for tendons, fascia, and joints that have stopped healing — honest, surgeon-supervised, and only recommended when the evidence supports it for your diagnosis.<ul><li><a href='/services/prp-therapy/'>PRP therapy</a></li><li><a href='/services/regenerative-medicine/'>Stem cell therapy</a></li></ul>",
      chips: ["How much does it cost?", "Book an appointment"]
    },
    {
      id: "doctor",
      match: ["doctor", "cedeno", "mustafa", "surgeon", "who", "podiatrist", "credentials", "qualified", "providers"],
      a: "Care is led by two foot &amp; ankle surgeons: <strong>Dr. Orlando Cedeno, DPM</strong> — board-certified, trained in reconstructive &amp; trauma surgery at Chestnut Hill Hospital/University of Pennsylvania — and <strong>Dr. Isin A. Mustafa, DPM, MSHS</strong> — Chief Resident-trained at Chino Valley Medical Center, specializing in minimally invasive surgery and regenerative medicine.<ul><li><a href='/meet-dr-cedeno/'>Meet Dr. Cedeno</a></li><li><a href='/meet-dr-mustafa/'>Meet Dr. Mustafa</a></li></ul>",
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "conditions",
      match: ["conditions", "what do you treat", "help with", "treat"],
      a: "We treat the full range of foot and ankle problems: <a href='/conditions/plantar-fasciitis/'>plantar fasciitis</a>, <a href='/conditions/heel-pain/'>heel pain</a>, <a href='/conditions/neuropathy/'>neuropathy</a>, <a href='/conditions/achilles-tendonitis/'>Achilles tendonitis</a>, <a href='/conditions/arthritis/'>arthritis</a>, <a href='/conditions/sports-injuries/'>sports injuries</a>, <a href='/conditions/sprains-strains/'>sprains</a>, and <a href='/conditions/diabetic-foot-care/'>diabetic foot care</a>.",
      chips: ["Book an appointment", "Tell me about laser therapy"]
    },
    {
      id: "referral",
      match: ["referral", "refer", "hmo", "pcp", "authorization", "primary care"],
      a: "Most patients <strong>don't need a referral</strong> to see a podiatrist — you can book directly. A few HMO plans require one; call " + PHONE_HTML + " and we'll help you check your plan. We're also happy to coordinate care and send records to any physician you choose, many patients come to us just for the laser or regenerative portion of their care.",
      chips: ["Book an appointment", "How much does it cost?"]
    },
    {
      id: "bring",
      match: ["bring", "first visit", "first appointment", "expect", "new patient", "checklist", "what to bring"],
      a: "Bring a photo ID, insurance card, medication list, any prior imaging, and <strong>your most-worn shoes</strong> (wear patterns tell us a lot). Plan 45–60 minutes; laser treatment can often start the same day.<ul><li><a href='/new-patients/'>Your first visit, step by step</a></li></ul>",
      chips: ["What happens at the first visit?", "Book an appointment", "What are your hours?"]
    },
    {
      id: "first-visit-depth",
      match: ["what happens at the first visit", "walk me through", "how does the first appointment work", "first exam"],
      a: "Here's the sequence: call or send an <a href='/contact/'>online request</a> (most new patients seen within the week); arrive ~15 minutes early for check-in; a focused history and hands-on exam with Dr. Cedeno, with digital imaging when needed; a plain-English diagnosis and every reasonable option — conservative, laser/regenerative, and (rarely) surgical — with honest pros, cons, and costs; and treatment can often start the same visit if laser therapy is part of your plan. Plan 45–60 minutes for visit one.<ul><li><a href='/new-patients/'>Full first-visit walkthrough</a></li></ul>",
      chips: ["What should I bring?", "Book an appointment"]
    },
    {
      id: "telehealth",
      match: ["telehealth", "video visit", "virtual visit", "video call", "zoom appointment", "online visit"],
      a: "Yes — we offer telehealth for visits that don't need hands-on exam: follow-ups, results reviews, wound-photo checks, medication questions, and \"should I come in?\" calls. Diagnosis of a new problem, laser/shockwave treatments, injections, and imaging still need an office visit. Call " + PHONE_HTML + " to schedule a video visit and we'll send you a link — any smartphone, tablet, or computer with a camera works.<ul><li><a href='/telehealth/'>How telehealth works here</a></li></ul>",
      chips: ["Book an appointment", "Where are you located?"]
    },
    {
      id: "vein",
      match: ["vein", "varicose", "spider vein", "evlt", "sclerotherapy", "leg swelling", "swollen ankle", "swollen legs", "venous"],
      a: "Swollen ankles, aching legs, and bulging veins usually trace back to <strong>venous insufficiency</strong> — leg vein valves that no longer close properly, letting blood pool. We treat it with sclerotherapy (spider/small varicose veins), endovenous laser therapy (EVLT) or radiofrequency ablation (larger veins), and compression therapy, with vein stripping/ligation reserved for advanced cases. An ultrasound maps which veins are involved before we recommend a treatment. Evaluation and medically necessary treatment are often covered by insurance; purely cosmetic spider-vein work generally isn't.<ul><li><a href='/services/vein-treatment/'>Vein treatment in depth</a></li><li><a href='/conditions/venous-insufficiency/'>Venous insufficiency</a></li></ul>",
      chips: ["How much does it cost?", "Book an appointment"]
    },
    {
      id: "pediatric",
      match: ["child", "children", "kid", "kids", "teen", "teenager", "pediatric", "my son", "my daughter"],
      a: "We see adolescent athletes for sports injuries, heel pain (Sever's disease is common in active kids), and ankle sprains. Call and describe the situation — if a pediatric specialist is a better fit for your child, we'll tell you honestly.",
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "postop",
      match: ["post-op", "post op", "after surgery", "surgical recovery", "recovering from surgery", "weight-bearing", "crutches"],
      a: "Post-surgical healing is one of MLS laser therapy's best uses — it helps manage swelling and supports tissue repair, and our surgeons routinely build it into post-operative protocols. Your recovery timeline and any weight-bearing restrictions come from the specific procedure performed, so follow the plan your surgeon gave you and call " + PHONE_HTML + " with any concerns during recovery.<ul><li><a href='/services/foot-ankle-surgery/'>Surgical care</a></li><li><a href='/services/mls-laser-therapy/'>MLS laser therapy</a></li></ul>",
      chips: ["Book an appointment", "Tell me about laser therapy"]
    },
    {
      id: "video",
      match: ["video", "youtube", "watch", "media"],
      a: "Dr. Cedeno's video library — treatment explainers and foot-health tips — is on our <a href='/media/'>Media page</a> and on <a href='https://www.youtube.com/@abacoapodiatryandlegveincenter' rel='noopener'>YouTube</a>.",
      chips: ["Tell me about laser therapy", "Book an appointment"]
    },
    {
      id: "emergency",
      match: ["emergency", "urgent", "can't walk", "cant walk", "pop", "broken", "fracture", "infection", "fever", "swollen"],
      a: "<strong>If you can't bear weight, felt a pop, have spreading redness, fever with foot pain, or any wound on a diabetic foot — call us now at " + PHONE_HTML + "</strong> and we'll tell you exactly where you need to be. For severe emergencies call 911 or go to the nearest ER.",
      chips: ["Where are you located?"]
    }
  ];

  /* ------------------------------------------------------------------
     Facts the booking flow states. See the header for each source.
     ------------------------------------------------------------------ */

  // _src/hours.py plain() output, verbatim. _dev/preflight.py imports
  // hours.plain() and fails the gate if either string stops matching.
  var HOURS = {
    jupiter: "Mon–Thu 8 AM–5 PM · Fri 8 AM–2 PM",
    pbg: "Mon–Wed 8 AM–4:30 PM · Fri 8 AM–2 PM"
  };

  var OFFICES = [
    { value: "Jupiter", where: "4601 Military Trail, Suite 202", hours: HOURS.jupiter, re: /jup|military/i },
    { value: "Palm Beach Gardens", where: "11380 Prosperity Farms Rd, Suite 204", hours: HOURS.pbg, re: /garden|pbg|prosperity/i }
  ];
  var EITHER_OFFICE = "Either office";

  // The contact form's "What can we help with?" options (minus "Something
  // else", which typing covers), plus the vein and wound care service lines.
  var REASONS = [
    "Heel or arch pain", "Bunion or big-toe problem", "Ingrown or painful toenail",
    "Neuropathy / burning feet", "Tendon or ankle problem", "Arthritis pain",
    "Sports injury", "Diabetic foot care", "Leg veins / swelling", "Wound care",
    "Interested in laser / regenerative therapy", "Not sure yet"
  ];

  // Same three values as the contact form's "Preferred doctor" select, so the
  // office reads one vocabulary whichever form the request came from.
  var DOCTORS = ["First available", "Dr. Orlando Cedeno", "Dr. Isin Mustafa"];

  // insurance.html, "Insurance plans we're credentialed with", in page order.
  var PLANS = ["Medicare", "Medicare RR", "Aetna", "BCBS", "Cigna", "UHC", "Coventry",
    "Dimension", "Florida College System", "Multiplan / PHCS", "Medicarease",
    "Prime Health Services", "CorVel (WC)", "Rockport (WC)", "DOL"];
  var PLANS_FIRST = ["Medicare", "Aetna", "BCBS", "Cigna", "UHC"];

  // Every window sits inside both offices' published hours (earliest open 8,
  // Friday close 2). "Afternoon" runs to whichever office's close applies.
  var TIMES = ["Morning (8–11)", "Midday (11–2)", "Afternoon (2–close)", "Any time"];

  var LIMITS = { name: 200, phone: 50, email: 200, reason: 120, message: 4000 };
  var DRAFT_KEY = "ap.assist.draft.v1";
  var QUEUE_KEY = "ap.assist.queue.v1";
  var DRAFT_MAX_AGE = 72 * 3600 * 1000;
  var ENDPOINT = "/api/contact/";   // trailingSlash: true in vercel.json

  /* ------------------------------------------------------------------
     Small helpers
     ------------------------------------------------------------------ */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9]+/g, ""); }
  function plainLabel(label) { return String(label).replace(/^[^A-Za-z0-9]+/, ""); }
  function hint(text) { return ' <span class="assist-hint">' + text + "</span>"; }

  function storage() { try { return window.localStorage; } catch (e) { return null; } }
  function load(key) {
    var s = storage(); if (!s) return null;
    try { return JSON.parse(s.getItem(key)); } catch (e) { return null; }
  }
  function save(key, val) {
    var s = storage(); if (!s) return;
    try { s.setItem(key, JSON.stringify(val)); } catch (e) { /* full or blocked */ }
  }
  function drop(key) {
    var s = storage(); if (!s) return;
    try { s.removeItem(key); } catch (e) {}
  }

  /* Same shape as track() in assets/js/main.js, which is private to that
     file's closure. Fired only after the endpoint confirms the lead is stored. */
  function trackLead() {
    if (typeof window.va === "function") window.va("event", { name: "form_submit", data: { form: "assistant" } });
    if (typeof window.gtag === "function") window.gtag("event", "form_submit", { form: "assistant" });
  }

  function answer(q) {
    var n = q.toLowerCase();
    var best = null, bestScore = 0;
    TOPICS.forEach(function (topic) {
      var score = 0;
      topic.match.forEach(function (term) {
        if (n.indexOf(term) !== -1) score += term.length; // longer term = stronger signal
      });
      if (score > bestScore) { bestScore = score; best = topic; }
    });
    return best;
  }

  /* ------------------------------------------------------------------
     DOM
     ------------------------------------------------------------------ */
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var fab = $("#assist-open"), panel = $("#assist-panel");
  if (!fab || !panel) return;
  var log = $("#assist-log"), chipsBox = $("#assist-chips"),
      form = $("#assist-form"), input = $("#assist-input"),
      restartBtn = $("#assist-restart");

  function scroll() { log.scrollTop = log.scrollHeight; }

  function addMsg(html, who, extra) {
    var el = document.createElement("div");
    el.className = "assist-msg " + who + (extra ? " " + extra : "");
    el.innerHTML = html;
    log.appendChild(el);
    scroll();
    return el;
  }

  var curChips = [];
  function setChips(defs) {
    chipsBox.innerHTML = "";
    curChips = (defs || []).map(function (d) {
      return typeof d === "string" ? { label: d, value: d } : d;
    });
    curChips.forEach(function (c) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "assist-chip" + (c.cls ? " " + c.cls : "");
      b.textContent = c.label;
      b.addEventListener("click", function () { handle(c.value, plainLabel(c.label)); });
      chipsBox.appendChild(b);
    });
    // The chips bar just changed height, which moves the bottom of the log.
    chipsBox.scrollTop = 0;
    scroll();
  }

  var busy = false;
  // Bot messages, one bubble at a time, each behind a short typing indicator.
  function botSay(msgs, done) {
    busy = true;
    setChips([]);
    var i = 0;
    (function next() {
      if (i >= msgs.length) { busy = false; if (done) done(); return; }
      var m = msgs[i];
      var html = typeof m === "string" ? m : m.html;
      var typing = addMsg('<span class="assist-typing"><i></i><i></i><i></i></span>', "bot");
      window.setTimeout(function () {
        typing.innerHTML = html;
        if (m.cls) typing.className += " " + m.cls;
        scroll();
        i++;
        next();
      }, Math.min(320 + html.replace(/<[^>]+>/g, "").length * 3, 900));
    })();
  }

  /* ------------------------------------------------------------------
     Conversation
     ------------------------------------------------------------------ */
  var flow = { state: "intent", data: {}, fixing: false };
  var FLOW_STATES = ["topic", "office", "doctor", "message", "name", "phone", "email",
    "time", "insurance", "confirm", "fix"];

  var APPT_CHIP = { label: "📅 Request an appointment", value: "go:appointment", cls: "primary" };
  var MESSAGE_CHIP = { label: "📨 Leave a message for the front desk", value: "go:message" };
  var FAQ_MENU = ["Tell me about laser therapy", "What conditions do you treat?",
    "How much does it cost?", "What are your hours?", "Where are you located?", "What should I bring?"];

  function faqChips(labels) {
    var out = [APPT_CHIP], seen = {};
    (labels || FAQ_MENU).forEach(function (l) {
      // The old lead-capture chips now start the appointment request.
      if (/^book an appointment$|call you back/i.test(l) || seen[l]) return;
      seen[l] = 1;
      out.push({ label: l, value: "q:" + l });
    });
    out.push(MESSAGE_CHIP);
    return out;
  }

  function officeFor(d) {
    for (var i = 0; i < OFFICES.length; i++) if (OFFICES[i].value === d.office) return OFFICES[i];
    return null;
  }
  function firstName(d) { return (d.name || "").trim().split(/\s+/)[0] || ""; }

  var STEPS = {
    intent: {
      prompt: function () {
        return ["Hi! I'm the Abacoa Podiatry &amp; Leg Vein Center assistant. I can request an appointment for you, answer questions about our treatments, costs and offices, or pass a message to the front desk.",
          "What brings you in today?"];
      },
      chips: function () {
        return [APPT_CHIP, { label: "💬 Ask a question", value: "go:faq" },
          { label: "👀 Just looking around", value: "go:browse" }];
      }
    },
    browse_end: {
      prompt: function () {
        return ["Enjoy looking around! I'll be right here in the corner if a question comes up. You can also call us at " + PHONE_HTML + "."];
      },
      chips: function () {
        return [{ label: "📅 Actually, book me in", value: "go:appointment", cls: "primary" },
          { label: "💬 I do have a question", value: "go:faq" }];
      }
    },
    topic: {
      prompt: function () {
        return ["Happy to set that up. What would you like us to look at?" + hint("Tap one, or type it in your own words.")];
      },
      chips: function () { return REASONS; },
      accept: function (v) {
        if (v.trim().length < 2) return { error: "Could you tell me in a word or two what it's about?" };
        return { value: v.slice(0, LIMITS.reason) };
      },
      save: "topic",
      next: function () { return "office"; }
    },
    office: {
      prompt: function () {
        return ["Which office suits you best?<br><strong>Jupiter</strong>, " + OFFICES[0].where + ": " + OFFICES[0].hours +
          ".<br><strong>Palm Beach Gardens</strong>, " + OFFICES[1].where + ": " + OFFICES[1].hours +
          "." + hint("Palm Beach Gardens is open fewer days and is closed Thursdays.")];
      },
      chips: function () {
        return [{ label: "Jupiter", value: "Jupiter" }, { label: "Palm Beach Gardens", value: "Palm Beach Gardens" },
          { label: "Either is fine", value: EITHER_OFFICE }];
      },
      accept: function (v) {
        if (v === EITHER_OFFICE || /either|any|no pref|whichever|doesn.?t matter|both/i.test(v)) return { value: EITHER_OFFICE, echo: "Either is fine" };
        for (var i = 0; i < OFFICES.length; i++) if (v === OFFICES[i].value || OFFICES[i].re.test(v)) return { value: OFFICES[i].value };
        return { error: "We have two offices, Jupiter and Palm Beach Gardens. Which one works for you?" };
      },
      save: "office",
      next: function () { return "doctor"; }
    },
    doctor: {
      prompt: function () { return ["Do you have a preferred doctor?" + hint("Optional. First available is fine.")]; },
      chips: function () { return DOCTORS; },
      accept: function (v) {
        if (/cedeno/i.test(v)) return { value: DOCTORS[1] };
        if (/mustafa/i.test(v)) return { value: DOCTORS[2] };
        if (/first|either|any|no pref|whoever|skip|doesn.?t matter/i.test(v)) return { value: DOCTORS[0] };
        return { error: "Our doctors are Dr. Orlando Cedeno and Dr. Isin Mustafa. Pick one, or First available." };
      },
      save: "doctor",
      next: function () { return "message"; }
    },
    message: {
      prompt: function (d) {
        var note = hint("No detailed medical history needed, just the basics please.");
        return d.intent === "question"
          ? ["Of course. What would you like to ask? I'll pass it straight to the front desk." + note]
          : ["Tell me a little about what's going on. A sentence or two is perfect." + note];
      },
      chips: function (d) { return d.intent === "question" ? [{ label: "Never mind", value: "go:faq" }] : []; },
      accept: function (v) {
        if (v.trim().length < 2) return { error: "Could you give me just a few words about it?" };
        return { value: v.slice(0, LIMITS.message) };
      },
      save: "message",
      next: function () { return "name"; }
    },
    name: {
      prompt: function () {
        return ["Thanks. Now your contact details so the front desk can reach you. What's your <strong>first and last name</strong>?"];
      },
      chips: function (d) { return d.intent === "question" ? [{ label: "Never mind", value: "go:faq" }] : []; },
      accept: function (v) {
        if (v.replace(/[^A-Za-zÀ-ɏ]/g, "").length < 2) return { error: "Please type your first and last name." };
        return { value: v.slice(0, LIMITS.name) };
      },
      save: "name",
      next: function () { return "phone"; }
    },
    phone: {
      prompt: function (d) {
        var first = firstName(d);
        return ["Thanks" + (first ? ", " + esc(first) : "") + "! What's the best <strong>phone number</strong> to reach you?"];
      },
      accept: function (v) {
        var digits = v.replace(/\D/g, "");
        if (digits.length === 11 && digits.charAt(0) === "1") digits = digits.slice(1);
        if (digits.length !== 10) {
          return { error: "Hmm, that doesn't look like a full US phone number. Mind double-checking it? (For example 561-555-1234.)" };
        }
        return { value: "(" + digits.slice(0, 3) + ") " + digits.slice(3, 6) + "-" + digits.slice(6) };
      },
      save: "phone",
      next: function () { return "email"; }
    },
    email: {
      prompt: function () {
        return ["And your <strong>email address</strong>, in case we can't reach you by phone?" + hint("Optional. Tap Skip if you'd rather not.")];
      },
      chips: function () { return [{ label: "Skip", value: "__skip__" }]; },
      accept: function (v) {
        if (v === "__skip__" || /^(skip|no|none|no thanks|n\/a)$/i.test(v.trim())) return { value: "", echo: "Skip" };
        if (!/^[^\s@<>]+@[^\s@<>]+\.[A-Za-z]{2,}$/.test(v.trim())) return { error: "That email doesn't look quite right. Want to try again, or tap Skip?" };
        return { value: v.trim().slice(0, LIMITS.email) };
      },
      save: "email",
      next: function (d) { return d.intent === "question" ? "confirm" : "time"; }
    },
    time: {
      prompt: function (d) {
        var o = officeFor(d) || OFFICES[0];
        return ["When's the best time for the front desk to call you? They call during " + o.value + " office hours, " + o.hours + "."];
      },
      chips: function () { return TIMES; },
      accept: function (v) {
        for (var i = 0; i < TIMES.length; i++) if (norm(v) === norm(TIMES[i])) return { value: TIMES[i] };
        if (/any/i.test(v)) return { value: TIMES[3] };
        if (/morn/i.test(v)) return { value: TIMES[0] };
        if (/mid|noon|lunch/i.test(v)) return { value: TIMES[1] };
        if (/after/i.test(v)) return { value: TIMES[2] };
        return { error: "The front desk calls during office hours, so pick one of these windows." };
      },
      save: "preferred_time",
      next: function () { return "insurance"; }
    },
    insurance: {
      prompt: function () {
        return ["Last one: which insurance do you have? Dr. Cedeno and Dr. Mustafa are credentialed with the plans below, and our team verifies your exact plan before your visit." + hint("Optional.")];
      },
      chips: function () { return planChips(PLANS_FIRST, true); },
      accept: function (v) {
        if (v === "__more__") return { rechips: planChips(PLANS.filter(function (p) { return PLANS_FIRST.indexOf(p) === -1; }), false), echo: "More plans" };
        if (v === "__skip__" || /^(skip|none|no)$/i.test(v.trim())) return { value: "", echo: "Skip" };
        if (/not sure|don.?t know|unsure/i.test(v)) return { value: "Not sure" };
        for (var i = 0; i < PLANS.length; i++) if (norm(v) === norm(PLANS[i])) return { value: PLANS[i] };
        return { value: v.trim().slice(0, 120) };
      },
      save: "insurance",
      next: function () { return "confirm"; }
    },
    confirm: {
      prompt: function (d) { return [{ html: summaryHTML(d), cls: "assist-card" }, "Did I get everything right?"]; },
      chips: function () {
        return [{ label: "✅ Yes, send it", value: "__send__", cls: "primary" }, { label: "✏️ Fix something", value: "__fix__" }];
      },
      accept: function (v) {
        if (v === "__fix__" || /\b(fix|no|nope|edit|change|wrong|not right)\b/i.test(v)) return { goto: "fix", echo: "Fix something" };
        if (v === "__send__" || /^(y|yes|yep|yeah|send|send it|correct|right|ok|okay|looks good)\b/i.test(v.trim())) return { send: true, echo: "Yes, send it" };
        return { error: "Tap “Yes, send it” when you're ready, or “Fix something” to change an answer." };
      }
    },
    fix: {
      prompt: function () { return ["No problem. Which part should I change?"]; },
      chips: function (d) {
        var out = rows(d).filter(function (r) { return r[2]; }).map(function (r) {
          return { label: r[0], value: "fix:" + r[2] };
        });
        out.push({ label: "↩ It's all correct", value: "go:confirm" });
        return out;
      }
    },
    sent: {}, queued: {}, faq: {}, resume: {}
  };

  function planChips(list, first) {
    var out = list.map(function (p) { return { label: p, value: p }; });
    if (first) out.push({ label: "More plans…", value: "__more__" });
    out.push({ label: "Not sure", value: "Not sure" }, { label: "Skip", value: "__skip__" });
    return out;
  }

  // [label, value, step that edits it]
  function rows(d) {
    if (d.intent === "question") {
      return [["Request", "A question for the front desk", null], ["Message", d.message, "message"],
        ["Name", d.name, "name"], ["Phone", d.phone, "phone"], ["Email", d.email || "Not given", "email"]];
    }
    return [["Reason", d.topic, "topic"], ["Office", d.office, "office"], ["Doctor", d.doctor, "doctor"],
      ["Details", d.message, "message"], ["Name", d.name, "name"], ["Phone", d.phone, "phone"],
      ["Email", d.email || "Not given", "email"], ["Call time", d.preferred_time, "time"],
      ["Insurance", d.insurance || "Not given", "insurance"]];
  }

  function summaryHTML(d) {
    var html = '<dl class="assist-summary">';
    rows(d).forEach(function (r) {
      if (r[1]) html += "<div><dt>" + r[0] + "</dt><dd>" + esc(r[1]) + "</dd></div>";
    });
    return html + "</dl>";
  }

  function persist() {
    if (FLOW_STATES.indexOf(flow.state) !== -1) {
      save(DRAFT_KEY, { state: flow.state, data: flow.data, fixing: flow.fixing, t: Date.now() });
    } else if (flow.state !== "resume") {
      drop(DRAFT_KEY);
    }
  }

  function focusInput() {
    // Not on phones: focusing would throw up the keyboard over the chips.
    if (!panel.hidden && window.matchMedia("(min-width: 761px)").matches) input.focus();
  }

  function runStep(id) {
    flow.state = id;
    persist();
    var step = STEPS[id];
    botSay(step.prompt(flow.data), function () {
      if (step.chips) setChips(step.chips(flow.data));
      focusInput();
    });
  }

  function enterFaq() {
    flow.state = "faq";
    flow.fixing = false;
    persist();
    botSay(["Happy to help. Tap a question below or type your own. If it's one I can't answer, I'll pass it to the front desk."],
      function () { setChips(faqChips()); focusInput(); });
  }

  function askQuestion(q) {
    var res = answer(q);
    if (res) {
      flow.state = "faq";
      persist();
      botSay([res.a], function () { setChips(faqChips(res.chips)); });
      return;
    }
    // Unknown: never guess. The question becomes a front-desk message.
    flow.data = { intent: "question", message: q.slice(0, LIMITS.message) };
    flow.fixing = false;
    botSay(["That one's beyond me, and I'd rather not guess. I'll pass it to the front desk so the right person can answer. (Or call " + PHONE_HTML + ".)"],
      function () { runStep("name"); });
  }

  function action(name) {
    if (name === "appointment") { flow.data = { intent: "appointment" }; flow.fixing = false; runStep("topic"); }
    else if (name === "message") { flow.data = { intent: "question" }; flow.fixing = false; runStep("message"); }
    else if (name === "faq") enterFaq();
    else if (name === "browse") runStep("browse_end");
    else if (name === "confirm") { flow.fixing = false; runStep("confirm"); }
    else if (name === "close") close();
    else if (name === "restart") restart();
    else if (name === "resume") resume();
  }

  // One entry point for chips and typed text alike.
  function handle(value, echo, typed) {
    if (busy) return false;

    // Typing a chip's label is the same as tapping it.
    if (typed) {
      for (var i = 0; i < curChips.length; i++) {
        if (norm(curChips[i].label) && norm(curChips[i].label) === norm(value)) {
          value = curChips[i].value;
          break;
        }
      }
    }

    if (value.indexOf("go:") === 0) {
      addMsg(esc(echo), "user");
      action(value.slice(3));
      return true;
    }
    if (value.indexOf("q:") === 0) {
      addMsg(esc(echo), "user");
      askQuestion(value.slice(2));
      return true;
    }
    if (value.indexOf("fix:") === 0) {
      addMsg(esc(echo), "user");
      flow.fixing = true;
      runStep(value.slice(4));
      return true;
    }

    var step = STEPS[flow.state];
    if (flow.state === "fix") {
      addMsg(esc(echo), "user");
      botSay(["Tap the part you'd like to change."], function () { setChips(STEPS.fix.chips(flow.data)); });
      return true;
    }
    if (!step || !step.accept) {
      // Not in a flow step: anything typed is a question.
      addMsg(esc(echo), "user");
      askQuestion(value);
      return true;
    }

    var res = step.accept(value);
    addMsg(esc(res.echo || (typed ? value : echo)), "user");
    if (res.error) {
      botSay([res.error], function () { if (step.chips) setChips(step.chips(flow.data)); });
      return true;
    }
    if (res.rechips) { setChips(res.rechips); return true; }
    if (res.send) { submit(); return true; }
    if (res.goto) { runStep(res.goto); return true; }

    if (step.save) flow.data[step.save] = res.value;
    if (flow.fixing) { flow.fixing = false; runStep("confirm"); return true; }
    runStep(step.next(flow.data));
    return true;
  }

  /* ------------------------------------------------------------------
     Delivery
     ------------------------------------------------------------------ */
  function refCode() {
    var abc = "ABCDEFGHJKMNPQRSTUVWXYZ23456789", out = "";
    for (var i = 0; i < 5; i++) out += abc.charAt(Math.floor(Math.random() * abc.length));
    return "AB-" + out;
  }

  function payloadFor(d) {
    var question = d.intent === "question";
    return {
      name: (d.name || "").slice(0, LIMITS.name),
      phone: (d.phone || "").slice(0, LIMITS.phone),
      email: d.email || "",
      reason: question ? "Website question" : (d.topic || "").slice(0, LIMITS.reason),
      topic: question ? "" : (d.topic || ""),
      office: question ? "" : (d.office || ""),
      doctor: question ? "" : (d.doctor || ""),
      preferred_time: question ? "" : (d.preferred_time || ""),
      insurance: question ? "" : (d.insurance || ""),
      message: (d.message || "").slice(0, LIMITS.message),
      ref: d.ref,
      intent: question ? "question" : "appointment",
      page: location.pathname,
      source: "assistant",
      _subject: (question ? "Website question " : "Appointment request ") + d.ref + " (website chat)"
    };
  }

  // Resolves only on HTTP 200 with success:"true" (a string, see api/contact.js).
  function deliver(payload) {
    return fetch(ENDPOINT, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json", Accept: "application/json" }
    }).then(function (r) {
      if (r.status !== 200) throw new Error("http " + r.status);
      return r.json();
    }).then(function (data) {
      if (!data || String(data.success).toLowerCase() !== "true") throw new Error("not stored");
      return true;
    });
  }

  function enqueue(payload) {
    var q = load(QUEUE_KEY);
    q = Array.isArray(q) ? q : [];
    q.push(payload);
    save(QUEUE_KEY, q.slice(-20));
  }

  var flushing = false;
  function flushQueue() {
    if (flushing) return;
    var q = load(QUEUE_KEY);
    if (!Array.isArray(q) || !q.length) return;
    flushing = true;
    var payload = q[0];
    deliver(payload).then(function () {
      trackLead();
      var rest = (load(QUEUE_KEY) || []).filter(function (p) { return p && p.ref !== payload.ref; });
      if (rest.length) save(QUEUE_KEY, rest); else drop(QUEUE_KEY);
      flushing = false;
      flushQueue();
    }).catch(function () { flushing = false; /* still failing; next page load */ });
  }

  function afterChips() {
    return [{ label: "💬 Ask a question", value: "go:faq" }, { label: "Close", value: "go:close" }];
  }

  function submit() {
    flow.data.ref = refCode();
    var payload = payloadFor(flow.data);
    busy = true;
    setChips([]);
    var typing = addMsg('<span class="assist-typing"><i></i><i></i><i></i></span>', "bot");

    deliver(payload).then(function () {
      trackLead();
      typing.remove();
      busy = false;
      flow.state = "sent";
      drop(DRAFT_KEY);
      botSay([
        "Perfect, it's on its way! 🎉 Your reference number is <strong>" + payload.ref + "</strong>.",
        "Our front desk will " + (payload.intent === "question" ? "get back to you" : "call you") + " at " +
          esc(payload.phone) + ", usually within one business day. Need us sooner? Call " + PHONE_HTML + "."
      ], function () { setChips(afterChips()); });
    }).catch(function () {
      typing.remove();
      busy = false;
      // The request lives in the queue now, so the draft would only duplicate it.
      enqueue(payload);
      flow.state = "queued";
      drop(DRAFT_KEY);
      botSay([
        "I couldn't get that through to the office just now, so it hasn't been received yet. It's saved on this device and I'll send it automatically the next time you open a page on this site.",
        "To make sure we reach you, please call us at " + PHONE_HTML + "."
      ], function () { setChips(afterChips()); });
    });
  }

  /* ------------------------------------------------------------------
     Open, close, resume, restart
     ------------------------------------------------------------------ */
  function restart() {
    log.innerHTML = "";
    flow = { state: "intent", data: {}, fixing: false };
    drop(DRAFT_KEY);
    runStep("intent");
  }

  var pendingDraft = null;
  function resume() {
    var d = pendingDraft;
    pendingDraft = null;
    if (!d) { restart(); return; }
    flow.data = d.data;
    flow.fixing = false;
    runStep(d.state === "fix" ? "confirm" : d.state);
  }

  var opened = false;
  function firstOpen() {
    var d = load(DRAFT_KEY);
    if (d && d.data && FLOW_STATES.indexOf(d.state) !== -1 && Date.now() - (d.t || 0) < DRAFT_MAX_AGE) {
      pendingDraft = d;
      flow.state = "resume";
      var what = d.data.intent === "question" ? "a message for the front desk" : "an appointment request";
      botSay(["Welcome back! You were partway through " + what + ". Pick up where you left off?"], function () {
        setChips([{ label: "Continue", value: "go:resume", cls: "primary" }, { label: "Start over", value: "go:restart" }]);
      });
    } else {
      runStep("intent");
    }
  }

  /* iOS does not shrink the layout viewport for the on-screen keyboard, so a
     panel pinned to the bottom slides behind it. On phones, follow the visual
     viewport instead: lift the panel by the keyboard's height and cap it to
     what is actually visible. */
  var vv = window.visualViewport;
  var phone = window.matchMedia("(max-width: 760px)");
  function fitViewport() {
    if (!vv || panel.hidden || !phone.matches) {
      panel.style.removeProperty("--assist-kb");
      panel.style.removeProperty("--assist-vh");
      return;
    }
    var kb = Math.max(0, window.innerHeight - (vv.offsetTop + vv.height));
    panel.style.setProperty("--assist-kb", kb + "px");
    panel.style.setProperty("--assist-vh", vv.height + "px");
    scroll();
  }
  if (vv) {
    vv.addEventListener("resize", fitViewport);
    vv.addEventListener("scroll", fitViewport);
  }

  function open() {
    panel.hidden = false;
    document.body.classList.add("assist-open");
    fab.setAttribute("aria-expanded", "true");
    fitViewport();
    if (!opened) {
      opened = true;
      firstOpen();
    }
    input.focus();
  }
  function close() {
    panel.hidden = true;
    document.body.classList.remove("assist-open");
    fab.setAttribute("aria-expanded", "false");
    fitViewport();
    fab.focus();
  }

  fab.addEventListener("click", open);
  $("#assist-close").addEventListener("click", close);
  if (restartBtn) restartBtn.addEventListener("click", function () { if (!busy) restart(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panel.hidden) close();
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q || busy) return;   // keep the text while the bot is still typing
    input.value = "";
    handle(q, q, true);
  });

  // Requests that failed to send on an earlier visit go out now.
  flushQueue();
  window.addEventListener("online", flushQueue);
})();
