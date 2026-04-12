#!/usr/bin/env python3
"""
product_audit.py - MTG product suite audit.

Usage:
    python product_audit.py path/to/set.json path/to/product_brief.json [--out product_audit_report.md]

Checks:
  1. Poster card presence — at least 3 poster cards at mythic/rare
  2. Precon theme connection — each precon theme maps to main set mechanics
  3. Precon commander validity — commanders are legendary creatures with correct colors
  4. Precon independence — precons don't require main set rares/mythics
  5. Special treatment distribution — treatments spread across colors and rarities
  6. Product differentiation — each product has a distinct audience
  7. Chase distribution — chase cards exist across multiple product types
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# --- Constants ---

MIN_POSTER_CARDS = 3
MIN_PRECON_THEMES = 2
MAX_PRECON_THEMES = 4
MIN_POSTER_COLORS = 3
PRECON_POWER_MIN = 5
PRECON_POWER_MAX = 8
MIN_NEW_CARDS_PER_PRECON = 8
MAX_NEW_CARDS_PER_PRECON = 20

# Cards that are red flags if they appear as precon-exclusive new cards
DANGEROUS_PATTERNS = [
    r"without paying.*mana cost",
    r"costs? \{0\}",
    r"for each opponent",
    r"for each player",
    r"free.*commander",
    r"if you control your commander.*\{0\}",
]

VALID_COLORS = {"W", "U", "B", "R", "G"}


# --- Helpers ---

def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def card_colors(card: dict) -> set[str]:
    colors = card.get("color", [])
    if isinstance(colors, str):
        colors = list(colors)
    return {c.upper() for c in colors}


def is_legendary(card: dict) -> bool:
    return "legendary" in (card.get("type") or "").lower()


def is_creature(card: dict) -> bool:
    return "creature" in (card.get("type") or "").lower()


def rarity(card: dict) -> str:
    return (card.get("rarity") or "common").lower()


# --- Checks ---

def check_poster_cards(brief: dict, cards: list[dict]) -> list[str]:
    """Check 1: At least 3 poster cards identified at mythic/rare."""
    flags: list[str] = []
    poster_cards = brief.get("poster_cards", [])

    if not poster_cards:
        flags.append(
            "POSTER-MISSING: No poster cards identified in product brief"
        )
        return flags

    if len(poster_cards) < MIN_POSTER_CARDS:
        flags.append(
            f"POSTER-FEW: Only {len(poster_cards)} poster cards identified "
            f"(minimum {MIN_POSTER_CARDS})"
        )

    # Check that poster cards exist in the set at mythic/rare
    card_names = {c.get("name", "").lower(): c for c in cards}
    poster_colors: set[str] = set()
    has_legendary = False
    has_noncreature = False

    for pc in poster_cards:
        pc_name = pc if isinstance(pc, str) else pc.get("name", "")
        pc_lower = pc_name.lower()
        if pc_lower not in card_names:
            flags.append(
                f"POSTER-NOT-FOUND: Poster card '{pc_name}' not found in set"
            )
            continue
        card = card_names[pc_lower]
        if rarity(card) not in ("mythic", "rare"):
            flags.append(
                f"POSTER-RARITY: Poster card '{pc_name}' is "
                f"{rarity(card)}, expected mythic or rare"
            )
        poster_colors.update(card_colors(card))
        if is_legendary(card):
            has_legendary = True
        if not is_creature(card):
            has_noncreature = True

    if len(poster_colors) < MIN_POSTER_COLORS:
        flags.append(
            f"POSTER-COLOR-GAP: Poster cards cover {len(poster_colors)} "
            f"colors (minimum {MIN_POSTER_COLORS}): "
            f"{', '.join(sorted(poster_colors))}"
        )
    if not has_legendary:
        flags.append(
            "POSTER-NO-LEGENDARY: No poster card is a legendary creature "
            "(missing Commander hook)"
        )
    if not has_noncreature:
        flags.append(
            "POSTER-ALL-CREATURES: No poster card is a non-creature spell "
            "(missing competitive hook)"
        )

    return flags


def check_precon_themes(brief: dict, cards: list[dict]) -> list[str]:
    """Check 2: Precon themes connect to main set mechanics."""
    flags: list[str] = []
    precons = brief.get("commander_precons", [])

    if not precons:
        flags.append("PRECON-MISSING: No Commander precons defined")
        return flags

    if len(precons) < MIN_PRECON_THEMES:
        flags.append(
            f"PRECON-FEW: Only {len(precons)} precons "
            f"(minimum {MIN_PRECON_THEMES})"
        )
    if len(precons) > MAX_PRECON_THEMES:
        flags.append(
            f"PRECON-MANY: {len(precons)} precons "
            f"(maximum {MAX_PRECON_THEMES})"
        )

    # Check that each precon has a connection to main set
    set_keywords: set[str] = set()
    set_archetypes: set[str] = set()
    for c in cards:
        for kw in c.get("keywords", []):
            set_keywords.add(kw.lower())
        for arch in c.get("archetypes", []):
            set_archetypes.add(arch.upper())

    for precon in precons:
        name = precon.get("precon_name", precon.get("name", "???"))
        connection = (precon.get("connection_to_main_set") or "").lower()
        theme = (precon.get("theme") or "").lower()
        if not connection and not theme:
            flags.append(
                f"PRECON-NO-CONNECTION: '{name}' has no documented "
                f"connection to main set"
            )

    return flags


def check_precon_commanders(brief: dict) -> list[str]:
    """Check 3: Commanders are legendary creatures with matching colors."""
    flags: list[str] = []
    precons = brief.get("commander_precons", [])

    for precon in precons:
        name = precon.get("precon_name", precon.get("name", "???"))
        precon_colors = set(precon.get("colors", []))
        commander = precon.get("commander", {})

        if not commander:
            flags.append(f"CMD-MISSING: '{name}' has no commander defined")
            continue

        cmd_name = commander.get("name", "???")
        cmd_type = (commander.get("type") or "").lower()

        # Check legendary
        if "legendary" not in cmd_type:
            flags.append(
                f"CMD-NOT-LEGENDARY: '{cmd_name}' in '{name}' "
                f"is not legendary"
            )

        # Check creature
        if "creature" not in cmd_type:
            flags.append(
                f"CMD-NOT-CREATURE: '{cmd_name}' in '{name}' "
                f"is not a creature"
            )

        # Check color match
        cmd_colors = set()
        mana_cost = commander.get("mana_cost", "")
        for c in VALID_COLORS:
            if c in mana_cost.upper():
                cmd_colors.add(c)
        if cmd_colors and precon_colors and cmd_colors != precon_colors:
            flags.append(
                f"CMD-COLOR-MISMATCH: '{cmd_name}' colors "
                f"{sorted(cmd_colors)} don't match precon '{name}' "
                f"colors {sorted(precon_colors)}"
            )

        # Check backup commander
        backup = precon.get("backup_commander")
        if not backup:
            flags.append(
                f"CMD-NO-BACKUP: '{name}' has no backup commander"
            )

    return flags


def check_precon_independence(brief: dict) -> list[str]:
    """Check 4: Precons don't require main set rares/mythics."""
    flags: list[str] = []
    precons = brief.get("commander_precons", [])

    for precon in precons:
        name = precon.get("precon_name", precon.get("name", "???"))
        new_cards = precon.get("new_cards_count", 0)

        if new_cards < MIN_NEW_CARDS_PER_PRECON:
            flags.append(
                f"PRECON-FEW-NEW: '{name}' has {new_cards} new cards "
                f"(minimum {MIN_NEW_CARDS_PER_PRECON})"
            )
        if new_cards > MAX_NEW_CARDS_PER_PRECON:
            flags.append(
                f"PRECON-MANY-NEW: '{name}' has {new_cards} new cards "
                f"(maximum {MAX_NEW_CARDS_PER_PRECON})"
            )

        # Check for dangerous card patterns in new card descriptions
        new_card_list = precon.get("new_cards", [])
        for card in new_card_list:
            card_name = card.get("name", "???")
            rules = (card.get("rules_text") or card.get("ability_summary") or "").lower()
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, rules, re.IGNORECASE):
                    flags.append(
                        f"PRECON-DANGEROUS: '{card_name}' in '{name}' "
                        f"has potentially format-warping text: "
                        f"'{rules[:60]}...'"
                    )
                    break

    return flags


