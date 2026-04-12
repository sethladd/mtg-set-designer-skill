# Play Design Framework

Operational reference for power-level evaluation, format health analysis, combo checking, Commander scaling, and play-pattern assessment. This framework provides the concrete methods and numerical baselines that the Play Design skill uses to evaluate a card file.

---

## Table of Contents

1. [Rate Baselines](#rate-baselines)
2. [Combo Detection Methodology](#combo-detection-methodology)
3. [Commander Scaling Analysis](#commander-scaling-analysis)
4. [Format Health Metrics](#format-health-metrics)
5. [Play-Pattern Evaluation Framework](#play-pattern-evaluation-framework)
6. [The Constructed Push Framework](#the-constructed-push-framework)
7. [Number Finalization Guidelines](#number-finalization-guidelines)

---

## Rate Baselines

"Rate" is what a card should deliver for its mana cost. Cards above rate are pushed; cards far above rate are ban risks. These baselines represent the "fair" expectation at each mana value.

### Creature Baselines

| CMC | Baseline P/T (vanilla) | With 1 keyword | With 2 keywords | Notes |
|-----|----------------------|-----------------|------------------|-------|
| 1 | 2/1 or 1/2 | 1/1 + keyword | — | 2/1 is aggressive-rate |
| 2 (1C) | 2/3 | 2/2 + keyword | 1/1 + 2 keywords | Modern 2-drops often exceed this |
| 2 (CC) | 3/3 | 2/3 + keyword | — | Double-color tax earns +1/+1 |
| 3 (2C) | 3/4 | 3/3 + keyword | 2/3 + 2 keywords | The "three-drop zone" — most glutted value |
| 3 (1CC) | 4/4 | 3/4 + keyword | — | Only green reliably gets this at common |
| 4 (3C) | 4/5 | 4/4 + keyword | 3/4 + 2 keywords | The midrange workhorse |
| 4 (2CC) | 5/5 | 4/5 + keyword | — | |
| 5 (4C) | 6/5 or 5/6 | 5/5 + keyword | — | Finisher territory |
| 6+ | 6/6+ | Variable | Variable | Should have significant impact |

**Modern Constructed shift:** Since ~2020, Constructed creatures need abilities beyond vanilla stats. A 3-mana 4/3 is "already considered inconsequential" in Constructed. Limited baselines remain closer to the table above.

**Keyword value:** Each keyword costs approximately 1 total stat point. Flying is the most expensive (~1.5 stats). Deathtouch, lifelink, and first strike cost ~1 stat. Trample and menace cost ~0.5 stats.

### Removal Baselines

| Type | Fair rate | Above rate (flag) | Broken rate (ban risk) |
|------|-----------|-------------------|------------------------|
| Unconditional spot removal (instant) | 3 mana | 2 mana | 1 mana + upside |
| Unconditional spot removal (sorcery) | 2 mana | 1 mana | — |
| Conditional removal (damage, instant) | 2 mana for 3 damage | 1 mana for 3 damage (Lightning Bolt) | 1 mana for 4+ damage |
| Board wipe (all creatures) | 4-5 mana | 3 mana | 2 mana |
| Board wipe (conditional) | 3-4 mana | 2-3 mana | — |
| Exile removal (instant) | 3-4 mana | 2 mana | 1 mana unconditional |
| Counter (hard) | 3 mana (Cancel) | 2 mana (Counterspell) | 1 mana hard counter |
| Counter (conditional) | 2 mana | 1 mana | 0 mana (Force of Will = eternal-only) |

**Key insight:** Removal that cantrips (removes + draws a card) is approximately 1.5 mana above the base removal rate. A 3-mana removal that also draws is really "4.5 mana of value for 3 mana."

### Card Draw Baselines

| Effect | Fair rate | Notes |
|--------|-----------|-------|
| Draw 1 (cantrip) | +1 mana to base effect | Opt costs U; Brainstorm is above rate |
| Draw 2 (sorcery) | 3 mana (Divination) | The eternal benchmark |
| Draw 2 (instant) | 4 mana (Inspiration) | Instant-speed premium is ~1 mana |
| Draw 3 | 5 mana | Below this is pushed |
| Repeatable draw (per turn) | Significant cost or condition | "Draw a card whenever..." needs real restrictions |

### Planeswalker Baselines

| CMC | Starting loyalty | Plus ability value | Minus ability value | Notes |
|-----|-----------------|--------------------|--------------------|-------|
| 3 | 3-4 | Minor advantage | Medium effect | DANGER ZONE — make sparingly |
| 4 | 3-5 | Moderate advantage | Significant effect | The bread-and-butter design space |
| 5 | 4-5 | Card advantage | Removal or token | High-cost = high loyalty + strong abilities |
| 6+ | 5-6 | Strong advantage | Game-changing | Should immediately impact the board |

**Critical rule:** Plus abilities should NOT remove threats (Oko's +1 violated this). Plus abilities generate incremental advantage; minus abilities are the powerful effects that cost loyalty.

### Mana Ramp Baselines

| Effect | Fair rate | Ban risk |
|--------|-----------|----------|
| Put a land from hand onto battlefield | 2 mana (sorcery) | 2 mana + cantrip (Growth Spiral) |
| Search library for a basic land | 2-3 mana | 1 mana + upside (Attune with Aether) |
| Add temporary mana (ritual) | Highly restricted in Standard | Any repeatable ritual |
| Mana doubling | 4+ mana enchantment | Wilderness Reclamation (untap all lands = free) |

**Key insight:** 2-mana ramp spells are historically the most dangerous card type in Standard. Growth Spiral was banned. Explore was format-defining. Rampant Growth was deliberately removed from Standard for years.

---

## Combo Detection Methodology

### The Priority Matrix

Testing every two-card combination in a format is combinatorially explosive. Play Design prioritizes by risk category:

**Tier 1 (Always check):**
- Any "cast without paying mana cost" effect × all high-CMC cards
- Any ETB blink/copy effect × all planeswalker minus abilities that create tokens
- Any Cascade/Discover effect × all clone/copy creatures at the discovered CMC
- Any "goes infinite with untap" creature × all tap-for-value effects

**Tier 2 (Check if the mechanic exists in the set):**
- Zero-cost activated abilities × all "whenever targeted" triggers
- Death triggers × sacrifice outlets × recursion (three-card but common)
- Token doublers × token generators
- Extra turn effects × recursion/copy effects

**Tier 3 (Spot-check):**
- Cost-reduction effects × expensive payoffs in adjacent sets
- "Whenever you gain life" × repeatable lifegain triggers
- "Whenever a creature enters" × mass token creation

### The Four Criteria for Healthy Combos

From Melissa DeTora's Play Design philosophy:

1. **Speed:** Combo should not be faster than the format's fastest aggro decks. If combo kills on turn 3 and aggro kills on turn 5, the format becomes non-interactive coin flips.

2. **Interactivity:** Healthy combos require permanents on the battlefield that opponents can remove. Problematic combos win from an empty board using only cards from hand.

3. **Consistency:** Tutors and card filtering amplify combo reliability. If a combo has 8+ functional copies of each piece, it's too consistent regardless of power.

4. **Deckbuilding cost:** Combo pieces should force inclusion of cards that "don't do a whole lot on their own." If every combo piece is independently strong, there's no trade-off for playing the combo.

### Red Flags for Combo Potential

- Card says "until end of turn" and can be copied/repeated → check for infinite loops
- Card references another card's CMC → check for mana cost exploitation
- Card creates copies of other cards → check against all ETB/death triggers
- Card untaps permanents → check against all tap-for-value effects
- Card returns things from graveyard → check against all sacrifice outlets

---

## Commander Scaling Analysis

### Why Commander Breaks Cards

In a 4-player Commander game:
- "Each opponent" effects are 3× stronger (drain 3 opponents instead of 1)
- 40 starting life makes life-as-resource costs nearly irrelevant
- 3 opponents means 3× the board state to exploit ("whenever an opponent...")
- Games last longer, making inevitability engines more dominant
- Social dynamics mean targeted answers are politically costly

### The Scaling Danger Categories

| Effect type | 1v1 impact | 4-player impact | Danger level |
|-------------|------------|-----------------|-------------|
| "Each opponent loses N life" | N damage | 3N damage + 3N life gain | HIGH |
| "Create treasure for each artifact/enchant opponents control" | 2-4 treasures | 6-15 treasures | CRITICAL |
| "Whenever an opponent casts a spell" | Triggers once per turn | Triggers 3-9 times per turn cycle | HIGH |
| "Draw a card" (per opponent's action) | 1 card per trigger | 3 cards per turn cycle | HIGH |
| Life loss as drawback | Meaningful at 20 life | Irrelevant at 40 life | MODERATE |
| "Target opponent" | Fixed | Political — choose weakest | LOW |
| Mana acceleration | Faster but symmetrical | Same speed, but multiplayer means fewer interactive spells aimed at you | MODERATE |

### Commander-Specific Rate Adjustments

When evaluating cards for Commander impact, apply these multipliers:

- **"Each opponent" damage/drain:** Multiply by 3 for true rate
- **"Whenever an opponent" triggers:** Evaluate at 3× trigger frequency
- **Life-based drawbacks:** Divide by 2 (40 life instead of 20)
- **Artifact/creature-based scaling:** Assume 3× the board state
- **Fast mana:** Evaluate as if the format has effectively zero early interaction (political protection + 40 life buffer)

### Recently Banned (Commander, September 2024)

| Card | Root cause | Scaling type |
|------|-----------|-------------|
| Mana Crypt | Life drawback irrelevant at 40 life | Fast mana + life scaling |
| Jeweled Lotus | Turn-2 commander with ward/protection | Fast mana |
| Dockside Extortionist | 6-15 treasures from 3 opponents | Board-state scaling |
| Nadu, Winged Wisdom | Zero-mana equipment loops | Combo |

---

## Format Health Metrics

### Limited Format Health

| Metric | Healthy range | Concerning | Broken |
|--------|--------------|------------|--------|
| Archetype win-rate spread | 46-54% | 42-58% | Outside 42-58% |
| Best archetype win rate | ≤54% | 55-57% | >58% |
| Worst archetype win rate | ≥46% | 43-45% | <42% |
| Best color win rate | ≤53% | 54-56% | >56% |
| Worst color win rate | ≥47% | 44-46% | <44% |
| Format speed (avg game end) | Turn 8-11 | Turn 6-7 or 12-14 | Turn <6 or >14 |
| Common play rate (per eligible deck) | 15-70% | 5-15% or 70-85% | <5% or >85% |
| Rare win-rate delta (rare opener vs not) | <5% | 5-8% | >8% (bomb-dominated) |

### Constructed Format Health

| Metric | Healthy | Concerning | Emergency |
|--------|---------|------------|-----------|
| Best deck metagame share | <20% | 20-35% | >35% |
| Best deck non-mirror win rate | <55% | 55-57% | >58% |
| Top-3 decks combined share | <50% | 50-65% | >65% |
| Viable tier-1 archetypes | 5+ | 3-4 | 1-2 |
| Format archetype diversity (aggro/midrange/control/combo) | All 4 present | 3 of 4 present | 2 or fewer |
| Single card in >20% of games | 0 cards | 1-2 cards | 3+ cards |

### The MTG Health Index Factors

Professional format health scoring weights seven factors:
1. **Metagame archetype distribution** (15%) — ideal is ~33% each of aggro/control/combo
2. **Metagame diversity index** (20%) — Shannon Index of deck diversity
3. **Monthly event count growth** (15%) — player participation trends
4. **Player growth** (15%) — new player acquisition
5. **Winner deck dominance** (15%) — diversity of tournament winners
6. **B&R health score** (10%) — community sentiment around bans
7. **Card price health** (10%) — demand + affordability balance

---

## Play-Pattern Evaluation Framework

### The Six Axes of Play Experience

Evaluate each card on these axes independently from power level:

1. **Interaction windows:** Does the opponent have meaningful response options?
   - Good: "When this creature attacks, if defending player controls no untapped creatures..."
   - Bad: "Players can't cast spells during your turn" (Teferi, Time Raveler)

2. **Game advancement:** Does the card move the game toward a conclusion?
   - Good: Creature that attacks and eventually wins
   - Bad: Extra-turn loop that extends the game without closing it (Nexus of Fate)

3. **Agency preservation:** Does the opponent still feel like their decisions matter?
   - Good: Powerful threat they can build a plan to answer
   - Bad: Elk ability that makes all their permanents identical (Oko)

4. **Repetitiveness:** Does the card create varied game states?
   - Good: Different each game depending on context
   - Bad: Same loop every game (Cat-Oven)

5. **Frustration scaling:** Does frustration increase over the game?
   - Good: Threat that creates urgency (I need to answer this soon)
   - Bad: Tax effect that gets worse every turn (Rhystic Study)

6. **Digital experience:** On Arena/MTGO, does this create excessive triggers/clicking?
   - Good: Clean resolution
   - Bad: Mandatory triggers every turn cycle (Cauldron Familiar)

### Flagging Criteria

Flag a card if it scores "bad" on 2+ axes, even if its power level is acceptable. Cards that are powerful AND have play-pattern problems should be redesigned, not just recosted.

---

## The Constructed Push Framework

### The Push Dilemma

Play Design must create exciting cards that see Constructed play (avoiding "bulk rare" sets) while avoiding bans. The history shows both failure modes:

- **Too conservative:** Ixalan Standard was considered underpowered and boring. Card sales suffered.
- **Too aggressive:** Throne of Eldraine Standard had 7+ bans. Player trust suffered.

### The Push Safety Hierarchy

From safest to most dangerous:

1. **Narrow sideboard staples** — Cards that are powerful against specific strategies but weak elsewhere. These see Constructed play without warping metagames. (Example: Damping Sphere)

2. **Build-around rares** — Cards that require specific deckbuilding to be strong. The deckbuilding cost provides a natural limiter. (Example: Arclight Phoenix)

3. **Pushed mythics** — High-impact cards at mythic appear infrequently enough to not warp Limited. (Example: most planeswalkers)

4. **Pushed rares in specific colors** — Mono-colored cards that require commitment to that color. The color requirement provides deckbuilding tension. (Example: Steel Overseer)

5. **Pushed colorless cards** — DANGER ZONE. Any colorless card above rate will appear in every deck. (Example: Smuggler's Copter → banned)

6. **Pushed free/modal spells** — EXTREME DANGER. Cards with no mana cost or minimal conditions. (Example: Once Upon a Time → banned)

### The Safe Push Checklist

Before pushing a card's power level, verify:
- [ ] The card has a meaningful deckbuilding cost (color requirement, tribal requirement, archetype requirement)
- [ ] The card has interaction windows (can be countered, removed, or otherwise answered)
- [ ] The card doesn't punish its own archetype's natural counters
- [ ] The card doesn't scale with future sets' inevitable mechanics
- [ ] The card has a reasonable floor (not also a Limited bomb)
- [ ] The card hasn't been modified after primary testing

---

## Number Finalization Guidelines

Play Design's final responsibility is setting the exact numbers on cards. These guidelines help make the right calls.

### The Adjustment Ladder

When a card is flagged as too strong:

1. **Increase mana cost by 1** — the bluntest instrument. Effective but may kill the card entirely.
2. **Reduce stats by 1** — keeps the cost the same, reduces rate. Subtle.
3. **Add a color requirement** — changes {2}{R} to {1}{R}{R}. Reduces splash viability.
4. **Add "once per turn"** — prevents repeated abuse of triggered abilities.
5. **Change "each opponent" to "target opponent"** — fixes Commander scaling.
6. **Add "nonland" or "nontoken"** — narrows the effect's scope.
7. **Remove cantrip** — the card no longer replaces itself, adding real cost.

### The "One Knob" Rule

When adjusting a card, change ONE thing at a time. Multiple simultaneous changes make it impossible to evaluate the result. If one change isn't enough, make a second change in a separate pass.

### When to Cut vs. When to Fix

**Cut the card if:**
- It fails 3+ of the named tests (rate, zero-mana, combo, anti-counterplay, etc.)
- Its core design is the problem, not just its numbers
- It's a systemic flaw (energy-style resource without interaction)

**Fix the card if:**
- It fails 1-2 tests and the fix is obvious (raise mana cost, lower stats)
- The design is healthy but the numbers are wrong
- It fills an important structural role (signpost uncommon, archetype anchor)
