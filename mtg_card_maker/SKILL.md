---
name: mtg-card-renderer
description: Render Magic&#58; The Gathering card descriptions as realistic card images (PNG). Use this skill whenever the user wants to generate, render, visualize, or create images of MTG cards — whether from JSON card data (like the output of mtg-set-designer), a card list, or even a single card description. Also trigger when the user says things like "show me what this card looks like", "make card images", "render my set", "generate card art", "create card mockups", "print proxies", or "I want to see the cards". Works entirely locally using Python/Pillow with no external API keys. Produces individual PNG files plus optional contact sheets showing multiple cards in a grid.
---

# MTG Card Renderer

Render Magic: The Gathering cards as realistic-looking PNG images from structured JSON card data. Designed to consume the output of the `mtg-set-designer` skill but works with any card JSON that has the right fields.

## When to use

Any time the user wants to turn card data into card images. This includes rendering a full set from `set.json`, rendering a handful of cards for review, and creating proxy sheets for playtesting.

## Input format

The renderer accepts card JSON objects with these fields (matching the mtg-set-designer output):

```json
{
  "name": "Ember Archon",
  "mana_cost": "{3}{R}{R}",
  "type": "Creature — Archon",
  "rules_text": "Flying, haste\nWhen Ember Archon enters, it deals 3 damage to each opponent.",
  "flavor_text": "The sky burned before she arrived. After, nothing remained to burn.",
  "power": 4,
  "toughness": 4,
  "rarity": "rare",
  "color": ["R"],
  "art_direction": "A towering archon made of living flame soaring above a burning battlefield, molten wings spread wide, cinematic lighting from below, dark smoke-filled sky",
  "art_image": "./art/ember_archon.png"
}
```

Required fields: `name`, `mana_cost`, `type`
Optional fields: `rules_text`, `flavor_text`, `power`, `toughness`, `rarity`, `color`, `id`, `art_direction`, `art_image`

The `color` field accepts: `W` (white), `U` (blue), `B` (black), `R` (red), `G` (green). Multi-color cards use arrays like `["W", "U"]`. Colorless cards use `[]` or omit the field. If `color` is omitted, the renderer infers it from `mana_cost`.

### Art fields

- **`art_direction`** — a text description of what the card art should depict: subject, composition, mood, lighting, and style cues. Provided by the `mtg-set-designer` skill or written by the user. Used to guide image search and generation.
- **`art_image`** — path to a local image file to use as the card art. When present, the renderer loads this image, centre-crops it to the 53 × 39 mm art box, and composites it onto the card. When absent, a procedural gradient placeholder is drawn instead.

## Art sourcing workflow

When cards include `art_direction`, follow this process to populate `art_image` before rendering. Do this as a **pre-pass** over the card list — update the JSON with `art_image` paths, then run the renderer.

### Step 1 — Determine if the set is based on well-known IP

Check the set's theme, world, or design doc. If the set adapts a recognisable IP (Lord of the Rings, Greek mythology, Star Wars, Marvel, a popular video game, etc.), the cards may depict characters, creatures, locations, or moments that already have iconic imagery. Mark these sets as `known_ip = true` for the art pass.

### Step 2 — For known-IP sets: image search first

For each card that has `art_direction`:

1. **Build a search query** from the card's `art_direction` combined with the IP name and the card name. For example, for a Lord of the Rings set card named "Gandalf, the White" with art direction "Gandalf in white robes standing atop Orthanc, dawn light behind him", search for something like: `Gandalf the White standing on Orthanc tower dawn light fantasy art`.

2. **Use WebSearch** to find candidate images. Look for high-resolution fan art, concept art, promotional stills, or illustrations that closely match the art direction.

3. **Evaluate each candidate** against the art direction. A match must be close — the subject, composition, and mood should all align. Don't use an image just because it contains the right character in a completely wrong scene.

4. **If a strong match is found**, download the image using WebFetch and save it to an `art/` directory alongside the set JSON. Set the card's `art_image` field to the saved path. The renderer will centre-crop it to the art box dimensions automatically.

5. **If no strong match is found**, fall through to Step 3 (image generation).

### Step 3 — Generate art with LLM image generation

For cards where no suitable existing image was found (or for original/non-IP sets):

1. **Craft an image generation prompt** from the card's `art_direction`. Enhance it with style cues that work well for MTG art: "digital painting, fantasy illustration, dramatic lighting, MTG card art style, highly detailed". Keep the prompt focused on a single clear subject — card art works best when it has one strong focal point.

2. **Generate the image** using the LLM's image generation capabilities. Request a landscape or square aspect ratio (the art box is wider than tall — 53:39 ratio ≈ 1.36:1).

3. **Save the generated image** to the `art/` directory and set `art_image` on the card.

### Step 4 — Render

Once all cards have `art_image` paths populated (or left blank for fallback gradients), run the renderer:

```bash
python scripts/render_cards.py set.json --output-dir ./output --dpi 300
```

The renderer handles cropping automatically — images of any size or aspect ratio are scaled to cover the art box and centre-cropped to fit exactly.

### Batch strategy for large sets

For a full 261-card set, generating art for every card is expensive. Recommended approach:

- **Always generate art for**: mythics, rares, and signpost uncommons (the cards people look at most closely)
- **Generate selectively for commons**: prioritize cards with distinctive art directions; use fallback gradients for vanilla creatures and simple spells during early drafts
- **Use `--filter-rarity`** to render and review one rarity tier at a time

## Rendering commands

```bash
python scripts/render_cards.py <input.json> [--output-dir ./output] [--dpi 300]
```

- `<input.json>` — a JSON file containing either a single card object, an array of card objects, or a set object with a `cards` array
- `--dpi N` — target print resolution (default: 300). 300 → 744 × 1039 px (exact MTG card size), 600 → 1488 × 2079 px (high-res print)
- `--output-dir` — where to save PNGs (default: `./card_images`)
- `--filter-rarity <rarity>` — only render cards of this rarity
- `--filter-color <color>` — only render cards of this color (W/U/B/R/G)

All fonts, symbols, margins, borders, and line spacing scale proportionally with DPI. PNG files include DPI metadata for correct print sizing.

### Single card from CLI

```bash
python scripts/render_cards.py --single --name "Ember Archon" --mana-cost "{3}{R}{R}" --type "Creature — Archon" --rules "Flying, haste" --power 4 --toughness 4 --rarity rare --color R
```

## Card appearance

The renderer composites cards using real M15-style frame PNG overlays from `assets/frames/` (`w.png`, `u.png`, `b.png`, `r.png`, `g.png`, `m.png` for multicolour, `c.png` for colourless), plus matching power/toughness overlays from `assets/frames/pt/`. On top of the frame it draws mana cost symbols, card name in Beleren Bold, type line, rules text in MPlantin, italicised flavour text with separator, and a rarity gem indicator.

If a frame PNG is missing, the renderer falls back to a procedural gradient frame and prints a `WARNING` line to stdout — watch the render output and make sure no such warnings appear, otherwise your cards will look flat/procedural instead of using the real frames.

All layout measurements match real MTG card dimensions (M15+ frame): 63 × 88 mm card, 53 × 39 mm art box, ~53 × 24 mm text box, 3 mm top/side borders, 5 mm bottom border.

## Dependencies

- Python 3.8+
- Pillow (PIL) — `pip install Pillow --break-system-packages`
- cairosvg (for SVG mana symbols) — `pip install cairosvg --break-system-packages`

No external APIs required for rendering. Image search and generation in the art workflow use Claude's built-in tools.
