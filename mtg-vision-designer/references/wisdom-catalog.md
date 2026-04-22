# Vision Design Wisdom Catalog

Failure stories, counterintuitive insights, evolved thinking, and named heuristics for Vision Design. These lessons were extracted from 20+ years of vision design handoff documents, Lessons Learned columns, and State of Design retrospectives. Consult this when defining pillars, choosing mechanics, or designing archetypes.

---

## Table of Contents

1. [Failure Stories](#failure-stories)
2. [Counterintuitive Insights](#counterintuitive-insights)
3. [Evolved Thinking](#evolved-thinking)
4. [Named Heuristics and Tests](#named-heuristics-and-tests)

---

## Failure Stories

### 1. Battle for Zendikar — The split identity failure

**The problem:** BFZ tried to be both "adventure world" (what players loved about original Zendikar) and "Eldrazi invasion" (the unresolved story hook). These two identities competed for card slots, mechanics, and emotional tone. The Eldrazi consumed a huge percentage of mechanical resources — defining their subtypes, reworking unpopular Rise of the Eldrazi choices, building Converge — leaving too little room for landfall, quests, and traps.
**Rosewater's self-diagnosis:** "I didn't figure out I was making the wrong set until after it was too late to change it." The problem wasn't execution — it was premise. The set's concept forced designers to spend resources on things players didn't enjoy.
**Root cause type:** Flawed premise. Brilliant execution cannot save a wrong concept.
**Lesson:** Before committing to a vision, ask: "Does this premise leave room for the mechanics players will enjoy?" If the concept forces you to spend most of your complexity budget on unfun things, pick a different concept. The key to a good set is setting yourself up to succeed at the concept stage, not grinding execution on a doomed premise.

### 2. Original Ixalan — The insular archetype web

**The problem:** Ixalan's vision was clear: four tribal factions (Pirates, Dinosaurs, Merfolk, Vampires) fighting over treasure. But the archetype web was too rigid — each tribe was mechanically self-contained with no cross-pollination. Vision Design defined distinct factions without defining connections between them.
**Root cause type:** Right vision, wrong structure. The identity was fine; the archetype web was broken.
**Lesson:** Vision Design must define not just what each archetype IS, but how adjacent archetypes CONNECT. The web matters more than individual nodes. If a drafter can't pivot from their first three picks to an adjacent archetype, the format is on rails.

### 3. Born of the Gods — The invisible set

**The problem:** Born of the Gods was the middle set of Theros block. Rosewater admitted he was so focused on making the third set (Journey into Nyx) work that he made the second set "give up too much." Enchantment-matters cards were withheld for the third set. Tribute replaced Monstrosity unnecessarily. Inspired triggered on untap but lacked sufficient enablers at common.
**Root cause type:** Vision sacrificed for another product. The set had no reason to exist beyond block obligation.
**Lesson:** Every release must justify its own existence with clear mechanical identity. Never sacrifice one product to set up another. If a mechanic (like Inspired) requires specific enablers, those enablers must exist at common in sufficient density to actually work in Limited.

### 4. Ikoria — Two high-maintenance mechanics

**The problem:** Vision Design handed off both mutate and companion — each demanding enormous downstream design and balance attention. Mutate's original creature-type restrictions were loosened for playability but lost thematic connection. Companion shipped with power-level problems that resulted in an unprecedented rules errata.
**Root cause type:** Vision overloaded. Rosewater's lesson: "A vision design should only have one high-maintenance component."
**Lesson:** Limit each set to ONE mechanic that requires extensive rules support, complex interactions, or novel design territory. If two mechanics each demand center stage, cut one — even if both are exciting in isolation. The downstream teams can only properly develop one complex mechanic at a time.

### 5. Kamigawa — Original vs. Neon Dynasty (same world, different visions)

**Original Kamigawa (2004):** Creative was locked in before mechanics were finalized, producing "ham-fisted design and parasitic mechanics." The Shinto mythology source material lacked mainstream resonance. The "legendary matters" theme was invisible at common. Market research scores were the lowest since tracking began — mechanically AND creatively.
**Neon Dynasty (2022):** Found "tradition versus modernity" — an authentic Japanese cultural tension that mapped perfectly onto enchantments-vs-artifacts. Modified/Enhanced bridged both sides mechanically. Returning mechanics (Channel, Ninjutsu) served as framework. Fan response was "the best I've seen" (Rosewater).
**Root cause type:** NEO found the vision through mechanical discovery (artifacts vs. enchantments), not by forcing mythology onto cards.
**Lesson:** The best visions find a core conflict that is simultaneously flavorful AND mechanically expressible. When mechanics and flavor are the same thing (tradition=enchantments, modernity=artifacts), design is frictionless. When they're bolted together (Kamigawa's Splice onto Arcane), you get parasitic, disconnected designs.

### 6. Strixhaven — Pillars that competed

**The problem:** Strixhaven had multiple identity layers competing for attention: five enemy-color colleges, instants-and-sorceries-matter mechanics, and the Mystical Archive (reprinted spells with special frames). The mechanical identity (spell-slinging) competed with the faction identity (five colleges with distinct philosophies). Most colleges didn't feel mechanically distinct from their Ravnica equivalents.
**Root cause type:** Pillars competing instead of reinforcing. The spell-matters pillar and the faction-identity pillar pulled design in different directions rather than converging on a unified experience.
**Lesson:** Run the Pillar Reinforcement Test: "If I describe all three pillars to a stranger, does it sound like ONE set or THREE sets?" Strixhaven sounded like three — a spell-matters set, a faction set, and a reprint showcase. The pillars needed to be aspects of one identity, not parallel tracks.

### 7. Avacyn Restored — Vision without commons-level support

**The problem:** "Angels vs. Demons" was a clear, compelling vision, but the Limited format was broken. The Loner mechanic (creatures better when they're your only creature) was thematically clever — villains fracturing while heroes unite via Soulbond — but mechanically terrible. Soulbond was pushed; removal was intentionally weakened; rare bombs dominated. Black became unplayable because Loner was anti-synergistic with board-building and too slow against aggro.
**Root cause type:** Vision that worked at mythic but broke at common. The theme was expressed through bombs and build-arounds, not through the commons that define Limited play.
**Lesson:** A vision that doesn't translate to commons is empty. If your villain mechanic is inherently disadvantageous in a game about building board states, the vision needs reworking. Commons carry the set. If only rares deliver on the theme, Limited breaks.

---

## Counterintuitive Insights

### 1. Overdelivery is a feature, not a bug

Vision Design should hand off MORE than Set Design needs — more mechanics, more card designs, more backup options. The handoff is a menu, not a prescription. Rosewater: "Vision Design deliberately includes extra mechanics so Set Design has options." Bloomburrow's handoff included Fellowship (ultimately cut), but because the handoff anticipated the problem Fellowship solved, Set Design could find alternative solutions. Give Set Design 4-5 mechanics knowing they'll keep 2-3.

### 2. The best mechanic is often the simplest one

Landfall, Flashback, Cycling, Kicker — the most beloved mechanics in Magic's history are conceptually simple. Complex novel mechanics impress in design documents but simple resonant mechanics play well for years. Vision designers instinctively want to invent something new and clever. But the cleverest thing may be to return a proven mechanic or create a simple twist on existing design space.

### 3. Backup mechanics should be fundamentally different, not variations

If your primary mechanic is a triggered ability (like Landfall), your backup shouldn't be another triggered ability (like Constellation). It should be something structurally different — a resource system, a cost reduction, a modal spell pattern. If the primary fails, you need a genuine alternative, not a slight variation that will fail for the same reasons.

### 4. Vision Design's job is to make Set Design's job easy, not impressive

A brilliant vision that Set Design can't execute is worse than a simple vision they nail. The handoff is a communication document. If the Set Design lead reads it and doesn't immediately see how to build a set from it, the vision has failed regardless of how innovative it is. Simplicity of communication trumps sophistication of concept.

### 5. Three pillars is not optional — it's the number

Two pillars produce thin sets that feel like they're about one thing. Four or more pillars produce unfocused sets that feel like they're about nothing. Three is backed by 20+ years of handoff documents. Every published handoff uses three pillars (occasionally four, but three is the strong default). The third pillar is often the play-feel pillar — how the set should FEEL to play, not just what it does mechanically.

---

## Evolved Thinking

### 1. From "design the set" to "design the identity"

**Old approach:** Vision Design tried to design actual cards — filling the skeleton, writing rules text, costing creatures.
**New approach:** Vision Design defines the set's identity (pillars, mechanics, archetypes, tone) and creates a prototype card file to prove the identity works. Set Design does the actual card-by-card design.
**Why it changed:** When Vision Design tried to make final cards, Set Design had to redo everything. The old handoff point was wrong. Vision's real job is to answer "What is this set about?" definitively, then let specialists build from that answer.

### 2. From "mechanic-first" to "play-pattern-first"

**Old approach:** Choose interesting mechanics, then figure out what play patterns they create.
**New approach:** Define the desired play experience first ("the board gets scarier each turn," "you're building toward a dramatic transformation," "resources matter more than creatures"), then find mechanics that deliver that experience.
**Why it changed:** Mechanic-first design produced sets with clever mechanics that didn't create fun play patterns (e.g., Radiance in original Ravnica looked clever but played terribly). Play-pattern-first design ensures the experience is fun before committing to specific implementations.

### 3. From "one lead designs everything" to "vision summit feedback"

**Old approach:** The lead designer developed the vision alone or with a small team, then handed it off.
**New approach:** Mid-process, Vision Design presents to the broader R&D group at a "Vision Summit." The summit catches pillar conflicts, blind spots, and execution risks before they're baked in. This was formalized after Ikoria showed what happens when a vision has problems no one caught early enough.
**Why it changed:** Individual designers have blind spots. BFZ's premise problems and Ikoria's overloaded mechanics might have been caught if a broader group had reviewed the vision mid-process.

### 4. From "UB is a reskin" to "UB is a translation"

**Old approach:** Universes Beyond was conceptualized as taking a normal Magic set and re-skinning it with IP flavor.
**New approach:** Build mechanics FROM the IP's systems (Rad counters from Fallout's radiation, The Ring Tempts You from LotR's corruption, Saga Creatures from Final Fantasy's summons). The set should feel designed FOR the IP, not decorated with it.
**Why it changed:** Re-skinned sets feel generic. System-translation sets feel authentic. LotR and Final Fantasy succeeded because their mechanics were inseparable from the IP; early UB products that re-used existing mechanics with IP art felt hollow.

---

## Named Heuristics and Tests

### 1. The Pillar Reinforcement Test

**Question:** If you describe all three pillars to a stranger, does it sound like ONE set or THREE sets?
**Application:** Innistrad's pillars (gothic horror / transformation / graveyard-as-resource) all point to one experience: surviving a haunted world where nothing stays dead. BFZ's pillars (adventure / Eldrazi / allies) pointed to three different games. If your pillars are parallel tracks rather than facets of one gem, they'll compete for design resources.
**Diagnostic:** Write each pillar on a separate card. Can someone reading all three cards predict what the set plays like? If each pillar suggests a different game, they're competing.

### 2. The Selling Sentence Test

**Question:** Can you sell this set in one sentence that a player would repeat to a friend?
**Application:** "It's the gothic horror set where your creatures transform at night." "It's the set where lands are alive and dangerous." "It's cute animals building civilizations." If your sentence is longer than 15 words or requires caveats, the identity isn't crisp enough.
**Diagnostic:** If you need "and" in your selling sentence ("it's about adventure AND alien invasion"), you might have competing identities.

### 3. The Common Stamp Test

**Question:** If you look at 5 random commons from this set, can you identify which set they're from?
**Application:** Innistrad commons feature transform, morbid, and flashback. Zendikar commons feature Landfall and adventure tropes. Born of the Gods commons look like they could be from any set. If your commons don't carry the set's identity, most players will never experience that identity.
**Diagnostic:** Pull 5 commons from each color. Do they collectively communicate the set's emotional promise and mechanical theme? If they could be from Core Set 2025, your vision isn't reaching common rarity.

### 4. The Drafter's First-Pick Test

**Question:** In pack 1, pick 1, does a drafter know which archetype a card points toward?
**Application:** Signpost uncommons should clearly signal their archetype. Common creatures should have obvious homes. If a drafter's first pick gives no information about what archetype they should be in, the archetypes aren't clearly signposted.
**Diagnostic:** For each signpost uncommon, could a new drafter guess the archetype from reading the card? If the connection requires deep knowledge of the format, the signpost isn't working.

### 5. The Backup Pivot Test

**Question:** If the primary mechanic fails, can you swap in the backup without rewriting more than 30% of the card file?
**Application:** Vision Design should include 1-2 backup mechanics. These backups should slot into the same archetype homes and serve the same pillars as the primary, so that cutting the primary doesn't require restructuring the entire set.
**Diagnostic:** Imagine Set Design kills your favorite mechanic. Does your backup fit in the same slots, serve the same pillar, and support the same archetypes? If swapping requires rewriting commons across three colors, the backup isn't a true backup.

### 6. The Archetype Adjacency Test

**Question:** For every pair of adjacent archetypes (sharing a color), can a drafter pivot from one to the other without losing their first 3 picks?
**Application:** In Innistrad, a drafter who starts picking blue self-mill cards can pivot from UB Zombies to UG Flashback without wasting early picks — blue self-mill serves both. In Ixalan, a drafter picking Merfolk cards was locked into Merfolk with no pivot available.
**Diagnostic:** For each shared color (e.g., blue is in WU, UB, UR, UG), list the commons. Do at least 40% of a color's commons work in multiple archetypes? If most commons only work in one archetype, the web is too rigid.

### 7. The NWO Common Budget

**Question:** Do more than 20% of your commons have red-flag complexity?
**Application:** Red flags include: multiple abilities, reference to zones other than the battlefield, state-tracking requirements, triggered abilities during opponent's turn, more than 3 lines of rules text, or new named keywords without reminder text. Target: ≤20% red-flagged commons out of ~81 total.
**Diagnostic:** Count your red-flagged commons. If it's 17+ (out of 81), simplify or promote complex cards to uncommon. See `references/new-world-order.md` for the full red-flag checklist.

### 8. The Handoff Clarity Test

**Question:** If you gave this handoff document to a Set Designer who knows nothing about this set, would they know what to build?
**Application:** The handoff should answer: What is this set about? What are the three pillars? What mechanics exist? What are the ten archetypes? What should the set feel like to play? What problems did you encounter and not solve? A Set Designer reading the handoff should feel confident starting work within an hour.
**Diagnostic:** Have someone unfamiliar with the set read the handoff. Can they summarize the set in one sentence? Can they name all three pillars? Can they describe at least 3 of the 10 archetypes? If not, the handoff needs revision.

---

---

## Wisdom from the Mechanics Catalog (2024–2025 era)

### 1. Ward replaced Hexproof as the protection default

Hexproof is still officially evergreen, but since Strixhaven (2021) Wizards has used Ward almost everywhere Hexproof would have appeared. Reason: Hexproof is feels-bad for opponents (no removal works, ever) while Ward gates interaction behind a cost without forbidding it. Default to Ward for any "this shouldn't be easy to kill" effect. Reach for Hexproof only when the design specifically wants the strongest possible protection (almost never at common).

**How to apply:** When sketching a creature that needs durability, write Ward {N} or Ward — pay-cost. Reserve Hexproof for niche cases and document why.

### 2. Prowess fell off evergreen with Foundations (Nov 2024)

Prowess was an evergreen keyword for years; it's now deciduous. This shifts what "spell-matters at common" looks like — you can no longer assume Prowess will be background texture. If your set's pillars need spell-matters identity, choose Prowess intentionally and put it in 1–2 archetypes.

**How to apply:** Don't rely on Prowess being "always there." Either pick it as one of your set's deciduous mechanics, or design spell-matters payoffs that don't depend on it.

### 3. Tribal became Kindred in 2024

The card type "Tribal" was renamed "Kindred." This is largely cosmetic but affects card-text references and search. If your set has noncreature cards that need creature types (e.g., a Sorcery — Goblin), use the Kindred type.

**How to apply:** Use "Kindred [Type]" in card type lines for noncreature spells with creature types. Update any older card-text references that use "Tribal."

### 4. Predefined artifact tokens are now Magic's universal palette

Treasure, Food, Clue, Blood, Map, Powerstone — these are evergreen-or-near-evergreen tokens with stable text. Reusing them is cheaper than inventing a new "Coin" or "Gem" token because players already know the rules. Reserve novel token types for genuinely new mechanics.

**How to apply:** When you'd reach for "create a token that does X," check whether an existing predefined token already covers it. Treasure for ramp/fix. Food for life/sac fodder. Clue for card draw. Map for explore. Blood for loot. Powerstone for colorless ramp.

### 5. Recent design has burned through many "alt-cost from hand" variants

Plot (OTJ), Impending (DSK), and Suspend before them all answer "pay something now, get the spell later." If your vision wants this play pattern, lean into a *combinatorial* difference (different exile zone, different counter type, different reveal mechanic) — or pick a different design space entirely. Re-treading Plot or Suspend so soon will feel derivative.

**How to apply:** Before specifying a "pay now, cast later" mechanic, list how it differs from Plot, Impending, Suspend, Foretell, Adventure. If it's just "Suspend with a different counter," reconsider.

### 6. "Cast face-down 2/2" got a major upgrade with Disguise/Cloak

Morph existed for 20 years. MKM's Disguise/Cloak rebuilt it with built-in Ward {2}, which fixed Morph's classic Limited problem (cheap removal made face-downs feel terrible). If your set wants face-down play, default to the Disguise/Cloak template, not the original Morph template.

**How to apply:** When designing face-down creature mechanics, copy the Disguise/Cloak baseline (face-down 2/2, Ward {2}). Document why you'd deviate.

### 7. Recent state-of-design lessons from Rosewater (2025)

Three concrete lessons from the 2025 State of Design retrospective:

- **Recontextualize, don't replicate.** Duskmourn was criticized as "too on the nose" with horror references. Top-down sets should *reinterpret* their genre, not directly transcribe its tropes.
- **Downstream support matters.** Bloomburrow's Otter and Vehicle decks lacked follow-up support in later sets, frustrating players who built into them. If your vision will spawn a sub-archetype, plan for whether subsequent sets can reinforce it.
- **Three-color complexity is hard.** Tarkir: Dragonstorm fought constant tension between tight mana (causes color-screw) and loose mana (causes excessive splashing). Three-color sets need explicit mana-fixing strategy in the vision document.

**How to apply:** Add a "Recontextualization check" to top-down vision work, a "Downstream support assumed" note to any pillar that creates sub-archetypes, and a "Mana strategy" subsection to any vision that goes beyond two-color archetypes.

---

## Wisdom from the Color Pie reference

### 8. Treasure-in-blue is the canonical "blue ramp" mistake

When designing a mechanic that produces resources, blue is almost never the right home. Ixalan put Treasure tokens in blue and Rosewater publicly called it a mistake — blue does not ramp. Treasure is red and black. Mana acceleration in green. Blue's resource trick is *cost reduction*, not adding mana to your pool.

**Why:** Color pie identity is preserved by *what each color cannot do*, not just by what it can. Blue ramp erodes blue's "perfection through patience" identity by giving it the burst-mana feel of red/black.

**How to apply:** When sketching a new mechanic that produces mana or mana-equivalent resources, default to red/black/green homes. If the vision document needs blue to feel resource-rich, reach for cost reduction, scry/surveil density, or counter-spell tempo — not mana production.

### 9. Three-primary mechanics usually map to clans, not colors

If a new mechanic feels equally at home in three colors, it's probably a multicolor (clan/wedge) mechanic, not a mono-color one. Tarkir Dragonstorm 2025 uses this pattern explicitly: Endure for Abzan, Mobilize for Mardu, etc.

**Why:** A mechanic with no single primary doesn't constrain card design and dilutes color identity. Promoting it to a faction/clan mechanic gives it a structural home.

**How to apply:** When you find yourself writing a mechanic with three "P" entries, ask: should this be a clan mechanic instead? If yes, your set may be a wedge/clan set rather than a two-color-pair set, which is a major vision-level decision worth surfacing.

### 10. Bends are vision design's currency; breaks are debt

A bend is when a card stretches the color pie deliberately ("white draws cards, but only when a creature enters"). A break is when it violates the pie outright ("red destroys an enchantment"). Vision design can authorize bends — they're the texture that makes a set feel distinct. Vision design should never authorize breaks unless the entire set is built around the break.

**Why:** Bends produce flavor; breaks produce balance and review chaos downstream. The Council of Colors will catch breaks in review and force changes — it's cheaper to design within the pie at vision time.

**How to apply:** When a mechanic flirts with a break, document it in "What We Tried and Cut" with the specific reason. If the vision really does need the break (e.g., a set built around "red learns magic"), call it out in the handoff so Set Design and the Council aren't surprised.

---

## Wisdom from the Templating reference

### 11. Use current templating from the start

Two big templating shifts landed in 2024: "enters the battlefield" became "enters" (Bloomburrow), and self-reference moved from CARDNAME to zone-based ("this creature," "this spell," "this card") (Foundations). Vision-time prototype text written in pre-2024 template costs Set Design and the Editor real time to translate before they can evaluate the design.

**Why:** When prototype card text uses old templating, downstream readers spend cognitive cycles deciding "is this a deliberate quirk or just stale phrasing?" That noise hides genuine design issues.

**How to apply:** Always write `When this creature enters, ...` not `When CARDNAME enters the battlefield, ...`. Always use `this card` for graveyard/hand references. Always include "another" on ETB self-targeting (the Hostage Taker trap) and "you control" where you mean yours. Distinguish replacement effects (`if X would Y, instead Z`) from triggers (`whenever X, Z`) — confusing them is the most common templating bug in prototype text.

---

## Wisdom from the Rate and Cost reference

### 12. Common removal must punch above its old weight

In the Play Booster era (2024+), ~41% of packs contain two or more rares. That changes the answer math: if commons can't kill rare-level threats, the format devolves into "whoever opened more bombs wins." Rosewater confirmed common red burn now reaches 6 damage (up from the old 5-damage ceiling) precisely because of this pressure.

**Why:** Pre-Play-Booster, commons could safely under-cost their answers because rares were rare. Post-Play-Booster, the answer side has to keep pace with the threat side or Limited stops being skill-driven.

**How to apply:** When sketching common removal, default to slightly higher efficiency than pre-2024 norms. {1}{B} kill spells with light conditions are more acceptable now than they were in 2018. If common removal can't credibly answer your set's signature mythic threat, the format will feel rare-warped.

### 13. Mechanic as-fan at common is the teach-rate

A new named mechanic needs to *appear* often enough to teach itself in the first few games. Concrete target: 8–12 commons should feature a primary set mechanic (≥1.0 per pack as-fan), 4–8 commons for a secondary mechanic. Below 4 commons, the mechanic feels under-supported and players forget it exists.

**Why:** In Limited, the play experience comes from commons. A mechanic that only appears at uncommon and above is invisible to most drafters. Vision Design is responsible for ensuring the planned common count for each mechanic actually hits the as-fan target.

**How to apply:** When defining each mechanic in the handoff, write its planned `rarity_spread` with the common count first. Apply the formula: needed_commons ≈ (target_as_fan × 81 / 7), rounded up. For a primary mechanic targeting ~1.0 per pack, that's ~12 commons.

### 14. The vanilla curve is the floor for evaluating prototype cards

A creature's total stats should be roughly twice its mana value (2-cost = 4 stats; 3-cost = 6 stats; 4-cost = 7–8 stats). Every keyword, every ETB ability, every triggered ability comes off this baseline at roughly the cost of one stat.

**Why:** Without an internalized rate, prototype cards drift either too strong (every creature has bonus abilities at curve) or too weak (every creature is a vanilla and the set has no memorable cards). The curve is what makes "above curve = build-around" and "below curve = fair body" legible.

**How to apply:** When sketching a creature, write the vanilla version first ("a 3/3 for 3"), then add features one at a time, subtracting one stat per added keyword/ETB. If the result still looks above curve, push to higher rarity or add a real downside.

---

## Wisdom from the Modern Case Studies

### 15. Typal sets need cross-tribe pivots, not islands (Bloomburrow lesson)

The Lorwyn-vs-Ixalan distinction is now sharper post-Bloomburrow. Lorwyn made tribal *type-referential* (Changeling, "Elves you control"). Ixalan made tribal *subtype-locked* (Pirates didn't help Dinosaurs). Bloomburrow added a third rule: even with type-referential payoffs, drafters need *cross-tribal common cards* so they can pivot in mid-draft without losing early picks.

**Why:** Without pivots, the "what tribe am I?" question gets locked at pick 1. With pivots, it stays open through several picks, which is what makes draft feel like a game of reading signals.

**How to apply:** For a typal set, design at least 30–40% of commons to be *playable in two adjacent tribes*. A green creature usable in both Squirrels and Otters keeps draft flexible. If most of your commons fit only one tribe, the format is on rails.

### 16. When the genre's been done, differentiate by sub-genre (Duskmourn lesson)

Innistrad already did horror; Duskmourn did *modern* horror — different period, different references, different mood. The differentiation has to be specific enough that pillars can name what the set is *not*. "Horror set" is meaningless for a fourth horror set; "haunted-house slasher with atmospheric dread, not gothic literature" is a useful constraint.

**Why:** A pillar that doesn't differentiate is a generic pillar; it could fit any set in the genre. Specificity creates design space.

**How to apply:** When entering an occupied genre, write each pillar in a form that contrasts with the previous occupant. "This is horror, but unlike Innistrad..." → "the suspense is what you don't see, not the monster reveal." That contrast then drives mechanic choice (Manifest Dread, enchantments-for-mood) that wouldn't have been chosen otherwise.

### 17. Don't transcribe the genre — interpret it (Duskmourn lesson)

Top-down sets fail when they replicate genre tropes too literally. Duskmourn was criticized as "too on the nose" — cards felt like direct adaptations of horror-film moments rather than designs that *captured the feeling*.

**Why:** Direct replication makes the cards feel like fan service rather than design. Players appreciate the *feeling* of a horror movie more than they appreciate a card called "Chainsaw Guy."

**How to apply:** For each top-down card concept, ask: am I copying a specific scene, or am I capturing the *play pattern* that makes that scene work? "A creature you can't see clearly until it acts" (Manifest Dread) captures slasher dread better than "a card called The Stalker that costs {3}{B}."

### 18. UB mechanics must be IP-system translations, not re-skins (Final Fantasy lesson)

Final Fantasy's Job Select, Tiered, and Saga Creatures are inseparable from the IP — they couldn't exist outside FF. That's why the set worked. By contrast, early UB products that re-used existing Magic mechanics with new art felt hollow. The system-translation pattern is now the bar for major UB releases.

**Why:** Players who love an IP love its *systems* (the job system, the spell-tier system, the summon system). Translating those systems into card mechanics is what makes a UB set feel like the IP, not just look like it.

**How to apply:** For UB sets, list the IP's interactive systems first (in `ip_catalog.md`'s system translation inventory) and choose 2–3 of them as the basis for your primary mechanics. Reserve existing Magic mechanics as backups for less iconic systems.

### 19. When the IP is too big for one set, use precons for breadth (Final Fantasy lesson)

Final Fantasy contained sixteen separate franchise entries. Wizards solved the breadth problem by making the main set serve the *constellation* (no unified plane, characters from all entries) and making Commander precons serve *individual fan bases* (one precon per major entry, with that entry's iconic commanders).

**Why:** Forcing a 16-entry IP into one ~280-card set would have shortchanged every entry. Separating breadth (main set) from depth (precons) lets each product serve its audience.

**How to apply:** When the input IP is too big for one set, write a "product split" section in the vision handoff: what does the main set carry, and what gets pushed to Commander precons or supplementary products? This is technically `mtg-product-architect` territory, but vision design needs to flag the constraint.

---

## Wisdom for using canonical references

### 20. Check the Storm Scale before reusing an old mechanic

Mark Rosewater's Storm Scale rates every named mechanic from 1 (very likely to return) to 10 (very unlikely). A mechanic at Storm Scale 8+ has been judged unlikely to return for *reasons* — usually rules complexity, parasitism, or unfun play patterns. If your vision wants a returning mechanic, look up its Storm Scale rating before committing.

**Why:** A high-Storm-Scale mechanic has design baggage that's already been litigated. Bringing it back as your primary mechanic re-opens problems Wizards already decided weren't worth solving in the standard pipeline. Modern Horizons-style sets can take Storm-Scale-7 risks; standard-legal sets generally shouldn't.

**How to apply:** Before listing a returning mechanic in your handoff, look up its Storm Scale via the community-aggregated index (URL in `sources.md`) or Rosewater's per-set Storm Scale articles. If it's 7+, document why your set can carry the baggage; if it's 8+, strongly reconsider unless your set is explicitly a depth-over-accessibility product.

### 21. The Comprehensive Rules are the tiebreaker, not the daily reference

When in doubt about a rules edge case while writing prototype card text, defer to the live Comprehensive Rules at `magic.wizards.com/en/rules` (or the Yawgatog hyperlinked mirror). Don't memorize them; *know they exist* and check them when something feels rules-uncertain.

**Why:** Vision design isn't templating — but vision-time card text that violates a rules invariant (e.g., writing a triggered ability that should have been a replacement effect) creates downstream cost. Knowing the Comprehensive Rules exist as a tiebreaker prevents bad rules assumptions from getting baked into the handoff.

**How to apply:** When writing prototype card text that uses an unfamiliar rules pattern (a new zone, an unusual timing, a state-tracking requirement), check the relevant Comprehensive Rules section or use Yawgatog's keyword search before finalizing. If the templating reference (`templating.md`) doesn't cover it, escalate to the rules document.

---

## Sources

- Mark Rosewater's "Lessons Learned" columns (Parts 1-6+)
- Mark Rosewater's "State of Design" columns (2014-2025)
- Vision Design Handoff Documents: Bloomburrow (Parts 1-3), Kamigawa: Neon Dynasty (Parts 1-2), Wilds of Eldraine, Aetherdrift, Strixhaven, Original Zendikar, Duskmourn
- Per-set mechanics articles for MKM, OTJ, BLB, DSK, MH3, FDN, DFT, TDM, FIN (see `references/sources.md` for URLs)
- "Vision Design, Set Design, and Play Design" (Rosewater, 2017)
- Drive to Work podcast: Top-Down vs. Bottom-Up, Vision Design episodes
- Avacyn Restored and Born of the Gods design retrospectives
