# Vision Design Framework

Canonical reference for pillar generation, handoff structure, and card file creation. This fills the operational gaps in the existing `references/vision.md` (which defines WHAT vision design produces) by explaining HOW to produce it. Read this alongside the shared references before starting any vision design.

---

## Table of Contents

1. [Pillar Generation Methodology](#pillar-generation-methodology)
2. [Pillar Testing Rubric](#pillar-testing-rubric)
3. [Tone and Play Feel Vocabulary](#tone-and-play-feel-vocabulary)
4. [Top-Down vs. Bottom-Up Decision Framework](#top-down-vs-bottom-up-decision-framework)
5. [How Pillars Constrain Mechanics and Archetypes](#how-pillars-constrain-mechanics-and-archetypes)
6. [Handoff Document Template](#handoff-document-template)
7. [UB-Specific Vision Design Guidance](#ub-specific-vision-design-guidance)
8. [Card File Generation Process](#card-file-generation-process)

---

## Pillar Generation Methodology

### What a pillar is (and isn't)

A pillar is a mechanical/experiential commitment the set makes. It describes what the set DOES, not what it IS ABOUT.

| Good pillar | Bad pillar | Why |
|------------|-----------|-----|
| "Creatures permanently transform into larger versions" | "Transformation" | The good one tells you the play pattern; the bad one is just a subject |
| "The graveyard is a second hand — cards are as useful dead as alive" | "Graveyard matters" | The good one implies specific mechanics; the bad one could mean anything |
| "Small creatures matter — the board should feel like a swarm" | "Tokens" | The good one describes the experience; the bad one names a card type |

### The three pillar generators

Generate pillar candidates from three sources, then select the best three:

1. **From emotional promise:** What should the player FEEL? "Dread builds each turn" → pillar about escalating threat. "Discovery around every corner" → pillar about revealing hidden information.

2. **From mechanical identity:** What gameplay hook defines this set? "Lands are the protagonist" → landfall pillar. "Enchantments vs. artifacts" → card-type tension pillar.

3. **From creative identity:** What world/IP element demands mechanical expression? "Five factions with distinct philosophies" → faction-mechanic pillar. "Corruption spreading" → progressive mechanic pillar.

### Worked examples

**Innistrad (top-down gothic horror):**
1. "Horror — the set should feel scary; every creature might be hiding something dark" → Transform mechanic
2. "Death feeds power — the graveyard is a resource, not a dump" → Flashback, Morbid
3. "Tribes of darkness hunt tribes of light" → Human/Spirit/Zombie/Vampire/Werewolf tribal with Human-vs-monsters dynamic

**Zendikar (bottom-up lands matter):**
1. "The land itself is the protagonist — every land drop is a significant event" → Landfall
2. "Exploration is dangerous — you're rewarded for going deeper but at risk" → Traps, Quests, adventure tropes
3. "Allies band together to survive" → Ally tribal / party formation

**Bloomburrow (top-down animal civilization):**
1. "Focus on the fun of animals — the most creature-type-centric set ever"
2. "Solve past typal gameplay problems — avoid drafts-on-rails"
3. "Achieve the most charming Magic set — pastoral, lighthearted flavor"

**Kamigawa: Neon Dynasty (hybrid top-down/bottom-up):**
1. "Tradition vs. modernity — an authentic cultural tension expressed through enchantments vs. artifacts"
2. "Both sides of the conflict are playable and compelling — no side is 'the bad guys'"
3. "Bridge mechanics unify the set — Modified rewards creatures with equipment, enchantments, OR counters"

---

## Pillar Testing Rubric

### The Reinforcement Test

**Ask:** "If I describe all three pillars to a stranger, does it sound like ONE set or THREE sets?"

- **Pass:** Innistrad's three pillars (horror/graveyard/tribal) all reinforce "surviving a haunted world."
- **Fail:** BFZ's pillars (adventure/Eldrazi/allies) describe three different games.

### The Constraint Test

**Ask:** "If I removed one pillar, would the set noticeably change?"

- **Pass:** Removing "graveyard as resource" from Innistrad fundamentally changes the set — no more Flashback, no self-mill enablers.
- **Fail:** If removing a pillar doesn't change any card designs, it wasn't load-bearing.

### The Competition Diagnostic

**Ask:** "Are any two pillars pulling design resources away from each other?"

Signs of competition:
- Two pillars need the same card slots but for different purposes
- A mechanic that serves one pillar actively undermines another
- Playtesters describe the set as "two games in one pack"

### The Specificity Test

**Ask:** "Could a designer who reads only this pillar make correct card design decisions?"

- **Pass:** "The board gets scarier each turn as creatures transform into larger predators" → designer knows to make transformation effects that increase P/T
- **Fail:** "Creatures transform" → designer doesn't know if transformation makes creatures bigger, smaller, different types, or something else entirely

---

## Tone and Play Feel Vocabulary

### Speed definitions

| Speed | Game length | Characteristics | Example sets |
|-------|-----------|----------------|-------------|
| **Fast** | Games end turn 6-7 | Cheap creatures, burn/combat tricks, low-toughness format, aggro dominates | Zendikar, Amonkhet |
| **Medium** | Games end turn 8-10 | Balanced curves, removal answers threats, midrange viable | Innistrad, Eldraine, Bloomburrow |
| **Slow** | Games end turn 10+ | High-toughness creatures, board stalls, card advantage matters | Rise of the Eldrazi, Dominaria |

### Emotional register vocabulary

| Register | What it means | Card design implications |
|----------|-------------|------------------------|
| **Dread** | Something bad is coming; tension builds | Escalating threats, "sacrifice" effects, growing creatures |
| **Wonder** | Discovery and surprise | Reveal effects, modal spells, adventure mechanics |
| **Heroism** | Overcoming the odds, growing stronger | +1/+1 counters, equipment, "underdog" mechanics |
| **Chaos** | Unpredictability, wild swings | Random effects, modal with downside, variance |
| **Inevitability** | Slow, grinding victory | Resource accumulation, recursion, control tools |
| **Whimsy** | Lighthearted, charming, fun | Token creation, size-changing, playful flavor |

### The selling sentence template

> "[Set name] is a [speed] [emotional register] set where [what you do] by [how the mechanics make you feel]."

Examples:
- "Innistrad is a medium-speed dread set where you survive gothic horror by weaponizing the graveyard."
- "Zendikar is a fast wonder set where you explore a dangerous world by triggering Landfall on every land drop."
- "Bloomburrow is a medium-speed whimsy set where you build animal civilizations by assembling creature-type synergies."

---

## Top-Down vs. Bottom-Up Decision Framework

### Decision criteria

| Factor | Use top-down | Use bottom-up |
|--------|-------------|---------------|
| **Resonance** | Genre is universally familiar (gothic horror, Greek myths) | Genre would need extensive explanation |
| **What's exciting** | The world/concept is the hook | A mechanical innovation is the hook |
| **Player response** | "I can't wait to see how they do X" | "I can't wait to see what X does" |
| **Design starting point** | Tropes → mechanics that express them | Mechanical hook → world that justifies it |

### Mismatch warning signs

- **Top-down set with forced mechanics:** If the source material doesn't naturally suggest mechanics, top-down is wrong. Original Kamigawa forced Shinto mythology onto card mechanics, producing parasitic designs.
- **Bottom-up set with no flavor hook:** If the mechanical innovation doesn't suggest a compelling world, the set won't sell. "Lands matter" needs "adventure world" to give it emotional resonance.
- **The hybrid option:** Many successful sets blend both. NEO found a mechanical hook (artifacts vs. enchantments) within a top-down framework (Japanese culture). When possible, find both.

### The resonance test

Describe the set's genre in one sentence. If most players immediately picture specific tropes, creatures, and expectations → top-down works. If the exciting part is mechanical novelty that doesn't map to existing genre → go bottom-up.

---

## How Pillars Constrain Mechanics and Archetypes

### The serves_pillar requirement

Every mechanic in the handoff must name a pillar it serves. This is not optional. If a mechanic doesn't serve any pillar, either:
- The mechanic doesn't belong in this set (cut it)
- A pillar is missing (add one)
- The mechanic serves a pillar you haven't articulated (articulate it)

### The pillar orphan test

**Check:** Is any mechanic an "orphan" — not connected to any pillar?
Orphan mechanics were probably included because they're cool, not because they serve the set. Cool orphans make good candidates for other sets.

### The pillar monopoly test

**Check:** Does any pillar have only one mechanic serving it?
If a pillar is served by only one mechanic and that mechanic gets cut, the pillar collapses. Each pillar should have at least two mechanical expressions.

### Archetype-pillar mapping

Each of the 10 archetypes should intersect with at least one pillar:

| Archetype | Pillar 1 | Pillar 2 | Pillar 3 |
|-----------|----------|----------|----------|
| WU | [how it touches P1] | - | [how it touches P3] |
| WB | - | [how it touches P2] | [how it touches P3] |
| ... | | | |

If an archetype doesn't touch any pillar, it's a generic archetype that could be in any set. That's a warning sign.

---

## Handoff Document Template

The `vision_handoff.md` should follow this structure:

```markdown
# Vision Design Handoff: [Set Name]

## Set Identity
**Elevator pitch:** [one sentence]
**Selling sentence:** [speed + register + what you do + how]
**Orientation:** [top-down / bottom-up / hybrid]
**Emotional promise:** [what the player should feel]

## Three Pillars
### Pillar 1: [Name]
[2-3 sentences: what this pillar means mechanically and experientially]

### Pillar 2: [Name]
[2-3 sentences]

### Pillar 3: [Name]
[2-3 sentences]

## Mechanics
### [Mechanic Name] (primary)
**Type:** [keyword / ability word / named mechanic]
**Reminder text:** [rules text]
**Serves pillar:** [which pillar]
**Colors:** primary [X], secondary [Y]
**Rarity spread:** [C/U/R/M counts]

### [Mechanic Name] (primary)
[same structure]

### Backup Mechanics
**[Backup Name]:** [brief description, which pillar it serves, why it was explored but not selected]

## Ten Two-Color Archetypes
### WU — [Archetype Name]
**Strategy:** [one sentence]
**Speed:** [fast / medium / slow]
**Key mechanics:** [which set mechanics this uses]
**Signpost uncommon (enabler):** [card sketch]
**Signpost uncommon (payoff):** [card sketch]
**Commons needed:** [what common slots must provide]

[Repeat for all 10 pairs]

## Tone and Play Feel
[3-5 sentences: speed, emotional register, violence/humor, hope-to-threat ratio]

## Card File Overview
**Total cards:** [count by rarity]
**Color balance:** [per-color distribution]
**Mechanic as-fan:** [how often each mechanic appears per pack]

## Open Questions for Set Design
[Unresolved questions, known problems, areas needing playtesting]

## Assumptions
[Decisions made where user input was ambiguous]

## What We Tried and Cut
[Mechanics explored and rejected, with reasoning]
```

---

## UB-Specific Vision Design Guidance

When the input includes `ip_catalog.md + ip_constraints.md` instead of `world_guide.md`:

### Non-negotiable constraints
- **Must-include list is fixed.** Those characters/items/moments MUST have cards. Design around them, not in spite of them.
- **Color gaps must be compensated, not "fixed."** If the IP skews toward black and away from green, you can't make the IP's villains green. Instead, find IP elements that plausibly fit green and lean on them.
- **Locked flavor cannot be redesigned.** Character names, appearances, and signature abilities are set by the IP holder.

### Character density adjustment
Original sets target 15-25 named legendary creatures. UB sets target 20-30% of the set as named characters (40-80 legendaries). The handoff must account for this higher character density by:
- Defining how many card versions each tier-1 character gets (2-3 max)
- Planning which characters appear at each rarity
- Ensuring character cards serve archetype needs (a legendary creature should fit into a draft archetype, not just be a flavor showcase)

### System translation priority
Select 2-3 IP systems from the system translation inventory in `ip_catalog.md` as primary mechanic candidates. These should be the IP's most iconic interactive systems. Reserve existing Magic mechanics as backups for less iconic systems.

### Flavor text strategy
Carry forward the flavor text strategy recommendation from `ip_catalog.md` (direct quotes / mixed / original in IP voice) and ensure it's documented in the handoff.

---

## Card File Generation Process

### What the vision card file is

The `vision_cardfile.json` is a **prototype draft environment** — not a finished set. It proves the vision works by providing a draftable card file. Set Design will revise, rebalance, and complete it.

### Minimum viable draft file

| Rarity | Target count | Priority |
|--------|-------------|----------|
| Common | 81 | Highest — commons define the set |
| Uncommon | 100 | High — signpost uncommons define archetypes |
| Rare | 40 | Medium — enough for draft variance |
| Mythic | 10-15 | Lower — flagship cards and bombs |

### Generation priority order

1. **Commons first** — they define what the set IS at the most-seen rarity. Start with the design skeleton (`references/design-skeleton.md`) and fill each slot.
2. **Signpost uncommons** — 10 gold uncommons, one per color pair, announcing each archetype (enabler + payoff pair)
3. **Remaining uncommons** — archetype depth, mechanic showcases, build-arounds
4. **Draft-critical rares/mythics** — bombs, format-defining cards, pillar showcases

### Per-color distribution targets (from `references/design-skeleton.md`)

| Color | Commons (creatures/non) | Uncommons |
|-------|------------------------|-----------|
| White | ~11 creatures / ~4 non | ~16-18 |
| Blue | ~8 creatures / ~7 non | ~16-18 |
| Black | ~9 creatures / ~5 non | ~16-18 |
| Red | ~9 creatures / ~5 non | ~16-18 |
| Green | ~10 creatures / ~4 non | ~16-18 |
| Colorless/Multi | ~9 | varies |

### Card schema

Each card follows the format in `references/set_template.json`:
```json
{
  "id": "SET-001",
  "name": "Card Name",
  "mana_cost": "{1}{W}",
  "cmc": 2,
  "color": ["W"],
  "type": "Creature",
  "subtypes": ["Human", "Soldier"],
  "power": 2,
  "toughness": 2,
  "rules_text": "...",
  "flavor_text": "...",
  "rarity": "common",
  "archetypes": ["WU", "WR"],
  "keywords": [],
  "notes": "..."
}
```

### NWO check during generation

While writing commons, track red-flag complexity. No more than ~16 commons (20% of 81) should have:
- Multiple abilities
- Reference to zones other than the battlefield
- State-tracking requirements
- Triggered abilities during opponent's turn
- More than 3 lines of rules text
- New named keywords without reminder text

See `references/new-world-order.md` for the complete framework.
