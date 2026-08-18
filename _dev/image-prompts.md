# Image prompts — 42 pages, one each

Every page on the site that has no image and no diagram. Verified against the built
output, so this list is exactly the gap: pages that already carry an SVG diagram (the six
anatomy pages) are excluded, and so are the homepage (it has the hero video), `/privacy/`
and `/accessibility/`.

## Where to put the results

Upload the raw downloads, any format, any size, to:

> **`assets/img/atmos/`** — https://github.com/Design-of-Man/abacoapodiatry/upload/main/assets/img/atmos

**Name each file exactly the slug in the left column below**, keeping whatever extension
the download has. `conditions-heel-pain.png`, `locations-jupiter.jpg`, and so on. The
slug is the page path with slashes turned into hyphens, so wiring them in afterwards is
mechanical rather than a guessing game.

Then say so, and I'll run `_dev/optimise-images.py` (resize to 1200px, WebP under 90KB,
originals moved out of the deployment), write the alt text, wire each into its page, and
confirm CLS stays at 0.000.

## Append this to every prompt

```
Editorial lifestyle photograph. Natural warm light, shallow depth of field, muted
natural colour, nothing oversaturated. Framed from the knee down only: no faces, no
torsos, nobody above the knee. No text, no logos, no watermarks, no medical equipment,
no clinical or hospital setting. 16:9 landscape.
```

## Reject and regenerate if

Feet are the hands problem in miniature, and this is the one site on the internet where
visitors notice.

- **More or fewer than five toes**, or toes merging into each other
- **The arch bending the wrong way**, or an ankle fused into the leg with no joint
- Anyone visible above the knee, or any face in frame
- Anything reading as a clinic, treatment room or medical device
- Text baked into the image, which these models still garble

Shod feet and close crops fail far less often than bare full-foot shots. If a bare-feet
prompt below fails three times, switch it to the shod version rather than fighting it.

---

## Conditions (7)

The thing the condition takes away.

| File | Prompt |
|---|---|
| `conditions-heel-pain` | Bare feet lowering onto a wooden bedroom floor from the edge of a bed, weight just taken on the heels, first light through a window |
| `conditions-arthritis` | Bare feet paused halfway up a wooden staircase, handrail shadow falling across the tread |
| `conditions-flat-feet` | Work shoes standing on a hard commercial floor beside a rubber anti-fatigue mat, flat overhead light, end of a long shift |
| `conditions-diabetic-foot-care` | Bare feet resting on a folded white towel on a bathroom floor, soft even daylight, calm and domestic |
| `conditions-sports-injuries` | Soccer cleats mid-pivot on turf, small spray of torn grass, motion blur at the frame edges |
| `conditions-sprains-strains` | Trail running shoes on an uneven rocky path, one foot rolling slightly on a loose stone |
| `conditions` | Several pairs of shoes lined up along a hallway wall, everyday and athletic mixed, warm light from a doorway |

## Services (9)

Feet and footwear as the subject.

| File | Prompt |
|---|---|
| `services-vein-treatment` | Lower legs and bare feet elevated on cushions at the end of a sofa, calves and ankles in frame, warm evening light |
| `services-shockwave-therapy` | Running shoes and a foam roller on a wooden floor after a session, low sun raking across the boards |
| `services-prp-therapy` | A bare heel resting on cool pale tile, one soft directional light source, quiet and still |
| `services-regenerative-medicine` | Feet in thick wool socks on a rug beside a window, morning light, restful |
| `services-stem-cell-therapy` | Bare feet standing on smooth river stones in shallow clear water, dappled light on the surface |
| `services-foot-ankle-surgery` | Clean white trainers on a sunlit garden path, laces neatly tied, a sense of getting back to normal |
| `services-foot-bbl` | Bare feet sinking into a thick soft rug, close crop on the heel and the ball of the foot, warm lamp light |
| `services-wound-care` | Feet in clean cotton socks resting on a footstool, soft daylight, patient and unhurried |
| `services` | Bare feet on smooth warm stone beside a shallow pool of still water, calm and restorative |

