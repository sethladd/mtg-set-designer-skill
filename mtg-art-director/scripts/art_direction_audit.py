#!/usr/bin/env python3
"""
art_direction_audit.py - MTG card art description audit.

Usage:
    python art_direction_audit.py path/to/set.json [--out art_direction_report.md]

Checks:
  1. Completeness — every card has an art_description with all 5 fields
  2. Field quality — scene length, focus brevity, mood word count, palette colors, frame specificity
  3. Mechanical readability — keywords cross-referenced with required visual cues
  4. Color identity alignment — palette colors vs. card color identity
  5. Scene specificity — flags generic/vague descriptions
  6. Focus singularity — flags descriptions with competing focal points
  7. Visual diversity — flags near-duplicate scenes across the set
  8. Frame variety — flags overuse of the same framing type
  9. UB consistency — checks canonical character references (if applicable)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# --- Constants ---

ART_FIELDS = ("scene", "focus", "mood", "palette", "frame")

SCENE_MIN_WORDS = 15
FOCUS_MAX_WORDS = 8
MOOD_MIN_WORDS = 2
MOOD_MAX_WORDS = 5

# Mechanical readability: keyword -> words that should appear in the scene or focus
MECHANIC_VISUAL_CUES: dict[str, list[str]] = {
    "flying": ["airborne", "soar", "wing", "flight", "fly", "flying", "aerial",
               "sky", "cloud", "hover", "glide", "dive", "swoop", "mid-air"],
    "reach": ["reach", "long", "extend", "stretch", "vine", "tendril", "web",
              "ranged", "bow", "spear", "thrown", "tentacle", "tall", "towering"],
    "first strike": ["lunge", "strike", "thrust", "speed", "quick", "fast",
                     "swift", "lance", "charge", "first", "slash"],
    "double strike": ["dual", "twin", "two", "double", "blur", "flurry",
                      "rapid", "both"],
    "vigilance": ["alert", "vigil", "watch", "guard", "ready", "scan",
                  "sentinel", "unwavering", "tireless", "patrol"],
    "deathtouch": ["venom", "poison", "toxic", "lethal", "death", "wither",
                   "necrotic", "decay", "blight", "drip", "fangs", "sting"],
    "lifelink": ["radiant", "heal", "life", "drain", "vitality", "glow",
                 "restore", "siphon", "light", "energy", "absorb"],
    "trample": ["massive", "colossal", "unstoppable", "crush", "smash",
                "thunder", "quake", "stomp", "towering", "charge", "enormous"],
    "haste": ["blur", "speed", "rush", "burst", "sprint", "dash", "sudden",
              "explosive", "momentum", "quick", "rapid", "urgency"],
    "menace": ["terrif", "menac", "fear", "dread", "loom", "intimidat",
               "nightmare", "horror", "multiple", "overwhelming"],
    "defender": ["wall", "barrier", "immov", "root", "shield", "block",
                 "fortif", "bulwark", "bastion", "unyielding"],
    "flash": ["sudden", "burst", "appear", "materialize", "surprise",
              "instant", "flash", "emerge", "snap"],
    "ward": ["barrier", "shield", "ward", "protect", "rune", "deflect",
             "aura", "shimmer", "repel"],
    "hexproof": ["shimmer", "untouchable", "ethereal", "phase", "intangible",
                 "aura", "impervious", "slide"],
    "indestructible": ["unyielding", "invulnerable", "unbreakable", "divine",
                       "eternal", "adamant", "impervious", "indestructible"],
}

# Color identity -> palette colors that SHOULD appear
COLOR_PALETTE_MAP: dict[str, list[str]] = {
    "W": ["white", "gold", "golden", "bright", "sunlit", "warm", "light",
          "ivory", "cream", "amber", "radiant", "silver", "clean"],
    "U": ["blue", "cool", "silver", "ice", "frost", "azure", "cerulean",
          "sapphire", "teal", "moonlit", "aqua", "indigo", "steel"],
    "B": ["black", "dark", "shadow", "purple", "grey", "sickly", "green",
          "crimson", "obsidian", "bone", "smoke", "ash", "violet"],
    "R": ["red", "orange", "fire", "flame", "crimson", "ember", "scarlet",
          "rust", "copper", "volcanic", "molten", "amber", "warm"],
    "G": ["green", "brown", "emerald", "verdant", "moss", "earth", "jade",
          "olive", "forest", "vine", "natural", "wood", "bark"],
}

# Colors that CONTRADICT a card's identity
COLOR_CONTRADICTIONS: dict[str, list[str]] = {
    "W": ["sickly", "shadow", "decay", "dark purpl", "obsidian"],
    "U": ["volcanic", "molten", "fire", "flame", "ember"],
    "B": ["bright sunl", "radiant gold", "clean white", "verdant"],
    "R": ["cool blue", "frost", "ice", "moonlit silver", "cerulean"],
    "G": ["obsidian", "shadow", "sickly", "bone white"],
}

# Generic/vague scene patterns
GENERIC_PATTERNS = [
    r"a (warrior|soldier|mage|wizard|creature) (fights|attacks|battles|stands)",
    r"a (magical|mystical|powerful) (spell|energy|force)",
    r"a (dark|bright|mysterious) (figure|shape|form)",
    r"someone (casting|doing|using) (magic|a spell)",
    r"^a creature in",
    r"^a person ",
]

# Frame types for variety tracking
FRAME_TYPES = {
    "close-up": ["close-up", "close up", "closeup", "tight shot", "portrait"],
    "medium": ["medium shot", "medium", "mid-shot", "waist-up", "half-body"],
    "wide": ["wide shot", "wide", "full body", "establishing", "full-body"],
    "extreme wide": ["extreme wide", "panoramic", "landscape", "vista"],
    "low angle": ["low angle", "worm's eye", "looking up", "from below"],
    "high angle": ["high angle", "bird's eye", "looking down", "from above", "aerial"],
    "dutch": ["dutch", "tilted", "canted", "angled"],
}

FRAME_VARIETY_THRESHOLD = 0.40  # warn if >40% same frame type


# --- Helpers ---

def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def card_colors(card: dict) -> list[str]:
    """Return the card's color identity as a list of single-letter codes."""
    colors = card.get("color", [])
    if isinstance(colors, str):
        colors = list(colors)
    return [c.upper() for c in colors]


