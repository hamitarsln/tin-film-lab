"""Build the sound-effects stem from sfx/events.json (written by tools/sfx-events.mjs).

usage: python3 tools/sfx.py [--key-db -22] [--click-db -16] [--every 3]

Samples are Mixkit SFX (free licence, no attribution), downloaded to sfx/raw/:
  2542 "Hard single key press in a laptop", 2533 "Single key type", 1117 "Classic click".
Each sample is placed so its measured onset lands on the event time. Keys: the page types ~36 characters a
second (fine on screen, a machine-gun roll in sound), so only a seeded subset of about one in three keystrokes is
voiced, with ±3 dB of seeded variation; Enter uses the hard key a little louder; clicks sit on the cursor presses.
Writes sfx/sfx.wav (48 kHz stereo, the film's exact length).
"""
import argparse, json, subprocess, random
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FF = str(ROOT.parents[1] / "bin" / "ffmpeg")
SR = 48000


def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def onset(a, frac=0.25):
    win = int(SR * 0.004)
    rms = np.sqrt(np.convolve(a ** 2, np.ones(win) / win, "same"))
    return int(np.argmax(rms > rms.max() * frac))


def cut(a, pre=0.004, post=0.12):
    """Trim around the onset, with a short fade-out; returns (clip, index of the onset inside the clip)."""
    o = onset(a)
    s, e = max(0, o - int(pre * SR)), min(len(a), o + int(post * SR))
    c = a[s:e].copy()
    fade = int(0.03 * SR)
    c[-fade:] *= np.linspace(1, 0, fade)
    return c / (np.abs(c).max() + 1e-9), o - s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-db", type=float, default=-22)
    ap.add_argument("--enter-db", type=float, default=-18)
    ap.add_argument("--click-db", type=float, default=-16)
    ap.add_argument("--every", type=int, default=3)
    a = ap.parse_args()
    cue = json.loads((ROOT / "music-cut" / "cue.json").read_text())
    n = int(round(cue["length"] * SR))
    out = np.zeros(n, dtype=np.float32)
    keys = [cut(load(ROOT / "sfx/raw/2542.wav")), cut(load(ROOT / "sfx/raw/2533.wav"))]
    enter = cut(load(ROOT / "sfx/raw/2542.wav"), post=0.16)
    click = cut(load(ROOT / "sfx/raw/1117.wav"), post=0.15)
    rng = random.Random(7)
    events = json.loads((ROOT / "sfx/events.json").read_text())
    voiced = 0
    last_key = -1.0
    for e in events:
        t, kind = e["t"], e["kind"]
        if kind in ("key", "space"):
            # Voice roughly one keystroke in `every`, never two within 60 ms (a person can't).
            if rng.random() > 1 / a.every or t - last_key < 0.06:
                continue
            last_key = t
            clip, o = keys[rng.randrange(2)]
            gain = 10 ** ((a.key_db + rng.uniform(-3, 3) - (2 if kind == "space" else 0)) / 20)
            voiced += 1
        elif kind == "enter":
            (clip, o), gain = enter, 10 ** (a.enter_db / 20)
        else:
            (clip, o), gain = click, 10 ** (a.click_db / 20)
        s = int(round(t * SR)) - o
        if s < 0:
            clip, s = clip[-s:], 0
        e_ = min(n, s + len(clip))
        out[s:e_] += clip[: e_ - s] * gain
    stereo = np.repeat(out[:, None], 2, axis=1)
    dst = ROOT / "sfx" / "sfx.wav"
    subprocess.run([FF, "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(dst)], input=stereo.astype(np.float32).tobytes(), check=True)
    print(f"wrote {dst}: {voiced} keys voiced, peak {20 * np.log10(np.abs(out).max() + 1e-9):.1f} dBFS")


if __name__ == "__main__":
    main()
