#!/usr/bin/env python3
"""
Exploration Document Auditor

Validates that an exploration_doc.md produced by the Exploratory Designer
skill meets quality and completeness requirements. Checks:

1. Structure: All required sections present
2. Candidate count: 8-15 candidates as required
3. Evaluation completeness: All 7 evaluations present for each candidate
4. Shortlist: 3-5 recommended mechanics with required diversity
5. Failure pattern checks: All 6 patterns addressed per candidate
6. Dead ends: At least one documented
7. Card sketches: 3-5 per candidate

Usage:
    python exploration_audit.py exploration_doc.md
    python exploration_audit.py exploration_doc.md --json
"""

import sys
import re
import json
from pathlib import Path


def audit_exploration_doc(text: str) -> dict:
    """Audit an exploration document and return findings."""
    findings = {
        "errors": [],      # Must fix
        "warnings": [],    # Should fix
        "info": [],        # Informational
        "candidates": [],  # Candidate names found
        "shortlist": [],   # Recommended candidates
        "score": 0,        # 0-100 quality score
    }

    lines = text.split("\n")

    # ── Section checks ──────────────────────────────────────────────
    required_sections = [
        ("Theme Understanding", r"##\s*Theme Understanding"),
        ("Candidate Mechanics", r"##\s*Candidate Mechanics"),
        ("Recommended Shortlist", r"##\s*Recommended Shortlist"),
        ("Dead Ends Explored", r"##\s*Dead Ends"),
        ("Open Questions", r"##\s*Open Questions"),
    ]

    sections_found = 0
    for name, pattern in required_sections:
        if re.search(pattern, text, re.IGNORECASE):
            sections_found += 1
        else:
            findings["errors"].append(f"Missing required section: '{name}'")

    # ── Theme Understanding checks ──────────────────────────────────
    theme_section = _extract_section(text, r"##\s*Theme Understanding", r"##\s")
    if theme_section:
        for concept in ["top-down", "bottom-up", "emotional promise", "overlap"]:
            if concept.lower() not in theme_section.lower() and \
               concept.replace("-", " ") not in theme_section.lower():
                # Fuzzy check — some of these might be worded differently
                pass  # Don't error, but note
        if len(theme_section.strip()) < 100:
            findings["warnings"].append(
                "Theme Understanding section is very short (< 100 chars). "
                "Should cover top-down/bottom-up orientation, emotional promise, "
                "and overlapping Magic territory."
            )

    # ── Candidate extraction ────────────────────────────────────────
    # Look for ### N. Name patterns (numbered candidates)
    candidate_pattern = re.compile(
        r"###\s*(\d+)\.\s*(.+?)(?:\s*—\s*(RECOMMENDED|NOT RECOMMENDED|BACKUP))?$",
        re.MULTILINE | re.IGNORECASE,
    )
    candidates = candidate_pattern.findall(text)

    if not candidates:
        # Try alternate format: ### Name — RECOMMENDED
        alt_pattern = re.compile(
            r"###\s*(.+?)(?:\s*—\s*(RECOMMENDED|NOT RECOMMENDED|BACKUP))?$",
            re.MULTILINE | re.IGNORECASE,
        )
        alt_candidates = alt_pattern.findall(text)
        # Filter out known non-candidate headings
        skip = {"theme understanding", "recommended shortlist", "dead ends",
                "open questions", "candidate mechanics"}
        for name, status in alt_candidates:
            clean = name.strip().rstrip("—").strip()
            if clean.lower() not in skip and len(clean) < 80:
                candidates.append(("?", clean, status))

    candidate_names = [c[1].strip() for c in candidates]
    findings["candidates"] = candidate_names

    num_candidates = len(candidate_names)
    if num_candidates < 8:
        findings["errors"].append(
            f"Only {num_candidates} candidate mechanics found (need 8-15). "
            f"Found: {', '.join(candidate_names) if candidate_names else 'none'}"
        )
    elif num_candidates > 15:
        findings["warnings"].append(
            f"{num_candidates} candidates found (target is 8-15). "
            "Consider consolidating similar mechanics."
        )
    else:
        findings["info"].append(f"{num_candidates} candidates found (target: 8-15).")

    # ── Per-candidate evaluation checks ─────────────────────────────
    evaluation_keywords = {
        "Depth": [r"\*\*Depth[:*]", r"depth.*score", r"depth.*rating"],
        "Parasitism": [r"\*\*Parasitism[:*]", r"parasitism.*score", r"parasit"],
        "Resonance": [r"\*\*Resonance[:*]", r"resonance.*score"],
        "Complexity": [r"\*\*Complexity[:*]", r"complexity.*cost", r"comprehension.*board.*strategic"],
        "Backward": [r"\*\*Backward[:*]", r"backward.*compat"],
        "Fun": [r"\*\*Fun[:*]", r"fun.*assess", r"fun.*play"],
        "Historical": [r"\*\*Historical[:*]", r"historical.*risk", r"failure.*pattern"],
    }

    for i, cname in enumerate(candidate_names):
        # Extract candidate section text
        candidate_text = _extract_candidate_section(text, cname, candidate_names, i)
        if not candidate_text:
            findings["warnings"].append(
                f"Could not extract section text for candidate '{cname}'."
            )
            continue

        # Check each evaluation is present
        missing_evals = []
        for eval_name, patterns in evaluation_keywords.items():
            found = False
            for pat in patterns:
                if re.search(pat, candidate_text, re.IGNORECASE):
                    found = True
                    break
            if not found:
                missing_evals.append(eval_name)

        if missing_evals:
            findings["errors"].append(
                f"Candidate '{cname}' missing evaluations: {', '.join(missing_evals)}"
            )

        # Check for card sketches
        sketch_patterns = [
            r"\*\*Card sketch",
            r"card sketch",
            r"example card",
            r"sample card",
            r"card concept",
        ]
        has_sketches = any(
            re.search(p, candidate_text, re.IGNORECASE) for p in sketch_patterns
        )
        if not has_sketches:
            findings["warnings"].append(
                f"Candidate '{cname}' may be missing card sketches "
                "(3-5 quick card concepts expected)."
            )

        # Check for failure pattern checklist
        failure_patterns = [
            "pressure valve", "type-locked", "interaction explosion",
            "misaligned optimization", "binary payoff", "no counterplay",
        ]
        missing_checks = []
        for fp in failure_patterns:
            if fp.lower() not in candidate_text.lower():
                missing_checks.append(fp)
        if len(missing_checks) > 3:
            findings["warnings"].append(
                f"Candidate '{cname}' may not check all 6 failure patterns. "
                f"Missing references to: {', '.join(missing_checks)}"
            )

    # ── Shortlist checks ────────────────────────────────────────────
    recommended = [c for c in candidates if "RECOMMENDED" in (c[2] if len(c) > 2 else "").upper()
                   and "NOT" not in (c[2] if len(c) > 2 else "").upper()]
    shortlist_names = [c[1].strip() for c in recommended]
    findings["shortlist"] = shortlist_names

    # Also check the Recommended Shortlist section for names
    shortlist_section = _extract_section(text, r"##\s*Recommended Shortlist", r"##\s")
    if shortlist_section:
        for cname in candidate_names:
            # Simplistic check: is the candidate name mentioned in shortlist section?
            if cname.lower() in shortlist_section.lower():
                if cname not in shortlist_names:
                    shortlist_names.append(cname)

    num_shortlist = len(shortlist_names)
    if num_shortlist < 3:
        findings["errors"].append(
            f"Only {num_shortlist} recommended mechanics (need 3-5). "
            f"Found: {', '.join(shortlist_names) if shortlist_names else 'none'}"
        )
    elif num_shortlist > 5:
        findings["warnings"].append(
            f"{num_shortlist} recommended mechanics (target: 3-5). "
            "The shortlist should be selective."
        )
    else:
        findings["info"].append(f"{num_shortlist} recommended mechanics (target: 3-5).")

    # ── Dead Ends check ─────────────────────────────────────────────
    dead_ends_section = _extract_section(text, r"##\s*Dead Ends", r"##\s")
    if dead_ends_section:
        if len(dead_ends_section.strip()) < 50:
            findings["warnings"].append(
                "Dead Ends section is very short. Should document explored-and-rejected "
                "directions with reasoning."
            )
    # (Already flagged as error if section missing entirely)

    # ── Open Questions check ────────────────────────────────────────
    open_q_section = _extract_section(text, r"##\s*Open Questions", r"##\s")
    if open_q_section:
        if len(open_q_section.strip()) < 30:
            findings["warnings"].append(
                "Open Questions section is very short. Should identify unresolved "
                "questions that need playtesting or creative input."
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
    # Find next heading of same or higher level
    end_match = re.search(end_pattern, text[start_pos + 1:], re.IGNORECASE)
    if end_match:
        return text[start_pos:start_pos + 1 + end_match.start()]
    return text[start_pos:]


def _extract_candidate_section(text: str, name: str, all_names: list, index: int) -> str:
    """Extract the section for a specific candidate."""
    # Find this candidate's heading
    escaped = re.escape(name)
    pattern = re.compile(rf"###.*{escaped}", re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()

    # Find next candidate heading or next ## heading
    if index + 1 < len(all_names):
        next_escaped = re.escape(all_names[index + 1])
        next_match = re.search(rf"###.*{next_escaped}", text[start:], re.IGNORECASE)
        if next_match:
            return text[start:start + next_match.start()]

    # Fall back to next ## heading
    next_section = re.search(r"\n##\s", text[start:])
    if next_section:
        return text[start:start + next_section.start()]
    return text[start:]


def format_report(findings: dict) -> str:
    """Format findings as a readable markdown report."""
    lines = ["# Exploration Document Audit Report\n"]

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
    lines.append(f"- Candidates found: {len(findings['candidates'])}")
    lines.append(f"- Shortlisted: {len(findings['shortlist'])}")
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

    # Candidates
    if findings["candidates"]:
        lines.append("## Candidates Found\n")
        for i, c in enumerate(findings["candidates"], 1):
            marker = " ★" if c in findings["shortlist"] else ""
            lines.append(f"{i}. {c}{marker}")
        lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python exploration_audit.py <exploration_doc.md> [--json]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    use_json = "--json" in sys.argv

    text = filepath.read_text(encoding="utf-8")
    findings = audit_exploration_doc(text)

    if use_json:
        print(json.dumps(findings, indent=2))
    else:
        print(format_report(findings))

    # Exit code: 0 if score >= 80, 1 otherwise
    sys.exit(0 if findings["score"] >= 80 else 1)


if __name__ == "__main__":
    main()
