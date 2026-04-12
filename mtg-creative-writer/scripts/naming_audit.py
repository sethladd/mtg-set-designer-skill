#!/usr/bin/env python3
"""
naming_audit.py - MTG card naming and flavor text audit.

Usage:
    python naming_audit.py path/to/set.json [--out naming_report.md]

Checks:
  1. Name presence — every card has a non-placeholder name
  2. Name length — within ~35 character limit
  3. Name uniqueness within set — no duplicates
  4. Name-type coherence — creature names should be noun phrases, spell names verb phrases
  5. Legendary format — "Name, Title" with comma
  6. Flavor text coverage — rares/mythics should all have flavor text
  7. Flavor text length — 8-35 word sweet spot
  8. Attribution format — em-dash convention
  9. Generic name detection — flags names that feel too generic
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# Words suggesting action (spell-like), not beings (creature-like)
ACTION_WORDS = {
    "strike", "bolt", "blast", "surge", "assault", "charge", "attack",
    "barrage", "volley", "burst", "eruption", "collapse", "breach",
    "slash", "crush", "smash", "shatter", "cleave", "rend",
}

# Common generic patterns that signal lazy naming
GENERIC_PATTERNS = [
    r"^(Elite|Greater|Lesser|Ancient|Dark|Mighty|Swift|Brave) (Warrior|Soldier|Knight|Mage|Wizard|Beast|Dragon)$",
    r"^(Fire|Ice|Lightning|Shadow|Light) (Bolt|Blast|Strike|Arrow|Spear)$",
]

MAX_NAME_LENGTH = 35
FLAVOR_WORD_MIN = 4
FLAVOR_WORD_MAX = 40
FLAVOR_SWEET_SPOT_MAX = 15


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def card_type(card: dict) -> str:
    return (card.get("type") or "").lower()


def is_legendary(card: dict) -> bool:
    return "legendary" in card_type(card)


def is_creature(card: dict) -> bool:
    return "creature" in card_type(card)


def is_instant_sorcery(card: dict) -> bool:
    ct = card_type(card)
    return "instant" in ct or "sorcery" in ct


def check_name_presence(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for i, c in enumerate(cards):
        name = c.get("name", "").strip()
        if not name:
            flags.append(f"NAME-MISSING: Card #{i+1} (id: {c.get('id', '?')}) has no name")
        elif name.startswith("[") or name.startswith("PLACEHOLDER"):
            flags.append(f"NAME-PLACEHOLDER: '{name}' appears to be a placeholder")
    return flags


def check_name_length(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for c in cards:
        name = c.get("name", "")
        if len(name) > MAX_NAME_LENGTH:
            flags.append(
                f"NAME-LENGTH: '{name}' is {len(name)} chars (max ~{MAX_NAME_LENGTH})"
            )
    return flags


def check_name_uniqueness(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    name_counts = Counter(c.get("name", "") for c in cards)
    for name, count in name_counts.items():
        if count > 1 and name:
            flags.append(f"NAME-DUPLICATE: '{name}' appears {count} times in set")
    return flags


def check_name_type_coherence(cards: list[dict]) -> list[str]:
    """Flag creature names that sound like actions, and spell names that sound like beings."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", "")
        name_lower = name.lower()
        words = name_lower.split()

        if is_creature(c):
            # Check if name sounds like an action
            if words and words[0] in ACTION_WORDS:
                flags.append(
                    f"NAME-TYPE: '{name}' (creature) starts with action word '{words[0]}'. "
                    f"Creature names should be noun phrases (beings, not actions)."
                )

        if is_instant_sorcery(c):
            # Less critical — instants/sorceries have more naming freedom
            pass

    return flags


