#!/usr/bin/env python3
"""
World Guide Auditor

Validates that a world_guide.md produced by the Worldbuilder skill meets
quality and completeness requirements. Checks:

1. Structure: All required sections present
2. Factions: 3-5 factions, all 5 colors covered, cross-pollination
3. Creature type matrix: Parseable, adequate types, bridge types
4. Characters: 5+ named, across multiple factions, mechanical hooks
5. Visual identity: Through-line motif defined, set palette present
6. Geography: 3+ regions with associated factions
7. Archetype mapping: All 10 color pairs covered
8. Tone: Present and substantive

Usage:
    python worldbuilding_audit.py world_guide.md
    python worldbuilding_audit.py world_guide.md --json
"""

import sys
import re
import json
from pathlib import Path


# Known MTG colors
COLORS = {"W", "U", "B", "R", "G"}
COLOR_NAMES = {
    "W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green",
    "white": "W", "blue": "U", "black": "B", "red": "R", "green": "G",
}

# All 10 two-color pairs
TWO_COLOR_PAIRS = [
    "WU", "WB", "WR", "WG", "UB", "UR", "UG", "BR", "BG", "RG",
]


def audit_world_guide(text: str) -> dict:
    """Audit a world guide document and return findings."""
    findings = {
        "errors": [],
        "warnings": [],
        "info": [],
        "factions": [],
        "characters": [],
        "regions": [],
        "score": 0,
    }

    # ── Section checks ──────────────────────────────────────────────
    required_sections = [
        ("World Argument", r"##\s*World Argument"),
        ("Factions", r"##\s*Factions"),
        ("Creature Type Matrix", r"##\s*Creature Type Matrix"),
        ("Geography", r"##\s*Geography"),
        ("Visual Identity", r"##\s*Visual Identity"),
        ("Key Characters", r"##\s*Key Characters"),
        ("Tone", r"##\s*Tone"),
        ("Archetype Mapping", r"##\s*Archetype Mapping"),
    ]

    for name, pattern in required_sections:
        if not re.search(pattern, text, re.IGNORECASE):
            findings["errors"].append(f"Missing required section: '{name}'")

    # ── World Argument checks ───────────────────────────────────────
    argument_section = _extract_section(text, r"##\s*World Argument", r"\n##\s")
    if argument_section:
        # Check for thesis statement
        if not re.search(r"\*\*Thesis[:*]|\bthesis\b|^On\s", argument_section,
                         re.IGNORECASE | re.MULTILINE):
            findings["warnings"].append(
                "World Argument section may be missing a clear thesis statement. "
                "Expected format: 'On [plane name], [thesis].'"
            )
        # Check for mechanical connection
        if not re.search(r"[Pp]illar|[Mm]echanical connection", argument_section):
            findings["warnings"].append(
                "World Argument section doesn't reference mechanical pillars. "
                "The argument should map to the set's mechanical pillars."
            )
        if len(argument_section.strip()) < 80:
            findings["warnings"].append(
                "World Argument section is very short (< 80 chars)."
            )

    # ── Faction checks ──────────────────────────────────────────────
    factions_section = _extract_section(text, r"##\s*Factions", r"\n##\s[^#]")
    if factions_section:
        # Find faction headings (### Faction Name or ### Faction Name (XY))
        faction_pattern = re.compile(
            r"###\s+(.+?)(?:\s*\(([A-Z]{1,3}(?:/[A-Z]{1,3})?)\))?\s*$",
            re.MULTILINE,
        )
        faction_matches = faction_pattern.findall(factions_section)

        # Also look for color pair mentions within faction subsections
        faction_data = []
        for name, color_pair in faction_matches:
            name = name.strip().rstrip("(").strip()
            # If color pair not in heading, look for it in the section
            if not color_pair:
                faction_text = _extract_faction_section(factions_section, name)
                color_match = re.search(
                    r"(?:color[s ]?(?:pair|identity)?|colors?)[:]\s*([WUBRG]{1,3}(?:/[WUBRG]{1,3})?)",
                    faction_text, re.IGNORECASE,
                )
                if color_match:
                    color_pair = color_match.group(1).upper()
                else:
                    # Look for color words
                    found_colors = set()
                    for cword, csym in COLOR_NAMES.items():
                        if isinstance(csym, str) and len(csym) == 1:
                            if re.search(rf"\b{cword}\b", faction_text, re.IGNORECASE):
                                found_colors.add(csym)
                    if found_colors:
                        color_pair = "".join(sorted(found_colors,
                                                    key="WUBRG".index))
            faction_data.append({"name": name, "colors": color_pair or "?"})

        findings["factions"] = [f["name"] for f in faction_data]
        num_factions = len(faction_data)

        if num_factions == 0:
            findings["errors"].append(
                "No factions found. Expected 3-5 factions as ### headings "
                "within the Factions section."
            )
        elif num_factions < 3:
            findings["errors"].append(
                f"Only {num_factions} faction(s) found (need 3-5): "
                f"{', '.join(f['name'] for f in faction_data)}"
            )
        elif num_factions > 7:
            findings["errors"].append(
                f"{num_factions} factions found (max recommended: 5, hard limit: 7). "
                "Faction Ceiling Rule: too many factions means none are deep enough."
            )
        elif num_factions > 5:
            findings["warnings"].append(
                f"{num_factions} factions found (recommended: 3-5). "
                "Consider whether all factions have enough card density."
            )
        else:
            findings["info"].append(f"{num_factions} factions found (target: 3-5).")

        # Check color coverage
        all_colors_found = set()
        for fd in faction_data:
            if fd["colors"] and fd["colors"] != "?":
                for c in fd["colors"].replace("/", ""):
                    if c in COLORS:
                        all_colors_found.add(c)

        missing_colors = COLORS - all_colors_found
        if missing_colors and any(fd["colors"] != "?" for fd in faction_data):
            findings["errors"].append(
                f"Colors not represented in any faction: "
                f"{', '.join(COLOR_NAMES.get(c, c) for c in sorted(missing_colors))}. "
                "All 5 colors must be covered."
            )
        elif not any(fd["colors"] != "?" for fd in faction_data):
            findings["warnings"].append(
                "Could not determine color assignments for factions. "
                "Each faction should specify its color pair."
            )

        # Check for cross-pollination signals
        cross_poll_terms = [
            "share", "overlap", "bridge", "common", "both",
            "cross", "adjacent", "connect",
        ]
        has_cross_poll = any(
            term in factions_section.lower() for term in cross_poll_terms
        )
        if not has_cross_poll:
            findings["warnings"].append(
                "No cross-pollination language detected in Factions section. "
                "Each faction should share at least one element with an "
                "adjacent faction (Cross-Pollination Requirement)."
            )

        # Check per-faction required fields
        faction_fields = [
            ("Philosophy", [r"\*\*Philosophy", r"philosophy"]),
            ("Territory", [r"\*\*Territory", r"territory", r"homeland"]),
            ("Creature types", [r"\*\*Creature type", r"creature type"]),
            ("Visual identity", [r"\*\*Visual", r"visual identity"]),
            ("Mechanical archetype", [r"\*\*Mechanical", r"archetype", r"strategy"]),
        ]
        for fname in [f["name"] for f in faction_data]:
            fsection = _extract_faction_section(factions_section, fname)
            if not fsection:
                continue
            missing_fields = []
            for field_name, patterns in faction_fields:
                if not any(re.search(p, fsection, re.IGNORECASE) for p in patterns):
                    missing_fields.append(field_name)
            if missing_fields:
                findings["warnings"].append(
                    f"Faction '{fname}' may be missing: {', '.join(missing_fields)}"
                )

    # ── Creature Type Matrix checks ─────────────────────────────────
    matrix_section = _extract_section(text, r"##\s*Creature Type Matrix", r"\n##\s")
    if matrix_section:
        # Look for markdown table
        table_rows = re.findall(r"^\|(.+)\|$", matrix_section, re.MULTILINE)
        # Filter out separator rows
        data_rows = [r for r in table_rows if not re.match(r"^[\s\-:|]+$", r)]
        # First data row is header
        if len(data_rows) > 1:
            type_count = len(data_rows) - 1  # Subtract header
            if type_count < 8:
                findings["warnings"].append(
                    f"Only {type_count} creature types in matrix (recommend 8+)."
                )
            else:
                findings["info"].append(
                    f"{type_count} creature types in matrix."
                )

            # Check for P (primary) entries per color
            for color in COLORS:
                primary_count = 0
                for row in data_rows[1:]:
                    cells = [c.strip() for c in row.split("|")]
                    # Try to find columns with P values
                    if any("P" in cell and len(cell.strip()) <= 3
                           for cell in cells):
                        primary_count += 1
                # Can't reliably determine which column is which color,
                # so just check overall P density
            p_count = sum(
                1 for row in data_rows[1:]
                if "P" in row
            )
            if p_count < 5:
                findings["warnings"].append(
                    f"Only {p_count} creature types marked as Primary (P). "
                    "Each color needs 2-3 primary types."
                )
        else:
            findings["warnings"].append(
                "Creature Type Matrix table may be empty or unparseable."
            )

        # Check for bridge types
        bridge_terms = ["bridge", "span", "multiple", "cross"]
        has_bridge = any(term in matrix_section.lower() for term in bridge_terms)
        if not has_bridge:
            findings["warnings"].append(
                "No bridge types identified. At least 2 creature types "
                "should span 3+ colors for cross-faction drafting."
            )
    else:
        pass  # Already flagged as missing section

    # ── Character checks ────────────────────────────────────────────
    char_section = _extract_section(text, r"##\s*Key Characters", r"\n##\s")
    if char_section:
        # Find character headings
        char_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        char_matches = char_pattern.findall(char_section)
        char_names = [c.strip() for c in char_matches if len(c.strip()) < 60]
        findings["characters"] = char_names

        num_chars = len(char_names)
        if num_chars < 5:
            findings["errors"].append(
                f"Only {num_chars} named character(s) found (need 5-10)."
            )
        elif num_chars > 15:
            findings["warnings"].append(
                f"{num_chars} named characters found (target: 5-10). "
                "Consider whether all characters are necessary."
            )
        else:
            findings["info"].append(f"{num_chars} named characters (target: 5-10).")

        # Check for required character fields
        char_fields = [
            ("Color identity", [r"\*\*Color", r"color identity"]),
            ("Mechanical hook", [r"\*\*Mechanical", r"mechanical hook",
                                 r"card should feel"]),
            ("Faction", [r"\*\*Faction", r"faction"]),
        ]
        for cname in char_names:
            csection = _extract_character_section(char_section, cname, char_names)
            if not csection:
                continue
            for field_name, patterns in char_fields:
                if not any(re.search(p, csection, re.IGNORECASE) for p in patterns):
                    findings["warnings"].append(
                        f"Character '{cname}' may be missing: {field_name}"
                    )

        # Check faction distribution
        if findings["factions"] and char_names:
            factions_mentioned = set()
            for cname in char_names:
                csection = _extract_character_section(
                    char_section, cname, char_names
                )
                if csection:
                    for fname in findings["factions"]:
                        if fname.lower() in csection.lower():
                            factions_mentioned.add(fname)
            if len(factions_mentioned) < min(3, len(findings["factions"])):
                findings["warnings"].append(
                    f"Characters only span {len(factions_mentioned)} faction(s). "
                    "Characters should span at least 3 different factions."
                )

    # ── Visual Identity checks ──────────────────────────────────────
    visual_section = _extract_section(text, r"##\s*Visual Identity", r"\n##\s")
    if visual_section:
        # Check for through-line motif
        motif_terms = ["through-line", "throughline", "motif", "visual identity"]
        has_motif = any(term in visual_section.lower() for term in motif_terms)
        if not has_motif:
            findings["warnings"].append(
                "Visual Identity section may be missing a through-line motif. "
                "The world needs one visual motif described in a single phrase."
            )

        # Check for set palette
        palette_terms = ["sky", "material", "light source", "palette"]
        palette_count = sum(
            1 for term in palette_terms
            if term in visual_section.lower()
        )
        if palette_count < 2:
            findings["warnings"].append(
                "Visual Identity section may be missing set palette details "
                "(sky, materials, light sources, recurring shapes)."
            )

        # Check for per-faction variants
        if findings["factions"]:
            variants_found = sum(
                1 for fname in findings["factions"]
                if fname.lower() in visual_section.lower()
            )
            if variants_found < len(findings["factions"]) // 2:
                findings["warnings"].append(
                    "Visual Identity section may be missing per-faction variants. "
                    "Each faction should express the through-line differently."
                )

    # ── Geography checks ────────────────────────────────────────────
    geo_section = _extract_section(text, r"##\s*Geography", r"\n##\s")
    if geo_section:
        region_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        region_matches = region_pattern.findall(geo_section)
        region_names = [r.strip() for r in region_matches if len(r.strip()) < 60]
        findings["regions"] = region_names

        num_regions = len(region_names)
        if num_regions < 3:
            findings["warnings"].append(
                f"Only {num_regions} geographic region(s) found (recommend 3-5)."
            )
        else:
            findings["info"].append(f"{num_regions} geographic regions (target: 3-5).")

    # ── Archetype Mapping checks ────────────────────────────────────
    archetype_section = _extract_section(
        text, r"##\s*Archetype Mapping", r"\n##\s"
    )
    if archetype_section:
        # Check for all 10 color pairs
        found_pairs = set()
        for pair in TWO_COLOR_PAIRS:
            if pair in archetype_section:
                found_pairs.add(pair)

        missing_pairs = set(TWO_COLOR_PAIRS) - found_pairs
        if missing_pairs:
            findings["errors"].append(
                f"Archetype Mapping missing color pairs: "
                f"{', '.join(sorted(missing_pairs))}. All 10 must be covered."
            )
        else:
            findings["info"].append("All 10 two-color pairs present in Archetype Mapping.")

        # Check for table format
        table_rows = re.findall(r"^\|(.+)\|$", archetype_section, re.MULTILINE)
        data_rows = [r for r in table_rows if not re.match(r"^[\s\-:|]+$", r)]
        if len(data_rows) < 11:  # header + 10 pairs
            findings["warnings"].append(
                f"Archetype Mapping table has {max(0, len(data_rows) - 1)} "
                "data rows (expected 10, one per color pair)."
            )

    # ── Tone checks ─────────────────────────────────────────────────
    tone_section = _extract_section(text, r"##\s*Tone", r"\n##\s")
    if tone_section:
        if len(tone_section.strip()) < 100:
            findings["warnings"].append(
                "Tone section is very short (< 100 chars). Should cover "
                "emotional register, violence level, humor level, and "
                "hope-to-threat ratio."
            )
    # (Already flagged as error if section missing)

    # ── Open Creative Questions check ───────────────────────────────
    open_q_section = _extract_section(
        text, r"##\s*Open Creative Questions", r"\n##\s"
    )
    if not open_q_section:
        findings["warnings"].append(
            "No 'Open Creative Questions' section found. Consider listing "
            "unresolved questions for Vision Design."
        )

    # ── Compute quality score ───────────────────────────────────────
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


