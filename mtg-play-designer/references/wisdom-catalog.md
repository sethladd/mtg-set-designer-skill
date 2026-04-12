# Play Design Wisdom Catalog

Every ban is a Play Design failure story. Every degenerate format is a lesson about what the testing process can miss. This catalog distills those lessons into a taxonomy of failure modes, counterintuitive insights, and named tests that the skill checks against when evaluating a card file.

---

## Table of Contents

1. [The Complete Ban Taxonomy](#the-complete-ban-taxonomy)
2. [Failure Stories — The Spectacular Misses](#failure-stories)
3. [Why Testing Misses Things — The Meta-Failures](#why-testing-misses-things)
4. [Counterintuitive Insights](#counterintuitive-insights)
5. [Named Tests and Checks](#named-tests-and-checks)

---

## The Complete Ban Taxonomy

Every major ban since 2017 falls into one of these root-cause categories. The skill checks for each category systematically.

### Category 1: Mana-Cost Mistake (Rate Too Pushed)

**Pattern:** The card does more than its mana cost should allow. Individual abilities are each reasonable, but the total exceeds fair rate for the cost.

**Examples:**
- **Oko, Thief of Crowns** (3 mana) — +1 that invalidated all permanent types by making them 3/3 Elk. ~70% of Mythic Championship field. Play Design admitted they "did not properly respect his ability to invalidate essentially all relevant permanent types."
- **Smuggler's Copter** (2 mana) — 3/3 flying, looting Vehicle with crew 1. 4-of in 60%+ of Standard decks. Colorless meant zero deckbuilding cost.
- **Omnath, Locus of Creation** (4 mana, RGWU) — Drew cards, gained life, added mana, dealt damage. Over 70% of Grand Finals field. Banned 18 days after release.
- **Fable of the Mirror-Breaker** (3 mana) — Generated tokens, filtered cards, copied creatures. Backbone of BR strategies for its entire Standard tenure.
- **Growth Spiral** (2 mana) — Instant-speed ramp + cantrip. 68% of day-1 metagame at Players Tour Finals.
- **Veil of Summer** (1 mana) — Hexproof + card draw against blue/black. Prevented metagame from self-correcting against green.
- **Uro, Titan of Nature's Wrath** (3 mana) — Life gain + draw + ramp that self-recurred from the graveyard. Couldn't be fought on any axis.
- **Rogue Refiner** (3 mana) — 3/2 that drew a card AND gave 2 energy. Above rate even without the mechanic.

**Detection heuristic:** For each card, tally the total value of all abilities in mana-equivalent. If total value exceeds the card's CMC by 2+, flag for review. Cards that cantrip (draw a card) on top of another meaningful effect are especially dangerous.

### Category 2: Mana-Cost Bypass

**Pattern:** A card or mechanic lets you deploy threats without paying their mana cost, breaking the fundamental resource balance of Magic.

**Examples:**
- **Aetherworks Marvel** — Cast Emrakul or Ulamog turn 3-4 by spending energy (which opponents can't interact with).
- **Fires of Invention** — Cast two free spells per turn. 55% win rate, favorable against all top 10 archetypes.
- **Hogaak, Arisen Necropolis** — 8/8 for zero mana via convoke + delve. Three times as many 5-0 trophies as the next deck in Modern.
- **Emrakul, the Promised End** — Delirium reduced the cast cost, but Aetherworks Marvel bypassed it entirely.

**Detection heuristic:** Any card with "cast without paying its mana cost," alternative casting costs, or cost-reduction mechanics needs testing against every high-CMC payoff in the target format. If the floor cost is 0, the card will cost 0 in competitive play.

### Category 3: Systemic Design Flaw

**Pattern:** An entire mechanic is broken, not just individual cards. The system has no interaction points or creates perverse incentives.

**Examples:**
- **Energy (Kaladesh)** — Energy is a resource opponents cannot interact with. No energy-removal effects exist. Cards that are above rate WITHOUT energy (Attune with Aether, Rogue Refiner) make the mechanic free upside. Four bans over two years. Storm Scale 6 — "play design issues are large."
- **Companion (Ikoria)** — Gave every player an extra guaranteed card. Restrictions that seemed meaningful were trivial in eternal formats. Lurrus: first card banned in Vintage for power since 1996. Unprecedented mechanic-wide errata (pay 3 to move companion to hand). Storm Scale 9 — "never have we needed to revise an entire mechanic for power-level concerns."

**Detection heuristic:** For any new resource system, verify: (a) opponents can interact with it, (b) cards aren't above rate even without the mechanic, (c) the mechanic doesn't give starting-hand consistency for free. For any "always available" effect, evaluate at 3x face value since it's guaranteed every game.

### Category 4: Unforeseen Two-Card Combo

**Pattern:** Two cards interact to create an infinite or game-winning combo that was missed in testing.

**Examples:**
- **Saheeli Rai + Felidar Guardian** — Infinite hasty tokens. R&D admitted the combo was overlooked. Emergency banned two days after an initial "no changes" announcement.
- **Geological Appraiser + Clone effects** — Discover into Glasspool Mimic/Mirror Image chain for turn-3 kills. Community found it day one of release.
- **Nadu, Winged Wisdom + Shuko** — Zero-mana equipment triggering Nadu repeatedly. Lead designer confirmed the final card version was never playtested.

**Detection heuristic:** Systematically cross-check: (a) ETB blink/copy effects against all planeswalker minus abilities, (b) Discover/Cascade effects against all clone/copy creatures at the discovered CMC, (c) zero-mana activated abilities against all "whenever targeted" triggers, (d) "cast without paying" effects against all high-CMC payoffs.

### Category 5: Play-Pattern Problem

**Pattern:** The card is balanced by win rate but makes the game miserable to play. Interaction is denied, agency is removed, or game length is distorted.

**Examples:**
- **Teferi, Time Raveler** — Static ability prevented opponents from casting instants. Created "repetitive play patterns and reduced capability for interaction." 20%+ of games included this card.
- **Nexus of Fate** — Infinite turns where opponents couldn't play. Balanced by win rate on paper, but "acts to prevent the opponent from playing at all." Banned in BO1 Standard, Historic, Pioneer.
- **Cauldron Familiar** — Cat-Oven loop was technically balanced but miserable to play against, especially on Arena (excessive clicking). Suppressed aggro/midrange creature strategies.
- **Reflector Mage** — Tempo loops that prevented opponents from deploying creatures.

**Detection heuristic:** Flag cards that: (a) prevent opponents from casting spells/creatures/abilities, (b) take extra turns repeatedly, (c) create mandatory repetitive loops, (d) remove opponent agency without advancing toward a game conclusion.

### Category 6: Anti-Counterplay Design

**Pattern:** The card shuts down the strategies that naturally counter its archetype, collapsing metagame self-correction.

**Examples:**
- **Rampaging Ferocidon** — Punished lifegain AND going wide — the exact strategies that counter aggro. Banned preemptively to keep metagame self-correction functional.
- **Invoke Despair** — Destroyed enchantments, creatures, and planeswalkers (or drew cards), preying on the exact permanent types that counter removal-heavy black.
- **Veil of Summer** — Gave complete protection against the colors (blue/black) that naturally check green.

**Detection heuristic:** For each card, identify what archetype it belongs to, then check whether it also punishes that archetype's natural predators. Cards that are strong against their own counters collapse the metagame rock-paper-scissors.

### Category 7: Scaling / Snowballing

**Pattern:** The card gets stronger with each new set, or generates resources that compound over time. What's fair at launch becomes broken later.

**Examples:**
- **Up the Beanstalk** — Drew cards whenever you cast 5+ mana spells. As more cost-reduction was printed, "the puzzle was solved" repeatedly.
- **Field of the Dead** — A land that made zombies. Zero deckbuilding cost. Eventually won the game by itself.
- **Wilderness Reclamation** — Mana doubling. 54% of metagame at Players Tour Finals.
- **Lucky Clover** — Doubled Adventure spells for free. 2-mana artifact with no tap cost scales dangerously.
- **Dockside Extortionist** (Commander) — Treasure generation scaling with three opponents' combined artifacts/enchantments.

**Detection heuristic:** Flag cards that: (a) trigger on a condition that future sets will inevitably expand, (b) generate resources based on opponents' board states, (c) have no mana investment beyond initial cast, (d) are lands with powerful non-mana abilities.

### Category 8: Late-Change Bypass

**Pattern:** The card was modified after the primary testing window closed, and the new version was never properly tested.

**Examples:**
- **Oko, Thief of Crowns** — Late redesigns "lost sight of the sheer, raw power of the card."
- **Nadu, Winged Wisdom** — "We didn't playtest with Nadu's final iteration." Flash was removed and replaced with triggers that interacted with zero-mana abilities.
- **Skullclamp** — Changed from +1/+2 to +1/-1 as a "nerf." Actually inverted the card's function into a 1-mana draw-two engine. "No one really thought about testing the new version."

**Detection heuristic:** This is a process check, not a card-file check. The skill flags it as a warning: "Any card modified after primary balance testing must receive dedicated re-testing."

### Category 9: Free/Zero-Cost Problem

**Pattern:** Cards that cost 0 mana (or effectively 0) have no real deckbuilding cost, so they warp formats by being auto-includes.

**Examples:**
- **Once Upon a Time** — Free on first cast. Made combo/synergy decks too consistent.
- **Ramunap Ruins** — A land that doubled as reach damage. No deckbuilding cost.
- **Field of the Dead** — A land that generated tokens. No deckbuilding cost.
- **Mana Crypt** (Commander) — At 40 life, the 1.5 life/turn drawback is irrelevant.
- **Jeweled Lotus** (Commander) — "Five mana on turn two without needing a good hand."

**Detection heuristic:** Any card that costs 0 under any circumstance, or any land with a powerful non-mana ability, or any card whose restriction is trivially easy to meet in the target format.

---

## Failure Stories

### 1. The FIRE Philosophy Overcorrection (2018-2020)

Play Design adopted the FIRE philosophy (Fun, Inviting, Replayable, Exciting) and intentionally powered up Standard to be "somewhere in the range of Standard circa Return to Ravnica and Theros." The result was the most ban-heavy period in Magic history: Oko, Uro, Omnath, Fires of Invention, Wilderness Reclamation, Growth Spiral, Teferi, Field of the Dead, Once Upon a Time, Veil of Summer — all banned within 18 months.

**Lesson:** Power level is not the same as fun. Pushing power creates memorable individual cards but can destroy format health. The line between "exciting" and "broken" is thinner than it appears.

### 2. The Energy Trap (2016-2018)

Energy was popular with players and had rich design space. But it was a closed resource system with no opponent interaction. Cards that were above rate even without their energy production (Attune with Aether = Lay of the Land + 2 energy; Rogue Refiner = 3/2 draw a card + 2 energy) made the mechanic "free upside" rather than a real cost. Four cards were banned across two years before the problem was fully addressed.

**Lesson:** Parasitic resource systems are either useless (underpowered cards that need the resource) or broken (above-rate cards that generate free resource). There is no stable middle ground without opponent interaction.

### 3. The Companion Catastrophe (2020)

Companion gave players a guaranteed extra card every game. Lurrus's deckbuilding restriction ("no permanents above 2 CMC") was trivial in Vintage, Legacy, and Modern. Within two weeks Lurrus was the most-played card in every eternal format. The fix — unprecedented mechanic-wide errata — broke the social contract that printed cards work as printed. Rosewater: Storm Scale 9, "nearly impossible to return."

**Lesson:** Starting-hand consistency is the most dangerous thing to give players for free. Any effect that adds a guaranteed card breaks foundational assumptions about variance. Deckbuilding restrictions must be genuinely costly in EVERY format the card is legal in.

### 4. The Nadu Process Failure (2024)

Nadu's lead designer confirmed the final printed version was never playtested. The card's text was changed after the testing window — flash was removed and replaced with a triggered ability that interacted with zero-mana equipment (Shuko). "The last round of folks who were shown the card in the building missed it too." Banned in Modern within weeks.

**Lesson:** Late-stage changes are not "small adjustments" — they are new cards that need full testing. The testing pipeline exists precisely to catch interactions designers can't see in isolation.

### 5. The Saheeli Emergency (2017)

Saheeli Rai + Felidar Guardian created an infinite-combo kill. R&D initially announced "no changes" to Standard, then reversed course two days later with an emergency ban — the first emergency ban in Standard's history. The combo had been identified before release but was incorrectly evaluated as too fragile.

**Lesson:** Known combos dismissed as "too fragile" should be treated as real until proven otherwise. The existence of a two-card infinite combo in Standard is always an emergency, regardless of perceived fragility.

---

## Why Testing Misses Things

### 1. Incomplete Card Pools

Play Design tests each set in isolation or with 1-2 adjacent sets. They cannot test against every card in Modern, Pioneer, or Commander. Hogaak combined mechanics from different eras (delve + convoke + graveyard casting) in ways no single-set test would catch.

### 2. Wrong Metagame Prediction

The Future Future League tries to predict what Standard will look like a year from now. But real metagames are solved by millions of players, not dozens. Field of the Dead was designed as a fun casual card, not as a competitive finisher.

### 3. Underestimating Synergy Shells

Individual cards test fine. But when combined with an existing shell of enablers, they become broken. Omnath was fine in vacuum but dominated because ramp cards (Growth Spiral, Uro, etc.) already existed.

### 4. Commander Blindspot

Until 2021 (when Casual Play Design was formed under Melissa DeTora), Commander was barely tested. Effects that scale with opponent count were evaluated for 1v1, not 4-player.

### 5. Digital Play Pattern Blindspot

Cauldron Familiar's Cat-Oven loop was "fine" in paper but miserable on Arena due to excessive clicking. Digital play patterns weren't systematically evaluated until after the ban.

### 6. Deckbuilding Cost Miscalculation

Companion restrictions that seemed meaningful in Standard were trivial in eternal formats. Ramunap Ruins cost "a land slot" — which is no cost when your deck wants deserts anyway.

### 7. Late-Change Testing Gap

Oko, Nadu, and Skullclamp were all changed after the primary testing window. The assumption that "small changes don't need retesting" is the most dangerous assumption in Play Design.

---

## Counterintuitive Insights

### 1. Win rate is not a sufficient measure of balance

Nexus of Fate, Teferi Time Raveler, and Cauldron Familiar all had acceptable win rates but were banned for play-pattern reasons. A card can have a 50% win rate and still ruin a format if every game it appears in is miserable.

### 2. Colorless cards are more dangerous than colored cards

Smuggler's Copter and Reckoner Bankbuster warped formats because they had zero deckbuilding cost — any deck could play them. A 3/3 flying vehicle for 2 is dangerous specifically because it's colorless.

### 3. Cards that are good against their own counters are format-warping

Rampaging Ferocidon punished the strategies that beat aggro. Veil of Summer protected green from the colors that check it. These cards collapse the metagame's immune system.

### 4. "Fair on its own" + parasitic mechanic = broken

Energy cards that were good even without energy (Attune, Rogue Refiner) made energy free upside. Any card in a parasitic system that exceeds rate without the mechanic breaks the system.

### 5. Lands with powerful abilities are the most underrated ban risks

Field of the Dead, Ramunap Ruins, and the original dual lands are all problematic because they occupy a slot that has zero opportunity cost. Lands don't compete with spells for deck slots.

### 6. Three-mana planeswalkers are categorically dangerous

After Oko, Play Design committed to making three-mana planeswalkers "sparingly, carefully." The combination of early deployment + loyalty growth + repeatable effects at that cost creates cards that warp games before opponents can interact.

### 7. The biggest danger is the card you changed last

Oko, Nadu, and Skullclamp share the same root cause: post-testing modifications. The cards that bypass the testing pipeline are statistically the most likely to be broken.

---

## Named Tests and Checks

### 1. The Rate Card Test

**Question:** Does this card's total value exceed the fair rate for its mana cost?
**Method:** Sum all abilities in mana-equivalent using the rate baselines. A 3-mana card that draws a card (~1.5 mana), gains 3 life (~0.5 mana), and puts a land into play (~2 mana) is providing ~4 mana of value for 3 mana — flag it.
**Catches:** Oko, Uro, Omnath, Fable.

### 2. The Zero-Mana Floor Test

**Question:** Can this card ever cost 0 mana to deploy?
**Method:** Check all alternative casting costs, cost-reduction mechanics, and "cast without paying" enablers in the target format. If the floor cost is 0, the card WILL cost 0 in competitive play.
**Catches:** Hogaak, Once Upon a Time, Mana Crypt.

### 3. The Colorless Ubiquity Test

**Question:** Is this card colorless and above rate for what it does?
**Method:** Any colorless card that's above rate in a specific category (card draw, creature stats, removal) will appear in every deck, because it has zero deckbuilding cost.
**Catches:** Smuggler's Copter, Reckoner Bankbuster, Mana Crypt.

### 4. The Anti-Counterplay Test

**Question:** Does this card punish the strategies that naturally counter its archetype?
**Method:** For each card, identify its archetype. Then check: does it also hate on the strategies that beat that archetype? Aggro cards that punish lifegain, control cards that punish instant-speed interaction, green cards that protect from blue/black.
**Catches:** Rampaging Ferocidon, Veil of Summer, Invoke Despair.

### 5. The Commander Scaling Test

**Question:** Is this card 3x as powerful in a 4-player game?
**Method:** Flag all instances of "each opponent," life-based drawbacks (irrelevant at 40 life), resource generation based on opponents' board states, and "target opponent" effects that become "choose the weakest" in multiplayer.
**Catches:** Dockside Extortionist, Rhystic Study, Mana Crypt, Jeweled Lotus.

### 6. The Two-Card Combo Scan

**Question:** Does this card form an infinite combo with any card in the target format?
**Method:** Cross-check against these high-risk patterns: (a) ETB blink/copy + planeswalker minus abilities, (b) Cascade/Discover + clone effects, (c) zero-cost activated abilities + "whenever targeted" triggers, (d) untap effects + tap-for-value creatures, (e) death triggers + sacrifice-recursion loops.
**Catches:** Saheeli + Felidar Guardian, Geological Appraiser + Glasspool Mimic, Nadu + Shuko.

### 7. The Play-Pattern Evaluation

**Question:** Even if balanced by win rate, is this card miserable to play against?
**Method:** Check for: (a) interaction denial (prevents casting spells/using abilities), (b) extra turns loops, (c) mandatory repetitive triggers, (d) removal of opponent agency, (e) excessive digital clicking/triggers.
**Catches:** Teferi Time Raveler, Nexus of Fate, Cauldron Familiar.

### 8. The Scaling Futures Test

**Question:** Will future sets make this card stronger?
**Method:** Flag cards that trigger on conditions future sets will inevitably expand (casting spells, playing lands, putting counters, etc.) unless they have built-in limiters (once per turn, costs increase, etc.).
**Catches:** Up the Beanstalk, Field of the Dead, Lucky Clover.

### 9. The Parasitic System Test

**Question:** Is this mechanic's resource interactable?
**Method:** For any new resource system, verify: (a) opponents can deplete or interact with the resource, (b) individual cards aren't above rate without the resource, (c) the resource doesn't accumulate indefinitely.
**Catches:** Energy (Kaladesh), Companion.

### 10. The Post-Testing Change Audit

**Question:** Was any card modified after primary balance testing?
**Method:** This is a process flag, not a card-file check. Any post-testing modification requires dedicated re-testing. "Small changes" are the most dangerous changes.
**Catches:** Oko, Nadu, Skullclamp.
