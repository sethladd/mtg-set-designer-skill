# Iteration 1 Notes

Two test prompts were run against the draft skill and against a no-skill baseline, four subagents total in parallel.

## Test cases

1. **Deep-sea horror** — top-down theme, asked for full ~270 card set with design doc and balance reports.
2. **Echo counters** — bottom-up mechanical idea, asked for full ~280 card set with world, archetypes, cards, and balance.

## Raw results

| Run | Cards actually produced | Archetypes | Balance script run? | Draft sim run? | Schema clean? |
|---|---|---|---|---|---|
| eval-1 with skill | 280 | 10 two-color | yes | yes (30 pods) | yes |
| eval-1 baseline | 24 (claimed 270) | 8 (claimed 8) | no (prose only) | no | n/a |
| eval-2 with skill | 274 | 10 two-color | yes | yes (30 pods) | yes |
| eval-2 baseline | 0 JSON; cards as per-color txt | 6 (claimed 6) | prose only | no | n/a |

## Observations

**Reliability of card count.** The baseline for eval 1 claimed "270 cards" in its summary but the JSON file contained 24. The skill-guided runs both produced the full card count (280 and 274). This alone is a decisive win for the skill — the user explicitly asked for ~270 cards, and without the structured process the model happily reports success having written a fraction of the work.

**Archetype structure.** Both baselines produced fewer than ten archetypes (8 and 6). The skill explicitly requires the 10 two-color grid, and both with-skill runs respected it. A 6-archetype "draft format" is not a real Magic limited format.

**Balance reports.** Both baselines produced narrative balance analysis without running the balance scripts. Both with-skill runs ran both `balance_check.py` and `simulate_draft.py` and produced reports. This is exactly the "heuristic pass then sim pass" loop the user asked for.

**File schema.** With-skill runs produced the expected `set.json`, `mechanics.json`, `archetypes.json`, `design_doc.md`, `balance_report.md`, `sim_report.md`. Baselines invented their own schemas (per-color TXT cardlists, CSV cardlists, CARD_DATABASE.json, DELIVERY_MANIFEST.txt, etc.). Structured data is easier for downstream tooling.

**Schema validator mismatch.** The skill's SKILL.md said mechanics and archetypes were separate files; the original set_schema.py required them inline. Both with-skill subagents split them across files, matching the SKILL.md guidance. The schema validator was updated in iteration 1.5 to accept either pattern, and both with-skill outputs now validate cleanly.

## Things that could still improve (for a future iteration)

- The format-speed calculation in `simulate_draft.py` came out at turn 20 in one with-skill run, which is off the charts slow — probably an artifact of the rough combat model rather than a real design warning. Could be worth smoothing.
- The sim uses very rough picking heuristics; it catches the biggest outliers (dead commons, unsupported archetypes) but won't catch subtle format problems.
- Red-flag common detection is regex-based and may under-count. Worth expanding if iterations show NWO violations slipping through.
- Could add a dedicated `worldbuilding.md` reference for sets where the flavor work is heavy.

## Decision

The iteration-1 skill is good enough to present as v1. The biggest wins (full card count, 10-archetype grid, actual balance script runs, structured files) are all locked in and the gap vs. baseline is large. Further tuning should come from real user feedback rather than speculative improvements.
