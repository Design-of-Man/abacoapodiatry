# Feb 15 evening talk: RSVP page and promo kit

"Tired, Achy Legs and Slow-Healing Joints." Monday, February 15, 2027, 5:00 PM, Jupiter office.

Landing page: **`/rsvp/`**. Source file: `_src/pages/event-feb-15-talk.html`.

---

## What the page does

- RSVP form: name, cell, email, topic of interest, seats (1 or 2), "how did you hear about this," and an optional text-reminder consent box.
- Submissions go through FormSubmit to the same recipients as the contact form (angela.d@ primary, with Janice, Patricia, both doctors and Nick on CC). It reuses the contact form's exact action URL, so no new FormSubmit activation is needed. Like the contact form, spam is labelled in the email (`verified`, `flags`), never blocked.
- **Confirmation email is automatic.** FormSubmit's `_autoresponse` emails the guest the date, time, address, and "call if you can't make it" as soon as they submit.
- **Confirmation text is not automatic yet.** A static page can't send texts. See "Still open" below.
- Every RSVP records the link it came from (`src` in the email), so each source can be counted even when the guest skips the "how did you hear" question.

## Before Dec 31 (Nick)

- [ ] **CallRail.** The site already runs CallRail's number swap on every page, this one included, so calls from `/rsvp/` are already tracked by source with no change to the page. What still needs a number is **print**: create one static CallRail number for the invite cards and flyer, so phone RSVPs from paper are counted too. Don't hard-code a number into the page.
- [ ] Once Dr. Cedeño approves the title, delete `"robots"` and `"sitemap"` from the page's META block so it can be indexed. It is `noindex` and kept out of the sitemap until then.
- [ ] Rebuild: `python3 _src/build.py`.
- [ ] Submit one test RSVP using your own email. Check that the RSVP email reaches the office inbox and the confirmation reaches you.
- [ ] Decide how the confirmation text gets sent (below).

## Source-tagged links

Give each channel its own link. The tag shows up as `src` in every RSVP email.

| Channel | Owner | Link |
|---|---|---|
| Patient blast #1 (Jan 4) | Janice | `/rsvp/?src=blast1` |
| Patient blast #2 (Jan 18) | Janice | `/rsvp/?src=blast2` |
| Printed invite cards (QR) | Danni / front desk | `/rsvp/?src=card` |
| Flyer (QR) | Rosie | `/rsvp/?src=flyer` |
| Facebook / Instagram paid ad | Rosie | `/rsvp/?src=meta-ad` |
| Facebook / Instagram organic posts | Rosie | `/rsvp/?src=social` |
| Jupiter Chamber | Rosie | `/rsvp/?src=chamber` |
| Wellness Collective | Rosie | `/rsvp/?src=wellness` |
| RegenOrtho / Elite | Rosie | `/rsvp/?src=regenortho` / `?src=elite` |

Phone RSVPs from the website show up in CallRail with `/rsvp/` as the landing page; phone RSVPs from print come in on the print number. Janice adds both to the list by hand and marks them "phone."

**Host:** jupiterlaser.com still serves the old site until the domain cutover. Anything printed before cutover should use `https://abacoapodiatry.vercel.app/rsvp/?src=...`, the same reason the HOTWORX flyer did.

---

## Copy

### Patient blast text (Janice, Jan 4 and Jan 18)

Send only to patients who have agreed to receive texts from the office.

```
Abacoa Podiatry: You're invited to a free evening talk, Mon Feb 15 at 5 PM at our Jupiter office. Achy legs and veins, regenerative medicine, and peptides, explained plainly. Light bites provided. Seating is limited: [link] Reply STOP to opt out.
```

### Patient blast email subject lines

- Free evening talk: tired, achy legs and slow-healing joints (Feb 15)
- You're invited: an evening of plain answers, Monday Feb 15
- Achy legs or joints? Come ask us, free, Feb 15 at 5 PM

### Reminder text, Feb 13 ("2 days away")

