#!/usr/bin/env python3
"""
IP Catalog & Constraints Auditor

Validates that ip_catalog.md and ip_constraints.md produced by the IP
Researcher skill meet quality and completeness requirements. Checks:

1. Structure: All required sections present in both files
2. Character catalog: Adequate count, tier distribution, color assignments
3. Faction catalog: Present with color alignments
4. Color distribution: Computed and imbalances flagged
5. Must-include list: 30-50 elements with required fields
6. Naming conventions: Documented
7. System translations: At least 1 flagged
8. Constraints document: All required sections present

Usage:
    python ip_catalog_audit.py ip_catalog.md [ip_constraints.md]
    python ip_catalog_audit.py ip_catalog.md [ip_constraints.md] --json
"""

import sys
import re
import json
from pathlib import Path


COLORS = {"W", "U", "B", "R", "G"}
COLOR_WORDS = {
    "white": "W", "blue": "U", "black": "B", "red": "R", "green": "G",
}


def audit_ip_catalog(catalog_text: str, constraints_text: str = "") -> dict:
    """Audit an IP catalog (and optional constraints doc) and return findings."""
    findings = {
        "errors": [],
        "warnings": [],
        "info": [],
        "characters": [],
        "factions": [],
        "must_includes": 0,
        "score": 0,
    }

    # ── Catalog section checks ──────────────────────────────────────
    catalog_sections = [
        ("Scope", r"##\s*Scope"),
        ("Tone Assessment", r"##\s*Tone Assessment"),
        ("Character Catalog", r"##\s*Character Catalog"),
        ("Faction Catalog", r"##\s*Faction Catalog"),
        ("Location Catalog", r"##\s*Location Catalog"),
        ("Item Catalog", r"##\s*Item Catalog"),
        ("Story Beat Catalog", r"##\s*Story Beat Catalog"),
        ("Color Pie Distribution", r"##\s*Color Pie Distribution"),
        ("Must-Include List", r"##\s*Must.Include List"),
        ("Naming Conventions", r"##\s*Naming Conventions"),
        ("System Translation", r"##\s*System Translation"),
    ]

    for name, pattern in catalog_sections:
        if not re.search(pattern, catalog_text, re.IGNORECASE):
            findings["errors"].append(f"Missing required section: '{name}'")

    # ── Scope check ─────────────────────────────────────────────────
    scope_section = _extract_section(catalog_text, r"##\s*Scope", r"\n##\s")
    if scope_section and len(scope_section.strip()) < 30:
        findings["warnings"].append(
            "Scope section is very short. Should define which parts of the IP "
            "are covered and the target product format."
        )

    # ── Tone Assessment check ───────────────────────────────────────
    tone_section = _extract_section(
        catalog_text, r"##\s*Tone Assessment", r"\n##\s"
    )
    if tone_section:
        if len(tone_section.strip()) < 50:
            findings["warnings"].append(
                "Tone Assessment is very short. Should assess IP-Magic fit "
                "and audience compatibility."
            )
        # Check for fit keywords
        fit_terms = ["fit", "compatible", "match", "fantasy", "tone", "audience"]
        if not any(t in tone_section.lower() for t in fit_terms):
            findings["warnings"].append(
                "Tone Assessment doesn't discuss IP-Magic compatibility. "
                "Apply the Tone Compatibility Test."
            )

    # ── Character Catalog checks ────────────────────────────────────
    char_section = _extract_section(
        catalog_text, r"##\s*Character Catalog", r"\n##\s[^#]"
    )
    if char_section:
        char_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        char_matches = char_pattern.findall(char_section)
        char_names = [c.strip() for c in char_matches if len(c.strip()) < 80]
        findings["characters"] = char_names

        num_chars = len(char_names)
        if num_chars < 10:
            findings["errors"].append(
                f"Only {num_chars} characters in catalog (need 10+ for a viable set)."
            )
        elif num_chars < 20:
            findings["warnings"].append(
                f"{num_chars} characters in catalog. UB sets typically need "
                "20-30% of cards as named characters (40+ for a full set)."
            )
        else:
            findings["info"].append(f"{num_chars} characters in catalog.")

        # Check for required character fields
        char_fields = [
            ("Tier", [r"\*\*Tier[:*]", r"tier.*[12345]"]),
            ("Proposed color", [r"\*\*Proposed color", r"color.*[WUBRG]"]),
            ("Mechanical hook", [r"\*\*Mechanical", r"mechanical hook",
                                 r"card should feel"]),
        ]
        sampled = char_names[:5]  # Check first 5 characters
        for cname in sampled:
            csection = _extract_character_section(char_section, cname, char_names)
            if not csection:
                continue
            for field_name, patterns in char_fields:
                if not any(re.search(p, csection, re.IGNORECASE) for p in patterns):
                    findings["warnings"].append(
                        f"Character '{cname}' may be missing: {field_name}"
                    )
                    break  # Only report once per character to reduce noise

        # Check tier distribution
        tier_5_count = len(re.findall(
            r"\*\*Tier[:*]\*?\s*5", char_section, re.IGNORECASE
        ))
        if tier_5_count == 0:
            findings["warnings"].append(
                "No Tier 5 (mandatory) characters found. "
                "At least a few characters should be Tier 5."
            )

    # ── Faction Catalog checks ──────────────────────────────────────
    faction_section = _extract_section(
        catalog_text, r"##\s*Faction Catalog", r"\n##\s[^#]"
    )
    if faction_section:
        faction_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        faction_matches = faction_pattern.findall(faction_section)
        faction_names = [f.strip() for f in faction_matches if len(f.strip()) < 80]
        findings["factions"] = faction_names

        num_factions = len(faction_names)
        if num_factions < 2:
            findings["warnings"].append(
                f"Only {num_factions} faction(s) in catalog. Most IPs have "
                "3+ notable factions or organizations."
            )
        else:
            findings["info"].append(f"{num_factions} factions in catalog.")

        # Check for color alignment
        color_terms = ["color", "alignment", "WUBRG", "white", "blue", "black",
                       "red", "green"]
        has_colors = any(t in faction_section.lower() for t in color_terms)
        if not has_colors:
            findings["warnings"].append(
                "Faction Catalog doesn't appear to include color alignments. "
                "Each faction should have philosophy-based color mapping."
            )

    # ── Location Catalog check ──────────────────────────────────────
    loc_section = _extract_section(
        catalog_text, r"##\s*Location Catalog", r"\n##\s"
    )
    if loc_section:
        loc_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        loc_matches = loc_pattern.findall(loc_section)
        num_locations = len([l for l in loc_matches if len(l.strip()) < 80])
        if num_locations < 3:
            findings["warnings"].append(
                f"Only {num_locations} location(s). Most IPs have 5+ "
                "iconic locations worth cataloging."
            )
        else:
            findings["info"].append(f"{num_locations} locations in catalog.")

    # ── Item Catalog check ──────────────────────────────────────────
    item_section = _extract_section(
        catalog_text, r"##\s*Item Catalog", r"\n##\s"
    )
    if item_section:
        item_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        item_matches = item_pattern.findall(item_section)
        num_items = len([i for i in item_matches if len(i.strip()) < 80])
        if num_items < 3:
            findings["warnings"].append(
                f"Only {num_items} item(s). Consider iconic weapons, "
                "artifacts, or objects from the IP."
            )
        else:
            findings["info"].append(f"{num_items} items in catalog.")

    # ── Story Beat Catalog check ────────────────────────────────────
    story_section = _extract_section(
        catalog_text, r"##\s*Story Beat Catalog", r"\n##\s"
    )
    if story_section:
        story_pattern = re.compile(r"###\s+(.+?)$", re.MULTILINE)
        story_matches = story_pattern.findall(story_section)
        num_stories = len([s for s in story_matches if len(s.strip()) < 80])
        if num_stories < 3:
            findings["warnings"].append(
                f"Only {num_stories} story beat(s). Iconic moments become "
                "Sagas, instants, and sorceries."
            )
        else:
            findings["info"].append(f"{num_stories} story beats in catalog.")

    # ── Color Pie Distribution checks ───────────────────────────────
    color_section = _extract_section(
        catalog_text, r"##\s*Color Pie Distribution", r"\n##\s"
    )
    if color_section:
        # Check for table
        table_rows = re.findall(r"^\|(.+)\|$", color_section, re.MULTILINE)
        data_rows = [r for r in table_rows if not re.match(r"^[\s\-:|]+$", r)]
        if len(data_rows) < 6:  # header + 5 colors
            findings["warnings"].append(
                "Color Pie Distribution table may be incomplete. "
                "Need entries for all 5 colors."
            )

        # Check for gap/imbalance flagging
        gap_terms = ["gap", "underrepresented", "overrepresented", "imbalance",
                     "skew", "compensation", "below", "above"]
        has_gap_analysis = any(t in color_section.lower() for t in gap_terms)
        if not has_gap_analysis:
            findings["warnings"].append(
                "Color Pie Distribution doesn't flag imbalances. "
                "Every UB IP has color gaps — they must be identified."
            )
    else:
        pass  # Already flagged as missing section

    # ── Must-Include List checks ────────────────────────────────────
    must_section = _extract_section(
        catalog_text, r"##\s*Must.Include List", r"\n##\s"
    )
    if must_section:
        # Count must-include entries (look for list items or ### headings)
        list_items = re.findall(
            r"^[\-\*\d]+[\.\)]\s+.+$", must_section, re.MULTILINE
        )
        heading_items = re.findall(r"^###\s+.+$", must_section, re.MULTILINE)
        # Also count table rows
        table_items = re.findall(r"^\|(?!\s*[-:]+).+\|$", must_section, re.MULTILINE)
        # Use whichever count method found the most
        num_items = max(len(list_items), len(heading_items),
                        max(0, len(table_items) - 1))  # subtract header
        findings["must_includes"] = num_items

        if num_items < 15:
            findings["errors"].append(
                f"Only {num_items} must-include element(s) (target: 30-50). "
                "Apply the Riot Test more broadly."
            )
        elif num_items < 30:
            findings["warnings"].append(
                f"{num_items} must-include elements (target: 30-50). "
                "Consider whether more elements pass the Riot Test."
            )
        elif num_items > 60:
            findings["warnings"].append(
                f"{num_items} must-include elements (target: 30-50). "
                "If everything is must-include, nothing is. Tighten criteria."
            )
        else:
            findings["info"].append(
                f"{num_items} must-include elements (target: 30-50)."
            )

    # ── Naming Conventions check ────────────────────────────────────
    naming_section = _extract_section(
        catalog_text, r"##\s*Naming Conventions", r"\n##\s"
    )
    if naming_section:
        if len(naming_section.strip()) < 80:
            findings["warnings"].append(
                "Naming Conventions section is very short. Should document "
                "character/location naming patterns, IP terminology, "
                "linguistic register, and flavor text strategy."
            )
        # Check for flavor text strategy
        flavor_terms = ["flavor text", "quote", "voice", "register", "tone"]
        has_flavor = any(t in naming_section.lower() for t in flavor_terms)
        if not has_flavor:
            findings["warnings"].append(
                "Naming Conventions doesn't discuss flavor text strategy. "
                "Specify: direct quotes, mixed, or original in IP voice."
            )

    # ── System Translation check ────────────────────────────────────
    system_section = _extract_section(
        catalog_text, r"##\s*System Translation", r"\n##\s"
    )
    if system_section:
        if len(system_section.strip()) < 50:
            findings["warnings"].append(
                "System Translation section is very short. If the IP has "
                "interactive systems (game mechanics, magic systems, etc.), "
                "document translation candidates."
            )

    # ── Constraints document checks ─────────────────────────────────
    if constraints_text:
        constraint_sections = [
            ("Scope", r"##\s*Scope"),
            ("Must-Include", r"##\s*Must.Include"),
            ("Color Pie Distribution", r"##\s*Color"),
            ("Locked Flavor", r"##\s*Locked Flavor"),
            ("Flexibility Zones", r"##\s*Flexibility"),
            ("Naming Conventions", r"##\s*Naming"),
            ("Tone Assessment", r"##\s*Tone"),
        ]

        for name, pattern in constraint_sections:
            if not re.search(pattern, constraints_text, re.IGNORECASE):
                findings["warnings"].append(
                    f"Constraints document missing section: '{name}'"
                )

        # Check for color gap flags
        gap_terms = ["gap", "underrepresented", "compensation", "imbalance"]
        if not any(t in constraints_text.lower() for t in gap_terms):
            findings["warnings"].append(
                "Constraints document doesn't flag color gaps. "
                "Every UB IP has color imbalances that must be surfaced."
            )
    else:
        findings["warnings"].append(
            "No ip_constraints.md provided for audit. "
            "The constraints document is a required deliverable."
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
    lines = ["# IP Catalog Audit Report\n"]

    score = findings["score"]
    if score >= 80:
        grade = "PASS"
    elif score >= 60:
        grade = "NEEDS WORK"
    else:
        grade = "INCOMPLETE"
    lines.append(f"**Quality Score: {score}/100 — {grade}**\n")

    lines.append(f"- Characters cataloged: {len(findings['characters'])}")
    lines.append(f"- Factions cataloged: {len(findings['factions'])}")
    lines.append(f"- Must-include elements: {findings['must_includes']}")
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

    if findings["characters"]:
        lines.append("## Characters Found\n")
        for c in findings["characters"][:20]:  # Cap display at 20
            lines.append(f"- {c}")
        if len(findings["characters"]) > 20:
            lines.append(
                f"- ... and {len(findings['characters']) - 20} more"
            )
        lines.append("")

    if findings["factions"]:
        lines.append("## Factions Found\n")
        for f in findings["factions"]:
            lines.append(f"- {f}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python ip_catalog_audit.py <ip_catalog.md> "
            "[ip_constraints.md] [--json]"
        )
        sys.exit(1)

    catalog_path = Path(sys.argv[1])
    if not catalog_path.exists():
        print(f"Error: File not found: {catalog_path}")
        sys.exit(1)

    constraints_text = ""
    use_json = "--json" in sys.argv

    # Check for constraints file
    for arg in sys.argv[2:]:
        if arg == "--json":
            continue
        p = Path(arg)
        if p.exists():
            constraints_text = p.read_text(encoding="utf-8")

    catalog_text = catalog_path.read_text(encoding="utf-8")
    findings = audit_ip_catalog(catalog_text, constraints_text)

    if use_json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))

    sys.exit(0 if findings["score"] >= 80 else 1)


if __name__ == "__main__":
    main()