def _extract_faction_section(factions_text: str, name: str) -> str:
    """Extract the subsection for a specific faction within the Factions section."""
    escaped = re.escape(name)
    pattern = re.compile(rf"###\s*{escaped}", re.IGNORECASE)
    match = pattern.search(factions_text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"\n###\s", factions_text[start:])
    if next_heading:
        return factions_text[start:start + next_heading.start()]
    return factions_text[start:]


def _extract_character_section(
    char_text: str, name: str, all_names: list
) -> str:
    """Extract the subsection for a specific character."""
    escaped = re.escape(name)
    pattern = re.compile(rf"###\s*{escaped}", re.IGNORECASE)
    match = pattern.search(char_text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"\n###\s", char_text[start:])
    if next_heading:
        return char_text[start:start + next_heading.start()]
    return char_text[start:]


def format_report(findings: dict) -> str:
    """Format findings as a readable markdown report."""
    lines = ["# World Guide Audit Report\n"]

    # Score
    score = findings["score"]
    if score >= 80:
        grade = "PASS"
    elif score >= 60:
        grade = "NEEDS WORK"
    else:
        grade = "INCOMPLETE"
    lines.append(f"**Quality Score: {score}/100 — {grade}**\n")

    # Summary
    lines.append(f"- Factions found: {len(findings['factions'])}")
    lines.append(f"- Characters found: {len(findings['characters'])}")
    lines.append(f"- Regions found: {len(findings['regions'])}")
    lines.append(f"- Errors: {len(findings['errors'])}")
    lines.append(f"- Warnings: {len(findings['warnings'])}")
    lines.append("")

    # Errors
    if findings["errors"]:
        lines.append("## Errors (must fix)\n")
        for e in findings["errors"]:
            lines.append(f"- {e}")
        lines.append("")

    # Warnings
    if findings["warnings"]:
        lines.append("## Warnings (should fix)\n")
        for w in findings["warnings"]:
            lines.append(f"- {w}")
        lines.append("")

    # Info
    if findings["info"]:
        lines.append("## Info\n")
        for i in findings["info"]:
            lines.append(f"- {i}")
        lines.append("")

    # Factions
    if findings["factions"]:
        lines.append("## Factions Found\n")
        for f in findings["factions"]:
            lines.append(f"- {f}")
        lines.append("")

    # Characters
    if findings["characters"]:
        lines.append("## Characters Found\n")
        for c in findings["characters"]:
            lines.append(f"- {c}")
        lines.append("")

    # Regions
    if findings["regions"]:
        lines.append("## Regions Found\n")
        for r in findings["regions"]:
            lines.append(f"- {r}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python worldbuilding_audit.py <world_guide.md> [--json]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    use_json = "--json" in sys.argv

    text = filepath.read_text(encoding="utf-8")
    findings = audit_world_guide(text)

    if use_json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))

    # Exit code: 0 if score >= 80, 1 otherwise
    sys.exit(0 if findings["score"] >= 80 else 1)


if __name__ == "__main__":
    main()