def card_keywords(card: dict) -> list[str]:
    """Extract keywords from a card."""
    keywords = card.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [keywords]
    # Also check rules_text for keyword mentions
    rules = (card.get("rules_text") or "").lower()
    all_kw = [k.lower().strip() for k in keywords]
    for kw in MECHANIC_VISUAL_CUES:
        if kw in rules and kw not in all_kw:
            all_kw.append(kw)
    return all_kw


def word_count(text: str) -> int:
    return len(text.split()) if text.strip() else 0


def scene_text(card: dict) -> str:
    ad = card.get("art_description", {})
    if isinstance(ad, dict):
        return (ad.get("scene") or "").lower()
    return ""


def classify_frame(frame: str) -> str | None:
    frame_lower = frame.lower()
    for frame_type, patterns in FRAME_TYPES.items():
        for p in patterns:
            if p in frame_lower:
                return frame_type
    return "other"


# --- Checks ---

def check_completeness(cards: list[dict]) -> list[str]:
    """Check 1: Every card has art_description with all 5 fields."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description")
        if not ad or not isinstance(ad, dict):
            flags.append(f"ART-MISSING: {name} has no art_description")
            continue
        for field in ART_FIELDS:
            val = ad.get(field, "").strip() if isinstance(ad.get(field), str) else ""
            if not val:
                flags.append(f"FIELD-MISSING: {name} missing art_description.{field}")
    return flags


def check_field_quality(cards: list[dict]) -> list[str]:
    """Check 2: Field values meet quality thresholds."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue

        scene = ad.get("scene", "")
        focus = ad.get("focus", "")
        mood = ad.get("mood", "")
        palette = ad.get("palette", "")
        frame = ad.get("frame", "")

        if scene and word_count(scene) < SCENE_MIN_WORDS:
            flags.append(
                f"SCENE-SHORT: {name} scene is {word_count(scene)} words "
                f"(minimum {SCENE_MIN_WORDS})"
            )
        if focus and word_count(focus) > FOCUS_MAX_WORDS:
            flags.append(
                f"FOCUS-LONG: {name} focus is {word_count(focus)} words "
                f"(maximum {FOCUS_MAX_WORDS})"
            )
        if mood:
            wc = word_count(mood)
            if wc < MOOD_MIN_WORDS or wc > MOOD_MAX_WORDS:
                flags.append(
                    f"MOOD-LENGTH: {name} mood is {wc} words "
                    f"(expected {MOOD_MIN_WORDS}-{MOOD_MAX_WORDS})"
                )
        if frame and not any(
            p in frame.lower()
            for patterns in FRAME_TYPES.values()
            for p in patterns
        ):
            flags.append(
                f"FRAME-VAGUE: {name} frame '{frame}' doesn't specify "
                f"a recognizable shot type or angle"
            )
    return flags


