# MTG Card Renderer

Renders Magic: The Gathering card JSON into print-ready PNG images using Python/Pillow, and (optionally) generates the card art for each card via the Gemini "Nano Banana" image-generation API. No external apps required; rendering runs fully local.

## Quick Start

```bash
pip install Pillow cairosvg
python scripts/render_cards.py cards.json --output-dir ./output --dpi 300
```

To generate art before rendering:

```bash
pip install google-genai
export GEMINI_API_KEY="..."   # free-tier key at https://aistudio.google.com/app/apikey
python scripts/generate_art.py set.json --update-json
python scripts/render_cards.py set.json --output-dir ./output --dpi 300
```

## Features

### Rendering (`scripts/render_cards.py`)

- **Exact physical dimensions** — 63 × 88 mm at any DPI (300 default, 600 for high-res)
- **Real MTG fonts** — Beleren Bold (titles) and MPlantin (rules text)
- **308 mana symbols** — SVG-rendered from the [andrewgioia/mana](https://github.com/andrewgioia/mana) project
- **Accurate layout** — art box (53 × 39 mm), text box, type line, and P/T box sized from real M15+ card measurements
- **Real frame PNGs** — per-colour M15 frames under `assets/frames/` with procedural-gradient fallback
- **Custom card art** — supply an `art_image` path and the renderer centre-crops it to the art box
- **Filters** — render by color (`--filter-color R`) or rarity (`--filter-rarity mythic`)

### Art generation (`scripts/generate_art.py`)

- **Gemini Nano Banana** — calls `gemini-3.1-flash-image-preview` by default; `--model gemini-3-pro-image-preview` for higher-quality rares/mythics
- **Art-box-aware cropping** — requests 4:3 landscape and centre-crops to the 53:39 art-box ratio so nothing distorts
- **Variants per card** — three variants by default so you can pick the best; per-card subdirectories keep Finder Quick Look tidy
- **Styled variants** — `--variant-styles` swaps the `style_anchor` per variant (e.g. oil / watercolor / digital) without mutating the set JSON; starter file at `scripts/variant_styles.example.json`
- **Parallel + resumable** — `--concurrency 4` by default; skips variants already on disk, so reruns only fill in failures
- **Retries with backoff** — transient errors (429s, 5xx, network, text-only responses) retry automatically; safety blocks and 4xx don't
- **Prompt assembly** — flat `art_direction` becomes `"<name>" (<type>): <text>` + style suffix + negative prompt; structured `art_description` flattens `style_anchor → scene → focus/mood/palette/frame → negative prompt`; every prompt gets a trailing centering directive so the subject survives the crop

## Input Format

Accepts JSON matching the `mtg-set-designer` skill output — a single card object, an array, or a set object with a `cards` array.

Required: `name`, `mana_cost`, `type`. Optional: `rules_text`, `flavor_text`, `power`, `toughness`, `rarity`, `color`, `art_direction`, `art_description`, `art_image`.

## Card Art

Each card can include up to three art-related fields:

- **`art_direction`** — flat text describing the desired art. Simplest form; used by `generate_art.py` as the scene description.
- **`art_description`** — a structured object (`scene`, `focus`, `mood`, `palette`, `frame`, `style_anchor`, `negative_prompt`). Takes precedence over `art_direction` when both are present, and is what the `mtg-art-director` skill produces.
- **`art_image`** — path to a local image file. The renderer centre-crops it to fill the art box. `generate_art.py --update-json` writes this field for you after a successful generation.

If no `art_image` is provided, a colour-gradient placeholder is drawn based on the card's colour identity.

See `SKILL.md` for the full art sourcing workflow (known-IP image-search first, generation fallback, variant picking, batch strategy for large sets).

## DPI Reference

| DPI | Pixels | Use |
|-----|--------|-----|
| 150 | 372 × 520 | Screen preview |
| 300 | 744 × 1039 | Standard print |
| 600 | 1488 × 2079 | Professional print |

## Dependencies

- Python 3.8+
- `Pillow` — core rendering
- `cairosvg` — SVG mana symbols
- `google-genai` — only for `generate_art.py`; requires `GEMINI_API_KEY` (or `GOOGLE_API_KEY`)
