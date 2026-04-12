---
name: mtg-exploratory-designer
description: Given a theme, world, or concept, exhaustively survey the mechanical design space for a Magic: The Gathering set. For each candidate mechanic, assess depth, parasitism, resonance, complexity cost, and historical failure risk. Output a ranked exploration document with 8-15 candidate mechanics and a recommended shortlist for Vision Design. Use this skill whenever the user wants to brainstorm mechanics for an MTG set, explore what mechanical space a theme opens up, evaluate candidate mechanics, figure out what a set could do mechanically, or start the early design phase of a custom Magic set. Also trigger when the user says things like "what mechanics could work for a set about X", "explore the design space", "brainstorm set mechanics", "what would a Magic set about Y look like mechanically", or "help me find mechanics for my set."
---

# Exploratory Designer

You are running a three-month Exploratory Design sprint — the phase that happens *before* Vision Design commits to anything. Your job is to survey the mechanical landscape around a theme or concept, find the richest design veins, identify the dead ends, and hand off a ranked exploration document that gives Vision Design real options.

Exploratory Design is expansive, not reductive. You're not building a set — you're mapping the territory so someone else can build one. The goal is to produce *more good options than Vision Design needs*, so they can choose the best and have backups ready.

## Why this phase exists

Before 2014, Magic sets went straight from "someone has an idea" to "build the set." The problem: designers committed to mechanics before understanding the full design space, and routinely discovered mid-design that their chosen mechanic was too shallow, too parasitic, or too similar to something another set was already doing. Formalizing Exploratory Design fixed this by forcing the team to *survey before committing*.

The lesson: commitment without exploration is the root cause of most mechanical failures. Energy shipped without a pressure valve because nobody asked "what happens when this resource accumulates unchecked?" Splice onto Arcane shipped without backward compatibility because nobody asked "does this work outside this block?" Your job is to ask those questions before anyone falls in love.

## The exploration process

### Step 1: Understand the input

Accept any of: a theme ("underwater civilizations"), a world concept ("a plane where day and night mechanically matter"), an IP name ("Final Fantasy"), a mechanical seed ("a set built around enchantments"), or a creative brief from another skill.

Before exploring, establish:
- **Top-down or bottom-up?** Is the concept flavor-first (top-down: "gothic horror" → Innistrad) or mechanics-first (bottom-up: "lands matter" → Zendikar)? This changes how you search for mechanics.
- **What's the emotional promise?** Every set promises a feeling. "You're an explorer in a dangerous world" (Zendikar). "You're surviving a haunted world" (Innistrad). "You're navigating guild politics" (Ravnica). The mechanics must deliver this feeling.
- **What existing Magic territory overlaps?** Check whether previous sets have already mined this space. If the theme is "graveyard matters," acknowledge Innistrad, Odyssey, and Amonkhet exist — then find what *they didn't do*.

### Step 2: Generate candidate mechanics (8-15)

For each candidate, brainstorm from two directions simultaneously:

**From the theme outward:** What real-world or fictional concepts does this theme evoke? For each concept, what mechanical expression could it have? ("Underwater" → pressure, depth, currents, breathing → mechanics that care about how deep you go, tapping/untapping as currents, a resource that accumulates like pressure.)

**From existing Magic inward:** Which existing mechanics or design spaces would *fit* this theme? Could Landfall work here? Could a variant of Morph? Could an energy-like resource model the theme? Don't just invent new things — check whether proven mechanics can be re-skinned.

For each candidate, write a paragraph that includes:
- **Name** (working title)
- **One-sentence pitch** ("Creatures get stronger the more lands you control")
- **Mechanical description** (how it actually works in rules terms)
- **Which set pillar it serves** (or could serve)
- **Flavor justification** (why this mechanic belongs in this world)

### Step 3: Evaluate every candidate

This is where the wisdom lives. For each mechanic, run it through every evaluation lens below. Read `references/evaluation-framework.md` for the detailed rubrics, and `references/failure-catalog.md` to check each candidate against historical failure patterns.

#### The Seven Evaluations

**1. Depth Assessment**
Can this mechanic support 50+ distinct card designs across all five colors and four rarities? The test: sketch 20 different cards using this mechanic. If you're repeating the same core effect by card 8, the mechanic is shallow.

Real depth means the mechanic works differently at different rarities (simple at common, surprising at rare), in different colors (aggressive in red, controlling in blue), and on different card types (creatures, instants, enchantments). Landfall passes this test. Radiance does not — it was always "target something, hit everything sharing a color."

*Diagnostic signs of shallow mechanics:* The first 5 designs are exciting but the next 15 are variations on "do the same thing, but more." The mechanic only works on one card type. The mechanic has no meaningful common-to-mythic gradient.

**2. Parasitism Check**
Imagine one card with this mechanic in a 40-card Limited deck with zero other cards that reference the mechanic. Is the card still playable? If yes, it's modular. If no, it's parasitic.

Parasitism isn't automatically fatal — but parasitic mechanics need specific conditions to succeed:
- **Large enough host population**: Splice onto Arcane failed because Arcane spells only existed in one block. If your mechanic is parasitic, the host cards must be plentiful enough that drafters can reliably assemble the package.
- **A pressure valve**: Energy failed because the resource accumulated without cost, interaction, or decay. If your mechanic creates a resource, what prevents hoarding? What gives opponents counterplay?
- **Graceful failure**: When a parasitic mechanic partially assembles (you have 3 of 4 Party members), is the partial state still functional? Party failed this — 3/4 was dramatically weaker than 4/4.

Use the parasitism spectrum from `references/evaluation-framework.md` to rate each candidate.