def check_treatment_distribution(brief: dict, cards: list[dict]) -> list[str]:
    """Check 5: Special treatments spread across colors and rarities."""
    flags: list[str] = []
    treatments = brief.get("special_treatments", {})

    if not treatments:
        flags.append("TREAT-MISSING: No special treatments defined")
        return flags

    # Check showcase frame exists
    showcase = treatments.get("showcase_frame", {})
    if not showcase:
        flags.append("TREAT-NO-SHOWCASE: No showcase frame defined")

    # Check that treatments aren't all in one color
    treated_cards = treatments.get("showcase_cards", [])
    treated_cards += treatments.get("borderless_cards", [])
    if treated_cards:
        card_names = {c.get("name", "").lower(): c for c in cards}
        treatment_colors: Counter[str] = Counter()
        for tc in treated_cards:
            tc_name = tc if isinstance(tc, str) else tc.get("name", "")
            card = card_names.get(tc_name.lower())
            if card:
                for color in card_colors(card):
                    treatment_colors[color] += 1

        if treatment_colors:
            total_treated = sum(treatment_colors.values())
            for color, count in treatment_colors.items():
                ratio = count / total_treated
                if ratio > 0.40:
                    flags.append(
                        f"TREAT-COLOR-SKEW: {ratio:.0%} of treated cards "
                        f"are {color} (threshold: 40%)"
                    )

    return flags


