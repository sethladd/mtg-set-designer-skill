# Mechanic Evaluation Framework

Detailed rubrics for the seven evaluations referenced in the Exploratory Designer skill. For each candidate mechanic, run it through all seven. A mechanic doesn't need to score perfectly on every axis — but it must score well enough on *enough* axes to justify its complexity cost.

---

## Table of Contents

1. [Depth Assessment](#1-depth-assessment)
2. [Parasitism Check](#2-parasitism-check)
3. [Resonance Test](#3-resonance-test)
4. [Complexity Budget](#4-complexity-budget)
5. [Backward Compatibility](#5-backward-compatibility)
6. [Fun-to-Play Assessment](#6-fun-to-play-assessment)
7. [Historical Failure Pattern Check](#7-historical-failure-pattern-check)
8. [Quick-Reference Scoring Summary](#quick-reference-scoring-summary)

---

## 1. Depth Assessment

**What you're measuring:** Can this mechanic support 50+ distinct card designs across five colors and four rarities without repeating itself?

### Scoring Scale

| Score | Label | Description |
|-------|-------|-------------|
| 5 | Bottomless | Mechanic generates new design space at every rarity, in every color, on multiple card types. You could build an entire block around it. Examples: Landfall, Flashback, Kicker. |
| 4 | Deep | Mechanic supports a full set's worth of designs (50+) with genuine variety. Some card types or colors work better than others, but all are viable. Examples: Morph, Adventure, Cycling. |
| 3 | Adequate | Mechanic supports 30-50 designs before patterns repeat. Good enough for a secondary mechanic but probably not the set's identity. Examples: Bestow, Exalted. |
| 2 | Shallow | Mechanic runs out of meaningfully different designs by card 15-20. The first 5 are exciting; the next 10 are variations on "do the same thing, but more." Examples: Radiance, Clash. |
| 1 | Paper-thin | Mechanic has 5-8 viable designs total. It's a card, not a mechanic. Examples: Haunt (the payoff is always "do the effect again"). |

### The 20-Card Sketch Test

The fastest way to measure depth: sketch 20 different cards using the mechanic, spread across all five colors, at common, uncommon, and rare. Then ask:

- **By card 8, are you repeating?** If yes, the mechanic is shallow (score 2).
- **Do commons feel different from rares?** If the mechanic works the same at every rarity, it has no vertical depth. Good mechanics are simple at common, surprising at rare.
- **Does it work on non-creature card types?** A mechanic that only goes on creatures has less design space than one that works on instants, enchantments, and artifacts too.
- **Does each color use it differently?** Red Landfall wants aggressive triggers. Blue Landfall wants card selection. Green Landfall wants size. If every color uses the mechanic identically, the mechanic is horizontally shallow.

### Diagnostic Signs of Shallow Mechanics

- The first 5 designs are exciting but the next 15 are "same effect, bigger number"
- The mechanic only works on one card type (creatures only, instants only)
- There's no meaningful common-to-mythic gradient — mythic versions are just common versions with higher numbers
- The mechanic has one mode of interaction with the rest of the game (it always wants the same thing)

### Depth Multipliers

These characteristics increase a mechanic's effective depth:

- **Scalable parameter:** A number that can change (Kicker costs, Morph costs, X spells). Each value creates a new design.
- **Multiple card types:** Works on creatures, instants, enchantments, artifacts — not just one.
- **Color differentiation:** Each color uses the mechanic to do something characteristic of that color.
- **Rarity gradient:** Simple at common, clever at uncommon, build-around at rare, jaw-dropping at mythic.
- **Combinatorial interaction:** The mechanic interacts with other mechanics in the set in non-obvious ways. (But beware — this borders on the "interaction explosion" failure pattern from the failure catalog.)

---

## 2. Parasitism Check

**What you're measuring:** How dependent is this mechanic on other cards in the same set? A modular mechanic works alone; a parasitic mechanic needs friends.

### The Parasitism Spectrum

| Score | Label | Description | Historic Example |
|-------|-------|-------------|-----------------|
| 5 | Fully modular | Works on its own with zero support. A single card with this mechanic is playable in any deck. | Landfall, Flashback, Kicker |
| 4 | Mostly modular | Works alone but gets better with light support. One card is fine; three is noticeably better. | Cycling (works alone, better with "cycling matters" payoffs) |
| 3 | Mildly parasitic | Functional alone but clearly designed to work with other cards in the set. Drafting one card with this feels slightly awkward. | Devotion (one card is fine, but the mechanic rewards mono-color commitment) |
| 2 | Significantly parasitic | Needs 3-5 other cards with the mechanic or related cards to function. A single copy in a draft deck is weak. | Energy (one energy card is playable but inefficient without the energy ecosystem) |
| 1 | Severely parasitic | Requires dedicated support to function at all. A single copy in isolation is a dead card. | Splice onto Arcane (dead without Arcane spells), Party (needs all four types) |

### Three Conditions for Acceptable Parasitism

A mechanic scoring 2-3 on parasitism can still succeed IF it meets all three of these conditions:

**1. Large enough host population.** Splice onto Arcane failed because Arcane spells only existed in one block. If your mechanic is parasitic, the host cards must be plentiful enough that drafters can reliably assemble the package. Rule of thumb: if the mechanic needs N cards to function, there must be at least 3N cards in the format that satisfy the requirement.

**2. A pressure valve.** Energy failed because the resource accumulated without cost, interaction, or decay. If your mechanic creates a resource or state that accumulates, ask:
- What prevents hoarding? (Decay, spending incentives, maximum capacity)
- What gives opponents counterplay? (Interaction, visibility, disruption)
- What happens if a player optimizes purely for accumulation? (If the answer is "they win," the mechanic is broken.)

**3. Graceful failure.** When the parasitic mechanic partially assembles, the partial state must still be functional. Party failed this test catastrophically — 3/4 of a party was dramatically weaker than 4/4. The payoff curve should be roughly linear, not exponential.

### The Isolation Test

Imagine one card with this mechanic in a 40-card Limited deck with zero other cards that reference the mechanic. Ask:
- Is the card still playable? If yes → score 4-5.
- Is the card weak but not embarrassing? → score 3.
- Is the card actively bad? → score 1-2.
- Is the card literally nonfunctional? → score 1.

### The Rotation Test

Imagine this set has rotated out of Standard. Can a card with this mechanic still be played in Pioneer/Modern/Commander? If the mechanic only works with cards from this set, it has a lifespan problem. (This doesn't automatically kill a mechanic — some parasitic mechanics are worth printing for a great Limited environment — but it's a cost to acknowledge.)

---

## 3. Resonance Test

**What you're measuring:** Can a player guess what this mechanic does from its name and flavor before reading the rules text?

### Scoring Scale

| Score | Label | Description | Historic Example |
|-------|-------|-------------|-----------------|
| 5 | Self-teaching | The mechanic name tells you exactly what it does. A new player can guess the rules. | Flying, Trample, Deathtouch, Lifelink, First Strike |
| 4 | Strongly resonant | The name strongly implies the rules, with maybe one unexpected detail. | Flashback ("flash back" = do it again), Landfall (something falls when land appears) |
| 3 | Moderately resonant | The name evokes the right *feeling* even if you can't guess the exact rules. | Morph (things changing shape), Devotion (commitment to a cause) |
| 2 | Weakly resonant | The name is thematic but doesn't help you understand the rules. | Exalted (why does attacking alone make you stronger?), Cascade (what cascades?) |
| 1 | Opaque | The name tells you nothing about the rules. You must read and memorize. | Banding, Phasing, Flanking, Bushido, Ninjutsu |

### The Piggybacking Principle

Mark Rosewater's most important resonance concept: "The use of preexisting knowledge to front-load game information to make learning easier." The best mechanics piggyback on concepts players already understand from real life, other games, or the source IP.

**Strong piggybacking:**
- Flying → birds fly, things that fly go over obstacles
- Deathtouch → one touch = death
- Flashback → you flash back to something that already happened
- Transform → werewolves transform under the full moon

**Weak piggybacking:**
- Banding → what bands? Why does banding change damage assignment?
- Phasing → the concept of phasing in/out isn't intuitive
- Annihilator → this could mean anything destructive; it doesn't hint at "sacrifice permanents"

### Top-Down vs Bottom-Up Resonance

**Top-down sets** have a natural resonance advantage because mechanics grow from concepts players already understand. If you're designing an underwater set, "Pressure" as a mechanic resonates because everyone knows water pressure increases with depth.

**Bottom-up sets** must work harder. If you've designed a clever mechanic about resource management, naming it something evocative of its *function* (Landfall = "land falls") is better than naming it something abstract (Converge, Sunburst).

### Resonance and Teaching Cost

High resonance directly reduces teaching cost. A mechanic with score 5 resonance costs almost nothing to teach — players get it immediately. A mechanic with score 1 resonance requires explicit explanation every time a new player encounters it. In a set with 3 new mechanics, you can afford one low-resonance mechanic if the other two are high. You cannot afford three low-resonance mechanics in the same set.

---

## 4. Complexity Budget

**What you're measuring:** How much of the set's limited complexity budget does this mechanic spend? Magic can only ask players to learn so much at once.

### The Three Complexity Axes

Every mechanic generates complexity on three independent axes. Rate each axis separately:

**Comprehension complexity** — How hard is the mechanic to read and understand?
| Level | Description |
|-------|-------------|
| Low | One sentence of reminder text. A new player gets it on first read. (Lifelink, Scry) |
| Medium | Requires a paragraph of reminder text. A new player needs to read it twice. (Morph, Flashback) |
| High | Requires extended rules explanation. New players will misplay for several games. (Mutate, Banding) |

**Board complexity** — How much mental load does it add when multiple instances are on the battlefield?
| Level | Description |
|-------|-------------|
| Low | Each instance is self-contained. 4 creatures with the mechanic are no harder to track than 1. (Flying, Deathtouch) |
| Medium | Instances interact but in predictable ways. Tracking 4 instances requires attention but not calculation. (Devotion — count symbols) |
| High | Instances create combinatorial state. Each new instance multiplies the mental load. (Mutate stacks, Slivers buffing Slivers) |

**Strategic complexity** — How much depth does it add for experienced players?
| Level | Description |
|-------|-------------|
| Low | Mechanic is autopilot — always use it when you can. (Strictly better to trigger Landfall → always play your land) |
| Medium | Mechanic creates occasional interesting decisions. (Flashback: cast now from hand or save mana to flash back later?) |
| High | Mechanic creates frequent, genuinely difficult decisions. (Morph: which face-down creature do I play? What does my opponent have face-down?) |

### The Ideal Profile: Lenticular Design

The ideal mechanic is **low comprehension, low board, high strategic complexity.** This is "lenticular design" — named after lenticular printing, where the same image looks different from different angles. A lenticular mechanic looks simple to a new player and deep to an expert.

**Examples of lenticular mechanics:**
- **Intimidate:** New player reads "can't be blocked except by artifacts or creatures that share a color." Simple! Expert realizes it means their removal-light mono-green deck can't block the black creature with Intimidate, creating a strategic puzzle about deck composition.
- **Morph:** New player pays 3, plays a face-down creature, eventually flips it. Simple! Expert reads every face-down creature as a bluff or threat, creating a metagame within the game about information asymmetry.

### The Worst Profile

The worst mechanic has **high comprehension, high board, low strategic complexity** — hard to understand AND not rewarding once you do. Radiance is close to this: you have to figure out which creatures share colors (cognitive load), it clutters the board with symmetric effects, but the optimal play is usually obvious.

### Budget Constraints

A set can afford approximately:
- **3 new named mechanics at common.** Each one costs comprehension from every player in every game.
- **1-2 additional mechanics at uncommon/rare.** These can be more complex because they appear less often.
- **Unlimited evergreen keywords.** Flying, haste, lifelink — these are "free" because players already know them.

If your candidate mechanic has High comprehension complexity, it costs as much as two Low-comprehension mechanics. Budget accordingly. A set with three High-comprehension mechanics at common will overwhelm new players and produce board states even experienced players find exhausting.

### New World Order Compliance

NWO (formalized ~2011) constrains common complexity specifically:
- **≤20% of commons** should trigger the "red flag" for complexity. A red flag is anything that creates unclear board states, unusual timing, or requires tracking hidden information.
- **A common card should be understandable to a player who has played 10 games of Magic.** If your mechanic at common fails this test, it needs to move to uncommon or get simplified.

---

## 5. Backward Compatibility

**What you're measuring:** Does this mechanic play cleanly with the 25,000+ existing Magic cards?

### Scoring Scale

| Score | Label | Description | Historic Example |
|-------|-------|-------------|-----------------|
| 5 | Invisible | Uses existing game actions and types. Zero rules interactions. | Landfall (triggers on land entering — a universal, well-understood action) |
| 4 | Clean | Minor rules questions that are easy to resolve. No confusing edge cases. | Flashback (interacts with graveyard exile, cost reduction — all clean) |
| 3 | Manageable | A handful of known edge cases that require FAQ entries. Judges can resolve them. | Adventure (what happens if the Adventure half is countered? Clear answer, needs FAQ) |
| 2 | Concerning | Creates confusion with common card types (Auras, Equipment, counters). Rules team flags it. | Transform DFCs (how do copy effects work? What about tokens?) |
| 1 | Dangerous | Interacts unexpectedly with many existing subsystems. Rules team rewrites sections of the Comprehensive Rules. | Mutate (Auras, Equipment, counters, copy effects, death triggers, ETB triggers, type-checking — all confused) |

### The Ten-Card Diagnostic

Pick 10 random Magic cards from the last 5 years. Check whether your mechanic interacts cleanly with each one. Specifically check interactions with:

1. **Auras** — Does the mechanic care about what a creature "is"? Auras change what creatures do.
2. **Equipment** — Similar to Auras but persists differently.
3. **+1/+1 counters** — Does the mechanic care about power/toughness? Counters change stats.
4. **Copy effects** — If you copy a card with this mechanic, what happens? Is it intuitive?
5. **Death triggers** — If a card with this mechanic dies, do both the death trigger and the mechanic interact cleanly?
6. **ETB triggers** — Same question for enter-the-battlefield.
7. **Exile effects** — If a card with this mechanic is exiled, does anything weird happen?
8. **Flicker effects** — Exile and return immediately — does the mechanic reset? Should it?
9. **Counterspells** — If a card with this mechanic is countered, are all parts of the mechanic properly negated?
10. **Token creation** — Can tokens have this mechanic? Should they?

If you find even one confusing interaction in 10 random cards, multiply by the ~25,000 existing cards and the problem becomes enormous.

### The Rules Team Cost

Every new mechanic requires rules support. Low backward compatibility means:
- Extended FAQ/Gatherer rulings
- Comprehensive Rules updates
- Judge education materials
- Tournament ruling disputes

This isn't just a design cost — it's a deployment cost that continues as long as the cards are legal. Mutate's rules interactions will confuse players for as long as the cards exist.

---

## 6. Fun-to-Play Assessment

**What you're measuring:** Is this mechanic fun to *play*, or just fun to *think about*?

### The Rosewater Distinction

Mark Rosewater's "Twenty Years, Twenty Lessons" (GDC 2016) identifies this as the most important distinction in game design: "Players think they know what they want, and they're wrong. What they WANT is to have fun. They will tell you a hundred different ways they think they should get that fun, and most of those ideas are wrong." A mechanic that sounds exciting in a design document but produces boring or frustrating gameplay is a failure regardless of how clever it is.

### Four Fun Tests

**Test 1: The Losing Player Test**
Imagine you're losing a game. Does this mechanic give you exciting moments even when behind? Or does it only feel good when you're already winning?
- **Pass:** Flashback — when losing, flashing back a removal spell from your graveyard creates a comeback moment.
- **Fail:** Annihilator — when losing, being forced to sacrifice permanents makes you feel helpless. No interesting decisions, just misery.

Mechanics that are "win-more" (amplify winning but don't help when behind) fail this test.

**Test 2: The "Fun to Lose To" Test**
When your *opponent* uses this mechanic against you, is the experience acceptable? Can you still make interesting decisions?
- **Pass:** Morph — your opponent plays a face-down creature. You don't know what it is. This creates tension and interesting decisions about when to block, when to use removal.
- **Fail:** Energy — opponents accumulate energy with no way for you to interact. You lose to a resource you can't touch, and it feels like losing to a puzzle, not a game.

**Test 3: The Decision Frequency Test**
How often does this mechanic present the player with a meaningful choice?
- **High frequency:** Morph (every face-down creature is a decision: when to flip, what to bluff). Cycling (every draw step: keep or cycle?).
- **Low frequency:** Clash (pure randomness — no decision at all). Radiance (usually only one target makes sense).

A mechanic with low decision frequency is boring regardless of how interesting the rare decisions are.

**Test 4: The Story Generation Test**
Does this mechanic produce moments players want to tell their friends about?
- **High story potential:** Miracle (the top-deck Miracle that saved the game). Transform (the moment the werewolf flipped). Morph (the bluff that won the game).
- **Low story potential:** Haunt (the chain of triggers is too convoluted to narrate). Radiance (effects are too diffuse to create a "moment").

### Fun Killers to Watch For

- **Bookkeeping:** If the mechanic requires tracking hidden state, counters, or multi-step trigger chains, the bookkeeping erodes the fun even if the mechanic is strategically rich. (Ring Tempts You, Haunt)
- **Analysis paralysis:** If the mechanic creates so many options that players freeze, the theoretical depth becomes practical frustration. (Mutate stacking decisions)
- **Opponent helplessness:** If the mechanic gives opponents no way to respond, interact, or play around it, the opponent's experience is ruined. (Annihilator, Energy)
- **Physical gameplay disruption:** If the mechanic requires players to change how they physically handle cards, the friction overwhelms the fun. (Miracle's "peek before adding to hand")
- **Punishing correct play:** If optimizing for the mechanic conflicts with playing the game well, the mechanic creates frustration instead of satisfaction. (Clash rewarding high mana values = bad deckbuilding)

### Composite Fun Score

| Score | Label | Description |
|-------|-------|-------------|
| 5 | Beloved | Players actively seek out this mechanic. It creates stories, decisions, and memorable moments. It's fun to play AND fun to play against. | 
| 4 | Enjoyable | Players like the mechanic. It adds to games more than it detracts. Occasional frustrations are minor. |
| 3 | Neutral | The mechanic neither adds nor detracts from fun. It does its job but isn't exciting. |
| 2 | Annoying | The mechanic creates more frustration than enjoyment. One or more fun tests fail clearly. |
| 1 | Miserable | Players actively dislike the mechanic. Multiple fun tests fail. Likely to receive negative reception. |

---

## 7. Historical Failure Pattern Check

**What you're measuring:** Does this candidate share characteristics with mechanics that have historically failed?

### How to Use This Evaluation

This is not scored on a 1-5 scale. Instead, it's a **checklist**. For each of the six failure patterns (from `failure-catalog.md`), explicitly state whether your candidate matches the pattern and, if so, whether it avoids the failure mode.

### The Six Failure Patterns

**Pattern 1: No Pressure Valve**
- *Symptom:* A resource accumulates without cost, interaction, or decay.
- *Historic victims:* Energy (Kaladesh)
- *Diagnostic:* "If a player accumulates this resource for 5 turns without spending it, is that (a) a strategic choice with tradeoffs, or (b) strictly optimal?"
- *To clear this check:* Document what prevents hoarding, what gives opponents interaction, and what makes accumulation costly.

**Pattern 2: Type-Locked Parasitism**
- *Symptom:* Mechanic only works with a subtype or card category unique to this set.
- *Historic victims:* Splice onto Arcane (Kamigawa)
- *Diagnostic:* "Does this mechanic reference a card type, subtype, or resource that only exists in this set?"
- *To clear this check:* Show that the mechanic works with a broad card population, or document why the parasitism is acceptable.

**Pattern 3: Interaction Explosion**
- *Symptom:* Mechanic touches too many existing rules subsystems, creating confusing edge cases.
- *Historic victims:* Mutate (Ikoria), Banding (Alpha)
- *Diagnostic:* "Pick 10 random Magic cards. Does your mechanic interact cleanly with all of them?"
- *To clear this check:* Run the Ten-Card Diagnostic from the Backward Compatibility evaluation. Document all edge cases found.

**Pattern 4: Misaligned Optimization**
- *Symptom:* Optimizing for the mechanic makes your deck worse at everything else.
- *Historic victims:* Clash (Lorwyn)
- *Diagnostic:* "Does optimizing for this mechanic conflict with playing optimally for the game?"
- *To clear this check:* Show that a deck optimized for this mechanic is also a good deck at doing other things.

**Pattern 5: Binary Payoff**
- *Symptom:* All-or-nothing threshold with no satisfying partial credit.
- *Historic victims:* Party (Zendikar Rising), early Poison
- *Diagnostic:* "If this mechanic requires assembling N pieces, is the partial payoff (N-1 pieces) still satisfying?"
- *To clear this check:* Show that partial assembly still provides meaningful value, ideally on a roughly linear curve.

**Pattern 6: No Counterplay**
- *Symptom:* Opponents have no interesting response to the mechanic.
- *Historic victims:* Annihilator (Rise of the Eldrazi), Energy (Kaladesh)
- *Diagnostic:* "When your opponent uses this mechanic against you, do you still have interesting decisions?"
- *To clear this check:* Document at least two ways opponents can interact with or play around the mechanic using cards that already exist in Magic.

### Recording the Check

For each candidate, write a section like:

```
**Historical Risk Assessment:**
- No pressure valve: [CLEAR / AT RISK — explanation]
- Type-locked parasitism: [CLEAR / AT RISK — explanation]  
- Interaction explosion: [CLEAR / AT RISK — explanation]
- Misaligned optimization: [CLEAR / AT RISK — explanation]
- Binary payoff: [CLEAR / AT RISK — explanation]
- No counterplay: [CLEAR / AT RISK — explanation]
```

If a candidate is AT RISK for even one pattern, it needs a **specific documented mitigation plan** before advancing to the shortlist. "We'll figure it out in Set Design" is not a mitigation plan.

---

## Quick-Reference Scoring Summary

Use this table for rapid comparison of candidates:

| Evaluation | Score Range | What 5 means | What 1 means |
|------------|-----------|---------------|---------------|
| Depth | 1-5 | 50+ distinct designs across all colors and rarities | 5-8 viable designs total |
| Parasitism | 1-5 | Works perfectly alone | Dead card without support |
| Resonance | 1-5 | Self-teaching from name alone | Name tells you nothing |
| Complexity | Low/Med/High × 3 axes | Low comp, low board, high strategic | High comp, high board, low strategic |
| Backward Compat | 1-5 | Zero rules interactions | Rewrites Comprehensive Rules sections |
| Fun | 1-5 | Players actively seek it out | Players actively avoid it |
| Historical Risk | Checklist (6 items) | All CLEAR | Multiple AT RISK |

### Minimum Thresholds for Shortlist

A mechanic should meet ALL of these to make the recommended shortlist:
- Depth ≥ 3
- Parasitism ≥ 3 (or 2 with all three acceptable-parasitism conditions met)
- Resonance ≥ 2 (but ≥ 3 preferred for commons-facing mechanics)
- Complexity: NOT high-comprehension AND high-board AND low-strategic
- Backward Compatibility ≥ 3
- Fun ≥ 3
- Historical Risk: No unmitigated AT RISK patterns

A mechanic can have one score below these thresholds if it's exceptional (5) on at least two other dimensions and the weakness is documented with a mitigation plan.

---

## Sources

- Mark Rosewater, "Twenty Years, Twenty Lessons" (GDC 2016)
- Mark Rosewater, "Nuts & Bolts" series (#1-16, Making Magic)
- Mark Rosewater, "New World Order" (Making Magic, 2011)
- Mark Rosewater, "Lenticular Design" (Making Magic, 2014)
- Mark Rosewater, "Storm Scale" rating articles (Making Magic)
- Mark Rosewater, "Lessons Learned" column series (Making Magic)
- Mark Rosewater, "State of Design" annual reviews (Making Magic)
- Sam Stoddard, Play Design columns (Latest Developments)
