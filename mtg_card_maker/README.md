# MTG Card Renderer

Renders Magic: The Gathering card JSON into print-ready PNG images using Python/Pillow. No external APIs or apps required.

## Quick Start

```bash
pip install Pillow cairosvg
python scripts/render_cards.py cards.json --output-dir ./output --dpi 300
```

## Features

- **Exact physical dimensions** — 63 × 88 mm at any DPI (300 default, 600 for high-res)
- **Real MTG fonts** — Beleren Bold (titles) and MPlantin (rules text)
- **308 mana symbols** — SVG-rendered from the [andrewgioia/mana](https://github.com/andrewgioia/mana) project
- **Accurate layout** — art box (53 × 39 mm), text box, type line, and P/T box sized from real card measurements
- **Custom card art** — supply an `art_image` path and the renderer crops it to fit the art box
- **Art direction workflow** — cards can include an `art_direction` field to guide image search or LLM generation
- **Filters** — render by color (`--filter-color R`) or rarity (`--filter-rarity mythic`)

## Input Format

Accepts JSON matching the `mtg-set-designer` skill output — a single card object, an array, or a set object with a `cards` array.

Required fields: `name`, `mana_cost`, `type`. Optional: `rules_text`, `flavor_text`, `power`, `toughness`, `rarity`, `color`, `art_direction`, `art_image`.

## Card Art

Each card can include two art-related fields:

- **`art_direction`** — text describing the desired art (subject, mood, composition). Used to guide image search or generation.
- **`art_image`** — path to a local image file. The renderer centre-crops it to fill the art box.

If no `art_image` is provided, a colour-gradient placeholder is drawn based on the card's colour identity.

## DPI Reference

| DPI | Pixels | Use |
|-----|--------|-----|
| 150 | 372 × 520 | Screen preview |
| 300 | 744 × 1039 | Standard print |
| 600 | 1488 × 2079 | Professional print |
