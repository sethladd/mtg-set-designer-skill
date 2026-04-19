#!/usr/bin/env python3
"""
Generate MTG card art with Gemini "Nano Banana" image models and crop to the
card art box.

For each card with an ``art_direction`` (and no existing ``art_image``),
this script calls the Gemini image-generation API, requests a landscape
image, and centre-crops it to exactly the aspect ratio of the M15+ art
box (53 × 39 mm ≈ 1.359:1). The generated PNG is saved under
``--art-dir`` and, if requested, the card's ``art_image`` field is
written back to the source JSON so a subsequent run of
``render_cards.py`` will pick it up.

The closest Nano-Banana-supported landscape aspect ratio is 4:3
(1.333:1); the ~2% overshoot in height is trimmed off the top and bottom
during the crop.

Requires:
    pip install google-genai Pillow --break-system-packages

Auth: set ``GEMINI_API_KEY`` (or ``GOOGLE_API_KEY``) with a key from
https://aistudio.google.com/app/apikey.

Usage:
    python generate_art.py set.json --update-json
    python generate_art.py set.json --filter-rarity mythic --limit 5
    python generate_art.py --single --name "Ember Archon" \\
        --art-direction "A towering archon of living flame soaring over a burning battlefield"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path

from PIL import Image

# ---------------------------------------------------------------------------
# Art box geometry — matches render_cards.py (M15+ frame)
# ---------------------------------------------------------------------------
ART_BOX_W_MM = 53.0
ART_BOX_H_MM = 39.0
ART_BOX_RATIO = ART_BOX_W_MM / ART_BOX_H_MM  # ≈ 1.3590

# Nano Banana landscape options include: 1:1, 3:2 (1.500), 4:3 (1.333),
# 5:4 (1.250), 16:9 (1.778), 21:9 (2.333).  4:3 is closest to 53:39 —
# small top/bottom crop only.
GEMINI_ASPECT = "4:3"

# Nano Banana model tiers (Gemini image generation, as of 2026):
# ``gemini-3.1-flash-image-preview``    — Nano Banana 2, latest Flash (default)
# ``gemini-3-pro-image-preview``        — Nano Banana Pro, asset-production quality
# ``gemini-2.5-flash-image``            — original Nano Banana, previous generation
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"

# Style cue appended only when composing a prompt from a flat
# ``art_direction`` string.  Not appended when the card already carries a
# structured ``art_description`` — those already specify ``style_anchor``.
# A per-variant style override (see ``--variant-styles``) replaces this
# string wholesale for its variant's generation; ``NEGATIVE_SUFFIX``
# below still applies regardless, because "no text, no borders" is a
# medium-independent requirement for the output to drop into a card
# frame.
STYLE_SUFFIX = (
    "Fantasy digital painting in the style of Magic: The Gathering card "
    "illustration. Cinematic composition, dramatic lighting, painterly, "
    "highly detailed. Landscape orientation."
)

# Baseline negatives for the flat-``art_direction`` path.  Kept separate
# from ``STYLE_SUFFIX`` so a variant style override can swap the medium
# without dropping the "no text, no borders, no UI" safeguards that keep
# the output compositable into a card frame.  Structured
# ``art_description`` carries its own ``negative_prompt`` field and does
# not use this constant.
NEGATIVE_SUFFIX = (
    "No text, no letters, no borders, no frames, no UI, no watermarks, "
    "no logos, no card layout."
)

# Hard requirement appended to EVERY prompt regardless of build path.
# The MTG art box is a 53:39 landscape window with a narrow top/bottom
# crop from the 4:3 source; if the subject drifts off-centre it gets
# clipped at the ears/feet.  Strong centering language keeps the main
# figure intact through the crop.
CENTER_DIRECTIVE = (
    "CRITICAL COMPOSITION REQUIREMENT: The main character or primary "
    "figure must be centered in the frame — both horizontally and "
    "vertically — fully visible, with clear headroom above and ground "
    "below. Do not crop the subject at the edges. Do not place the "
    "subject in a corner or off to one side. The hero of the scene "
    "occupies the visual middle of the landscape image. Background "
    "elements may extend to the edges, but the main figure stays "
    "centrally framed so it survives a symmetric crop to a 53:39 "
    "aspect ratio."
)


def _load_genai():
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.stderr.write(
            "ERROR: google-genai SDK not installed.\n"
            "Install with: pip install google-genai Pillow --break-system-packages\n"
        )
        sys.exit(1)
    return genai, types


def _api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.stderr.write(
            "ERROR: set GEMINI_API_KEY (or GOOGLE_API_KEY) with a Google AI Studio key.\n"
            "Get one at https://aistudio.google.com/app/apikey\n"
        )
        sys.exit(1)
    return key


def build_prompt(card: dict, style_override: dict | None = None) -> str:
    """Produce the text prompt to send to Nano Banana for a given card.

    Precedence:
      1. ``art_description`` as a structured object — flattened to
         ``style_anchor\\n\\nscene\\n\\nFocus: … Mood: … Palette: … Framing: …\\n\\nNegative prompt: …``.
         Missing keys are skipped.  No generic style suffix.  This is the
         canonical assembler referenced by the mtg-art-director skill; if
         the assembly order changes here, update that skill's Step 9 too.
      2. ``art_direction`` — flat string.  Composed as ``"<name>" (<type>):
         <direction>`` and the generic MTG style suffix is appended, since
         these short freeform strings benefit from style coaching.

    ``style_override`` — when supplied (driven by ``--variant-styles``),
    its ``style_anchor`` replaces the card's own ``style_anchor`` on the
    structured path, or ``STYLE_SUFFIX`` on the flat path.  The card's
    on-disk data is never mutated: the override is applied only to the
    body string for this one generation, so the set's canonical
    ``style_anchor`` stays intact for future runs.

    Every path appends ``CENTER_DIRECTIVE`` at the end.  The MTG art box
    is a narrow 53:39 window cropped from a 4:3 source, so drift from
    the centre clips the subject; the directive is mandatory regardless
    of what the caller specified.
    """
    body = _compose_body(card, style_override)
    if not body:
        return ""
    return f"{body}\n\n{CENTER_DIRECTIVE}"


def _compose_body(card: dict, style_override: dict | None = None) -> str:
    """Build the prompt body (everything before the centering directive)."""
    override_anchor = (
        style_override["style_anchor"].strip() if style_override else None
    )
    art = card.get("art_description")
    if isinstance(art, dict):
        parts: list[str] = []
        anchor = override_anchor or (art.get("style_anchor") or "").strip()
        if anchor:
            parts.append(anchor)
        if art.get("scene"):
            parts.append(art["scene"].strip())
        extras = []
        for key, label in (("focus", "Focus"), ("mood", "Mood"),
                           ("palette", "Palette"), ("frame", "Framing")):
            val = (art.get(key) or "").strip()
            if val:
                extras.append(f"{label}: {val}")
        if extras:
            parts.append(". ".join(extras) + ".")
        if art.get("negative_prompt"):
            parts.append(f"Negative prompt: {art['negative_prompt'].strip()}")
        if parts:
            return "\n\n".join(parts)

    direction = (card.get("art_direction") or "").strip()
    if not direction:
        return ""
    head_bits = []
    if card.get("name"):
        head_bits.append(f'"{card["name"]}"')
    ctype = card.get("type") or card.get("type_line")
    if ctype:
        head_bits.append(f"({ctype})")
    head = " ".join(head_bits)
    lead = f"{head}: {direction}" if head else direction
    # A variant style override replaces the generic style suffix but
    # never the negative baseline — "no text, no borders" applies no
    # matter what medium we're asking for.
    style = override_anchor or STYLE_SUFFIX
    return f"{lead}\n\n{style}\n\n{NEGATIVE_SUFFIX}"


def crop_to_art_box(img: Image.Image) -> Image.Image:
    """Centre-crop so the result's aspect ratio matches the MTG art box exactly."""
    w, h = img.size
    src_ratio = w / h
    if abs(src_ratio - ART_BOX_RATIO) < 1e-3:
        return img
    if src_ratio > ART_BOX_RATIO:
        new_w = round(h * ART_BOX_RATIO)
        off = (w - new_w) // 2
        return img.crop((off, 0, off + new_w, h))
    new_h = round(w / ART_BOX_RATIO)
    off = (h - new_h) // 2
    return img.crop((0, off, w, off + new_h))


