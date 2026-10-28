# Nov 16 evening talk: RSVP page and promo kit

"Tired, Achy Legs and Slow-Healing Joints: What's New in 2026." Monday, November 16, 2026, 5:00 PM, Jupiter office (4601 Military Trail, Suite 202).

Landing page: **https://jupiterlaser.com/rsvp/**. Source file: `_src/pages/event-nov-16-talk.html`.

The date moved from Feb 15, 2027 to Nov 16, 2026. Anything still saying February is out of date.

---

## What the page does

- RSVP form: name, cell, email, topic of interest, seats (1 or 2), "how did you hear about this," and an optional text-reminder consent box.
- Submissions go through FormSubmit to the same recipients as the contact form (angela.d@ primary, with Janice, Patricia, both doctors and Nick on CC). It reuses the contact form's exact action URL, so no new FormSubmit activation is needed. Like the contact form, spam is labelled in the email (`verified`, `flags`), never blocked.
- **Confirmation email (guest).** The office copy still comes from FormSubmit, unchanged. The guest's confirmation comes from `api/rsvp-confirm.js` through Resend, from events@jupiterlaser.com with replies going to angela.d@. It includes the date, address, "call if you can't make it" and a calendar invite. main.js only asks for it after FormSubmit confirms the office copy. If it fails, or `RESEND_API_KEY` isn't set in Vercel, the page says the office will confirm by text or phone, and Janice does. DNS for Resend (added Oct 28 in Dr. Cedeno's GoDaddy, via Nick's delegate access): TXT `resend._domainkey`, CNAME `send` → send.forge.rmta.net, CNAME `rsend` → rsend.forge.rmta.net. The Microsoft 365 records weren't touched.
- **Confirmation text is not automatic.** A static page can't send texts. See "Texting" below.
- Every RSVP records the link it came from (`src` in the email), so each source can be counted even when the guest skips the "how did you hear" question.
- **Calls are already tracked.** CallRail's number swap runs on every page, this one included, so calls from `/rsvp/` show up in CallRail with `/rsvp/` as the landing page.

## Checklist (Nick)

- [ ] **Today (Wed Oct 28):** get PR #94 reviewed and merged. The page and the QR codes only work once it's on `main`. HotWorx is tomorrow.
- [ ] **Today:** create one static CallRail number for print (cards and flyer) and send it to Rosie, so phone RSVPs from paper are counted. Don't hard-code it into the page. If it can't be done by Thursday, print the office number and rely on "how did you hear."
- [x] Live test Oct 28 ("TEST - Nick, please ignore"): reached the office with every field. No guest email, by design now (see above).
- [ ] **Thu Oct 29:** send Rosie and Janice their tagged links and QR codes (below).
- [ ] **Tue Nov 17:** take the page down. Add `/rsvp/` to `_src/redirect-map.tsv` pointing at `/services/vein-treatment/` (or a future events page), delete the page source, rebuild.

## Source-tagged links and QR codes

Give each channel its own link. The tag shows up as `src` in every RSVP email.

| Channel | Owner | Link | QR code |
|---|---|---|---|
| HotWorx sign-up table (Oct 29) | Rosie | `https://jupiterlaser.com/rsvp/?src=hotworx` | `assets/img/events/nov-16-qr-hotworx.png` |
| Printed invite cards | Danni / front desk | `https://jupiterlaser.com/rsvp/?src=card` | `assets/img/events/nov-16-qr-card.png` |
| Flyer | Rosie | `https://jupiterlaser.com/rsvp/?src=flyer` | `assets/img/events/nov-16-qr-flyer.png` |
| Patient blast (Nov 2) | Janice | `https://jupiterlaser.com/rsvp/?src=blast1` | |
| Second blast, if needed (Nov 9) | Janice | `https://jupiterlaser.com/rsvp/?src=blast2` | |
| Facebook / Instagram paid ad | Rosie | `https://jupiterlaser.com/rsvp/?src=meta-ad` | |
| Facebook / Instagram organic posts | Rosie | `https://jupiterlaser.com/rsvp/?src=social` | |
| Jupiter Chamber | Rosie | `https://jupiterlaser.com/rsvp/?src=chamber` | |
| Wellness Collective | Rosie | `https://jupiterlaser.com/rsvp/?src=wellness` | |
| RegenOrtho / Elite | Rosie | `https://jupiterlaser.com/rsvp/?src=regenortho` / `?src=elite` | |

The QR codes are 900px PNGs, made by `_src/event_nov16_qr.py`. Each one was decoded after generating to confirm it opens the right link.

**HotWorx backup:** bring a paper sign-up sheet (name, cell, email, topic) for anyone who won't scan. Janice enters those as "HotWorx."

Phone RSVPs from the website show up in CallRail with `/rsvp/` as the landing page; phone RSVPs from print come in on the print number. Janice adds both to the RSVP list by hand and marks them "phone."

---

## Copy

### Patient blast text (Janice, Mon Nov 2)

Send only to patients who have agreed to receive texts from the office. Everyone else gets the email.

