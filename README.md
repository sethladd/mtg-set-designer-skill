# MTG Set Design Pipeline

A 12-skill pipeline for designing complete, balanced, draftable Magic: The Gathering sets. Each skill mirrors a real role in Wizards of the Coast's production pipeline — from exploratory design through card rendering — compressed into an AI-driven workflow.

Give it a theme ("deep-sea horror," "a world where spells leave behind echoes") or an existing IP ("Final Fantasy," "Dune") and the pipeline walks through the full design process: exploration, worldbuilding, vision, set design, balance testing, editing, naming, art direction, and product architecture. The output is structured files (JSON + markdown) ready for playtesting or image rendering.

## The pipeline

```
USER INPUT: Theme/Concept OR IP Name
         |
         v
  1. Exploratory Designer -----> exploration_doc.md
         |
    [Branch: Original World OR Existing IP]
         |                          |
  2. Worldbuilder            3. IP Researcher
     world_guide.md             ip_catalog.md
         |__________________________|
         |
  4. Vision Designer -----------> vision_handoff.md + vision_cardfile.json
         |
  5. Set Designer ---------------> set.json (~261 cards)
         |
  6. Color Pie Reviewer ---------> color_pie_review.md  [feedback loop -> 5]
         |
  7. Play Designer --------------> play_design_report.md + set.json (final numbers) [feedback loop -> 5]
         |
  8. Editor ---------------------> set.json (templated) + editing_report.md
         |
  9. Creative Writer ------------> set.json (named, flavored) + naming_guide.md
         |
 10. Art Director ---------------> set.json (with art descriptions) + card_concepts.json
         |
 11. Card Renderer --------------> card_images/*.png
         |
 12. Product Architect ----------> product_brief.md + commander_precon_briefs.json
```

## The skills

| # | Skill | WotC Equivalent | What It Does |
|---|-------|----------------|--------------|
| 1 | `mtg-exploratory-designer` | Exploratory Design team | Surveys mechanical design space, ranks 8-15 candidate mechanics, recommends 3-5 directions |
| 2 | `mtg-worldbuilder` | Creative/Worldbuilding lead | Invents an original Magic plane with factions, creatures, geography, tone, and visual identity |
| 3 | `mtg-ip-researcher` | UB Creative / IP adaptation | Researches and catalogs an existing IP for Universes Beyond adaptation |
| 4 | `mtg-vision-designer` | Vision Design lead | Defines three pillars, selects mechanics, designs 10 two-color archetypes, produces handoff document |
| 5 | `mtg-set-designer` | Set Design lead | Builds the complete ~261-card file with balanced Limited format |
| 6 | `mtg-color-pie-reviewer` | Council of Colors | Reviews every card for color pie breaks and bends on a 1-4 scale |
| 7 | `mtg-play-designer` | Play Design team | Tests balance, finds combos, finalizes numbers, produces risk assessment |
| 8 | `mtg-editor` | Editing / Delta team | Templates rules text, assigns collector numbers, verifies name uniqueness |
| 9 | `mtg-creative-writer` | Names & Flavor Text writers | Names every card, writes flavor text, establishes naming culture |
| 10 | `mtg-art-director` | Art Director / Card Concepter | Concepts each card, writes structured art descriptions for every card |
| 11 | `mtg-card-renderer` | (rendering) | Renders card data as PNG images |
| 12 | `mtg-set-pipeline` | The pipeline itself | Orchestrates all skills in sequence with checkpoints and feedback loops |

Skills 2 and 3 are mutually exclusive — one runs per set depending on whether the user wants an original world or a Universes Beyond adaptation.

## Skill architecture

Every skill follows the same structure:

```
mtg-{skill-name}/
├── SKILL.md                    # Process steps, inputs, outputs, guiding principles
├── CLAUDE.md                   # Sources policy
├── references/
│   ├── wisdom-catalog.md       # Failure stories, counterintuitive insights, named heuristics
│   ├── {domain}-framework.md   # Operational handbook with decision trees and checklists
│   ├── sources.md              # All URLs researched during skill creation
│   └── {copied references}     # Self-contained copies of shared reference files
└── scripts/
    └── {audit}.py              # Automated validation checks
```

Each skill is self-contained — it carries copies of all reference files it needs, so it can run independently without depending on shared files.

## What it's based on

The design process and wisdom are drawn from published sources by Wizards of the Coast designers, primarily Mark Rosewater's Making Magic column and Drive to Work podcast, plus design handoff documents and interviews with Erik Lauer, Aaron Forsythe, Ethan Fleischer, Gavin Verhey, Melissa DeTora, Cynthia Sheppard, and Doug Beyer. Each skill's `references/sources.md` contains the full list of URLs consulted during its creation (400+ total across all skills).

