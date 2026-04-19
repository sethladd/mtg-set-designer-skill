---
name: mtg-card-renderer
description: Render Magic&#58; The Gathering card descriptions as realistic card images (PNG). Use this skill whenever the user wants to generate, render, visualize, or create images of MTG cards — whether from JSON card data (like the output of mtg-set-designer), a card list, or even a single card description. Also trigger when the user says things like "show me what this card looks like", "make card images", "render my set", "generate card art", "create card mockups", "print proxies", or "I want to see the cards". Works entirely locally using Python/Pillow with no external API keys. Produces individual PNG files at exact MTG card dimensions.
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
Optional fields: `rules_text`, `flavor_text`, `power`, `toughness`, `rarity`, `color`, `id`, `art_direction`, `art_description`, `art_image`

The `color` field accepts: `W` (white), `U` (blue), `B` (black), `R` (red), `G` (green). Multi-color cards use arrays like `["W", "U"]`. Colorless cards use `[]` or omit the field. If `color` is omitted, the renderer infers it from `mana_cost`.

### Art fields

Either `art_direction` (simple) or `art_description` (structured) tells `generate_art.py` what to make. `art_image` tells `render_cards.py` what to draw.

- **`art_direction`** — a flat text description of what the card art should depict. When present, `generate_art.py` composes `"<name>" (<type>): <art_direction>`, appends a generic MTG style suffix, and appends a short negative-prompt baseline ("no text, no borders, …") before sending to the model.
- **`art_description`** — a structured object with any of these keys: `scene`, `focus`, `mood`, `palette`, `frame`, `style_anchor`, `negative_prompt`. Takes precedence over `art_direction` when both are present. The script flattens the available keys to `<style_anchor>\n\n<scene>\n\nFocus: … Mood: … Palette: … Framing: ….\n\nNegative prompt: <negative_prompt>`. This is the canonical assembler — do not write a pre-flattened `prompt` field into the JSON; the mtg-art-director skill has been updated accordingly.
- **Every prompt — regardless of build path — receives a trailing centering directive** that requires the main character or figure to be centered both horizontally and vertically in the 4:3 source image, so the subject survives the centre-crop to the 53:39 art box without clipping. This overrides off-centre framing hints (e.g. `frame: "edge-cropped at the lifting boot"`) by design — centering is mandatory because an off-centre subject will almost always get clipped at the ears/feet when the renderer crops the art into the card frame.
- **`art_image`** — path to a local image file to use as the card art. When present, the renderer loads this image, centre-crops it to the 53 × 39 mm art box, and composites it onto the card. When absent, a procedural gradient placeholder is drawn instead. `generate_art.py` writes this field (with `--update-json`) after a successful generation.

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

### Step 3 — Generate art with Gemini Nano Banana

For cards where no suitable existing image was found (or for original/non-IP sets), use the bundled `scripts/generate_art.py` helper. It calls the **Gemini "Nano Banana" image-generation API** (model `gemini-3.1-flash-image-preview` by default — "Nano Banana 2"), requests a landscape image, and **centre-crops the result to the exact aspect ratio of the M15+ art box (53:39 ≈ 1.359:1)** so the output drops into the card frame with no distortion.

The Nano-Banana-supported landscape aspect ratio closest to the art box is 4:3 (1.333:1); the ~2% excess height is trimmed during the crop step. No horizontal crop is needed.

#### Setup

```bash
pip install google-genai Pillow --break-system-packages
export GEMINI_API_KEY="..."   # get a free-tier key at https://aistudio.google.com/app/apikey
```

#### Generate art for a whole set

```bash
# Populate art_image on every card with an art_direction, then write the
# updated paths back into set.json so render_cards.py picks them up.
python scripts/generate_art.py set.json --update-json
```

Useful flags:

- `--art-dir ./art` — root directory for generated PNGs (default `./art`). Each card gets its own subdirectory; see "Variants" below.
- `--variants N` — number of variants to generate per card (default `2`). See "Variants" below. Ignored when `--variant-styles` is set.
- `--variant-styles PATH` — JSON file of per-variant artistic-medium overrides (e.g. oil / watercolor / digital realism). The file's length determines the number of variants per card, and each variant's `style_anchor` replaces the set's canonical anchor for that one generation. See "Styled variants" below. A starter file lives at `scripts/variant_styles.example.json`.
- `--model gemini-3-pro-image-preview` — Nano Banana Pro, higher quality (slower and more expensive); good for mythics and rares
- `--model gemini-2.5-flash-image` — original Nano Banana (previous generation)
- `--image-size 2K` / `4K` — output resolution before cropping (default `1K`; `512` also supported)
- `--concurrency N` — number of images to generate in parallel (default `4`). See "Parallelism" below.
- `--retries N` — retry attempts per card on transient errors (default `3`). See "Retries" below.
- `--filter-rarity mythic` / `--filter-color R` — generate only a slice
- `--limit 5` — cap the number of **cards** (each still generates `--variants` images, so total API calls = `--limit × --variants`)
- `--force` — regenerate even if the variant file already exists on disk
- `--dry-run` — print the prompts that would be sent, no API calls

