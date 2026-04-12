# Exploratory Design Wisdom Catalog

The exploratory designer's job looks simple — brainstorm mechanics, test them, rank them. The wisdom is in knowing which ideas to chase, which to kill, and which to hand off in a form that Vision Design can actually use. This catalog encodes the thinking patterns, traps, and hard-won insights that separate productive exploration from wandering.

---

## Exploration Failure Stories

### 1. Energy in Kaladesh — The Mechanic That Couldn't Be Balanced

Energy passed every exploratory evaluation with flying colors: deep (hundreds of possible energy costs and payoffs), resonant (everyone understands "charging up"), low parasitism (energy cards work alongside normal cards), backward compatible (doesn't interact negatively with existing mechanics). Exploratory Design greenlit it enthusiastically.

**What went wrong downstream:** Energy created a self-contained economy with no external interaction points. Ian Duke (Play Design lead) described it as a "knife's edge" parasitic balance problem — energy is either strong enough to dominate or too weak to play. Crucially, the lack of counterplay was a DELIBERATE design choice: Rosewater admitted they "were concerned that energy wasn't going to be played if it was too easily disrupted" and acknowledged "hindsight is 20/20." They chose not to print anti-energy cards, and the result was a resource opponents could not interact with at all — unlike life totals, cards in hand, or creatures on the battlefield. Energy earned a Storm Scale rating of 6 (unlikely to return without significant redesign).

**The lesson:** Add "counterplay surface" to your evaluation. Every mechanic needs at least one axis where opponents can interact with it. The energy lesson is doubly important: even when the design team KNOWS a mechanic lacks counterplay, the temptation to ship it anyway (because "it might be too weak otherwise") can override better judgment. If your mechanic creates a closed resource system, the burden of proof should be on proving it's safe WITHOUT counterplay, not on proving it needs counterplay.

### 2. Splice onto Arcane — Parasitism Hiding Behind Depth

Splice onto Arcane appeared deep: any Arcane spell could carry any splice effect, creating combinatorial possibilities. Exploratory evaluation would score it well on depth (many combinations), resonance (casting spells within spells is intuitive), and fun (building up big combo turns feels great).

**What went wrong downstream:** "Arcane" is a subtype that exists on exactly zero cards from any other set. Splice onto Arcane cards are literally unplayable without other Arcane cards in your deck. Rosewater uses Splice onto Arcane as THE canonical example of parasitic design: "a parasitic mechanic only works with a subset of cards from the set/block it's in. For example, splice onto arcane only worked with arcane and that only existed in Kamigawa block." He's also noted that Splice itself is not parasitic — "Splice onto Instant" could work. The Arcane restriction is what created the walled garden. Additionally, Rosewater has flagged that splice cards "require a lot of infrastructure, are hard to balance, and lead to repetition of play."

**The lesson:** Parasitism isn't just about whether a mechanic works in isolation — it's about whether the mechanic's ENABLERS exist outside the set. When your mechanic requires a specific enabler (card type, subtype, counter type), apply the Enabler Abundance Test: does that enabler already exist in abundance across Magic's history? Rosewater's own framework (from Design 103) distinguishes modular (flexible), linear (works best with specific cards), and parasitic (only works within the set). The critical insight: when parasitic design becomes tournament-relevant, players complain "You're building our decks for us."

### 3. Companions — The Dangerous Excitement of Breaking Rules

The Companion mechanic (Ikoria) must have felt electric during exploration. "What if your deck had a guaranteed card?" The design space is enormous — every possible deckbuilding restriction creates a different companion. It tested as fun (guaranteed access to a powerful card), deep (many possible restrictions), and novel (nothing like this existed).

**What went wrong downstream:** Breaking the fundamental rule that your opening hand is random turned out to be catastrophic for competitive play. Companion decks had "too high of win rates and metagame share in Standard, Pioneer, and Modern" and "already necessitated bans in Legacy and Vintage." The mechanic required unprecedented errata on June 1, 2020 — adding a 3-mana tax to move companion from sideboard to hand. Ian Duke wrote: "It's rare that we use a rules change to address metagame balance, and this isn't something we have plans to do in the future." Rosewater called companions "the biggest mistake of the set... the biggest mistake of the year." Vision design originally allowed MULTIPLE companions per game — playtesting cut this, but even one was too strong. Even after the errata, Lurrus was banned in Pioneer and Modern (March 2022) and Yorion was banned in Modern (October 2022). Aaron Forsythe said he would "love to go back in time and take another crack at getting them right."

**The lesson:** When a mechanic breaks a foundational game rule, the exploratory evaluation must include a "what if this is too good at ANY deckbuilding cost?" stress test. Part of the problem was that Ikoria also had Mutate — two high-maintenance mechanics in one set. Rosewater's takeaway: "Part of the job of design is not overtaxing play design, and I believe in Ikoria, that's what we did." Exploration should flag rule-breaks with a mandatory caution label AND limit the set to one such mechanic maximum.

### 4. Party (Zendikar Rising) — The Appealing Puzzle That Couldn't Compete

Party seemed deep: track how many of four creature types you control (Cleric, Rogue, Warrior, Wizard), get scaling bonuses for "full party." The design space appeared large — any effect could scale from 1-4 party members. It was even praised by some as potentially "the best tribal mechanic of all time" for Limited play.

**What went wrong downstream:** Party succeeded in Limited and casual play but failed entirely in Constructed. Rosewater acknowledged in his State of Design 2021: "Party didn't live up to its potential in Constructed." The problem was NOT that all party decks looked identical — it was that party decks couldn't viably exist in Standard at all. The payoffs weren't strong enough to justify the creature-heavy, type-specific deckbuilding constraints. Players wanted "more seeding pre- and post-Zendikar Rising of the four relevant class creature types" and individual cards "positioned to be more potent." The mechanic created an appealing deckbuilding puzzle with insufficient reward for solving it.

**The lesson:** During exploration, test whether a mechanic's payoffs justify its deckbuilding constraints at COMPETITIVE power levels, not just casual ones. A mechanic can feel wonderful in Limited (where you draft what's available) but collapse in Constructed (where every card must earn its slot against the entire card pool). If the mechanic requires you to play specific creature types, the payoff for assembling them must exceed what you'd get from just playing the best cards regardless of type.

