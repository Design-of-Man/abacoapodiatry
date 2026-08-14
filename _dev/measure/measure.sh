#!/usr/bin/env bash
# Lighthouse (mobile) + axe across representative pages, against the built site.
#
#   bash _dev/measure/measure.sh baseline     # before changes
#   bash _dev/measure/measure.sh after        # after changes, then diff.sh
#
# Results land in _dev/measure/results/<label>/. Run the identical command both
# times or the delta means nothing.
#
# Known limitation: Google Fonts is blocked by this environment's egress policy,
# so local runs do not reflect production font loading and font-related LCP will
# read better here than in reality. Everything else is genuine.
set -u
LABEL="${1:-baseline}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
OUT="$HERE/results/$LABEL"
PORT=8770
CDP_PORT=9223
BASE="http://127.0.0.1:$PORT"

export NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost
export CHROME_PATH="${CHROME_PATH:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"

# Representative rather than exhaustive: the money page, a condition page and a
# service page (the two templates that carry the long tail), the conversion
# page, and the one page still carrying placeholder content.
PAGES=(/ /conditions/plantar-fasciitis/ /services/mls-laser-therapy/ /contact/ /reviews/)

cleanup() {
  [ -n "${SRV:-}" ] && kill "$SRV" 2>/dev/null
  [ -n "${CHR:-}" ] && kill "$CHR" 2>/dev/null
  return 0
}
trap cleanup EXIT

[ -d "$HERE/node_modules/lighthouse" ] || {
  echo "deps missing. run:  cd _dev/measure && npm install --ignore-scripts lighthouse axe-core"
  echo "(--ignore-scripts matters: chromedriver's postinstall fetches a blocked host)"
  exit 1; }

mkdir -p "$OUT"
cd "$ROOT"
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SRV=$!
curl --retry 20 --retry-connrefused --retry-delay 1 -sf "$BASE/" >/dev/null || {
  echo "local server never came up"; exit 1; }

echo "=== Lighthouse (mobile preset, throttled) ==="
for p in "${PAGES[@]}"; do
  slug=$(echo "$p" | sed 's|^/||; s|/$||; s|/|_|g'); slug=${slug:-home}
  "$HERE/node_modules/.bin/lighthouse" "$BASE$p" \
    --only-categories=performance,accessibility,seo,best-practices \
    --quiet --output=json --output-path="$OUT/$slug.json" \
    --chrome-flags="--headless=new --no-sandbox --disable-gpu" >/dev/null 2>&1
  python3 - "$OUT/$slug.json" "$p" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
c = d["categories"]; a = d["audits"]
def s(k):
    v = c[k]["score"]
    return f"{round(v*100):3d}" if v is not None else "  -"
print(f"  {sys.argv[2]:<34} perf {s('performance')}  a11y {s('accessibility')}  "
      f"seo {s('seo')}  bp {s('best-practices')}   "
      f"LCP {a['largest-contentful-paint']['numericValue']:.0f}ms  "
      f"CLS {a['cumulative-layout-shift']['numericValue']:.3f}  "
      f"TBT {a['total-blocking-time']['numericValue']:.0f}ms")
PY
done

echo
echo "=== axe-core ==="
"$CHROME_PATH" --headless=new --disable-gpu --no-sandbox \
  --remote-debugging-port="$CDP_PORT" --remote-allow-origins='*' \
  --user-data-dir="$HERE/.cdp-profile" about:blank >/dev/null 2>&1 &
CHR=$!
curl --retry 25 --retry-connrefused --retry-delay 1 -sf \
  "http://127.0.0.1:$CDP_PORT/json/version" >/dev/null || {
  echo "chrome CDP never came up"; exit 1; }
node "$HERE/axerun.mjs" "http://127.0.0.1:$CDP_PORT" "$BASE" \
  "$HERE/node_modules/axe-core/axe.min.js" "${PAGES[@]}" | tee "$OUT/axe.txt"

echo
echo "results in _dev/measure/results/$LABEL/"
