# MTG Set Designer

A skill for designing complete, balanced, draftable Magic: The Gathering sets from a theme or idea. Designed for the **Play Booster era** (2024+).

Give it a theme — "deep-sea horror," "a world where spells leave behind echoes," "nomadic desert tribes fighting over water" — and it walks through the full design pipeline: vision, worldbuilding, mechanics, ten two-color draft archetypes, ~261 cards across four rarities, and automated balance testing. The output is structured files (JSON + markdown) ready for playtesting, not a loose pile of card ideas.

## What it's based on

The design process and heuristics are drawn from published sources by Wizards of the Coast designers, primarily Mark Rosewater's *Making Magic* column and *Drive to Work* podcast, plus design handoff documents and interviews with Erik Lauer, Aaron Forsythe, Ethan Fleischer, Melissa DeTora, and Doug Beyer. Key frameworks include the three-pillar vision model, New World Order complexity management, the ten two-color archetype grid (originating from Ravnica), the mechanical color pie, and the parasitic-vs-modular mechanic spectrum.

## How it works

The skill guides Claude through nine phases that mirror the real WotC pipeline (Vision Design → Set Design → Play Design), compressed into a single-designer workflow:

1. **Intake** — confirm theme, top-down vs. bottom-up, set size, constraints
2. **Theme Research** — web research, source material decomposition, faction-to-color mapping, resonance/anti-resonance inventories, tone calibration, cultural sensitivity scan. Produces a Theme Brief in the design doc.
3. **Vision** — elevator pitch, three pillars, tone and play feel
4. **Worldbuilding** — just enough world to justify creature types, factions, and card names
5. **Mechanics** — 2–4 named new mechanics, each assessed for parasitic risk
6. **Archetype grid** — 10 two-color archetypes with signpost uncommons and required commons
7. **Card file** — ~261 cards written commons-first using the design skeleton, then uncommons, rares, mythics
8. **Balance: heuristic pass** — automated checks on color distribution, creature curves, removal density, NWO complexity, archetype support, color pie violations
9. **Balance: simulated draft** — stochastic 8-player draft simulation reporting archetype win rates, card play rates, and format speed

## Output files

A finished set produces:

| File | Purpose |
|---|---|
| `design_doc.md` | Narrative design document — theme brief (with research sources), vision, pillars, worldbuilding, mechanics, archetypes |
| `set.json` | Every card with name, mana cost, type, rules text, P/T, rarity, color, flavor, archetype tags |
| `mechanics.json` | Each named mechanic with reminder text, color distribution, rarity spread, parasitic risk |
| `archetypes.json` | The 10 two-color archetypes with strategy, signpost uncommons, support requirements |
| `balance_report.md` | Heuristic check results and any documented intentional deviations |
| `sim_report.md` | Simulated draft results — archetype win rates, card play rates, format speed |

## Play Booster era targets

The skill designs for the current product format (Play Boosters replaced Draft Boosters in February 2024):

- **81 commons** (~14–15 per color) — fewer but higher-impact; no filler
- **100 uncommons** (~16–18 per color + ~20 gold signposts) — the largest rarity, carrying significant archetype support
- **60 rares, 20 mythics**
- **~261 unique cards total**

Pack structure: 14 playable cards (7C, 3U, 1R/M, 1 land, 2 wildcards). ~41% of packs contain 2+ rares, so common/uncommon removal is designed to answer rare-level threats.

## Directory structure

```
mtg-set-designer/
├── SKILL.md                      # Main skill — the 9-phase process
├── CLAUDE.md                     # Project instructions (source tracking rules)
├── references/
│   ├── art-direction.md            # WotC art brief format, card art best practices, set palette
│   ├── theme-research.md          # Theme exploration methodology and Theme Brief template
│   ├── vision.md                 # Three pillars, top-down vs. bottom-up
│   ├── color-pie.md              # Mechanical color pie, bending vs. breaking
│   ├── mechanics.md              # Keyword vs. ability word, parasitic vs. modular
│   ├── archetypes.md             # The 10 two-color archetype grid
│   ├── new-world-order.md        # Complexity at common, red-flag rules
│   ├── rarity-structure.md       # Play Booster rarity counts and jobs
│   ├── cycles.md                 # Cycle types and when to use them
│   ├── balance-heuristics.md     # Numerical targets the scripts check
│   ├── design-skeleton.md        # The WotC design skeleton concept and how to use it
│   ├── case-studies.md           # Innistrad, Ravnica, Theros, Lorwyn, Kamigawa, Zendikar
│   └── sources.md                # Web links used to build this skill (not per-set research)
├── scripts/
│   ├── balance_check.py          # Heuristic balance checker
│   ├── simulate_draft.py         # Stochastic draft-and-play simulator
│   └── set_schema.py             # JSON schema validator
├── assets/
│   ├── design_skeleton.json      # Official WotC design skeleton (Play Booster era)
│   ├── design_skeleton_2021.csv  # Community "Bones" spreadsheet (Draft Booster, historical)
│   └── set_template.json         # JSON schema example for set.json
└── evals/
    └── evals.json                # Test prompts used during skill development
```

## Scripts

**`balance_check.py`** — fast heuristic pass over a `set.json`. Reports per-color card counts, creature mana curves, removal density, New World Order red-flag ratio, color pie violation warnings, archetype support density, and mechanic spread vs. targets.

```
python scripts/balance_check.py set.json --out balance_report.md
```

**`simulate_draft.py`** — runs N simulated 8-player Play Booster drafts. Bots pick cards using color affinity and power heuristics, build 40-card decks, and play rough games. Reports archetype win rates (healthy band: 42–58%), card play rates, and average game length.

```
python scripts/simulate_draft.py set.json --pods 200 --out sim_report.md
```

**`set_schema.py`** — validates that `set.json` has required fields and consistent data. Accepts mechanics and archetypes either inlined in `set.json` or as sibling files.

```
python scripts/set_schema.py set.json
```

## Key design principles

These come from the reference material and inform every phase:

- **The set is more important than any one card.** A cool card that hurts the format gets cut.
- **Commons carry the set** (now alongside uncommons). If your theme only shows up at rare, you don't have a theme.
- **Parasitism is the default failure mode.** Every mechanic should work even if it's the only card with that mechanic in a draft deck.
- **Bleed to serve the set, never to fix a color's weakness.** The weaknesses are the point.
- **Complexity is finite.** Spend it where it matters.
- **Design, then test, then design again.** The balance scripts exist so you can be wrong quickly and cheaply.