The script skips variants whose PNG already exists on disk, so repeat runs only fill in the gaps. Failed generations are reported per-variant without aborting the batch.

#### Variants

By default `generate_art.py` generates **two variants per card** so the human can pick the better one. Nano Banana output is stochastic and sometimes weird (a character loses a hand, the camera is in the floor, the wrong subject is centred); having a second option makes that recoverable without a regenerate step.

Disk layout is always per-card-subdirectory, regardless of `--variants` value:

```
./art/
  joe_grunt/
    joe_grunt_1.png
    joe_grunt_2.png
    joe_grunt_3.png
  zartan_master_of_disguise/
    zartan_master_of_disguise_1.png
    zartan_master_of_disguise_2.png
    zartan_master_of_disguise_3.png
```

**Picking a variant:** after generation, open a card's subdirectory in Finder (macOS) and Quick Look through the PNGs — Cmd-Down to enter the folder, Space to preview, arrow keys to step through. When you find the one you want, edit the card's `art_image` field in the JSON to point at `<slug>_2.png` or `<slug>_3.png` instead of the default `_1.png`.

**Default `art_image`:** with `--update-json`, the script sets each card's `art_image` to the **lowest-numbered variant whose PNG actually exists**. So variant 1 is the default, but if variant 1 was safety-blocked and only variants 2 and 3 succeeded, the pointer automatically falls through to variant 2. If you've already hand-picked a variant and the file still exists, your choice is preserved on rerun — the script never clobbers a valid manual pick.

**Cost:** each variant is a separate API call, so generating 2 variants × 273 cards at Nano Banana 2 1K is ~2× the single-variant cost. Dial `--variants 1` for quick drafts, `--variants 3` for more options, `--variants 5` if you really want options.

**Failure handling:** if variant 2 fails but 1 and 3 succeed, the card still has art — the post-pass finds the lowest existing variant. Rerunning the command picks up only the failed variant (skip-existing works per-variant).

#### Styled variants

Default `--variants N` generates N options using a single identical prompt, so the differences you see are just Nano Banana's own stochasticity — usually pose/lighting jitter, rarely a genuinely different *look*. When you want the variants to feel like the same scene *illustrated by three different artists* (oil painting vs watercolor vs digital realism, say), use `--variant-styles PATH` instead.

The file is a JSON array of `{name, style_anchor}` objects. Each entry's `style_anchor` replaces the card's own `art_description.style_anchor` — only for that one generation. The on-disk set JSON is never mutated, so the art-director's canonical anchor is preserved. The `name` is slugified into the output filename so Finder Quick Look shows the style at a glance:

```
./art/
  joe_grunt/
    joe_grunt_oil.png
    joe_grunt_watercolor.png
    joe_grunt_digital.png
```

A starter file with three mediums ships at `scripts/variant_styles.example.json`:

```json
[
  {"name": "oil",        "style_anchor": "Magic: The Gathering card art, oil painting on canvas with visible impasto brushwork, classical chiaroscuro, warm varnished palette, 4:3 landscape aspect ratio, cinematic composition"},
  {"name": "watercolor", "style_anchor": "Magic: The Gathering card art, watercolor and ink illustration with soft wet-into-wet washes, loose linework, luminous negative space, 4:3 landscape aspect ratio, cinematic composition"},
  {"name": "digital",    "style_anchor": "Magic: The Gathering card art, digital realism with crisp rendering, cinematic volumetric lighting, photoreal textures and materials, 4:3 landscape aspect ratio, cinematic composition"}
]
```

Copy it, edit to taste, point `--variant-styles` at your copy. Keep the MTG framing and the `4:3 landscape aspect ratio` cue in each entry — those keep the output compatible with the card frame crop.

```bash
python scripts/generate_art.py set.json \
    --variant-styles scripts/variant_styles.example.json \
    --update-json
```

**Default `art_image` in style mode:** the first style in the file wins — so put your preferred "safe default" first. The human can still hand-edit `art_image` to `<slug>_watercolor.png` etc. to override.

**Tradeoff to be aware of:** the mtg-art-director skill's guiding principle #6 is that `style_anchor` is picked once per set and never varies, because the repeated anchor is the primary mechanism for set-wide visual cohesion. Styled variants swim against that intent by design — they're a *selection-time* tool for giving the human options. Once you pick a winner, that card's effective style diverges from the set's declared anchor, so be deliberate: picking a mix of mediums across a set will break visual cohesion. The intended workflow is "pick one style consistently for all cards" or "pick per-card but record the picks in the set style guide."

#### Parallelism