def check_product_differentiation(brief: dict) -> list[str]:
    """Check 6: Each product has a distinct audience."""
    flags: list[str] = []
    hooks = brief.get("marketing_hooks", {})

    audiences = ["competitive", "casual", "collector"]
    for audience in audiences:
        hook = hooks.get(audience, "")
        if not hook:
            flags.append(
                f"HOOK-MISSING: No marketing hook for {audience} audience"
            )

    # Check for selling sentences
    selling = brief.get("selling_sentences", {})
    if not selling and not hooks:
        flags.append(
            "HOOK-NO-SENTENCES: No selling sentences defined for any audience"
        )

    return flags


def check_chase_distribution(brief: dict) -> list[str]:
    """Check 7: Chase cards exist across multiple product types."""
    flags: list[str] = []
    poster = brief.get("poster_cards", [])
    precons = brief.get("commander_precons", [])
    treatments = brief.get("special_treatments", {})

    has_booster_chase = len(poster) >= 1
    has_precon_chase = any(
        p.get("commander", {}).get("name")
        for p in precons
    )
    has_collector_chase = bool(
        treatments.get("textured_foil_cards")
        or treatments.get("serialized_cards")
        or treatments.get("showcase_cards")
    )

    chase_count = sum([has_booster_chase, has_precon_chase, has_collector_chase])
    if chase_count < 2:
        flags.append(
            f"CHASE-CONCENTRATED: Chase content found in only "
            f"{chase_count}/3 product types "
            f"(boosters: {has_booster_chase}, precons: {has_precon_chase}, "
            f"collector: {has_collector_chase})"
        )

    return flags


# --- Report ---

def audit_product(set_data: dict, brief: dict) -> str:
    cards = set_data.get("cards", [])

    out: list[str] = []
    all_flags: list[str] = []

    out.append("# Product Architecture Audit Report")
    out.append(f"\nSet: {set_data.get('set_name', 'Unknown')}")
    out.append(f"Cards in set: {len(cards)}")
    precons = brief.get("commander_precons", [])
    out.append(f"Commander precons: {len(precons)}")
    out.append("")

    checks = [
        ("Poster Card Presence", check_poster_cards(brief, cards)),
        ("Precon Theme Connection", check_precon_themes(brief, cards)),
        ("Precon Commander Validity", check_precon_commanders(brief)),
        ("Precon Independence", check_precon_independence(brief)),
        ("Special Treatment Distribution",
         check_treatment_distribution(brief, cards)),
        ("Product Differentiation", check_product_differentiation(brief)),
        ("Chase Distribution", check_chase_distribution(brief)),
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
    poster = brief.get("poster_cards", [])
    out.append(f"- Poster cards: {len(poster)}")
    out.append(f"- Commander precons: {len(precons)}")
    total_new = sum(
        p.get("new_cards_count", 0) for p in precons
    )
    out.append(f"- Total new precon cards: {total_new}")

    # Precon color coverage
    precon_colors: set[str] = set()
    for p in precons:
        for c in p.get("colors", []):
            precon_colors.add(c.upper())
    out.append(
        f"- Precon color coverage: "
        f"{', '.join(sorted(precon_colors)) or 'none'} "
        f"({len(precon_colors)}/5)"
    )
    missing_colors = VALID_COLORS - precon_colors
    if missing_colors:
        out.append(
            f"- Colors not covered by precons: "
            f"{', '.join(sorted(missing_colors))}"
        )
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
        out.append("✓ No issues detected. Product architecture passes audit.")
    out.append("")
    return "\n".join(out)


# --- CLI ---

def main() -> int:
    ap = argparse.ArgumentParser(
        description="MTG product architecture audit"
    )
    ap.add_argument("set_path", type=Path, help="Path to set.json")
    ap.add_argument("brief_path", type=Path,
                    help="Path to product_brief.json")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output report path (default: stdout)")
    args = ap.parse_args()

    set_data = load_json(args.set_path)
    brief = load_json(args.brief_path)
    report = audit_product(set_data, brief)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
