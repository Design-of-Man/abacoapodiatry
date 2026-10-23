# Fact-check log: Abacoa Podiatry condition pages

Method: /home/claude/research/FACTCHECK.md, with practice facts and writing rules from /home/claude/research/abacoa/BRIEF.md. Checked 2026-10-07 by an independent reviewer who did not write the pages. Sources fetched via Firecrawl / WebFetch (direct curl is blocked by the sandbox egress proxy, so "resolves" means the page was retrieved with HTTP 200 through Firecrawl or WebFetch). ICD-10 codes checked against the cited icd10data.com pages.

## ingrown-toenail
Sources fetched: ACFAS FootHealthFacts, APMA, Cleveland Clinic, MedlinePlus, Mayo Clinic, NHS. All 6 resolve (200).
- Cleveland Clinic: teens, athletes, diabetes, nerve damage, poor circulation at higher risk -> SUPPORTED -> kept
- Cleveland Clinic: "two in every ten people who see a provider for a foot problem" -> SUPPORTED (verbatim "Two out of every 10") -> kept
- Symptoms (pain, redness, swelling, warmth, pus/drainage, odor, proud flesh) -> SUPPORTED (ACFAS, APMA, CC) -> kept
- Causes (short/rounded trimming, tight shoes/socks, trauma incl. running/kicking, heredity, nail too wide, tearing, fungal/prior nail loss) -> SUPPORTED (ACFAS, MedlinePlus, CC) -> kept
- Intro "ACFAS: podiatrist treats nail edge and infection" -> SUPPORTED -> kept
- Intro/method 1 "Cleveland Clinic: mild cases respond to careful lifting and trimming with sterile instruments" -> MISATTRIBUTED in part (CC says same techniques as home care, i.e. lifting, with sterile instruments; no trimming; ACFAS warns repeated border trimming worsens it) -> reworded to lifting only, label changed to "In-office care for mild cases", schema treatment changed; reviewer note added
- APMA: topical or oral antibiotic for infection -> SUPPORTED (APMA "topical or oral medication to treat the infection"; ACFAS oral antibiotic) -> kept
- MedlinePlus: partial nail avulsion with numbing injection; nail regrows in 2 to 4 months -> SUPPORTED -> kept (not a listed service; reviewer note already asks)
- APMA/ACFAS matrixectomy with chemical or other method -> SUPPORTED -> kept
- MedlinePlus: poorly fitting shoes and improper trimming most common causes -> SUPPORTED -> kept
- ACFAS: very little pain, resume normal activity next day -> SUPPORTED -> kept
- Self-care: CC twice-daily warm Epsom soak -> SUPPORTED (note ACFAS says room-temperature water) -> kept, reviewer note added
- Self-care: OTC acetaminophen/ibuprofen -> SUPPORTED (CC, NHS) -> kept; ACFAS "bathroom surgery" -> SUPPORTED; diabetes skip home care -> SUPPORTED (ACFAS, APMA, MedlinePlus)
- Red flags (spreading pus/redness; fever or hot/shivery; severe pain/redness/swelling; diabetes/neuropathy/poor circulation; no improvement in a few days) -> SUPPORTED (Mayo, NHS, MedlinePlus, CC) -> kept
- FAQ2 "procedure should not be painful beyond the numbing shot" -> UNSUPPORTED near-promise -> softened to "meant to keep the procedure itself comfortable once the toe is numb"
- FAQ3 infection signs (CC, ACFAS, NHS) -> SUPPORTED -> kept
- FAQ4 "Recurring ingrown nails are often linked to ... according to APMA and ACFAS" -> MISATTRIBUTED (sources list general causes, not causes of recurrence) -> reworded to "APMA and ACFAS list heredity, improper trimming and shoe pressure among the causes", plus ACFAS "some nails become ingrown again"
- FAQ5 MedlinePlus trimming tips; APMA nail length and no ripping -> SUPPORTED -> kept
- FAQ6 practice facts -> matches BRIEF -> kept
- ICD-10 L60.0 Ingrowing nail -> SUPPORTED -> kept

