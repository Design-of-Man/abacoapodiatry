#!/bin/bash
# Vercel build: pull the site from the GitHub branch, then optionally fetch the
# hero video from a public URL supplied via the HERO_VIDEO_URL env var.
set -euo pipefail
mkdir -p public
curl -sL https://codeload.github.com/nicholasbkashuba-lab/abacoapodiatry/tar.gz/refs/heads/claude/jupiter-laser-redesign-55fr8l \
  | tar xz --strip-components=1 -C public
rm -rf public/_src public/.nojekyll public/_redirects public/.htaccess

if [ -n "${HERO_VIDEO_URL:-}" ]; then
  mkdir -p public/assets/video
  curl -sL --max-time 180 -o public/assets/video/lighthouse.mp4 "$HERO_VIDEO_URL" \
    && echo "hero video fetched" || echo "hero video fetch failed - poster fallback"
fi
