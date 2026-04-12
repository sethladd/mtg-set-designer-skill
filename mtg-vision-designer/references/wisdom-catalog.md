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

## Sources

- Mark Rosewater's "Lessons Learned" columns (Parts 1-6+)
- Mark Rosewater's "State of Design" columns (2014-2024)
- Vision Design Handoff Documents: Bloomburrow (Parts 1-3), Kamigawa: Neon Dynasty (Parts 1-2), Wilds of Eldraine, Aetherdrift, Strixhaven, Original Zendikar
- "Vision Design, Set Design, and Play Design" (Rosewater, 2017)
- Drive to Work podcast: Top-Down vs. Bottom-Up, Vision Design episodes
- Avacyn Restored and Born of the Gods design retrospectives
