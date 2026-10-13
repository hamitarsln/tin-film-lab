#!/usr/bin/env bash
# Review sheets for the critique loop. Usage: tools/sheets.sh <video.mp4> [outdir] [strip_at_seconds ...]
#   contact.png  2 frames per second, 6 across          (pacing, variety, composition)
#   phone.png    1 frame per second at 360 px wide      (readability on a phone)
#   strip-<t>.png 12 consecutive frames around t        (pops, overlaps, ghosting in fast moves)
set -euo pipefail
FF="${FFMPEG:-$(cd "$(dirname "$0")/../../.." && pwd)/bin/ffmpeg}"
v="$1"; out="${2:-out/review}"; shift $(( $# > 1 ? 2 : 1 )) || true
mkdir -p "$out"
dur=$( ("$FF" -i "$v" 2>&1 || true) | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')
rows=$(python3 -c "import math;print(max(1,math.ceil($dur*2/6)))")
"$FF" -y -loglevel error -i "$v" -vf "fps=2,scale=320:-1,tile=6x${rows}:padding=4:color=white" -frames:v 1 "$out/contact.png"
prow=$(python3 -c "import math;print(max(1,math.ceil($dur/5)))")
"$FF" -y -loglevel error -i "$v" -vf "fps=1,scale=360:-1,tile=5x${prow}:padding=4:color=white" -frames:v 1 "$out/phone.png"
for t in "$@"; do
  s=$(python3 -c "print(max(0,$t-0.1))")
  "$FF" -y -loglevel error -ss "$s" -i "$v" -vf "scale=320:-1,tile=6x2:padding=2:color=white" -frames:v 1 "$out/strip-$t.png"
done
echo "$out/contact.png $out/phone.png (duration ${dur}s)"
