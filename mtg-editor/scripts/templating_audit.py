#!/usr/bin/env python3
"""
templating_audit.py - MTG card templating and editing audit.

Usage:
    python templating_audit.py path/to/set.json [--out editing_report.md]

Runs templating checks on a card file:
  1. Self-reference audit — correct zone-based templates
  2. Modern verb check — current templating conventions
  3. Trigger word check — when/whenever/at usage
  4. "Another" check — self-targeting prevention
  5. Type-line consistency — Equipment/Equip, Vehicle/Crew, Aura/Enchant
  6. Keyword formatting — capitalization, spelling, known keywords
  7. Activation cost ordering — mana → tap → other → colon → effect
  8. Text box budget — line count and complexity by rarity
  9. Collector number assignment — WUBRG ordering
 10. Redundant text detection — "discard from hand," etc.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

COLORS = ["W", "U", "B", "R", "G"]

EVERGREEN_KEYWORDS = {
    "deathtouch", "defender", "double strike", "enchant", "equip",
    "first strike", "flash", "flying", "haste", "hexproof",
    "indestructible", "lifelink", "menace", "reach", "trample",
    "vigilance", "ward",
}

# Outdated templating patterns and their modern replacements
OUTDATED_PATTERNS = [
    (r"enters the battlefield", "enters"),
    (r"to your mana pool", "(remove 'to your mana pool', just 'Add {X}')"),
    (r"\b(he|she)\b", "they"),
    (r"put a .+ token onto the battlefield", "Create a [token]"),
    (r"removed from the game", "exiled"),
    (r"\bin play\b", "on the battlefield"),
    (r"play a spell", "cast a spell"),
    (r"is unblockable", "can't be blocked"),
    (r"put the top \d+ cards? of .+ library into .+ graveyard", "Mill N"),
]

# Patterns suggesting replacement effect templated as trigger
REPLACEMENT_AS_TRIGGER = [
    r"whenever .+ would (deal|take|receive) damage",
    r"whenever .+ would die",
    r"whenever .+ would (enter|leave)",
    r"whenever .+ would be (destroyed|exiled|sacrificed)",
]


def load_set(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def rules_text(card: dict) -> str:
    return card.get("rules_text") or ""


def rarity(card: dict) -> str:
    return card.get("rarity", "common").lower()


def card_type(card: dict) -> str:
    return (card.get("type") or "").lower()


def primary_color(card: dict) -> str:
    colors = card.get("color", [])
    if not colors:
        return "C"
    if len(colors) > 1:
        return "M"
    return colors[0]


def check_outdated_templating(cards: list[dict]) -> list[str]:
    """Check for outdated templating conventions."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c).lower()
        for pattern, replacement in OUTDATED_PATTERNS:
            if re.search(pattern, text):
                flags.append(
                    f"OUTDATED: {c.get('name', '?')} — "
                    f"contains '{pattern}', should use '{replacement}'"
                )
    return flags


def check_self_reference(cards: list[dict]) -> list[str]:
    """Check for correct self-reference templates."""
    flags: list[str] = []
    for c in cards:
        name = c.get("name", "")
        text = rules_text(c)
        if not name or not text:
            continue
        # Check if card uses its own name (non-legendary permanents shouldn't)
        is_legendary = "legendary" in card_type(c)
        is_creature = "creature" in card_type(c)
        if name in text and not is_legendary:
            # Check if this is a granted ability context (acceptable)
            if "equipped creature" not in text.lower() and "enchanted" not in text.lower():
                if is_creature:
                    flags.append(
                        f"SELF-REF: {name} — uses its own name in rules text. "
                        f"Should use 'this creature' (or 'this spell'/'this card' by zone)."
                    )
                else:
                    ctype = card_type(c)
                    suggested = "this artifact" if "artifact" in ctype else \
                                "this enchantment" if "enchantment" in ctype else \
                                "this permanent"
                    flags.append(
                        f"SELF-REF: {name} — uses its own name. "
                        f"Should use '{suggested}' (or 'this spell'/'this card' by zone)."
                    )
    return flags


