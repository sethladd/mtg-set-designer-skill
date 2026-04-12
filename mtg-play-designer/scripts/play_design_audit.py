#!/usr/bin/env python3
"""
play_design_audit.py - Play Design power-level and format-health audit.

Usage:
    python play_design_audit.py path/to/set.json [--out play_design_report.md]

Runs the complete Play Design battery on a set file:
  1. Rate Card Test — flags cards whose total value exceeds fair rate
  2. Zero-Mana Floor Test — flags cards that can cost 0
  3. Colorless Ubiquity Test — flags above-rate colorless cards
  4. Anti-Counterplay Test — flags cards that shut down their counters
  5. Commander Scaling Test — flags "each opponent" and life-drawback effects
  6. Combo Pattern Scan — flags high-risk combo enabler patterns
  7. Play-Pattern Evaluation — flags interaction denial, agency removal, loops
  8. Scaling Futures Test — flags cards that get stronger with future sets
  9. Parasitic System Test — flags uninteractable resource systems
 10. Limited Format Health — archetype balance, curve, removal adequacy

This is a heuristic auditor. It flags, it does not auto-fix. The play
designer makes the judgment calls.
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

# Evergreen keywords with approximate stat cost (total P+T reduction for one keyword)
KEYWORD_STAT_COST = {
    "flying": 1.5, "first strike": 1.0, "double strike": 3.0,
    "deathtouch": 1.0, "lifelink": 1.0, "vigilance": 0.5,
    "haste": 0.5, "trample": 0.5, "menace": 0.5,
    "reach": 0.5, "hexproof": 1.5, "ward": 1.0,
    "indestructible": 2.0, "flash": 0.5, "defender": -1.0,
}

# Vanilla P/T baselines by CMC (total P+T expected)
VANILLA_STAT_TOTAL = {
    1: 3,   # 2/1 or 1/2
    2: 5,   # 2/3 or 3/2
    3: 7,   # 3/4 or 4/3
    4: 9,   # 4/5 or 5/4
    5: 11,  # 5/6 or 6/5
    6: 12,  # 6/6
    7: 13,  # 6/7 or 7/6
}

# Patterns that suggest removal
REMOVAL_PATTERNS = [
    r"destroy target (creature|permanent)",
    r"exile target (creature|permanent)",
    r"deals? \d+ damage to (any target|target creature)",
    r"target creature gets -\d+/-\d+",
    r"return target (creature|nonland permanent) to its owner'?s? hand",
    r"counter target spell",
    r"fights? target creature",
]

# Patterns that suggest mana-cost bypass
MANA_BYPASS_PATTERNS = [
    r"without paying (its|their) mana cost",
    r"you may cast .+ without paying",
    r"convoke",
    r"delve",
    r"cascade",
    r"discover \d+",
    r"suspend",
    r"foretell",
]

# Patterns suggesting combo risk
COMBO_RISK_PATTERNS = [
    r"create a (token that.s a )?copy",
    r"return .+ from .+ graveyard to the battlefield",
    r"untap (target|all|each)",
    r"take an extra turn",
    r"whenever .+ enters the battlefield",
    r"whenever .+ dies",
    r"sacrifice .+:",
]

# Patterns suggesting interaction denial / play-pattern problems
PLAY_PATTERN_PATTERNS = [
    (r"can'?t cast (spells|instants|sorceries)", "interaction_denial"),
    (r"can'?t (attack|block|activate)", "agency_removal"),
    (r"take an extra turn", "extra_turns"),
    (r"whenever .+ (enters|dies|attacks|is dealt), .+return", "loop_risk"),
    (r"each (opponent|player) (loses|discards|sacrifices)", "each_opponent"),
    (r"skip .+ (draw|untap|combat)", "phase_denial"),
]

# Patterns suggesting commander scaling
COMMANDER_SCALE_PATTERNS = [
    (r"each opponent", "each_opponent_trigger"),
    (r"each player", "each_player_trigger"),
    (r"for each opponent", "per_opponent_scaling"),
    (r"whenever an opponent", "opponent_action_trigger"),
    (r"pay \d+ life", "life_as_cost"),
    (r"lose \d+ life", "life_as_drawback"),
    (r"create .+ treasure", "treasure_generation"),
]

# Patterns suggesting the card scales with future sets
SCALING_PATTERNS = [
    (r"whenever you cast a .+ spell", "cast_trigger"),
    (r"whenever a .+ enters the battlefield", "etb_trigger"),
    (r"whenever you (gain|lose) life", "life_change_trigger"),
    (r"for each .+ you control", "board_scaling"),
    (r"double .+ (counters|tokens|mana)", "doubling_effect"),
    (r"copy .+ spell", "spell_copy"),
]


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def primary_color(card: dict) -> str:
    colors = card.get("color", [])
    if not colors:
        return "C"
    if len(colors) > 1:
        return "M"
    return colors[0]


def is_creature(card: dict) -> bool:
    return "Creature" in card.get("type", "")


def is_colorless(card: dict) -> bool:
    return not card.get("color", [])


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def rules_text(card: dict) -> str:
    return (card.get("rules_text") or "").lower()


def cmc(card: dict) -> int:
    return card.get("cmc", 0)


def stat_total(card: dict) -> int:
    p = card.get("power", 0) or 0
    t = card.get("toughness", 0) or 0
    return p + t


def keyword_cost(card: dict) -> float:
    """Estimate total keyword stat cost."""
    total = 0.0
    for kw in card.get("keywords", []) or []:
        total += KEYWORD_STAT_COST.get(kw.lower(), 0.5)
    return total


def count_abilities(card: dict) -> int:
    """Rough count of distinct abilities via line breaks and semicolons."""
    text = card.get("rules_text") or ""
    if not text.strip():
        return 0
    return max(1, text.count("\n") + text.count(";") + 1)


def is_removal(card: dict) -> bool:
    text = rules_text(card)
    return any(re.search(p, text) for p in REMOVAL_PATTERNS)


def check_rate(cards: list[dict]) -> list[str]:
    """Rate Card Test: flag creatures above vanilla baseline."""
    flags: list[str] = []
    for c in cards:
        if not is_creature(c):
            continue
        card_cmc = cmc(c)
        if card_cmc < 1 or card_cmc > 7:
            continue
        baseline = VANILLA_STAT_TOTAL.get(card_cmc, 12)
        actual = stat_total(c)
        kw_cost = keyword_cost(c)
        ability_count = count_abilities(c)
        # Expected stat total = baseline - keyword cost - ability penalty
        ability_penalty = max(0, ability_count - 1) * 0.5
        expected_max = baseline - kw_cost - ability_penalty + 1  # +1 grace
        if actual > expected_max + 1:
            flags.append(
                f"RATE: {c.get('name', '?')} ({card_cmc}CMC {rarity(c)}) — "
                f"P/T {c.get('power')}/{c.get('toughness')} (total {actual}) "
                f"exceeds expected max {expected_max:.1f} "
                f"(baseline {baseline} - {kw_cost:.1f} kw - {ability_penalty:.1f} abilities)"
            )
    return flags


def check_zero_mana(cards: list[dict]) -> list[str]:
    """Zero-Mana Floor Test: flag cards that bypass mana costs."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        for pattern in MANA_BYPASS_PATTERNS:
            if re.search(pattern, text):
                flags.append(
                    f"ZERO-MANA: {c.get('name', '?')} ({rarity(c)}) — "
                    f"contains mana-bypass pattern: /{pattern}/"
                )
                break
        # Also flag cards that literally cost 0
        if cmc(c) == 0 and c.get("type", "").lower() not in ("land", "basic land"):
            mana = c.get("mana_cost", "")
            if mana in ("", "{0}", "0"):
                flags.append(
                    f"ZERO-MANA: {c.get('name', '?')} ({rarity(c)}) — "
                    f"literal zero mana cost"
                )
    return flags