## hammertoes
Sources fetched: ACFAS, AAOS OrthoInfo, APMA, Cleveland Clinic, Mayo Clinic. All 5 resolve (200).
- APMA: contracture of the PIP joint, usually second to fifth toes; flexible then rigid -> SUPPORTED -> kept
- APMA: more common in women -> SUPPORTED (also Mayo) -> kept
- Cleveland Clinic: "up to 20% of all foot and ankle issues" -> SUPPORTED (verbatim) -> kept
- Risk factors bunions, high arches, flat feet, long toes, arthritis, diabetes -> SUPPORTED (CC, APMA, Mayo) -> kept
- Symptoms list (pain in shoes, corns on top/between toes/ball of foot, redness/burning, stiffness, ball-of-foot pain, open sores in severe cases) -> SUPPORTED (ACFAS, APMA, AAOS) -> kept
- Causes list (muscle/tendon imbalance, tight/high-heeled shoes, long toe, prior trauma, bunions/arch shape, arthritis/diabetes/heredity) -> SUPPORTED (ACFAS, Mayo, CC, APMA) -> kept
- ACFAS: progressive; flexible stage responds to conservative care; rigid toes stop responding; surgery when rigid and painful or open sore -> SUPPORTED -> kept
- ACFAS deep toe box, heels no higher than two inches; AAOS shoes one-half inch longer than longest toe -> SUPPORTED -> kept
- Padding, splints/straps (ACFAS), medical tape (CC) -> SUPPORTED -> kept (not a listed service; existing reviewer note asks)
- Custom orthotics control muscle/tendon imbalance (ACFAS; APMA "controlling foot function") -> SUPPORTED -> kept
- NSAIDs and corticosteroid injections (ACFAS, APMA) -> SUPPORTED -> kept (reviewer note asks practice to confirm)
- AAOS manual stretches, picking up objects, towel curls -> SUPPORTED -> kept
- AAOS tendon lengthening/transfer for flexible toe, arthrodesis with pin and/or plate for rigid toe -> SUPPORTED -> kept
- First visit flexibility check, X-rays "may order" (AAOS, ACFAS, APMA) -> SUPPORTED -> kept
- AAOS: stiffness, swelling, redness for up to 4 to 6 weeks after surgery -> SUPPORTED -> kept
- Self-care (deep toe box, nonmedicated pads, stretches/towel curls, shop end of day per CC) -> SUPPORTED -> kept
- Red flags (lasting pain affecting walking per Mayo; open sore; stiff toe; pain persisting per APMA) -> SUPPORTED / conservative -> kept
- FAQ1, FAQ2, FAQ4, FAQ5 attributions to ACFAS, CC, AAOS, APMA -> SUPPORTED -> kept
- FAQ3 Mayo: hammertoe middle joint, mallet toe joint nearest nail -> SUPPORTED -> kept
- FAQ6 practice facts -> matches BRIEF -> kept
- ICD-10 M20.40 Other hammer toe(s) (acquired), unspecified foot -> SUPPORTED -> kept
- No changes required.

