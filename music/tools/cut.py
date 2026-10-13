"""Cut a mapped track to a film's length and re-time its map to film time.

usage:
  python cut.py <track_dir> <out_dir> --bars 12 [--land drop --at 4] [--fade-bars 1]

  --bars N        film length in whole bars (the film always ends on a bar line)
  --land WHAT     what to land at a film moment: "drop" (the first drop section or the
                  biggest bass entry), "section:<bar>" (a section starting at that song bar),
                  "bar:<n>" (any song bar), or "start" (song bar 1)
  --at BARS       film bar the landing falls on, counted from 0 (4 = the start of film bar 5)
  --fade-bars N   fade the music out over the last N bars (0 = hard stop on the final bar line)

Writes:
  music.wav   the cut, 48 kHz stereo, faded
  cue.json    the map in film time (bars renumbered from 1, times from 0)
  cue.js      the same as a script that sets window.CUE (for file:// pages)
  CUE.md      the film-time bar sheet a model plans scenes against
"""
import argparse, json, subprocess
from pathlib import Path

import numpy as np

FF = str(Path(__file__).resolve().parents[2] / "bin" / "ffmpeg")
LIB = Path(__file__).resolve().parents[1] / "catalogue" / "mp3"


def pick_landing(m, what):
    bars = m["bars"]
    if what == "start":
        return bars[0]["bar"]
    if what.startswith("bar:"):
        return int(what.split(":")[1])
    if what.startswith("section:"):
        return int(what.split(":")[1])
    if what == "drop":
        drops = [s for s in m["sections"] if s["name"] == "drop"]
        if drops:
            return drops[0]["start_bar"]
        ins = [e for e in m["events"] if e["type"] in ("bass_in", "break")]
        if ins:
            e = max(ins, key=lambda e: e.get("db", 0))
            return e.get("back_in_bar", e["bar"])
        return max(m["sections"], key=lambda s: s["energy"])["start_bar"]
    raise SystemExit(f"unknown --land {what}")


def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def glyph(x, w=8):
    k = int(round(x * w))
    return "█" * k + "·" * (w - k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("track"); ap.add_argument("out")
    ap.add_argument("--bars", type=int, required=True)
    ap.add_argument("--land", default="drop"); ap.add_argument("--at", type=int, default=4)
    ap.add_argument("--fade-bars", type=float, default=1)
    a = ap.parse_args()
    tdir, out = Path(a.track), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    m = json.loads((tdir / "map.json").read_text())
    by_bar = {b["bar"]: b for b in m["bars"]}
    land = pick_landing(m, a.land)
    first = land - a.at
    if first < 1:
        raise SystemExit(f"--at {a.at} needs {a.at} bars before song bar {land}; the song only has {land - 1}. Lower --at.")
    if by_bar[first]["end"] - by_bar[first]["t"] < m["bar"] * 0.9:
        raise SystemExit(f"song bar {first} is a partial pickup bar; lower --at by one")
    last = first + a.bars - 1
    if last not in by_bar:
        raise SystemExit(f"the song ends at bar {m['bars'][-1]['bar']}; {a.bars} bars from bar {first} runs past it")
    t0 = by_bar[first]["t"]
    t1 = by_bar[last]["end"]
    length = t1 - t0
    fade = min(a.fade_bars * m["bar"], length / 2)

    # audio
    src = LIB / f"{m['id']}.mp3"
    af = f"afade=t=in:d=0.01,afade=t=out:st={max(0.0, length - fade):.3f}:d={max(fade, 0.01):.3f}" if fade > 0 else "afade=t=in:d=0.01,afade=t=out:st={:.3f}:d=0.03".format(length - 0.03)
    subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{t0:.4f}", "-t", f"{length:.4f}", "-i", str(src),
                    "-af", af, "-ar", "48000", "-ac", "2", str(out / "music.wav")], check=True)

    # re-time the map
    def ft(t):
        return round(t - t0, 4)
    inwin = lambda t: t0 - 1e-6 <= t < t1 - 1e-6
    first_full = 2 if m["bars"][0]["end"] - m["bars"][0]["t"] < m["bar"] * 0.9 else 1
    bars = []
    for b in m["bars"]:
        if first <= b["bar"] <= last:
            bars.append({**b, "song_bar": b["bar"], "bar": b["bar"] - first + 1, "t": ft(b["t"]), "end": ft(b["end"]),
                         "phrase_start": (b["bar"] - first_full) % 4 == 0})
    phrase_offset = next((b["bar"] for b in bars if b["phrase_start"]), 1)
    secs = []
    for s in m["sections"]:
        a0, a1 = max(s["start_bar"], first), min(s["end_bar"], last)
        if a0 <= a1:
            secs.append({**s, "start_bar": a0 - first + 1, "end_bar": a1 - first + 1, "bars": a1 - a0 + 1,
                         "t": ft(by_bar[a0]["t"]), "end": ft(by_bar[a1]["end"]), "song_start_bar": s["start_bar"]})
    events = []
    for e in m["events"]:
        if inwin(e["t"]):
            e2 = {**e, "t": ft(e["t"])}
            for k in ("bar", "to_bar", "back_in_bar"):
                if k in e2:
                    e2[k] = e2[k] - first + 1
            if "back_in" in e2:
                e2["back_in"] = ft(e2["back_in"])
            events.append(e2)
    def refpos(pos):
        b, rest = pos.split(".", 1)
        return f"{int(b) - first + 1}.{rest}"
    hits = [{**h, "t": ft(h["t"]), "pos": refpos(h["pos"])} for h in m["hits"] if inwin(h["t"])]
    beats = [ft(t) for t in m["beats"] if inwin(t)]
    downs = [ft(t) for t in m["downbeats"] if inwin(t)]
    env = m["envelope"]; fps = env["fps"]
    i0, i1 = int(round(t0 * fps)), int(round(t1 * fps))
    envelope = {"fps": fps, **{k: v[i0:i1] for k, v in env.items() if k != "fps"}}
    cue = {
        "track": {"id": m["id"], "title": m["title"], "author": m["author"], "song_start": round(t0, 4),
                  "song_bars": [first, last], "license": "Mixkit Stock Music Free License"},
        "length": round(length, 4), "fade_out": round(fade, 3),
        "bpm": m["bpm"], "beat": m["beat"], "bar": m["bar"], "beats_per_bar": m["beats_per_bar"],
        "phrase_offset": phrase_offset,
        "landing": {"what": a.land, "song_bar": land, "film_bar": a.at + 1, "t": ft(by_bar[land]["t"])},
        "beats": beats, "downbeats": downs, "bars": bars, "sections": secs, "events": events, "hits": hits,
        "envelope": envelope,
    }
    (out / "cue.json").write_text(json.dumps(cue, separators=(",", ":")))
    # file:// pages can't fetch JSON, so also ship it as a script: <script src="music/cue.js"></script> -> window.CUE
    (out / "cue.js").write_text("window.CUE = " + json.dumps(cue, separators=(",", ":")) + ";\n")
    write_cue_md(out / "CUE.md", cue)
    print(json.dumps({"length": cue["length"], "bars": a.bars, "song_start": cue["track"]["song_start"],
                      "landing_t": cue["landing"]["t"], "sections": [f"{s['name']}@{s['start_bar']}" for s in secs]}))