def safe_slug(name: str) -> str:
    s = re.sub(r"[^\w\-]+", "_", name.lower().strip())
    return re.sub(r"_+", "_", s).strip("_") or "card"


def _variant_path(art_dir: Path, card: dict, variant_key: str) -> Path:
    """Return the PNG path for a given card's variant.

    ``variant_key`` is a string suffix baked into the filename — either
    a 1-based index (``"1"``, ``"2"``, ``"3"``) in the default numbered
    mode or a style slug (``"oil"``, ``"watercolor"``, ``"digital"``)
    when ``--variant-styles`` is used.  Named keys make Finder Quick
    Look more useful: the style shows up in the filename so the human
    can judge without opening each image.

    Layout is always ``<art_dir>/<slug>/<slug>_<key>.png`` — a per-card
    subdirectory so all variants for a card sit side by side.
    """
    slug = safe_slug(card.get("name") or "card")
    return art_dir / slug / f"{slug}_{variant_key}.png"


def _load_variant_styles(path: Path) -> list[dict]:
    """Load a ``--variant-styles`` JSON file.

    Expected shape: a non-empty JSON array of
    ``{"name": str, "style_anchor": str}`` objects.  The ``name`` is
    slugified into each output filename so ``Joe Grunt`` rendered under
    the ``"oil"`` style saves to ``joe_grunt/joe_grunt_oil.png``.  The
    ``style_anchor`` value replaces the card's
    ``art_description.style_anchor`` only for that variant's generation;
    the on-disk card JSON is never mutated, so the set's canonical
    anchor is preserved.

    Raises ``ValueError`` on any structural problem; the caller is
    expected to surface that through ``argparse``'s error path.
    """
    try:
        data = json.loads(path.read_text("utf-8"))
    except FileNotFoundError:
        raise ValueError(f"variant styles file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"variant styles file {path} is not valid JSON: {e}")
    if not isinstance(data, list) or not data:
        raise ValueError(
            f"variant styles file {path} must be a non-empty JSON array of "
            '{"name": ..., "style_anchor": ...} objects'
        )
    styles: list[dict] = []
    seen_keys: set[str] = set()
    for i, entry in enumerate(data, 1):
        if not isinstance(entry, dict):
            raise ValueError(
                f"variant style #{i} in {path} is not an object; each entry "
                'must be {"name": ..., "style_anchor": ...}'
            )
        name = (entry.get("name") or "").strip()
        anchor = (entry.get("style_anchor") or "").strip()
        if not name or not anchor:
            raise ValueError(
                f"variant style #{i} in {path} needs both 'name' and "
                "'style_anchor' fields"
            )
        key = safe_slug(name)
        if key in seen_keys:
            raise ValueError(
                f"variant style name '{name}' slugifies to '{key}' which is "
                f"already used by another entry in {path}; names must be "
                "unique after slugifying"
            )
        seen_keys.add(key)
        styles.append({"name": name, "key": key, "style_anchor": anchor})
    return styles


# ---------------------------------------------------------------------------
# Retry classification
# ---------------------------------------------------------------------------
#
# Transient errors worth retrying: rate limits, server errors, network
# hiccups, and "text-only" responses (the model occasionally returns a
# response with no image part, which usually succeeds on a retry).
#
# Not-retryable: safety-filter blocks and other 4xx client errors — the
# same prompt will produce the same failure, so retrying just wastes
# quota.  These win ties when a token appears in both lists.
_RETRYABLE_TOKENS = (
    "429", "resource_exhausted", "rate limit", "ratelimit",
    "500", "502", "503", "504",
    "internal", "unavailable", "deadline_exceeded",
    "timeout", "timed out",
    "connection reset", "connectionerror", "connection error",
    "no image part",
)

_NON_RETRYABLE_TOKENS = (
    "safety", "prohibited_content", "blocked_reason", "safety-filter",
    "permission_denied", "invalid_argument", "unauthenticated",
)


def _is_retryable(exc: BaseException) -> bool:
    msg_lower = f"{type(exc).__name__}: {exc}".lower()
    # Explicit non-retryable wins a collision (e.g. an "INVALID_ARGUMENT"
    # error that happens to mention "500" somewhere in its message).
    if any(tok in msg_lower for tok in _NON_RETRYABLE_TOKENS):
        return False
    # Prefer numeric HTTP status if the SDK attached one.
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    if isinstance(code, int):
        if code == 429 or 500 <= code < 600:
            return True
        if 400 <= code < 500:
            return False
    return any(tok in msg_lower for tok in _RETRYABLE_TOKENS)


def _with_retries(fn, *, retries: int, card_name: str):
    """Call ``fn()`` with exponential backoff on transient errors.

    ``retries`` is the number of *retry* attempts after the initial try,
    so ``retries=3`` means up to 4 total attempts.  Sleeps 2s, 4s, 8s,
    16s, 32s between attempts.  Retry notices go to stderr so they
    interleave cleanly with the main thread's stdout progress lines.
    """
    total_attempts = retries + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return fn()
        except Exception as e:
            if attempt >= total_attempts or not _is_retryable(e):
                raise
            sleep_s = min(2 ** attempt, 32)
            sys.stderr.write(
                f"    [retry] {card_name}: {type(e).__name__}: {e} — "
                f"sleeping {sleep_s}s before attempt "
                f"{attempt + 1}/{total_attempts}\n"
            )
            sys.stderr.flush()
            time.sleep(sleep_s)


def _iter_response_parts(resp):
    """Yield parts from a generate_content response, tolerating SDK shape drift.

    Newer ``google-genai`` releases expose ``response.parts`` as a shortcut to
    the first candidate's content parts; older ones only expose
    ``response.candidates[*].content.parts``.
    """
    parts = getattr(resp, "parts", None)
    if parts:
        yield from parts
        return
    for cand in getattr(resp, "candidates", None) or []:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", None) or []:
            yield part


def generate_one(client, types, card: dict, model: str,
                 image_size: str,
                 style_override: dict | None = None) -> Image.Image:
    prompt = build_prompt(card, style_override)
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=GEMINI_ASPECT,
                image_size=image_size,
            ),
        ),
    )
    for part in _iter_response_parts(resp):
        inline = getattr(part, "inline_data", None)
        if inline is not None and getattr(inline, "data", None):
            return Image.open(BytesIO(inline.data)).convert("RGB")
    # Neutral wording: we don't actually know whether the model was
    # filtered or just returned a text-only response.  Retry logic treats
    # "no image part" as transient; if it keeps happening after retries,
    # the prompt is likely the problem.
    raise RuntimeError(
        "no image part in response (may be a transient text-only "
        "response; retry is safe)"
    )


