# Pipeline Orchestration Framework

The operational handbook for running the MTG set design pipeline end-to-end. This document defines the data flow contracts between skills, the checkpoint specifications, the feedback loop protocol, and the artifact validation rules.

---

## 1. Orchestrator Design Principles

### Sequential with Bounded Feedback Loops
The pipeline is fundamentally sequential — each skill depends on the previous one's output. Two feedback loops (Color Pie Review → Set Design, Play Design → Set Design) can send work backward, but are bounded to 2 iterations maximum.

### Artifact-Based State
All pipeline state lives in files on disk, not in conversation context. The orchestrator tracks progress by checking which artifacts exist. This enables:
- Session-break resilience (pipeline can be resumed from last completed stage)
- User inspection (every intermediate artifact is readable)
- Clean skill invocations (each skill reads its inputs from disk, not from conversation)

### Human-in-the-Loop Checkpoints
The user reviews and approves at 7 defined checkpoints. At each checkpoint:
- Present the ACTUAL artifact (or key excerpts), not just a summary
- Ask SPECIFIC questions tied to decisions the user can make
- Offer binary approval (proceed or revise) — no partial approvals
- Preview what will happen next if approved

### Minimal Context Per Invocation
Each skill receives ONLY the artifacts it directly needs:
- The primary data artifact (set.json, exploration_doc.md, etc.)
- The world/IP reference (world_guide.md or ip_catalog.md)
- Reports from prior stages ONLY if the skill explicitly references them

---

## 2. Data Flow Contracts

| Stage | Skill | Required Inputs | Produced Outputs |
|-------|-------|----------------|------------------|
| 1 | `mtg-exploratory-designer` | User theme/concept OR IP name | `exploration_doc.md` |
| 2A | `mtg-worldbuilder` | Theme + mechanical pillars from exploration | `world_guide.md` |
| 2B | `mtg-ip-researcher` | IP name + source scope | `ip_catalog.md` + `ip_constraints.md` |
| 3 | `mtg-vision-designer` | `exploration_doc.md` + (`world_guide.md` OR `ip_catalog.md`) | `vision_handoff.md` + `vision_cardfile.json` |
| 4 | `mtg-set-designer` | `vision_handoff.md` + `vision_cardfile.json` + world/IP doc | `set.json` + `balance_report.md` |
| 5 | `mtg-color-pie-reviewer` | `set.json` | `color_pie_review.md` |
| 6 | `mtg-play-designer` | `set.json` | `play_design_report.md` + updated `set.json` |
| 7 | `mtg-editor` | `set.json` (final numbers) | `set.json` (templated) + `editing_report.md` |
| 8 | `mtg-creative-writer` | `set.json` (templated) + world/IP doc | `set.json` (named/flavored) + `naming_guide.md` |
| 9 | `mtg-art-director` | `set.json` (named/flavored) + world/IP doc | `set.json` (with art_description) + `card_concepts.json` |
| 10 | `mtg-card-renderer` | `set.json` (with art_description) | `card_images/*.png` |
| 11 | `mtg-product-architect` | `set.json` + `vision_handoff.md` | `product_brief.md` + `commander_precon_briefs.json` |

### Branch Decision (Stage 2)
- **Original world** → Run `mtg-worldbuilder` (Stage 2A)
- **Existing IP** → Run `mtg-ip-researcher` (Stage 2B)
- Only ONE runs per pipeline execution
- Both produce equivalent downstream artifacts (a creative reference document)

### Product Architect Timing
`mtg-product-architect` can run any time after Play Design (Stage 6) completes, since it needs the final-numbers `set.json`. It runs in parallel with the polish stages (Editor, Creative Writer, Art Director) or after them — it doesn't block or depend on those stages.

---

## 3. Pipeline Stages (Execution Order)

### Phase 1: Foundation

**Stage 1 — Exploratory Design**
- Invoke: `mtg-exploratory-designer`
- Input: User's theme/concept or IP name
- Output: `exploration_doc.md` (8-15 ranked mechanics, dead ends, recommendations)
- **CHECKPOINT 1**: Present exploration results. User confirms the 3-5 recommended mechanical directions

**Stage 2 — Creative Foundation (BRANCH)**

