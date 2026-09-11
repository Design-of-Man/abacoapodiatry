// Runs axe-core against a list of pages by injecting the library over CDP.
//
// @axe-core/cli would be the obvious tool, but it pulls chromedriver, whose
// postinstall downloads a binary from googlechromelabs.github.io -- blocked by
// this environment's egress policy. axe-core itself is pure JS with no binary,
// so inject it into a page we drive ourselves. Node 22 has WebSocket built in.
import { readFileSync } from "node:fs";

const [CDP, BASE, AXE_PATH, ...PAGES] = process.argv.slice(2);
const AXE = readFileSync(AXE_PATH, "utf8");

const send = (ws, id, method, params = {}) =>
  ws.send(JSON.stringify({ id, method, params }));

const open = (url) =>
  new Promise((res, rej) => {
    const ws = new WebSocket(url);
    ws.onopen = () => res(ws);
    ws.onerror = rej;
  });

const waitFor = (ws, pred) =>
  new Promise((res) => {
    const h = (e) => {
      const m = JSON.parse(e.data);
      if (pred(m)) { ws.removeEventListener("message", h); res(m); }
    };
    ws.addEventListener("message", h);
  });

let id = 0;
let total = 0;
const rows = [];

for (const page of PAGES) {
  const tab = await (await fetch(`${CDP}/json/new?about:blank`, { method: "PUT" })).json();
  const ws = await open(tab.webSocketDebuggerUrl);
  send(ws, ++id, "Page.enable"); await waitFor(ws, (m) => m.id === id);
  send(ws, ++id, "Runtime.enable"); await waitFor(ws, (m) => m.id === id);

  const loaded = waitFor(ws, (m) => m.method === "Page.loadEventFired");
  send(ws, ++id, "Page.navigate", { url: BASE + page });
  await loaded;

  send(ws, ++id, "Runtime.evaluate", { expression: AXE, returnByValue: false });
  await waitFor(ws, (m) => m.id === id);

  send(ws, ++id, "Runtime.evaluate", {
    // Default rule set; report only what axe is confident about.
    expression: `axe.run(document, { resultTypes: ['violations'] })
      .then(r => JSON.stringify(r.violations.map(v => ({
        id: v.id, impact: v.impact, n: v.nodes.length, help: v.help
      }))))`,
    awaitPromise: true,
    returnByValue: true,
  });
  const res = await waitFor(ws, (m) => m.id === id);

  if (res.result?.exceptionDetails) {
    console.log(`  ${page.padEnd(34)} axe FAILED to run`);
    ws.close();
    continue;
  }
  const violations = JSON.parse(res.result.result.value);
  const n = violations.reduce((s, v) => s + v.n, 0);
  total += n;
  rows.push([page, n, violations]);
  ws.close();
}

for (const [page, n, violations] of rows) {
  console.log(`  ${page.padEnd(34)} ${String(n).padStart(3)} violation node(s)`);
  for (const v of violations) {
    console.log(`      ${(v.impact || "?").padEnd(8)} ${v.id} (${v.n}) — ${v.help}`);
  }
}
console.log(`\n  axe total: ${total} violation node(s) across ${rows.length} pages`);