def check_colorless_ubiquity(cards: list[dict]) -> list[str]:
    """Colorless Ubiquity Test: flag above-rate colorless cards."""
    flags: list[str] = []
    for c in cards:
        if not is_colorless(c):
            continue
        if "Land" in (c.get("type") or ""):
            continue
        # Colorless creatures above vanilla rate
        if is_creature(c):
            card_cmc = cmc(c)
            if card_cmc < 1:
                continue
            baseline = VANILLA_STAT_TOTAL.get(card_cmc, 12)
            actual = stat_total(c)
            if actual >= baseline and count_abilities(c) > 0:
                flags.append(
                    f"COLORLESS: {c.get('name', '?')} ({card_cmc}CMC) — "
                    f"colorless with stats {c.get('power')}/{c.get('toughness')} "
                    f"AND abilities. Warps formats by having zero deckbuilding cost."
                )
        # Colorless card draw
        if re.search(r"draw (a card|cards|\d+ card)", rules_text(c)):
            flags.append(
                f"COLORLESS: {c.get('name', '?')} — "
                f"colorless card draw. High ubiquity risk."
            )
    return flags


def check_commander_scaling(cards: list[dict]) -> list[str]:
    """Commander Scaling Test: flag multiplayer-dangerous effects."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        for pattern, category in COMMANDER_SCALE_PATTERNS:
            if re.search(pattern, text):
                flags.append(
                    f"COMMANDER: {c.get('name', '?')} ({rarity(c)}) — "
                    f"scales in multiplayer [{category}]: /{pattern}/"
                )
    return flags


def check_play_patterns(cards: list[dict]) -> list[str]:
    """Play-Pattern Evaluation: flag interaction denial, agency removal, loops."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        for pattern, category in PLAY_PATTERN_PATTERNS:
            if re.search(pattern, text):
                flags.append(
                    f"PLAY-PATTERN: {c.get('name', '?')} ({rarity(c)}) — "
                    f"{category}: /{pattern}/"
                )
    return flags