def check_mechanical_readability(cards: list[dict]) -> list[str]:
    """Check 3: Keywords cross-referenced with visual cues in scene/focus."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue

        combined_text = (
            (ad.get("scene") or "") + " " + (ad.get("focus") or "")
        ).lower()
        if not combined_text.strip():
            continue

        for kw in card_keywords(c):
            cues = MECHANIC_VISUAL_CUES.get(kw)
            if not cues:
                continue
            if not any(cue in combined_text for cue in cues):
                flags.append(
                    f"MECH-MISMATCH: {name} has '{kw}' but art description "
                    f"lacks visual cues ({', '.join(cues[:5])}...)"
                )
    return flags


def check_color_alignment(cards: list[dict]) -> list[str]:
    """Check 4: Palette colors align with card color identity."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue

        palette = (ad.get("palette") or "").lower()
        if not palette:
            continue

        colors = card_colors(c)
        if not colors:
            continue  # colorless cards have no alignment requirement

        # Check for contradictions
        for color in colors:
            contradictions = COLOR_CONTRADICTIONS.get(color, [])
            for contra in contradictions:
                if contra in palette:
                    flags.append(
                        f"COLOR-CLASH: {name} ({color}) palette contains "
                        f"contradictory '{contra}'"
                    )
    return flags


def check_scene_specificity(cards: list[dict]) -> list[str]:
    """Check 5: Flag generic/vague scene descriptions."""
    flags: list[str] = []
    compiled = [re.compile(p, re.IGNORECASE) for p in GENERIC_PATTERNS]
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue

        scene = ad.get("scene", "")
        if not scene:
            continue
        for pattern in compiled:
            if pattern.search(scene):
                flags.append(
                    f"SCENE-GENERIC: {name} scene uses generic phrasing: "
                    f"'{scene[:60]}...'"
                )
                break
    return flags


def check_focus_singularity(cards: list[dict]) -> list[str]:
    """Check 6: Flag focus fields with multiple competing subjects."""
    flags: list[str] = []
    # Patterns that suggest multiple focal points
    split_patterns = [
        r"\band\b",
        r"\bwith\b.*\band\b",
        r",\s*\w+\s+and\b",
    ]
    compiled = [re.compile(p, re.IGNORECASE) for p in split_patterns]
    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue

        focus = ad.get("focus", "")
        if not focus:
            continue
        # Simple "and" check for competing focal points
        if re.search(r"\band\b", focus, re.IGNORECASE):
            flags.append(
                f"FOCUS-SPLIT: {name} focus has competing subjects: '{focus}'"
            )
    return flags


def check_visual_diversity(cards: list[dict]) -> list[str]:
    """Check 7: Flag near-duplicate scenes using keyword overlap."""
    flags: list[str] = []
    scenes: list[tuple[str, set[str]]] = []

    for c in cards:
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue
        scene = ad.get("scene", "")
        if not scene:
            continue
        # Extract meaningful words (skip common stop words)
        stop_words = {
            "a", "an", "the", "in", "on", "at", "of", "to", "and", "or",
            "is", "are", "was", "were", "its", "their", "this", "that",
            "with", "from", "by", "as", "for", "it", "be", "has", "have",
        }
        words = {
            w.lower().strip(".,;:!?")
            for w in scene.split()
            if w.lower().strip(".,;:!?") not in stop_words and len(w) > 2
        }
        scenes.append((name, words))

    # Compare all pairs
    seen_pairs: set[tuple[str, str]] = set()
    for i, (name_a, words_a) in enumerate(scenes):
        for j, (name_b, words_b) in enumerate(scenes):
            if i >= j:
                continue
            pair = (name_a, name_b)
            if pair in seen_pairs:
                continue
            if not words_a or not words_b:
                continue
            overlap = words_a & words_b
            union = words_a | words_b
            similarity = len(overlap) / len(union) if union else 0
            if similarity > 0.60:
                seen_pairs.add(pair)
                flags.append(
                    f"SCENE-DUPLICATE: {name_a} and {name_b} have "
                    f"{similarity:.0%} scene overlap"
                )
    return flags


def check_frame_variety(cards: list[dict]) -> list[str]:
    """Check 8: Flag overuse of the same framing type."""
    flags: list[str] = []
    frame_counts: Counter[str] = Counter()
    total = 0

    for c in cards:
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue
        frame = ad.get("frame", "")
        if not frame:
            continue
        total += 1
        frame_type = classify_frame(frame)
        if frame_type:
            frame_counts[frame_type] += 1

    if total == 0:
        return flags

    for frame_type, count in frame_counts.items():
        ratio = count / total
        if ratio > FRAME_VARIETY_THRESHOLD and frame_type != "other":
            flags.append(
                f"FRAME-MONOTONY: {frame_type} framing used for "
                f"{count}/{total} cards ({ratio:.0%}, threshold {FRAME_VARIETY_THRESHOLD:.0%})"
            )

    # Also flag if fewer than 3 distinct frame types are used
    distinct = len([k for k in frame_counts if k != "other"])
    if total >= 20 and distinct < 3:
        flags.append(
            f"FRAME-LOW-VARIETY: Only {distinct} distinct frame types "
            f"across {total} cards (recommend ≥3)"
        )

    return flags


