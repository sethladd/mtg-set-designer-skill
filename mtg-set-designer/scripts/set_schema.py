#!/usr/bin/env python3
"""
set_schema.py - validate set.json structure.

Usage:
    python set_schema.py path/to/set.json

Checks required fields and basic shape. Does not check balance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_SET_FIELDS = ["set_code", "set_name", "cards"]
OPTIONAL_SET_FIELDS = ["pillars", "mechanics", "archetypes"]
# mechanics and archetypes may also live in sibling mechanics.json / archetypes.json files;
# the validator accepts either pattern.
REQUIRED_CARD_FIELDS = ["id", "name", "mana_cost", "cmc", "color", "type", "rarity"]
REQUIRED_MECHANIC_FIELDS = ["name", "type", "reminder_text", "colors", "parasitic_risk"]
REQUIRED_ARCHETYPE_FIELDS = ["name", "strategy", "speed", "signpost_uncommons"]
VALID_RARITIES = {"common", "uncommon", "rare", "mythic"}
VALID_COLORS = {"W", "U", "B", "R", "G"}


def validate(set_data: dict, set_dir: Path | None = None) -> list[str]:
    errors: list[str] = []

    for f in REQUIRED_SET_FIELDS:
        if f not in set_data:
            errors.append(f"Missing required field: {f}")

    if "pillars" in set_data:
        if not isinstance(set_data["pillars"], list) or not (3 <= len(set_data["pillars"]) <= 4):
            errors.append("'pillars' should be a list of 3 or 4 strings")

    # Mechanics: inline or sibling file
    mechanics = set_data.get("mechanics")
    if mechanics is None and set_dir is not None:
        sibling = set_dir / "mechanics.json"
        if sibling.exists():
            mechanics = json.loads(sibling.read_text())
    if mechanics is None:
        errors.append("No mechanics found (neither inline nor in sibling mechanics.json)")
    else:
        mech_list = mechanics if isinstance(mechanics, list) else mechanics.get("mechanics", [])
        for i, m in enumerate(mech_list):
            for f in REQUIRED_MECHANIC_FIELDS:
                if f not in m:
                    errors.append(f"mechanics[{i}] missing field {f}")

    # Archetypes: inline or sibling file
    archetypes = set_data.get("archetypes")
    if archetypes is None and set_dir is not None:
        sibling = set_dir / "archetypes.json"
        if sibling.exists():
            archetypes = json.loads(sibling.read_text())
    if archetypes is None:
        errors.append("No archetypes found (neither inline nor in sibling archetypes.json)")
    elif not isinstance(archetypes, dict):
        errors.append("'archetypes' must be an object keyed by color pair")
    else:
        arch_map = archetypes.get("archetypes", archetypes)
        if not isinstance(arch_map, dict):
            arch_map = archetypes
        for pair, data in arch_map.items():
            if not isinstance(data, dict):
                continue
            for f in REQUIRED_ARCHETYPE_FIELDS:
                if f not in data:
                    errors.append(f"archetypes.{pair} missing field {f}")

    card_ids = set()
    for i, c in enumerate(set_data.get("cards", [])):
        for f in REQUIRED_CARD_FIELDS:
            if f not in c:
                errors.append(f"cards[{i}] ({c.get('name','?')}) missing field {f}")
        if c.get("rarity") not in VALID_RARITIES:
            errors.append(f"cards[{i}] ({c.get('name','?')}) invalid rarity: {c.get('rarity')}")
        for col in c.get("color", []) or []:
            if col not in VALID_COLORS:
                errors.append(f"cards[{i}] ({c.get('name','?')}) invalid color: {col}")
        cid = c.get("id")
        if cid in card_ids:
            errors.append(f"duplicate card id: {cid}")
        card_ids.add(cid)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: set_schema.py path/to/set.json", file=sys.stderr)
        return 2
    set_path = Path(sys.argv[1])
    data = json.loads(set_path.read_text())
    errors = validate(data, set_dir=set_path.parent)
    if errors:
        print(f"{len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("set.json validates cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