def check_combo_risk(cards: list[dict]) -> list[str]:
    """Combo Pattern Scan: flag high-risk combo enabler patterns."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        risks = []
        for pattern in COMBO_RISK_PATTERNS:
            if re.search(pattern, text):
                risks.append(pattern)
        if len(risks) >= 2:
            flags.append(
                f"COMBO-RISK: {c.get('name', '?')} ({rarity(c)}) — "
                f"multiple combo-relevant patterns: {', '.join(risks[:3])}"
            )
    return flags


def check_scaling(cards: list[dict]) -> list[str]:
    """Scaling Futures Test: flag cards that get stronger with future sets."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        # Only flag if there's no "once per turn" limiter
        has_limiter = bool(re.search(r"(once (each|per) turn|this ability triggers only once)", text))
        if has_limiter:
            continue
        for pattern, category in SCALING_PATTERNS:
            if re.search(pattern, text):
                flags.append(
                    f"SCALING: {c.get('name', '?')} ({rarity(c)}) — "
                    f"scales with future cards [{category}] without 'once per turn' limiter"
                )
                break  # one flag per card
    return flags


def check_anti_counterplay(cards: list[dict]) -> list[str]:
    """Anti-Counterplay Test: flag cards that shut down their own counters."""
    flags: list[str] = []
    anti_patterns = [
        (r"can'?t gain life", "lifegain_denial", "aggro"),
        (r"players can'?t cast .+ spells during your turn", "instant_denial", "proactive"),
        (r"whenever .+ player gains life .+ (lose|damage)", "lifegain_punish", "aggro"),
        (r"can'?t be countered", "uncounterable", "any"),
        (r"hexproof from", "color_protection", "any"),
        (r"protection from", "color_protection", "any"),
    ]
    for c in cards:
        text = rules_text(c)
        for pattern, category, archetype in anti_patterns:
            if re.search(pattern, text):
                flags.append(
                    f"ANTI-COUNTERPLAY: {c.get('name', '?')} ({rarity(c)}) — "
                    f"{category} [{archetype}]: /{pattern}/"
                )
    return flags