def load_cards(path: Path):
    data = json.loads(path.read_text("utf-8"))
    if isinstance(data, list):
        return {"kind": "list", "cards": data, "raw": data}
    if isinstance(data, dict):
        if "cards" in data:
            return {"kind": "object", "cards": data["cards"], "raw": data}
        return {"kind": "single", "cards": [data], "raw": data}
    raise ValueError(f"Unsupported JSON root: {type(data).__name__}")


def save_updated(parsed, out_path: Path):
    if parsed["kind"] == "list":
        data = parsed["cards"]
    elif parsed["kind"] == "object":
        parsed["raw"]["cards"] = parsed["cards"]
        data = parsed["raw"]
    else:
        data = parsed["cards"][0]
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), "utf-8")


def _card_matches_color(card: dict, filter_color: str) -> bool:
    fc = filter_color.upper()
    colors = card.get("color") or card.get("colors") or []
    if isinstance(colors, str):
        colors = [colors]
    return fc in [c.upper() for c in colors]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate MTG card art with Gemini Nano Banana and crop to the art box.",
    )
    ap.add_argument("input", nargs="?",
                    help="Path to JSON file with card data (single card, list, or set object)")
    ap.add_argument("--art-dir", default="./art",
                    help="Directory to save generated PNGs (default: ./art). "
                         "Each card gets a subdirectory with its variants, "
                         "e.g. ./art/joe_grunt/joe_grunt_1.png.")
    ap.add_argument("--variants", type=int, default=2,
                    help="Number of variants to generate per card "
                         "(default: 2). Nano Banana sometimes produces "
                         "weird compositions; generating multiple gives "
                         "the human a choice. The JSON's art_image field "
                         "defaults to variant 1; hand-edit to pick "
                         "another. Variants are independent API calls so "
                         "each is billed separately. Ignored when "
                         "--variant-styles is set (in that case the "
                         "styles-file length determines the variant "
                         "count).")
    ap.add_argument("--variant-styles", dest="variant_styles",
                    help="Path to a JSON file describing per-variant "
                         "artistic styles (e.g. oil painting, watercolor, "
                         "digital realism). Format: a non-empty array of "
                         "{\"name\": ..., \"style_anchor\": ...} objects. "
                         "Each entry's style_anchor replaces the card's "
                         "own style_anchor for that variant only — the "
                         "set's canonical anchor on disk is untouched. "
                         "The 'name' is slugified into the output "
                         "filename so Finder shows the style (e.g. "
                         "joe_grunt_oil.png). Overrides --variants. See "
                         "scripts/variant_styles.example.json for a "
                         "three-medium starter set.")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Gemini image model ID (default: {DEFAULT_MODEL}, Nano Banana 2). "
                         "Alternatives: gemini-3-pro-image-preview (Nano Banana Pro, "
                         "higher quality / slower / pricier), gemini-2.5-flash-image "
                         "(original Nano Banana)")
    ap.add_argument("--image-size", default="1K",
                    choices=["512", "1K", "2K", "4K"],
                    help="Gemini output resolution before cropping (default: 1K)")
    ap.add_argument("--update-json", action="store_true",
                    help="Write art_image paths back into the input JSON")
    ap.add_argument("--out-json",
                    help="Write updated JSON to this path (implies --update-json)")
    ap.add_argument("--force", action="store_true",
                    help="Regenerate even if art_image is already set and the file exists")
    ap.add_argument("--filter-rarity",
                    help="Only generate for cards of this rarity")
    ap.add_argument("--filter-color",
                    help="Only generate for cards containing this color (W/U/B/R/G)")
    ap.add_argument("--limit", type=int,
                    help="Maximum number of cards to process. Each card "
                         "still generates --variants images, so the total "
                         "API call count is --limit × --variants.")
    ap.add_argument("--concurrency", type=int, default=4,
                    help="Number of images to generate in parallel "
                         "(default: 4). Set to 1 for strictly serial. "
                         "Higher values speed up large sets but risk 429 "
                         "rate-limit errors — Nano Banana 2 free tier is "
                         "roughly 10 RPM, paid tier much higher.")
    ap.add_argument("--retries", type=int, default=3,
                    help="Retry attempts per card on transient errors "
                         "(default: 3). Retried: 429 rate limits, 5xx "
                         "server errors, network timeouts, text-only "
                         "responses. Not retried: safety-filter blocks "
                         "and other 4xx client errors. Backoff: 2s, 4s, "
                         "8s, 16s, 32s.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the prompts that would be sent and exit")

    ap.add_argument("--single", action="store_true",
                    help="One-off mode: generate a single image from CLI args")
    ap.add_argument("--name", help="Card name (for --single)")
    ap.add_argument("--art-direction", dest="art_direction",
                    help="Art direction text (for --single)")
    ap.add_argument("--type", dest="card_type",
                    help="Type line (for --single, optional)")

    args = ap.parse_args()

    # --- Build the work list ---------------------------------------------
    parsed = None
    input_path: Path | None = None

    if args.single:
        if not (args.name and args.art_direction):
            ap.error("--single requires --name and --art-direction")
        cards = [{
            "name": args.name,
            "art_direction": args.art_direction,
            "type": args.card_type,
        }]
    elif args.input:
        input_path = Path(args.input).resolve()
        parsed = load_cards(input_path)
        cards = parsed["cards"]
    else:
        ap.error("provide a JSON file path or use --single mode")
        return

    if args.filter_rarity:
        cards = [c for c in cards
                 if str(c.get("rarity", "")).lower() == args.filter_rarity.lower()]
    if args.filter_color:
        cards = [c for c in cards if _card_matches_color(c, args.filter_color)]

    art_dir = Path(args.art_dir).resolve()
    art_dir.mkdir(parents=True, exist_ok=True)

    # Resolve variant mode.  With --variant-styles the styles file is the
    # source of truth for both count and per-variant style_anchor; without
    # it we fall back to N identically-styled variants.
    variant_styles: list[dict] | None = None
    if args.variant_styles:
        try:
            variant_styles = _load_variant_styles(Path(args.variant_styles))
        except ValueError as e:
            ap.error(str(e))
            return

    if variant_styles:
        variant_keys = [s["key"] for s in variant_styles]
        style_by_key = {s["key"]: s for s in variant_styles}
    else:
        variants_per_card = max(1, args.variants)
        variant_keys = [str(v) for v in range(1, variants_per_card + 1)]
        style_by_key = {}
    variant_count = len(variant_keys)

    # Which cards have a prompt at all?  Used both for the work queue and
    # for the post-pass that points art_image at a real variant file.
    promptable_cards = [c for c in cards if build_prompt(c)]

    # Expand each card into (card, variant_key) tasks. Variants whose PNG
    # already exists on disk are announced and skipped (unless --force).
    to_generate: list[tuple[dict, str]] = []
    cards_with_work: list[dict] = []
    seen_with_work: set[int] = set()
    for c in promptable_cards:
        name = c.get("name") or "card"
        for key in variant_keys:
            out_path = _variant_path(art_dir, c, key)
            if out_path.is_file() and not args.force:
                print(f"  [skip] {name} {key} — already on disk: {out_path}")
                continue
            if id(c) not in seen_with_work:
                seen_with_work.add(id(c))
                cards_with_work.append(c)
            to_generate.append((c, key))

    if args.limit:
        kept_ids = {id(c) for c in cards_with_work[: args.limit]}
        to_generate = [(c, k) for (c, k) in to_generate if id(c) in kept_ids]

    if not to_generate:
        print("No cards need art generation (use --force to regenerate).")
        # Still run the art_image post-pass so existing files get linked up.
        _update_art_image_paths(promptable_cards, art_dir, variant_keys)
        _maybe_persist_json(parsed, input_path, args)
        return

    # --- Dry run ---------------------------------------------------------
    if args.dry_run:
        card_count = len({id(c) for c, _ in to_generate})
        style_note = (
            f", styles: {', '.join(s['name'] for s in variant_styles)}"
            if variant_styles else ""
        )
        print(f"[dry-run] Would generate {len(to_generate)} image(s) "
              f"({card_count} card(s) × up to {variant_count} variant(s)"
              f"{style_note}) with {args.model} at {args.image_size}, "
              f"aspect {GEMINI_ASPECT}, cropped to "
              f"{ART_BOX_W_MM:.0f}:{ART_BOX_H_MM:.0f}.")
        if variant_styles:
            # In style mode, print one prompt per (card, style) combination
            # so the human can inspect exactly how each style rewrites the
            # prompt.  Without this, all three medium variants would render
            # as a single line and the diff would be invisible.
            seen_pairs: set[tuple[int, str]] = set()
            for c, key in to_generate:
                pair = (id(c), key)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                prompt = build_prompt(c, style_by_key[key]).replace("\n", " ")
                print(f"  - {c.get('name', '<unnamed>')} [{key}]: "
                      f"{prompt[:140]}...")
        else:
            shown: set[int] = set()
            for c, _ in to_generate:
                if id(c) in shown:
                    continue
                shown.add(id(c))
                prompt = build_prompt(c).replace("\n", " ")
                print(f"  - {c.get('name', '<unnamed>')}: {prompt[:140]}...")
        return

    # --- Generate --------------------------------------------------------
    genai, types = _load_genai()
    client = genai.Client(api_key=_api_key())

    failures: list[tuple[str, str]] = []
    total = len(to_generate)
    concurrency = max(1, args.concurrency)

    def worker(task: tuple[dict, str]) -> dict:
        """Generate, crop, and save one variant of one card.

        Returns a small dict the main thread prints.  Raises on any failure —
        the main thread's ``future.exception()`` collects it.  Workers never
        mutate ``card["art_image"]``; the main-thread post-pass does that
        after all generations complete, so the final pointer is deterministic
        even when variants finish out of order or some fail.
        """
        card, variant_key = task
        name = card.get("name") or "card"
        out_path = _variant_path(art_dir, card, variant_key)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        style_override = style_by_key.get(variant_key)
        t0 = time.monotonic()
        raw_img = _with_retries(
            lambda: generate_one(
                client, types, card,
                model=args.model,
                image_size=args.image_size,
                style_override=style_override,
            ),
            retries=args.retries,
            card_name=f"{name} {variant_key}",
        )
        cropped = crop_to_art_box(raw_img)
        cropped.save(out_path, "PNG")
        return {
            "name": name,
            "variant_key": variant_key,
            "out_path": out_path,
            "size": cropped.size,
            "elapsed": time.monotonic() - t0,
        }

    if concurrency == 1:
        print(f"Generating {total} image(s) with {args.model} "
              f"at {args.image_size} "
              f"({variant_count} variant(s) per card)...")
        for i, task in enumerate(to_generate, 1):
            card, variant_key = task
            name = card.get("name") or f"card_{i}"
            # Show progress *before* the API call — single-threaded mode
            # would otherwise sit silent for 20-30 s per image.
            print(f"  [{i}/{total}] {name} {variant_key} ... ",
                  end="", flush=True)
            try:
                r = worker(task)
                print(f"-> {r['out_path']} ({r['size'][0]}x{r['size'][1]}) "
                      f"in {r['elapsed']:.1f}s", flush=True)
            except Exception as e:
                print("FAILED", flush=True)
                sys.stderr.write(
                    f"    [{i}/{total}] {name} {variant_key}: {e}\n")
                failures.append((f"{name} {variant_key}", str(e)))
    else:
        print(f"Generating {total} image(s) with {args.model} "
              f"at {args.image_size} "
              f"({variant_count} variant(s) per card, "
              f"concurrency={concurrency})...")
        done = 0
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = {ex.submit(worker, task): task for task in to_generate}
            for fut in as_completed(futures):
                card, variant_key = futures[fut]
                name = card.get("name") or "card"
                done += 1
                try:
                    r = fut.result()
                    print(f"  [{done}/{total}] {r['name']} "
                          f"{r['variant_key']} -> {r['out_path']} "
                          f"({r['size'][0]}x{r['size'][1]}) "
                          f"in {r['elapsed']:.1f}s", flush=True)
                except Exception as e:
                    print(f"  [{done}/{total}] {name} {variant_key} "
                          f"FAILED: {e}", flush=True)
                    sys.stderr.write(f"    {name} {variant_key}: {e}\n")
                    failures.append((f"{name} {variant_key}", str(e)))

    # --- Point art_image at a real variant file --------------------------
    _update_art_image_paths(promptable_cards, art_dir, variant_keys)

    # --- Persist JSON ----------------------------------------------------
    _maybe_persist_json(parsed, input_path, args)

    succeeded = total - len(failures)
    print(f"Done. {succeeded}/{total} image(s) succeeded.")
    if variant_count > 1:
        if variant_styles:
            style_list = ", ".join(s["name"] for s in variant_styles)
            default_style = variant_styles[0]["name"]
            print(
                f"Variants are under {art_dir}/<card_slug>/ — one per style "
                f"({style_list}). Open a card's folder in Finder to Quick "
                f"Look through them. Each card's art_image defaults to the "
                f"first style ({default_style}); to pick another, edit the "
                f"card's \"art_image\" field in the JSON to point at "
                f"<slug>_<style>.png (e.g. _watercolor.png)."
            )
        else:
            print(
                f"Variants are under {art_dir}/<card_slug>/ — open a card's "
                f"folder in Finder to compare all {variant_count} side by "
                f"side. Each card's art_image defaults to variant 1; to pick "
                f"a different variant, edit the card's \"art_image\" field "
                f"in the JSON to point at _2.png, _3.png, etc."
            )
    if failures:
        sys.exit(1)


