#!/usr/bin/env python3
"""
Vision Design Auditor

Validates that vision_handoff.md and vision_cardfile.json produced by the
Vision Designer skill meet quality and completeness requirements.

Handoff checks:
1. All required sections present
2. Three pillars defined
3. 2-4 named mechanics with serves_pillar
4. All 10 two-color archetypes defined
5. Signpost uncommons mentioned
6. Tone section present
7. Backup mechanics mentioned

Card file checks:
1. Valid JSON with correct structure
2. Rarity distribution (~81C/100U/30-40R/10-15M)
3. Color balance per rarity
4. Archetype support (cards per color pair)
5. Signpost gold uncommons for each pair
6. NWO complexity estimate at common

Usage:
    python vision_design_audit.py vision_handoff.md vision_cardfile.json
    python vision_design_audit.py vision_handoff.md vision_cardfile.json --json
"""

import sys
import re
import json
from pathlib import Path


COLORS = {"W", "U", "B", "R", "G"}
TWO_COLOR_PAIRS = [
    "WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG",
]


def audit_vision_design(handoff_text: str, cardfile_data: dict) -> dict:
    """Audit vision handoff and card file, return findings."""
    findings = {
        "errors": [],
        "warnings": [],
        "info": [],
        "pillars": [],
        "mechanics": [],
        "archetypes_found": [],
        "card_counts": {},
        "score": 0,
    }

    # ═══════════════════════════════════════════════════════════════
    # HANDOFF CHECKS
    # ═══════════════════════════════════════════════════════════════

    # ── Required sections ───────────────────────────────────────────
    handoff_sections = [
        ("Set Identity", r"##\s*Set Identity"),
        ("Three Pillars", r"##\s*(?:Three )?Pillars"),
        ("Mechanics", r"##\s*Mechanics"),
        ("Archetypes", r"##\s*(?:Ten )?(?:Two.Color )?Archetypes"),
        ("Tone", r"##\s*Tone"),
        ("Open Questions", r"##\s*Open Questions"),
    ]

    for name, pattern in handoff_sections:
        if not re.search(pattern, handoff_text, re.IGNORECASE):
            findings["errors"].append(
                f"Handoff missing required section: '{name}'"
            )

    # ── Set Identity checks ─────────────────────────────────────────
    identity_section = _extract_section(
        handoff_text, r"##\s*Set Identity", r"\n##\s"
    )
    if identity_section:
        identity_terms = ["elevator", "pitch", "selling", "orientation",
                          "emotional", "promise"]
        found = sum(1 for t in identity_terms if t in identity_section.lower())
        if found < 2:
            findings["warnings"].append(
                "Set Identity section may be missing key elements. "
                "Expected: elevator pitch, selling sentence, orientation, "
                "emotional promise."
            )

    # ── Pillar checks ───────────────────────────────────────────────
    pillar_section = _extract_section(
        handoff_text, r"##\s*(?:Three )?Pillars", r"\n##\s[^#]"
    )
    if pillar_section:
        pillar_headings = re.findall(
            r"###\s*(?:Pillar\s*\d+[:.]?\s*)?(.+?)$",
            pillar_section, re.MULTILINE
        )
        pillar_names = [p.strip() for p in pillar_headings
                        if len(p.strip()) < 100]
        findings["pillars"] = pillar_names

        num_pillars = len(pillar_names)
        if num_pillars < 3:
            findings["errors"].append(
                f"Only {num_pillars} pillar(s) defined (need exactly 3). "
                f"Found: {', '.join(pillar_names) if pillar_names else 'none'}"
            )
        elif num_pillars > 4:
            findings["warnings"].append(
                f"{num_pillars} pillars defined (target: exactly 3). "
                "More than 3 pillars risks unfocused design."
            )
        elif num_pillars == 3:
            findings["info"].append("3 pillars defined (correct).")
        else:
            findings["info"].append(f"{num_pillars} pillars defined (3 preferred, 4 acceptable).")

    # ── Mechanic checks ─────────────────────────────────────────────
    mechanic_section = _extract_section(
        handoff_text, r"##\s*Mechanics", r"\n##\s[^#]"
    )
    if mechanic_section:
        mech_headings = re.findall(
            r"###\s+(.+?)(?:\s*\((?:primary|secondary|backup)\))?\s*$",
            mechanic_section, re.MULTILINE | re.IGNORECASE
        )
        # Filter out "Backup Mechanics" heading
        mech_names = [m.strip() for m in mech_headings
                      if "backup" not in m.lower() and len(m.strip()) < 80]
        findings["mechanics"] = mech_names

        num_mechs = len(mech_names)
        if num_mechs < 2:
            findings["errors"].append(
                f"Only {num_mechs} named mechanic(s) (need 2-4)."
            )
        elif num_mechs > 5:
            findings["warnings"].append(
                f"{num_mechs} named mechanics (target: 2-4). "
                "Too many mechanics strain the complexity budget."
            )
        else:
            findings["info"].append(f"{num_mechs} named mechanics (target: 2-4).")

        # Check serves_pillar
        serves_pillar_count = len(re.findall(
            r"[Ss]erves?\s*[Pp]illar", mechanic_section
        ))
        if serves_pillar_count < num_mechs and num_mechs > 0:
            findings["warnings"].append(
                "Not all mechanics specify which pillar they serve. "
                "Every mechanic must name a pillar (no orphan mechanics)."
            )

        # Check for backup mechanics
        if "backup" not in mechanic_section.lower():
            findings["warnings"].append(
                "No backup mechanics mentioned. Vision should include "
                "1-2 backups that are fundamentally different from primaries."
            )

    # ── Archetype checks ────────────────────────────────────────────
    archetype_section = _extract_section(
        handoff_text, r"##\s*(?:Ten )?(?:Two.Color )?Archetypes", r"\n##\s[^#]"
    )
    if archetype_section:
        found_pairs = set()
        for pair in TWO_COLOR_PAIRS:
            if pair in archetype_section:
                found_pairs.add(pair)
        findings["archetypes_found"] = sorted(found_pairs)

        missing_pairs = set(TWO_COLOR_PAIRS) - found_pairs
        if missing_pairs:
            findings["errors"].append(
                f"Archetypes missing color pairs: "
                f"{', '.join(sorted(missing_pairs))}. All 10 required."
            )
        else:
            findings["info"].append("All 10 two-color archetypes present.")

        # Check for signpost mentions
        signpost_terms = ["signpost", "enabler", "payoff"]
        has_signposts = any(
            t in archetype_section.lower() for t in signpost_terms
        )
        if not has_signposts:
            findings["warnings"].append(
                "Archetypes section doesn't mention signpost uncommons. "
                "Each archetype needs an enabler + payoff uncommon pair."
            )

    # ── Tone checks ─────────────────────────────────────────────────
    tone_section = _extract_section(
        handoff_text, r"##\s*Tone", r"\n##\s"
    )
    if tone_section:
        if len(tone_section.strip()) < 80:
            findings["warnings"].append(
                "Tone section is very short. Should cover speed, "
                "emotional register, and hope-to-threat ratio."
            )

    # ── "What We Tried and Cut" check ───────────────────────────────
    tried_terms = ["tried and cut", "what we tried", "cut mechanic",
                   "explored and rejected", "dead mechanic"]
    has_tried = any(t in handoff_text.lower() for t in tried_terms)
    if not has_tried:
        findings["warnings"].append(
            "No 'What We Tried and Cut' section detected. Document "
            "explored-and-rejected mechanics for Set Design's reference."
        )

    # ═══════════════════════════════════════════════════════════════
    # CARD FILE CHECKS
    # ═══════════════════════════════════════════════════════════════

    if not cardfile_data:
        findings["errors"].append("No card file data to audit.")
        findings["score"] = max(0, 100 - len(findings["errors"]) * 10
                                - len(findings["warnings"]) * 3)
        return findings

    cards = cardfile_data.get("cards", [])
    if not cards:
        findings["errors"].append("Card file contains no cards.")
        findings["score"] = max(0, 100 - len(findings["errors"]) * 10
                                - len(findings["warnings"]) * 3)
        return findings

    # ── Rarity distribution ─────────────────────────────────────────
    rarity_counts = {}
    for card in cards:
        r = card.get("rarity", "unknown").lower()
        rarity_counts[r] = rarity_counts.get(r, 0) + 1
    findings["card_counts"] = rarity_counts

    commons = rarity_counts.get("common", 0)
    uncommons = rarity_counts.get("uncommon", 0)
    rares = rarity_counts.get("rare", 0)
    mythics = rarity_counts.get("mythic", 0)

    if commons < 70:
        findings["errors"].append(
            f"Only {commons} commons (target: ~81, minimum: 70)."
        )
    elif commons < 75 or commons > 87:
        findings["warnings"].append(
            f"{commons} commons (target: ~81)."
        )
    else:
        findings["info"].append(f"{commons} commons (target: ~81).")

    if uncommons < 80:
        findings["errors"].append(
            f"Only {uncommons} uncommons (target: ~100, minimum: 80)."
        )
    elif uncommons < 90 or uncommons > 110:
        findings["warnings"].append(
            f"{uncommons} uncommons (target: ~100)."
        )
    else:
        findings["info"].append(f"{uncommons} uncommons (target: ~100).")

    if rares + mythics < 20:
        findings["warnings"].append(
            f"Only {rares + mythics} rares+mythics (target: 40-55 for draft)."
        )
    else:
        findings["info"].append(
            f"{rares} rares + {mythics} mythics = {rares + mythics} total."
        )

    total = len(cards)
    findings["info"].append(f"Total cards: {total}")

    # ── Color balance at common ─────────────────────────────────────
    common_colors = {}
    for card in cards:
        if card.get("rarity", "").lower() != "common":
            continue
        for c in card.get("color", []):
            if c in COLORS:
                common_colors[c] = common_colors.get(c, 0) + 1

    if common_colors:
        for color in COLORS:
            count = common_colors.get(color, 0)
            if count < 10:
                findings["errors"].append(
                    f"Only {count} {color} commons (minimum: ~13)."
                )
            elif count < 12 or count > 18:
                findings["warnings"].append(
                    f"{count} {color} commons (target: 13-16)."
                )

        # Check color spread
        if common_colors:
            min_c = min(common_colors.values())
            max_c = max(common_colors.values())
            if max_c - min_c > 4:
                findings["warnings"].append(
                    f"Common color spread is {max_c - min_c} "
                    f"(max {max_c}, min {min_c}). Target: within 3."
                )

    # ── Color balance at uncommon ────────────────────────────────────
    uncommon_colors = {}
    for card in cards:
        if card.get("rarity", "").lower() != "uncommon":
            continue
        for c in card.get("color", []):
            if c in COLORS:
                uncommon_colors[c] = uncommon_colors.get(c, 0) + 1

    if uncommon_colors:
        for color in COLORS:
            count = uncommon_colors.get(color, 0)
            if count < 10:
                findings["warnings"].append(
                    f"Only {count} {color} uncommons (target: 14-20)."
                )

    # ── Signpost gold uncommons ─────────────────────────────────────
    gold_uncommons = set()
    for card in cards:
        if card.get("rarity", "").lower() != "uncommon":
            continue
        colors = card.get("color", [])
        if len(colors) == 2:
            pair = "".join(sorted(colors, key="WUBRG".index))
            gold_uncommons.add(pair)

    missing_signposts = set(TWO_COLOR_PAIRS) - gold_uncommons
    if missing_signposts:
        findings["warnings"].append(
            f"Missing gold uncommons for archetype pairs: "
            f"{', '.join(sorted(missing_signposts))}. "
            "Each pair needs at least one signpost uncommon."
        )
    else:
        findings["info"].append(
            "All 10 color pairs have gold uncommons."
        )

    # ── Creature/noncreature ratio at common ────────────────────────
    common_creatures = 0
    common_noncreatures = 0
    for card in cards:
        if card.get("rarity", "").lower() != "common":
            continue
        card_type = card.get("type", "").lower()
        if "creature" in card_type:
            common_creatures += 1
        else:
            common_noncreatures += 1

    if common_creatures + common_noncreatures > 0:
        creature_pct = common_creatures / (common_creatures + common_noncreatures)
        if creature_pct < 0.5:
            findings["warnings"].append(
                f"Only {common_creatures}/{common_creatures + common_noncreatures} "
                f"common creatures ({creature_pct:.0%}). Target: ~60%."
            )
        elif creature_pct > 0.75:
            findings["warnings"].append(
                f"{common_creatures}/{common_creatures + common_noncreatures} "
                f"common creatures ({creature_pct:.0%}). Target: ~60%."
            )
        else:
            findings["info"].append(
                f"Common creature ratio: {creature_pct:.0%} "
                f"({common_creatures} creatures / "
                f"{common_creatures + common_noncreatures} total)."
            )

    # ── NWO complexity estimate at common ───────────────────────────
    complex_commons = 0
    for card in cards:
        if card.get("rarity", "").lower() != "common":
            continue
        rules = card.get("rules_text", "")
        flags = 0
        # Multiple abilities (newline separated)
        if rules.count("\n") >= 2:
            flags += 1
        # Long rules text
        if len(rules) > 120:
            flags += 1
        # References zones
        zone_words = ["graveyard", "exile", "library", "hand"]
        if any(z in rules.lower() for z in zone_words):
            flags += 1
        if flags >= 2:
            complex_commons += 1

    if commons > 0:
        complexity_pct = complex_commons / max(commons, 1)
        if complexity_pct > 0.25:
            findings["warnings"].append(
                f"~{complex_commons} commons ({complexity_pct:.0%}) appear "
                f"complex (NWO target: ≤20%). Consider simplifying."
            )
        else:
            findings["info"].append(
                f"NWO estimate: ~{complex_commons} complex commons "
                f"({complexity_pct:.0%}, target ≤20%)."
            )

    # ── Required card fields ────────────────────────────────────────
    required_fields = ["name", "mana_cost", "color", "type", "rarity"]
    missing_field_cards = 0
    for card in cards[:20]:  # Sample first 20
        for field in required_fields:
            if field not in card:
                missing_field_cards += 1
                break
    if missing_field_cards > 0:
        findings["warnings"].append(
            f"{missing_field_cards} of first 20 cards missing required fields "
            f"({', '.join(required_fields)})."
        )

    # ═══════════════════════════════════════════════════════════════
    # SCORE
    # ═══════════════════════════════════════════════════════════════

    score = 100
    score -= len(findings["errors"]) * 10
    score -= len(findings["warnings"]) * 3
    findings["score"] = max(0, min(100, score))

    return findings


