#!/usr/bin/env python3
"""Fetch every video in the practice's YouTube playlist into a manifest.

Runs at DEPLOY time (Vercel build), where YouTube is reachable. Extracts
video IDs + titles from the playlist page's embedded ytInitialData and
writes assets/data/videos.js, which the /media/ page renders as a
thumbnail grid. If the fetch fails, the existing manifest is left alone
and the page falls back to the embedded playlist player.

Usage: python3 _src/fetch_videos.py [output_path]
"""
import json
import re
import sys
import urllib.request

PLAYLIST = "https://www.youtube.com/playlist?list=PLCPM-92qYtTdOlcUc4XqyHI66gRvd-BkW"
OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/data/videos.js"


def main():
    req = urllib.request.Request(PLAYLIST, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

    # playlistVideoRenderer blocks hold {"videoId":"...", ..., "title":{"runs":[{"text":"..."}]}}
    videos, seen = [], set()
    for m in re.finditer(
        r'"playlistVideoRenderer":\{"videoId":"([A-Za-z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"',
        html,
    ):
        vid, raw_title = m.group(1), m.group(2)
        if vid in seen:
            continue
        seen.add(vid)
        title = json.loads(f'"{raw_title}"')  # unescape \uXXXX etc.
        videos.append({"id": vid, "title": title})

    if not videos:
        print("fetch_videos: no videos parsed — leaving existing manifest untouched")
        return 1

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// Auto-generated at deploy time from the practice's YouTube playlist.\n")
        f.write("window.JL_VIDEOS = ")
        json.dump(videos, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    print(f"fetch_videos: wrote {len(videos)} videos to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
