#!/usr/bin/env python3
"""
balance_check.py - Heuristic balance checker for an MTG set file.

Usage:
    python balance_check.py path/to/set.json [--out balance_report.md]

Reads a set.json produced by the mtg-set-designer skill and writes a markdown
report flagging deviations from the heuristic targets documented in
references/balance-heuristics.md.

The checker is deliberately conservative: it flags things for the designer's
attention; it does not fail the set. Judgment calls belong to the designer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


COLORS = ["W", "U", "B", "R", "G"]
RARITIES = ["common", "uncommon", "rare", "mythic"]

# Target card counts per color (Play Booster era, 2024+). See references/rarity-structure.md.
TARGET_COMMONS_PER_COLOR = 14  # 81 total / 5 colors ≈ 14-15 + colorless
TARGET_UNCOMMONS_PER_COLOR = 17  # 100 total / 5 colors ≈ 16-18 + gold/colorless
TARGET_RARES_PER_COLOR = 10
TARGET_MYTHICS_PER_COLOR = 4

# New World Order: max fraction of red-flagged commons.
NWO_RED_FLAG_MAX = 0.20

# Archetype support: commons+uncommons that plausibly support each archetype.
ARCHETYPE_SUPPORT_MIN = 22  # ~14-16 commons + ~8-12 uncommons per archetype

# Removal density heuristic patterns.
REMOVAL_PATTERNS = [
    r"destroy target (creature|permanent)",
    r"exile target (creature|permanent)",
    r"deals? \d+ damage to (any target|target creature|target player)",
    r"target creature gets -\d+/-\d+",
    r"target creature (you don't control )?can't block",
    r"return target (creature|nonland permanent) to its owner'?s? hand",
    r"counter target spell",
    r"fights? target creature",
    r"sacrifices? a creature",
]

# Color pie check: very rough regex-based flags for potential violations.
# These are *warnings*, not errors — the tool cannot tell a bend from a break.
COLOR_PIE_ALARMS = {
    # Blue shouldn't get unconditional creature kill.
    "U": [r"destroy target creature(?! with)", r"exile target creature(?! with)"],
    # Red shouldn't get enchantment removal or card draw.
    "R": [r"destroy target enchantment", r"draw (two|three|\d+) cards?"],
    # Green shouldn't get direct damage (non-fight) or counterspells.
    "G": [r"counter target spell", r"deals? \d+ damage to any target(?! creature)"],
    # White shouldn't get raw card draw without a condition.
    "W": [r"^draw (two|three|\d+) cards?$"],
    # Black has few restrictions in common forms, but note enchantment removal.
    "B": [r"destroy target enchantment(?! you)"],
}


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def is_creature(card: dict) -> bool:
    return "Creature" in card.get("type", "")


def primary_color(card: dict) -> str:
    colors = card.get("color", [])
    if not colors:
        return "C"
    if len(colors) > 1:
        return "M"  # multicolor
    return colors[0]


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def is_red_flag_common(card: dict) -> bool:
    """Apply New World Order red-flag heuristics. Returns True if the common is flagged as complex."""
    if rarity(card) != "common":
        return False
    text = card.get("rules_text", "") or ""
    if not text.strip():
        return False

    reasons = 0
    # More than ~3 lines of rules text.
    if len(text) > 120:
        reasons += 1
    # Triggered abilities beyond simple ETB.
    if re.search(r"\bwhenever\b|\bat the beginning\b", text, re.IGNORECASE):
        reasons += 1
    # Multiple distinct abilities (very rough: count semicolons or newlines).
    ability_breaks = text.count("\n") + text.count(";")
    if ability_breaks >= 2:
        reasons += 1
    # New (non-evergreen) named mechanic reference - crude proxy: capitalized words not in evergreen list.
    evergreens = {
        "Flying", "First", "Double", "Deathtouch", "Defender", "Haste", "Hexproof",
        "Indestructible", "Lifelink", "Menace", "Reach", "Trample", "Vigilance",
        "Ward", "Flash", "Scry", "Prowess",
    }
    keywords = card.get("keywords", []) or []
    non_evergreen_kw = [k for k in keywords if k not in evergreens]
    if len(non_evergreen_kw) >= 1:
        reasons += 1
    return reasons >= 2


def is_removal(card: dict) -> bool:
    text = (card.get("rules_text") or "").lower()
    return any(re.search(p, text) for p in REMOVAL_PATTERNS)


def color_pie_alarms(card: dict) -> list[str]:
    text = (card.get("rules_text") or "").lower()
    alarms = []
    for color in card.get("color", []):
        for pattern in COLOR_PIE_ALARMS.get(color, []):
            if re.search(pattern, text):
                alarms.append(f"{card.get('name', '?')} ({color}): matches pattern /{pattern}/")
    return alarms


def creature_curve(cards: list[dict], color: str) -> dict[int, int]:
    curve: dict[int, int] = defaultdict(int)
    for c in cards:
        if not is_creature(c):
            continue
        if primary_color(c) != color:
            continue
        if rarity(c) != "common":
            continue
        cmc = c.get("cmc", 0)
        curve[cmc] += 1
    return dict(curve)


def check_set(set_data: dict) -> str:
    cards = set_data.get("cards", [])
    archetypes = set_data.get("archetypes", {})
    mechanics = set_data.get("mechanics", [])

    out: list[str] = []
    out.append(f"# Balance Report: {set_data.get('set_name', 'Unnamed Set')}")
    out.append(f"Total cards: **{len(cards)}**")
    out.append("")

    # --- Rarity distribution ---
    out.append("## Rarity distribution")
    by_rarity: dict[str, int] = defaultdict(int)
    for c in cards:
        by_rarity[rarity(c)] += 1
    for r in RARITIES:
        out.append(f"- {r}: {by_rarity.get(r, 0)}")
    out.append("")

    # --- Color distribution per rarity ---
    out.append("## Color distribution by rarity")
    out.append("| Rarity | W | U | B | R | G | Multi | Colorless |")
    out.append("|---|---|---|---|---|---|---|---|")
    for r in RARITIES:
        row = {k: 0 for k in COLORS + ["M", "C"]}
        for c in cards:
            if rarity(c) != r:
                continue
            row[primary_color(c)] += 1
        out.append(
            f"| {r} | {row['W']} | {row['U']} | {row['B']} | {row['R']} | {row['G']} | {row['M']} | {row['C']} |"
        )
    out.append("")

    # Flag color imbalance at common
    common_by_color = {
        color: sum(1 for c in cards if primary_color(c) == color and rarity(c) == "common")
        for color in COLORS
    }
    avg = sum(common_by_color.values()) / 5 if common_by_color else 0
    out.append("### Common color balance")
    warnings = []
    for color, count in common_by_color.items():
        delta = count - avg
        flag = " ⚠️" if abs(delta) > 3 else ""
        out.append(f"- {color}: {count} commons (avg {avg:.1f}){flag}")
        if abs(delta) > 3:
            warnings.append(f"Color {color} commons deviate from average by {delta:+.1f}")
    out.append("")

    # --- New World Order check ---
    commons = [c for c in cards if rarity(c) == "common"]
    red_flagged = [c for c in commons if is_red_flag_common(c)]
    rf_ratio = len(red_flagged) / len(commons) if commons else 0
    out.append("## New World Order (complexity at common)")
    out.append(f"- Commons: {len(commons)}")
    out.append(f"- Red-flagged as complex: {len(red_flagged)} ({rf_ratio:.0%})")
    out.append(f"- Target: ≤{int(NWO_RED_FLAG_MAX * 100)}%")
    if rf_ratio > NWO_RED_FLAG_MAX:
        warnings.append(f"Red-flagged common ratio {rf_ratio:.0%} exceeds NWO target {NWO_RED_FLAG_MAX:.0%}")
        out.append("")
        out.append("**Red-flagged commons:**")
        for c in red_flagged:
            out.append(f"- {c.get('name', '?')} — {c.get('rules_text', '')[:80]}")
    out.append("")

    # --- Creature curves ---
    out.append("## Common creature curves by color")
    for color in COLORS:
        curve = creature_curve(cards, color)
        parts = [f"{cmc}:{curve.get(cmc, 0)}" for cmc in range(1, 8)]
        out.append(f"- {color}: " + " ".join(parts))
        # Check for missing curve slots
        missing = [cmc for cmc in (2, 3, 4) if curve.get(cmc, 0) < 2]
        if missing:
            warnings.append(f"Color {color} is thin at common CMC {missing}")
    out.append("")

    # --- Removal density ---
    out.append("## Removal density (by color, common)")
    for color in COLORS:
        removal_cards = [
            c for c in cards
            if primary_color(c) == color and rarity(c) == "common" and is_removal(c)
        ]
        out.append(f"- {color}: {len(removal_cards)} common removal cards")
        if len(removal_cards) < 2:
            warnings.append(f"Color {color} has only {len(removal_cards)} common removal cards")
    out.append("")

    # --- Color pie alarms ---
    out.append("## Potential color pie alarms")
    all_alarms = []
    for c in cards:
        all_alarms.extend(color_pie_alarms(c))
    if all_alarms:
        out.append(f"**{len(all_alarms)} potential pie violations flagged** (judgment required):")
        for a in all_alarms[:20]:
            out.append(f"- {a}")
        if len(all_alarms) > 20:
            out.append(f"- ...and {len(all_alarms) - 20} more.")
        warnings.append(f"{len(all_alarms)} potential color pie violations to review")
    else:
        out.append("No obvious color pie violations detected.")
    out.append("")

    # --- Archetype support (Play Booster era: count commons + uncommons together) ---
    out.append("## Archetype support at common + uncommon")

    def card_supports_archetype(card: dict, pair: str) -> bool:
        """Check if a card supports an archetype. A card supports a pair if:
        1. The pair is explicitly listed in the card's 'archetypes' array, OR
        2. The card is mono-colored in one of the pair's colors (these are
           playable in the archetype's deck and are implicitly supportive).
        Gold cards that don't list the pair are excluded since they belong to
        a specific archetype by design."""
        # Explicit tag always counts.
        if pair in (card.get("archetypes") or []):
            return True
        # Mono-colored cards in one of the pair's colors implicitly support the pair.
        card_colors = card.get("color", [])
        if len(card_colors) == 1 and card_colors[0] in pair:
            return True
        # Colorless cards are draftable by any archetype — count them.
        if not card_colors:
            return True
        return False

    for pair, data in archetypes.items():
        tagged_c = sum(1 for c in cards if rarity(c) == "common" and pair in (c.get("archetypes") or []))
        tagged_u = sum(1 for c in cards if rarity(c) == "uncommon" and pair in (c.get("archetypes") or []))
        implicit_c = sum(1 for c in cards if rarity(c) == "common" and card_supports_archetype(c, pair)) - tagged_c
        implicit_u = sum(1 for c in cards if rarity(c) == "uncommon" and card_supports_archetype(c, pair)) - tagged_u
        total_tagged = tagged_c + tagged_u
        total_with_implicit = total_tagged + implicit_c + implicit_u

        if total_tagged >= ARCHETYPE_SUPPORT_MIN:
            out.append(f"- {pair} ({data.get('name', '?')}): {tagged_c}C + {tagged_u}U = {total_tagged} (tagged)")
        else:
            status = "" if total_with_implicit >= ARCHETYPE_SUPPORT_MIN else f" ⚠️ (target ≥ {ARCHETYPE_SUPPORT_MIN})"
            out.append(
                f"- {pair} ({data.get('name', '?')}): {tagged_c}C + {tagged_u}U = {total_tagged} tagged"
                f" (+{implicit_c + implicit_u} mono/colorless in-color = {total_with_implicit}){status}"
            )
            if total_with_implicit < ARCHETYPE_SUPPORT_MIN:
                warnings.append(
                    f"Archetype {pair} has only {total_with_implicit} supporting common+uncommon cards "
                    f"({total_tagged} tagged + {implicit_c + implicit_u} implicit; target ≥ {ARCHETYPE_SUPPORT_MIN})"
                )
    out.append("")

    # --- Mechanic spread ---
    out.append("## Mechanic spread vs. target")
    # Build a case-insensitive lookup: lowercase keyword -> {rarity: count}
    mechanic_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for c in cards:
        for kw in c.get("keywords", []) or []:
            mechanic_counts[kw.lower()][rarity(c)] += 1
        # Also scan rules_text for mechanic names that may not be in keywords array
        rules = (c.get("rules_text") or "").lower()
        for m in mechanics:
            mname_lower = m.get("name", "").lower()
            if mname_lower and mname_lower in rules and mname_lower not in [k.lower() for k in (c.get("keywords") or [])]:
                mechanic_counts[mname_lower][rarity(c)] += 1
    for m in mechanics:
        name = m.get("name", "")
        target = m.get("rarity_spread", {})
        actual = mechanic_counts.get(name.lower(), {})
        out.append(f"### {name}")
        for r in RARITIES:
            t = target.get(r, 0)
            a = actual.get(r, 0)
            flag = " ⚠️" if abs(a - t) > max(1, t // 2) else ""
            out.append(f"- {r}: target {t}, actual {a}{flag}")
            if abs(a - t) > max(1, t // 2):
                warnings.append(f"Mechanic {name} off target at {r}: {a} vs target {t}")
    out.append("")

    # --- Summary ---
    out.append("## Summary")
    if warnings:
        out.append(f"**{len(warnings)} warnings:**")
        for w in warnings:
            out.append(f"- {w}")
    else:
        out.append("No warnings — heuristic pass clean. Proceed to draft simulation.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("set_path", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    set_data = load_set(args.set_path)
    report = check_set(set_data)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
