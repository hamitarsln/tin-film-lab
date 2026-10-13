# tin-film-lab

Launch films for Tin, made entirely in code by Claude Code on Opus 5.5: a `seek(t)` HTML page per film, rendered
with Playwright and ffmpeg, cut to a vetted and bar-mapped music library, reviewed frame by frame before the final.

Start with [HANDOFF.md](HANDOFF.md): what we did, how it works, what's left.

| Folder | What |
|---|---|
| `music/` | The vetted track library with bar-by-bar maps, the cut tool and the film runtime. See `music/README.md`. |
| `films/tin-launch/` | Product demo film (32 s, 16:9). Final: `out/tin-launch.mp4`. |
| `films/tin-art/` | Art film in the style of Fable 5 (21.6 s, square). Share copy: `out/tin-art-share.mp4`. |

## Setup

```bash
uv sync                                    # librosa 0.11 / numba 0.61 pins matter (newer numba segfaults)
mkdir -p bin && ln -sf "$(uv run python -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')" bin/ffmpeg
(cd films/tin-launch/tools && npm ci && npx playwright install chromium)
(cd films/tin-art/tools && npm ci)
```

Licensed files are not in the repo. Restore them before rendering:
- **Fonts:** copy `FunktionalGrotesk-*.ttf` and `SFMono-Medium.otf` from tin-web's `public/fonts/` (private, Tin team access)
  into `films/*/refs/brand/fonts/` and `films/tin-art/src/fonts/`.
- **Music:** `music/catalogue/*.py` re-downloads the Mixkit tracks; `music/tools/map_track.py` rebuilds each track's
  `check.mp3`; `music/tools/cut.py` recreates each film's `music-cut/music.wav` with the arguments in its `docs/MUSIC.md`.
  The demo film's sound effects are Mixkit downloads listed in `films/tin-launch/sfx/`.

Also not in the repo (too large, regenerable or third-party): the full Mixkit mp3s (`music/catalogue/*.py` rebuild them),
the art film's archive masters and cutouts (every source URL and rights field is in
`films/tin-art/materials/assets.json`; ask Ege for a tarball rather than re-downloading 5 GB), intermediate renders,
run logs and the downloaded reference films.
