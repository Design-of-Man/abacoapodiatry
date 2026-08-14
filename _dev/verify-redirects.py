#!/usr/bin/env python3
"""Prove every old URL resolves on a deployed build, not just in vercel.json.

    python3 _dev/verify-redirects.py                      # against production
    python3 _dev/verify-redirects.py https://<preview>    # against a preview

Reads _dev/old-site-urls.tsv (from _dev/crawl-old-site.py), requests every path
against a live deployment in the trailing-slash form WordPress publishes, and
follows the chain to its end. Fails on anything that does not finish at HTTP 200.

Why this exists rather than trusting the config. Checking vercel.json is not the
same as checking the deployment, and the difference was not academic here:
vercel.json sets "trailingSlash": true, so Vercel 308s /foo to /foo/ before it
matches the redirect table. Every source was written slash-less, so the entire
array was inert -- /veins/ and /venous-insufficiency/ returned a hard 404 in
production while looking perfectly correct in the file. The only legacy URLs
that resolved did so through a meta-refresh stub, which is why spot-checking by
hand missed it: the paths a person thinks to try are the ones with a stub.

A redirect you have not requested over the wire is a redirect you have not
tested. Run this against the preview before cutover, and against production
after.
"""
import concurrent.futures as cf
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "_dev" / "old-site-urls.tsv"
DEFAULT_ORIGIN = "https://abacoapodiatry.vercel.app"
UA = {"User-Agent": "Mozilla/5.0 (compatible; redirect-audit)"}
MAX_HOPS = 5


class Tracer(urllib.request.HTTPRedirectHandler):
    """Record each hop so a chain that is too long can be reported, not just followed."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        req.redirect_hops = getattr(req, "redirect_hops", []) + [(code, newurl)]
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None:
            new.redirect_hops = req.redirect_hops
        return new


def check(origin: str, path: str, attempts: int = 3) -> dict:
    """Request one old URL and follow it to the end.

    Retries connection-level failures only. A 404 is an answer and is reported
    immediately; a TLS handshake timeout is not an answer, and 156 concurrent
    requests to one host produce a few of those. Retrying an HTTP status would
    just hide a real break, so the two cases are kept apart deliberately.
    """
    url = origin + path + "/"
    last = None
    for attempt in range(attempts):
        opener = urllib.request.build_opener(Tracer)
        req = urllib.request.Request(url, headers=UA, method="GET")
        try:
            with opener.open(req, timeout=40) as r:
                return {"path": path, "status": r.status, "final": r.url,
                        "hops": getattr(req, "redirect_hops", [])}
        except urllib.error.HTTPError as e:
            return {"path": path, "status": e.code, "final": url,
                    "hops": getattr(req, "redirect_hops", [])}
        except Exception as exc:
            last = str(exc)
            if attempt < attempts - 1:
                time.sleep(1.5 * (attempt + 1))
    return {"path": path, "status": 0, "final": url, "hops": [], "error": last}


def main() -> None:
    origin = (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGIN).rstrip("/")
    if not INVENTORY.exists():
        sys.exit(f"{INVENTORY.relative_to(ROOT)} missing -- run _dev/crawl-old-site.py")
    paths = [l.split("\t")[0] for l in INVENTORY.read_text().splitlines()[1:] if l.strip()]
    paths = [p for p in paths if p != "/"]

    print(f"verify-redirects: {len(paths)} old URL(s) against {origin}\n")
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda p: check(origin, p), paths))

    broken = [r for r in results if r["status"] != 200]
    longchain = [r for r in results if r["status"] == 200 and len(r["hops"]) > 2]

    for r in broken:
        print(f"  BROKEN  {r['status'] or 'conn'}  {r['path']}")
        if r.get("error"):
            print(f"            {r['error']}")
    for r in longchain:
        print(f"  CHAIN   {len(r['hops'])} hops  {r['path']}")

    ok = len(results) - len(broken)
    print(f"\n  {ok}/{len(results)} resolve to 200"
          + (f", {len(longchain)} with more than 2 hops" if longchain else ""))
    if broken:
        print(f"  FAIL -- {len(broken)} old URL(s) do not resolve. These 404 at cutover.")
        sys.exit(1)
    print("  OK -- every URL the old site publishes lands on a real page")


if __name__ == "__main__":
    main()