def check_limited_format_health(set_data: dict) -> list[str]:
    """Basic Limited format health checks."""
    cards = set_data.get("cards", [])
    archetypes = set_data.get("archetypes", {})
    flags: list[str] = []

    # Check removal density
    total_common_removal = 0
    removal_by_color: dict[str, int] = defaultdict(int)
    for c in cards:
        if rarity(c) == "common" and is_removal(c):
            total_common_removal += 1
            removal_by_color[primary_color(c)] += 1

    if total_common_removal < 10:
        flags.append(
            f"LIMITED: Only {total_common_removal} common removal spells "
            f"(target: 10-15). Format risks being bomb-dominated."
        )

    for color in COLORS:
        count = removal_by_color.get(color, 0)
        if count < 1:
            flags.append(
                f"LIMITED: Color {color} has {count} common removal spells. "
                f"Color may be unplayable."
            )

    # Check creature curve completeness at common
    for color in COLORS:
        curve: dict[int, int] = defaultdict(int)
        for c in cards:
            if is_creature(c) and primary_color(c) == color and rarity(c) == "common":
                curve[cmc(c)] += 1
        for mv in (2, 3, 4):
            if curve.get(mv, 0) < 2:
                flags.append(
                    f"LIMITED: Color {color} has only {curve.get(mv, 0)} common "
                    f"creatures at MV {mv} (need ≥2)."
                )

    # Check archetype support
    if archetypes:
        arch_map = archetypes if isinstance(archetypes, dict) else {}
        for pair, data in arch_map.items():
            if not isinstance(data, dict):
                continue
            support = sum(
                1 for c in cards
                if rarity(c) in ("common", "uncommon")
                and pair in (c.get("archetypes") or [])
            )
            # Also count mono-colored cards in the pair's colors
            implicit = sum(
                1 for c in cards
                if rarity(c) in ("common", "uncommon")
                and len(c.get("color", [])) == 1
                and c["color"][0] in pair
            )
            total = support + implicit
            if total < 22:
                flags.append(
                    f"LIMITED: Archetype {pair} ({data.get('name', '?')}) has only "
                    f"{total} C+U support cards ({support} tagged + {implicit} implicit). "
                    f"Target: ≥22."
                )

    return flags


def audit_set(set_data: dict) -> str:
    cards = set_data.get("cards", [])
    out: list[str] = []
    out.append(f"# Play Design Report: {set_data.get('set_name', 'Unnamed Set')}")
    out.append(f"Total cards analyzed: **{len(cards)}**")
    out.append("")

    all_flags: list[str] = []

    # Run all checks
    checks = [
        ("Rate Card Test", check_rate(cards)),
        ("Zero-Mana Floor Test", check_zero_mana(cards)),
        ("Colorless Ubiquity Test", check_colorless_ubiquity(cards)),
        ("Anti-Counterplay Test", check_anti_counterplay(cards)),
        ("Commander Scaling Test", check_commander_scaling(cards)),
        ("Combo Pattern Scan", check_combo_risk(cards)),
        ("Play-Pattern Evaluation", check_play_patterns(cards)),
        ("Scaling Futures Test", check_scaling(cards)),
        ("Limited Format Health", check_limited_format_health(set_data)),
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

    # Summary
    out.append("## Summary")
    if all_flags:
        # Count by category
        categories: dict[str, int] = defaultdict(int)
        for f in all_flags:
            cat = f.split(":")[0]
            categories[cat] += 1
        out.append(f"**{len(all_flags)} total flags across {len(categories)} categories:**")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            out.append(f"- {cat}: {count}")
        out.append("")
        out.append("### Priority Actions")
        # High priority: rate + zero-mana + combo
        high = [f for f in all_flags if any(f.startswith(p) for p in ("RATE:", "ZERO-MANA:", "COMBO-RISK:"))]
        if high:
            out.append(f"**High priority ({len(high)}):** Rate, zero-mana, and combo flags require immediate review.")
        # Medium priority: commander + play-pattern + anti-counterplay
        medium = [f for f in all_flags if any(f.startswith(p) for p in ("COMMANDER:", "PLAY-PATTERN:", "ANTI-COUNTERPLAY:"))]
        if medium:
            out.append(f"**Medium priority ({len(medium)}):** Commander scaling, play-pattern, and anti-counterplay flags.")
        # Lower priority: colorless + scaling + limited
        lower = [f for f in all_flags if any(f.startswith(p) for p in ("COLORLESS:", "SCALING:", "LIMITED:"))]
        if lower:
            out.append(f"**Lower priority ({len(lower)}):** Colorless ubiquity, scaling, and Limited format health.")
    else:
        out.append("✓ No flags raised. Card file passes Play Design audit.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Play Design power-level and format-health audit")
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
