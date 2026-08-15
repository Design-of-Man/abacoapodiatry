#!/usr/bin/env bash
# Kept in a file so the pkill patterns below don't appear in the invoking
# shell's own command line -- pkill -f happily matches the caller and kills it.
set -u
export NO_PROXY=127.0.0.1,localhost no_proxy=127.0.0.1,localhost
S="$(cd "$(dirname "$0")" && pwd)"
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

cleanup() {
  [ -n "${CHROME_PID:-}" ] && kill "$CHROME_PID" 2>/dev/null
  [ -n "${MOCK_PID:-}" ] && kill "$MOCK_PID" 2>/dev/null
  return 0
}
trap cleanup EXIT

rm -rf "$S/cdp-profile"
python3 "$S/mockserver.py" >"$S/mock.log" 2>&1 &
MOCK_PID=$!
"$CHROME" --headless=new --disable-gpu --no-sandbox --remote-debugging-port=9222 \
  --remote-allow-origins='*' --user-data-dir="$S/cdp-profile" about:blank \
  >"$S/chrome.log" 2>&1 &
CHROME_PID=$!

curl --retry 30 --retry-connrefused --retry-delay 1 -sf \
  http://127.0.0.1:9222/json/version >/dev/null || {
  echo "chrome CDP never came up:"; tail -5 "$S/chrome.log"; exit 1; }
curl --retry 15 --retry-connrefused --retry-delay 1 -sf \
  http://127.0.0.1:8767/test/ok >/dev/null || {
  echo "mock server never came up:"; tail -5 "$S/mock.log"; exit 1; }

echo "=== contact form behaviour against each /api/contact outcome ==="
echo
node "$S/formtest.mjs" http://127.0.0.1:9222