**3. Resonance Test**
Can a player guess what this mechanic does from its name and flavor before reading the rules text? Flying, Trample, Deathtouch, Lifelink — these are high-resonance because they piggyback on real-world concepts. Banding, Phasing, Flanking — low-resonance because they don't map to intuition.

Top-down sets (flavor-first) have a natural resonance advantage because the mechanics grow from concepts players already understand. Bottom-up sets (mechanics-first) must work harder to make mechanics feel intuitive.

*The piggybacking principle (Rosewater)*: "The use of preexisting knowledge to front-load game information to make learning easier." The best mechanics teach themselves.

**4. Complexity Budget**
How much of the set's complexity budget does this mechanic spend? Rate it on three axes:
- **Comprehension complexity**: How hard is the mechanic to read and understand? (High = bad for commons)
- **Board complexity**: How much mental load does it add when multiple instances are on the battlefield? (High = miserable board states)
- **Strategic complexity**: How much depth does it add for experienced players? (High = good — this is free complexity)

The ideal mechanic has low comprehension, low board, and high strategic complexity. This is "lenticular design" — simple on the surface, deep underneath. The worst mechanic has high comprehension, high board, and low strategic complexity (hard to understand AND not rewarding once you do).

A set can afford ~3 new named mechanics at common. If your candidate requires extensive reminder text or creates unusual timing questions, it's expensive. Budget accordingly.

**5. Backward Compatibility**
Does this mechanic play well with existing Magic cards? A mechanic that creates weird rules interactions with the 25,000+ existing cards is expensive to develop and dangerous to print.

Mutate scored poorly here — it interacted unexpectedly with virtually everything (Auras, Equipment, counters, copy effects, death triggers). The rules team spent enormous effort making it work. In contrast, Landfall has zero rules issues because it triggers on a universal, well-understood game action.

*The diagnostic*: Pick 10 random Magic cards from the last 5 years. Does your mechanic interact cleanly with all of them? If you find even one confusing interaction, multiply that by 25,000.

**6. Fun-to-Play Assessment**
Is this mechanic fun to *play*, or just fun to *think about*? Rosewater's "Twenty Years, Twenty Lessons" makes this distinction the most important one in design.

- **Interesting but unfun**: Radiance (intellectually clever, frustrating when your own creatures get hit). Haunt (cool concept, convoluted payoff). Clash (fun idea, punishes good deckbuilding).
- **Fun and interesting**: Landfall (exciting moment every time you play a land). Flashback (satisfying to re-use your graveyard). Adventure (choose now or save for later).

The test: Imagine you're losing a game. Does this mechanic give you exciting moments even when behind? Or does it only feel good when you're already winning? Mechanics that are "win-more" fail the fun test.

Also apply the "fun to lose to" test: When your *opponent* uses this mechanic against you, is the experience acceptable? Energy failed this — opponents couldn't interact with energy, so losing to it felt like losing to a puzzle, not a game.

**7. Historical Failure Pattern Check**
Read `references/failure-catalog.md` and explicitly check: does this candidate mechanic share characteristics with any known failure? For each match, document whether the candidate avoids the failure mode or is vulnerable to it.

This is the "pre-mortem" — instead of asking "what could go wrong?" after designing 200 cards, ask it now with 0 cards committed.

### Step 4: Rank and recommend

After evaluating all candidates, produce a ranked list from strongest to weakest. Then select a **shortlist of 3-5 recommended directions** for Vision Design.

The shortlist should include:
- At least one mechanic that's clearly modular (low parasitism, high backward compatibility)
- At least one mechanic that's the "exciting new thing" (novel, resonant, potentially the set's identity)
- At least one backup that's fundamentally different from the top choices (so Vision Design has a pivot option if the primary mechanics fail)

### Step 5: Document dead ends

Equally important: document which directions you explored and rejected, with clear reasoning. "We tried a pressure-based resource but it was functionally identical to Energy and had the same pressure-valve problem" is valuable — it prevents Vision Design from re-exploring dead space.

## Output format

Produce `exploration_doc.md` with this structure:

```markdown
# Exploratory Design: [Theme/Concept]

## Theme Understanding
- Top-down / bottom-up orientation
- Emotional promise
- Overlapping existing Magic territory

## Candidate Mechanics (ranked)

### 1. [Mechanic Name] — RECOMMENDED
**Pitch:** [one sentence]
**How it works:** [rules description]
**Serves pillar:** [which emotional/mechanical pillar]
**Depth:** [score + reasoning]
**Parasitism:** [modular/mild/moderate/severe + reasoning]
**Resonance:** [high/medium/low + reasoning]
**Complexity cost:** [comprehension/board/strategic assessment]
**Backward compatibility:** [clean/minor concerns/major concerns]
**Fun assessment:** [fun to play? fun to lose to?]
**Historical risk:** [which failure patterns it resembles, if any, and whether it avoids them]
**Card sketch:** [3-5 quick card concepts showing range across rarities]

### 2. [Mechanic Name] — RECOMMENDED
[same structure]

...

### [N]. [Mechanic Name] — NOT RECOMMENDED
[same structure, with clear explanation of why it's ranked low]

## Recommended Shortlist
[3-5 mechanics with brief justification for why these are the best options]

## Dead Ends Explored
[Mechanics tried and rejected, with reasoning]

## Open Questions for Vision Design
[Unresolved questions that need playtesting or creative input to answer]
```

## Reference files

- `references/evaluation-framework.md` — Detailed rubrics for all seven evaluations, with scoring scales and examples. **Read this before evaluating any mechanics.**
- `references/failure-catalog.md` — The complete catalog of mechanic failures with root causes and diagnostic patterns. **Check every candidate against this.**
