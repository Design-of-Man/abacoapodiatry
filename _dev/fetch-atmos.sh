#!/usr/bin/env bash
# Fetch the 42 generated atmos images straight into assets/img/atmos/<slug>.png.
# Works only once d8j0ntlcm91z4.cloudfront.net is allowed by the egress policy;
# until then every request fails at CONNECT and this reports each one.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ok=0; fail=0
while IFS=$'\t' read -r idx slug model job framing url status; do
  [ "$idx" = "index" ] && continue
  if curl -fsS --max-time 60 -o "assets/img/atmos/$slug.png" "$url"; then
    ok=$((ok+1)); printf "  ok   %s\n" "$slug"
  else
    fail=$((fail+1)); printf "  FAIL %s\n" "$slug"
  fi
done < _dev/atmos-manifest.tsv
printf "\n  %d downloaded, %d failed\n" "$ok" "$fail"
[ "$fail" -eq 0 ] || exit 1
