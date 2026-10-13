---
name: materials
description: Find, license-check, download, cut out and catalogue real public-domain images (archival scans and photographs) for the art film. Use whenever the film needs a material, object or texture.
---

# Materials

The film's richness comes from real things: scans of objects, prints, signs and surfaces that existed.
No image models, no stock photos with unclear rights, no screenshots of living brands.

## Sources (open access; images free to reuse)
| Archive | API (no key unless noted) | Rights field to check |
|---|---|---|
| Art Institute of Chicago | `https://api.artic.edu/api/v1/artworks/search?q=...&query[term][is_public_domain]=true&fields=id,title,date_display,image_id,is_public_domain` → IIIF `https://www.artic.edu/iiif/2/{image_id}/full/1686,/0/default.jpg` | `is_public_domain: true` |
| Cleveland Museum of Art | `https://openaccess-api.clevelandart.org/api/artworks/?q=...&cc0=1&has_image=1` → `images.print.url` | `share_license_status: CC0` |
| Library of Congress | `https://www.loc.gov/pictures/search/?q=...&fo=json` and `https://www.loc.gov/photos/?q=...&fo=json` | "No known restrictions" in rights |
| Smithsonian Open Access | `https://api.si.edu/openaccess/api/v1.0/search?q=...&api_key=DEMO_KEY` (rate-limited) | `usage.access: CC0` |
| Wikimedia Commons | `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=...&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata&format=json` | `extmetadata.LicenseShortName` is "Public domain" or "CC0" only |
| The Met | `https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&q=...` | `isPublicDomain: true` (the API may be down; skip it if so) |

Send a descriptive User-Agent (`tin-film-lab/1.0`), go slowly (one request a second per archive), and back
off on 429. Prefer the largest image the archive offers; a material must survive being shown at 2160 px.

## Rules
- Public domain or CC0 only. If the rights field is missing or says anything else, skip the image.
- No identifiable living people, no modern brand logos, no trademarks as the subject. Old, generic advertising is
  fine (an anonymous 1900s tin sign for soap), a famous current mark is not.
- Record every image in `materials/ASSETS.md` and `materials/assets.json`: id, file, title, date, archive,
  object URL, image URL, rights as stated, and what the film uses it for. Nothing enters the film unrecorded.

## Preparing a material
- Raw downloads go to `materials/raw/`. Never edit them.
- Cut out objects (a sign, a matchbook, a stamp, a punch card) with the local background remover:
  `uv run --project ../.. python -c "from rembg import remove, new_session; ..."` using `new_session('isnet-general-use')`.
  Check every cutout by eye; fix bad edges by hand-tuned masks rather than shipping fringes.
- Textures (paper, halftone, a map, a ceiling of pressed tin) are used whole, masked by the Tin mark.
- Prepared files go to `materials/cut/` as PNG with alpha, named `<nn>-<slug>.png`.
- Code may make textures where code is the honest medium (halftone dots, a CRT scanline, the terminal, pixels),
  and those are listed in ASSETS.md as "made in code".