```
Abacoa Podiatry: See you Monday! Our free talk is Feb 15 at 5 PM, 4601 Military Trail, Suite 202, Jupiter. Light bites at 5, talk at 5:15. Can't make it? Call (561) 915-1934 so we can give your seat away. Reply STOP to opt out.
```

### Morning of Feb 15

```
Abacoa Podiatry: Tonight at 5 PM! Free talk at 4601 Military Trail, Suite 202, Jupiter. Free parking. Reply STOP to opt out.
```

### 3:00 PM, Feb 15

```
Abacoa Podiatry: See you in 2 hours. Doors and light bites at 5:00, talk at 5:15. Suite 202. Reply STOP to opt out.
```

### Thank-you text (Feb 16, attendees)

```
Abacoa Podiatry: Thank you for coming last night! If you'd like to talk about anything from the evening one on one, call us at (561) 915-1934 to book a visit. Reply STOP to opt out.
```

### No-show call script (Feb 16 to 19, Janice)

> "Hi, this is Janice from Abacoa Podiatry. We missed you at Monday's talk and wanted to check in. If you had a question about your legs, joints or anything we covered, we'd be glad to set up a visit with Dr. Cedeño. Is there a day that works?"

---

## Still open

**Confirmation text.** Options, best first:
1. CallRail: if our plan includes form tracking with an automated text reply, point it at this form and the text goes out on its own from the tracked number. Check the plan.
2. If not, Janice texts each new RSVP from the office texting tool the same business day, to anyone who ticked the text box.

Either way, the number that sends texts must be registered for business texting (A2P 10DLC) before Jan 4. Registration can take a few weeks, so start it in November.

---

## Reply to Dr. Cedeño (draft)

> Hi Dr. Cedeño,
>
> The RSVP page is built and ready for review: name, cell, email, topic, number of seats, and "how did you hear about this." Each sign-up gets a confirmation email automatically, and every RSVP records which link it came from (patient blast, card, ad, Chamber), so we'll be able to see what worked. A few questions and conflicts:
>
> 1. **Title year.** It says "What's New in 2026," but the talk is in February 2027. I've used 2027 on the page. OK?
> 2. **12 seats vs. 25 RSVPs.** If we advertise "limited to 12 seats," we should stop taking RSVPs at 12, but the plan needs 25. If more show up than expected (15 at a 60% show rate), we'd also be over capacity. I'd suggest saying "seating is limited" and setting up 15 to 18 chairs. The page says "seating is limited" for now.
> 3. **Presidents' Day staffing.** Is the office open that Monday? Office hours end at 5:00, so we need someone at check-in from 4:45, plus Danni for setup and food, through about 6:30.
> 4. **Location and speakers.** I assumed the Jupiter office (4601 Military Trail). Please confirm. Who presents each segment? Is it you for all three, or is RegenOrtho/Elite presenting regenerative medicine or peptides? The page only names you for the welcome.
> 5. **End time.** Q&A ends at 6:15 and consult booking comes after, so the page says 5:00 to 6:30.
> 6. **Confirmation text.** The automatic confirmation email is built in. The automatic text needs a texting service on the CallRail number, plus business-text registration, which takes a few weeks. I'll start that in November. Until then, Janice may need to send confirmation texts by hand.
> 7. **Patient texts.** The Jan 4 and Jan 18 blasts should only be texted to patients who have agreed to receive texts from us. Everyone else gets the email. Janice, can ModMed filter on that?
> 8. **Facebook ads.** Age and 10-mile targeting is fine. We should not upload the ModMed patient list to Facebook as an ad audience. There's no Facebook tracking pixel on the RSVP page, and I'll keep it that way.
> 9. **Giveaways and wine.** Light food is fine. For Medicare patients, keep giveaways under the OIG's nominal-value limit ($15 per item, $75 per patient per year). For wine, it's worth checking with our insurance first.
> 10. **Printed cards.** These are due Dec 31. If the jupiterlaser.com switchover hasn't happened by then, the QR codes will point at the temporary address so they don't break.
>
> No conflicts with my December 31 date.
>
> Thanks,
> Nick
