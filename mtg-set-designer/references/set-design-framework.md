# Set Design Framework

Canonical reference for skeleton filling, curve management, removal calibration, and card-by-card design. This fills the operational gaps in the shared references (which define targets) by explaining HOW to achieve those targets and WHAT to do when they conflict.

---

## Table of Contents

1. [The Set Design Pipeline](#the-set-design-pipeline)
2. [Skeleton-First Design Process](#skeleton-first-design-process)
3. [Removal Calibration](#removal-calibration)
4. [Curve Management](#curve-management)
5. [As-Fan Engineering](#as-fan-engineering)
6. [Build-Around Design](#build-around-design)
7. [Format Speed Tuning](#format-speed-tuning)
8. [Constructed Seeding](#constructed-seeding)
9. [Iteration Protocol](#iteration-protocol)
10. [UB-Specific Set Design Guidance](#ub-specific-set-design-guidance)

---

## The Set Design Pipeline

Set Design receives a vision handoff (pillars, mechanics, archetypes, prototype cards) and produces a complete, balanced, draftable set. The job is NOT to reinvent the vision — it's to execute it at the level of 261 individual cards that work together as a system.

### What Set Design does

1. **Fills the design skeleton** — every slot gets a real card
2. **Calibrates removal** — the right density, efficiency, and color distribution for the target format speed
3. **Manages curves** — every color and every archetype has a functional mana curve
4. **Tunes mechanics** — adjusts rarity spread, as-fan, and individual card power to make mechanics feel present without dominating
5. **Balances archetypes** — no archetype is unplayable, no archetype dominates
6. **Plants Constructed seeds** — cards that will matter in Standard/Commander without warping Limited
7. **Polishes** — names, flavor text, art descriptions, type-line consistency

### What Set Design does NOT do

- Redefine pillars (that's Vision Design's job)
- Invent new mechanics without a very good reason (if a mechanic must change, swap in a backup from the vision handoff)
- Redesign the world or IP constraints

---

## Skeleton-First Design Process

### Why skeleton-first

Without a skeleton, designers tend to:
- Clump mana curves (too many 3-drops, too few 1-drops and 6-drops)
- Forget removal (exciting mechanics crowd out boring-but-essential answers)
- Under-support archetypes (cool signposts but no common enablers)
- Break color balance (one color gets 18 commons, another gets 12)

The skeleton prevents all of this by making structural requirements visible before card text is written.

### The filling order

1. **Commons first, all five colors in parallel.** Commons define the set. Fill the skeleton slot by slot — each slot has a prescribed mana value, type, and role. Your job is to express that role through the set's theme and mechanics. Per-color targets:
   - White: ~15 commons (~11 creatures, ~4 noncreatures)
   - Blue: ~15 commons (~8 creatures, ~7 noncreatures)
   - Black: ~14 commons (~9 creatures, ~5 noncreatures)
   - Red: ~14 commons (~9 creatures, ~5 noncreatures)
   - Green: ~14 commons (~10 creatures, ~4 noncreatures)
   - Colorless/Artifact: ~9 commons

2. **Signpost uncommons.** 20 gold uncommons (2 per archetype: one enabler, one payoff). These come from the vision handoff's archetype definitions. Refine them, don't redesign them.

3. **Remaining uncommons.** ~80 mono-colored uncommons (~16-18 per color) plus ~13 colorless. These provide archetype depth, mechanic showcases, removal variety, and build-arounds.

4. **Rares.** ~60 total (~10-12 per color + gold + lands). Bombs, format-defining cards, Constructed plants.

5. **Mythics.** ~20 total (~3-4 per color + gold). "Wow" moments that do something the rare slot cannot.

6. **Cycles.** After the main file is drafted, identify opportunities for cycles — a card per color, per pair, or per archetype. Cycles are a cheap way to make a set feel cohesive.

### Slot-filling technique

For each skeleton slot:
1. Read the slot's mana value, type, and role notes
2. Check which archetypes this card's color participates in
3. Design a card that (a) fills the structural role, (b) expresses the set's theme, (c) supports at least one archetype, and (d) uses a set mechanic where appropriate
4. Verify the card against the color pie (`references/color-pie.md`)
5. For commons, check NWO complexity — if it's red-flagged, confirm you're within the 20% budget

### Card type planning

Before filling any slots, decide which non-creature permanent types the set uses:

| Type | When to use | Target count |
|------|-------------|-------------|
| Battle (Siege) | War, invasion, territorial conflict, missions | 3-5 at U/R |
| Saga | Iconic story beats, historical events, episodes | 3-8 at U/R |
| Vehicle | Iconic machines, ships, mounts, transportation | 3-6 across rarities |
| Equipment | Weapons, armor, tools, signature gear | 3-8 across rarities |
| Class | Character roles, jobs, training paths | 2-5 at U/R |
| Room | Explorable locations, dungeons, buildings | 2-6 at U/R |
| Case | Mysteries, investigations, puzzles | 2-4 at U/R |

Reserve skeleton slots for non-creature permanents early — 10-15% of permanent slots (~8-15 cards) should be non-creature types.

### Name-to-type coherence

Every creature's name must identify a BEING (person, animal, monster, construct). Names that describe actions ("Cover Fire"), events ("Flanking Maneuver"), or phenomena ("Tidal Surge") belong on instants, sorceries, or enchantments. If a skeleton slot says "creature" but your concept is an action, find a being that performs that action.

---

## Removal Calibration

### Why removal is the #1 format lever

Removal density and efficiency determine:
- **Format speed** — expensive removal means aggro goes unanswered; cheap removal means boards stall
- **Bomb impact** — too little removal and rares dominate; too much and rares feel irrelevant
- **Color viability** — if one color's removal is much worse, that color becomes undraftable

### Per-color removal targets at common

| Color | Slots | Types |
|-------|-------|-------|
| White | 2 | Combat removal (exile attacker/blocker) + conditional exile (CMC/power restriction) |
| Blue | 2-3 | Counterspell (conditional) + bounce + freeze aura (tap-down enchantment) |
| Black | 3 | Small conditional kill + unconditional kill (overcosted) + drain/weaken (-X/-X) |
| Red | 2 | Small burn (2-3 damage) + large burn (4-6 damage, sorcery speed) |
| Green | 2 | Fight + bite (deal power as damage, no fight back) |

### Removal as-fan target

Total removal as-fan per booster: **1.7-2.0** for a medium-speed format.
- Below 1.5: bomb-dominated format (Avacyn Restored territory)
- Above 2.5: board-stall grind

### The removal-threat calibration loop

1. Identify the set's most common threats (what P/T and keywords do common creatures have?)
2. Verify that common removal can efficiently answer those threats
3. If average creature toughness is 4, removal that only hits 3-toughness is insufficient
4. If the format's best aggro creatures have 2 power, removal that only hits 3+ power won't stop aggro

### Play Booster era adjustment

Because ~41% of packs contain 2+ rares, common removal must punch slightly above its weight. If commons can't answer rare-level threats, the format devolves into rare-matters. Design common removal with an eye toward "can this reasonably deal with a 4/4 or 5/5?"

---

## Curve Management

### The critical curve slots

| Mana Value | Why it matters | Target per color at common |
|-----------|----------------|---------------------------|
| 1 | Aggro openers | 1-2 creatures (White/Red need more) |
| 2 | The make-or-break value — if a color lacks 2-drops, it can't function | 2-3 creatures |
| 3 | The most glutted value; designers over-design here | 2-3 creatures (resist adding more) |
| 4 | Midrange workhorse | 2-3 creatures |
| 5 | Finishers begin | 1-2 creatures |
| 6+ | Top-end; limited slots | 0-1 creatures |

### The three-drop glut

Every set's first draft has too many 3-drops. This is because MV 3 is the "Goldilocks zone" — not too cheap, not too expensive, room for one ability. Resist the temptation. A set with 5+ three-drops per color at common and only 2 two-drops is a broken format where every game stalls on turn 3.

### Archetype curve verification

Don't just check per-color curves — check per-archetype curves. A WU deck combines White and Blue commons. If White has three 2-drops and Blue has one, WU has four total — barely enough. But if White has one 2-drop and Blue has one, WU has only two — not enough for a functional aggro or tempo deck.

For each of the 10 archetypes:
1. Combine both colors' common creatures
2. Verify at least 4 creatures at MV 2, 5 at MV 3, 4 at MV 4
3. Verify the curve matches the archetype's speed (aggro needs more 1s and 2s; control needs more 5s and 6s)

### Vanilla baselines

| MV | Baseline P/T | French vanilla (one keyword) | Notes |
|----|-------------|------------------------------|-------|
| 1 | 1/1 | 2/1 if aggressive | White/Green lean bigger |
| 2 | 2/2 | 2/1 flyer, 3/1 | 3/1 if aggro-leaning |
| 3 | 2/3 or 3/3 | 2/3 flyer | Green/White lean bigger |
| 4 | 4/3 or 3/4 | 3/3 flyer | 4/4 in Green |
| 5 | 4/5 or 5/4 | 4/4 flyer | Bigger in Green |
| 6 | 5/6 or 6/5 | — | |
| 7 | 6/7 or 7/7 | — | Green gets 7/7 vanilla |

Cards above the curve must have a real downside. Cards below the curve need utility to compensate.

---

## As-Fan Engineering

### The formula

As-fan per booster = (% of commons with trait × 10) + (% of uncommons × 3) + (% of rares × 7/8) + (% of mythics × 1/8)

This gives the expected number of cards with a given trait per booster pack.

### Target bands

| As-fan | What it means | Use case |
|--------|--------------|----------|
| < 1.0 | Most packs have 0 copies — mechanic feels absent | Too low for any named mechanic |
| 1.0-1.5 | ~50% of packs have 1 copy | Minor/secondary mechanics |
| 1.5-2.75 | Most packs have 1-3 copies — sweet spot | Primary set mechanics |
| > 3.0 | Nearly every pack has 3+ copies — may crowd out other gameplay | Too high unless it's the set's central theme |

### Per-color as-fan

Set-wide as-fan hides color distribution problems. A mechanic with set-wide as-fan of 2.0 but only 3 cards in its secondary color means drafters in that color won't see it reliably. Calculate as-fan within the mechanic's primary and secondary colors separately.

### Engineering as-fan through rarity distribution

To achieve as-fan of 2.0 for a mechanic:
- Option A: 8 commons + 6 uncommons + 4 rares + 1 mythic → as-fan ≈ 2.2
- Option B: 6 commons + 10 uncommons + 2 rares → as-fan ≈ 2.1
- Option C: 12 commons + 3 uncommons → as-fan ≈ 2.4 (heavy common presence)

Choose the distribution that matches the mechanic's complexity. Simple mechanics (like Landfall) can be common-heavy. Complex mechanics (like Mutate) should be uncommon/rare-heavy.

---

## Build-Around Design

### The build-around spectrum

| Type | Floor (no synergy) | Ceiling (full synergy) | Example |
|------|-------|---------|---------|
| **Trap** | Unplayable | Good | Bad design — only works in perfect scenarios |
| **Signpost** | Playable but below rate | Excellent | Good design — rewards synergy but not required |
| **Auto-include** | Already good | Broken | Bad design — synergy is irrelevant |

### Designing good signpost build-arounds

1. **Start with a reasonable body.** A 3-mana 2/3 with an ability is pickable on stats alone. A 3-mana 1/1 with an ability is a trap unless the ability is spectacular.

2. **Put synergy on ETB or attack triggers.** This way the card does something even if the synergy never fires again — the ETB already happened.

3. **Make the enablers generic.** If the signpost says "whenever you cast a spell with mana value 3 or less," the enablers are just... cheap spells. Every deck has those. If it says "whenever you cast a Merfolk spell," you need dedicated enablers.

4. **Don't require two build-arounds to assemble.** If the archetype only works when you draft both signpost uncommons, it's too fragile. Each signpost should function independently.

### Verifying support density

For each signpost uncommon, list the commons in both of its colors that support its strategy. The list should contain at least 10 cards. If it's under 10, either redesign the signpost to require less specific support or add more common enablers.

---

## Format Speed Tuning

### Speed levers and their settings

| Lever | Fast format | Medium format | Slow format |
|-------|------------|---------------|-------------|
| **2-drop quality** | 3+ playable 2-drops/color at C | 2 per color | 1-2 per color, defensive stats |
| **Removal cost** | Efficient (2-3 mana conditional) | Standard (3-4 mana) | Expensive (4-5 mana) |
| **Removal in aggro colors** | Best removal in R/W | Removal distributed evenly | Best removal in B/U |
| **Average toughness** | Low (most creatures have 2-3 toughness) | Medium (3-4) | High (4-5) |
| **Mana sinks** | Few or none | Some (kicker, cycling) | Many (activated abilities, X-spells) |
| **Evasion density** | High (many flyers/menace) | Medium | Low |
| **Game-ending turn** | 6-8 | 8-11 | 10-14 |

### How to verify speed matches intent

1. Check the vision handoff's target speed
2. Set the levers according to the table above
3. Run the draft simulator
4. Compare the simulator's average game-ending turn to the target
5. If too fast: increase removal efficiency, increase average toughness, add mana sinks
6. If too slow: improve 2-drop quality, reduce removal efficiency, add evasion

### The speed mismatch trap

A set whose pillars say "slow and grindy" but whose creatures are all cheap and aggressive will frustrate players. The pillars promise one experience; the cards deliver another. Speed must be a deliberate choice made through the levers, not an accident of individual card designs.

---

## Constructed Seeding

### The dual mandate

Set Design must plant cards that matter in Standard, Pioneer, Modern, and Commander without warping Limited. Techniques:

1. **Pushed rares that are bad in Limited.** A card that requires a specific Constructed deck to function (like a tribal lord for a tribe not in this set) is powerful in Constructed but mediocre in Limited.

2. **Efficient answers at uncommon.** Cheap, narrow answers (1-mana discard spells, sideboard hate cards) are Constructed staples that are too narrow for Limited maindecks.

3. **Mythic ceiling-raisers.** Mythics that require specific archetypes or combos are exciting for Constructed brewers without warping Limited (where they appear too infrequently to build around).

4. **Land cycles at rare.** Dual lands and utility lands are critical Constructed infrastructure and low-impact in Limited.

### The Constructed seed danger signs

- A pushed rare that's ALSO a Limited bomb (like Oko) — this creates a format where opening the right rare determines the draft
- A hate card that accidentally hates on a set mechanic — this can make an entire archetype unplayable
- A combo piece that's too easy to assemble in Limited — check that combo enablers aren't both at common

---

## Iteration Protocol

### The balance loop

1. Fill the skeleton completely
2. Run `balance_check.py` — address all flags
3. Run `simulate_draft.py --pods 200` — check archetype win rates, card play rates, format speed
4. Fix the most severe problems (win rate outliers, dead cards, speed mismatch)
5. Re-run the simulator once more
6. Document any remaining flags with reasoning
7. Move to Polish

### When to stop iterating

**Do not iterate more than twice on simulator results alone.** The simulator is a rough sanity check, not a precision instrument. After two passes:
- Fix obvious stat imbalances, missing removal, evasion gaps
- Document remaining flags with justification
- Proceed to Polish

The simulator cannot model set-specific mechanic synergies, conditional triggers, or complex board states. If a flag is about something the simulator can't see, document and move on.

### What the simulator catches vs. what it misses

**Catches:** Unsupported archetypes, dead cards, format speed miscalibration, bomb warping, color imbalances, missing removal, creature curve gaps.

**Cannot catch:** Subtle mechanic synergies, complex board interactions, conditional triggers, rule text interactions, play-feel quality.

---

## UB-Specific Set Design Guidance

When the input includes `ip_catalog.md + ip_constraints.md` instead of `world_guide.md`:

### Non-negotiable constraints

- **Must-include characters must have cards.** Every character on the must-include list gets a card at the appropriate rarity. These are placed FIRST, before filling remaining skeleton slots.
- **Color assignments are fixed.** If the IP catalog assigns a character to specific colors, those colors are non-negotiable.
- **Locked flavor cannot be redesigned.** Names, appearances, and signature abilities are set by the IP holder.

### Character density targets

| Rarity | Named characters | Notes |
|--------|-----------------|-------|
| Mythic | 4-8 | Protagonists, main villains |
| Rare | 10-20 | Supporting cast, fan favorites |
| Uncommon | 5-15 | Including signpost uncommons when characters fit |
| Common | 0-3 | Rarely individual characters; reference characters in names and flavor |

Total named-character cards: 20-40 (representing 20-30% of the set).

### IP naming conventions

- **Named characters:** "Name, Title/Descriptor" format — descriptor captures a specific story moment
- **Non-character cards:** Direct IP terminology ("You Cannot Pass!" not "Heroic Smite")
- **Zero generic cards:** Even common 2/2s use IP terminology in name, creature type, or both
- **Knowledge pyramid:** Base-tier (most iconic) at mythic/rare, mid-tier at rare/uncommon, deep cuts at uncommon or flavor text

### Flavor text strategy

Apply the strategy from the IP catalog consistently:
- Literary IPs with beloved prose → direct quotes heavily
- IPs with iconic catchphrases → mix direct quotes with original in IP voice
- Game/visual IPs → original flavor text using IP terminology and tone

### Power-level expectations for iconic characters

Fan-favorite characters must feel powerful. A mythic Gandalf that dies to a common removal spell will disappoint players regardless of format balance. Techniques:
- Give iconic characters protective abilities (hexproof, ward, indestructible)
- Make them expensive enough that they're not format-warping at lower rarities
- Design them to feel like "the answer to this specific character" rather than "any removal works"

---

## Card Design Checklist (Per Card)

For every card written, check:

1. **Skeleton fit:** Does it match the slot's mana value, type, and role?
2. **Color pie:** Is this ability in this color? (`references/color-pie.md`)
3. **Archetype support:** Does it help at least one archetype? Tag it in the `archetypes` field.
4. **Mechanic usage:** If it uses a set mechanic, is the mechanic name consistent with `mechanics` definitions?
5. **NWO (commons only):** Is it within the complexity budget? Red-flag if 2+ complexity markers.
6. **Type-line consistency:** Equipment has Equip, Vehicle has Crew, Aura has Enchant, Saga has chapters.
7. **Name-to-type coherence:** Creature names describe beings, not actions or events.
8. **Art description:** Five fields — scene, focus, mood, palette, frame.
9. **Vanilla baseline:** Is P/T appropriate for the mana value? Above-curve cards need downsides.
10. **Keyword tagging:** `keywords` array uses exact same casing as mechanic definitions.
