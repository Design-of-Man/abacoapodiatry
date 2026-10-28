/**
 * Guest confirmation email for the Nov 16 evening talk RSVP form (/rsvp/).
 *
 * The office copy of every RSVP still comes from FormSubmit, exactly as it
 * did before -- the office is used to those emails and nothing about them
 * changed. This endpoint does one thing on top: email the GUEST a
 * confirmation, from events@jupiterlaser.com, through Resend.
 *
 * Why not FormSubmit's own _autoresponse: tested live on 2026-10-28. It does
 * not work for AJAX forms (FormSubmit's docs say so), and on the standard
 * endpoint it needed a fresh per-website activation, held submissions behind
 * a captcha for 30+ seconds, and still never delivered a confirmation.
 *
 * main.js calls this only AFTER FormSubmit has confirmed the office copy
 * (success:"true"), so a guest is never told they are registered for an RSVP
 * the office never received. If this call fails, the page falls back to
 * "our team will confirm by text or phone" -- the RSVP itself is unaffected.
 *
 * The message is fixed text: the only guest-supplied values used are the
 * first name in the greeting (escaped, links rejected) and the recipient
 * address. That keeps this from being useful as a relay for anyone else's
 * content.
 *
 * Zero dependencies and CommonJS, same as api/contact.js and for the same
 * reason: the site deploys with no install step.
 *
 * Environment:
 *   RESEND_API_KEY  required. Without it this answers 503 and the page shows
 *                   the text-or-phone fallback.
 *   RSVP_FROM       optional sender, default events@jupiterlaser.com
 *   RSVP_REPLY_TO   optional reply-to, default angela.d@jupiterlaser.com
 */

"use strict";

const TIMEOUT_MS = 8000;
const FROM = process.env.RSVP_FROM ||
  "Abacoa Podiatry & Leg Vein Center <events@jupiterlaser.com>";
const REPLY_TO = process.env.RSVP_REPLY_TO || "angela.d@jupiterlaser.com";
const OK = { success: "true" };
const NOT_OK = { success: "false" };

function json(res, status, body) {
  res.status(status).setHeader("Content-Type", "application/json");
  res.send(JSON.stringify(body));
}