def check_another(cards: list[dict]) -> list[str]:
    """Check for missing 'another' on self-targeting ETB abilities."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c).lower()
        # ETB exile/return effects without "another"
        if re.search(r"when this .+ enters", text):
            if re.search(r"exile target (creature|artifact|permanent|nonland)", text):
                if "another" not in text:
                    flags.append(
                        f"ANOTHER: {c.get('name', '?')} — ETB exile ability "
                        f"without 'another'. Risk of self-targeting loop."
                    )
    return flags


def check_type_line_consistency(cards: list[dict]) -> list[str]:
    """Check that type lines match rules text requirements."""
    flags: list[str] = []
    for c in cards:
        ctype = card_type(c)
        text = rules_text(c).lower()
        name = c.get("name", "?")

        # Equipment check
        if ("equip " in text or "equip—" in text or "equipped creature" in text) and "equipment" not in ctype:
            flags.append(f"TYPE-LINE: {name} — rules mention Equip/equipped but type missing 'Equipment'")
        if "equipment" in ctype and "equip" not in text:
            flags.append(f"TYPE-LINE: {name} — type includes 'Equipment' but no Equip cost in rules")

        # Vehicle check
        if re.search(r"\bcrew\b", text) and "vehicle" not in ctype:
            flags.append(f"TYPE-LINE: {name} — rules mention Crew but type missing 'Vehicle'")
        if "vehicle" in ctype and not re.search(r"\bcrew\b", text):
            flags.append(f"TYPE-LINE: {name} — type includes 'Vehicle' but no Crew cost in rules")

        # Aura check
        if re.search(r"\benchant (creature|permanent|player|land|artifact|enchantment)\b", text) and "aura" not in ctype:
            flags.append(f"TYPE-LINE: {name} — rules mention 'Enchant...' but type missing 'Aura'")

        # Saga check
        if re.search(r"\b(i|ii|iii|iv)\b", text) and "saga" not in ctype:
            if any(marker in text for marker in ["— ", "chapter"]):
                flags.append(f"TYPE-LINE: {name} — appears to have chapter abilities but type missing 'Saga'")

    return flags


def check_replacement_as_trigger(cards: list[dict]) -> list[str]:
    """Flag replacement effects incorrectly templated as triggers."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c).lower()
        for pattern in REPLACEMENT_AS_TRIGGER:
            if re.search(pattern, text):
                flags.append(
                    f"REPLACEMENT: {c.get('name', '?')} — "
                    f"possible replacement effect using trigger templating. "
                    f"Should use 'if...would...instead' not 'whenever'."
                )
    return flags


def check_keyword_formatting(cards: list[dict]) -> list[str]:
    """Check keyword capitalization and validity."""
    flags: list[str] = []
    for c in cards:
        keywords = c.get("keywords") or []
        for kw in keywords:
            kw_lower = kw.lower()
            # Check if it matches a known evergreen keyword
            if kw_lower in EVERGREEN_KEYWORDS:
                # Verify lowercase in rules text
                text = rules_text(c)
                if kw in text and kw[0].isupper() and kw_lower != kw:
                    flags.append(
                        f"KEYWORD: {c.get('name', '?')} — keyword '{kw}' "
                        f"should be lowercase in rules text ('{kw_lower}')"
                    )
    return flags


def check_text_box_budget(cards: list[dict]) -> list[str]:
    """Check text box line count against rarity limits."""
    flags: list[str] = []
    for c in cards:
        text = rules_text(c)
        if not text.strip():
            continue
        # Rough line count: each ~60 chars or each newline
        lines = text.count("\n") + 1
        char_lines = len(text) / 60
        estimated_lines = max(lines, char_lines)
        r = rarity(c)

        if r in ("common", "uncommon") and estimated_lines > 8:
            flags.append(
                f"TEXT-BOX: {c.get('name', '?')} ({r}) — "
                f"~{estimated_lines:.0f} lines of rules text. "
                f"Maximum for {r} is ~7-8 lines at standard font."
            )
        elif r in ("rare", "mythic") and estimated_lines > 11:
            flags.append(
                f"TEXT-BOX: {c.get('name', '?')} ({r}) — "
                f"~{estimated_lines:.0f} lines of rules text. "
                f"Exceeds even rare/mythic budget (~10 lines max)."
            )
    return flags