def _extract_section(text: str, start_pattern: str, end_pattern: str) -> str:
    """Extract text between a heading matching start_pattern and the next heading."""
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    if not start_match:
        return ""
    start_pos = start_match.end()
    end_match = re.search(end_pattern, text[start_pos + 1:], re.IGNORECASE)
    if end_match:
        return text[start_pos:start_pos + 1 + end_match.start()]
    return text[start_pos:]


def format_report(findings: dict) -> str:
    """Format findings as a readable markdown report."""
    lines = ["# Vision Design Audit Report\n"]

    score = findings["score"]
    if score >= 80:
        grade = "PASS"
    elif score >= 60:
        grade = "NEEDS WORK"
    else:
        grade = "INCOMPLETE"
    lines.append(f"**Quality Score: {score}/100 — {grade}**\n")

    # Summary
    lines.append(f"- Pillars: {len(findings['pillars'])}")
    lines.append(f"- Mechanics: {len(findings['mechanics'])}")
    lines.append(f"- Archetypes: {len(findings['archetypes_found'])}/10")
    if findings["card_counts"]:
        cc = findings["card_counts"]
        lines.append(
            f"- Cards: {cc.get('common', 0)}C / {cc.get('uncommon', 0)}U / "
            f"{cc.get('rare', 0)}R / {cc.get('mythic', 0)}M"
        )
    lines.append(f"- Errors: {len(findings['errors'])}")
    lines.append(f"- Warnings: {len(findings['warnings'])}")
    lines.append("")

    if findings["errors"]:
        lines.append("## Errors (must fix)\n")
        for e in findings["errors"]:
            lines.append(f"- {e}")
        lines.append("")

    if findings["warnings"]:
        lines.append("## Warnings (should fix)\n")
        for w in findings["warnings"]:
            lines.append(f"- {w}")
        lines.append("")

    if findings["info"]:
        lines.append("## Info\n")
        for i in findings["info"]:
            lines.append(f"- {i}")
        lines.append("")

    if findings["pillars"]:
        lines.append("## Pillars\n")
        for i, p in enumerate(findings["pillars"], 1):
            lines.append(f"{i}. {p}")
        lines.append("")

    if findings["mechanics"]:
        lines.append("## Mechanics\n")
        for m in findings["mechanics"]:
            lines.append(f"- {m}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python vision_design_audit.py "
            "<vision_handoff.md> <vision_cardfile.json> [--json]"
        )
        sys.exit(1)

    handoff_path = Path(sys.argv[1])
    cardfile_path = Path(sys.argv[2])
    use_json = "--json" in sys.argv

    if not handoff_path.exists():
        print(f"Error: Handoff file not found: {handoff_path}")
        sys.exit(1)

    handoff_text = handoff_path.read_text(encoding="utf-8")

    cardfile_data = {}
    if cardfile_path.exists():
        try:
            cardfile_data = json.loads(
                cardfile_path.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in card file: {e}")
            sys.exit(1)
    else:
        print(f"Warning: Card file not found: {cardfile_path}")

    findings = audit_vision_design(handoff_text, cardfile_data)

    if use_json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))

    sys.exit(0 if findings["score"] >= 80 else 1)


if __name__ == "__main__":
    main()