def write_cue_md(path, c):
    L = []
    tr = c["track"]
    L.append(f"# Music cue: {tr['title']}\n")
    L.append(f"{c['length']:.3f} s · {len(c['bars'])} bars · {c['bpm']:.2f} BPM · {c['beats_per_bar']}/4 · "
             f"song {fmt(tr['song_start'])} onward (song bars {tr['song_bars'][0]}–{tr['song_bars'][1]})\n")
    L.append("All times are film seconds from 0. Bars are film bars from 1.\n")
    L.append("## Timing\n")
    L.append(f"- Beat = {c['beat']:.5f} s. Bar = {c['bar']:.5f} s. Film bar n starts at (n − 1) × {c['bar']:.5f} s.")
    L.append(f"- The song moves in 4-bar phrases. In this cut they start on film bars {', '.join(str(b['bar']) for b in c['bars'] if b['phrase_start'])}. Big changes belong on those.")
    L.append(f"- Time of bar n, beat k: (n − 1) × {c['bar']:.5f} + (k − 1) × {c['beat']:.5f}.")
    L.append(f"- The {c['landing']['what']} lands on film bar {c['landing']['film_bar']} at {c['landing']['t']:.3f} s.")
    if c["fade_out"] > 0:
        L.append(f"- The music fades out over the last {c['fade_out']:.2f} s. Hold the end card through it.")
    L.append("")
    L.append("## Sections\n")
    L.append("| Section | Film bars | Seconds | Level | Energy |")
    L.append("|---|---|---|---|---|")
    for s in c["sections"]:
        L.append(f"| {s['name']} | {s['start_bar']}–{s['end_bar']} | {s['t']:.2f}–{s['end']:.2f} | {s['level']} | {s['energy']:.2f} |")
    L.append("")
    L.append("## Sync points\n")
    for e in c["events"]:
        if e["type"] == "break":
            L.append(f"- {e['t']:.3f} s, bar {e['bar']}: break. The bass drops out, then slams back on bar {e['back_in_bar']} at {e['back_in']:.3f} s.")
        elif e["type"] == "riser":
            L.append(f"- {e['t']:.3f} s, bar {e['bar']}: riser building into bar {e['to_bar']}.")
        elif e["type"] == "stop":
            L.append(f"- {e['t']:.3f} s: {e['length']} s of near silence.")
        else:
            L.append(f"- {e['t']:.3f} s, bar {e['bar']}: {e['type'].replace('_', ' ')}.")
    if not c["events"]:
        L.append("- None inside this cut. Change scenes on phrase starts.")
    L.append("")
    if c["hits"]:
        L.append("Accents (strongest transients): " + ", ".join(f"{h['t']:.3f} s @{h['pos']}" for h in c["hits"]) + "\n")
    L.append("## Bar sheet\n")
    L.append("```")
    L.append("bar   start    section    energy    low     high    events")
    starts = {s["start_bar"] for s in c["sections"]}
    sec_at = {b: s["name"] for s in c["sections"] for b in range(s["start_bar"], s["end_bar"] + 1)}
    ev_at = {}
    for e in c["events"]:
        if "bar" in e:
            lab = {"break": f"break→{e.get('back_in_bar')}", "riser": f"riser→{e.get('to_bar')}"}.get(e["type"], e["type"].replace("_", " "))
            ev_at.setdefault(e["bar"], []).append(lab)
    land_bar = c["landing"]["film_bar"]
    for b in c["bars"]:
        n = b["bar"]
        mark = "▶" if n in starts else "┊" if b["phrase_start"] else " "
        extra = ev_at.get(n, []) + (["◆ landing"] if n == land_bar else [])
        L.append(f"{n:>3}{mark} {b['t']:>7.3f}  {sec_at.get(n, ''):<10} {glyph(b['energy'])}  {glyph(b['low_n'], 6)}  {glyph(b['high_n'], 6)}  {' '.join(extra)}")
    L.append("```\n")
    L.append("▶ section start, ┊ 4-bar phrase start, ◆ the landing. Plan scenes in bars, not seconds.\n")
    path.write_text("\n".join(L))


if __name__ == "__main__":
    main()
