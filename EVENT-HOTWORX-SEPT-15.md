# Promo kit — "Sweat. Recover. Stand." · Tue Sept 15, 4:00 PM

Everything needed to push the HOTWORX Palm Beach Gardens event. Copy blocks below
are meant to be pasted as-is.

---

## Assets

| File | What it's for |
|---|---|
| `assets/img/events/hotworx-sept-15.jpg` | The original poster, unmodified. Instagram/Facebook feed, stories. |
| `assets/img/events/hotworx-sept-15-flyer.png` | **Print this.** Letter portrait, 150 DPI. Poster + a QR band and the office number. Front desk at HOTWORX, checkout at both offices. |
| `assets/img/events/hotworx-sept-15-qr.png` | The QR on its own, 900px. For dropping into someone else's layout. |
| `assets/img/events/hotworx-sept-15-og.png` | 1200×630 link preview. Used automatically when the event page is shared. |

Landing page: **`/hotworx/`** — see `_src/pages/event-hotworx.html`.

### ⚠️ Read this before printing the flyer

The QR points at **`https://abacoapodiatry.vercel.app/hotworx/`**, not at
jupiterlaser.com. That is deliberate: the domain has not cut over yet, so
jupiterlaser.com still serves the *old* site and a QR aimed there would land on a
404 in front of a room full of people. The Vercel host works today.

The flyer prints no typed-out web address for the same reason — the QR carries the
link, and the phone number carries everyone who won't scan.

After the domain cutover, regenerate all four assets with the real URL:

```
EVENT_URL=https://jupiterlaser.com/hotworx/ python3 _src/event_hotworx.py
```

(Requires `pip install Pillow segno`.)

---

## Google Business Profile — "Event" post

Do this on **each** participating business's profile. Same event, four listings, four
audiences. It's free and it surfaces in Maps and in local searches.

**Where:** Google Business Profile → Promote → Add event.

**Event title** (58 char limit)

```
Sweat. Recover. Stand. — Free Foot & Ankle Q&A
```

**Start:** Sept 15, 2026, 4:00 PM · **End:** Sept 15, 2026, 6:00 PM

**Photo:** upload `hotworx-sept-15.jpg`

**Button:** *Call now* → (561) 915-1934

### Details text — Abacoa Podiatry & Leg Vein Center

```
Bring us the foot question you've been putting off.

Tuesday, September 15 at 4:00 PM, Dr. Orlando Cedeno is at HOTWORX Palm Beach
Gardens (3980 Northlake Blvd) to answer questions in person — no appointment, no
paperwork, no cost.

Ask about custom orthotics built from your own foot, shockwave and cold laser for
heel pain that won't quit, or laser treatment for fungal nails and spider veins.

Joined by RegenOrtho Palm Beach, Elite Sports Medicine, and HOTWORX. Snacks and
refreshments provided. Drop in any time after 4:00.

Questions, or to save a spot for the IV night: (561) 915-1934
```

### Details text — RegenOrtho Palm Beach

```
An afternoon of recovery under one roof.

Tuesday, September 15 at 4:00 PM at HOTWORX Palm Beach Gardens, 3980 Northlake
Blvd. Come talk with us about peptides and biologics, physician-directed
regenerative care, and clinician-supervised IV wellness and NAD+ drips — and put
your name down for the upcoming IV night.

Joined by Abacoa Podiatry, Elite Sports Medicine, and HOTWORX. Snacks and
refreshments provided. Free to attend, drop in any time.

Questions or IV night sign-ups: (561) 915-1934
```

### Details text — HOTWORX Palm Beach Gardens

```
We're opening the studio.

Tuesday, September 15 at 4:00 PM, we're hosting Abacoa Podiatry, RegenOrtho Palm
Beach, and Elite Sports Medicine at 3980 Northlake Blvd. Bring your questions
about recovery, training through pain, orthotics, heel pain, and IV wellness.

Never tried infrared sauna training? Sessions run 15 to 45 minutes — ask us about
your first one while you're here.

Snacks and refreshments provided. Free, and you don't need to work out to come.
```

### Details text — Elite Sports Medicine