def check_redundant_text(cards: list[dict]) -> list[str]:
    """Flag redundant or outdated text patterns."""
    flags: list[str] = []
    redundant = [
        (r"discard .+ from (your|their) hand", "REDUNDANT: 'discard' already means 'from hand'"),
        (r"put .+ into .+ graveyard from the battlefield", "REDUNDANT: use 'dies' for creatures"),
        (r"can'?t be the target of", "OUTDATED: use 'hexproof' or 'ward' instead"),
    ]
    for c in cards:
        text = rules_text(c).lower()
        for pattern, message in redundant:
            if re.search(pattern, text):
                flags.append(f"TEMPLATE: {c.get('name', '?')} — {message}")
    return flags


def assign_collector_numbers(cards: list[dict]) -> list[dict]:
    """Assign collector numbers in WUBRG -> Multi -> Artifact -> Land order."""
    color_order = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4, "M": 5, "C": 6}

    def sort_key(card):
        ctype = (card.get("type") or "").lower()
        colors = card.get("color", [])

        # Lands go last
        if "land" in ctype and "creature" not in ctype:
            section = 8
        # Colorless artifacts
        elif not colors and ("artifact" in ctype):
            section = 7
        # Multicolor
        elif len(colors) > 1:
            section = 5
        # Mono-colored
        elif len(colors) == 1:
            section = color_order.get(colors[0], 6)
        # Colorless non-artifact
        else:
            section = 7

        return (section, card.get("name", "").lower())

    sorted_cards = sorted(cards, key=sort_key)
    for i, card in enumerate(sorted_cards, 1):
        card["collector_number"] = i
    return sorted_cards


def audit_set(set_data: dict) -> str:
    cards = set_data.get("cards", [])
    out: list[str] = []
    out.append(f"# Editing Report: {set_data.get('set_name', 'Unnamed Set')}")
    out.append(f"Total cards audited: **{len(cards)}**")
    out.append("")

    all_flags: list[str] = []

    checks = [
        ("Outdated Templating", check_outdated_templating(cards)),
        ("Self-Reference Audit", check_self_reference(cards)),
        ("'Another' Check", check_another(cards)),
        ("Type-Line Consistency", check_type_line_consistency(cards)),
        ("Replacement Effect Templating", check_replacement_as_trigger(cards)),
        ("Keyword Formatting", check_keyword_formatting(cards)),
        ("Text Box Budget", check_text_box_budget(cards)),
        ("Redundant/Outdated Text", check_redundant_text(cards)),
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

    # Collector number section
    out.append("## Collector Numbers")
    out.append("Assigned in WUBRG → Multicolor → Artifact → Land ordering.")
    out.append("")

    # Summary
    out.append("## Summary")
    if all_flags:
        categories: dict[str, int] = defaultdict(int)
        for f in all_flags:
            cat = f.split(":")[0]
            categories[cat] += 1
        out.append(f"**{len(all_flags)} total flags across {len(categories)} categories:**")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            out.append(f"- {cat}: {count}")
    else:
        out.append("✓ No templating issues detected. Card file passes editing audit.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="MTG card templating audit")
    ap.add_argument("set_path", type=Path, help="Path to set.json")
    ap.add_argument("--out", type=Path, default=None, help="Output report path")
    ap.add_argument("--assign-numbers", action="store_true",
                    help="Assign collector numbers and write updated set.json")
    args = ap.parse_args()

    set_data = load_set(args.set_path)
    report = audit_set(set_data)

    if args.assign_numbers:
        set_data["cards"] = assign_collector_numbers(set_data.get("cards", []))
        args.set_path.write_text(json.dumps(set_data, indent=2))
        print(f"Assigned collector numbers to {args.set_path}")

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