## mortons-neuroma
Sources fetched: ACFAS, AAOS OrthoInfo, Cleveland Clinic, Mayo Clinic. All 4 resolve (200).
- AAOS: thickening of tissue around a small nerve; nerve passes under transverse metatarsal ligament -> SUPPORTED -> kept
- ACFAS: most often between third and fourth toes -> SUPPORTED -> kept
- AAOS: about 8 times more common in women; typically ages 30 to 60 -> SUPPORTED -> kept
- Risk: running, tennis/court sports, narrow or high-heeled shoes, bunions, hammertoes, flat/high/flexible feet, injury -> SUPPORTED (ACFAS, CC, Mayo) -> kept
- Symptoms (burning/stabbing pain, pebble/marble feeling, tingling/numbness in two toes, bunched sock, worse with activity/heels, relief removing shoe, clicking) -> SUPPORTED (Mayo, CC, ACFAS) -> kept
- ACFAS first-line list (padding, icing, orthotics, activity and shoe changes, injections) -> SUPPORTED -> kept
- "AAOS reports conservative care relieves symptoms in up to about 50%" -> WRONG emphasis (AAOS: "may provide some degree of relief in up to about 50%") -> corrected wording
- ACFAS surgery only after inadequate response -> SUPPORTED -> kept
- Methods: metatarsal padding, wide/low shoes, custom orthotics, ice/activity, injections (ACFAS), chemical/radiofrequency ablation and neurectomy/decompression (AAOS) -> SUPPORTED -> kept (non-listed services; existing reviewer notes ask)
- First visit: web-space compression test, click, imaging "may order" (AAOS) -> SUPPORTED -> kept
- AAOS: stiff-soled post-op shoe, normal shoes by 4 weeks -> SUPPORTED -> kept
- "AAOS notes that symptoms come back in 5 to 20%" -> overstated (AAOS: "around 5 to 20% may have symptoms return and need additional treatment") -> corrected
- Self-care and red flags (Mayo few days / not improving with shoe change; CC two weeks / worsening) -> SUPPORTED -> kept
- FAQ1 -> SUPPORTED but incomplete; added Cleveland Clinic statement that the neuroma itself does not simply go away
- FAQ2 ACFAS activity avoidance, CC lower-impact exercise -> SUPPORTED -> kept
- FAQ3 "They help many people... corticosteroid injections relieve symptoms in about 50 to 70%" -> WRONG (AAOS: short-term relief in 50 to 70%, long-term relief less common) -> corrected with the qualifier
- FAQ4 shoes (ACFAS, Mayo) -> SUPPORTED -> kept
- FAQ5 AAOS 80 to 95% surgical success -> SUPPORTED ("most studies reporting") -> qualifier added; national figure, reviewer note already flags percentages
- Reviewer note "no listed authoritative source supports EPAT for Morton's" -> WRONG (AAOS lists ESWT and PRP as second-line add-ons with limited research) -> note corrected; doctor decision flagged
- ICD-10 G57.60 Lesion of plantar nerve, unspecified lower limb (G57.6 includes Morton's metatarsalgia) -> SUPPORTED -> kept

## toenail-fungus
Sources fetched: AAD treatment page, AAD FAQ/overview page, APMA, Cleveland Clinic, Mayo Clinic. All 5 resolve (200).
- APMA: infection underneath the nail surface caused by fungi -> SUPPORTED -> kept
- Cleveland Clinic: dermatophytes (keratin-feeding mold) cause 90% of toenail fungal infections -> SUPPORTED -> kept
- Cleveland Clinic: 1 in 10 overall, 1 in 2 over 70 -> SUPPORTED -> kept
- Risk factors (damp public areas, athlete's foot, sweaty shoes, nail injury/shoe pressure, diabetes, circulation, immune weakness, older age, shared towels/clippers) -> SUPPORTED (APMA, Mayo, CC, AAD) -> kept
- Symptoms (discoloration, thickening, crumbly edges, chalky patches, debris, lifting, odor) -> SUPPORTED (CC, Mayo, APMA) -> kept
- AAD: almost never goes away on its own, can spread -> SUPPORTED -> kept
- AAD: microscopy of clippings/scrapings to rule out nail psoriasis -> SUPPORTED -> kept
- APMA: FDA-approved oral antifungals may be the most effective treatment -> SUPPORTED -> kept
- AAD: terbinafine or itraconazole daily for 12 weeks for toenails, liver function testing -> SUPPORTED -> kept
- AAD: efinaconazole and tavaborole daily, usually 48 weeks; ciclopirox once-daily lacquer -> SUPPORTED -> kept
- AAD: trimming, abrasion/filing, debridement; APMA/AAD surgical or chemical nail removal -> SUPPORTED -> kept (non-listed services; existing reviewer note asks)
- "AAD notes nail fungus can return months or years later" (method and FAQ4) -> MISATTRIBUTED detail (AAD: "can occur a year or more after clearing"; no "months") -> corrected in both places
- AAD maintenance therapy for a year or longer -> SUPPORTED -> kept
- Recovery: AAD 12 weeks oral, 48 weeks topical, a year or longer for nail to grow out, toenail regrowth 12 to 18 months after removal -> SUPPORTED -> kept
- Self-care (shower shoes, dry feet, straight trimming, unshared/disinfected clippers, treat athlete's foot) -> SUPPORTED (APMA, Mayo, CC) -> kept
- Red flags (diabetes; redness/pain/pus per CC; bleeding/difficulty walking per Mayo; worsening despite self-care per Mayo; circulation/immune per CC) -> SUPPORTED -> kept
- FAQ1 AAD/APMA statements -> SUPPORTED -> kept; FAQ2 contagion routes (CC, AAD) -> SUPPORTED; FAQ3 oral antifungal safety and liver testing (APMA, AAD) -> SUPPORTED; FAQ5 psoriasis look-alike (AAD) -> SUPPORTED; FAQ6 practice facts -> matches BRIEF
- Laser treatment correctly absent (BRIEF forbids; AAD states no laser is FDA approved to treat the infection) -> kept absent
- ICD-10 B35.1 Tinea unguium -> SUPPORTED -> kept

## stress-fractures
Sources fetched: AAOS OrthoInfo, Mayo Clinic (symptoms/causes), Mayo Clinic (diagnosis/treatment), icd10data M84.37. All 4 resolve (200).
- AAOS: small crack or severe bruising in bone; metatarsals most common, especially second and third; calcaneus, navicular, talus, sesamoids also -> SUPPORTED -> kept
- Typical patients (runners, dancers, tennis/basketball, military recruits, sudden increase in walking) -> SUPPORTED (Mayo, AAOS) -> kept
- Mayo: female athletes, thinning bones, flat feet or rigid high arches -> SUPPORTED -> kept
- "Around Jupiter and Palm Beach Gardens we often see them after..." -> UNSUPPORTED practice claim (BRIEF allows no practice facts beyond the list) -> reworded to "worth mentioning to your podiatrist"; reviewer note updated
- Lede "Our podiatrists help it heal properly" -> implied outcome promise -> softened to "help protect it as it heals"
- Symptoms (gradual pain worse with weight bearing, eases with rest, point tenderness, top-of-foot/ankle swelling, possible bruising, pain at rest/night) -> SUPPORTED (AAOS, Mayo) -> kept
- Cause "switching from a treadmill to pavement or sand" -> partly UNSUPPORTED (sand not in sources) -> changed to AAOS examples (treadmill to outdoor running, grass to hard court)
- Other causes (training increase, worn shoes, osteoporosis/low calcium and vitamin D, foot shape, prior fracture, female athletes with low energy intake/irregular periods) -> SUPPORTED (AAOS, Mayo) -> kept
- Intro "Mayo Clinic adds that fractures in bones with poor blood supply, such as the navicular or the fifth metatarsal near the midfoot..." -> MISATTRIBUTED (Mayo names no bones; AAOS names the base of the fifth metatarsal) -> reattributed to AAOS, Mayo kept for "surgery more likely" in poor-blood-supply areas
- AAOS treatment (rest, crutches, stiff-soled shoe or brace, casting, internal fixation with pins/screws/plates) and Mayo (boot/brace/crutches) -> SUPPORTED -> kept
- "Swimming or cycling, which the AAOS lists as usually acceptable" -> slight paraphrase drift -> changed to "good alternative activities" (AAOS wording; doctor approval caveat kept)
- AAOS 6 to 8 weeks to heal; longer for poor blood supply/chronic; Mayo "weeks or months"; returning too soon risks larger fracture (Mayo) -> SUPPORTED -> kept
- Self-care ice ~15 minutes (Mayo), stiff supportive shoe (AAOS), NSAID caution (Mayo) -> SUPPORTED; NSAID source conflict already flagged for reviewer -> kept
- Red flags (recurring pain, pain at rest/night per Mayo, tenderness/swelling, trouble bearing weight, snap/deformity -> urgent care) -> SUPPORTED / standard conservative guidance -> kept
- FAQ3 Mayo: X-rays often negative early; MRI considered the best way to find stress fractures -> SUPPORTED -> kept
- FAQ4 Mayo early treatment speeds recovery -> SUPPORTED; FAQ5 continuing can cause complete fracture (AAOS) -> SUPPORTED; FAQ6 10% rule (AAOS, Mayo), cross-training, shoes, calcium/vitamin D, strength training -> SUPPORTED
- ICD-10 M84.37 Stress fracture, ankle, foot and toes -> SUPPORTED, non-billable parent (icd10data) -> kept; reviewer note already says so
- Length limits rechecked after edits (lede 30 words, intro 92, what_it_is 86/87).

## metatarsalgia
Sources fetched: Mayo Clinic (symptoms/causes), Mayo Clinic (diagnosis/treatment), Cleveland Clinic, ACFAS capsulitis of the second toe, icd10data M77.40. All resolve (200); the Mayo diagnosis URL drc-20354796 redirects to drc-20354795.
- Mayo diagnosis/treatment source URL -> resolves only via redirect -> updated to canonical drc-20354795
- Cleveland Clinic: pain centers under one or more metatarsal heads -> SUPPORTED -> kept
- Mayo: common in runners/high-impact sports, high heels/tight shoes, excess weight; bunions, hammertoes, high arches, long second toe -> SUPPORTED -> kept
- Cleveland Clinic: rheumatoid arthritis, gout, diabetes as contributors -> SUPPORTED -> kept
- Symptoms (sharp/aching/burning pain, pebble feeling, worse standing/barefoot on hard floors, toe numbness/tingling, eases with rest, swelling at base of second toe per ACFAS capsulitis) -> SUPPORTED -> kept
- Causes incl. tight calf (ACFAS), stress fracture and Morton's neuroma (Mayo) -> SUPPORTED -> kept
- Mayo: rest, ice, shoes, arch supports, metatarsal pads; surgery rarely -> SUPPORTED -> kept
- ACFAS (capsulitis): taping/splinting, calf stretching, stiff-soled shoes, custom inserts/metatarsal pad -> SUPPORTED -> kept (non-listed services; existing reviewer note asks)
- Method 1 "metatarsal pad placed just behind the painful bone ... a measure Mayo Clinic recommends" -> MISATTRIBUTED placement detail (Mayo: "just ahead of the metatarsal bone to help keep stress off the painful area") -> rewritten to Mayo/ACFAS wording; self-care tip and FAQ4 likewise; reviewer note added
- Cleveland Clinic: athletic and rocker-soled shoes; injection or surgery for underlying cause if simpler measures fail -> SUPPORTED -> kept
- Mayo: exam standing and sitting; X-ray for stress fracture -> SUPPORTED -> kept
- Cleveland Clinic: see a provider if no improvement after two weeks -> SUPPORTED -> kept
- Mayo: ice about 20 minutes several times a day -> SUPPORTED -> kept
- Red flags (two weeks, activity-limiting or recurring pain, numbness/tingling, diabetes per CC; drifting toe per ACFAS) -> SUPPORTED -> kept
- FAQ5 Mayo: untreated metatarsalgia can cause pain elsewhere in foot, other foot, hip, low back -> SUPPORTED -> kept
- FAQ6 Cleveland Clinic diabetes with foot pain -> SUPPORTED; callus-to-wound statement is standard diabetic foot guidance, conservative -> kept
- ICD-10 M77.40 Metatarsalgia, unspecified foot (billable) -> SUPPORTED -> kept

## gout
Sources fetched: ACFAS, NIAMS, Mayo Clinic (symptoms/causes), Mayo Clinic (diagnosis/treatment), icd10data M10.9. All 5 resolve (200).
- NIAMS: inflammatory arthritis, needle-shaped urate crystals; purines from body tissues and foods -> SUPPORTED -> kept
- ACFAS: big toe most affected because uric acid crystallizes at cooler temperatures and the toe is farthest from the heart -> SUPPORTED -> kept
- NIAMS: more common in men, middle age, women rarely before menopause -> SUPPORTED -> kept
- Risk factors (HBP, diabetes, obesity, kidney disease, family history, diuretics, low-dose aspirin, niacin, surgery/injury/illness, beer, fructose drinks, red/organ meat, shellfish) -> SUPPORTED (NIAMS, Mayo, ACFAS) -> kept
- Symptom "shiny, warm skin" -> "shiny" UNSUPPORTED (not in sources) -> changed to "Redness and warmth over the joint"
- Other symptoms (sudden night pain, bedsheet intolerance, extreme tenderness, other joints, tophi) -> SUPPORTED (Mayo, ACFAS, NIAMS) -> kept
- ACFAS: symptoms usually resolve in three to ten days with treatment -> SUPPORTED -> kept
- Mayo: NSAIDs, colchicine (best within 24 hours), corticosteroids by mouth or joint shot; urate-lowering medicines for repeated attacks; joint fluid, blood tests, imaging for diagnosis -> SUPPORTED -> kept
- "Corticosteroid joint injection ... Mayo Clinic and ACFAS describe when pills are not a good fit" -> MISATTRIBUTED (neither source gives that indication) -> reworded to what Mayo and ACFAS actually say; non-listed service, reviewer note already asks
- ACFAS rest/immobilize and elevate; fluids; purine restriction; see primary care for maintenance -> SUPPORTED -> kept
- Recovery "NIAMS describes untreated flares lasting a week or two" -> MISATTRIBUTED qualifier (NIAMS does not say untreated) -> corrected
- NIAMS: untreated flares may become more frequent; tophi; "one of the most controllable forms of arthritis" -> SUPPORTED -> kept
- Self-care cool pack -> UNSUPPORTED by cited pages, conservative general advice -> kept, reviewer note added; alcohol/beer, purine foods, aspirin caution -> SUPPORTED
- Red flags (fever with hot joint per Mayo; first sudden intense joint pain per Mayo; infection signs; not improving; repeated attacks/tophi) -> SUPPORTED / standard -> kept
- FAQ1 "big toe joint also takes a lot of force with every step" -> UNSUPPORTED -> replaced with NIAMS statement that many first flares start in the big toe
- FAQ2 ACFAS 3 to 10 days, NIAMS week or two, Mayo worst in 8 to 12 hours then days to weeks -> SUPPORTED -> kept
- FAQ4 foods (ACFAS, Mayo) -> SUPPORTED; FAQ5 Mayo fever with hot joint, joint fluid test -> SUPPORTED; FAQ6 NIAMS tophi damage, kidney stones -> SUPPORTED
- ICD-10 M10.9 Gout, unspecified -> SUPPORTED -> kept

## corns-calluses
Sources fetched: ACFAS corns, Mayo Clinic (symptoms/causes), Mayo Clinic (diagnosis/treatment), NHS, icd10data L84. All 5 resolve (200). Added and fetched: AAOS OrthoInfo "Corns" (200).
- Lede "Our podiatrists safely trim them and fix the rubbing" -> trimming is not a listed service and "fix" reads as a promise -> reworded to "A podiatrist can trim them safely and look for the rubbing"
- "ACFAS describes a corn as ... hard central core, which presses into the deeper skin and can hurt" -> MISATTRIBUTED in part (ACFAS: small circular lesion with central core; "deeper" and "painful when pressed" are Mayo) -> split attribution ACFAS/Mayo
- "Soft corns ... where skin stays moist" and symptom "soft, whitish corn" -> UNSUPPORTED detail -> removed
- Callus usually on soles/heels, rarely painful (Mayo) -> SUPPORTED -> kept
- Mayo risk factors (tight/loose shoes, no socks, hammertoe, hallux valgus, seams, inherited tendency) -> SUPPORTED -> kept; NHS "not often serious" -> SUPPORTED
- Mayo: diabetes/poor blood flow, minor injury can become infected ulcer -> SUPPORTED -> kept
- Symptoms (thick rough skin, raised bump, tenderness, flaky/dry/waxy skin; infection signs per NHS) -> SUPPORTED -> kept
- ACFAS: corn may return if cause not treated; avoid home removal and medicated pads -> SUPPORTED -> kept
- Mayo: paring with scalpel "a standard in office treatment" -> overstated (Mayo: "can be done during an office visit") -> corrected
- Padding "toe sleeves ... according to Mayo Clinic" -> MISATTRIBUTED item (Mayo lists felt pads, nonmedicated pads, toe separators, lamb's wool) -> toe sleeves replaced with lamb's wool, AAOS added; same fix in self-care
- Mayo: 40% salicylic acid patch; OTC salicylic acid can irritate skin and cause infection, especially in diabetes -> SUPPORTED -> kept
- Mayo/AAOS: custom orthotics, surgery to correct bone alignment -> SUPPORTED -> kept
- "Regular professional care of calluses lowers the chance of a hidden sore forming" -> UNSUPPORTED effectiveness claim -> replaced with Mayo advice to get care before self-treating; wound care (listed service) kept
- First visit "the doctor may trim the thick skin" -> implies a same-day procedure (BRIEF forbids inventing) -> reworded to "explains your options, which may include trimming"; reviewer note added
- Recovery "Trimming a painful corn often brings quick relief" -> UNSUPPORTED effectiveness wording -> replaced with AAOS "a doctor may trim a corn to relieve pain"
- Recovery "People with diabetes often benefit from regular, scheduled foot care" -> UNSUPPORTED -> replaced with Mayo advice
- NHS: see a professional after 3 weeks without improvement; do not cut corns yourself; do not self-treat with diabetes/circulation/immune problems -> SUPPORTED -> kept
- Self-care (thick socks, wide low-heeled shoes per NHS; moisturize per Mayo/NHS; no pumice with diabetes per Mayo) -> SUPPORTED -> kept
- Red flags (diabetes/circulation/immune; bleeding/pus/discharge; severe or activity-limiting pain; 3 weeks per NHS; spreading redness and fever as standard infection signs) -> SUPPORTED / conservative -> kept
- FAQ1-FAQ4 -> SUPPORTED (Mayo, ACFAS, NHS) -> kept
- FAQ5 soft corn mechanism (bones pressing, sweat keeps it soft and whitish) -> UNSUPPORTED -> rewritten to AAOS wording; AAOS source appended
- FAQ6 "a thick callus raises pressure" and "regular trimming and pressure relief helps protect the skin" -> UNSUPPORTED effectiveness -> rewritten to Mayo wording
- No Medicare/coverage statements present -> compliant
- ICD-10 L84 Corns and callosities (billable) -> SUPPORTED -> kept

## peroneal-tendonitis
Sources: ACFAS (200), Cleveland Clinic (200), icd10data M76.7 (200), NCBI StatPearls NBK544354 (resolves; Firecrawl hit a reCAPTCHA wall, content retrieved via WebFetch).
- ACFAS anatomy (two tendons behind outer ankle bone; one to outer midfoot, one under foot to arch; stabilize and protect from sprains) -> SUPPORTED -> kept
- ACFAS: sports with repetitive ankle motion; high arches -> SUPPORTED -> kept
- Cleveland Clinic risk list (over 40, tight tendons, prior tendon injury, overweight, smoking, diabetes, gout, RA) -> SUPPORTED -> kept
- "Runners, tennis players, and pickleball players around Jupiter are common examples" -> UNSUPPORTED prevalence-style claim -> reworded as framing about repeated stress
- Lede "early care in Jupiter can keep a strain from becoming a tear" -> implied outcome promise -> replaced with Cleveland Clinic statement that untreated tendonitis can progress to a tear
- Symptoms (outer ankle pain, worse with activity, swelling/warmth/redness, thickened tendon, instability, snapping suggests subluxation) -> SUPPORTED (ACFAS, CC) -> kept
- Causes incl. congenital groove/bone shape (ACFAS), sprain, instability -> SUPPORTED -> kept
- "StatPearls ... a boot or cast ... which may run four to six months for stubborn cases" -> MISATTRIBUTED nuance (StatPearls: NSAIDs, ice, rest or immobilization, PT, lateral heel wedge; "non-operative treatment should be for 4 to 6 months", not limited to stubborn cases) -> corrected
- ACFAS nonsurgical list (immobilization, medication, PT, bracing) -> SUPPORTED -> kept
- Cleveland Clinic steroid injection into tendon sheath -> SUPPORTED; "steroid exposure is a listed risk factor for tendon tears" -> overstated (StatPearls: steroids associated with tendon disease) -> corrected
- PRP "StatPearls: may help when the first round of conservative care does not settle the tendon" -> MISATTRIBUTED indication (StatPearls: ultrasound-guided PRP has shown improved functional outcomes in tendinopathy) -> corrected; PRP is a listed practice service
- Surgery: debridement/synovectomy (CC, StatPearls), tear repair (ACFAS, StatPearls), groove deepening (StatPearls) -> SUPPORTED -> kept
- First visit resisted eversion, subluxation check (StatPearls), imaging (ACFAS, CC) -> SUPPORTED -> kept
- Recovery: CC 3 to 4 weeks conservative, longer after sprain; 4 to 6 weeks cast after surgery then PT; StatPearls return to sport by three months -> SUPPORTED -> kept
- Self-care (activity reduction, ice, supportive shoes, elevation) -> SUPPORTED (CC RICE); avoid sand runs -> conservative framing -> kept
- Red flags (cannot bear weight, cannot rotate ankle, snap/pop, sudden severe pain, swelling/discoloration per CC; instability per ACFAS) -> SUPPORTED -> kept
- FAQ3 "about 60 percent of peroneal tendon injuries were first misdiagnosed" -> overstated scope (CC: one study of 40 people) -> qualifier added
- FAQ2, FAQ4, FAQ5 (CC rupture risk; ACFAS bracing; StatPearls 4 to 6 months) -> SUPPORTED -> kept; FAQ6 practice facts -> matches BRIEF
- ICD-10 M76.7 Peroneal tendinitis -> SUPPORTED; non-billable parent (children M76.70/71/72) already noted -> kept

## posterior-tibial-tendon-dysfunction
Sources: ACFAS (adult-acquired-flatfoot URL redirects to /conditions/posterior-tibial-tendon-dysfunction-(pttd), 200), Cleveland Clinic (22057 URL redirects to /health/diseases/posterior-tibial-tendonitis-posterior-tibial-tendon-dysfunction, 200), NCBI StatPearls NBK542160 (resolves; retrieved via WebFetch), icd10data M76.82 (200).
- ACFAS and Cleveland Clinic source URLs -> resolve only via redirect -> updated to canonical URLs
- Anatomy (calf muscle to inner foot bones, behind inner ankle bump, major arch support) -> SUPPORTED (CC, ACFAS) -> kept
- ACFAS: acquired, typically progressive -> SUPPORTED -> kept
- "StatPearls: classic patient in her fifties or sixties" -> WRONG (StatPearls: woman with obesity in her sixth decade, i.e. her fifties) -> corrected
- StatPearls risk factors (hypertension, obesity, diabetes, previous trauma, steroid exposure) -> SUPPORTED -> kept
- Symptoms (inner ankle pain/swelling, worse with walking/stairs, flattening arch, ankle rolls in and toes turn out, weak push-off/heel rise, later lateral pain) -> SUPPORTED (ACFAS, CC) -> kept
- Causes (overuse per ACFAS; weight, injury, RA, flat foot structure per CC) -> SUPPORTED -> kept
- StatPearls: boot or cast up to 3 to 4 weeks, eccentric strengthening PT, conservative therapy 3 to 4 months -> SUPPORTED -> kept
- "89 percent of patients with early-stage disease responded" (intro and FAQ1) -> MISATTRIBUTED scope (StatPearls: stages I and II) -> corrected in both places and in reviewer note
- ACFAS orthotics/bracing, immobilization, PT, NSAIDs, shoe modifications; surgery when progressed or failed -> SUPPORTED -> kept (orthotics/braces not listed services; reviewer note already asks)
- Reconstructive surgery (tendon repair/transfer, calcaneal osteotomy, arthrodesis by stage) -> SUPPORTED (StatPearls) -> kept
- First visit too-many-toes sign (StatPearls: more than two toes), single-limb heel rise, imaging -> SUPPORTED -> kept
- Recovery (CC: acute tendonitis a few weeks; 3 to 4 months conservative; 2 to 4 months after surgery; surgical outcome less predictable, lingering effects; StatPearls less predictable) -> SUPPORTED -> kept
- FAQ4 StatPearls custom orthotics with medial forefoot posting -> SUPPORTED -> kept
- Self-care and red flags -> conservative, consistent with CC/ACFAS -> kept
- FAQ6 practice facts (Dr. Cedeno board-certified foot and ankle surgeon) -> matches BRIEF -> kept
- ICD-10 M76.82 Posterior tibial tendinitis -> SUPPORTED; non-billable parent already noted; reviewer asked to choose vs M21.4- -> kept

## haglunds-deformity
Sources: ACFAS curly-apostrophe URL haglund%E2%80%99s-deformity (fetched, HTTP 200, correct page; left unchanged), Cleveland Clinic (200), APMA /heelpain (redirects to /patients-and-the-public/conditions-affecting-the-foot-and-ankle/heel-pain/, 200), AAOS /en/diseases--conditions/achilles-tendinitis/ (redirects to /diseases--conditions/achilles-tendinitis/, 200).
- APMA and AAOS URLs -> resolve only via redirect -> updated to canonical; ACFAS curly-apostrophe URL -> resolves -> no fix needed, stale reviewer note removed
- Lede "most cases settle with the right care" -> outcome-style claim -> replaced with Cleveland Clinic "surgery is rarely needed"
- ACFAS: bony enlargement on back of heel; bursitis from shoe rubbing; pump bump from rigid backs (pumps, men's dress shoes, ice skates) -> SUPPORTED -> kept
- "work boots" (what_it_is and causes) -> UNSUPPORTED (not in any source) -> removed
- Cleveland Clinic: very common, more frequent in women, family history; at Achilles attachment -> SUPPORTED -> kept
- ACFAS: high arch, tight Achilles, walking on outside of heel -> SUPPORTED -> kept; "high arches that tilt the heel back against the shoe" mechanism -> UNSUPPORTED -> trimmed to "High arches"
- Symptoms (bump, pain at Achilles attachment, swelling, redness, discoloration, heel counter aggravation per APMA, one or both heels) -> SUPPORTED -> kept
- ACFAS nonsurgical list; nonsurgical care does not shrink the bone; CC surgery rarely needed -> SUPPORTED -> kept
- Shoe changes "often the single biggest relief" -> UNSUPPORTED superlative -> replaced with Cleveland Clinic "most important way to manage symptoms is to avoid the shoes..."
- Heel lifts (ACFAS, AAOS), heel cups/orthotics (CC), stretching/PT (ACFAS, CC), NSAIDs/ice -> SUPPORTED -> kept
- EPAT "AAOS lists ESWT among nonsurgical options for insertional Achilles tendinitis" -> MISATTRIBUTED scope and missing caveat (AAOS: ESWT studies show improvement for Achilles tendinitis; more information needed before strong recommendations) -> rewritten with caveat; EPAT is a listed service; reviewer note added
- Surgery: remove bony growth and inflamed tissue (CC), with damaged tendon (AAOS debridement) -> SUPPORTED -> kept
- Recovery "Many people feel relief within weeks" -> UNSUPPORTED timeframe -> replaced with Cleveland Clinic "most people feel better over time"; CC several weeks to a few months after surgery; AAOS boot within 2 weeks, up to 12 months rehab when tendon involved -> SUPPORTED -> kept
- Self-care (soft/open-backed shoes, padding, ice, stretching, avoid uphill/hard-surface running per ACFAS) -> SUPPORTED -> kept
- Red flags (pain beyond a few weeks, trouble walking, swelling, sudden loss of function or severe pain -> ER per CC; pop per AAOS; skin breakdown with diabetes) -> SUPPORTED / conservative -> kept
- FAQs 1 to 5 (CC, ACFAS, APMA, AAOS) -> SUPPORTED -> kept; FAQ6 practice services (EPAT, surgery) -> on the BRIEF list -> kept
- ICD-10 null -> acceptable per BRIEF (no single verified code); doctor to choose

## sesamoiditis
Sources fetched: AAOS OrthoInfo, Cleveland Clinic, ACFAS. All 3 resolve (200).
- AAOS: two sesamoids about the size of a corn kernel, attached to big toe flexor tendons, act like pulleys -> SUPPORTED -> kept
- CC: inflammation of the sesamoid bones and the tendons they sit in -> SUPPORTED -> kept
- AAOS: common in ballet dancers, runners, baseball catchers -> SUPPORTED -> kept; CC high heels, high arches, bunions -> SUPPORTED; ACFAS basketball, tennis, high arches -> SUPPORTED
- Look-alikes stress fracture and turf toe (ACFAS) -> SUPPORTED -> kept
- Symptoms (pain under big toe, dull ache building per CC, worse with certain shoes/activities per ACFAS, trouble bending toe, difficulty bearing weight, swelling/bruising per AAOS) -> SUPPORTED -> kept
- AAOS nonsurgical list (rest, aspirin/ibuprofen, ice, soft-soled low-heeled or stiff-soled shoes, felt pad, taping toe slightly downward, steroid injection, short-leg fracture brace 4 to 6 weeks if symptoms continue; J-shaped pad for fracture) -> SUPPORTED -> kept
- AAOS "most sesamoid problems go away without surgery" -> SUPPORTED -> kept; ACFAS immobilization, PT, cortisone, custom orthotics -> SUPPORTED
- Orthotics "with cushioning or a cutout under the big toe joint" -> "cutout" UNSUPPORTED -> rewritten to ACFAS wording (custom orthotics to balance pressure)
- Surgery (removal or repair; rare per CC; AAOS for longstanding cases, displaced or nonhealing fractures) -> SUPPORTED -> kept
- First visit (press on sesamoids, move big toe, gait and shoe wear per ACFAS; X-rays incl. other foot, bone scan, MRI per AAOS) -> SUPPORTED -> kept
- Recovery (CC mild cases days, severe months; AAOS weeks or months in cast/brace because every step loads the forefoot) -> SUPPORTED -> kept
- Red flag "does not improve after a week or two of rest" -> UNSUPPORTED timeframe -> changed to "does not improve with rest"; other red flags conservative -> kept
- FAQ1 (AAOS fracture pain after hyperextension; X-ray, bone scan, MRI for subtle stress fracture) -> SUPPORTED -> kept
- FAQ4 taping "reduces stretch on the tendons" and "pad that sits behind the sesamoids" -> UNSUPPORTED mechanism/position -> replaced with ACFAS (relieves tension) and AAOS (felt or dense foam cushioning pad)
- FAQ2, FAQ5 (CC timelines, high heels) -> SUPPORTED -> kept
- ICD-10 null -> acceptable per BRIEF; doctor to choose code

## Summary (all 12 files)
- All 12 JSON files re-validated after edits: parse OK; zero em/en dashes; no banned words, exclamation marks or "not only / more than just" constructions; seo_title <= 60, seo_desc 140 to 158, lede <= 30 words, intro 60 to 100, what_it_is 50 to 90, first_visit 50 to 80, recovery 60 to 110, FAQ answers 40 to 80 words.
- No Medicare, insurance, referral or Florida-law claims appear in any page body (one reviewer note in corns-calluses asks about Medicare routine foot care; nothing was written).
- Source URLs: every cited URL was retrieved. Six resolved only via redirect and were updated to canonical URLs (metatarsalgia Mayo drc; PTTD ACFAS and Cleveland Clinic; Haglund's APMA and AAOS). The ACFAS Haglund's curly-apostrophe URL resolves (HTTP 200, correct page) and was left as is. NCBI Bookshelf pages sit behind a reCAPTCHA for Firecrawl but were retrieved through WebFetch.
- ICD-10 codes verified on icd10data.com (2027 edition): L60.0, M20.40, G57.60, B35.1, M84.37 (non-billable parent), M77.40, M10.9, L84, M76.7 (non-billable parent), M76.82 (non-billable parent). Haglund's and sesamoiditis left null.
