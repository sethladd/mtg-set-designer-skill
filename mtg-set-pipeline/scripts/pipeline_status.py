#!/usr/bin/env python3
"""
pipeline_status.py - MTG set pipeline stage completion checker.

Usage:
    python pipeline_status.py path/to/working_directory [--out pipeline_status_report.md]

Checks:
  1. Stage completeness — which artifacts exist at each pipeline stage
  2. Artifact format — files are parseable and well-formed
  3. Data flow integrity — set.json gains expected fields at each stage
  4. Pipeline progress — reports current stage and next action
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


# --- Pipeline Stage Definitions ---

STAGES = [
    {
        "number": 1,
        "name": "Exploratory Design",
        "skill": "mtg-exploratory-designer",
        "artifacts": ["exploration_doc.md"],
        "set_json_fields": [],
        "description": "Mechanical space exploration",
    },
    {
        "number": 2,
        "name": "Creative Foundation",
        "skill": "mtg-worldbuilder OR mtg-ip-researcher",
        "artifacts": [
            # Either world_guide.md OR (ip_catalog.md + ip_constraints.md)
            # We check for at least one
        ],
        "alt_artifact_groups": [
            ["world_guide.md"],
            ["ip_catalog.md", "ip_constraints.md"],
        ],
        "set_json_fields": [],
        "description": "Worldbuilding or IP research",
    },
    {
        "number": 3,
        "name": "Vision Design",
        "skill": "mtg-vision-designer",
        "artifacts": ["vision_handoff.md", "vision_cardfile.json"],
        "set_json_fields": [],
        "description": "Set identity, pillars, mechanics, archetypes",
    },
    {
        "number": 4,
        "name": "Set Design",
        "skill": "mtg-set-designer",
        "artifacts": ["set.json"],
        "set_json_fields": ["id", "mana_cost", "type", "rarity", "rules_text"],
        "description": "Complete card file (~261 cards)",
    },
    {
        "number": 5,
        "name": "Color Pie Review",
        "skill": "mtg-color-pie-reviewer",
        "artifacts": ["color_pie_review.md"],
        "set_json_fields": [],
        "description": "Color pie compliance check",
    },
    {
        "number": 6,
        "name": "Play Design",
        "skill": "mtg-play-designer",
        "artifacts": ["play_design_report.md"],
        "set_json_fields": [],
        "description": "Balance testing, final numbers",
    },
    {
        "number": 7,
        "name": "Editing / Templating",
        "skill": "mtg-editor",
        "artifacts": ["editing_report.md"],
        "set_json_fields": ["id"],  # collector numbers
        "description": "Rules text templating, collector numbers",
    },
    {
        "number": 8,
        "name": "Creative Writing",
        "skill": "mtg-creative-writer",
        "artifacts": ["naming_guide.md"],
        "set_json_fields": ["name"],
        "description": "Card names and flavor text",
    },
    {
        "number": 9,
        "name": "Art Direction",
        "skill": "mtg-art-director",
        "artifacts": ["card_concepts.json"],
        "set_json_fields": ["art_description"],
        "description": "Card concepts and art descriptions",
    },
    {
        "number": 10,
        "name": "Card Rendering",
        "skill": "mtg-card-renderer",
        "artifacts": [],  # checks for card_images/ directory
        "set_json_fields": [],
        "description": "Rendered card images",
        "check_dir": "card_images",
    },
    {
        "number": 11,
        "name": "Product Architecture",
        "skill": "mtg-product-architect",
        "artifacts": ["product_brief.md"],
        "set_json_fields": [],
        "description": "Product suite definition",
    },
]


# --- Helpers ---

def check_json_parseable(path: Path) -> tuple[bool, str]:
    """Check if a file is valid JSON."""
    try:
        with path.open() as f:
            json.load(f)
        return True, "valid JSON"
    except json.JSONDecodeError as e:
        return False, f"invalid JSON: {e}"
    except Exception as e:
        return False, f"error reading: {e}"


def check_markdown_nonempty(path: Path) -> tuple[bool, str]:
    """Check if a markdown file exists and is non-empty."""
    try:
        content = path.read_text()
        if len(content.strip()) < 10:
            return False, "file is nearly empty"
        return True, f"{len(content)} chars"
    except Exception as e:
        return False, f"error reading: {e}"


def load_set_json(work_dir: Path) -> dict | None:
    """Load set.json if it exists."""
    path = work_dir / "set.json"
    if not path.exists():
        return None
    try:
        with path.open() as f:
            return json.load(f)
    except Exception:
        return None


def check_set_json_fields(
    set_data: dict, required_fields: list[str]
) -> list[str]:
    """Check that cards in set.json have the required fields."""
    flags: list[str] = []
    cards = set_data.get("cards", [])
    if not cards:
        return ["No cards found in set.json"]

    for field in required_fields:
        missing = sum(
            1 for c in cards
            if not c.get(field)
        )
        if missing > 0:
            coverage = (len(cards) - missing) / len(cards)
            if coverage < 0.9:
                flags.append(
                    f"FIELD-INCOMPLETE: '{field}' present on "
                    f"{len(cards) - missing}/{len(cards)} cards "
                    f"({coverage:.0%})"
                )
    return flags


# --- Main Assessment ---

def assess_pipeline(work_dir: Path) -> str:
    """Assess pipeline stage completion and produce a status report."""
    out: list[str] = []
    out.append("# Pipeline Status Report")
    out.append(f"\nWorking directory: `{work_dir}`")
    out.append("")

    set_data = load_set_json(work_dir)
    completed_stages: list[int] = []
    first_incomplete: int | None = None

    # Detect track
    has_world = (work_dir / "world_guide.md").exists()
    has_ip = (work_dir / "ip_catalog.md").exists()
    track = "original" if has_world else ("ub" if has_ip else "unknown")
    out.append(f"**Track:** {'Original World' if track == 'original' else 'Universes Beyond' if track == 'ub' else 'Not yet determined'}")
    out.append("")

    out.append("## Stage Status")
    out.append("")

    for stage in STAGES:
        num = stage["number"]
        name = stage["name"]
        artifacts = stage["artifacts"]
        fields = stage["set_json_fields"]
        issues: list[str] = []
        complete = True

        # Check artifacts
        if "alt_artifact_groups" in stage:
            # Stage 2: need at least one group fully present
            any_group_complete = False
            for group in stage["alt_artifact_groups"]:
                if all((work_dir / a).exists() for a in group):
                    any_group_complete = True
                    break
            if not any_group_complete:
                complete = False
                issues.append("No creative foundation artifacts found "
                              "(need world_guide.md OR ip_catalog.md)")
        else:
            for artifact in artifacts:
                path = work_dir / artifact
                if not path.exists():
                    complete = False
                    issues.append(f"Missing: {artifact}")
                else:
                    # Validate format
                    if artifact.endswith(".json"):
                        ok, msg = check_json_parseable(path)
                        if not ok:
                            issues.append(f"{artifact}: {msg}")
                    elif artifact.endswith(".md"):
                        ok, msg = check_markdown_nonempty(path)
                        if not ok:
                            issues.append(f"{artifact}: {msg}")

        # Check directory-based artifacts
        check_dir = stage.get("check_dir")
        if check_dir:
            dir_path = work_dir / check_dir
            if not dir_path.exists() or not dir_path.is_dir():
                complete = False
                issues.append(f"Missing directory: {check_dir}/")
            else:
                files = list(dir_path.glob("*.png"))
                if not files:
                    complete = False
                    issues.append(f"{check_dir}/ exists but contains no PNGs")

        # Check set.json fields
        if fields and set_data:
            field_issues = check_set_json_fields(set_data, fields)
            if field_issues:
                issues.extend(field_issues)
                # Field issues are warnings, not blockers
                # (partial coverage is allowed)

        # Record status
        status = "✓" if complete and not issues else "✗" if not complete else "⚠"
        if complete:
            completed_stages.append(num)
        elif first_incomplete is None:
            first_incomplete = num

        out.append(f"### Stage {num}: {name}")
        out.append(f"**Status:** {status} {'Complete' if complete else 'Incomplete'}")
        out.append(f"**Skill:** `{stage['skill']}`")
        if issues:
            for issue in issues:
                out.append(f"- {issue}")
        else:
            out.append(f"- All artifacts present and valid")
        out.append("")

    # Summary
    out.append("## Summary")
    out.append(f"- Completed stages: {len(completed_stages)}/{len(STAGES)}")
    out.append(f"- Stages completed: {', '.join(str(s) for s in completed_stages) or 'none'}")

    if set_data:
        cards = set_data.get("cards", [])
        out.append(f"- Cards in set.json: {len(cards)}")
        named = sum(1 for c in cards if c.get("name"))
        out.append(f"- Cards with names: {named}/{len(cards)}")
        with_art = sum(
            1 for c in cards
            if isinstance(c.get("art_description"), dict)
        )
        out.append(f"- Cards with art descriptions: {with_art}/{len(cards)}")

    out.append("")

    if first_incomplete:
        stage = STAGES[first_incomplete - 1]
        out.append(f"## Next Action")
        out.append(
            f"**Run Stage {first_incomplete}: {stage['name']}** "
            f"using `{stage['skill']}`"
        )
        out.append(f"- {stage['description']}")
    elif len(completed_stages) == len(STAGES):
        out.append("## Next Action")
        out.append("**Pipeline complete!** All stages finished.")
    else:
        out.append("## Next Action")
        out.append("**Review incomplete stages above and address issues.**")

    out.append("")
    return "\n".join(out)


# --- CLI ---

def main() -> int:
    ap = argparse.ArgumentParser(
        description="MTG pipeline stage completion checker"
    )
    ap.add_argument(
        "work_dir", type=Path,
        help="Path to the pipeline working directory"
    )
    ap.add_argument(
        "--out", type=Path, default=None,
        help="Output report path (default: stdout)"
    )
    args = ap.parse_args()

    if not args.work_dir.is_dir():
        print(f"Error: {args.work_dir} is not a directory", file=sys.stderr)
        return 1

    report = assess_pipeline(args.work_dir)

    if args.out:
        args.out.write_text(report)
        print(f"Wrote {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
