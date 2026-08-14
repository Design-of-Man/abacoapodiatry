# Image prompts, one per page

Paste these into Microsoft Copilot (or anything else that generates images), download the
results, and upload the raw files to `assets/img/atmos/` using GitHub's web uploader:

> https://github.com/Design-of-Man/abacoapodiatry/upload/main/assets/img/atmos

Name each file with the slug given in the left column, any extension. Resizing, WebP
conversion, `alt` text and wiring into the pages is handled from there — none of that
needs a subscription.

## Append this to every prompt

```
Editorial lifestyle photograph. Natural warm light, shallow depth of field, muted
natural colour, nothing oversaturated. Framed from the knee down only: no faces, no
torsos, nobody above the knee. No text, no logos, no watermarks, no medical equipment,
no clinical or hospital setting. 16:9 landscape.
```

## Reject and regenerate if

Feet are the hands problem in miniature, and this is the one site on the internet where
visitors will notice.

- **More or fewer than five toes**, or toes that merge into each other
- **The arch bending the wrong way**, or an ankle that fuses into the leg with no joint
- Anyone visible above the knee, or any face in frame
- Anything that reads as a clinic, a treatment room or a medical device
- Text baked into the image, which these models still garble

Shod feet and close crops fail far less often than bare full-foot shots. Where a prompt
below asks for bare feet and the result is wrong three times, switch to the shod version
rather than fighting it.

---

## Locations (15)

Each one is a different town, so each gets a different activity. The point is the thing
people in that town are on their feet doing.

| File | Prompt |
|---|---|
| `loc-abacoa` | Walking shoes on a paved town-centre walkway beside low landscaped planters, late afternoon shadows |
| `loc-hobe-sound` | Worn hiking shoes on a sandy pine-scrub trail, dappled light through slash pines |
| `loc-juno-beach` | Bare feet at the waterline on hard-packed sand beside weathered pier pilings, shallow wash of seawater |
| `loc-jupiter` | Running shoes mid-stride on a wooden riverwalk boardwalk, turquoise inlet water blurred behind |
| `loc-lake-park` | Boat shoes on a sun-bleached marina dock, cleat and mooring line in the foreground |
| `loc-north-palm-beach` | Golf shoes on clipped fairway grass, long morning shadow, golf bag strap just in frame |
| `loc-palm-beach-gardens` | Court shoes on a blue pickleball court, paddle resting against one ankle |
| `loc-palm-city` | Riding boots in stirrups seen from behind and below, sandy paddock, warm low light |
| `loc-port-salerno` | Deck boots on a working fishing dock, coiled rope and wet planking |
| `loc-riviera-beach` | Sandals on a concrete marina walkway, boat hulls out of focus behind |
| `loc-singer-island` | Bare feet on hot pale sand with a beach towel corner, dune sea oats blurred behind |
| `loc-stuart` | Leather loafers on a brick historic-downtown sidewalk, shopfront awning shadow |
| `loc-tequesta` | Sneakers on a quiet tree-lined residential sidewalk, dappled oak shade |
| `loc-west-palm-beach` | Dress shoes on a downtown waterfront promenade, palm shadows across pale pavers |
| `loc-index` | Two pairs of shoes side by side on a wooden dock, one athletic and one dress, warm evening light |

## Conditions (7)

The thing the condition takes away.

| File | Prompt |
|---|---|
| `cond-heel-pain` | Bare feet lowering onto a wooden bedroom floor from the edge of a bed, first light through a window |
| `cond-arthritis` | Bare feet paused halfway up a wooden staircase, hand rail spindle shadow across the step |
| `cond-flat-feet` | Work shoes on a hard commercial floor beside a rubber anti-fatigue mat, flat overhead light |
| `cond-diabetic-foot-care` | Bare feet resting on a folded towel on a bathroom floor, soft even daylight, calm and domestic |
| `cond-sports-injuries` | Soccer cleats mid-pivot on turf, small spray of grass, motion blur at the edges |
| `cond-sprains-strains` | Trail shoes on an uneven rocky path, one foot rolled slightly on a loose stone |
| `cond-index` | Several pairs of shoes lined up by a front door, everyday and athletic mixed, warm hallway light |

## Services (9)

Feet and footwear as the subject.

| File | Prompt |
|---|---|
| `svc-index` | Bare feet on smooth warm stone beside a shallow pool of water, calm and restorative |
| `svc-mls-alt` | A foot flexing over the edge of a wooden step, calf and achilles in warm side light |
| `svc-shockwave` | Running shoes and a foam roller on a wooden floor after a session, low sun across the boards |
| `svc-prp-therapy` | Bare heel resting on cool tile, single soft light source, quiet and clinical-free |
| `svc-regenerative-medicine` | Feet in thick wool socks on a rug beside a window, morning light, restful |
| `svc-stem-cell-therapy` | Bare feet on smooth river stones in shallow clear water, dappled light |
| `svc-foot-ankle-surgery` | Clean white trainers on a sunlit path, laces neatly tied, a sense of returning to normal |
| `svc-foot-bbl` | Bare feet on a thick soft rug, close crop on the heel and forefoot cushion, warm lamp light |
| `svc-wound-care` | Feet in clean cotton socks resting on a footstool, soft daylight, calm domestic setting |

## Blog (3)

| File | Prompt |
|---|---|
| `blog-index` | An open notebook and a pair of running shoes on a wooden table, morning coffee light |
| `blog-plantar-fasciitis` | Bare feet on a bedroom floor at dawn, weight just taken on the heels, long low light |
| `blog-laser-vs-cortisone` | Two pairs of shoes on a bench, one athletic one everyday, even neutral light, a sense of choosing |

## Also worth having (3)

| File | Prompt |
|---|---|
| `page-about` | Two pairs of shoes on a doorstep in warm evening light, one larger one smaller, welcoming |
| `page-new-patients` | Clean sneakers on a doormat at an open front door, bright inviting daylight |
| `page-telehealth` | Feet in socks up on a sofa beside a laptop on a low table, relaxed home light |

---

**Not on this list, deliberately.** Nothing depicting the practice: no office, no treatment
rooms, no equipment, no staff, no patients. A generated photo of "our treatment room" is a
false claim on a medical site, and those shots are the ones only a real camera can supply.
They are in `_dev/photo-shotlist.md`, including the two that `preflight.py` currently
blocks launch on.

Anatomy stays on the six hand-built SVG diagrams. These models garble vessel structure and
any text baked into an image, and a wrong anatomical illustration on a page someone is
reading about their own condition is worse than no illustration.
