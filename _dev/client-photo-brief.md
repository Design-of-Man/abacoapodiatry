# For the practice — the photos we need

Forward the section below to whoever can walk around the office with a phone. It's written
for someone who does not work in tech or photography, so please don't add jargon to it.

**Why it matters:** the new site currently uses generic lifestyle imagery on the condition,
service and location pages. That is fine for atmosphere, and it is deliberately *not* a
picture of your office. Anything that shows the practice itself — the building, the rooms,
the machines, the doctors — has to be a real photograph, because on a medical site a photo
is a claim about the room and the equipment, and that claim should be true. We will not
generate those.

Two of the shots below are already referenced in the built pages, so the site's own
pre-launch check fails until they exist. Both pages currently show a gold monogram tile
instead, which reads as deliberate rather than broken, so nothing looks wrong to a visitor
in the meantime.

**Every shot below also does double duty on the Google Business Profile**, where the
listing is thin and photos drive local ranking. One walk-around covers both jobs.

---

## Copy from here

Hi — we need some real photos of the practice for the new website.

Your phone is genuinely fine for all of this. A few ground rules that make the difference
between usable and not:

- **Shoot landscape** (turn the phone sideways), not portrait.
- **Daylight wherever possible.** Open blinds, turn on the lights, avoid using flash.
- **Clear the clutter** out of frame first — coffee cups, paperwork, cables, bins.
- **Hold still,** tap the screen on the thing you want sharp, then take three of each.
- **No patients in any shot** unless they have signed a release, and **no computer screens
  showing patient information** — please double-check the background for this one.

### The two we need most

These two are already built into the site and are the last things holding up the check.

1. **The building from the parking lot.** Entrance and signage visible. This is the photo a
   patient looks at to know they have arrived at the right place. Stand back far enough to
   get the whole entrance in.
2. **The MLS laser unit.** Three-quarter view, from slightly to the side rather than
   straight on, with the treatment head in the shot. It needs to be *your* machine.

### Then, in order of how much each one earns

3. **A treatment room, wide.** Stand in the doorway and get the whole room. Patients want
   to see where they will be sitting.
4. **A treatment happening** — the laser head over a foot, no faces in frame. This is the
   single most useful image on the whole site. It is the one that makes the treatment pages
   feel real instead of theoretical.
5. **Both doctors together.** The site has separate portraits but no shot of the pair. A
   practice with two surgeons should look like one.
6. **The front desk and waiting area.** This reduces first-visit nerves, and it is the
   image Google shows most often in local search results.
7. **The shockwave unit and the ultrasound machine.** The website describes both; showing
   them is the proof.
8. **The Palm Beach Gardens office from outside.** That location has its own page and its
   own Google listing, and right now no photo at all.

Send them however is easiest — email, text, a shared folder, whatever. Originals please,
not screenshots, and don't crop or filter them; we'll handle that end.

If anything on the list is awkward to photograph, just tell us and we'll work around it.

## Copy to here

---

## On our side, once they arrive

1. Drop `office.jpg` and `mls-laser.jpg` into `assets/img/photos/`. Those two clear the
   `ASSETS` section of `_dev/preflight.py`, taking the baseline from 4 failures to 2.
2. Resize to 1600px wide or less before committing. The atmos budget in
   `_dev/optimise-images.py` is 90KB for generated images; real photography can run a
   little heavier, but not unbounded — check the payload after.
3. The remaining shots slot into existing `.photo-frame` figures on `/technology/`,
   `/about/` and the service pages. **These get a `<figcaption>`** — that is the convention
   the 42 generated images deliberately do not use, so a caption reliably means "this is
   the practice's own photography."
4. Push the same set to the Google Business Profile in one pass. See `_dev/listings-nap.md`.
5. Tick the photo items in the `README.md` pre-launch checklist.