Ask the user: "Is this set based on an original Magic world or an existing IP?"

**Stage 2A — Worldbuilding** (if original world)
- Invoke: `mtg-worldbuilder`
- Input: Theme + mechanical pillars from exploration
- Output: `world_guide.md`
- **CHECKPOINT 2A**: Present world guide. User confirms factions, creature types, tone, visual identity

**Stage 2B — IP Research** (if Universes Beyond)
- Invoke: `mtg-ip-researcher`
- Input: IP name + source material scope
- Output: `ip_catalog.md` + `ip_constraints.md`
- **CHECKPOINT 2B**: Present IP catalog. User confirms character roster, color pie mappings, must-includes

### Phase 2: Design

**Stage 3 — Vision Design**
- Invoke: `mtg-vision-designer`
- Input: `exploration_doc.md` + (`world_guide.md` OR `ip_catalog.md` + `ip_constraints.md`)
- Output: `vision_handoff.md` + `vision_cardfile.json`
- **CHECKPOINT 3**: Present vision handoff — three pillars, mechanics, archetypes. User confirms this is the set they want before committing to full design

**Stage 4 — Set Design**
- Invoke: `mtg-set-designer`
- Input: `vision_handoff.md` + `vision_cardfile.json` + world/IP doc
- Output: `set.json` (~261 cards) + `balance_report.md`
- **CHECKPOINT 4**: Present set statistics (rarity distribution, archetype balance, mana curves). User confirms the set feels complete

### Phase 3: Quality Gates (with Feedback Loops)

**Stage 5 — Color Pie Review**
- Invoke: `mtg-color-pie-reviewer`
- Input: `set.json`
- Output: `color_pie_review.md`
- **Feedback loop**: If any card rated 3+ (significant bend or break):
  - Pass `color_pie_review.md` to `mtg-set-designer` for revisions
  - Re-run Color Pie Review on the updated `set.json`
  - Maximum 2 iterations. If issues persist, present to user for decision
- If clean or only 1-2 ratings: proceed

**Stage 6 — Play Design**
- Invoke: `mtg-play-designer`
- Input: `set.json` (post-color-pie)
- Output: `play_design_report.md` + updated `set.json` (final numbers)
- **Feedback loop**: If high-risk flags:
  - Route by severity (see Feedback Severity Router)
  - Minor: Play Design adjusts numbers directly (no loop)
  - Moderate: Send back to `mtg-set-designer` with flags, re-run Play Design
  - Critical: Present to user, potentially re-run from Vision Design
  - Maximum 2 iterations
- **CHECKPOINT 5**: Present play design report — power outliers, format predictions, risk flags. User acknowledges risks before proceeding to polish

### Phase 4: Polish

**Stage 7 — Editing/Templating**
- Invoke: `mtg-editor`
- Input: `set.json` (final numbers from Play Design)
- Output: `set.json` (templated, collector numbers assigned) + `editing_report.md`
- No checkpoint — this is mechanical

**Stage 8 — Creative Writing**
- Invoke: `mtg-creative-writer`
- Input: `set.json` (templated) + world/IP doc
- Output: `set.json` (named, flavored) + `naming_guide.md`
- **CHECKPOINT 6**: Present named set. User reviews names and flavor text, requests rewrites if needed

**Stage 9 — Art Direction**
- Invoke: `mtg-art-director`
- Input: `set.json` (named/flavored) + world/IP doc
- Output: `set.json` (with art_description) + `card_concepts.json`
- No checkpoint — validated by audit script

### Phase 5: Delivery

**Stage 10 — Card Rendering**
- Invoke: `mtg-card-renderer`
- Input: `set.json` (with art_description)
- Output: `card_images/*.png`

**Stage 11 — Product Architecture** (can run in parallel with Phases 4-5)
- Invoke: `mtg-product-architect`
- Input: `set.json` (final numbers) + `vision_handoff.md`
- Output: `product_brief.md` + `commander_precon_briefs.json` + `marketing_hooks.md`

**CHECKPOINT 7 (Final)**: Present complete deliverables:
- `set.json` (complete with all fields)
- `card_images/*.png` (rendered cards)
- `product_brief.md` (product suite)
- All reports from the pipeline

---

## 4. Feedback Loop Protocol