`generate_art.py` dispatches work through a `ThreadPoolExecutor` and runs `--concurrency N` (default **4**) API calls simultaneously. Each worker is fully independent — it touches only its own card dict and writes to its own output file — so no locking or shared state is involved.

Each (card, variant) pair is its own work unit, so with `--variants 3 --concurrency 4` you're running 4 generations in parallel and the total queue is `cards × variants`. Output is reordered to match completion order and includes the variant index and per-image elapsed time:

```
Generating 819 image(s) with gemini-3.1-flash-image-preview (3 variant(s) per card, concurrency=4)...
  [1/819] Zartan, Master of Disguise v2 -> /…/zartan_master_of_disguise/zartan_master_of_disguise_2.png (1024x754) in 21.3s
  [2/819] Joe Grunt v1 -> /…/joe_grunt/joe_grunt_1.png (1024x754) in 24.7s
  [3/819] Joe Grunt v3 -> /…/joe_grunt/joe_grunt_3.png (1024x754) in 18.9s
```

Throughput rule of thumb at `--variants 3 --concurrency 4`: a 273-card set (819 images) takes ~1.5–2 hours versus ~5 hours serial. Set `--concurrency 1` to fall back to strict serial (useful for debugging a single prompt or when the API is flaky), which also switches the progress output to the `[k/N] name vX ... -> /path` two-stage pattern so you can see which image is currently in flight.

Watch for rate limits: Nano Banana 2's free tier is roughly **10 RPM**, so 4 workers is comfortable but 8+ will earn you 429s. Paid tier is much higher. Drop `--concurrency` if you see retry storms in stderr.

#### Retries

Transient failures are retried automatically with exponential backoff. `--retries N` (default **3**) sets the retry attempts per card *after* the initial try, so by default each card gets up to 4 total attempts. Backoff schedule: **2s, 4s, 8s, 16s, 32s**.

Retried (transient):
- `429 RESOURCE_EXHAUSTED` rate limits
- `5xx` server errors (`500 INTERNAL`, `502 BAD_GATEWAY`, `503 UNAVAILABLE`, `504 DEADLINE_EXCEEDED`)
- Network hiccups: timeouts, connection resets
- Text-only responses (the model occasionally returns a candidate with no image part; usually resolves on retry)

Not retried (deterministic):
- Safety-filter blocks (`SAFETY`, `PROHIBITED_CONTENT`, `BLOCKED_REASON`) — same prompt will fail the same way; edit the prompt instead
- Other 4xx client errors (`400 INVALID_ARGUMENT`, `401 UNAUTHENTICATED`, `403 PERMISSION_DENIED`)

Retry notices go to **stderr** so they don't pollute the stdout progress stream:

```
    [retry] Joe Grunt: APIError: 429 RESOURCE_EXHAUSTED — sleeping 2s before attempt 2/4
    [retry] Joe Grunt: APIError: 429 RESOURCE_EXHAUSTED — sleeping 4s before attempt 3/4
  [47/273] Joe Grunt -> /…/joe_grunt.png (1024x754) in 38.1s
```

If a card exhausts all retries, it's counted as a failure (printed to both streams) and the batch moves on. Rerun the same command afterwards — the skip-existing check means only the failed cards are re-attempted, and they'll pick up fresh retry budgets.

#### One-off generation

```bash
python scripts/generate_art.py --single \
    --name "Ember Archon" \
    --type "Creature — Archon" \
    --art-direction "A towering archon of living flame soaring above a burning battlefield, molten wings spread wide, cinematic lighting from below, dark smoke-filled sky" \
    --art-dir ./art
```

#### Prompt construction

For flat `art_direction` cards the script composes `"<card name>" (<type>): <art_direction>`, appends a short style suffix ("fantasy digital painting … landscape orientation"), and appends a negative-prompt baseline ("no text, no borders, no UI, no watermarks, …") that keeps the model from rendering frame elements or caption text that would clash with the card template. If you need a very different prompt, edit the card's `art_direction` itself — the script is a thin wrapper, not a prompt rewriter.

For structured `art_description` cards the script flattens `style_anchor → scene → Focus / Mood / Palette / Framing → Negative prompt` in that order (diffusion-model-optimal). When `--variant-styles` is active, the leading `style_anchor` is replaced with the per-variant override for that one generation; the scene, focus, mood, palette, frame, and negative_prompt fields are used verbatim regardless.

Nano Banana is called via `client.models.generate_content(...)` with `response_modalities=['TEXT','IMAGE']` and a nested `image_config=ImageConfig(aspect_ratio='4:3', image_size=...)`. The image bytes come back as `part.inline_data.data` on the multimodal response parts — unlike Imagen's dedicated `generate_images` endpoint.

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
- google-genai (only needed for `generate_art.py`) — `pip install google-genai --break-system-packages`

Rendering (`render_cards.py`) requires no external APIs. Art generation (`generate_art.py`) calls the Gemini Nano Banana image-generation API and needs a `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) environment variable.
