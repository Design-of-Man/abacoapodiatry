/**
 * Appointment request handler for the /contact/ form.
 *
 * Replaces FormSubmit, which never delivered a single lead. FormSubmit requires
 * a one-time activation link to be clicked in the recipient's inbox before it
 * forwards anything; until that click it answers 200 with {"success":"false"}
 * and drops the submission. Nobody ever clicked it, so the site had no working
 * lead path at all -- and the failure was invisible from the outside.
 *
 * The rule this file exists to enforce: NEVER report success for a lead that
 * was not stored. Supabase is written first and its result decides the
 * response. Email is sent afterwards and cannot affect it, because an inbox
 * being down is not a reason to tell a patient in pain that their request
 * vanished -- the row is already safe and the office can work from the table.
 *
 * Deliberately zero dependencies and CommonJS. This project has no
 * package.json, no build command and framework: null on Vercel; the whole
 * safety model is "serve the committed root statically". Adding a dependency
 * would introduce an install step to the deploy. Node 24 has global fetch, so
 * PostgREST and Resend are both reachable over plain HTTP.
 *
 * Capture goes through a Supabase Edge Function (contact-lead) rather than
 * straight to PostgREST, and that is on purpose. Edge Functions get
 * SUPABASE_SERVICE_ROLE_KEY injected automatically, so the one true secret
 * never leaves Supabase and nobody has to paste it into a hosting dashboard
 * before the form starts working. This site's whole outage was caused by a lead
 * path that waited on a human action; it should not ship with a new one.
 *
 * The publishable key below is committed deliberately. Supabase publishable
 * keys are designed to be public and normally ship inside browser bundles, and
 * the leads table has RLS enabled with zero policies, so this key can do
 * nothing at all against it directly. Every write goes through the function.
 *
 * Environment (all OPTIONAL -- capture works with none of them set):
 *   SUPABASE_FN_URL   override the Edge Function URL
 *   SUPABASE_ANON_KEY override the publishable key
 *   RESEND_API_KEY    enable email notification
 *   LEAD_TO           comma-separated office recipients
 *   LEAD_FROM         verified Resend sender
 */

"use strict";

// Bound what a single request can write. The columns are text, so without
// these one POST could push an arbitrarily large row.
const LIMITS = {
  name: 200,
  phone: 50,
  email: 200,
  reason: 120,
  message: 4000,
};

const TIMEOUT_MS = 8000;

// Which UI submitted the lead. Allowlisted so a stray/garbage value can't
// pollute the Supabase column -- anything not on the list quietly becomes the
// historical default so old callers (and anyone omitting the field) keep
// working exactly as before.
const SOURCES = ["contact-form", "assistant"];

// Supabase project "Design of Man". See the header comment on why the
// publishable key is committed rather than held in an environment variable.
const FN_URL = process.env.SUPABASE_FN_URL ||
  "https://iiabylugbnmcdzqjenus.supabase.co/functions/v1/contact-lead";
const ANON_KEY = process.env.SUPABASE_ANON_KEY ||
  "sb_publishable_i5weJFCr68SAOsBaErXaFw_A3HrshPP";

function clean(value, max) {
  if (typeof value !== "string") return "";
  return value.trim().slice(0, max);
}

function json(res, status, body) {
  res.status(status).setHeader("Content-Type", "application/json");
  res.send(JSON.stringify(body));
}

// The browser handler in assets/js/main.js treats the STRING "true" as the
// only success signal, matching the shape FormSubmit used. Keeping that
// contract means the success/failure logic there did not have to change, and
// anything unexpected still routes the patient to the phone number.
const OK = { success: "true" };
const NOT_OK = { success: "false" };

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return json(res, 405, NOT_OK);
  }

  // Vercel's Node runtime parses application/json into req.body. main.js sends
  // JSON for exactly this reason -- it does not parse multipart.
  const body = req.body && typeof req.body === "object" ? req.body : {};

  // Honeypot. A bot that fills the hidden _honey field gets a cheerful 200 and
  // nothing is stored: a visible rejection just tells it to try again.
  if (clean(body._honey, 100)) return json(res, 200, OK);

  const lead = {
    name: clean(body.name, LIMITS.name),
    phone: clean(body.phone, LIMITS.phone),
    email: clean(body.email, LIMITS.email) || null,
    reason: clean(body.reason, LIMITS.reason) || null,
    message: clean(body.message, LIMITS.message) || null,
  };

  if (!lead.name || !lead.phone) {
    return json(res, 400, NOT_OK);
  }

  const source = SOURCES.includes(body.source) ? body.source : "contact-form";

  const forwarded = req.headers["x-forwarded-for"];
  const row = {
    ...lead,
    site: "jupiterlaser.com",
    source: source,
    user_agent: clean(req.headers["user-agent"], 500) || null,
    ip: (typeof forwarded === "string" ? forwarded.split(",")[0].trim() : "") || null,
  };

  // --- Durable capture. This decides the response. ---
  try {
    const r = await fetch(FN_URL, {
      method: "POST",
      headers: {
        apikey: ANON_KEY,
        Authorization: `Bearer ${ANON_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(row),
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    const stored = r.ok &&
      await r.json().then((d) => String(d && d.success) === "true").catch(() => false);
    if (!stored) {
      console.error("contact: capture failed", r.status);
      return json(res, 502, NOT_OK);
    }
  } catch (err) {
    console.error("contact: capture threw", err && err.message);
    return json(res, 502, NOT_OK);
  }

  // --- Notification. Best effort, and never allowed to fail the request. ---
  // The lead is already stored by this point. If RESEND_API_KEY is not
  // configured yet this is skipped entirely and the form still works -- switch
  // email on later by adding the variable and redeploying. While it is off,
  // someone has to read the Supabase table.
  if (process.env.RESEND_API_KEY && process.env.LEAD_TO && process.env.LEAD_FROM) {
    try {
      const lines = [
        `Name:    ${lead.name}`,
        `Phone:   ${lead.phone}`,
        `Email:   ${lead.email || "(not given)"}`,
        `Reason:  ${lead.reason || "(not given)"}`,
        "",
        lead.message || "(no additional message)",
        "",
        "-- Submitted from the appointment form on jupiterlaser.com.",
      ];
      const payload = {
        from: process.env.LEAD_FROM,
        to: process.env.LEAD_TO.split(",").map((a) => a.trim()).filter(Boolean),
        subject: `New appointment request — ${lead.name}`,
        text: lines.join("\n"),
      };
      // Lets the office hit reply and reach the patient directly.
      if (lead.email) payload.reply_to = lead.email;

      const mail = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
      if (!mail.ok) {
        console.error("contact: resend failed", mail.status, await mail.text());
      } else {
        console.log("contact: lead stored and notification sent");
      }
    } catch (err) {
      console.error("contact: resend threw", err && err.message);
    }
  } else {
    // Say so out loud. Skipping notification is a supported state -- capture
    // still works and the office can read the table -- but it is indistinguishable
    // from a working one in the logs, because a block that never runs logs
    // nothing. That silence is exactly how this site went months with a lead
    // path nobody was being told about: the patient saw the success message, the
    // row was written, and the only missing piece left no trace anywhere.
    const missing = ["RESEND_API_KEY", "LEAD_TO", "LEAD_FROM"]
      .filter((k) => !process.env[k]);
    console.warn(
      "contact: lead stored but NO email sent -- unset: " + missing.join(", ") +
      ". Someone must be reading the Supabase leads table."
    );
  }

  return json(res, 200, OK);
};