### 5. Dungeons/Venture (Adventures in the Forgotten Realms) — External Component Trap

Venture into the Dungeon introduced external game pieces (dungeon cards) that sit outside the deck. Exploration likely saw this as resonant (D&D players know dungeons), deep (multiple dungeon paths with branching choices), and novel (first external progression tracker).

**What went wrong downstream:** Each dungeon room delivered approximately 1 to 1.5 mana value — far too weak for the comprehension cost. The mechanic was called "one of the most disappointing major mechanics ever" and "feels underbaked." Worse, the three-dungeon choice was described as "actually a false one" — players overwhelmingly chose Lost Mine of Phandelver for its immediate benefits, making the other two dungeons nearly obsolete. Rosewater himself rated dungeons "medium parasitic." The design team found that three dungeons was the right number (two felt too limited, more than three was too complex), but landed in an unsatisfying middle where the mechanic was too slow to be worth the rules overhead.

**The lesson:** When a mechanic introduces a new game system (external cards, counters with special rules, mini-games), the payoff must be proportional to the learning cost. If the mechanic's effects could be achieved with a simpler execution (just use ETB triggers), the new system is overhead without value. Additionally, when a mechanic offers choices (three dungeon paths), test whether the choices are REAL. If one option dominates, you have a false choice — complexity without depth.

---

## Counterintuitive Insights

### 1. The Best Exploration Rejects the Obvious

