#!/usr/bin/env bash
# Gate 5: the final film. 2160x2160, 24 fps, no motion blur (every change is a hard cut, and blur would ghost the
# previous shot into the first frame after each cut), mixed at -14 LUFS.
#   scripts/final.sh [poster_time_seconds]
# Writes out/tin-art.mp4 (the master), out/tin-art-share.mp4 (a lighter copy for sharing), out/poster.png and the
# review sheets in out/review/final/.
set -euo pipefail
cd "$(dirname "$0")/.."
FF=../../bin/ffmpeg
POSTER_T="${1:-6.35}"   # 04, the tin sign, at the end of its push
node scripts/editdoc.mjs
node tools/determinism.mjs src/index.html 0.1 1.2 3.0 5.0 7.0 8.2 10.4 12.3 13.6 14.5 15.3 16.6 17.9 18.9 21.5
node tools/render.mjs video --page src/index.html --w 2160 --h 2160 --fps 24 --sub 1 --workers 6 --out out/tin-art-silent.mp4
tools/mix.sh out/tin-art-silent.mp4 music-cut/music.wav out/tin-art.mp4
# share copy: same picture at a constrained bitrate (the master's per-frame grain makes it ~70 Mb/s), same audio
"$FF" -y -loglevel error -i out/tin-art.mp4 -c:v libx264 -preset slow -crf 21 -maxrate 24M -bufsize 48M -pix_fmt yuv420p \
  -c:a copy -movflags +faststart out/tin-art-share.mp4
node tools/render.mjs stills --page src/index.html --at "$POSTER_T" --outdir out/poster-tmp --w 2160 --h 2160
mv "out/poster-tmp/$(ls out/poster-tmp | head -1)" out/poster.png && rmdir out/poster-tmp
python3 scripts/filmsheets.py out/tin-art.mp4 out/review/final
python3 scripts/syncsheet.py out/tin-art.mp4 out/review/final/sync.png
"$FF" -hide_banner -i out/tin-art.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" || true
ls -la out/tin-art.mp4 out/tin-art-share.mp4 out/poster.png
