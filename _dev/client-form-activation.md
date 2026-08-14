# For the practice — switching on the appointment form

Forward the section below to whoever reads **`doctor.cedeno@jupiterlaser.com`**. That is
the address the confirmation email goes to, and only that address can complete this. It's
written to be read by someone who does not work in tech, so please don't add jargon to it.

**Why it matters:** the service that emails the form submissions will not send anything at
all until someone clicks a confirmation link once. Until that click, the website says
"thank you" to the patient and the request goes nowhere. Nobody gets an error. That is the
whole reason this note exists.

**Note on who receives what.** Every appointment request goes to all four addresses:
`doctor.cedeno@jupiterlaser.com` plus `janice.j@`, `angela.d@` and
`AbacoaPodiatry@gmail.com` as copies. Only the first one needs to be confirmed — the
copies need nothing. The subject line will read **Appointment Request**.

---

## Copy from here

Hi — quick one-time step to switch on the appointment form on the new website.

The form emails every request straight to the office, but the service that sends those
emails needs the address confirmed once before it will deliver anything. Until that
happens, requests submitted on the site won't reach anyone.

**What to do**

1. Look in the **`doctor.cedeno@jupiterlaser.com`** inbox for an email from
   **FormSubmit**. The subject line mentions confirming or activating your form.
   **Check the spam and junk folders too** — it very often lands in one of them.
2. Open it and click the confirmation link inside.
3. After you click, a page will load showing a short random code (it looks something like
   `a1b2c3d4e5f6`). **Please copy that code and send it back to us.** It lets us take the
   email address off the public web page, so spam bots can't scrape it.

**If you can't find the email:** tell us and we'll submit a test request from the website,
which makes the service send it again straight away.

**Once you've clicked**, we'll send one test request through the form so you can confirm a
real one arrives. Janice, Angela and the Gmail account should each get a copy as well.
Watch for it and let us know either way — if it doesn't show up we'd much rather find out
now than after the new site goes live.

Thanks — this is the last thing standing between the new site and taking bookings.

## Copy to here

---

## After they've clicked

1. Get the alias code and swap the form's `action` in `_src/pages/contact.html` from
   `https://formsubmit.co/ajax/doctor.cedeno@jupiterlaser.com` to
   `https://formsubmit.co/ajax/<alias>`. Rebuild and commit. This is worth doing: it is
   the only way to stop the address being harvested from the page source.
2. Submit a real request on the live site and confirm it lands in **every** inbox, spam
   included. CC delivery not reaching everyone is the common surprise here.
3. Confirm exactly one `form_submit` event in Vercel Web Analytics — which needs Web
   Analytics switched on first, or there will be nothing to see.

Step 2 is the one people skip, and it's the one that costs money when it's wrong.

## Two things that are not bugs

**Patients do not get an automatic acknowledgement email.** FormSubmit's `_autoresponse`
does not work on forms submitted through AJAX, which this one is, so the field was removed
rather than left sitting there looking functional. Patients see the confirmation on the
page and are told the office will call. If an emailed receipt is ever wanted, it needs a
different sending path, not that field.

**Changing the address in the form restarts activation.** The confirmation is tied to the
address in the form's `action`. Swapping it — including swapping it for the alias in step
1 — means confirming again. Do step 1 and step 2 in that order and only once.