def check_ub_consistency(cards: list[dict], is_ub: bool) -> list[str]:
    """Check 9: UB sets should reference canonical visual descriptions."""
    if not is_ub:
        return []
    flags: list[str] = []
    # Check legendary creatures for canonical reference anchoring
    for c in cards:
        card_t = (c.get("type") or "").lower()
        if "legendary" not in card_t:
            continue
        if "creature" not in card_t and "planeswalker" not in card_t:
            continue
        name = c.get("name", c.get("id", "???"))
        ad = c.get("art_description", {})
        if not isinstance(ad, dict):
            continue
        scene = (ad.get("scene") or "").lower()
        # Check for canonical anchoring phrases
        anchors = ["as depicted", "canonical", "from the", "as seen in",
                    "faithful to", "recognizable", "iconic", "signature"]
        if not any(a in scene for a in anchors):
            flags.append(
                f"UB-UNANCHORED: Legendary {name} scene lacks canonical "
                f"reference anchoring (add 'as depicted in...' or similar)"
            )
    return flags


# --- Report ---

def audit_set(set_data: dict, is_ub: bool = False) -> str:
    cards = set_data.get("cards", [])
    if not cards:
        return "# Art Direction Audit\n\nNo cards found in set data.\n"

    out: list[str] = []
    all_flags: list[str] = []

    out.append("# Art Direction Audit Report")
    out.append(f"\nSet: {set_data.get('set_name', 'Unknown')}")
    out.append(f"Cards audited: {len(cards)}")
    out.append("")

    checks = [
        ("Completeness", check_completeness(cards)),
        ("Field Quality", check_field_quality(cards)),
        ("Mechanical Readability", check_mechanical_readability(cards)),
        ("Color Identity Alignment", check_color_alignment(cards)),
        ("Scene Specificity", check_scene_specificity(cards)),
        ("Focus Singularity", check_focus_singularity(cards)),
        ("Visual Diversity", check_visual_diversity(cards)),
        ("Frame Variety", check_frame_variety(cards)),
        ("UB Consistency", check_ub_consistency(cards, is_ub)),
    ]

    for name, flags in checks:
        out.append(f"## {name}")
        if flags:
            out.append(f"**{len(flags)} flags:**")
            for f in flags:
                out.append(f"- {f}")
            all_flags.extend(flags)
        else:
            out.append("✓ No issues detected.")
        out.append("")

    # Statistics
    out.append("## Statistics")
    total = len(cards)
    with_art = sum(
        1 for c in cards
        if isinstance(c.get("art_description"), dict)
        and all(c["art_description"].get(f) for f in ART_FIELDS)
    )
    out.append(f"- Cards with complete art descriptions: {with_art}/{total} "
               f"({with_art/total:.0%})")

    # Frame type distribution
    frame_counts: Counter[str] = Counter()
    for c in cards:
        ad = c.get("art_description", {})
        if isinstance(ad, dict) and ad.get("frame"):
            ft = classify_frame(ad["frame"])
            if ft:
                frame_counts[ft] += 1
    if frame_counts:
        out.append("- Frame type distribution:")
        for ft, count in frame_counts.most_common():
            out.append(f"  - {ft}: {count}")

    # Keyword coverage
    kw_total = 0
    kw_matched = 0
    for c in cards:
        for kw in card_keywords(c):
            if kw in MECHANIC_VISUAL_CUES:
                kw_total += 1
                ad = c.get("art_description", {})
                if isinstance(ad, dict):
                    combined = (
                        (ad.get("scene") or "") + " " + (ad.get("focus") or "")
                    ).lower()
                    if any(cue in combined
                           for cue in MECHANIC_VISUAL_CUES[kw]):
                        kw_matched += 1
    if kw_total:
        out.append(f"- Mechanical readability: {kw_matched}/{kw_total} "
                   f"keywords have visual cues ({kw_matched/kw_total:.0%})")
    out.append("")

    # Summary
    out.append("## Summary")
    if all_flags:
        categories: dict[str, int] = defaultdict(int)
        for f in all_flags:
            cat = f.split(":")[0]
            categories[cat] += 1
        out.append(f"**{len(all_flags)} total flags:**")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            out.append(f"- {cat}: {count}")
    else:
        out.append("✓ No issues detected. Art direction passes audit.")
    out.append("")
    return "\n".join(out)


# --- CLI ---

def main() -> int:
    ap = argparse.ArgumentParser(description="MTG art direction audit")
    ap.add_argument("set_path", type=Path, help="Path to set.json")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output report path (default: stdout)")
    ap.add_argument("--ub", action="store_true",
                    help="Enable Universes Beyond consistency checks")
    args = ap.parse_args()

    set_data = load_set(args.set_path)
    report = audit_set(set_data, is_ub=args.ub)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
