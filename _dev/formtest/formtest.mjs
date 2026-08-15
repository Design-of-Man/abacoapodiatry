// Drives headless Chrome over CDP (Node 22 has WebSocket built in, no deps).
// Run via run-formtest.sh, not directly.
// Fills the real contact form, submits it against each faked FormSubmit reply,
// and reports what the patient would actually see plus whether a lead
// event fired.
const CDP = process.argv[2];

const send = (ws, id, method, params = {}, sessionId) =>
  ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));

function open(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    ws.onopen = () => resolve(ws);
    ws.onerror = reject;
  });
}

const waitFor = (ws, pred) =>
  new Promise((resolve) => {
    const h = (e) => {
      const m = JSON.parse(e.data);
      if (pred(m)) { ws.removeEventListener("message", h); resolve(m); }
    };
    ws.addEventListener("message", h);
  });

const CASES = [
  ["ok",      "stored",                 "expect SUCCESS + conversion"],
  ["dropped", "accepted then dropped",  "expect ERROR + no conversion"],
  ["invalid", "rejected 400",           "expect ERROR + no conversion"],
  ["down",    "database write failed",  "expect ERROR + no conversion"],
];

let id = 0;
let failures = 0;

for (const [kase, label, expectation] of CASES) {
  const tab = await (await fetch(`${CDP}/json/new?about:blank`, { method: "PUT" })).json();
  const ws = await open(tab.webSocketDebuggerUrl);

  send(ws, ++id, "Page.enable");
  await waitFor(ws, (m) => m.id === id);
  send(ws, ++id, "Runtime.enable");
  await waitFor(ws, (m) => m.id === id);

  // Navigate explicitly and wait for load -- /json/new returns before the
  // document exists, which is why every selector came back null.
  const loaded = waitFor(ws, (m) => m.method === "Page.loadEventFired");
  send(ws, ++id, "Page.navigate", { url: `http://127.0.0.1:8767/test/${kase}` });
  await loaded;

  // Capture conversions instead of letting them fly, fill the form, submit,
  // then wait for the handler to settle and report what the visitor sees.
  const script = `
    (async () => {
      // track() emits through Vercel Web Analytics (window.va) and no-ops when
      // the script isn't present -- which it never is on localhost. Stand one
      // up so a conversion has somewhere to land.
      window.__events = [];
      window.va = (...a) => { window.__events.push(a); };

      document.querySelector('#f-name').value  = 'Test Patient';
      document.querySelector('#f-phone').value = '5615550123';
      document.querySelector('#f-email').value = 'test@example.com';
      document.querySelector('#contact-form').dispatchEvent(
        new Event('submit', { bubbles: true, cancelable: true })
      );

      const s = document.querySelector('#form-status');
      for (let i = 0; i < 60 && !s.textContent.trim(); i++) {
        await new Promise(r => setTimeout(r, 50));
      }
      const fired = JSON.stringify(window.__events).includes('form_submit');
      return JSON.stringify({
        action: document.querySelector('#contact-form').getAttribute('action'),
        cls: s.className, text: s.textContent.trim().slice(0, 60), fired,
        btn: document.querySelector('#contact-form button[type=submit]').textContent.trim(),
      });
    })()
  `;
  send(ws, ++id, "Runtime.evaluate", { expression: script, awaitPromise: true, returnByValue: true });
  const res = await waitFor(ws, (m) => m.id === id);
  if (res.result?.exceptionDetails) {
    console.log("  page threw:", JSON.stringify(res.result.exceptionDetails).slice(0, 400));
    failures++;
    ws.close();
    continue;
  }
  const raw = res.result?.result?.value;
  if (typeof raw !== "string") {
    console.log("  unexpected CDP shape:", JSON.stringify(res).slice(0, 400));
    failures++;
    ws.close();
    continue;
  }
  const r = JSON.parse(raw);

  const isOk = r.cls.includes("ok");
  const pass = kase === "ok" ? (isOk && r.fired) : (!isOk && !r.fired);
  if (!pass) failures++;

  console.log(`  ${pass ? "PASS" : "FAIL"}  ${kase.padEnd(8)} (${label})`);
  console.log(`         ${expectation}`);
  console.log(`         shown: ${isOk ? "SUCCESS" : "ERROR"} — "${r.text}…"`);
  console.log(`         lead event fired: ${r.fired}   button reset: ${r.btn}`);
  console.log();
  ws.close();
}

console.log(failures ? `  ${failures} case(s) FAILED`
                     : `  all ${CASES.length} cases behave correctly`);
process.exit(failures ? 1 : 0);