### Color Pie Review Loop

```
set.json → Color Pie Review → color_pie_review.md
                                    │
                              Any card rated 3+?
                              │           │
                              No          Yes
                              │           │
                              ▼           ▼
                          Proceed    Set Designer revises
                                         │
                                         ▼
                                    Re-run Color Pie Review
                                         │
                                    Iteration 2?
                                    │           │
                                    Pass        Still issues
                                    │           │
                                    ▼           ▼
                                Proceed    Escalate to user
```

### Play Design Loop

```
set.json → Play Design → play_design_report.md + set.json (updated)
                              │
                         Risk level?
                    ┌─────┼─────────┐
                    │     │         │
                  Low   Medium    High
                    │     │         │
                    ▼     ▼         ▼
               Proceed  Loop    Escalate
                       (Set Design)  (User decision)
```

### Convergence Rule
If iteration 2 produces MORE flags than iteration 1, the problem is systemic. Do not loop again — escalate to the user with a summary of what's wrong and recommend either:
- Accepting the remaining issues
- Re-running from an earlier stage (Vision or Set Design)

---

## 5. Checkpoint Specifications

| # | After Stage | What to Present | What to Ask | Consequence of Rejection |
|---|-------------|----------------|-------------|-------------------------|
| 1 | Exploratory Design | Top 5 mechanics with pros/cons | "Do these mechanical directions match your vision?" | Re-run exploration with adjusted parameters |
| 2 | Worldbuilder/IP Researcher | World guide or IP catalog summary | "Does this world/catalog capture the right factions, tone, and characters?" | Revise world guide or re-research IP |
| 3 | Vision Design | Three pillars, mechanics, 10 archetypes | "Is this the set you want to build?" | Revise vision (most expensive rejection — resets Phase 2) |
| 4 | Set Design | Rarity distribution, archetype stats, format speed | "Does this set feel complete and balanced?" | Send back to Set Design with notes |
| 5 | Play Design | Power outliers, combo warnings, format predictions | "Do you accept these risks?" | Re-run Play Design or revise flagged cards |
| 6 | Creative Writer | Named cards, flavor text samples | "Do the names and flavor capture the world's voice?" | Revise specific names/text |
| 7 | Final Delivery | All artifacts | "Is the set ready?" | Revise specific stages as needed |

---

## 6. Artifact Validation Rules

At each stage transition, verify:

| After Stage | Required Artifacts | Key Validation |
|-------------|-------------------|----------------|
| Exploratory | `exploration_doc.md` | Contains ranked mechanics list |
| Worldbuilder | `world_guide.md` | Contains factions, creature types, tone |
| IP Researcher | `ip_catalog.md`, `ip_constraints.md` | Contains characters, color mappings |
| Vision | `vision_handoff.md`, `vision_cardfile.json` | Handoff has 3 pillars, card file has 200+ cards |
| Set Design | `set.json`, `balance_report.md` | JSON valid, 240+ cards, all rarities present |
| Color Pie | `color_pie_review.md` | Report exists, no unresolved 4-rated cards |
| Play Design | `play_design_report.md`, `set.json` | Report exists, set.json updated with final numbers |
| Editor | `set.json`, `editing_report.md` | Collector numbers assigned, templating applied |
| Creative Writer | `set.json`, `naming_guide.md` | All cards have names, rares/mythics have flavor |
| Art Director | `set.json`, `card_concepts.json` | All cards have art_description with 5 fields |
| Card Renderer | `card_images/*.png` | Image files exist |
| Product Architect | `product_brief.md` | Brief exists with poster cards and precon themes |

---

## 7. Error Recovery

| Situation | Response |
|-----------|----------|
| Skill produces invalid JSON | Halt, report parsing error, ask user to fix or re-run |
| Skill produces valid but incomplete output (90% coverage) | Flag, proceed, note gaps for manual attention |
| Feedback loop doesn't converge (pass 2 worse than pass 1) | Halt loop, escalate to user with analysis |
| User rejects checkpoint | Identify which stage to re-run, re-execute from that point |
| Session ends mid-pipeline | On resume, run `pipeline_status.py` to assess state, continue from last completed stage |
| Downstream skill can't find required input | Halt, report missing artifact, identify which stage should have produced it |
