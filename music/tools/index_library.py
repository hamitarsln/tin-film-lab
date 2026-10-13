"""Write library/LIBRARY.md (the model's track chooser) and library/index.json from every map."""
import json
from pathlib import Path

LIB = Path(__file__).resolve().parents[1] / "library"
cat = {t["id"]: t for t in json.loads((LIB.parent / "catalogue" / "candidates.json").read_text()).values()}
rows = []
for d in sorted(LIB.iterdir()):
    if not (d / "map.json").exists():
        continue
    m = json.loads((d / "map.json").read_text())
    tags = cat.get(m["id"], {}).get("tags", [])
    drops = [s for s in m["sections"] if s["name"] == "drop"]
    breaks = [e for e in m["events"] if e["type"] == "break"]
    conf = "solid" if m["aligned_share"] >= 0.9 and m["downbeat_agreement"] >= 0.75 else "check by ear"
    rows.append({
        "id": m["id"], "dir": d.name, "title": m["title"], "author": m["author"], "bpm": round(m["bpm"], 2),
        "meter": f"{m['beats_per_bar']}/4", "bar": m["bar"], "duration": m["duration"], "bars": len(m["bars"]),
        "tags": tags, "grid": conf, "aligned_share": m["aligned_share"], "downbeat_source": m["downbeat_source"],
        "first_drop_bar": drops[0]["start_bar"] if drops else None,
        "first_drop_t": drops[0]["t"] if drops else None,
        "breaks": [e["bar"] for e in breaks],
        "structure": " → ".join(f"{s['name']} {s['start_bar']}–{s['end_bar']}" for s in m["sections"]),
    })
rows.sort(key=lambda r: r["bpm"])
(LIB / "index.json").write_text(json.dumps(rows, indent=1))
L = ["# Music library", "",
     "Tracks vetted by ear for Tin launch films. Each folder holds the full map of how the track moves:",
     "`MAP.md` to read, `map.json` for code, `map.png` to look at, `check.mp3` to hear the grid as clicks.", "",
     "Pick a track by the film's pace, then cut it with `music/tools/cut.py` so the drop lands where the story turns.",
     "Bars are the unit: at 120 BPM in 4/4 one bar is 2 s, so a 24 s film is 12 bars.", "",
     "| Track | BPM | Meter | Bar (s) | Length | First drop | Breaks | Grid | Feel |",
     "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    drop = f"bar {r['first_drop_bar']} ({r['first_drop_t']:.1f} s)" if r["first_drop_bar"] else "none"
    L.append(f"| [{r['title']}]({r['dir']}/MAP.md) #{r['id']} | {r['bpm']:.1f} | {r['meter']} | {r['bar']:.3f} | "
             f"{int(r['duration']//60)}:{int(r['duration']%60):02d} | {drop} | {', '.join(map(str, r['breaks'])) or '—'} | {r['grid']} | {', '.join(r['tags'][:5])} |")
L += ["", "## Structure", ""]
for r in rows:
    L.append(f"- **{r['title']}** ({r['bpm']:.1f} BPM): {r['structure']}")
L += ["", "Grid \"check by ear\" means fewer than 90% of detected beats sit on the fitted grid, or bar 1 was",
      "placed from the kick because the downbeat model was unsure. Listen to `check.mp3` before cutting to it.", ""]
(LIB / "LIBRARY.md").write_text("\n".join(L))
print(len(rows), "tracks")
