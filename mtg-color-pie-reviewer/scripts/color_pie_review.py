#!/usr/bin/env python3
"""
color_pie_review.py — Automated color pie review for MTG card files.

Usage:
    python color_pie_review.py path/to/set.json [--out color_pie_review.md]

Reads a set.json (or any JSON file containing a "cards" array) and flags
potential color pie violations using pattern matching against known effect-to-color
assignments. Produces a markdown report sorted by severity.

This is a FIRST PASS — it catches mechanical pattern matches but cannot evaluate
context, set themes, or philosophical nuance. The skill's LLM-based review layers
judgment on top of these automated findings.

The script is deliberately conservative: it flags things for attention rather than
making final calls. A flag from this script means "a human or LLM reviewer should
look at this," not "this is definitely wrong."
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Core weakness violations — these are always rating 4 (break)
# Each entry: (color, pattern, explanation)
# ---------------------------------------------------------------------------
CORE_WEAKNESS_VIOLATIONS: list[tuple[str, str, str]] = [
    # Red cannot remove enchantments
    ("R", r"destroy target enchantment", "Red cannot destroy enchantments — core weakness"),
    ("R", r"exile target enchantment", "Red cannot exile enchantments — core weakness"),
    ("R", r"return target enchantment.*(hand|library)", "Red cannot bounce enchantments — functional removal is still a break"),

    # Blue cannot destroy creatures efficiently
    ("U", r"destroy target creature(?!\s+with)", "Blue cannot destroy creatures — use bounce, tap, or transformation instead"),
    ("U", r"exile target creature(?!\s+with)", "Blue cannot exile creatures unconditionally"),
    ("U", r"target creature gets -\d+/-\d+", "Negative P/T modification is black, not blue"),

    # Green cannot counter spells
    ("G", r"counter target spell", "Green cannot counter spells — core weakness"),
    ("G", r"counter target (instant|sorcery|creature|artifact|enchantment|planeswalker) spell",
     "Green cannot counter any type of spell"),

    # Green cannot deal non-combat damage to players
    ("G", r"deals? \d+ damage to (target player|any target|target opponent|each opponent)",
     "Green cannot deal direct damage to players — damage must be creature-mediated (fight/trample)"),

    # Red cannot gain life
    ("R", r"(gain|gains) \d+ life", "Red cannot gain life — core weakness"),
    ("R", r"\blifelink\b", "Red does not get lifelink — core weakness (exception: multicolor with W or B)"),

    # Blue cannot gain life
    ("U", r"(gain|gains) \d+ life", "Blue cannot gain life — core weakness"),
    ("U", r"\blifelink\b", "Blue does not get lifelink — core weakness"),

    # Blue cannot destroy artifacts or enchantments
    ("U", r"destroy target artifact", "Blue cannot destroy artifacts — blue interacts with artifacts via animation/theft"),
    ("U", r"destroy target (artifact or enchantment|enchantment or artifact)",
     "Blue cannot destroy artifacts or enchantments"),

    # Black cannot destroy enchantments unconditionally
    ("B", r"destroy target enchantment(?!.*(sacrifice|you control))",
     "Black's enchantment removal must require sacrifice — unconditional enchantment destruction is a break"),

    # White cannot draw cards unconditionally
    ("W", r"^draw (two|three|four|five|\d+) cards?\.?$",
     "White cannot draw cards without conditions — must be once-per-turn, creature-triggered, or opponent-dependent"),
]

# ---------------------------------------------------------------------------
# Significant bend patterns — these are rating 3 (needs discussion)
# ---------------------------------------------------------------------------
SIGNIFICANT_BEND_PATTERNS: list[tuple[str, str, str]] = [
    # Green card draw without creature/land condition
    ("G", r"draw (two|three|four|\d+) cards(?!.*(creature|land|power|toughness|permanent))",
     "Green card draw should be tied to creatures, lands, or board state (Harmonize problem)"),

    # Red drawing cards (not impulsive)
    ("R", r"draw (two|three|four|\d+) cards(?!.*(exile|discard|until end of turn))",
     "Red card draw must be impulsive (exile + play this turn), wheel, or rummage — not traditional draw"),

    # Green unconditional permanent removal
    ("G", r"destroy target (permanent|nonland permanent|noncreature)",
     "Green removal should require creatures (fight/bite) — unconditional permanent destruction is Beast Within territory"),

    # Blue mana ramp
    ("U", r"(add|adds) \{?\w\}? (to your mana pool|mana)",
     "Blue does not ramp — mana production is green primary, red secondary (temporary)"),
    ("U", r"create.* treasure token",
     "Blue creating Treasures was explicitly called a mistake (Ixalan) — mana production isn't blue"),

    # White hard counterspells
    ("W", r"counter target spell(?!.*(unless|pay|tax))",
     "White gets tax-based counters only (pay N more) — hard counters are blue's domain"),

    # Any color: colorless card with strong in-pie effect
    # (Can't easily pattern-match this — flagged by colorless_danger_check instead)
]

# ---------------------------------------------------------------------------
# Notable bend patterns — rating 2 (acceptable, document it)
# ---------------------------------------------------------------------------
NOTABLE_BEND_PATTERNS: list[tuple[str, str, str]] = [
    # Green self-mill (acceptable in graveyard sets)
    ("G", r"mill|put.* cards? from.* library.* graveyard",
     "Green self-mill: acceptable if the set has a graveyard theme, otherwise a bend toward blue/black"),

    # White reanimation (must be restricted)
    ("W", r"return.* creature.* from.* graveyard.* to.* battlefield",
     "White reanimation: acceptable if restricted to small creatures or creatures that died this turn"),

    # Red recursion of instants/sorceries
    ("R", r"return.* (instant|sorcery).* from.* graveyard",
     "Red instant/sorcery recursion: secondary, acceptable at uncommon+"),

    # Black lifegain (via drain only)
    ("B", r"(gain|gains) \d+ life(?!.*(drain|lose|loses|damage))",
     "Black lifegain should be tied to drain effects (opponent loses life, you gain) — pure lifegain is white/green"),
]


@dataclass
class CardFlag:
    """A single color pie flag on a card."""
    card_name: str
    mana_cost: str
    colors: list[str]
    card_type: str
    rarity: str
    rating: int  # 1-4
    effect_text: str
    violation: str
    category: str  # "core_weakness", "significant_bend", "notable_bend", "colorless_danger"


@dataclass
class ReviewResult:
    """Complete review results for a set."""
    set_name: str
    total_cards: int
    flags: list[CardFlag] = field(default_factory=list)
    clean_count: int = 0


def extract_colors(card: dict) -> list[str]:
    """Extract color identity from a card."""
    colors = card.get("color", card.get("colors", card.get("color_identity", [])))
    if isinstance(colors, str):
        return list(colors)
    return colors or []


def is_multicolor(card: dict) -> bool:
    return len(extract_colors(card)) > 1


def is_colorless(card: dict) -> bool:
    return len(extract_colors(card)) == 0


def check_core_weaknesses(card: dict) -> list[CardFlag]:
    """Check for core weakness violations (rating 4)."""
    flags = []
    colors = extract_colors(card)
    rules = (card.get("rules_text", "") or card.get("oracle_text", "") or "").lower()
    name = card.get("name", "Unknown")
    mana_cost = card.get("mana_cost", "")
    card_type = card.get("type", card.get("type_line", ""))
    rarity = card.get("rarity", "common").lower()

    if not rules.strip():
        return flags

    for violation_color, pattern, explanation in CORE_WEAKNESS_VIOLATIONS:
        if violation_color not in colors:
            continue

        if re.search(pattern, rules):
            # Exception: multicolor cards where the OTHER color provides the effect
            if is_multicolor(card) and violation_color in colors:
                other_colors = [c for c in colors if c != violation_color]
                # Check if the effect is in-pie for the other color(s)
                if _effect_covered_by_partner(pattern, explanation, other_colors):
                    # Downgrade to notable bend for multicolor
                    flags.append(CardFlag(
                        card_name=name, mana_cost=mana_cost, colors=colors,
                        card_type=card_type, rarity=rarity, rating=2,
                        effect_text=_extract_matching_line(rules, pattern),
                        violation=f"[Multicolor exception] {explanation} — but partner color(s) {other_colors} may provide this",
                        category="notable_bend"
                    ))
                    continue

            flags.append(CardFlag(
                card_name=name, mana_cost=mana_cost, colors=colors,
                card_type=card_type, rarity=rarity, rating=4,
                effect_text=_extract_matching_line(rules, pattern),
                violation=explanation,
                category="core_weakness"
            ))

    return flags


def check_significant_bends(card: dict) -> list[CardFlag]:
    """Check for significant bend patterns (rating 3)."""
    flags = []
    colors = extract_colors(card)
    rules = (card.get("rules_text", "") or card.get("oracle_text", "") or "").lower()
    name = card.get("name", "Unknown")
    mana_cost = card.get("mana_cost", "")
    card_type = card.get("type", card.get("type_line", ""))
    rarity = card.get("rarity", "common").lower()

    if not rules.strip():
        return flags

    for bend_color, pattern, explanation in SIGNIFICANT_BEND_PATTERNS:
        if bend_color not in colors:
            continue
        if re.search(pattern, rules):
            flags.append(CardFlag(
                card_name=name, mana_cost=mana_cost, colors=colors,
                card_type=card_type, rarity=rarity, rating=3,
                effect_text=_extract_matching_line(rules, pattern),
                violation=explanation,
                category="significant_bend"
            ))

    return flags


def check_notable_bends(card: dict) -> list[CardFlag]:
    """Check for notable bend patterns (rating 2)."""
    flags = []
    colors = extract_colors(card)
    rules = (card.get("rules_text", "") or card.get("oracle_text", "") or "").lower()
    name = card.get("name", "Unknown")
    mana_cost = card.get("mana_cost", "")
    card_type = card.get("type", card.get("type_line", ""))
    rarity = card.get("rarity", "common").lower()

    if not rules.strip():
        return flags

    for bend_color, pattern, explanation in NOTABLE_BEND_PATTERNS:
        if bend_color not in colors:
            continue
        if re.search(pattern, rules):
            flags.append(CardFlag(
                card_name=name, mana_cost=mana_cost, colors=colors,
                card_type=card_type, rarity=rarity, rating=2,
                effect_text=_extract_matching_line(rules, pattern),
                violation=explanation,
                category="notable_bend"
            ))

    return flags


def check_colorless_danger(card: dict) -> list[CardFlag]:
    """Check colorless cards for effects that bypass the color pie."""
    flags = []
    if not is_colorless(card):
        return flags

    rules = (card.get("rules_text", "") or card.get("oracle_text", "") or "").lower()
    name = card.get("name", "Unknown")
    mana_cost = card.get("mana_cost", "")
    card_type = card.get("type", card.get("type_line", ""))
    rarity = card.get("rarity", "common").lower()

    if not rules.strip():
        return flags

    # Check for effects that normally belong to specific colors
    colorless_concerns = [
        (r"draw (two|three|four|\d+) cards", "Efficient card draw on a colorless card — normally blue's domain. Every deck can access this."),
        (r"destroy target creature", "Creature destruction on a colorless card — normally black's domain."),
        (r"counter target spell", "Counterspells on a colorless card — normally blue's exclusive."),
        (r"destroy target enchantment", "Enchantment destruction on a colorless card — normally white/green."),
        (r"(gain|gains) \d+ life(?!.*pay)", "Significant lifegain on a colorless card — normally white's domain."),
        (r"search your library for.* land.* onto the battlefield", "Land ramp on a colorless card — normally green's exclusive."),
    ]

    for pattern, explanation in colorless_concerns:
        if re.search(pattern, rules):
            flags.append(CardFlag(
                card_name=name, mana_cost=mana_cost, colors=[],
                card_type=card_type, rarity=rarity, rating=3,
                effect_text=_extract_matching_line(rules, pattern),
                violation=f"[Colorless danger] {explanation}",
                category="colorless_danger"
            ))

    return flags


def _effect_covered_by_partner(pattern: str, explanation: str, partner_colors: list[str]) -> bool:
    """Check if a flagged effect is in-pie for at least one partner color in a multicolor card."""
    # Mapping: which colors naturally provide which flagged effects
    effect_providers = {
        "destroy": {"B", "W"},  # Black/white destroy creatures
        "exile": {"W"},  # White exiles
        "enchantment": {"W", "G"},  # White/green handle enchantments
        "artifact": {"R", "G", "W"},  # Red/green/white handle artifacts
        "counter": {"U"},  # Blue counters
        "life": {"W", "G", "B"},  # White/green/black gain life
        "lifelink": {"W", "B"},  # White/black get lifelink
        "damage": {"R"},  # Red deals damage
        "draw": {"U", "B"},  # Blue/black draw cards
    }

    for keyword, providers in effect_providers.items():
        if keyword in explanation.lower():
            if any(c in providers for c in partner_colors):
                return True
    return False


def _extract_matching_line(rules_text: str, pattern: str) -> str:
    """Extract the line from rules text that matches the pattern."""
    for line in rules_text.split("\n"):
        if re.search(pattern, line.lower()):
            return line.strip()[:120]
    # If no line match, return first 120 chars
    return rules_text.strip()[:120]


def review_set(set_data: dict) -> ReviewResult:
    """Review an entire set for color pie violations."""
    cards = set_data.get("cards", [])
    set_name = set_data.get("set_name", set_data.get("name", "Unnamed Set"))

    result = ReviewResult(set_name=set_name, total_cards=len(cards))

    for card in cards:
        card_flags = []
        card_flags.extend(check_core_weaknesses(card))
        card_flags.extend(check_significant_bends(card))
        card_flags.extend(check_notable_bends(card))
        card_flags.extend(check_colorless_danger(card))

        if card_flags:
            # Deduplicate: keep highest-severity flag per card per pattern
            seen = set()
            for f in card_flags:
                key = (f.card_name, f.violation[:50])
                if key not in seen:
                    seen.add(key)
                    result.flags.append(f)
        else:
            result.clean_count += 1

    # Sort by severity (highest first), then by card name
    result.flags.sort(key=lambda f: (-f.rating, f.card_name))

    return result


def format_report(result: ReviewResult) -> str:
    """Format review results as a markdown report."""
    breaks = [f for f in result.flags if f.rating == 4]
    sig_bends = [f for f in result.flags if f.rating == 3]
    noted_bends = [f for f in result.flags if f.rating == 2]

    lines: list[str] = []
    lines.append(f"# Color Pie Review: {result.set_name}")
    lines.append("")
    lines.append(f"Reviewed **{result.total_cards}** cards. "
                 f"Found **{len(breaks)} breaks**, **{len(sig_bends)} significant bends**, "
                 f"**{len(noted_bends)} noted bends**.")
    lines.append("")
    lines.append("*This is an automated first pass. Pattern matching catches mechanical violations "
                 "but cannot evaluate set context, theme justification, or philosophical nuance. "
                 "Layer human/LLM judgment on top of these findings.*")
    lines.append("")

    if breaks:
        lines.append("## Breaks (Must Change)")
        lines.append("")
        for f in breaks:
            lines.append(f"### {f.card_name} ({f.mana_cost}) — Rating: 4")
            lines.append(f"**Color(s):** {', '.join(f.colors) or 'Colorless'}  ")
            lines.append(f"**Type:** {f.card_type}  ")
            lines.append(f"**Rarity:** {f.rarity}  ")
            lines.append(f"**Flagged text:** {f.effect_text}  ")
            lines.append(f"**Violation:** {f.violation}")
            lines.append("")

    if sig_bends:
        lines.append("## Significant Bends (Needs Discussion)")
        lines.append("")
        for f in sig_bends:
            lines.append(f"### {f.card_name} ({f.mana_cost}) — Rating: 3")
            lines.append(f"**Color(s):** {', '.join(f.colors) or 'Colorless'}  ")
            lines.append(f"**Type:** {f.card_type}  ")
            lines.append(f"**Rarity:** {f.rarity}  ")
            lines.append(f"**Flagged text:** {f.effect_text}  ")
            lines.append(f"**Concern:** {f.violation}")
            lines.append("")

    if noted_bends:
        lines.append("## Noted Bends (Acceptable with Justification)")
        lines.append("")
        for f in noted_bends:
            lines.append(f"### {f.card_name} ({f.mana_cost}) — Rating: 2")
            lines.append(f"**Color(s):** {', '.join(f.colors) or 'Colorless'}  ")
            lines.append(f"**Note:** {f.violation}")
            lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Rating | Count | % |")
    lines.append("|--------|-------|---|")
    total_flagged = len(result.flags)
    total = result.total_cards
    lines.append(f"| 1 (Clean) | {result.clean_count} | {result.clean_count/total*100:.0f}% |" if total else "| 1 (Clean) | 0 | 0% |")
    lines.append(f"| 2 (Noted bend) | {len(noted_bends)} | {len(noted_bends)/total*100:.0f}% |" if total else "| 2 | 0 | 0% |")
    lines.append(f"| 3 (Significant bend) | {len(sig_bends)} | {len(sig_bends)/total*100:.0f}% |" if total else "| 3 | 0 | 0% |")
    lines.append(f"| 4 (Break) | {len(breaks)} | {len(breaks)/total*100:.0f}% |" if total else "| 4 | 0 | 0% |")
    lines.append("")

    # Most common violation types
    if result.flags:
        violation_counts: dict[str, int] = defaultdict(int)
        color_counts: dict[str, int] = defaultdict(int)
        for f in result.flags:
            # Extract a short category from the violation text
            violation_counts[f.category] += 1
            for c in f.colors:
                color_counts[c] += 1

        lines.append("**Violation breakdown by category:**")
        for cat, count in sorted(violation_counts.items(), key=lambda x: -x[1]):
            label = cat.replace("_", " ").title()
            lines.append(f"- {label}: {count}")
        lines.append("")

        if color_counts:
            lines.append("**Colors with most flags:**")
            for color, count in sorted(color_counts.items(), key=lambda x: -x[1]):
                color_name = {"W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green"}.get(color, color)
                lines.append(f"- {color_name} ({color}): {count}")
            lines.append("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Color pie review for MTG card files")
    ap.add_argument("set_path", type=Path, help="Path to set.json or card file")
    ap.add_argument("--out", type=Path, default=None, help="Output path for markdown report")
    args = ap.parse_args()

    with args.set_path.open() as f:
        data = json.load(f)

    # Handle both {"cards": [...]} and bare [...] formats
    if isinstance(data, list):
        data = {"cards": data, "set_name": args.set_path.stem}

    result = review_set(data)
    report = format_report(result)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote color pie review to {args.out}")
        print(f"  {len([f for f in result.flags if f.rating == 4])} breaks, "
              f"{len([f for f in result.flags if f.rating == 3])} significant bends, "
              f"{len([f for f in result.flags if f.rating == 2])} noted bends")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