## Locations (15)

One activity per town, because fifteen palm trees is not fifteen images.

| File | Prompt |
|---|---|
| `locations-jupiter` | Running shoes mid-stride on a wooden riverwalk boardwalk, turquoise inlet water blurred behind |
| `locations-abacoa` | Walking shoes on a paved town-centre walkway beside low landscaped planters, long late-afternoon shadows |
| `locations-palm-beach-gardens` | Court shoes on a blue pickleball court, a paddle resting against one ankle |
| `locations-north-palm-beach` | Golf shoes on closely mown fairway grass, long morning shadow, a bag strap just entering frame |
| `locations-juno-beach` | Bare feet at the waterline on hard-packed sand beside weathered pier pilings, thin wash of seawater |
| `locations-tequesta` | Sneakers on a quiet tree-lined residential sidewalk, dappled shade from live oaks |
| `locations-hobe-sound` | Worn hiking shoes on a sandy pine-scrub trail, dappled light through slash pines |
| `locations-singer-island` | Bare feet on hot pale sand beside the corner of a beach towel, sea oats blurred behind |
| `locations-riviera-beach` | Sandals on a concrete marina walkway, boat hulls out of focus behind |
| `locations-lake-park` | Boat shoes on a sun-bleached marina dock, a cleat and coiled mooring line in the foreground |
| `locations-west-palm-beach` | Dress shoes on a downtown waterfront promenade, palm shadows striping pale pavers |
| `locations-stuart` | Leather loafers on a brick historic-downtown sidewalk, striped shopfront awning shadow |
| `locations-port-salerno` | Deck boots on a working fishing dock, wet planking and coiled rope |
| `locations-palm-city` | Riding boots in stirrups seen from behind and below, sandy paddock, warm low light |
| `locations` | Two pairs of shoes side by side on a wooden dock, one athletic and one dress, warm evening light |

## Articles and blog (5)

| File | Prompt |
|---|---|
| `blog-5-signs-your-heel-pain-is-plantar-fasciitis` | Bare feet on a bedroom floor at dawn, weight just settling onto the heels, long low light |
| `blog-laser-therapy-vs-cortisone-injections` | Two pairs of shoes side by side on a wooden bench, one athletic one everyday, even neutral light, a sense of choosing between them |
| `how-mls-laser-therapy-relieves-foot-and-ankle-pain` | A bare foot flexing over the edge of a wooden step, calf and achilles caught in warm side light |
| `innovative-treatments-for-heel-pain-exploring-mls-laser-therapy` | A bare heel resting on a folded towel, single warm directional light, close and quiet |
| `blog` | An open notebook and a pair of running shoes on a wooden table, morning light across the page |

## Everything else (6)

| File | Prompt |
|---|---|
| `about` | Two pairs of shoes on a doorstep in warm evening light, one larger and one smaller, side by side |
| `new-patients` | Clean sneakers on a doormat at an open front door, bright inviting daylight beyond |
| `telehealth` | Feet in socks up on a sofa beside a laptop on a low table, relaxed lamp-lit evening |
| `faq` | Shoes slipped off beside an armchair with a mug on the floor next to them, unhurried afternoon light |
| `media` | Trainers on a wooden floor beside a notebook and a pair of headphones, soft window light |
| `reviews` | Shoes on a porch step in warm golden evening light, welcoming and settled |

---

**Not on this list, deliberately.** Nothing depicting the practice: no office, no treatment
rooms, no equipment, no staff, no patients. A generated photo of "our treatment room" is a
false claim on a medical site, and those are the shots only a real camera can supply. They
are in `_dev/photo-shotlist.md`, including the two that `preflight.py` blocks launch on.

Anatomy stays on the six hand-built SVG diagrams. These models garble vessel and joint
structure and any text baked into an image, and a wrong anatomical illustration on a page
someone is reading about their own condition is worse than no illustration at all.
