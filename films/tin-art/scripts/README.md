# Board pipeline

Everything here runs from the folder `films/tin-art`. Python scripts that use OpenCV or rembg run in the lab's
environment: `uv run --project ../.. python …`. The others need only Pillow and numpy (`python3`).

## 1. Reference breakdown (gate 1)
- `refsheet.py <frames dir> <out.png> <fps> <step> <cols> <tile w> [from] [to]`: timestamped contact sheet of extracted frames.
- `cuts.py <frames dir> <fps> <threshold>`: cut list and hold lengths from frame differences.
- `grid.py <out.png> <cols> <tile w> files…`: labelled tile sheet.

Frames came from `../../bin/ffmpeg -i refs/films/<film>.mp4 -vf scale=480:-1 out/ref/<film>/f%04d.jpg`. Findings are in
`docs/REFERENCE.md`.

## 2. Raw materials
Research agents downloaded into `materials/raw/` (never edited) and recorded every candidate in
`materials/candidates/<agent>.json`. Four Commons files were throttled to reduced copies and later fetched again at full
size as `*-orig.jpg`.

## 3. Prepared materials (`materials/cut/`)
Final names follow the materials skill: `<nn>-<slug>.png` for textures and `<nn>-<slug>-<kk>.png` for object sets, numbered
in the order the board lays them along the strokes. `materials/cut/MANIFEST.json` maps every file to its archive ids and raw
files. Working files from earlier rounds are in `materials/cut/work/`.

**Textures** (B and C treatments): `python3 scripts/prep.py scripts/recipes.json [names…]` crops each recipe's box
(fractions of the source), squares it about its centre, and resizes it to 2160 × 2160 so frame pixels map 1:1 to source.
It warns on any upscale. Only three board textures are upscaled at all: 05 biscuit tin 1.24×, 06 can label 1.18× and 15 radio dial 1.03×.

**Made in code from a real source** (`scripts/codetex.py`):
- `09-halftone.png`: `codetex.py halftone materials/raw/halftone__si-CHSDM-94743AECF1492-000001.jpg materials/cut/09-halftone.png --crop 0.326,0.312,0.671,0.743 --cell 22 --blur 5 --gamma 0.9`
- `18-banner-pixels.png`: `codetex.py pixels materials/raw/labels__commons-155898625.jpg materials/cut/18-banner-pixels.png --crop 0,0,1,1 --px 24`

**Cut-out objects** (A treatment): `uv run --project ../.. python scripts/cutout.py <raw> <out.png> [options]`
- `--mode flat` keys out a flat scan background in Lab space (`--tol`). `--mode rembg` uses `isnet-general-use` for
  studio photos.
- `--hull` fills the object's convex hull so light print areas are not punched out, and `--band f` keeps the colour matte
  in an outer band so perforations and torn edges survive.
- `--erode n` pulls the edge in by n px; the edge band is then recoloured from the interior, so no background fringe
  survives.
- `--split n` and `--crop` separate several objects scanned together.

| Set | Options used |
|---|---|
| 01 engraved cards | `--mode flat --tol 14 --erode 2 --hull --maxside 1400`. Commons 90033412 and 90221414 were instead cropped inside their dark museum mounts (boxes `0.046,0.105,0.972,0.862` and `0.032,0.036,0.979,0.882`). |
| 03 trade cards | `--mode flat --tol 20 --erode 2 --hull --maxside 1400` (22 for the first three Met cards) |
| 10 poster stamps | `--mode flat --tol 16 --erode 1 --hull --band 0.035`. Sheets split with `--crop`: Vibuha 3×2 at `--band 0.04`, Finkenstedt `0,0,0.483,1` and `0.5,0,1,1`, Wiener Messe `0,0,0.565,1`. |
| 13 matchbooks | Pairs and triples: `--mode flat --tol 30 --erode 2 --hull --split 2/3`. Dutch Grille halves: `--crop 0,0,0.52,1` / `0.5,0,1,1`. Opened-flat covers: `--tol 22 --hull`. Koch Bros: `--tol 24 --split 2`. Cormaine: `--tol 24 --hull --maxside 1800`. Schaber's, Milk Bar, White Spot and Clover Club fill their scans, so they were only trimmed by 0.6 %. |
| 16 punched cards | `--mode flat --tol 20` (blue) / `--tol 14` (cream) `--erode 1 --hull --maxside 2400` |
| A1 match safes | `--mode rembg --erode 2 --hull --maxside 1400` |

Each set was checked on paper and on charcoal with `python3 scripts/cutsheet.py <out.jpg> files…` before use.

## 4. Board (gate 3)
- `src/index.html`: the page. Mark geometry, paper and grain, the treatments (`inside`, `knockout`, `chain`, `pile`),
  type-in-mark helpers, and `seek(i)`.
- `src/stills.js`: the 20 stills, 4 alternates and the end card, with sources and parameters.
- `node scripts/board.mjs [--only n,m] [--outdir out/board]` renders through `tools/render.mjs stills` at 2160 × 2160,
  names the files `NN-slug.png`, and builds `BOARD.png` (5 across) with `scripts/boardsheet.py`.
- `python3 scripts/reviewsheets.py out/board out/review/<round>`: 360 px, 640 px and 1:1 sheets for the critique.
- `node tools/determinism.mjs src/index.html 1 4 9 14 19 25` confirms every still is a pure function of its index.

## 5. Catalogue
`python3 scripts/assets.py` writes `materials/assets.json` and `materials/ASSETS.md` from the research files,
`scripts/usage.json` (which ids each still uses) and `materials/cut/MANIFEST.json`.
