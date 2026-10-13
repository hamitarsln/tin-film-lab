"""Scrape Mixkit music listing pages into candidates.json (metadata only)."""
import json, re, sys, html, urllib.request
from pathlib import Path

LISTINGS = sys.argv[1:] or []
OUT = Path(__file__).with_name("candidates.json")
card_re = re.compile(
    r'data-audio-player-item-id-value="(\d+)".*?item-grid-card__title">\s*(.*?)\s*</h2>'
    r'.*?music-preview__author">\s*by (.*?)\s*</p>(.*?)data-test-id="duration">\s*([\d:]+)',
    re.S)
tag_re = re.compile(r'class="meta-links__link"[^>]*href="(/free-stock-music/[^"]+)">([^<]+)</a>')

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

tracks = json.loads(OUT.read_text()) if OUT.exists() else {}
for listing in LISTINGS:
    for page in range(1, 6):
        url = f"https://mixkit.co{listing}" + (f"?page={page}" if page > 1 else "")
        try:
            body = get(url)
        except Exception as e:
            print("stop", url, e); break
        found = card_re.findall(body)
        if not found: break
        for tid, title, author, meta, dur in found:
            m, s = dur.split(":")
            t = tracks.setdefault(tid, {"id": int(tid), "title": html.unescape(title), "author": html.unescape(author),
                                        "duration": int(m) * 60 + int(s), "tags": [], "listings": []})
            t["tags"] = sorted(set(t["tags"]) | {html.unescape(n) for _, n in tag_re.findall(meta)})
            if listing not in t["listings"]: t["listings"].append(listing)
        print(url, len(found))
OUT.write_text(json.dumps(tracks, indent=1))
print("total", len(tracks))
