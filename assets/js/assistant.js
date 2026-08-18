/* Abacoa Podiatry virtual assistant.
   Self-contained concierge: keyword-matched answers grounded in the site's own
   pages. No external services, no data leaves the browser. */
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
      a: "We have two offices.<br><strong>Jupiter:</strong> 4601 Military Trail, Suite 202, Jupiter, FL 33458 — minutes from Abacoa and I-95, free on-site parking. Open Mon–Thu 8 AM–5 PM · Fri 8 AM–2 PM.<br><strong>Palm Beach Gardens:</strong> 11380 Prosperity Farms Rd, Suite 204, FL 33410. Open Mon &amp; Wed 8 AM–4:30 PM.<ul><li><a href='/locations/palm-beach-gardens/'>Palm Beach Gardens office</a></li><li><a href='/contact/'>Map &amp; directions</a></li><li><a href='/locations/'>All areas we serve</a></li></ul>",
      chips: ["What are your hours?", "Book an appointment"]
    },
    {
      id: "hours",
      match: ["hours", "open", "close", "weekend", "saturday", "sunday", "lunch"],
      // Two offices on different schedules. Kept in step with _src/hours.py by
      // a check in _dev/preflight.py -- this file is not generated by build.py,
      // so nothing else would catch it drifting.
      a: "<strong>Jupiter</strong> (4601 Military Trail): Mon–Thu 8 AM–5 PM · Fri 8 AM–2 PM, closed for lunch 12:30–1:30 PM.<br><strong>Palm Beach Gardens</strong> (11380 Prosperity Farms Rd): Mon &amp; Wed 8 AM–4:30 PM — closed Tue, Thu, Fri.<br>Both closed weekends and holidays. Call " + PHONE_HTML + " to schedule at either office.",
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
      a: "We offer <strong>PRP</strong> (your own concentrated growth factors) and <strong>regenerative cell therapies</strong> for tendons, fascia, and joints that have stopped healing — honest, surgeon-supervised, and only recommended when the evidence supports it for your diagnosis.<ul><li><a href='/services/prp-therapy/'>PRP therapy</a></li><li><a href='/services/stem-cell-therapy/'>Stem cell therapy</a></li></ul>",
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

  var GREETING = "Hi! I'm the Abacoa Podiatry assistant. I can answer questions about our treatments, conditions we treat, costs, and booking. What's on your mind?";
  var FALLBACK = "I want to make sure you get an accurate answer, and that one's beyond me. The team can help in one call: " + PHONE_HTML + " (Jupiter office Mon–Thu 8–5, Fri 8–2). You can also browse the<a href='/faq/'>full FAQ</a> — it answers 60+ common questions.";
  var START_CHIPS = ["Tell me about laser therapy", "What conditions do you treat?", "How much does it cost?", "Book an appointment"];

  /* --- Lead capture: a tiny state machine layered on top of the same
     #assist-input/#assist-form text box. When `capture` is non-null, the
     next submitted message is consumed as a form field instead of being run
     through answer(). Mirrors the /contact/ form's exact POST contract
     (assets/js/main.js ~L386-435, api/contact.js) so success/failure read
     the same way. */
  var LEAD_TRIGGER_RE = /leave your info|call you back/i;
  var LEAD_LIMITS = { name: 200, phone: 50, reason: 120, message: 4000 };
  var CANCEL_CHIP = "Never mind";
  var capture = null;          // { step, name, phone, reason, message }
  var lastQuestion = "";       // most recent free-text question, threaded through as the lead's "reason"

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  }

  function isCancelWord(t) {
    var n = t.trim().toLowerCase();
    return n === "cancel" || n === "nevermind" || n === "never mind" || n === CANCEL_CHIP.toLowerCase();
  }

  function typingBubble() {
    return addMsg('<span class="assist-typing"><i></i><i></i><i></i></span>', "bot");
  }

  function cancelCapture(typing) {
    capture = null;
    typing.innerHTML = "No problem — what else can I help with?";
    setChips(START_CHIPS);
    scroll();
  }

  function beginCapture() {
    capture = { step: "name", reason: (lastQuestion || "").slice(0, LEAD_LIMITS.reason) };
    var typing = typingBubble();
    window.setTimeout(function () {
      typing.innerHTML = "Happy to have our team call you back. What's your name?";
      setChips([CANCEL_CHIP]);
      scroll();
    }, 450);
  }

  function submitLead(typing) {
    var payload = {
      name: capture.name,
      phone: capture.phone,
      reason: (capture.reason || "").slice(0, LEAD_LIMITS.reason),
      message: capture.message || "",
      source: "assistant"
    };
    fetch("/api/contact/", {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json", Accept: "application/json" }
    }).then(function (r) {
      if (!r.ok) throw new Error("http " + r.status);
      return r.json();
    }).then(function (data) {
      // success comes back as the string "true", same contract as the contact form.
      var delivered = data && String(data.success).toLowerCase() === "true";
      if (!delivered) throw new Error("not delivered");
      typing.innerHTML = "Got it, " + escapeHtml(capture.name) + " — our team will call you back at " +
        escapeHtml(capture.phone) + " to confirm. Talk soon!";
      setChips(START_CHIPS);
      capture = null;
      scroll();
    }).catch(function () {
      typing.innerHTML = "Something went wrong sending that through. Please call us directly at " + PHONE_HTML +
        " and we'll take care of you.";
      setChips(START_CHIPS);
      capture = null;
      scroll();
    });
  }

  function handleCaptureInput(text) {
    if (isCancelWord(text)) {
      cancelCapture(typingBubble());
      return;
    }
    var typing = typingBubble();
    if (capture.step === "name") {
      window.setTimeout(function () {
        capture.name = text.slice(0, LEAD_LIMITS.name);
        capture.step = "phone";
        typing.innerHTML = "Thanks, " + escapeHtml(capture.name) + ". What's the best phone number to reach you?";
        setChips([CANCEL_CHIP]);
        scroll();
      }, 450);
    } else if (capture.step === "phone") {
      window.setTimeout(function () {
        capture.phone = text.slice(0, LEAD_LIMITS.phone);
        capture.step = "reason";
        typing.innerHTML = 'Got it. Anything specific you\'d like us to know before we call? (Or type "skip".)';
        setChips(["Skip", CANCEL_CHIP]);
        scroll();
      }, 450);
    } else if (capture.step === "reason") {
      capture.message = /^skip$/i.test(text.trim()) ? "" : text.slice(0, LEAD_LIMITS.message);
      window.setTimeout(function () { submitLead(typing); }, 450);
    }
  }

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var fab = $("#assist-open"), panel = $("#assist-panel");
  if (!fab || !panel) return;
  var log = $("#assist-log"), chipsBox = $("#assist-chips"),
      form = $("#assist-form"), input = $("#assist-input");
  var opened = false;

  function scroll() { log.scrollTop = log.scrollHeight; }

  function addMsg(html, who) {
    var el = document.createElement("div");
    el.className = "assist-msg " + who;
    el.innerHTML = html;
    log.appendChild(el);
    scroll();
    return el;
  }

  function setChips(labels) {
    chipsBox.innerHTML = "";
    (labels || []).forEach(function (label) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "assist-chip";
      b.textContent = label;
      b.addEventListener("click", function () { ask(label); });
      chipsBox.appendChild(b);
    });
  }

  function answer(q) {
    var norm = q.toLowerCase();
    var best = null, bestScore = 0;
    TOPICS.forEach(function (topic) {
      var score = 0;
      topic.match.forEach(function (term) {
        if (norm.indexOf(term) !== -1) score += term.length; // longer term = stronger signal
      });
      if (score > bestScore) { bestScore = score; best = topic; }
    });
    return best || { a: FALLBACK, chips: START_CHIPS };
  }

  function ask(q) {
    var trimmed = q.trim();
    if (!trimmed) return;
    addMsg(escapeHtml(trimmed), "user");
    setChips([]);

    // Mid-capture: the next message is a form field, not a question.
    if (capture) {
      handleCaptureInput(trimmed);
      return;
    }

    // Entry point into lead capture, from the "Leave your info…" chip or
    // someone typing the same intent.
    if (LEAD_TRIGGER_RE.test(trimmed)) {
      beginCapture();
      return;
    }

    lastQuestion = trimmed;
    var typing = typingBubble();
    window.setTimeout(function () {
      var res = answer(trimmed);
      typing.innerHTML = res.a;
      setChips(res.chips || START_CHIPS);
      scroll();
    }, 550);
  }

  function open() {
    panel.hidden = false;
    document.body.classList.add("assist-open");
    fab.setAttribute("aria-expanded", "true");
    if (!opened) {
      opened = true;
      addMsg(GREETING, "bot");
      setChips(START_CHIPS);
    }
    input.focus();
  }
  function close() {
    panel.hidden = true;
    document.body.classList.remove("assist-open");
    fab.setAttribute("aria-expanded", "false");
    fab.focus();
  }

  fab.addEventListener("click", open);
  $("#assist-close").addEventListener("click", close);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panel.hidden) close();
  });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q) return;
    input.value = "";
    ask(q);
  });
})();
