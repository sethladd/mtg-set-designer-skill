# The Real MTG Set Production Pipeline — Mapped to Skills

## How Wizards of the Coast Actually Makes a Set

Magic sets are designed roughly **two years ahead** of release. The modern pipeline (post-2018, codified with Dominaria) splits into four sequential phases, each owned by a distinct team with a distinct mandate. Parallel to all of them, a Creative/Worldbuilding track runs on its own timeline, intersecting at key handoff points.

Here is the real pipeline, followed by the roles within it, followed by the proposed Skill for each.

---

## The Pipeline (Timeline)

```
YEAR 1                                          YEAR 2
├─ Exploratory Design (3 mo) ─┐
│                              ├─ Vision Design (6 mo) ─┐
│  Worldbuilding (parallel) ───┤                         │
│                              │                         ├─ Set Design (6 mo) ──────────┐
│                              │                         │   Art concepting begins       │
│                              │                         │   (3 mo into Set Design)      ├─ Play Design (3 mo) ─┐
│                              │                         │                               │                      ├─ Editing/Templating ─┐
│                              │                         │                               │                      │   Names & Flavor     ├─ PRINT
│                              │                         │                               │                      │   Final Art           │
└──────────────────────────────┴─────────────────────────┴───────────────────────────────┴──────────────────────┴──────────────────────┘
```

---

## The Roles

### 1. EXPLORATORY DESIGNER

**Real WotC role:** Exploratory Design is a small team (often led by Mark Rosewater) that meets twice weekly for ~3 months before Vision Design begins. They don't build a card file — they brainstorm design *spaces*. "What could a set about racing do?" "What mechanical territories does an underwater world open up?" They build quick prototype decks, jam games, and identify which ideas have the deepest design veins to mine.

**Key responsibilities:**
- Survey mechanical design space around a theme/world concept
- Identify which mechanics are "deep" (can support 50+ cards across rarities) vs. "shallow"
- Prototype rough decks to test whether ideas are fun to *play*, not just fun to read
- Flag potential rules problems early (consult the rules manager informally)
- Produce a shortlist of promising mechanical directions and anti-patterns to avoid
- Consider how the set interacts with the broader Standard environment and Magic product line

**Inputs:** A theme, world, or concept brief (often from Product Architecture / long-range planning)
**Outputs:** A design-space exploration document: promising mechanical veins, dead ends tried, and rough deck prototypes

**Proposed Skill: `mtg-exploratory-designer`**
> Given a theme/world/concept, exhaustively survey the mechanical design space. For each candidate mechanic or theme, assess depth (how many cards can it support?), parasitism (does it only work with itself?), backward compatibility (does it play well with existing Magic?), complexity budget (how much cognitive load does it add?), and fun factor. Output a ranked exploration document with 8-15 candidate mechanics/themes, each with a paragraph of reasoning, plus a shortlist of 3-5 recommended directions for Vision Design.

---

### 2. VISION DESIGNER (Lead)

**Real WotC role:** The Vision Design lead (historically Rosewater, but increasingly other designers like Chris Mooney, Doug Beyer, Ari Nieh) spends ~6 months establishing the *blueprint* for the set. They pick the mechanics, define the ten two-color draft archetypes, establish the set's "three pillars" (the three most important things the set must deliver), and hand off a playable card file with all commons and uncommons plus enough rares/mythics to draft.