When given a theme like "underwater world," the obvious mechanical space is "sea creatures, swimming, water magic." But the best explorations push PAST the obvious to find the unexpected mechanical truth of the theme. Zendikar's "adventure world" became "landfall" — not because adventurers explore lands, but because the LAND ITSELF was the adventure. The mechanic came from asking "what's mechanically interesting about this theme?" not "what's thematically on-the-nose?"

**Why this matters:** Obvious mechanics tend to be shallow because they map 1:1 to flavor. Deep mechanics find an abstract mechanical principle UNDERNEATH the theme that generates hundreds of card designs. "Landfall" is infinitely deeper than "Explore" (Ixalan) because it taps into a fundamental game action (playing lands) rather than a specific flavor action.

### 2. Kill Your Favorites Early

The first mechanic that excites the team is rarely the best one. It's the one that's most obvious, most resonant, and most likely to be shallow. The exploratory phase must resist the urge to commit to the first exciting idea and instead explore PAST it to find what's hiding behind it.

**Evidence:** Rosewater has repeatedly noted that many of Magic's best mechanics were discovered mid-exploration after an initial favorite was killed. Morph (Onslaught) was not the first mechanic explored for a "secrets and deception" theme — it emerged after several face-down card experiments that each failed differently, teaching the team what worked.

### 3. Parasitic Mechanics Are Sometimes Worth It

The evaluation framework flags parasitism as a risk, and it is. But some of Magic's most beloved mechanics are parasitic: Tribal synergies (Elves, Goblins, Merfolk), energy, snow. The difference between good parasitism and bad parasitism is whether the parasitic cards are fun IN THE SET. If a mechanic creates a self-contained ecosystem that's thrilling to draft and play in Limited, it can succeed even if those cards are dead in other contexts.

**The rule of thumb:** Parasitism is acceptable if the set creates enough critical mass for the mechanic to function without external support. It's unacceptable if the set ALSO requires cards from other sets (Splice onto Arcane needed more Arcane spells than Kamigawa block provided).

### 4. Complexity Is Not Depth

A mechanic can be extremely complex (many rules, many interactions, many edge cases) without being deep (many meaningfully different cards). Banding is the canonical example: incredibly complex rules (how does banding work in combat? with trample? with first strike?) but almost no design depth (every banding creature is "this creature has banding"). Conversely, kicker is extremely simple (pay extra for a bonus) but infinitely deep (every possible bonus creates a new card).

**The diagnostic:** If explaining the mechanic takes 100 words but designing 50 different cards using it takes 10 minutes, it's deep. If explaining it takes 100 words but you run out of interesting designs after 10 cards, it's complex without depth.

### 5. The Exploration Document Is the Product, Not the Mechanics

Exploratory Design's output isn't "three good mechanics." It's a DOCUMENT that enables Vision Design to make informed decisions quickly. A brilliant mechanic described poorly is worth less than a good mechanic described thoroughly — with depth assessment, parasitism analysis, failure mode warnings, and backup options clearly laid out.

**Why this matters:** Vision Design has limited time. If they have to re-derive the reasoning behind each candidate, they'll waste weeks. If the exploration document anticipates their questions and answers them preemptively, Vision can move straight to selection and refinement.

---

## Common Exploration Traps

### Trap 1: Falling in Love With the Theme Instead of the Mechanics
The team gets so excited about the world concept ("steampunk plane! underwater civilization!") that they only explore mechanics that literally represent the theme. This produces flavorful but shallow mechanics. The fix: spend the first third of exploration on the theme, then spend the remaining two-thirds asking "what MECHANICAL space does this theme unlock?" regardless of flavor fit.

### Trap 2: Exploring Variations Instead of Alternatives
After finding one promising mechanic, the team explores 10 variations of it (kicker but with different costs, kicker but it triggers differently, kicker but it only works on creatures). This produces one mechanic with 10 skins, not 10 different candidates. The fix: each candidate in the shortlist must use a DIFFERENT mechanical axis. If two candidates are both "pay extra for a bonus," one of them needs to go.

