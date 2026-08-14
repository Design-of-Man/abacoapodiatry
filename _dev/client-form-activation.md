# For the practice — switching on the appointment form

Forward the section below to whoever reads `AbacoaPodiatry@gmail.com`. It's written to be
read by someone who does not work in tech, so please don't add jargon to it.

**Why it matters:** the service that emails the form submissions will not send anything at
all until someone clicks a confirmation link once. Until that click, the website says
"thank you" to the patient and the request goes nowhere. Nobody gets an error. That is the
whole reason this note exists.

---

## Copy from here

Hi — quick one-time step to switch on the appointment form on the new website.

The form emails every request straight to your inbox, but the service that sends those
emails needs you to confirm your address once before it will deliver anything. Until that
happens, requests submitted on the site won't reach you.

**What to do**

1. Look in the `AbacoaPodiatry@gmail.com` inbox for an email from **FormSubmit**. The
   subject line mentions confirming or activating your form. **Check the spam and
   Promotions folders too** — it very often lands in one of them.
2. Open it and click the confirmation link inside.
3. After you click, a page will load showing a short random code (it looks something like
   `a1b2c3d4e5f6`). **Please copy that code and send it back to us.** It lets us take your
   email address off the public web page, so spam bots can't scrape it.

**If you can't find the email:** tell us and we'll submit a test request from the website,
which makes the service send it again straight away.

**Once you've clicked**, we'll send one test request through the form so you can confirm a
real one arrives. Watch for it and let us know either way — if it doesn't show up we'd
much rather find out now than after the new site goes live.

One last thing: if you'd like these requests to reach more than one person, send us the
other email addresses and we'll add them.

Thanks — this is the last thing standing between the new site and taking bookings.

## Copy to here

---

## After they've clicked

1. Get the alias code and swap the form's `action` in `_src/pages/contact.html` from
   `https://formsubmit.co/ajax/AbacoaPodiatry@gmail.com` to
   `https://formsubmit.co/ajax/<alias>`. Rebuild and commit.
2. Add the three additional recipients as a `_cc` hidden field (comma-separated).
3. Submit a real request on the live site and confirm it lands in **every** inbox,
   spam included. CC delivery not reaching everyone is the common surprise here.
4. Confirm exactly one `form_submit` event in Vercel Web Analytics.

Step 3 is the one people skip, and it's the one that costs money when it's wrong.
