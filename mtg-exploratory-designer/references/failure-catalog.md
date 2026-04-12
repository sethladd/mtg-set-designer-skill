# Mechanic Failure Catalog

Every entry here is a mechanic that shipped and caused problems — or a mechanic that was killed before shipping because the exploratory/design team caught the issue. When evaluating a candidate mechanic, check it against every entry. If your candidate shares characteristics with a failure, document whether it avoids the failure mode or is vulnerable to it.

---

## Table of Contents

1. [Parasitism Failures](#parasitism-failures)
2. [Complexity Failures](#complexity-failures)
3. [Depth Illusion Failures](#depth-illusion-failures)
4. [Linearity Failures](#linearity-failures)
5. [Play Pattern Failures](#play-pattern-failures)
6. [Resource System Failures](#resource-system-failures)

---

## Parasitism Failures

### Energy (Kaladesh, 2016) — No Pressure Valve

**What it did:** Cards generated and spent energy counters. Energy persisted between turns with no decay.
**What went wrong:** No opponent interaction with energy. No cost to holding energy. Self-contained resource loop that created puzzles instead of games. Led to multiple Standard bans.
**The root cause:** The resource had no pressure valve — nothing forced spending, nothing let opponents interact, nothing made accumulation costly.
**The diagnostic question your candidate must answer:** "If a player accumulates this resource for 5 turns without spending it, is that (a) a strategic choice with tradeoffs, or (b) strictly optimal? If (b), the resource needs a pressure valve."
**What a fix looks like:** Energy with decay (lose 1 energy each upkeep), or energy visible to opponents who can interact with it, or energy that opponents also benefit from somehow.

### Splice onto Arcane (Kamigawa, 2004) — Extreme Type-Lock

**What it did:** Pay a cost to copy a spell's effect onto an Arcane spell you're casting.
**What went wrong:** Only worked with Arcane spells, which existed only in Kamigawa block. Outside that block, Splice cards were completely dead.
**The root cause:** Mechanic was locked to a subtype with no broader population. When the block rotated, the entire mechanic became nonfunctional.
**The diagnostic question:** "Does this mechanic reference a card type, subtype, or resource that only exists in this set? If so, what happens when those cards rotate or aren't drafted?"
**What a fix looks like:** "Splice onto Instant" would have been modular. The concept was sound; the type restriction killed it.

### Party (Zendikar Rising, 2020) — Fragile Assembly

**What it did:** Rewarded controlling one each of Cleric, Rogue, Warrior, and Wizard.
**What went wrong:** Full party (4 creatures of specific types) was too hard to assemble and too easy to disrupt. A single removal spell undid turns of work. The partial payoff (1-3 members) was dramatically weaker than full.
**The root cause:** High assembly cost + high vulnerability + non-proportional payoff. 3/4 of a party was worth far less than 3/4 of the full reward.
**The diagnostic question:** "If this mechanic requires assembling N pieces, is the partial payoff (N-1 pieces) still satisfying? If the payoff is binary (have it all or have nothing), it's fragile."
**What a fix looks like:** Proportional scaling (each party member adds equal value) or built-in redundancy (Changelings counting as any type, which ZNR did include but not enough of).

### Dungeons/Venture (AFR, 2021) — False Choice

**What it did:** Three dungeon tracks with escalating rooms. Each "venture" advanced you one room.
**What went wrong:** Lost Mine of Phandelver was almost always the correct dungeon. The other two were traps — their delayed payoffs weren't worth the setup. The mechanic promised meaningful choice but delivered a solved puzzle.
**The root cause:** When you offer N options, they must be within ~10% power of each other, or N-1 become irrelevant. One dominant path turns a "choice" mechanic into a linear one.
**The diagnostic question:** "If this mechanic offers multiple paths/modes, is there a clearly optimal one? Have you tested whether skilled players always choose the same option?"

---

## Complexity Failures

### Mutate (Ikoria, 2020) — Hidden Interaction Explosion

**What it did:** Stack creature cards to create chimeric creatures, combining abilities.
**What went wrong:** Interacted confusingly with virtually everything — Auras, Equipment, counters, copy effects, death triggers, ETB triggers, type-checking. Even expert players made mistakes during streamed events.
**Rosewater's assessment:** "Mutate is one of the most complicated mechanics we've ever made, and we've seen it confuse a lot of many players."
**The root cause:** The mechanic touched too many existing rules subsystems simultaneously. Each individual interaction was resolvable, but the combinatorial explosion was overwhelming.
**The diagnostic question:** "Pick 10 random Magic cards from recent sets. Does your mechanic interact cleanly with all of them? If you find even one confusing interaction, multiply by 25,000."
**Storm Scale:** 7/10 — hasn't returned since 2020.

### Banding (Alpha, 1993) — Combat Complexity Catastrophe

**What it did:** Creatures could form "bands" that attacked or blocked together, with the banding player assigning combat damage.
**What went wrong:** Combat is Magic's core system. Adding complexity to combat damage assignment confused even expert players. Rosewater: "When I was a judge, the number one rules question from the best players in the world was 'how does banding work?'"
**The root cause:** Complexity hidden inside the most frequently used game system (combat) is the most expensive complexity possible, because it triggers every single turn.
**The diagnostic question:** "Does this mechanic change how combat damage works? If yes, it must be dramatically simpler than you think it is. If a judge can't explain it in 15 seconds, it's too complex for combat."
**Storm Scale:** 11/10 — will never return.

### The Ring Tempts You (LotR, 2023) — Tracking Burden

**What it did:** Progressive mechanic with four levels. Each "tempt" advanced one level, granting escalating abilities to your Ring-bearer.
**What went wrong:** Required tracking which level you were at, which creature was the Ring-bearer, and what abilities that level granted — none of which was visible on the card. Conceptually rich but physically hard to track in paper play.
**The root cause:** Progressive mechanics without on-board representation create memory burden. If the game state isn't visible, players forget or dispute it.
**The diagnostic question:** "Can a player look at the board and determine the complete game state related to this mechanic? If the answer requires remembering hidden state (which level, which mode, how many triggers), the tracking burden may exceed the payoff."

### Companions (Ikoria, 2020) — Deckbuilding Restriction Miscalibration

**What it did:** Ten creatures with deckbuilding restrictions. If your deck met the restriction, you could cast the companion from outside the game.
**What went wrong:** The restrictions were far too easy to meet in competitive formats. Lurrus ("no permanents above 2 CMC") was trivial in Legacy/Modern. The power of a free eighth card overwhelmed any deckbuilding cost.
**The root cause:** Restrictions were tested against the wrong card pools. A restriction that's meaningful in Standard may be trivial in Modern, where decks already have tight curves.
**The diagnostic question:** "Test this restriction in EVERY format where the card will be legal. Is the restriction actually binding, or just a speedbump?"
**Historical note:** Companions were emergency errata'd (unprecedented) — now they cost 3 mana to move to hand, effectively a nerf applied after release.

---

## Depth Illusion Failures

### Radiance (Ravnica, 2005) — Symmetry Masking Shallowness

**What it did:** Target a creature, then the effect applies to all creatures sharing a color with it.
**What went wrong:** Effects were symmetrical, hitting your own creatures too. In a multicolor set (Ravnica), "all creatures sharing a color" was often "almost everything on the board." The targeting felt meaningless.
**Rosewater's assessment:** "Radiance is the least liked of all the guild mechanics. It's also hard to design cards for."
**The root cause:** The mechanic seemed to offer targeting choices, but in practice those choices rarely mattered — the effect hit everything anyway. Apparent depth (choose a target!) masked actual shallowness (the target barely matters).
**The diagnostic question:** "Does this mechanic create meaningful decisions, or does it create the *illusion* of decisions? If the optimal play is almost always the same regardless of the choice, the mechanic is shallow."

### Haunt (Guildpact, 2006) — Convoluted Setup, Mediocre Payoff

**What it did:** When a creature with haunt dies, exile it haunting another creature. When the haunted creature dies, the haunt effect triggers again.
**What went wrong:** Multi-step trigger chain (cast → ETB effect → die → exile → haunted creature dies → effect again). The payoff (getting the effect twice) wasn't proportional to the complexity of tracking it.
**Rosewater's verdict:** Called it a mistake with no plans to bring it back.
**The root cause:** The complexity-to-payoff ratio was inverted. The mechanic spent enormous complexity budget for a modest reward. Players couldn't tell if they were playing the mechanic correctly.
**The diagnostic question:** "Is the payoff proportional to the setup complexity? If explaining the mechanic takes 30 seconds and the payoff is 'the same effect happens again eventually,' the ratio is wrong."

### Clash (Lorwyn, 2007) — Punishes Correct Play

**What it did:** Both players reveal the top card of their library. Higher mana value wins the clash.
**Rosewater's assessment:** "I consider it a noble but failed attempt."
**What went wrong:** Winning clashes required having expensive cards on top — which means either your deck is full of expensive cards (bad deckbuilding) or you got lucky. The mechanic punished correct deckbuilding and rewarded randomness.
**The root cause:** The mechanic's optimization axis (high mana value cards) was misaligned with correct gameplay (efficient curve). A mechanic that rewards bad play is broken at a fundamental level.
**The diagnostic question:** "Does optimizing for this mechanic make your deck worse at everything else? If playing optimally for the mechanic conflicts with playing optimally for the game, the mechanic is misaligned."

---

## Linearity Failures

### Tribal in Ixalan (2017) — Drafts on Rails

**What it did:** Four tribes (Vampires, Dinosaurs, Merfolk, Pirates) each in specific color pairs with tribal payoffs.
**What went wrong:** Tribes were too insular — each only worked with itself. Drafts felt "on rails" because your first tribal pick locked you into a lane with no ability to pivot. There was no strategic tension in draft because the optimal play was always "take more of your tribe."
**The root cause:** No cross-pollination between tribes. Compare to Innistrad, where blue's self-mill fed both UB Zombies AND UG Flashback. In Ixalan, blue's Merfolk cards only helped Merfolk.
**The diagnostic question:** "If a player has drafted 5 cards toward Archetype A and then sees a powerful card for adjacent Archetype B, can they pivot? Or are their first 5 picks wasted?"
**What Innistrad did differently:** Tribes overlapped at the color level. Blue cards supported multiple strategies regardless of creature type. Each color was coherent on its own, and pairing any two colors produced a viable deck.

### Slivers — Linear Density Requirement

**What it did:** Every Sliver buffs every other Sliver, creating compound effects.
**What went wrong:** Requires extremely high density (25%+ of your deck must be Slivers) to function. In sets without enough Slivers, the mechanic is unplayable. In sets with enough Slivers, the mechanic dominates everything else.
**The root cause:** Ultra-linear mechanics create binary outcomes — either you have critical mass (deck is great) or you don't (deck is terrible). There's no middle ground.
**The diagnostic question:** "Does this mechanic have a critical mass threshold below which it doesn't function? If yes, is that threshold achievable in a normal draft without forcing?"

---

## Play Pattern Failures

### Annihilator (Rise of the Eldrazi, 2010) — No Counterplay

**What it did:** When this creature attacks, defending player sacrifices N permanents.
**What went wrong:** Creates a death spiral — once Annihilator triggers, the defending player falls further behind, making the next Annihilator trigger even worse. Games effectively ended on the first attack.
**The root cause:** No counterplay. The mechanic was miserable to be on the receiving end of. It violated the "fun to lose to" test completely.
**The diagnostic question:** "When your opponent uses this mechanic against you, do you still have interesting decisions? Or is the game effectively over?"
**Storm Scale:** 10/10 — Rosewater has called it a mistake.

### Miracle (Avacyn Restored, 2012) — Physical Gameplay Disruption

**What it did:** If the first card you draw each turn is a Miracle card, you may cast it for a reduced cost.
**What went wrong:** Required players to change how they physically draw cards (peeking at the card before adding it to hand). This created feel-bad moments (accidentally adding to hand = no Miracle), judge calls, and suspicion of cheating.
**The root cause:** A mechanic that requires players to alter their physical habits at the most frequent game action (drawing a card) creates friction that overwhelms any strategic depth.
**The diagnostic question:** "Does this mechanic require players to change how they physically interact with the game? If it changes drawing, shuffling, or card handling, the friction cost is enormous."

---

## Resource System Failures

### Poison Counters (early versions) — All-or-Nothing

**What early poison did wrong:** Original poison (10 counters = death) created a parallel win condition with no interaction. You either killed with poison or you didn't; there was no middle ground and no way for the defending player to remove counters.
**What Phyrexia: All Will Be One (2023) got right:** Toxic + Corrupted gave poison incremental payoffs (Corrupted cards get stronger when opponent has 3+ poison), created decision points (go all-in on poison or use it as an enabler?), and existed alongside normal damage as complementary strategies.
**The lesson:** A resource/counter system needs incremental payoffs, not just a binary threshold. If the only thing that matters is "do you have 10?", every number below 10 is equally meaningless.

---

## Pattern Summary: The Six Ways Mechanics Fail

When checking a candidate mechanic, verify it doesn't match any of these patterns:

1. **No pressure valve** — Resource accumulates without cost, interaction, or decay (Energy)
2. **Type-locked parasitism** — Only works with cards from this specific set (Splice onto Arcane)
3. **Interaction explosion** — Touches too many rules subsystems, creating confusing edge cases (Mutate)
4. **Misaligned optimization** — Rewards play that conflicts with correct deckbuilding (Clash)
5. **Binary payoff** — All-or-nothing thresholds with no satisfying partial credit (Party, early Poison)
6. **No counterplay** — Opponents have no interesting response to the mechanic (Annihilator, Energy)

If a candidate matches even one of these patterns, it needs a specific documented mitigation plan before it advances to the shortlist.

---

## Sources

- Mark Rosewater, "Lessons Learned" column series (Making Magic)
- Mark Rosewater, "State of Design" annual reviews (Making Magic)
- Mark Rosewater, "Twenty Years, Twenty Lessons" (GDC 2016)
- Mark Rosewater, "Storm Scale" rating articles (Making Magic)
- Mark Rosewater, "Vision Design, Set Design, and Play Design" (2017)
- Various "Mechanics of Magic" retrospectives
