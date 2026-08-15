#!/usr/bin/env python3
"""Serves the real built site, plus a fake /api/contact that can be told how to lie.

Proves what the PATIENT sees for each backend outcome, and whether a lead
conversion fires. It does not prove api/contact.js itself -- that needs a real
request against a deployment.

/test/<case>  -> the real contact page with its form action pointed at /mock/<case>
/mock/ok      -> 200 {"success":"true"}   stored, and reported as stored
/mock/dropped -> 200 {"success":"false"}  accepted but NOT stored: the silent failure
/mock/invalid -> 400 {"success":"false"}  rejected: name or phone missing
/mock/down    -> 502 {"success":"false"}  database write failed
"""
import json
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = "/home/user/abacoapodiatry"
CASES = {
    "ok":      (200, {"success": "true"}),
    "dropped": (200, {"success": "false"}),
    "invalid": (400, {"success": "false"}),
    "down":    (502, {"success": "false"}),
}


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass

    def do_GET(self):
        m = re.match(r"^/test/(\w+)$", self.path)
        if not m:
            return super().do_GET()
        with open(f"{ROOT}/contact/index.html", encoding="utf-8") as f:
            html = f.read()
        html = re.sub(r'action="/api/contact/"',
                      f'action="/mock/{m.group(1)}"', html)
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        m = re.match(r"^/mock/(\w+)$", self.path)
        code, payload = CASES.get(m.group(1) if m else "", (404, {"error": "no case"}))
        self.rfile.read(int(self.headers.get("Content-Length", 0) or 0))
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


ThreadingHTTPServer(("127.0.0.1", 8767), H).serve_forever()