### Trap 3: Ignoring the "Fun to Lose To" Test
Playtesting during exploration tends to focus on the player USING the mechanic. But half of every game is spent on the RECEIVING end. If the exploration doesn't test how it feels to play AGAINST the mechanic, it will miss anti-fun patterns that only emerge in adversarial play (energy's lack of counterplay, Annihilator's "lose everything" feel).

### Trap 4: Confusing Novelty With Quality
"We've never done this before!" is exciting but not evaluative. The fact that Magic hasn't done something doesn't mean it should. Sometimes the gap in design space exists because the space is bad (see: ante, manual dexterity, subgames). The fix: evaluate novel mechanics with the same rigor as familiar ones. Novelty is a bonus, not a pass.

### Trap 5: Under-Exploring the Backup Space
Teams tend to explore their top candidate deeply and their backup candidates shallowly. But Vision Design needs backup candidates that are GENUINELY viable alternatives, not afterthoughts. If the top candidate is killed during Vision (it happens), the backup must be ready to carry the set. The fix: the top 3 candidates should each get at minimum 30% of the exploration depth of the leader.

---

## Named Heuristics

### 1. The Counterplay Surface Test
Can opponents interact with this mechanic? If the mechanic creates a resource, can opponents destroy/drain/steal it? If it creates a board state, can opponents disrupt it? If the answer is "no, the mechanic operates in a closed system," flag it for counterplay design before advancing. Energy failed this test; Clue tokens pass it (opponents can destroy artifacts).

### 2. The Enabler Abundance Test
Does this mechanic require a specific enabler (card type, subtype, zone interaction) to function? If yes, does that enabler already exist in abundance across Magic's history? "Whenever you cast an instant or sorcery" passes (thousands exist). "Whenever you cast an Arcane spell" fails (only exists in Kamigawa block). The more the enabler depends on this specific set, the more parasitic the mechanic.

### 3. The Deckbuilding Decision Count
How many UNIQUE deckbuilding decisions does this mechanic create? If every card with the mechanic pushes toward the same 60-card deck, the count is 1 (regardless of how many cards carry the mechanic). If different cards with the mechanic pull toward different strategies, the count is higher. Target: a mechanic should create at least 3-4 distinct deckbuilding paths.

### 4. The Complexity-to-Payoff Ratio
Divide the words needed to explain the mechanic by the number of meaningfully different cards it can produce. High ratio (many words, few cards) = complexity trap. Low ratio (few words, many cards) = design gold. Kicker has the best ratio in Magic's history. Banding has one of the worst.

### 5. The Downstream Stress Test
Before finalizing the shortlist, ask: "What happens if Set Design makes this mechanic the centerpiece of Limited, and it doesn't work?" Each candidate should have a plausible rescue path — either it can be dialed down to a minor role, or the backup mechanics can absorb its slot. If killing a candidate would collapse the entire set, that candidate is too load-bearing for the exploration stage.

### 6. The Handoff Clarity Test
Read the exploration document as if you were Vision Design receiving it for the first time. For each candidate: Do you understand what it does in one sentence? Do you know its ceiling and floor? Do you know what to watch out for? Do you know why it was ranked where it is? If any answer is "no," the document isn't ready for handoff.

### 7. The Ten-Card Quick Design Test
For each candidate mechanic, design 10 cards using it in under 15 minutes. If you can't, the mechanic may lack depth. If the 10 cards all feel the same, the mechanic lacks variety. If 3 of the 10 are obviously broken, the mechanic has balance risks. This quick test reveals more about a mechanic's viability than hours of abstract discussion.

### 8. The Format Collision Check
Before finalizing candidates, check: is another set in the same Standard rotation using a similar mechanical space? Two landfall sets in the same Standard is redundant. A graveyard set alongside a delve set creates parasitic cross-set interactions. The exploration document should note any known format collisions.
