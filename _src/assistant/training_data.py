"""
Abacoa Podiatry & Leg Vein Center — AI assistant training dataset
=================================================================

Variable-based intent dataset for training / grounding the site assistant
("Abacoa Podiatry Assistant" on jupiterlaser.com).

Structure
---------
PRACTICE   : every practice fact lives here ONCE. Answers reference these as
             {placeholders}, so a phone/hours/doctor change is a one-line edit.
SLOTS      : variable lists used inside question templates ({nail_color},
             {side}, {duration}...). Expanded into many phrasings per intent.
INTENTS    : one Intent per topic. Each has MANY questions (user phrasings,
             may contain {slots}) and MANY answers (equivalent variants the
             model can learn from / rotate between).

Fields worth knowing
--------------------
urgency    : "routine" | "soon" | "urgent" | "emergency" — lets the agent
             escalate correctly.
verify     : True = general podiatry content NOT yet confirmed on the live site
             (e.g. whether a specific procedure is offered). Have Dr. Cedeno /
             the front desk sign off before training on these.
follow_ups : what the agent should ask next to narrow things down.

Grounding: practice facts and treatment details pulled from jupiterlaser.com
(home, FAQ, Foot BBL pages) on 2026-10-07.

Usage
-----
    python3 _src/assistant/training_data.py              # validate + export
    python3 _src/assistant/training_data.py --stats      # counts only
    python3 _src/assistant/training_data.py --ask "my heel hurts in the morning"

Validation also fails on any jupiterlaser.com link with no matching page in
this repo, so the assistant never sends a patient to a 404.

Exports (to _src/assistant/training_out/, git-ignored; regenerate any time):
    chat_finetune.jsonl   system/user/assistant message records
    qa_pairs.jsonl        flat question -> answer pairs with metadata
    knowledge_base.json   one doc per intent (for RAG / vector store)
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. PRACTICE VARIABLES — single source of truth
# ---------------------------------------------------------------------------

PRACTICE = {
    "practice_name": "Abacoa Podiatry & Leg Vein Center",
    "short_name": "Abacoa Podiatry",
    "site": "https://jupiterlaser.com",
    "phone": "(561) 915-1934",
    "phone_note": "call or text",
    "email": "angela.d@jupiterlaser.com",
    "portal_url": "https://abacoapodiatry.modmedapp.com/",
    "booking_url": "https://jupiterlaser.com/contact/",
    "new_patient_url": "https://jupiterlaser.com/new-patients/",
    "faq_url": "https://jupiterlaser.com/faq/",
    "telehealth_url": "https://jupiterlaser.com/telehealth/",
    "locations_url": "https://jupiterlaser.com/locations/",
    "media_url": "https://jupiterlaser.com/media/",
    # Offices
    "jupiter_address": "4601 Military Trail, Suite 202, Jupiter, FL 33458",
    "jupiter_landmarks": "on Military Trail between Donald Ross Rd and Frederick Small Rd, minutes from Abacoa and I-95, free parking on site",
    "jupiter_hours": "Mon–Thu 8 AM–5 PM, Fri 8 AM–2 PM",
    "pbg_address": "11380 Prosperity Farms Rd, Suite 204, Palm Beach Gardens, FL 33410",
    "pbg_hours": "Mon–Wed 8 AM–4:30 PM, Fri 8 AM–2 PM (closed Thursday)",
    "weekend_hours": "Saturday by concierge appointment only at both offices; closed Sunday and holidays",
    # Doctors
    "dr1": "Dr. Orlando Cedeno, DPM, FACFAS",
    "dr1_short": "Dr. Cedeno",
    "dr1_bio": "a board-certified podiatric foot & ankle surgeon and the practice founder",
    "dr1_url": "https://jupiterlaser.com/meet-dr-cedeno/",
    "dr2": "Dr. Isin A. Mustafa, DPM, MSHS, DABPM, DACFAS",
    "dr2_short": "Dr. Mustafa",
    "dr2_bio": "a foot & ankle surgeon with a three-year PMSR/RRA surgical residency and a focus on minimally invasive surgery and regenerative medicine",
    "dr2_url": "https://jupiterlaser.com/meet-dr-mustafa/",
    # Sister practices
    "ortho_name": "ELITE Sports Medicine",
    "ortho_doc": "Dr. Marc F. Matarazzo, MD",
    "ortho_url": "https://elitesportsmed.org/",
    "regen_name": "RegenOrtho Palm Beach",
    "regen_url": "https://regenorthopb.com/",
    "vein_url": "https://jupiterveincenter.com/",
    # Service / condition pages
    "url_mls": "https://jupiterlaser.com/services/mls-laser-therapy/",
    "url_epat": "https://jupiterlaser.com/services/shockwave-therapy/",
    "url_prp": "https://jupiterlaser.com/services/prp-therapy/",
    "url_regen": "https://jupiterlaser.com/services/regenerative-medicine/",
    "url_bbl": "https://jupiterlaser.com/services/foot-bbl/",
    "url_surgery": "https://jupiterlaser.com/services/foot-ankle-surgery/",
    "url_wound": "https://jupiterlaser.com/services/wound-care/",
    "url_pf": "https://jupiterlaser.com/conditions/plantar-fasciitis/",
    "url_heel": "https://jupiterlaser.com/conditions/heel-pain/",
    "url_neuro": "https://jupiterlaser.com/conditions/neuropathy/",
    "url_achilles": "https://jupiterlaser.com/conditions/achilles-tendonitis/",
    "url_arthritis": "https://jupiterlaser.com/conditions/arthritis/",
    "url_sports": "https://jupiterlaser.com/conditions/sports-injuries/",
    "url_bunions": "https://jupiterlaser.com/conditions/bunions/",
    "url_flatfeet": "https://jupiterlaser.com/conditions/flat-feet/",
    "url_sprains": "https://jupiterlaser.com/conditions/sprains-strains/",
    "url_diabetic": "https://jupiterlaser.com/conditions/diabetic-foot-care/",
    # Treatment facts
    "mls_session": "10–15 minutes",
    "mls_course": "6–12 sessions, 2–3 times per week",
    "regen_timeline": "first improvement around 4–6 weeks, with gains continuing for 3–6 months",
    "bbl_duration": "typically 18–24+ months, and refreshable",
    "cta": "Call or text {phone} or book at {booking_url}.",
    "disclaimer": "This is general information, not a diagnosis.",
}

# ---------------------------------------------------------------------------
# 2. SLOT VARIABLES — expanded inside question templates
# ---------------------------------------------------------------------------

SLOTS = {
    "side": ["left", "right", "both"],
    "toe": ["big toe", "second toe", "pinky toe", "toes"],
    "nail_color": ["yellow", "white", "brown", "black", "purple", "green", "dark"],
    "duration": ["a few days", "two weeks", "a month", "several months", "over a year"],
    "pain_level": ["slight", "mild", "bad", "sharp", "throbbing", "constant"],
    "activity": ["running", "walking", "standing all day", "playing pickleball", "playing tennis", "golfing", "working out"],
    "shoe": ["heels", "work boots", "flip flops", "running shoes", "dress shoes"],
    "town": ["Jupiter", "Abacoa", "Palm Beach Gardens", "Tequesta", "Juno Beach", "North Palm Beach",
             "Hobe Sound", "Stuart", "West Palm Beach", "Palm City", "Riviera Beach"],
    "time_of_day": ["in the morning", "at night", "after sitting", "at the end of the day"],
    "family": ["my mom", "my dad", "my husband", "my wife", "my son", "my daughter"],
}

# ---------------------------------------------------------------------------
# 3. INTENT MODEL
# ---------------------------------------------------------------------------

@dataclass
class Intent:
    id: str
    category: str
    questions: list[str]
    answers: list[str]
    urgency: str = "routine"          # routine | soon | urgent | emergency
    urls: list[str] = field(default_factory=list)   # PRACTICE keys or raw URLs
    follow_ups: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    verify: bool = False              # needs practice sign-off before training


C = "{cta}"  # shorthand appended to answers that should end with a booking CTA

INTENTS: list[Intent] = [

    # ======================= PRACTICE & LOGISTICS ==========================
    Intent(
        id="practice_overview", category="practice_info",
        questions=[
            "What does {short_name} do?",
            "What kind of doctor is this?",
            "What services do you offer?",
            "Are you a podiatrist?",
            "What do you treat?",
            "Tell me about your practice",
            "Is this a foot doctor?",
        ],
        answers=[
            "{practice_name} is a foot & ankle practice in Jupiter and Palm Beach Gardens. We treat heel pain, plantar fasciitis, neuropathy, Achilles problems, bunions, arthritis, sports injuries, diabetic foot issues and leg veins, using MLS laser, EPAT shockwave, PRP and regenerative medicine, and minimally invasive surgery when it's truly needed. " + C,
            "We're podiatrists: foot and ankle specialists led by surgeons {dr1} and {dr2}. Our approach is diagnosis first, conservative care before surgery, and tracking progress every visit. " + C,
            "Everything from the ankle down, plus leg vein care. That covers heel and arch pain, toes and nails, sprains, tendon injuries, nerve pain, diabetic foot care, and surgery like bunion correction. Want help figuring out whether your issue is something we treat?",
        ],
        urls=["site"], tags=["about"],
    ),
    Intent(
        id="doctors", category="practice_info",
        questions=[
            "Who are the doctors?",
            "Who is {dr1_short}?",
            "Who is {dr2_short}?",
            "Is the doctor board certified?",
            "Which doctor should I see?",
            "Are your doctors surgeons?",
            "Can I see {dr1_short} specifically?",
        ],
        answers=[
            "Care is led by two foot & ankle surgeons: {dr1}, {dr1_bio}, and {dr2}, {dr2_bio}. You can request either doctor when you book at {phone}.",
            "{dr1_short} is {dr1_bio}. {dr2_short} is {dr2_bio}. Both see patients at our offices. Learn more at {dr1_url} and {dr2_url}.",
            "Yes, both are foot & ankle surgeons, which means that when they recommend non-surgical care, it's because you don't need surgery, not because they can't do it. To request a specific doctor, call {phone}.",
        ],
        urls=["dr1_url", "dr2_url"], tags=["about", "doctors"],
    ),
    Intent(
        id="locations_hours", category="practice_info",
        questions=[
            "Where are you located?",
            "What are your hours?",
            "Are you open today?",
            "Are you open on Saturday?",
            "Are you open Thursday in Palm Beach Gardens?",
            "What's your address?",
            "Do you have an office in Palm Beach Gardens?",
            "How do I get to the Jupiter office?",
            "Is there parking?",
        ],
        answers=[
            "We have two offices.\n• Jupiter: {jupiter_address} ({jupiter_hours})\n• Palm Beach Gardens: {pbg_address} ({pbg_hours})\n{weekend_hours}. Call {phone} and we'll book whichever is more convenient.",
            "Our main office is at {jupiter_address}, {jupiter_landmarks}. Hours: {jupiter_hours}. The Palm Beach Gardens office is open {pbg_hours}. {weekend_hours}.",
            "Jupiter is open {jupiter_hours}; Palm Beach Gardens is open {pbg_hours}. On days Palm Beach Gardens is closed, Jupiter is 10–15 minutes north. Directions: {locations_url}",
        ],
        urls=["locations_url"], tags=["hours", "address"],
    ),
    Intent(
        id="service_area", category="practice_info",
        questions=[
            "I live in {town}, is it worth the drive?",
            "Do you see patients from {town}?",
            "How far are you from {town}?",
            "Is there a podiatrist near {town}?",
            "Foot doctor near me",
        ],
        answers=[
            "Yes, we see patients from all over the northern Palm Beaches and the Treasure Coast, from West Palm Beach to Stuart. Robotic MLS laser, EPAT shockwave and surgeon-supervised regenerative care are hard to find in that stretch. Drive times by city: {locations_url}",
            "We regularly see patients from {town}. Pick whichever office is closer: Jupiter ({jupiter_address}) or Palm Beach Gardens ({pbg_address}). " + C,
        ],
        urls=["locations_url"], tags=["local"],
    ),
    Intent(
        id="contact", category="practice_info",
        questions=[
            "What's your phone number?",
            "How do I contact you?",
            "Can I text you?",
            "What's your email?",
            "Is the old 624-4800 number still working?",
        ],
        answers=[
            "Call or text {phone}. You can also email {email} or send a message at {booking_url}.",
            "The best number is {phone} (call or text). Our old (561) 624-4800 number is no longer in service.",
        ],
        tags=["contact"],
    ),

    # ======================= BOOKING & VISITS ===============================
    Intent(
        id="book_appointment", category="booking",
        questions=[
            "How do I book an appointment?",
            "I want to make an appointment",
            "Can I schedule online?",
            "How soon can I be seen?",
            "Do you have anything this week?",
            "I need to see a podiatrist",
            "Can {family} get an appointment?",
        ],
        answers=[
            "Call or text {phone}, or request a time at {booking_url}. Most new patients are seen within the week, and acute injuries often sooner.",
            "Happy to help you get in. The fastest way is {phone}; you can also use the request form at {booking_url}. Same-week appointments are usually available.",
            "Book at {booking_url} or call {phone}. Tell us what's going on (for example, heel pain or an ingrown nail) and we'll match you to the right visit type.",
        ],
        urls=["booking_url"], tags=["booking", "cta"],
    ),
    Intent(
        id="first_visit", category="booking",
        questions=[
            "What happens at the first visit?",
            "What should I bring to my appointment?",
            "What do I need for a new patient visit?",
            "How long is the first appointment?",
            "Can I start treatment the same day?",
            "Should I bring my shoes?",
        ],
        answers=[
            "Your first visit includes a focused history, a hands-on exam, imaging if needed, a clear explanation of what's wrong, and a written plan with options and costs. Laser treatment can often start the same day. Bring a photo ID, insurance card, medication list, any prior imaging, and the shoes you wear most, since the wear pattern tells us a lot.",
            "Bring an ID, insurance card, medication list, past X-rays or MRI reports, and your most-worn shoes. Expect an exam, a diagnosis, and a written plan with costs before anything starts. Details: {new_patient_url}",
        ],
        urls=["new_patient_url"], tags=["new_patient"],
    ),
    Intent(
        id="referral", category="booking",
        questions=[
            "Do I need a referral?",
            "Does my doctor have to refer me?",
            "I have an HMO, do I need a referral?",
        ],
        answers=[
            "Most patients don't. You can see a podiatrist directly. A few HMO plans do require a referral; call {phone} and we'll check your plan for you.",
            "Usually no referral is needed. If you're on an HMO, call us first and we'll confirm what your plan requires.",
        ],
        tags=["insurance", "booking"],
    ),
    Intent(
        id="telehealth", category="booking",
        questions=[
            "Do you do telehealth?",
            "Can I do a virtual visit?",
            "Can I send a picture of my foot?",
            "Can I talk to the doctor online?",
        ],
        answers=[
            "Yes, for visits that don't need a hands-on exam: follow-ups, results reviews, wound-photo checks, and \"should I come in?\" questions. Details at {telehealth_url}.",
            "Telehealth works well for follow-ups and quick checks, including reviewing photos. New problems usually need an in-person exam first. Call {phone} to set it up.",
        ],
        urls=["telehealth_url"], tags=["telehealth"],
    ),
    Intent(
        id="portal", category="booking",
        questions=[
            "Where is the patient portal?",
            "How do I log into the portal?",
            "Can I see my records online?",
            "How do I fill out paperwork before my visit?",
        ],
        answers=[
            "The patient portal is at {portal_url}. If you have trouble logging in, call {phone} and the front desk will help.",
        ],
        urls=["portal_url"], tags=["portal"],
    ),
    Intent(
        id="accessibility_family", category="booking",
        questions=[
            "Is the office wheelchair accessible?",
            "Can my family member come with me?",
            "Can my daughter join by phone?",
            "Do you speak Spanish?",
            "Do you have interpreters?",
        ],
        answers=[
            "Both offices are wheelchair accessible, with parking close to the entrance. Family members are welcome in the room or by phone, which is especially helpful when weighing treatment options.",
            "Yes. Tell us about any accessibility or language needs when you book at {phone} and we'll arrange it, including interpretation when needed.",
        ],
        tags=["accessibility"],
    ),

    # ======================= COST & INSURANCE ===============================
    Intent(
        id="insurance", category="insurance_cost",
        questions=[
            "Do you take insurance?",
            "Do you take Medicare?",
            "Is my insurance accepted?",
            "Will insurance cover my visit?",
            "Do you accept Blue Cross?",
        ],
        answers=[
            "Your evaluation and most standard podiatric care are typically covered by insurance. Call {phone} with your plan details and we'll verify your benefits before your visit.",
            "We work with insurance for evaluations and standard podiatry care. Coverage varies by plan, so the quickest way to confirm is to call {phone}; we'll check your benefits first.",
        ],
        follow_ups=["Which insurance plan do you have?"],
        tags=["insurance"], verify=True,
    ),
    Intent(
        id="cost_advanced", category="insurance_cost",
        questions=[
            "How much does laser therapy cost?",
            "Does insurance cover shockwave?",
            "Is PRP covered by insurance?",
            "What's the price of treatment?",
            "Do you have payment plans?",
            "Can I use my HSA or FSA?",
            "Do you take CareCredit?",
        ],
        answers=[
            "Laser, shockwave and regenerative therapies are usually elective and out of pocket, because most insurers classify them as emerging treatments. We quote exact package pricing up front before you commit, with no surprise bills. Call {phone} for current pricing.",
            "When these treatments are prescribed for a medical condition, they're generally HSA/FSA-eligible; confirm with your plan administrator and we'll provide the documentation. Ask the front desk at {phone} about packages and payment options.",
            "Pricing depends on your condition and plan length, so we give you the full cost picture at your evaluation, before anything starts. Financing such as CareCredit is available for some procedures.",
        ],
        tags=["cost"],
    ),
    Intent(
        id="auto_accident_wc", category="insurance_cost",
        questions=[
            "I hurt my foot in a car accident",
            "Do you treat auto accident injuries?",
            "Do you take PIP?",
            "Do you take workers comp?",
            "I hurt my ankle at work",
        ],
        answers=[
            "Yes, we treat foot and ankle injuries from auto accidents and work injuries. Call {phone} with your claim information so we can set up billing correctly.",
            "We see auto accident and workers' comp foot and ankle injuries. Bring your claim number and adjuster info when you call {phone}.",
        ],
        urls=["booking_url"], tags=["pip", "workers_comp"],
    ),

    # ======================= SAFETY / TRIAGE ================================
    Intent(
        id="emergency", category="triage", urgency="emergency",
        questions=[
            "I can't put any weight on my foot",
            "I heard a pop in my ankle and now it's weak",
            "My foot is cold and blue",
            "There are red streaks going up my leg",
            "I have a fever and my foot is swollen and red",
            "My calf is swollen, hot and painful",
            "Is this an emergency?",
            "When should I go to the ER for foot pain?",
        ],
        answers=[
            "That needs prompt care. If you have a cold/blue foot, spreading redness or red streaks with fever, a swollen painful calf, chest pain or shortness of breath, call 911 or go to the nearest ER now. For a suspected break or a \"pop\" with sudden weakness, call us right away at {phone} and we'll tell you where you need to be.",
            "Signs that need same-day care: you can't bear weight, you felt a pop followed by weakness, there's spreading redness or red streaks, you have a fever with foot pain, your foot is cold or blue, or there's any wound on a diabetic foot. If it feels life- or limb-threatening, call 911. Otherwise call {phone} now.",
        ],
        tags=["red_flag", "escalate"],
    ),
    Intent(
        id="diagnose_me", category="triage",
        questions=[
            "What's wrong with my foot?",
            "Can you diagnose me?",
            "Do I need surgery?",
            "What medication should I take?",
            "Should I take antibiotics?",
        ],
        answers=[
            "I can't diagnose you here, but I can explain common causes and help you get seen quickly. Can you tell me where it hurts, how long it's been going on, and whether there was an injury? For an actual diagnosis, book an evaluation with {dr1_short} or {dr2_short} at {phone}.",
            "Medication and surgery decisions need an exam by one of our doctors. I'm happy to share general information in the meantime, and the doctor can give you a real answer within the week. " + C,
        ],
        follow_ups=["Where on the foot is the pain?", "How long has it been going on?", "Was there an injury?"],
        tags=["guardrail"],
    ),

    # ======================= HEEL & ARCH ====================================
    Intent(
        id="plantar_fasciitis", category="heel_arch", urgency="soon",
        questions=[
            "My heel hurts {time_of_day}",
            "Stabbing heel pain with the first steps in the morning",
            "What is plantar fasciitis?",
            "How do you treat plantar fasciitis?",
            "My heel has hurt for {duration}",
            "Heel pain after {activity}",
            "Will my plantar fasciitis go away on its own?",
            "Is it OK to exercise with plantar fasciitis?",
        ],
        answers=[
            "Sharp heel pain on your first steps in the morning, or after sitting, is the classic sign of plantar fasciitis. The fascia tightens at rest, and those first steps re-stretch the injured tissue. It's the most common cause of heel pain and one of the most treatable. We use MLS laser, EPAT shockwave, PRP, stretching, footwear changes and orthotics when needed. " + C,
            "Plantar fasciitis is irritation of the thick band along the bottom of your foot. Most cases resolve without surgery. Chronic ones respond well to shockwave and laser, which break up scar tissue and restart healing. You can usually keep exercising in a modified way. More: {url_pf}",
            "{disclaimer} Heel pain that has lasted weeks usually means the tissue is stuck in a chronic cycle, and that's when shockwave or laser helps most. We'll also look at the cause (shoes, load, foot mechanics) so it doesn't come back. " + C,
        ],
        follow_ups=["Is it worst with the first steps in the morning?", "How long has it been going on?"],
        urls=["url_pf", "url_epat", "url_mls"], tags=["heel", "plantar_fasciitis"],
    ),
    Intent(
        id="heel_spur", category="heel_arch",
        questions=[
            "Do I have a heel spur?",
            "Do heel spurs need to be removed?",
            "My X-ray showed a heel spur",
            "Can a heel spur be treated without surgery?",
        ],
        answers=[
            "Heel spurs rarely need to be removed. Spurs show up on X-rays of plenty of pain-free feet; the pain almost always comes from the soft tissue (the fascia), not the bone. Treat the fascia and the pain usually resolves, spur and all. More: {url_heel}",
            "A spur on an X-ray isn't usually what hurts. We focus on the inflamed tissue around it with laser, shockwave and mechanics fixes. Surgery is rarely needed. " + C,
        ],
        urls=["url_heel"], tags=["heel"],
    ),
    Intent(
        id="heel_pain_other", category="heel_arch", urgency="soon",
        questions=[
            "Pain at the back of my heel",
            "My child's heel hurts after sports",
            "Heel pain with numbness",
            "Heel pain that isn't plantar fasciitis",
            "Bump on the back of my heel",
        ],
        answers=[
            "Heel pain has several causes besides plantar fasciitis: Achilles insertional tendonitis or a bump at the back of the heel, nerve entrapment (burning or numbness), a stress fracture (pain with squeezing the heel), fat pad thinning, and Sever's disease in active kids. The location of the pain is the biggest clue. Can you tell me exactly where it hurts? Overview: {url_heel}",
            "Back-of-heel pain often points to the Achilles insertion or a heel bump (Haglund's). Burning or tingling suggests a nerve. In kids 8–14, it's often Sever's (growth plate irritation). Each one is treated differently, so an exam is worth it. " + C,
        ],
        follow_ups=["Is the pain on the bottom or back of the heel?", "Any numbness or burning?"],
        urls=["url_heel"], tags=["heel"],
    ),
    Intent(
        id="arch_pain_flat_feet", category="heel_arch",
        questions=[
            "My arch hurts",
            "Do I have flat feet?",
            "My arches are collapsing",
            "Flat feet in adults",
            "Pain on the inside of my ankle and arch",
            "My child has flat feet",
            "Do I need orthotics for flat feet?",
        ],
        answers=[
            "Arch pain is usually plantar fasciitis, posterior tibial tendon strain, or fallen arches. Left untreated, it changes how you walk and can send pain up to the knees, hips and back. Flat feet that hurt, or arches that are getting flatter over time, deserve an exam. Treatments range from supportive shoes and orthotics to laser and, rarely, reconstruction. More: {url_flatfeet}",
            "Flat feet themselves aren't a problem if they don't hurt. Pain along the inside of the ankle and arch, or an arch that's newly collapsing, can mean the posterior tibial tendon is failing, and that's worth catching early. " + C,
        ],
        urls=["url_flatfeet"], tags=["arch", "flat_feet"],
    ),
    Intent(
        id="high_arches", category="heel_arch", verify=True,
        questions=[
            "I have very high arches",
            "Pain from high arches",
            "My ankles keep rolling and I have high arches",
        ],
        answers=[
            "High arches (cavus foot) concentrate pressure on the heel and ball of the foot and can make ankles prone to rolling. Cushioned, stable shoes and custom orthotics help most people; we also check for tendon or nerve causes. " + C,
        ],
        tags=["arch"],
    ),

    # ======================= FOREFOOT =======================================
    Intent(
        id="bunions", category="forefoot", urgency="routine",
        questions=[
            "I have a bunion",
            "Bump on the side of my big toe",
            "Do bunions need surgery?",
            "What is minimally invasive bunion surgery?",
            "How long is recovery from bunion surgery?",
            "My bunion hurts in {shoe}",
            "Can bunions be fixed without surgery?",
            "Tailor's bunion on my pinky toe",
        ],
        answers=[
            "A bunion is a misalignment of the big toe joint that creates a bump on the side of the foot. Wider shoes, padding and orthotics can ease symptoms, but they don't reverse the deformity. When it hurts or limits activity, our surgeons offer bunion correction, including minimally invasive techniques with small incisions. More: {url_bunions}",
            "Bunion correction is one of our specialties (our Instagram is @bunionboss_abacoapodiatry). Minimally invasive surgery uses tiny incisions; recovery depends on the technique and your foot, and the surgeon will go over your timeline at the consult. " + C,
            "{disclaimer} If your bunion is painful, growing, or making shoes hard to wear, it's worth an evaluation with X-rays to see how much correction you need. " + C,
        ],
        follow_ups=["Does it hurt, or is it mostly the look and shoe fit?"],
        urls=["url_bunions", "url_surgery"], tags=["bunion", "surgery"],
    ),
    Intent(
        id="ball_of_foot", category="forefoot", urgency="soon",
        questions=[
            "Pain in the ball of my foot",
            "Feels like I'm walking on a pebble",
            "Burning between my toes",
            "What is Morton's neuroma?",
            "What is metatarsalgia?",
            "Numbness between my third and fourth toes",
            "Pain under my big toe joint",
        ],
        answers=[
            "Ball-of-foot pain usually comes from metatarsalgia (overloaded metatarsal heads), Morton's neuroma (a pinched nerve, often burning or numbness between the 3rd and 4th toes), sesamoiditis (under the big toe joint), a stress fracture, or fat pad thinning. They feel similar but are treated differently, so an exam is the fastest path to relief. " + C,
            "That pebble-in-the-shoe or burning feeling is often a neuroma or fat pad thinning. Wider shoes and metatarsal pads help at first; after that we use targeted treatment based on the cause. " + C,
        ],
        follow_ups=["Is it burning or numb, or more of a bruised feeling?"],
        tags=["forefoot", "neuroma"], verify=True,
    ),
    Intent(
        id="fat_pad_bbl", category="forefoot",
        questions=[
            "What is a Foot BBL?",
            "It feels like I'm walking on bones",
            "I can't wear heels anymore",
            "My feet have lost their padding",
            "Fat pad atrophy treatment",
            "Does the Foot BBL use my own fat?",
            "How long does a Foot BBL last?",
            "How much is a Foot BBL?",
        ],
        answers=[
            "The Foot BBL™ is our in-office fat-pad restoration. It rebuilds the cushion under the ball of the foot or heel using Liposana™ (an allograft adipose matrix) or Sculptra (a collagen-stimulating injectable). It's done under local anesthesia in under an hour, with no liposuction and no donor site. Results typically last {bbl_duration}. More: {url_bbl}",
            "That walking-on-bones or marbles feeling, and heels you can't wear anymore, are classic signs of plantar fat pad atrophy. The Foot BBL™ restores the cushion. Recovery is short: offloading for a few days, most activities within a week, normal shoes by weeks 2–4.",
            "The Foot BBL™ is generally out of pocket; some medically documented cases may qualify for partial coverage. We give transparent pricing at the consultation, and financing such as CareCredit is available. " + C,
        ],
        urls=["url_bbl"], tags=["foot_bbl", "cosmetic"],
    ),

    # ======================= TOES & NAILS ===================================
    Intent(
        id="toenail_discoloration", category="toes_nails", urgency="soon",
        questions=[
            "Discoloration in my toenail",
            "My {toe} nail is {nail_color}",
            "{nail_color} toenail with {pain_level} pain",
            "Discoloration in my big toe nail, slight pain",
            "Dark spot under my toenail",
            "Black toenail after {activity}",
            "My toenail turned {nail_color} after I stubbed it",
            "Dark streak in my toenail",
        ],
        answers=[
            "Toenail discoloration usually comes from one of a few causes: trauma or shoe pressure (red, purple, brown or black from bleeding under the nail, common after running or a stubbed toe), fungus (yellow, white or brown, often with thickening or crumbling), an infection around the nail (green, red, swollen), or an ingrown nail. A dark streak or spot with no injury you can remember should be checked promptly to rule out something more serious. " + C,
            "{disclaimer} If you remember an injury, the dark area usually grows out with the nail over months. If the nail is thickening or turning yellow or white, fungus is likely. Any dark streak without an injury, redness, swelling or drainage, or if you have diabetes, is worth getting seen soon. Taking a photo now helps track changes. " + C,
            "A few questions will narrow it down: What color is it? Did you stub it or wear tight shoes? How long has it been there? Is the nail thicker or lifting? We can usually tell at the visit and test a clipping if fungus is suspected.",
        ],
        follow_ups=["What color is the discoloration?", "Any injury or tight shoes?", "Is the nail thick, crumbly or lifting?", "Do you have diabetes?"],
        tags=["nails", "red_flag_possible"],
    ),
    Intent(
        id="toenail_fungus", category="toes_nails",
        questions=[
            "Do I have toenail fungus?",
            "Thick yellow toenails",
            "How do you treat toenail fungus?",
            "Crumbly toenails",
            "Will my toenail fungus go away?",
            "Laser for toenail fungus",
        ],
        answers=[
            "Fungal nails usually turn yellow, white or brown and get thick, brittle or crumbly. They rarely clear on their own. Treatment depends on how many nails are involved and your health history; we can confirm fungus with a nail clipping test and go over options. " + C,
            "Thick, discolored, crumbly nails are often fungal, but psoriasis and repeated trauma can look the same, so testing matters before treatment. Nails grow slowly, so a clear nail takes months to grow in. " + C,
        ],
        tags=["nails", "fungus"], verify=True,
    ),
    Intent(
        id="ingrown_toenail", category="toes_nails", urgency="soon",
        questions=[
            "I have an ingrown toenail",
            "The side of my {toe} is red and swollen",
            "Pus around my toenail",
            "Should I cut out my ingrown toenail?",
            "My ingrown nail keeps coming back",
            "How do you fix an ingrown toenail?",
        ],
        answers=[
            "Ingrown toenails are a quick in-office fix. Under local numbing, the doctor removes the offending edge of the nail, and for nails that keep coming back can treat the root so that edge doesn't regrow. Please don't dig it out yourself, as that often makes it worse. If there's pus, spreading redness, or you have diabetes, get seen soon. " + C,
            "Redness and swelling along the nail edge is typical of an ingrown nail, and pus means it's infected. Soaks give temporary relief, but the real fix is removing the edge. Recurring ingrowns can be treated permanently. " + C,
        ],
        tags=["nails", "ingrown"], verify=True,
    ),
    Intent(
        id="hammertoes", category="toes_nails",
        questions=[
            "My toes are curling",
            "What is a hammertoe?",
            "Corn on top of my toe",
            "Can hammertoes be fixed?",
            "My second toe is crossing over",
        ],
        answers=[
            "Hammertoes are toes that bend at the middle joint, often causing corns on top where they rub the shoe. Flexible ones can be helped with roomier shoes, padding and splints; rigid or painful ones can be corrected surgically, often with minimally invasive techniques. " + C,
        ],
        urls=["url_surgery"], tags=["toes", "hammertoe"], verify=True,
    ),
    Intent(
        id="big_toe_arthritis_gout", category="toes_nails", urgency="soon",
        questions=[
            "My big toe joint is stiff and sore",
            "Sudden severe pain and redness in my big toe",
            "Do I have gout?",
            "Arthritis in my big toe",
            "Hallux rigidus",
        ],
        answers=[
            "A stiff, sore big toe joint is usually arthritis (hallux rigidus). A big toe that suddenly becomes red, hot, swollen and too painful to touch is a classic gout attack, which should be seen promptly, and you may need bloodwork with your primary doctor. Arthritis options range from stiff-soled shoes and laser to joint procedures. More: {url_arthritis}",
            "{disclaimer} Gradual stiffness points to arthritis; a sudden hot, red flare points to gout or infection. Either way we can help, and a red, hot joint with fever needs same-day care. " + C,
        ],
        urls=["url_arthritis"], tags=["toes", "arthritis", "gout"],
    ),

    # ======================= SKIN ===========================================
    Intent(
        id="plantar_warts", category="skin",
        questions=[
            "I have a wart on the bottom of my foot",
            "How do I get rid of plantar warts?",
            "Is this a wart or a callus?",
            "My plantar wart keeps coming back",
            "Black dots in a callus on my foot",
        ],
        answers=[
            "Plantar warts are caused by a virus and often have tiny black dots (clotted blood vessels) and hurt when squeezed side to side. Calluses hurt more with direct pressure. Stubborn warts usually need in-office treatment. " + C,
            "If over-the-counter treatments haven't worked after a few weeks, or the wart is spreading or painful, have it treated in the office. If you have diabetes or poor circulation, don't use acid treatments at home. " + C,
        ],
        tags=["skin", "warts"], verify=True,
    ),
    Intent(
        id="corns_calluses", category="skin",
        questions=[
            "Painful callus on my foot",
            "How do I get rid of corns?",
            "Can you shave my calluses?",
            "Hard skin on my heel is cracking",
        ],
        answers=[
            "Corns and calluses are the skin's response to pressure. We can safely pare them down in the office, and more importantly find the pressure source (toe shape, bone prominence, shoes) so they stop coming back. With diabetes, please don't cut them yourself. " + C,
            "Cracked heels and thick calluses respond to regular moisturizing with a urea cream, but deep cracks that bleed, or calluses with diabetes, should be seen. " + C,
        ],
        tags=["skin"], verify=True,
    ),
    Intent(
        id="athletes_foot", category="skin",
        questions=[
            "Itchy peeling skin between my toes",
            "Do I have athlete's foot?",
            "Rash on my feet",
            "My feet smell and peel",
        ],
        answers=[
            "Itching, peeling or cracking between the toes is often athlete's foot, a fungal skin infection. Keep feet dry, change socks daily, and try an over-the-counter antifungal for 2–4 weeks. If it doesn't clear, keeps returning, blisters, or you have diabetes, come in, because untreated athlete's foot can spread to the nails. " + C,
        ],
        tags=["skin", "fungus"], verify=True,
    ),

    # ======================= ANKLE, TENDON, SPORTS ==========================
    Intent(
        id="ankle_sprain", category="ankle_tendon", urgency="soon",
        questions=[
            "I rolled my ankle",
            "I sprained my ankle {duration} ago and it still hurts",
            "My ankle keeps giving out",
            "Swollen ankle after {activity}",
            "Is my ankle broken or sprained?",
            "Chronic ankle instability",
        ],
        answers=[
            "For a fresh sprain, rest, ice, compress, elevate, and get seen if you can't bear weight or there's pain directly on the bone. Sprains that never fully healed are a leading cause of chronic instability, because the ligament heals loose and balance reflexes stay dull, which causes that giving-way feeling. It's fixable at any stage. More: {url_sprains}",
            "If your ankle still hurts or gives out months later, it likely healed loose. Laser speeds recovery, and targeted rehab restores stability. Surgery is only for cases that don't respond. If you can't put weight on it, call {phone} today.",
        ],
        follow_ups=["Can you put weight on it?", "When did it happen?"],
        urls=["url_sprains"], tags=["ankle", "sprain"],
    ),
    Intent(
        id="achilles", category="ankle_tendon", urgency="soon",
        questions=[
            "Pain in my Achilles",
            "Pain above my heel at the back",
            "My Achilles is stiff in the morning",
            "Achilles tendonitis treatment",
            "I felt a pop in the back of my leg",
        ],
        answers=[
            "Pain or stiffness along the cord above your heel is usually Achilles tendonitis, an overuse injury. Chronic cases build scar tissue that responds well to MLS laser and EPAT shockwave, along with a strengthening program. A sudden pop with weakness could be a rupture, which needs urgent evaluation, so call {phone} right away. More: {url_achilles}",
            "Achilles pain from {activity} is very treatable without surgery in most cases. We combine laser or shockwave with load management so you can stay active while it heals. " + C,
        ],
        urls=["url_achilles"], tags=["achilles", "tendon"],
    ),
    Intent(
        id="sports_injury", category="ankle_tendon",
        questions=[
            "Foot pain from {activity}",
            "Top of my foot hurts after {activity}",
            "Do I have a stress fracture?",
            "Shin splints",
            "Pickleball foot injury",
            "I'm a runner with foot pain",
        ],
        answers=[
            "Athletes most often see us for plantar fasciitis, Achilles problems, ankle sprains, stress fractures and top-of-foot tendonitis. Pain on one spot of bone that gets worse with activity can be a stress fracture, so get it checked before it becomes a full break. Our goal is to keep you active while you heal. More: {url_sports}",
            "Soreness across the top of the foot after ramping up activity is often extensor tendonitis or a stress reaction. Laser and shockwave can speed healing with no downtime. " + C,
        ],
        urls=["url_sports"], tags=["sports"],
    ),
    Intent(
        id="pediatric", category="ankle_tendon",
        questions=[
            "Do you treat children?",
            "Do you see kids?",
            "{family} has heel pain from soccer",
            "What is Sever's disease?",
            "My teenager sprained their ankle",
        ],
        answers=[
            "We see adolescent athletes with sports injuries, heel pain, and ankle sprains. Sever's disease, an irritation of the heel growth plate, is common in active kids. Call {phone} and describe the situation, and if a pediatric specialist is a better fit we'll tell you.",
        ],
        tags=["pediatric"],
    ),

    # ======================= ARTHRITIS ======================================
    Intent(
        id="arthritis", category="arthritis",
        questions=[
            "Arthritis in my foot",
            "Ankle arthritis",
            "Deep aching in my ankle",
            "Midfoot arthritis",
            "Can laser help arthritis in my feet?",
        ],
        answers=[
            "Foot and ankle arthritis causes deep aching, stiffness and swelling. We start conservatively with MLS laser, regenerative injections, bracing and shoe modifications. Joint surgery is reserved for cases that don't respond. More: {url_arthritis}",
            "Laser therapy reduces arthritis pain and inflammation with no downtime, and PRP or other regenerative options may help selected joints. The exam and X-rays decide the plan. " + C,
        ],
        urls=["url_arthritis"], tags=["arthritis"],
    ),

    # ======================= DIABETIC & NEURO ===============================
    Intent(
        id="diabetic_foot", category="diabetic_neuro", urgency="soon",
        questions=[
            "I have diabetes, how often should my feet be checked?",
            "Diabetic foot exam",
            "Do you do diabetic foot care?",
            "Diabetic nail trimming",
            "Diabetic shoes",
        ],
        answers=[
            "With diabetes, get your feet checked at least once a year, or every 3–6 months if you have neuropathy, circulation problems, a deformity, or a history of ulcers. Regular podiatric care measurably lowers amputation risk. Check your feet daily, never go barefoot, and call us about any wound. More: {url_diabetic}",
            "Yes, we provide full diabetic foot care, including exams, nail and callus care, wound prevention, and surgery when truly needed. " + C,
        ],
        urls=["url_diabetic"], tags=["diabetes"],
    ),
    Intent(
        id="diabetic_wound", category="diabetic_neuro", urgency="urgent",
        questions=[
            "I have diabetes and a sore on my foot",
            "Open wound on my foot that won't heal",
            "Blister on my diabetic foot",
            "Wound care for my foot",
            "My foot ulcer is getting worse",
        ],
        answers=[
            "Any wound, blister or sore on a diabetic foot should be seen quickly, ideally within a day or two, and immediately if there's redness spreading, drainage, odor, fever, or the area is dark or black. Call {phone} now. If you have fever, chills or rapidly spreading redness, go to the ER. Wound care info: {url_wound}",
            "Non-healing wounds need professional care: offloading pressure, cleaning, and checking circulation and infection. Please don't wait on this. Call {phone} today.",
        ],
        urls=["url_wound", "url_diabetic"], tags=["diabetes", "wound", "escalate"],
    ),
    Intent(
        id="neuropathy", category="diabetic_neuro",
        questions=[
            "Burning and tingling in my feet",
            "My feet are numb",
            "Pins and needles in my toes {time_of_day}",
            "Can laser help neuropathy?",
            "Neuropathy treatment",
            "My feet burn at night",
        ],
        answers=[
            "Burning, tingling or pins and needles in the toes is a hallmark of peripheral neuropathy, especially with diabetes. For many patients, MLS laser improves the circulation that feeds nerve tissue and meaningfully reduces burning and nighttime symptoms. It won't revive completely dead nerves, and the earlier you treat, the better the odds. More: {url_neuro}",
            "Neuropathy usually needs a longer laser course than other conditions, and some patients benefit from periodic maintenance. We'll tell you that up front, including cost. Numb feet also need regular checks for unnoticed injuries. " + C,
        ],
        urls=["url_neuro"], tags=["neuropathy"],
    ),

    # ======================= VASCULAR / VEINS ===============================
    Intent(
        id="veins", category="vascular",
        questions=[
            "Do you treat varicose veins?",
            "My legs are heavy and swollen at the end of the day",
            "Spider veins on my legs",
            "What is venous insufficiency?",
            "Ankle swelling and leg cramps",
            "Vein treatment near me",
        ],
        answers=[
            "Yes, we're a leg vein center too. Heavy, achy, swollen legs that worsen through the day, visible varicose veins, night cramps, or skin changes near the ankles can signal chronic venous insufficiency, where vein valves don't push blood back up efficiently. We evaluate and treat it. More: {vein_url}",
            "Leg heaviness and ankle swelling are classic vein symptoms. A vein evaluation shows whether the valves are leaking. Note: a single swollen, hot, painful calf needs same-day care to rule out a blood clot. " + C,
        ],
        urls=["vein_url"], tags=["veins"],
    ),
    Intent(
        id="circulation", category="vascular", urgency="soon",
        questions=[
            "My feet are always cold",
            "Calf pain when I walk that goes away when I rest",
            "Poor circulation in my feet",
            "My toes turn purple",
        ],
        answers=[
            "Calf cramping with walking that eases with rest, cold feet, slow-healing sores or color changes can mean reduced arterial circulation (PAD). That's important to evaluate, especially with diabetes or smoking history. A suddenly cold, pale or blue foot is an emergency, so call 911. Otherwise, " + C,
        ],
        tags=["circulation", "red_flag_possible"], verify=True,
    ),

    # ======================= TREATMENTS =====================================
    Intent(
        id="mls_laser", category="treatments",
        questions=[
            "What is MLS laser therapy?",
            "Does laser therapy hurt?",
            "How many laser sessions will I need?",
            "Is MLS laser FDA approved?",
            "How is MLS different from cold laser?",
            "Are there side effects from laser therapy?",
            "Who can't get laser therapy?",
            "Can I exercise after a laser session?",
        ],
        answers=[
            "MLS (Multiwave Locked System) laser is FDA-cleared. It delivers two synchronized wavelengths, 808 nm to resolve inflammation and 905 nm to relieve pain, which stimulate your cells' own repair (photobiomodulation). It's painless: most people feel nothing or a mild warmth. Sessions take {mls_session}, with no downtime. More: {url_mls}",
            "Most conditions respond within {mls_course}. Acute injuries need fewer sessions, and chronic ones like neuropathy need more. Many patients notice relief within the first 1–3 sessions, and improvement keeps building for weeks after. " + C,
            "Compared with cheap cold lasers, MLS is class IV (deep therapeutic dose), uses a patented dual-wavelength pulse, and has robotic, reproducible delivery. We don't treat over active cancer, a pregnant uterus, or near the thyroid or eyes, and the doctor screens your history first.",
        ],
        urls=["url_mls"], tags=["laser", "treatment"],
    ),
    Intent(
        id="shockwave", category="treatments",
        questions=[
            "What is shockwave therapy?",
            "What is EPAT?",
            "Does shockwave hurt?",
            "Laser vs shockwave, which do I need?",
            "Does shockwave work for plantar fasciitis?",
        ],
        answers=[
            "EPAT shockwave sends acoustic pressure waves into chronically injured tissue, breaking down scar tissue and restarting healing. It's one of the best-evidenced non-surgical options for chronic plantar fasciitis and Achilles tendinopathy. It feels like firm, rapid tapping, sessions take 10–15 minutes, and there's no downtime. More: {url_epat}",
            "Rule of thumb: laser calms and speeds healing (pain, inflammation), while shockwave provokes and rebuilds (old, scarred, stubborn tissue). Chronic cases often benefit from both. Best results are typically measured around 12 weeks after treatment.",
        ],
        urls=["url_epat"], tags=["shockwave", "treatment"],
    ),
    Intent(
        id="prp_regen", category="treatments",
        questions=[
            "What is PRP?",
            "Is PRP better than a cortisone shot?",
            "Do you do stem cell therapy?",
            "Are stem cells FDA approved?",
            "Can regenerative medicine help me avoid surgery?",
            "How long does PRP take to work?",
        ],
        answers=[
            "PRP (platelet-rich plasma) uses a small sample of your own blood, concentrated and injected into injured tendons, fascia or joints to restart healing. Unlike cortisone, which suppresses inflammation fast but temporarily, PRP builds tissue. Expect {regen_timeline}. More: {url_prp}",
            "No regenerative cell therapy for orthopedic conditions is FDA-approved. They're elective treatments offered under physician judgment, where the evidence is promising but still developing, and we're upfront about that. In well-selected cases they can help avoid surgery, and candidacy is decided by a surgeon with no incentive to steer you away from an operation you actually need. More: {url_regen}",
        ],
        urls=["url_prp", "url_regen"], tags=["prp", "regenerative"],
    ),
    Intent(
        id="orthotics_shoes", category="treatments", verify=True,
        questions=[
            "Do you make custom orthotics?",
            "Do I need orthotics?",
            "What shoes should I wear?",
            "Are {shoe} bad for my feet?",
            "Best shoes for plantar fasciitis",
            "Are over-the-counter insoles OK?",
        ],
        answers=[
            "Orthotics help when foot mechanics (flat feet, high arches, overpronation) are driving the problem, and they're part of many of our treatment plans. Good over-the-counter inserts are fine for mild cases; custom devices are for when mechanics need real correction. " + C,
            "In general, look for a firm heel counter, a sole that only bends at the toes, and a roomy toe box. Shoes that are flat and floppy (like flip flops) or high heels for long stretches are common culprits. Bring your most-worn shoes to the visit, since the wear pattern is diagnostic.",
        ],
        tags=["orthotics", "footwear"],
    ),

    # ======================= SURGERY ========================================
    Intent(
        id="surgery", category="surgery",
        questions=[
            "Do you do foot surgery?",
            "Will I need surgery?",
            "What is minimally invasive foot surgery?",
            "Where is surgery performed?",
            "How long is recovery from foot surgery?",
            "Can laser help after surgery?",
            "I want a second opinion on foot surgery",
        ],
        answers=[
            "Both of our doctors are foot & ankle surgeons, and surgery is offered only when conservative care isn't enough. That includes bunion correction, hammertoes, tendon repair and reconstruction, often with minimally invasive techniques. Recovery depends entirely on the procedure, and your surgeon will map it out at the consult. More: {url_surgery}",
            "Second opinions are welcome. We'll review your imaging and tell you honestly whether surgery is needed. Laser is also often used after surgery to reduce swelling and support healing. " + C,
        ],
        urls=["url_surgery"], tags=["surgery"],
    ),

    # ======================= OUT OF SCOPE / ROUTING =========================
    Intent(
        id="route_ortho", category="routing",
        questions=[
            "Do you treat knee pain?",
            "I need a knee replacement",
            "Shoulder pain",
            "Hip pain",
            "Torn ACL",
        ],
        answers=[
            "We focus on the foot and ankle. For knees, hips and shoulders, our orthopedic sister practice {ortho_name} with {ortho_doc} handles MAKO robotic knee replacement, ACL and meniscus surgery, shoulder replacement and sports medicine: {ortho_url}. One caveat: foot mechanics sometimes cause knee and hip pain, so if your feet are involved too, we're happy to take a look.",
        ],
        urls=["ortho_url"], tags=["routing"],
    ),
    Intent(
        id="route_regen_iv", category="routing",
        questions=[
            "Do you do IV therapy?",
            "Weight loss injections",
            "Semaglutide",
            "Peptides",
            "IV vitamin drip",
        ],
        answers=[
            "Those services are offered at our sister practice {regen_name} in Palm Beach Gardens: regenerative and orthobiologic therapies, medical weight-loss and peptide programs, and an IV therapy lounge. Visit {regen_url} or call {phone} and we'll point you in the right direction.",
        ],
        urls=["regen_url"], tags=["routing"],
    ),
    Intent(
        id="greeting_thanks", category="smalltalk",
        questions=["Hi", "Hello", "Thanks", "Thank you", "That helps"],
        answers=[
            "Hi! I can help with foot and ankle questions, treatments, insurance, and booking at {short_name}. What's going on with your feet?",
            "You're welcome! If you'd like to get it checked, call or text {phone} or book at {booking_url}.",
        ],
        tags=["smalltalk"],
    ),
    Intent(
        id="fallback", category="fallback",
        questions=[
            "Can you help me with my taxes?",
            "What's the weather?",
            "Tell me a joke",
        ],
        answers=[
            "I'm the {short_name} assistant, so I can help with foot and ankle questions, treatments, visits and booking. For anything else, I'm not the right resource. Is there something about your feet I can help with?",
            "I'm not sure I can help with that. For specific questions, the team at {phone} is happy to help, and real humans answer.",
        ],
        tags=["fallback"],
    ),
]

SYSTEM_PROMPT = (
    "You are the virtual assistant for {practice_name}, a foot & ankle and leg vein "
    "practice with offices in Jupiter and Palm Beach Gardens, FL. Be warm, concise and "
    "accurate. Give general educational information only and never diagnose, prescribe, "
    "or promise outcomes. Use only practice facts provided to you. For red-flag symptoms "
    "(can't bear weight, cold/blue foot, spreading redness or red streaks, fever with foot "
    "pain, a wound on a diabetic foot, a swollen hot calf), direct the patient to urgent "
    "care: 911/ER for emergencies, otherwise call {phone}. Ask one clarifying question "
    "when it would change the advice. End with a clear next step to book: {phone} or "
    "{booking_url}."
)

# ---------------------------------------------------------------------------
# 4. RENDERING & EXPANSION
# ---------------------------------------------------------------------------

class _Safe(dict):
    """Leaves unknown {placeholders} intact instead of raising KeyError."""
    def __missing__(self, key):
        return "{" + key + "}"


def render(text: str, extra: dict | None = None, passes: int = 3) -> str:
    """Fill {placeholders} from PRACTICE (+ extra slot values). Multi-pass so
    PRACTICE values can themselves contain placeholders (e.g. {cta})."""
    ctx = _Safe({**PRACTICE, **(extra or {})})
    for _ in range(passes):
        new = text.format_map(ctx)
        if new == text:
            break
        text = new
    return text


SLOT_RE = re.compile(r"\{(\w+)\}")


def expand_question(template: str, max_variants: int = 6, seed: int = 0) -> list[tuple[str, dict]]:
    """Expand a question template's {slots} into concrete phrasings.
    Returns [(question, slot_values)]. Capped to avoid combinatorial blow-up."""
    slot_names = [s for s in SLOT_RE.findall(template) if s in SLOTS]
    if not slot_names:
        return [(render(template), {})]
    combos = list(itertools.product(*(SLOTS[s] for s in slot_names)))
    rng = random.Random(f"{template}-{seed}")
    rng.shuffle(combos)
    out = []
    for combo in combos[:max_variants]:
        values = dict(zip(slot_names, combo))
        out.append((render(template, values), values))
    return out


def iter_pairs(max_variants: int = 6, include_unverified: bool = True):
    """Yield every (intent, question, answer, slots) training pair."""
    for intent in INTENTS:
        if intent.verify and not include_unverified:
            continue
        for q_tpl in intent.questions:
            for q, slots in expand_question(q_tpl, max_variants):
                for a_tpl in intent.answers:
                    yield intent, q, render(a_tpl, slots), slots


# ---------------------------------------------------------------------------
# 5. EXPORTERS
# ---------------------------------------------------------------------------

def _resolve_urls(intent: Intent) -> list[str]:
    return [PRACTICE.get(u, u) for u in intent.urls]


def export_chat_jsonl(path: Path, **kw) -> int:
    system = render(SYSTEM_PROMPT)
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for intent, q, a, _ in iter_pairs(**kw):
            f.write(json.dumps({
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": q},
                    {"role": "assistant", "content": a},
                ],
                "metadata": {"intent": intent.id, "category": intent.category,
                             "urgency": intent.urgency, "verify": intent.verify},
            }, ensure_ascii=False) + "\n")
            n += 1
    return n


def export_qa_jsonl(path: Path, **kw) -> int:
    n = 0
    with path.open("w", encoding="utf-8") as f:
        for intent, q, a, slots in iter_pairs(**kw):
            f.write(json.dumps({
                "intent": intent.id, "category": intent.category, "urgency": intent.urgency,
                "question": q, "answer": a, "slots": slots, "tags": intent.tags,
                "urls": _resolve_urls(intent), "verify": intent.verify,
            }, ensure_ascii=False) + "\n")
            n += 1
    return n


def export_knowledge_base(path: Path) -> int:
    docs = []
    for i in INTENTS:
        docs.append({
            "id": i.id, "category": i.category, "urgency": i.urgency,
            "questions": [render(q) for q in i.questions],
            "answers": [render(a) for a in i.answers],
            "follow_ups": i.follow_ups, "tags": i.tags,
            "urls": _resolve_urls(i), "verify": i.verify,
        })
    path.write_text(json.dumps({"practice": {k: render(v) for k, v in PRACTICE.items()},
                                "system_prompt": render(SYSTEM_PROMPT),
                                "intents": docs}, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(docs)


# ---------------------------------------------------------------------------
# 6. VALIDATION & QUICK MATCHER (for testing before training)
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parents[2]
SITE_URL_RE = re.compile(r"https://jupiterlaser\.com(/[^\s\"')]*)")


def _missing_site_pages() -> list[str]:
    """jupiterlaser.com links that have no built page in this repo."""
    dummy = {s: "x" for s in SLOTS}
    texts = [render(v) for v in PRACTICE.values()]
    for i in INTENTS:
        texts += [render(a, dummy) for a in i.answers] + _resolve_urls(i)
    missing = []
    for path in sorted({p.rstrip(".,") for p in SITE_URL_RE.findall(" ".join(texts))}):
        rel = path.strip("/")
        if rel and not (SITE_ROOT / rel / "index.html").exists():
            missing.append(path)
    return missing


def validate() -> list[str]:
    problems, seen = [], set()
    for path in _missing_site_pages():
        problems.append(f"link to a page that doesn't exist: https://jupiterlaser.com{path}")
    for i in INTENTS:
        if i.id in seen:
            problems.append(f"duplicate intent id: {i.id}")
        seen.add(i.id)
        if len(i.questions) < 2:
            problems.append(f"{i.id}: needs 2+ questions")
        if not i.answers:
            problems.append(f"{i.id}: no answers")
        if i.urgency not in {"routine", "soon", "urgent", "emergency"}:
            problems.append(f"{i.id}: bad urgency {i.urgency}")
        for a in i.answers:
            leftover = SLOT_RE.findall(render(a, {s: "x" for s in SLOTS}))
            if leftover:
                problems.append(f"{i.id}: unfilled placeholders {leftover}")
        for u in i.urls:
            if u not in PRACTICE and not u.startswith("http"):
                problems.append(f"{i.id}: unknown url key {u}")
    return problems


def _tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z']+", s.lower())) - {
        "i", "my", "a", "the", "is", "do", "you", "it", "in", "of", "and", "to", "for", "on", "what", "how", "me"}


def match(user_text: str, top_k: int = 3) -> list[tuple[float, Intent]]:
    """Naive keyword-overlap matcher, good enough to sanity-check coverage."""
    ut = _tokens(user_text)
    scored = []
    for i in INTENTS:
        best = 0.0
        for q_tpl in i.questions:
            for q, _ in expand_question(q_tpl, 3):
                qt = _tokens(q)
                if qt:
                    best = max(best, len(ut & qt) / len(ut | qt))
        scored.append((best, i))
    return sorted(scored, key=lambda x: -x[0])[:top_k]


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "training_out"))
    ap.add_argument("--max-variants", type=int, default=6, help="slot expansions per question template")
    ap.add_argument("--verified-only", action="store_true", help="skip intents flagged verify=True")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--ask", help="test the matcher with a user question")
    args = ap.parse_args()

    problems = validate()
    if problems:
        print("VALIDATION PROBLEMS:\n  " + "\n  ".join(problems))
        raise SystemExit(1)

    if args.ask:
        for score, intent in match(args.ask):
            print(f"{score:.2f}  {intent.id} [{intent.urgency}]")
        best = match(args.ask, 1)[0][1]
        print("\n" + render(random.choice(best.answers)))
        return

    kw = {"max_variants": args.max_variants, "include_unverified": not args.verified_only}
    n_pairs = sum(1 for _ in iter_pairs(**kw))
    n_questions = sum(len(expand_question(q, args.max_variants)) for i in INTENTS for q in i.questions)
    print(f"intents: {len(INTENTS)} | expanded questions: {n_questions} | "
          f"answers: {sum(len(i.answers) for i in INTENTS)} | Q/A pairs: {n_pairs} | "
          f"needs verification: {sum(i.verify for i in INTENTS)}")
    if args.stats:
        return

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    print("chat_finetune.jsonl :", export_chat_jsonl(out / "chat_finetune.jsonl", **kw))
    print("qa_pairs.jsonl      :", export_qa_jsonl(out / "qa_pairs.jsonl", **kw))
    print("knowledge_base.json :", export_knowledge_base(out / "knowledge_base.json"), "intents")


if __name__ == "__main__":
    main()
