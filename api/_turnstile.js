// Shared helper, not a Vercel function (files starting "_" in api/ are not
// routed, same as api/_email.js). Used by api/contact.js and api/rsvp-confirm.js.
// The block between the markers is copied verbatim from the shared Design of
// Man Turnstile block; only the export line below it is local.

"use strict";

// ---- shared Turnstile block (start) ----
// Cloudflare Turnstile, shared by every Design of Man client site (keep this
// block identical across abacoapodiatry, elite, regenortho, firstrehabnpb and
// legacymed; adapt only the require/export style to the file it lives in).
//
// ON only when BOTH TURNSTILE_SITE_KEY and TURNSTILE_SECRET_KEY are set, so a
// half-configured environment can never mark every real lead unverified.
// The browser sends the token as `_turnstile` (leading underscore: a control
// field, never printed in an email).
//
// Verification outcome is three-way:
//   "off"        keys unset: behave exactly as before Turnstile existed
//   "verified"   Cloudflare said success, OR Cloudflare could not be reached
//                (fail open: their outage must not demote real patients)
//   "unverified" token missing or rejected. The lead is still KEPT wherever this
//                site stores leads, and still emailed, but only to the
//                monitoring inbox (TURNSTILE_UNVERIFIED_TO, else LEAD_CC), with
//                "[Unverified] " on the subject, and the visitor gets NO
//                confirmation email. That confirmation to scraped addresses is
//                what drew spam complaints on the shared Resend account.
//                If neither monitoring variable is set, it goes to the normal
//                recipients with the prefix: a lead is never silently lost.

const TURNSTILE_VERIFY = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

function turnstileOn() {
  return Boolean(process.env.TURNSTILE_SITE_KEY && process.env.TURNSTILE_SECRET_KEY);
}

// What GET on the lead endpoint returns, so the browser can find the site key.
function turnstileConfig() {
  return { siteKey: turnstileOn() ? process.env.TURNSTILE_SITE_KEY : "" };
}

async function turnstileCheck(req, body) {
  if (!turnstileOn()) return "off";
  const token = body && typeof body._turnstile === "string" ? body._turnstile.trim() : "";
  if (!token || token.length > 2048) return "unverified";
  const params = new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY, response: token });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim();
  if (ip) params.set("remoteip", ip);
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 5000);
  try {
    const r = await fetch(TURNSTILE_VERIFY, { method: "POST", body: params, signal: ctrl.signal });
    const j = await r.json();
    if (j && j.success === true) return "verified";
    console.warn("turnstile: rejected", (j && j["error-codes"] || []).join(","));
    return "unverified";
  } catch (e) {
    console.warn("turnstile: siteverify unreachable, failing open:", e.message);
    return "verified";
  } finally {
    clearTimeout(timer);
  }
}

// Recipients for an unverified lead: the monitoring inbox, or null meaning
// "use the normal recipients" (subject still gets the prefix).
function unverifiedRecipients() {
  const raw = process.env.TURNSTILE_UNVERIFIED_TO || process.env.LEAD_CC || "";
  const list = raw.split(",").map((s) => s.trim()).filter(Boolean);
  return list.length ? list : null;
}
// ---- shared Turnstile block (end) ----

module.exports = { turnstileOn, turnstileConfig, turnstileCheck, unverifiedRecipients };
