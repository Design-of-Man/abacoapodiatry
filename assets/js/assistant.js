/* Jupiter Laser virtual assistant.
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
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "book",
      match: ["book", "appointment", "schedule", "visit", "come in", "see the doctor", "consultation", "availab"],
      a: "The fastest way to book is to call " + PHONE_HTML + " — most new patients are seen <strong>within the week</strong>. You can also <a href='/contact/'>request an appointment online</a> and our team will call you back to confirm.",
      chips: ["What should I bring?", "Where are you located?", "What are your hours?"]
    },
    {
      id: "location",
      match: ["where", "located", "location", "address", "directions", "parking", "office"],
      a: "We're at <strong>4601 Military Trail, Suite 202, Jupiter, FL 33458</strong> — minutes from Abacoa and I-95, with free on-site parking. Our sister office is at 11380 Prosperity Farms Rd, Suite 204, Palm Beach Gardens.<ul><li><a href='/contact/'>Map &amp; directions</a></li><li><a href='/locations/'>All areas we serve</a></li></ul>",
      chips: ["What are your hours?", "Book an appointment"]
    },
    {
      id: "hours",
      match: ["hours", "open", "close", "weekend", "saturday", "sunday", "lunch"],
      a: "<strong>Monday–Thursday:</strong> 8:00 AM – 5:00 PM<br><strong>Friday:</strong> 8:00 AM – 2:00 PM<br>Closed for lunch 12:30–1:30 PM, closed weekends and holidays. Call " + PHONE_HTML + " to schedule.",
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
      chips: ["Is it painful?", "How much does it cost?", "Book an appointment"]
    },
    {
      id: "flatfeet",
      match: ["flat feet", "flat foot", "flatfoot", "fallen arch", "arches", "pttd"],
      a: "Flat feet that ache, tire quickly, or roll inward deserve evaluation — especially if the arch is newly lowering (often a failing posterior tibial tendon). Care runs from custom orthotics and bracing to full flatfoot reconstruction by our surgeons.<ul><li><a href='/conditions/flat-feet/'>Flat feet treatment</a></li></ul>",
      chips: ["Book an appointment", "What conditions do you treat?"]
    },
    {
      id: "wound",
      match: ["wound", "ulcer", "sore that won't heal", "not healing", "open sore"],
      a: "Any wound that hasn't clearly improved in two weeks — or <strong>any wound on a diabetic foot</strong> — should be seen promptly. Our advanced wound care program includes debridement, offloading, biologics, and limb preservation. Please call " + PHONE_HTML + " today rather than waiting.<ul><li><a href='/services/wound-care/'>Wound care program</a></li></ul>",
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
      match: ["referral", "refer", "hmo", "pcp"],
      a: "Most patients <strong>don't need a referral</strong> to see a podiatrist. A few HMO plans require one — call " + PHONE_HTML + " and we'll help you check your plan.",
      chips: ["Book an appointment", "How much does it cost?"]
    },
    {
      id: "bring",
      match: ["bring", "first visit", "first appointment", "expect", "new patient"],
      a: "Bring a photo ID, insurance card, medication list, any prior imaging, and <strong>your most-worn shoes</strong> (wear patterns tell us a lot). Plan 45–60 minutes; laser treatment can often start the same day.<ul><li><a href='/new-patients/'>Your first visit, step by step</a></li></ul>",
      chips: ["Book an appointment", "What are your hours?"]
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

  var GREETING = "Hi! I'm the Jupiter Laser assistant. I can answer questions about our treatments, conditions we treat, costs, and booking. What's on your mind?";
  var FALLBACK = "I want to make sure you get an accurate answer, and that one's beyond me. The team can help in one call: " + PHONE_HTML + " (Mon–Thu 8–5, Fri 8–2). You can also browse the <a href='/faq/'>full FAQ</a> — it answers 60+ common questions.";
  var START_CHIPS = ["Tell me about laser therapy", "What conditions do you treat?", "How much does it cost?", "Book an appointment"];

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
    addMsg(q.replace(/&/g, "&amp;").replace(/</g, "&lt;"), "user");
    setChips([]);
    var typing = addMsg('<span class="assist-typing"><i></i><i></i><i></i></span>', "bot");
    window.setTimeout(function () {
      var res = answer(q);
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
