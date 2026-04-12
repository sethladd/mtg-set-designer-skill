# Set Design Wisdom Catalog

Failure stories, counterintuitive insights, evolved thinking, and named heuristics for Set Design. These lessons were extracted from development columns, banned-card autopsies, and broken Limited format retrospectives. Consult this when filling the skeleton, calibrating removal, tuning curves, or balancing archetypes.

---

## Table of Contents

1. [Failure Stories](#failure-stories)
2. [Counterintuitive Insights](#counterintuitive-insights)
3. [Evolved Thinking](#evolved-thinking)
4. [Named Heuristics and Tests](#named-heuristics-and-tests)

---

## Failure Stories

### 1. Avacyn Restored — Vision without commons-level support

**The problem:** "Angels vs. Demons" was a clear vision, but Set Design broke the Limited format. Removal was intentionally weakened while rare bombs stayed at full power. Soulbond was pushed with only 19 cards, so even common soulbond creatures like Trusted Forcemage became overwhelming. The Loner mechanic (creatures better when alone) contradicted Soulbond (which requires pairing). Black got neither Miracles nor Soulbond — only Loners — making it the worst color. Blue-green dominated due to bounce and soulbond synergies.
**Root cause type:** Multiple format parameters adjusted simultaneously — weak removal AND increased bomb variance AND contradictory mechanics in one set.
**Lesson:** Never adjust multiple core format levers simultaneously. If you weaken removal, you must also weaken bombs. If two mechanics in the same set contradict each other's play patterns, one color will be stranded with the losing side.

### 2. Amonkhet — Hyper-aggro format that punished slow strategies

**The problem:** Exert was one of the most powerful aggressive mechanics ever printed, requiring "so much less work" than previous aggro mechanics. Cards like Gust Walker became effectively double-faced — one side reasonable, the other insane. The set's other mechanics (Embalm, Aftermath, Cycling) all punished slower strategies by requiring hefty mana investment. Critical failure: the best removal (Magma Spray, Compulsory Rest) was concentrated in the aggressive colors (red, white), while defensive removal like Electrify and Final Reward traded terribly on mana against Exert creatures. The format enabled unprecedented fourteen-land aggro decks.
**Root cause type:** Removal distribution mismatch. The aggressive colors got the efficient removal, creating a feedback loop where aggro both had the best threats AND the best answers.
**Lesson:** When calibrating format speed, check not just the total removal count but which colors own it. If the aggro colors have the best removal AND the best creatures, defensive strategies have no viable answer window. Removal quality must be distributed to give slower colors their own efficient answers.

### 3. Battle for Zendikar — Synergy collapse into bomb format

**The problem:** BFZ was designed as a synergy format, but when players discovered that splashing a third color for raw power outperformed any synergy line, "synergy format turned into a power level format." Green was the worst color by a massive margin. With everyone fighting over the same powerful cards, decks ran thin on playables. The format was simultaneously too slow (nothing closed games efficiently) and too bomb-dependent (rare quality determined outcomes).
**Root cause type:** Synergy payoffs were weaker than generic power. When synergy doesn't pay off, drafters abandon synergy for raw stats.
**Lesson:** In a synergy format, synergy payoffs must exceed generic power level by a visible margin. If a deck that ignores all your mechanics and just plays the best raw cards wins more than the deck that assembles your intended synergy, your format has failed. Test this explicitly: draft once ignoring all mechanics and once maximizing them. The synergy deck should win.

### 4. Ixalan — Drafts on rails with no pivot points

**The problem:** Four tribal factions (Pirates, Dinosaurs, Merfolk, Vampires) were so insular that once you committed to a tribe, there was no pivoting. "You just pick one of the themes and draft all the cards of that theme and most decks end up looking the same." Pirates were notably weak, "often feeling like the entire deck is Grizzly Bears." The lack of cross-archetype commons meant drafters who misread signals were punished catastrophically.
**Root cause type:** Archetypes designed as islands rather than a web. Each tribe's commons only worked in that tribe's deck.
**Lesson:** At least 40% of a color's commons must work in multiple archetypes. Shared enablers (self-mill that serves both UB Zombies and UG Flashback) create pivot points that make drafting a skill rather than a coin flip.

### 5. Oko, Thief of Crowns — Late redesign bypassed testing

**The problem:** Play Design "did not properly respect his ability to invalidate essentially all relevant permanent types, and over the course of a slew of late redesigns, lost sight of the sheer, raw power of the card." The team focused on his creature-stealing -5 ability and missed that his +1 elk ability was the broken part — it turned any opposing threat into a vanilla 3/3 while also making food tokens into 3/3 attackers. The card was pushed to make the Food mechanic work in Standard, but when Oko was banned, "you see basically no Food" — the mechanic's sole enabler was its biggest problem.
**Root cause type:** Late-stage changes bypassing the testing pipeline. Three-mana planeswalkers proved "riskier space than we were giving them credit for."
**Lesson:** Any card modification after primary playtesting ends is extremely high-risk. The testing pipeline exists to catch interactions the designer can't see. Bypassing it for "one small change" produces the most catastrophic failures in the game's history.

### 6. Hogaak, Arisen Necropolis — Mechanic stacking without interaction testing

**The problem:** Hogaak combined three powerful mechanics (delve, convoke, graveyard casting) on a single card. Delve had already caused bans (Treasure Cruise, Dig Through Time). Adding convoke meant the 8/8 could be cast for effectively zero mana. It could be recast from the graveyard, meaning removal wasn't permanent. Players needed "between six and ten sideboard cards" to face the matchup — an excessive sideboard tax indicating fundamental imbalance.
**Root cause type:** Combining previously-banned mechanics without recognizing their interaction. Each mechanic alone was manageable; together they were broken.
**Lesson:** When combining cost-reduction mechanics, test the absolute floor cost, not the expected cost. If a creature can theoretically cost 0 mana, it will cost 0 mana in competitive play. Every cost-reduction mechanic on a single card multiplies the danger.

### 7. Skullclamp — "Nerf" that created the strongest card

**The problem:** Originally +1/+2, Skullclamp was changed late in development to +1/-1 as a "nerf." This actually made it stronger by turning every 1-toughness creature into a 1-mana draw-two engine. Despite a month of remaining testing time, "no one really thought about testing the new version." Widely considered R&D's biggest design mistake.
**Root cause type:** Late change that inverted the card's function without re-evaluation. The new version was a fundamentally different card that needed fresh testing.
**Lesson:** A stat change is not a simple tweak — it can invert a card's function. +1/-1 is not "like +1/+2 but weaker"; it's a death trigger enabler. When modifying a card late, ask "does this change what the card DOES, or just how well it does it?" If the function changes, restart testing.

### 8. Omnath, Locus of Creation — Too many abilities on one card

**The problem:** Omnath replaced itself (draw a card), gained life, ramped mana, blocked well as a 4/4, AND dealt 4 damage — all on one card. It appeared in 72% of decks at the Grand Finals and was banned 18 days after release. Even after banning other enablers, Omnath decks had favorable matchups against 9 of 10 top decks.
**Root cause type:** Each individual ability was reasonable, but the combination covered every weakness. The card had no bad matchups because it did everything.
**Lesson:** When a card has 4+ abilities, test it not by evaluating each ability individually but by asking "what does this card NOT do?" If the answer is "nothing," the card is broken regardless of how reasonable each piece looks in isolation.

### 9. Born of the Gods — Mechanics without enablers at common

**The problem:** Inspired triggered on untap but lacked sufficient tap/untap enablers at common. Players had to rely on attacking to trigger Inspired, but in a board-stall format, attacking was dangerous. The set compounded Theros's problems while making its cooler aspects less accessible. Red and white were the only viable Limited colors.
**Root cause type:** Mechanic designed without ensuring the enabling infrastructure existed at the right rarity and density.
**Lesson:** For every mechanic that requires an enabler, count the enablers at common. If a mechanic triggers "whenever you do X," there must be enough common cards that do X — not at uncommon or rare, but at common, where drafters will reliably find them. The as-fan of enablers must match or exceed the as-fan of payoffs.

### 10. Kamigawa — Splice onto Arcane (parasitic design)

**The problem:** Splice onto Arcane only works with Arcane-subtyped spells, which only exist in Kamigawa block. "Soulshift and Splice Onto Arcane were incredibly insular and took up such a large part of the design space that the really excellent mechanics usually did not get the space they deserved." Combined with power-level concerns after Mirrodin, every card was underpowered AND parasitic.
**Root cause type:** Mechanic that creates its own ecosystem rather than plugging into Magic's existing systems.
**Lesson:** A mechanic that only works with other cards bearing the same mechanic consumes design space disproportionately. It forces the skeleton to dedicate critical common slots to enablers that are useless outside the mechanic's deck, starving other archetypes of support.

---

## Counterintuitive Insights

### 1. The skeleton matters more than individual card designs

Designers instinctively want to start with their coolest card idea and build around it. But the skeleton provides the "bird's-eye view" that prevents systemic failures. "You can sometimes lose the ability to see the big picture because you're too much in the details." A brilliant individual card that fills the wrong skeleton slot harms the format more than a boring card in the right slot helps it. Fill the skeleton first, then make cards interesting.

### 2. Removal density is the primary format speed lever

The creature suite gets most of the attention, but the removal suite defines the metagame. When common removal costs 1-2 mana more on average, formats get faster because aggressive creatures go unanswered. In Amonkhet, the best removal was in the aggro colors, creating an accelerating feedback loop. In Avacyn Restored, intentionally weakened removal alongside unchanged bombs made games feel decided by luck. Tuning removal is more impactful than tuning creatures.

### 3. As-fan is more important than total count

A mechanic can have 22 cards in a set but if they're concentrated at rare/mythic, most drafters never see them. Conversely, 13 cards with 5 at common can have meaningful pack presence. The formula-based as-fan calculation matters more than raw card count because commons appear ~3x more frequently than uncommons in packs. Design for as-fan, not for total card count.

### 4. Build-arounds need to be good even when they miss

Experienced designers put synergy effects on enters-the-battlefield abilities of otherwise-playable creatures. This ensures the card has baseline value even without its synergy pieces. A build-around that's unplayable without support creates a terrible experience for the drafter who opened it first and committed. You can't guarantee seeing more than one of any specific uncommon at a draft table — build-arounds must maintain reasonable floors.

### 5. Curve holes at common are catastrophic and unfixable at higher rarities

A missing 2-drop in a color at common means that color cannot build a reliable early game. An uncommon or rare 2-drop cannot fix this because they appear too infrequently. The design skeleton exists specifically to prevent this — it prescribes exact mana value slots per color. When you deviate from the skeleton's curve, you're accepting that some drafters will have unplayable decks.

### 6. Symmetric effects are not fair

R&D historically assumed symmetrical cards (Balance, Armageddon, Wheel of Fortune) were balanced because they affected all players equally. In practice, the player who can exploit the effect gains a massive advantage despite symmetrical wording. Symmetry of text does not produce symmetry of outcome.

### 7. Late-stage card changes are the most dangerous changes

Skullclamp, Oko, Smuggler's Copter, Aetherworks Marvel — all had critical changes after primary testing ended. The pattern: last-minute "fixes" bypass the testing pipeline that would have caught problems. If a card must change post-testing, it requires dedicated retesting proportional to the change's magnitude, not a casual "this seems fine."

---

## Evolved Thinking

### 1. From "commons carry the set" to "commons and uncommons carry the set together"

**Old approach (Draft Booster era):** 101 commons with 80 uncommons meant commons did most of the archetype support work. Signpost uncommons announced archetypes, but commons carried them.
**New approach (Play Booster era):** 81 commons with 100 uncommons means the load is shared. Uncommons now do much of the heavy lifting for archetype support, with signpost pairs (enabler + payoff) per archetype and supporting uncommons filling depth. An archetype needs ~14-16 commons plus ~8-12 uncommons.
**Why it changed:** Fewer commons means each common carries more weight. The uncommon increase provides the density that lost common slots would have provided.

### 2. From "removal as afterthought" to "removal as format architecture"

**Old approach:** Design exciting creatures and mechanics first, then fill remaining slots with removal. Removal was the last thing designed.
**New approach:** Design the removal suite early — it's the primary format speed lever. Decide target format speed first, then design removal density and efficiency to achieve that speed. The removal suite shapes the metagame more than any individual creature or mechanic.
**Why it changed:** Formats like Amonkhet (too fast due to weak defensive removal) and Avacyn Restored (bomb-dominated due to weak all removal) demonstrated that removal calibration determines format health.

### 3. From "rares are for Constructed, commons are for Limited" to "rares matter in Limited too"

**Old approach:** Rares were designed primarily for Constructed, and their Limited impact was secondary. Commons and uncommons defined Limited.
**New approach:** In Play Booster era, ~41% of packs contain two or more rares. Rares show up in draft much more frequently, so common removal must be able to answer rare-level threats. If commons can't deal with rares, the format devolves into "whoever opened the best rare wins."
**Why it changed:** The Play Booster structure puts more rares into circulation, making rare-vs-common interactions a first-order Limited concern rather than a corner case.

### 4. From "balance each card individually" to "balance the ecosystem"

**Old approach:** Cost each card on its own merits — a 3-mana 3/3 is fine, a removal spell at 2 mana is fine.
**New approach:** Evaluate cards in context. A 2-mana removal spell is fine in a slow format but format-warping in a fast one. A 3/3 for 3 is below rate in a format where the baseline creature is 3/4. Individual card balance only makes sense relative to the format's power level, speed, and archetype needs.
**Why it changed:** Hogaak, Oko, and Omnath demonstrated that individually-reasonable abilities become broken in combination. Cards exist in ecosystems, not in isolation.

---

## Named Heuristics and Tests

### 1. The Skeleton Completeness Test

**Question:** Does every slot in the design skeleton have a card, and does every card fit its slot's prescribed mana value, type, and role?
**Application:** Walk through each skeleton slot (CW01 through MA20). Flag any empty slots, any cards whose mana value doesn't match the slot's target, any creature slots filled with non-creatures (or vice versa), and any removal slots filled with non-removal.
**Diagnostic:** Export the set and the skeleton side-by-side. Every slot should map to exactly one card. Mismatches are the most common source of curve problems and archetype gaps.

### 2. The Curve Gap Diagnostic

**Question:** Does every color have at least 2 common creatures at each critical mana value (2, 3, 4)?
**Application:** For each color, count common creatures at MV 2, 3, 4, and 5. If any critical value has fewer than 2 creatures, that color has a curve gap that will produce non-functional decks. Check combined curves for each two-color archetype — a WU deck needs at least 4 playable 2-drops across both colors.
**Diagnostic:** Build a 5x7 grid (colors x mana values). Any cell with 0-1 creatures is a red flag. Zero at MV 2 is a format-breaking problem.

### 3. The Removal Density Check

**Question:** Does each color have its prescribed removal slots at common, and does the total removal produce the right as-fan?
**Application:** White: 2 removal (combat + exile). Blue: 2-3 (counterspell + bounce + freeze aura). Black: 3 (conditional + unconditional + overcosted). Red: 2 (small burn + large burn). Green: 2 (fight + bite). Total common+uncommon removal across all colors: 20-30 cards. Target as-fan: ~1.7-2.0 removal spells per booster.
**Diagnostic:** Count removal by color and rarity. If total removal as-fan is below 1.5, the format will be bomb-dominated. If above 2.5, the format will be a board-stall grind.

### 4. The As-Fan Threshold Test

**Question:** Does each named mechanic hit its target as-fan?
**Application:** Calculate using the formula: (% of commons with mechanic × 10) + (% of uncommons × 3) + (% of rares × 7/8) + (% of mythics × 1/8). Main set mechanics should target 1.5-2.75 per booster. Below 1.0 means most packs have zero copies and the mechanic feels absent. Above 3.0 means the mechanic may crowd out other gameplay.
**Diagnostic:** Calculate as-fan for each mechanic and for each mechanic within its primary colors. A mechanic with set-wide as-fan of 2.0 but color-specific as-fan of 0.5 in its secondary color means drafters in that color won't see it reliably.

### 5. The Build-Around Rate Test

**Question:** Does each signpost build-around uncommon have a reasonable floor AND sufficient common support?
**Application:** For each signpost uncommon: (a) Is it pickable even without synergy? It should have baseline value as a standalone card. (b) Do at least 10 commons in its two colors support its strategy? (c) Does the strategy work with only one copy of the signpost, since you can't guarantee multiples? (d) Do crossover cards with generic mana costs provide shared resources across archetypes?
**Diagnostic:** For each signpost, list the commons that support it. If the list is under 10, the archetype won't come together reliably in an 8-player draft.

### 6. The Format Speed Lever Check

**Question:** Do the format's speed levers match the intended format speed?
**Application:** Identify the format's "magic numbers": what power profitably attacks, what toughness profitably blocks, what toughness removal must beat. Count playable 2-drops per color at common (fast format: 3+, medium: 2, slow: 1-2). Verify at least one mechanic serves as a mana sink. Check whether common removal efficiently answers the format's best aggressive creatures. Count fast vs. slow archetypes — aim for balance with slight skew toward the intended speed.
**Diagnostic:** If the intended speed is "medium" but 7/10 archetypes are aggro and common removal costs 4+ mana, the format will be faster than intended.

### 7. The Archetype Support Count

**Question:** Does each of the 10 archetypes have enough card support to be draftable?
**Application:** Each archetype needs: 2 multicolor uncommon signposts (1 enabler + 1 payoff), 14-16 supporting commons across both colors, 8-12 supporting uncommons, and differentiation from archetypes sharing a color. Total minimum: ~22 cards at common+uncommon.
**Diagnostic:** Count supporting cards per archetype. Any archetype below 22 combined common+uncommon support cards is at risk of being undraftable.

### 8. The Color Balance Audit

**Question:** Are all five colors equally viable in Limited?
**Application:** Verify creature percentages match targets: White ~73%, Green ~71%, Red ~64%, Black ~62%, Blue ~53% creatures at common. Check that removal quality doesn't concentrate in only 1-2 colors. Ensure each color can support both aggressive and defensive strategies with its common suite. No color should have more than 2 commons above or below the per-color average.
**Diagnostic:** If one color has visibly worse removal, fewer on-curve creatures, or mechanics that contradict its archetype needs (like Black getting only Loners in Avacyn Restored), that color will be undraftable.

### 9. The Synergy vs. Power Test

**Question:** Does the synergy-maximizing draft strategy beat the generic-power draft strategy?
**Application:** Mentally draft two decks: one that ignores all set mechanics and picks the highest raw power cards, and one that maximizes the intended synergy lines. The synergy deck should have a meaningful edge. If the generic-power deck wins, the synergy payoffs need to be pushed harder.
**Diagnostic:** This catches the BFZ problem — a synergy format where ignoring synergy was correct. The test can be run with the draft simulator by comparing archetype-loyal vs. power-pick drafting strategies.

### 10. The Enabler-Payoff Ratio

**Question:** For every mechanic that requires enablers, do enablers outnumber payoffs?
**Application:** Count enablers and payoffs at each rarity. Enablers should outnumber payoffs by approximately 2:1 at common. If payoffs outnumber enablers, drafters will have rewards they can never trigger (Born of the Gods' Inspired problem). If enablers vastly outnumber payoffs, the mechanic feels mechanical rather than rewarding.
**Diagnostic:** For each mechanic, list enablers and payoffs separately with rarity. If the enabler-to-payoff ratio at common is below 1.5:1, the mechanic will feel unreliable.

---

## Sources

- Sam Stoddard's "Latest Developments" columns (2013-2017)
- Play Design Lessons Learned (Wizards, 2019)
- Mark Rosewater's "Nuts & Bolts" articles (#12-16)
- Rosewater's "Do the Math" (as-fan methodology)
- Avacyn Restored, Amonkhet, BFZ, Ixalan, Born of the Gods Limited retrospectives
- Oko, Hogaak, Skullclamp, Omnath banned-card autopsies
- Hipsters of the Coast format speed analysis
- MTGScribe Play Booster Design Skeleton Fact Sheet