```
Abacoa Podiatry: You're invited to a free evening talk, Mon Nov 16 at 5 PM at our Jupiter office. Achy legs and veins, regenerative medicine, and peptides, explained plainly. Light bites provided. Seating is limited: https://jupiterlaser.com/rsvp/?src=blast1 Reply STOP to opt out.
```

### Patient blast email subject lines

- Free evening talk: tired, achy legs and slow-healing joints (Nov 16)
- You're invited: an evening of plain answers, Monday Nov 16
- Achy legs or joints? Come ask us, free, Nov 16 at 5 PM

### Reminder text and email, Sat Nov 14 ("2 days away")

The office is closed Saturdays, so schedule this on Friday Nov 13.

```
Abacoa Podiatry: See you Monday! Our free talk is Nov 16 at 5 PM, 4601 Military Trail, Suite 202, Jupiter. Light bites at 5, talk at 5:15. Can't make it? Call (561) 915-1934 so we can give your seat away. Reply STOP to opt out.
```

### Morning of Mon Nov 16

```
Abacoa Podiatry: Tonight at 5 PM! Free talk at 4601 Military Trail, Suite 202, Jupiter. Free parking. Reply STOP to opt out.
```

### 3:00 PM, Mon Nov 16

```
Abacoa Podiatry: See you in 2 hours. Doors and light bites at 5:00, talk at 5:15. Suite 202. Reply STOP to opt out.
```

### Thank-you text (Tue Nov 17, attendees)

```
Abacoa Podiatry: Thank you for coming last night! If you'd like to talk about anything from the evening one on one, call us at (561) 915-1934 to book a visit. Reply STOP to opt out.
```

### No-show call script (Nov 17 to 20, Janice)

> "Hi, this is Janice from Abacoa Podiatry. We missed you at Monday's talk and wanted to check in. If you had a question about your legs, joints or anything we covered, we'd be glad to set up a visit with Dr. Cedeño. Is there a day that works?"

---

## Texting

The plan asks for an automatic confirmation text by Friday. That depends on one thing: **is the number that will send texts already registered for business texting (A2P 10DLC)?**

- **If CallRail texting is already set up and registered on your account:** check whether your plan can auto-reply to form submissions, and point it at this form.
- **If not:** registration takes days to weeks, so it won't be ready by Friday, and probably not by Nov 2. Janice texts each new RSVP from the office texting tool the same business day, to anyone who ticked the text box, and sends the blast and reminders the same way.

---

## Reply to Dr. Cedeño (draft, due Thu Oct 29)

> Hi Dr. Cedeño,
>
> The RSVP page is built with the November 16 date: name, cell, email, topic, number of seats, and "how did you hear about this." Each sign-up gets a confirmation email right away, and every RSVP records which link it came from (patient blast, card, flyer, ad, HotWorx, Chamber), so we'll see what worked. It's live at jupiterlaser.com/rsvp, so the QR code works at HotWorx tomorrow. A few questions and conflicts:
>
> 1. **12 seats vs. 25 RSVPs.** If we advertise "limited to 12 seats," we should stop taking RSVPs at 12, but the plan needs 25. If more people show up than expected (15 at a 60% show rate), we'd also be over capacity. I'd suggest "seating is limited" and setting up 15 to 18 chairs. The page says "seating is limited" for now.
> 2. **Confirmation texts by Friday.** Each sign-up now gets an automatic confirmation email. An automatic text needs a number registered for business texting, which takes days to weeks if we don't already have one. Until then, Janice would send confirmation texts by hand, and the Nov 2 blast may need to go mostly by email.
> 3. **Patient texts.** The Nov 2 blast should only be texted to patients who have agreed to receive texts from us. Everyone else gets the email. Janice, can ModMed filter on that?
> 4. **CallRail.** Calls from the page are already tracked. For the printed cards and flyer, I'll set up a separate tracked number today and send it to Rosie.
> 5. **HotWorx tomorrow.** Rosie will have a QR code that goes straight to the sign-up page, plus a paper sheet as backup for anyone who won't scan.
> 6. **Staffing on the 16th.** Office hours end at 5:00 on Mondays, so we need someone at check-in from 4:45, plus Danni for setup and food, through about 6:30.
> 7. **Saturday reminder.** November 14 is a Saturday, so the "2 days away" reminder should be scheduled on Friday the 13th.
> 8. **Location and speakers.** I've put the Jupiter office (4601 Military Trail) on the page. Please confirm. Who presents each segment? Is it you for all three, or is RegenOrtho/Elite presenting regenerative medicine or peptides? The page only names you for the welcome.
> 9. **End time.** Q&A ends at 6:15 and consult booking comes after, so the page says 5:00 to 6:30.
> 10. **Facebook ads.** Meta can take a day or more to approve an ad, so Rosie should submit it by Friday for a Nov 2 start. Age and 10-mile targeting is fine. We should not upload the ModMed patient list to Facebook as an ad audience.
> 11. **Giveaways and wine.** Light food is fine. For Medicare patients, keep giveaways under the OIG's nominal-value limit ($15 per item, $75 per patient per year). For wine, it's worth checking with our insurance first.
>
> No conflicts with my Friday date.
>
> Thanks,
> Nick
