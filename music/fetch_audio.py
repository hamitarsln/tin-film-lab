"""Download the Mixkit audio this repo uses and rebuild every audio file made from it.

The repo ships the maps and cut lists but not Mixkit's audio: Mixkit's free licence lets the music be used inside
videos, not redistributed as standalone files. This script restores everything locally in one go.

usage (from the repo root):
  uv run python music/fetch_audio.py               # the 19 library tracks, the films' cuts, check clips and SFX
  uv run python music/fetch_audio.py --catalogue   # also all 255 measured catalogue tracks (about 1.1 GB)
  uv run python music/fetch_audio.py --sources-only

What it writes:
  music/catalogue/mp3/<id>.mp3          full tracks from assets.mixkit.co, checked against audio-manifest.json
  music/library/<dir>/check.mp3         60 s with clicks on the grid and a bell per section (from map.json)
  films/*/music-cut/music.wav           each film's cut, recreated with the bars recorded in its cue.json
  films/tin-launch/sfx/raw/<id>.wav     Mixkit sound effects
  films/tin-launch/sfx/sfx.wav          the demo film's sound-effects stem (tools/sfx.py)
"""
import argparse, hashlib, json, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUSIC = ROOT / "music"
MP3 = MUSIC / "catalogue" / "mp3"
MANIFEST = MUSIC / "audio-manifest.json"
UA = {"User-Agent": "tin-film-lab/1.0 (+https://github.com/tin-computer/tin-film-lab)"}
SFX_IDS = [1111, 1113, 1117, 2533, 2541, 2542]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest, expect=None):
    if dest.exists() and (expect is None or sha256(dest) == expect):
        return "kept"
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                data = r.read()
            break
        except Exception as e:
            if attempt == 3:
                raise SystemExit(f"failed: {url} ({e})")
            time.sleep(5 * (attempt + 1))
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(data)
    if expect and sha256(tmp) != expect:
        tmp.unlink()
        raise SystemExit(f"checksum mismatch for {url}: Mixkit changed the file, so the maps may no longer line up")
    tmp.replace(dest)
    return "downloaded"


def library():
    return json.loads((MUSIC / "library" / "index.json").read_text())


def fetch_sources(manifest, catalogue):
    ids = [r["id"] for r in library()]
    if catalogue:
        ids += [int(x) for x in (MUSIC / "catalogue" / "shortlist_ids.txt").read_text().split()]
    ids = sorted(set(ids))
    for n, i in enumerate(ids, 1):
        state = download(f"https://assets.mixkit.co/music/{i}/{i}.mp3", MP3 / f"{i}.mp3", manifest.get(f"music/{i}"))
        print(f"[{n}/{len(ids)}] track {i}: {state}")
    for i in SFX_IDS:
        dest = ROOT / "films" / "tin-launch" / "sfx" / "raw" / f"{i}.wav"
        state = download(f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}.wav", dest, manifest.get(f"sfx/{i}"))
        print(f"sfx {i}: {state}")


def rebuild_checks():
    sys.path.insert(0, str(MUSIC / "tools"))
    import numpy as np
    from map_track import write_check
    for r in library():
        d = MUSIC / "library" / r["dir"]
        m = json.loads((d / "map.json").read_text())
        downs = set(m["downbeats"])
        grid = {"beats": np.array(m["beats"]), "is_down": np.array([b in downs for b in m["beats"]])}
        write_check(d / "check.mp3", str(MP3 / f"{m['id']}.mp3"), grid, m["sections"], m["check"]["start"], m["check"]["length"])
        print(f"check clip: {r['dir']}")


def rebuild_cuts():
    for cue_path in sorted(ROOT.glob("films/*/music-cut/cue.json")) + sorted(ROOT.glob("films/*/tools/example/music/cue.json")):
        c = json.loads(cue_path.read_text())
        tid = c["track"]["id"]
        track_dir = next(MUSIC / "library" / r["dir"] for r in library() if r["id"] == tid)
        first, last = c["track"]["song_bars"]
        land = c["landing"]
        args = ["--bars", str(last - first + 1), "--land", land["what"], "--at", str(land["film_bar"] - 1),
                "--fade-bars", f"{c['fade_out'] / c['bar']:.6f}"]
        subprocess.run([sys.executable, str(MUSIC / "tools" / "cut.py"), str(track_dir), str(cue_path.parent), *args],
                       check=True, stdout=subprocess.DEVNULL)
        print(f"cut: {cue_path.parent.relative_to(ROOT)} ({c['track']['title']}, song bars {first}-{last})")


def rebuild_sfx():
    film = ROOT / "films" / "tin-launch"
    # the levels the final mix used (films/tin-launch/README.md)
    subprocess.run([sys.executable, str(film / "tools" / "sfx.py"), "--key-db", "-16", "--enter-db", "-13", "--click-db", "-10"], check=True, cwd=film, stdout=subprocess.DEVNULL)
    print("sfx stem: films/tin-launch/sfx/sfx.wav")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalogue", action="store_true", help="also fetch all 255 measured catalogue tracks")
    ap.add_argument("--sources-only", action="store_true", help="download only; don't rebuild derived audio")
    ap.add_argument("--write-manifest", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.write_manifest:  # maintainers: record checksums of the audio on disk
        man = {f"music/{p.stem}": sha256(p) for p in sorted(MP3.glob("*.mp3"))}
        man.update({f"sfx/{i}": sha256(ROOT / "films/tin-launch/sfx/raw" / f"{i}.wav") for i in SFX_IDS})
        MANIFEST.write_text(json.dumps(man, indent=1) + "\n")
        print(f"wrote {MANIFEST.relative_to(ROOT)} ({len(man)} files)")
        return
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    fetch_sources(manifest, a.catalogue)
    if not a.sources_only:
        rebuild_checks()
        rebuild_cuts()
        rebuild_sfx()
    print("done")


if __name__ == "__main__":
    main()