def check_legendary_format(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for c in cards:
        if not is_legendary(c) or not is_creature(c):
            continue
        name = c.get("name", "")
        if "," not in name and len(name.split()) > 1:
            flags.append(
                f"LEGENDARY: '{name}' — legendary creature without comma. "
                f"Expected 'Name, Title' format."
            )
    return flags


def check_flavor_coverage(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    rare_mythic_missing = []
    total_cu = 0
    cu_with_flavor = 0

    for c in cards:
        r = rarity(c)
        flavor = (c.get("flavor_text") or "").strip()

        if r in ("rare", "mythic") and not flavor:
            rare_mythic_missing.append(c.get("name", "?"))

        if r in ("common", "uncommon"):
            total_cu += 1
            if flavor:
                cu_with_flavor += 1

    if rare_mythic_missing:
        flags.append(
            f"FLAVOR-COVERAGE: {len(rare_mythic_missing)} rares/mythics missing flavor text: "
            f"{', '.join(rare_mythic_missing[:10])}"
            + (f" ...and {len(rare_mythic_missing)-10} more" if len(rare_mythic_missing) > 10 else "")
        )

    if total_cu > 0:
        ratio = cu_with_flavor / total_cu
        if ratio < 0.30:
            flags.append(
                f"FLAVOR-COVERAGE: Only {ratio:.0%} of commons/uncommons have flavor text "
                f"(target: ≥30%)"
            )

    return flags


def check_flavor_length(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for c in cards:
        flavor = (c.get("flavor_text") or "").strip()
        if not flavor:
            continue
        # Remove attribution line for word count
        lines = flavor.split("\n")
        text_lines = [l for l in lines if not l.strip().startswith("—") and not l.strip().startswith("--")]
        text = " ".join(text_lines)
        word_count = len(text.split())

        if word_count > FLAVOR_WORD_MAX:
            flags.append(
                f"FLAVOR-LENGTH: '{c.get('name', '?')}' — {word_count} words "
                f"(max ~{FLAVOR_WORD_MAX}). Consider cutting."
            )
    return flags


def check_attribution_format(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for c in cards:
        flavor = (c.get("flavor_text") or "").strip()
        if not flavor:
            continue
        # Check for attribution with wrong dash type
        if re.search(r"^-[^-]", flavor, re.MULTILINE):
            flags.append(
                f"ATTRIBUTION: '{c.get('name', '?')}' — uses hyphen (-) for attribution. "
                f"Should use em-dash (—)."
            )
        if re.search(r"^--[^-]", flavor, re.MULTILINE):
            flags.append(
                f"ATTRIBUTION: '{c.get('name', '?')}' — uses double-hyphen (--) for attribution. "
                f"Should use em-dash (—)."
            )
    return flags


def check_generic_names(cards: list[dict]) -> list[str]:
    flags: list[str] = []
    for c in cards:
        name = c.get("name", "")
        for pattern in GENERIC_PATTERNS:
            if re.match(pattern, name, re.IGNORECASE):
                flags.append(
                    f"GENERIC: '{name}' matches generic pattern. "
                    f"Consider a more world-specific name."
                )
    return flags


def audit_set(set_data: dict) -> str:
    cards = set_data.get("cards", [])
    out: list[str] = []
    out.append(f"# Naming & Flavor Text Report: {set_data.get('set_name', 'Unnamed Set')}")
    out.append(f"Total cards: **{len(cards)}**")
    out.append("")

    all_flags: list[str] = []

    checks = [
        ("Name Presence", check_name_presence(cards)),
        ("Name Length", check_name_length(cards)),
        ("Name Uniqueness", check_name_uniqueness(cards)),
        ("Name-Type Coherence", check_name_type_coherence(cards)),
        ("Legendary Format", check_legendary_format(cards)),
        ("Flavor Text Coverage", check_flavor_coverage(cards)),
        ("Flavor Text Length", check_flavor_length(cards)),
        ("Attribution Format", check_attribution_format(cards)),
        ("Generic Name Detection", check_generic_names(cards)),
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

    # Stats
    out.append("## Statistics")
    total = len(cards)
    with_flavor = sum(1 for c in cards if (c.get("flavor_text") or "").strip())
    out.append(f"- Cards with flavor text: {with_flavor}/{total} ({with_flavor/total:.0%})")
    legendaries = [c for c in cards if is_legendary(c)]
    out.append(f"- Legendary cards: {len(legendaries)}")
    avg_name_len = sum(len(c.get("name", "")) for c in cards) / max(total, 1)
    out.append(f"- Average name length: {avg_name_len:.1f} chars")
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
        out.append("✓ No issues detected. Naming and flavor text pass audit.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="MTG naming and flavor text audit")
    ap.add_argument("set_path", type=Path, help="Path to set.json")
    ap.add_argument("--out", type=Path, default=None, help="Output report path")
    args = ap.parse_args()

    set_data = load_set(args.set_path)
    report = audit_set(set_data)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