**Key responsibilities:**
- Define the set's **three pillars** — the three non-negotiable things the set must deliver on
- Select and refine 3-5 named mechanics (keyword or ability word)
- Define the 10 two-color draft archetypes (theme, speed category, key synergies)
- Decide top-down vs. bottom-up orientation and ensure mechanics serve the chosen approach
- Design commons and uncommons that form the skeleton of Limited play
- Create signpost uncommons (gold cards that announce each archetype's strategy)
- Hand off a **vision design handoff document** to Set Design: goals, themes, mechanics, structure, open questions, backup mechanics
- Hand off a **card file** complete enough to draft

**Inputs:** Exploratory design findings; worldbuilding concepts from Creative
**Outputs:** Vision design handoff document + draftable card file (~200+ cards)

**Proposed Skill: `mtg-vision-designer`**
> Given exploratory findings and a world concept, produce the vision design handoff document and initial card file. Establish three pillars, select mechanics, define ten two-color archetypes, and design all commons and uncommons plus enough rares/mythics to draft. Include backup mechanics in case primary choices don't survive Set Design. Output: `vision_handoff.md` (the narrative document) and `vision_cardfile.json` (the draftable file).

---

## Two Creative Tracks: Original Worldbuilding vs. IP Research

Starting in 2021, WotC began running two parallel creative tracks instead of one. The **in-universe** track builds original Magic worlds (Bloomburrow, Duskmourn, Lorwyn Eclipsed). The **Universes Beyond** track adapts existing IPs (Lord of the Rings, Final Fantasy, Doctor Who, Fallout, Warhammer 40,000). As of 2025, roughly half of premier sets are Universes Beyond.

These are *fundamentally different creative jobs*, requiring different skills, different research, and different outputs. The rest of the pipeline is nearly identical between them — the divergence is almost entirely in this one phase.

In our pipeline, the user chooses one of two tracks at the start:

1. **Original Worldbuilding** — The user provides a theme, mood, or concept, and we invent a plane from scratch (the classic Magic process).
2. **IP Research & Cataloging** — The user names an existing IP (a book series, video game, film franchise, TV show), and we research and catalog it exhaustively to produce an adaptation-ready reference document (the Universes Beyond process).

Only one of these skills runs for a given set. The output of either feeds into the same downstream pipeline (Vision Design, Set Design, etc.) — but Vision Design behaves differently depending on which track was chosen, because IP sets have different constraints (locked character rosters, pre-existing factions, color pie mismatches, reprint limitations, earlier art commitment).

---

### 3A. WORLDBUILDER (Original Magic World)

**Real WotC role:** The Creative team (worldbuilding + art) works in parallel with Exploratory and Vision Design. A **creative lead** (e.g., Doug Beyer, Jenna Helland) is responsible for the world's identity — its races, cultures, geography, conflicts, visual identity, and tone. They work with concept artists during a 3-week "concept push" to generate a **style guide**: a 100+ page internal document that defines what everything on the plane looks like, from armor styles to architecture to flora and fauna.

**Key responsibilities:**
- Develop the world's setting: geography, cultures, factions, history, conflicts
- Define the plane's races, creatures, and notable characters (including Planeswalkers)
- Collaborate with concept artists (3-6 artists, ~3 weeks) to produce the **style guide**
- Ensure creative and mechanical themes reinforce each other (e.g., if the mechanic is "mutate," the world needs creatures that visually transform)
- Establish tone and mood (whimsical? gothic? epic? intimate?)
- Define which creature types map to which colors/archetypes
- Work with the Narrative team on story beats that will appear on cards

**Inputs:** Theme direction from Product Architecture; mechanical themes from Exploratory/Vision Design
**Outputs:** World guide / style guide; creature type matrix; faction descriptions; character profiles; tone/mood guide; story outline

**Proposed Skill: `mtg-worldbuilder`**
> Given a set's mechanical themes and pillars, **invent** a new Magic plane. Define factions, races, geography, key characters, creature type distribution by color, tone, and visual identity. Produce a world guide document that a card designer or artist could use as reference. Output: `world_guide.md` with sections for each faction/culture, a creature-type-to-color matrix, character profiles, and a tone/mood summary. Should explicitly map creative elements to mechanical archetypes (e.g., "The Tidecallers (UG) inhabit the reef cities and practice living architecture — this maps to the UG 'grow' archetype"). **This skill is for original Magic worlds only. For existing IPs, use `mtg-ip-researcher` instead.**

---

### 3B. IP RESEARCHER (Universes Beyond)

**Real WotC role:** For Universes Beyond sets, there is no worldbuilding — the world already exists. Instead, a team works with the IP rights holder (e.g., Middle-earth Enterprises for LotR, Square Enix for Final Fantasy) to exhaustively catalog the source material. They identify which characters matter, which events are iconic, which locations resonate, which factions map to the MTG color pie, and which elements of the IP are "must-haves" vs. nice-to-haves. The output is effectively a compressed encyclopedia of the IP, filtered for what will translate to a Magic set. Ethan Fleischer led the Warhammer 40,000 Commander set design; similar processes produced LotR: Tales of Middle-earth and Final Fantasy.

This is a research job, not a creative invention job. The challenges are fundamentally different:
- **Color pie mismatch**: Source IPs weren't built around WUBRG. Warhammer 40K is heavy on black and light on green. LotR has more whites and greens than blues or reds. The cataloging must explicitly flag these imbalances so Vision Design knows what to compensate for.
- **Character density vs. color balance**: The most iconic characters may all be in one or two colors. The catalog must identify enough characters across all five colors to fill a set.
- **Locked-in flavor**: Because rights holders approve art direction before cards are fully designed, concepts must be committed to much earlier. This means the catalog needs to be more complete and decisive than an original world guide.
- **Reprint constraints**: Existing Magic cards can only be reprinted in UB sets if their names and effects make sense within the IP. The catalog must identify candidate reprints.
- **"Must-include" lists**: Every IP has sacred cows — characters, items, locations, moments that the fanbase will riot if excluded. These must be identified with near-total coverage.
- **Power level of iconic moments**: Gandalf must feel like Gandalf. Cloud must feel like Cloud. Power level is dictated by fan expectation of iconic abilities, which can conflict with game balance.

**Key responsibilities:**
- Research the source IP exhaustively (books, games, films, canonical guides, wikis)
- Catalog every major character, faction, location, creature, item, and event
- Assign each catalog entry to a MTG color or color pair with reasoning
- Identify "must-include" elements the fanbase expects
- Identify iconic abilities, powers, and moments that could become mechanics
- Flag color pie imbalances (where the IP's natural distribution doesn't match MTG's even five-color split)
- Identify candidate Magic card reprints whose names/effects fit the IP
- Extract visual identity elements (art style, character designs, environmental aesthetics)
- Flag IP-specific terminology and naming conventions
- Document story beats that could become cards or entire set arcs
- Coordinate with IP rights holders on approvals (in the real process; in our pipeline, flag items that would normally need external approval)

**Inputs:** An existing IP name (e.g., "Lord of the Rings," "Final Fantasy VII," "Dune," "The Witcher"); optional fan preferences (favorite characters, specific games/books/seasons to emphasize)
**Outputs:** An IP catalog document structured for Vision Design consumption — functionally equivalent to a world guide, but derived from research rather than invention

**Proposed Skill: `mtg-ip-researcher`**
> Given the name of an existing IP, exhaustively research and catalog it into an adaptation-ready document. Use web search to find canonical sources (wikis, author statements, official guides, reputable fan references). Build a full catalog of characters, factions, locations, creatures, items, iconic moments, and visual identity elements. Assign each catalog entry to a MTG color or color pair with specific reasoning. Identify "must-include" elements the fanbase expects. Flag color pie imbalances in the source material. Identify candidate reprints from the existing Magic card pool. Extract naming conventions and terminology for use by the Creative Writer downstream. Output: `ip_catalog.md` (functionally equivalent to `world_guide.md`) plus an explicit `ip_constraints.md` that tells Vision Design what it CAN'T do (color pie mismatches, locked flavor elements, mandatory inclusions).

---

### 4. SET DESIGNER (Lead)

**Real WotC role:** The Set Design lead (e.g., Erik Lauer, Dave Humpherys, Corey Bowen) receives the vision handoff and spends ~6 months building the *actual* set. This is where theory meets reality. They field-test every mechanic, redesign cards that don't work, fill holes in the card file, manage the mana curve, tune power levels, balance the Limited environment, and ensure Constructed has appealing chase cards. Set Design has two sub-phases: a 6-month build phase and (after a 3-month gap) a 3-month finalization phase with Play Design.

**Key responsibilities:**
- Take Vision Design's blueprint and build it into a shippable card file
- Stress-test mechanics in actual Limited games — cut or replace mechanics that don't play well
- Design all remaining cards (rares, mythics, sideboard staples, build-arounds)
- Manage the **commons skeleton**: ensure each color has the right creature-to-spell ratio, curve, and removal suite
- Tune mana costs, power/toughness, and rider effects
- Ensure each archetype has sufficient enablers and payoffs at the right rarities
- Manage "as-fan" — the frequency at which mechanical themes appear in a typical booster
- Coordinate with Creative on card concepts (what each card represents in the world)
- Balance Limited speed (aggro, midrange, and control should all be viable)

**Inputs:** Vision design handoff document + card file; world guide
**Outputs:** Complete, balanced card file; updated design document reflecting all changes

**Proposed Skill: `mtg-set-designer`** *(existing — to be refactored)*
> The current `mtg-set-designer` skill tries to do everything. In the new pipeline, this skill should focus specifically on the Set Design phase: receive a vision handoff and card file, then iterate toward a balanced, complete set. Core work includes filling card holes, tuning curves, stress-testing mechanics via simulated drafts, managing as-fan, and producing the final card file. This is the most mechanically rigorous skill.

---

### 5. PLAY DESIGNER

**Real WotC role:** Play Design (created in 2017, originally led by Dan Burdick, with notable members like Melissa DeTora, Paul Cheon, Andrew Brown) focuses on the health of tournament formats. They work on the set for ~3 months, roughly one year before release. They have two sub-teams: **Competitive Play Design** (Standard, Draft, Sealed, Modern) and **Casual Play Design** (Commander, casual formats). Their job is to find broken cards, degenerate combos, and format-warping interactions *before* they ship.

**Key responsibilities:**
- Finalize mana costs, power/toughness, and other "numbers" on cards
- Playtest the set extensively in Constructed (Standard, Pioneer, Modern, Commander)
- Playtest Limited (Draft and Sealed) to verify archetype balance and format speed
- Identify cards that will warp formats and either weaken them or ensure answers exist
- Check for two-card infinite combos with existing cards in the format
- Verify that the best deck in each format isn't also the most fun-suppressing
- Ensure rares/mythics meant for Constructed actually see play (avoid "bulk rare" problems)
- Produce a play design report with power-level assessments and risk flags

**Inputs:** Near-final card file from Set Design
**Outputs:** Final-numbers card file; play design report (power outliers, format impact predictions, risk flags)

**Proposed Skill: `mtg-play-designer`**
> Given a near-complete card file, run competitive and casual play analysis. Simulate Limited games to verify archetype win rates are within bounds (45%-55%). Check for degenerate Constructed combos against a reference database of format staples. Flag cards whose rate (stats-to-cost ratio) exceeds historical norms. Verify each color has adequate removal, card advantage, and board presence. Output: `play_design_report.md` with per-archetype win rates, power outlier flags, combo warnings, and format health predictions.

---

### 6. COLOR PIE COUNCILOR

**Real WotC role:** The **Council of Colors** is a standing team of ~8 designers (overseen by Rosewater and Gottlieb) that reviews *every* card in *every* set to ensure color pie integrity. Each member is assigned a color (W, U, B, R, G, or colorless) and rates every card in that color on a 1-4 scale of color pie appropriateness. Cards rated above 2 are discussed by the full council. The council also makes long-term color pie evolution decisions (e.g., "green should get more haste").

**Key responsibilities:**
- Review every card in the set for color pie breaks (an effect in a color that shouldn't have it)
- Review for color pie bends (technically allowable but pushing boundaries)
- Rate each card on a 1-4 scale: 1 = fine, 2 = minor concern, 3 = significant bend, 4 = break
- Discuss all 3+ rated cards and recommend changes
- Maintain the canonical mechanical color pie reference document
- Make long-term color pie evolution recommendations

**Inputs:** Card file at any stage of design
**Outputs:** Color pie review report with ratings, flags, and recommended changes

**Proposed Skill: `mtg-color-pie-reviewer`**
> Given a card file, review every card against the canonical mechanical color pie (per Rosewater's 2021 Mechanical Color Pie article and subsequent updates). Flag breaks (hard violations), bends (pushing boundaries), and innovations (new territory being explored intentionally). Rate each card 1-4. Produce a `color_pie_review.md` report sorted by severity, with specific recommended fixes for each flagged card. Should understand primary/secondary/tertiary color assignments for all major mechanics.

---

### 7. CARD CONCEPTER / ART DIRECTOR

**Real WotC role:** Once card mechanics are near-final, the Creative team **concepts** each card — deciding what it represents in the world. A creature card might be concepted as "a reef guardian from the Tidecaller faction" or "a vampire noble from the Dusk Court." The Art Director then writes an **art description** (a structured prompt) for each card and commissions freelance artists. An AD at WotC commissions ~500+ pieces per year. They review sketches and finals, ensuring consistency with the style guide.

**Key responsibilities:**
- Concept each card: what creature/spell/object does it represent in the world?
- Write art descriptions (structured prompts with sections for: Setting, Color, Action, Focus, Mood)
- Commission artists (match artist style to card needs)
- Review sketch and final art for consistency with style guide
- Manage art budget and schedule
- Ensure mechanical identity matches visual identity (e.g., flying creatures look like they fly)

**Inputs:** Near-final card file; world guide / style guide
**Outputs:** Card concepts; art descriptions for every card; commissioned art

**Proposed Skill: `mtg-art-director`**
> Given a card file and world guide, produce card concepts and art descriptions for every card. Each art description follows the WotC format: Setting (plane, location), Color (MTG color identity / mood), Action (what's happening in the frame), Focus (the central subject), Mood (emotional tone). Art descriptions should be specific enough to commission from, referencing the style guide's visual language. Output: `card_concepts.json` (card name → concept mapping) and `art_descriptions.json` (card name → structured art prompt). This skill can also generate AI image prompts optimized for image generation tools.

---

### 8. EDITOR / TEMPLATER

**Real WotC role:** The Editing team (historically led by Del Laugel) works with the Rules Manager to ensure every card's rules text is correctly templated, unambiguous, and follows current Magic templating conventions. They manage reminder text, ensure text fits on cards, handle collector numbers, and give final approval before print. The team is often called the "Delta team."

**Key responsibilities:**
- Template all rules text according to current Magic conventions
- Ensure consistent keyword usage and reminder text
- Work with the Rules Manager to verify new mechanics work within the comprehensive rules
- Manage text fitting — ensure rules text + flavor text fit in the text box at legible size
- Assign collector numbers
- Verify card names don't conflict with existing cards
- Proofread everything

**Inputs:** Final card file
**Outputs:** Templated card file with correct formatting, reminder text, collector numbers

**Proposed Skill: `mtg-editor`**
> Given a card file, apply rigorous Magic templating rules. Verify keyword usage matches current Oracle standards. Add/correct reminder text. Check for templating inconsistencies (e.g., "When ~ enters the battlefield" is now "When this creature enters"). Flag rules text that's too long to fit on a card. Verify card names are unique and don't conflict with existing Magic cards. Assign collector numbers following WUBRG-then-multicolor-then-artifact-then-land ordering. Output: a corrected card file and an `editing_report.md` listing every change made and why.

---

### 9. NAMES & FLAVOR TEXT WRITER

**Real WotC role:** A creative lead for each set works with a team of writers (internal and freelance) to name every card and write flavor text. Each writer submits multiple options per card via an internal database. The creative lead selects the best options, working with the editing lead to ensure names fit on cards and don't conflict with existing names. Flavor text must serve worldbuilding, be evocative in ~15 words, and sometimes carry story weight.

**Key responsibilities:**
- Name every card (evocative, fits the world, mechanically suggestive, fits on the card)
- Write flavor text that builds the world in 1-2 sentences
- Maintain naming conventions (e.g., how this world names its spells, its creatures, its places)
- Ensure legendary creatures have appropriately weighty names
- Write reminder text for new mechanics (with the editing team)
- Keyword naming — give new mechanics their final published names

**Inputs:** Card file with concepts; world guide; style guide
**Outputs:** Named card file with flavor text

**Proposed Skill: `mtg-creative-writer`**
> Given a card file with mechanical text and card concepts, plus the world guide, name every card and write flavor text. Follow MTG naming conventions: spells are verbs or verb phrases, creatures are nouns or noun phrases, legendary creatures get proper names from the world's naming cultures. Flavor text should average 8-15 words, use em-dashes for attribution, and collectively build the world's story across the full set. Ensure no name conflicts with existing MTG cards. Output: updated card file with `name` and `flavor_text` fields populated, plus a `naming_guide.md` documenting the naming conventions used.

---

### 10. PRODUCT ARCHITECT

**Real WotC role:** The Product Architect (e.g., Mark Globus, Gavin Verhey, Mike Turian) oversees the product from a high level — how the set fits into the yearly release calendar, what booster products it appears in, how Commander decks relate to the main set, what the marketing hooks are. They're the connective tissue between R&D, Brand, and Production.

**Key responsibilities:**
- Define what products the set appears in (Play Boosters, Collector Boosters, Commander decks, Bundles)
- Ensure the set has clear marketing hooks (exciting mechanics, chase cards, thematic appeal)
- Coordinate timing with other releases in the calendar year
- Define Commander precon themes that complement the main set
- Interface between R&D and Brand/Marketing

**Inputs:** Set vision and card file at various stages
**Outputs:** Product brief; Commander precon briefs; marketing hook document

**Proposed Skill: `mtg-product-architect`** *(lower priority — more relevant for complete product suites)*
> Given a set's design document and card file, define the product suite: Commander precon themes (2-4 decks), Collector Booster special treatments, Bundle promo candidates, and marketing hooks. Identify the set's "poster cards" — the 3-5 cards that will drive excitement. Suggest Commander precon commanders that synergize with but aren't required by the main set's themes.

---

## The Orchestration Layer

Beyond individual roles, the real pipeline needs an **orchestrator** — something that runs the pipeline end-to-end, passing outputs from one skill to the next, and handling the feedback loops (e.g., Play Design sends cards back to Set Design for revision).

**Proposed Skill: `mtg-set-pipeline`**
> The master orchestrator. Given a starting concept, run the full pipeline: Exploratory → Vision → Worldbuilding (parallel with Vision) → Set Design → Color Pie Review → Play Design → Editing → Creative Writing → Art Direction. Handle feedback loops (Play Design flagging cards for Set Design revision; Color Pie Review sending cards back). Produce all final artifacts. This skill calls the other skills in sequence, manages state between phases, and presents checkpoints to the user.

---

## Proposed Skill Inventory (Summary)

| # | Skill Name | WotC Equivalent | Primary Output |
|---|-----------|----------------|----------------|
| 1 | `mtg-exploratory-designer` | Exploratory Design team | Design-space exploration document |
| 2 | `mtg-vision-designer` | Vision Design lead | Vision handoff doc + draftable card file |
| 3A | `mtg-worldbuilder` | Creative/Worldbuilding lead (in-universe) | World guide (invented plane) |
| 3B | `mtg-ip-researcher` | UB Creative / IP adaptation team | IP catalog + constraints document |
| 4 | `mtg-set-designer` | Set Design lead (refactor existing) | Complete, balanced card file |
| 5 | `mtg-play-designer` | Play Design team | Play design report, final numbers |
| 6 | `mtg-color-pie-reviewer` | Council of Colors | Color pie review report |
| 7 | `mtg-art-director` | Art Director / Card Concepter | Card concepts + art descriptions |
| 8 | `mtg-editor` | Editing / Delta team | Templated card file + editing report |
| 9 | `mtg-creative-writer` | Names & Flavor Text writers | Named cards with flavor text |
| 10 | `mtg-product-architect` | Product Architecture | Product suite brief |
| 11 | `mtg-card-renderer` | (already exists) | Card image PNGs |
| 12 | `mtg-set-pipeline` | The overall process itself | Orchestrates everything |

**Note:** Skills 3A and 3B are mutually exclusive for any given set — one or the other runs based on whether the user wants an original world or an IP adaptation. Both produce the same downstream artifact (a world guide / catalog) but through fundamentally different processes.

---

## How the Skills Chain Together

```
User provides: Theme / World / Concept  — OR —  Existing IP name
         │
         ▼
┌─────────────────────────┐
│ mtg-exploratory-designer │  ← "What design space exists?"
└────────────┬────────────┘
             │ exploration_doc.md
             ▼
      ┌──────┴──────┐
      │  Which      │
      │  track?     │
      └──┬───────┬──┘
         │       │
  Original│     │Existing IP
      │       │
      ▼       ▼
┌─────────────┐   ┌──────────────────┐
│mtg-          │   │ mtg-ip-researcher │
│worldbuilder  │   │ (research & catalog)
│(invent world)│   └────────┬─────────┘
└──────┬──────┘            │
       │                    │
       │   ip_catalog.md +  │
       │   ip_constraints.md│
       │                    │
       │  world_guide.md    │
       │                    │
       └─────────┬──────────┘
                 │
                 ▼
    ┌──────────────────────┐
    │ mtg-vision-designer  │  ← Consumes either world guide
    └──────────┬───────────┘     OR ip catalog + constraints
               │ vision_handoff.md
               │ vision_cardfile.json
               ▼
    ┌──────────────────────┐
    │ mtg-set-designer     │  ← Build the real set
    └──────────┬───────────┘
               │ set.json (draft 1)
               ▼
    ┌────────────────────────┐
    │ mtg-color-pie-reviewer │  ← "Any color pie breaks?"
    └──────────┬─────────────┘
               │ color_pie_review.md
               │ (feedback loop → set-designer if needed)
               ▼
    ┌──────────────────────┐
    │ mtg-play-designer    │  ← "Is this balanced and fun?"
    └──────────┬───────────┘
               │ play_design_report.md
               │ set.json (final numbers)
               │ (feedback loop → set-designer if needed)
               ▼
    ┌──────────────────────┐
    │ mtg-editor           │  ← "Is the templating correct?"
    └──────────┬───────────┘
               │ set.json (templated)
               ▼
    ┌──────────────────────┐
    │ mtg-creative-writer  │  ← "Name everything, write flavor"
    └──────────┬───────────┘      (uses IP terminology if UB)
               │ set.json (named, flavored)
               ▼
    ┌──────────────────────┐
    │ mtg-art-director     │  ← "Concept and describe art"
    └──────────┬───────────┘      (uses IP visuals if UB)
               │ art_descriptions.json
               ▼
    ┌──────────────────────┐
    │ mtg-card-renderer    │  ← "Render the cards" (already exists)
    └──────────┬───────────┘
               │ card_images/*.png
               ▼
             DONE
```

---

## Priority Order for Building

Given that the existing `mtg-set-designer` already tries to do everything monolithically, here's the recommended build order:

1. **`mtg-vision-designer`** — Extract the "Phase 1-3" vision work from the current skill into its own dedicated skill. This is where the creative magic happens.
2. **`mtg-worldbuilder`** — The creative half that the current skill barely touches. This is where in-universe sets get their soul.
3. **`mtg-ip-researcher`** — The UB adaptation track. Parallel to `mtg-worldbuilder`; one of them runs per set. Critical because ~half of modern Magic sets are UB, and the constraints are fundamentally different.
4. **`mtg-play-designer`** — Extract and dramatically expand the balance/testing portions. This is where quality comes from.
5. **`mtg-color-pie-reviewer`** — A standalone review pass. Relatively self-contained and high-value.
6. **`mtg-editor`** — Templating is highly rule-based and well-suited to automation. High impact on output quality.
7. **`mtg-creative-writer`** — Names and flavor text are where sets feel alive. Separating this lets it focus deeply.
8. **`mtg-exploratory-designer`** — The most open-ended skill, but valuable for generating starting material.
9. **`mtg-art-director`** — Card concepts and art descriptions; high value when paired with image generation.
10. **`mtg-set-designer`** (refactor) — Slim down the existing skill to focus purely on the Set Design phase.
11. **`mtg-product-architect`** — Lower priority; only matters for full product suite generation.
12. **`mtg-set-pipeline`** — Build last, once all component skills exist and are tested.

---

## What Changes About the Existing Skills

### `mtg-set-designer` (existing)
Currently does everything from intake through balance checking. Should be **refactored** to:
- Accept a vision handoff document as input (rather than starting from scratch)
- Focus on the Set Design phase: filling the card file, tuning curves, managing as-fan
- Delegate balance checking to `mtg-play-designer`
- Delegate naming/flavor to `mtg-creative-writer`
- Delegate templating to `mtg-editor`

### `mtg-card-renderer` (existing)
No changes needed. Already well-scoped. It's the end of the pipeline and consumes the final card file.

### `mtg-set-designer` references/
The existing skill's reference files (theme-research.md, universes-beyond-patterns.md, etc.) should be **shared** across skills or migrated to the skills that need them (e.g., theme research → exploratory designer, UB patterns → vision designer).