```
Training through something that hurts?

Tuesday, September 15 at 4:00 PM at HOTWORX Palm Beach Gardens, 3980 Northlake
Blvd. We're there with Abacoa Podiatry and RegenOrtho Palm Beach to answer
questions about injuries that keep coming back, getting back to activity, and
what's actually worth treating.

Free to attend. Snacks and refreshments provided. Drop in any time after 4:00.
```

---

## Facebook Event

Create it on the **Abacoa Podiatry** page, then add HOTWORX Palm Beach Gardens,
RegenOrtho Palm Beach, and Elite Sports Medicine as **co-hosts** — that is the whole
point. Co-hosting puts the event in front of all four audiences instead of one, and
Facebook sends attendees an automatic reminder the day before and again at the hour.

| Field | Value |
|---|---|
| Name | Sweat. Recover. Stand. |
| Date | Tuesday, September 15, 2026 · 4:00 PM – 6:00 PM |
| Location | HOTWORX Palm Beach Gardens, 3980 Northlake Blvd, Palm Beach Gardens, FL |
| Cover photo | `hotworx-sept-15.jpg` |
| Category | Health & Wellness |
| Ticket/link URL | the `/hotworx/` page |

Description:

```
One afternoon. Four practices. Bring your questions.

Dr. Orlando Cedeno of Abacoa Podiatry will be in the studio answering foot and
ankle questions in person — custom orthotics, heel pain, shockwave and cold laser,
fungal nails, spider veins. No appointment, no paperwork, no cost.

RegenOrtho Palm Beach on peptides, biologics, IV wellness and NAD+ (sign up for the
IV night while you're there). Elite Sports Medicine on training through pain and
getting back to activity. HOTWORX on infrared sauna training — sessions run 15 to
45 minutes, ask about trying your first one.

Snacks and refreshments provided. Come at 4:00 or come at 5:15 — it runs as an open
house, not a lecture. You don't have to work out.

HOTWORX Palm Beach Gardens · 3980 Northlake Blvd
Questions, or to save a spot for IV night: (561) 915-1934
```

---

## Patient text / email blast

The highest-intent list in this whole thing. Send to the Jupiter and Palm Beach
Gardens area, weighted toward anyone seen for heel pain, orthotics, or nail concerns.

**SMS** (keep it under 320 characters so it doesn't split badly):

```
Abacoa Podiatry: Dr. Cedeno is doing a free open Q&A this Tuesday 9/15 at 4 PM at
HOTWORX Palm Beach Gardens, 3980 Northlake Blvd. Bring any foot question — orthotics,
heel pain, nails. Snacks provided, no appointment needed. Details: [link]
Reply STOP to opt out.
```

**Email subject lines** — pick one:

- Free foot & ankle Q&A this Tuesday — bring your questions
- Dr. Cedeno is answering questions Tuesday at 4 (no appointment)
- That foot thing you've been meaning to ask about

---

## Instagram / Facebook caption

```
The foot question you've been putting off? Tuesday. 4 PM. Free.

Dr. Cedeno is at HOTWORX Palm Beach Gardens answering foot and ankle questions in
person — orthotics, heel pain, shockwave and cold laser, fungal nails, spider veins.
No appointment. No paperwork. No cost.

Plus @regenortho on peptides, IV wellness and NAD+, and Elite Sports Medicine on
training through pain.

Snacks and refreshments. Come any time after 4.
3980 Northlake Blvd · Questions: (561) 915-1934

#jupiterfl #palmbeachgardens #footpain #plantarfasciitis #heelpain #recovery
#infraredsauna #podiatrist
```

## Story text (run one a day until Tuesday)

Add the **countdown sticker** to each, and the **location sticker** for HOTWORX
Palm Beach Gardens. All four businesses should reshare each other's.

1. `4 days out. Bring us your worst foot question.`
2. `Free. Tuesday. 4 PM. No appointment.`
3. `Heel hurts every morning? Come ask why.`
4. `Tomorrow. HOTWORX PBG, 4 PM. Snacks are on us.`
5. `Today. 4 PM. Walk in whenever.`