def _update_art_image_paths(cards: list[dict], art_dir: Path,
                             variant_keys: list[str]) -> None:
    """Ensure each card's ``art_image`` points at a real variant file.

    Only runs in the main thread, after all workers complete.  Rules:

    * If the card's current ``art_image`` already points at an existing
      file, leave it alone — the human may have hand-picked a specific
      variant and we don't want to clobber that.
    * Otherwise, set ``art_image`` to the first variant in
      ``variant_keys`` order whose PNG exists on disk.  Handles partial
      failures gracefully: if the first style/index was blocked but a
      later one succeeded, the card still gets a valid pointer to the
      earliest surviving variant.
    * If no variant file exists, leave ``art_image`` untouched.
    """
    for c in cards:
        current = c.get("art_image")
        if current and os.path.isfile(current):
            continue
        for key in variant_keys:
            p = _variant_path(art_dir, c, key)
            if p.is_file():
                c["art_image"] = str(p)
                break


def _maybe_persist_json(parsed, input_path: Path | None, args) -> None:
    if parsed is None:
        return
    if not (args.update_json or args.out_json):
        return
    target = Path(args.out_json).resolve() if args.out_json else input_path
    save_updated(parsed, target)
    print(f"Updated JSON written to {target}")


if __name__ == "__main__":
    main()