Key frameworks encoded across the pipeline include: the three-pillar vision model, New World Order complexity management, the ten two-color archetype grid, the mechanical color pie, the parasitic-vs-modular spectrum, the WotC art description format (Setting/Color/Action/Focus/Mood), the Commander precon paradox, and the feedback loop protocol between Set Design and Play Design.

## Pipeline features

- **Two tracks**: Original Magic worlds (worldbuilder) or Universes Beyond IP adaptation (IP researcher) — downstream skills handle both
- **Bounded feedback loops**: Color Pie Review and Play Design can send cards back to Set Design, with a 2-iteration maximum and convergence checks
- **7 user checkpoints**: The orchestrator pauses for user review at key decision points (after exploration, worldbuilding, vision, set design, play design, naming, and final delivery)
- **Artifact-based state**: All pipeline state lives in files on disk, making the pipeline resumable across sessions
- **Automated audits**: Every skill has a Python audit script that validates its output (9 scripts total)

## Play Booster era targets

The pipeline designs for the current product format (Play Boosters replaced Draft Boosters in February 2024):

- **81 commons** (~14-15 per color)
- **100 uncommons** (~16-18 per color + ~20 gold signposts)
- **60 rares, 20 mythics**
- **~261 unique cards total**

## Installation

Clone the repo, then add it to Claude Code's project skill path. Each skill directory contains a `SKILL.md` that Claude will automatically discover.

### Option 1: Use the repo directly as your working directory

```bash
git clone https://github.com/sethladd/mtg_set_skill.git
cd mtg_set_skill
claude
```

Claude Code automatically loads skills from the current project. All 12 skills will be available immediately.

### Option 2: Install skills into an existing project

If you want to use these skills from a different project directory, add this repo's path to your Claude Code settings. Create or edit `~/.claude/settings.json`:

```json
{
  "skills": [
    "/path/to/mtg_set_skill/mtg-set-pipeline",
    "/path/to/mtg_set_skill/mtg-exploratory-designer",
    "/path/to/mtg_set_skill/mtg-worldbuilder",
    "/path/to/mtg_set_skill/mtg-ip-researcher",
    "/path/to/mtg_set_skill/mtg-vision-designer",
    "/path/to/mtg_set_skill/mtg-set-designer",
    "/path/to/mtg_set_skill/mtg-color-pie-reviewer",
    "/path/to/mtg_set_skill/mtg-play-designer",
    "/path/to/mtg_set_skill/mtg-editor",
    "/path/to/mtg_set_skill/mtg-creative-writer",
    "/path/to/mtg_set_skill/mtg-art-director",
    "/path/to/mtg_set_skill/mtg-product-architect"
  ]
}
```

Replace `/path/to/` with the actual path where you cloned the repo.

### Verify installation

Start Claude Code and ask:

```
What skills do you have available for MTG set design?
```

Claude should list the pipeline skills. You can also invoke any skill directly by name (e.g., "use the mtg-exploratory-designer skill").

## Running the pipeline

Start with the orchestrator:

```
Use the mtg-set-pipeline skill to design a complete Magic set based on [your theme or IP].
```

Or run individual skills standalone:

```
Use the mtg-exploratory-designer skill to explore mechanics for [your theme].
Use the mtg-vision-designer skill with this exploration document to create a vision.
Use the mtg-set-designer skill with this vision handoff to build the card file.
```

Each skill's SKILL.md documents its inputs, outputs, and process steps.

## Directory overview

```
mtg_set_skill/
├── mtg-exploratory-designer/       # Skill 1: Mechanical exploration
├── mtg-worldbuilder/               # Skill 2: Original world creation
├── mtg-ip-researcher/              # Skill 3: IP cataloging for Universes Beyond
├── mtg-vision-designer/            # Skill 4: Set identity and blueprint
├── mtg-set-designer/               # Skill 5: Complete card file construction
├── mtg-color-pie-reviewer/         # Skill 6: Color pie compliance review
├── mtg-play-designer/              # Skill 7: Balance testing and number finalization
├── mtg-editor/                     # Skill 8: Rules text templating and editing
├── mtg-creative-writer/            # Skill 9: Card naming and flavor text
├── mtg-art-director/               # Skill 10: Card concepts and art descriptions
├── mtg_card_maker/                 # Skill 11: Card image rendering
├── mtg-product-architect/          # Skill 12: Product suite definition
├── mtg-set-pipeline/               # Orchestrator: Runs the full pipeline
├── assets/                         # Shared templates (set_template.json, design skeletons)
├── old-references/                 # Legacy reference files (skills copy what they need)
├── scripts/                        # Shared utility scripts
├── mtg_set_design_pipeline_roles.md  # Pipeline specification document
└── skill_development_checklist.md    # Research targets and requirements per skill
```