function esc(s) {
  return s.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

// 5:00-6:30 PM EST on Mon Nov 16, 2026 = 22:00-23:30 UTC.
const ICS = [
  "BEGIN:VCALENDAR",
  "VERSION:2.0",
  "PRODID:-//Abacoa Podiatry & Leg Vein Center//Evening Talk//EN",
  "METHOD:PUBLISH",
  "BEGIN:VEVENT",
  "UID:nov-16-2026-evening-talk@jupiterlaser.com",
  "DTSTAMP:20261028T000000Z",
  "DTSTART:20261116T220000Z",
  "DTEND:20261116T233000Z",
  "SUMMARY:Free evening talk: Tired\\, Achy Legs and Slow-Healing Joints",
  "LOCATION:Abacoa Podiatry & Leg Vein Center\\, 4601 Military Trail\\, Suite 202\\, Jupiter\\, FL 33458",
  "DESCRIPTION:Arrive at 5:00 PM for check-in and light bites. The talk starts at 5:15. Can't make it? Call (561) 915-1934.",
  "URL:https://jupiterlaser.com/rsvp/",
  "END:VEVENT",
  "END:VCALENDAR",
  "",
].join("\r\n");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return json(res, 405, NOT_OK);
  }
  if (!process.env.RESEND_API_KEY) {
    console.warn("rsvp-confirm: RESEND_API_KEY not set -- no confirmation sent");
    return json(res, 503, NOT_OK);
  }

  const body = req.body && typeof req.body === "object" ? req.body : {};
  // Honeypot: pretend success, send nothing.
  if (typeof body._honey === "string" && body._honey.trim()) return json(res, 200, OK);

  const email = typeof body.email === "string" ? body.email.trim().slice(0, 200) : "";
  const fullName = typeof body.name === "string" ? body.name.trim().slice(0, 200) : "";
  if (!/^[^\s@<>]+@[^\s@<>]+\.[a-z]{2,}$/i.test(email) || !fullName ||
      /https?:\/\/|www\.|[<>]/i.test(fullName)) {
    return json(res, 400, NOT_OK);
  }
  const first = fullName.split(/\s+/)[0];
  const plusOne = body.seats === "Me plus one guest";
  const seatLine = plusOne ? "We've saved two seats: one for you and one for your guest." :
    "We've saved your seat.";

  const text = [
    `Hi ${first},`,
    "",
    `You're on the list for our free evening talk, "Tired, Achy Legs and Slow-Healing Joints: What's New in 2026." ${seatLine}`,
    "",
    "When: Monday, November 16, 2026. Doors and light bites at 5:00 PM, the talk starts at 5:15.",
    "Where: Abacoa Podiatry & Leg Vein Center, 4601 Military Trail, Suite 202, Jupiter, FL 33458. Free parking on site.",
    "",
    "A calendar invite is attached. Bring your questions.",
    "",
    "Can't make it after all? Call us at (561) 915-1934 so we can offer your seat to someone else.",
    "",
    "See you there,",
    "Abacoa Podiatry & Leg Vein Center",
    "https://jupiterlaser.com/rsvp/",
  ].join("\n");

  const html = `<!doctype html><html><body style="margin:0;background:#f4f1ea;font-family:Arial,Helvetica,sans-serif;color:#1d1a14">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:12px;overflow:hidden">
<tr><td style="background:#000;padding:28px 28px 22px">
<div style="font-size:12px;letter-spacing:3px;text-transform:uppercase;color:#e96e32;font-weight:bold">You're on the list</div>
<div style="font-family:Georgia,serif;font-size:30px;line-height:1.15;color:#ffffff;font-weight:bold;margin-top:10px">Seat saved.<br><span style="color:#f3c35e">See you Monday.</span></div>
</td></tr>
<tr><td style="background:linear-gradient(90deg,#c63d2a,#e96e32,#f3c35e);background-color:#e96e32;padding:16px 28px;color:#2a1006">
<div style="font-size:20px;font-weight:bold;color:#ffffff">MONDAY, NOV 16 &middot; 5:00 PM</div>
<div style="font-size:12px;font-weight:bold;letter-spacing:0.5px;text-transform:uppercase;margin-top:4px">Abacoa Podiatry &middot; 4601 Military Trail, Suite 202, Jupiter</div>
</td></tr>
<tr><td style="padding:26px 28px;font-size:16px;line-height:1.55">
<p style="margin:0 0 14px">Hi ${esc(first)},</p>
<p style="margin:0 0 14px">You're on the list for our free evening talk, <strong>&ldquo;Tired, Achy Legs and Slow-Healing Joints: What's New in 2026.&rdquo;</strong> ${esc(seatLine)}</p>
<p style="margin:0 0 14px"><strong>Doors and light bites at 5:00 PM.</strong> The talk starts at 5:15: leg veins, regenerative medicine and peptides, then your questions. Free parking on site.</p>
<p style="margin:0 0 14px">A calendar invite is attached.</p>
<p style="margin:0 0 14px">Can't make it after all? Call <a href="tel:+15619151934" style="color:#c63d2a">(561) 915-1934</a> so we can offer your seat to someone else.</p>
<p style="margin:0">See you there,<br>Abacoa Podiatry &amp; Leg Vein Center</p>
</td></tr></table>
<div style="font-size:12px;color:#8a8170;margin-top:14px">You're receiving this because you RSVP'd at jupiterlaser.com/rsvp.</div>
</td></tr></table></body></html>`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: FROM,
        to: [email],
        reply_to: REPLY_TO,
        subject: "You're registered: free evening talk, Mon Nov 16 at 5 PM",
        text,
        html,
        attachments: [{
          filename: "evening-talk-nov-16.ics",
          content: Buffer.from(ICS).toString("base64"),
          content_type: "text/calendar",
        }],
      }),
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!r.ok) {
      console.error("rsvp-confirm: resend failed", r.status, await r.text());
      return json(res, 502, NOT_OK);
    }
    console.log("rsvp-confirm: confirmation sent");
    return json(res, 200, OK);
  } catch (err) {
    console.error("rsvp-confirm: resend threw", err && err.message);
    return json(res, 502, NOT_OK);
  }
};
