# MTG Skill Pipeline — Master Build Plan

## Philosophy

**The point of each skill is to be a bottle containing 30 years of someone's career wisdom.**

A skill that describes the *steps* of a job is a checklist. A skill that encodes the *wisdom* of a job is an expert. We are building experts, not checklists.

The difference:
- **Checklist**: "Define 10 two-color draft archetypes."
- **Expert**: "Define 10 two-color archetypes, but remember that Onslaught's mistake was making archetypes too insular — each tribe only worked with itself, so drafts were on rails. Innistrad fixed this by making archetypes overlap at the color level: blue's self-mill fed both UB zombies and UG flashback. Your archetypes must form a web where each color is coherent regardless of which partner it's paired with, and where drafters can pivot between adjacent archetypes without losing their early picks."

The second version contains a *lesson learned from failure*. That's what we're encoding.

### What "wisdom" means concretely

For each skill, the research phase must extract and encode these four categories:

1. **Failure stories** — What went wrong in real sets, and what principle was derived from the failure? (e.g., Energy in Kaladesh had no opponent interaction → lesson: every resource system needs a pressure valve)
2. **Counterintuitive insights** — What do experts know that beginners get wrong? (e.g., "Restrictions breed creativity" — having fewer mechanics to work with produces better individual card designs, not worse ones)
3. **Evolved thinking** — How has the role's approach changed over the decades, and *why* did the old approach fail? (e.g., the shift from Design/Development to Vision/Set/Play happened because the old handoff point was wrong — developers were redoing too much design work)
4. **Named heuristics and tests** — The specific mental tools experts use to evaluate their work (e.g., "the squint test" for visual design, "the parasitism test" for mechanics, "the fun to lose to test" for play patterns)

If the research phase for a skill doesn't produce at least **5 failure stories**, **3 counterintuitive insights**, **3 examples of evolved thinking**, and **5 named heuristics**, the research isn't done yet.

### The build process

For each skill:
1. **Research** — Deep-dive into primary sources (Making Magic articles, Drive to Work transcripts, GDC talks, handoff documents, Blogatog answers, "Lessons Learned" columns, "State of Design" retrospectives, banned-and-restricted announcements, designer interviews). **The goal is not to learn what the role does. The goal is to learn what the role has learned.**
2. **Distill** — Organize raw findings into the four wisdom categories above. Write each lesson as a concrete, actionable principle with its origin story (which set, which mistake, which designer).
3. **Embed** — Write these lessons directly into the skill's instructions as guardrails, warnings, and evaluation criteria — not as background reading, but as rules the skill must follow.
4. **Build** — Write the rest of the skill (inputs, outputs, process steps) around the embedded wisdom.
5. **Test** — Run the skill on 2-3 different set concepts. Evaluate whether the output *avoids* the known failure modes. If a set designed with this skill would have repeated Kaladesh's energy mistake or Ixalan's too-linear tribal, the wisdom isn't embedded deeply enough.
6. **Iterate** — Fix what's wrong, re-test.

---

## Build Order & Research Plans

---

### SKILL 1: `mtg-color-pie-reviewer`

**Why build first:** The color pie is the foundation everything else sits on. Every other skill needs to be able to check its work against color pie rules. Building this first gives us a validation tool we can use while building everything else. It's also the most self-contained — it has a clear canonical reference (the Mechanical Color Pie article) and a well-documented process (the Council of Colors).

**Research targets:**

| Source | What to extract |
|--------|----------------|
| "Mechanical Color Pie 2021" (Rosewater) | The canonical list: every ability, which colors get it at primary/secondary/tertiary |
| "Mechanical Color Pie 2021 Changes" | Every change from the 2017 version and *why* each change was made — **the reasoning behind each change IS the wisdom** |
| "The Council of Colors" (2016 article) | How the review process works: the 1-4 rating scale, what triggers a flag |
| "The Council of Colors, Revisited" (2024) | How the process evolved — **what they learned in 8 years of doing it wrong or right** |
| "Ari Nieh interview" (Card Kingdom blog) | A color councilor's perspective on what "break" vs. "bend" means in practice — **the gray area is where all the wisdom lives** |
| "Let's Talk Color Pie" (link collection article) | Master index of all color pie philosophy articles and podcasts |
| Blogatog color pie Q&As | Edge cases: the specific cards players ask about and Rosewater's rulings — **edge cases reveal the real principles** |
| Drive to Work episodes on individual colors | The philosophy behind *why* each color gets what it gets — **not the assignments, but the reasoning** |
| "Deciduous" and "Evergreen" keyword lists | Which abilities are always available vs. set-specific |
| Cards that were color pie breaks in shipped sets | **THE most important source**: which cards slipped through, why they were wrong, what damage they caused, and what process change resulted |
| "State of Design" discussions of color pie problems | Rosewater reflecting on where color pie enforcement failed in specific sets |
| History of color pie shifts (e.g., green getting card draw, red getting impulse draw) | **Why the pie changes**: what problem was being solved, what was gained, what was lost |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories**: Which shipped cards were color pie breaks? What damage did each one cause to the game? (e.g., Beast Within giving green unconditional permanent destruction — what was the fallout?) What process failures allowed them to ship?
- **The break/bend/exploration spectrum**: This isn't a binary. How do experienced councilors actually navigate the gray zone? What's the decision framework when a card *might* be a break? Find the specific mental model they use.
- **Why the pie moves**: The color pie isn't static — it evolves. Research every major shift (e.g., moving "haste" into green, giving white more card draw, creating "impulse draw" as red's card advantage). For each shift, find: what problem it solved, what resistance it faced, and whether it's considered a success in retrospect.
- **Rarity changes enforcement**: How does a common white removal spell differ in acceptable effects from a mythic white removal spell? Find the specific examples where rarity was the deciding factor in whether something was a break or not.
- **Multicolor philosophy**: A UB card can do things neither U nor B can do alone — but *which* things, and how far can it go? Find the framework for evaluating multicolor cards specifically.
- **The artifact/colorless loophole**: How do colorless cards relate to the pie? When is "any deck can play this" a feature vs. a bug? Find the historical mistakes here.
- **Set-specific bending**: When a set needs a color to do something slightly outside its slice (e.g., Innistrad giving green more self-mill than usual), what's the framework for acceptable bending vs. unacceptable breaking? Find the principles and the failures.
- **The trap effects**: What are the effects that designers *constantly* try to put in the wrong color? (Every generation of designers tries to give white direct damage or give red unconditional card draw.) Find the full list of these "attractive nuisances."

**Pre-known lessons to verify and deepen during research:**
- The difference between a **break** (should never happen), a **bend** (acceptable if the set needs it, with guard rails), and an **exploration** (intentionally pushing boundaries)
- How color pie enforcement changes by rarity (commons must be strict; mythics get more latitude)
- How multicolor cards change the rules
- The "sixth color" problem: how colorless/artifact cards interact with the pie
- How the pie bends for set-specific needs

**Deliverable:** A skill that can ingest any card file and produce a review report with per-card ratings, categorized flags, and recommended fixes. The skill must contain, as embedded reference material, the full mechanical color pie assignments AND the reasoning/wisdom behind those assignments — so that its reviews explain *why* something is a break, not just *that* it is one.

---

### SKILL 2: `mtg-exploratory-designer`

**Why build second:** This is the first step of the actual pipeline. We need it to generate the raw material that feeds Vision Design. It's also a good early skill because it's the most "brainstorming-shaped" — it needs to be expansive before the later skills get reductive.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| "Advanced Planning" (Rosewater, 2014) | How exploratory design was formalized; what it replaced; **what problems the old informal approach caused** |
| "Vision Design, Set Design, and Play Design" (2017 article) | The section on how exploratory design feeds into vision — **what happens when exploration is too shallow or too deep** |
| Drive to Work: "Exploratory Design" episodes | How the team actually works: meeting cadence, prototyping method |
| "Nuts & Bolts" series (Rosewater) | The annual design fundamentals series — especially #1 (card codes), #3 (filling in design skeleton) |
| Vision design handoff documents (all published) | **Read backwards**: what did Vision Design find most valuable from Exploratory? Where did they say "I wish we'd explored this more"? What got discarded? |
| "Ten Principles for Good Design" (Rosewater) | The foundational design principles that govern what's worth exploring |
| "Twenty Years, Twenty Lessons" (GDC 2016 talk) | Rosewater's distilled career lessons — **specifically the ones about knowing when to kill your darlings and when to trust your instincts** |
| "Restrictions Breed Creativity" (Rosewater) | The counterintuitive lesson about how constraints improve exploration |
| Theme-specific exploration articles | **How specific sets found their mechanical identity through exploration — and how others FAILED to**: e.g., how Innistrad found "graveyard matters," how Zendikar found "lands matter," but also how Battle for Zendikar lost the plot by not exploring what "lands matter" meant at a deeper level |
| "Lessons Learned" articles for sets with mechanical problems | **What happens when exploration fails**: sets where the wrong mechanic was chosen, or a good mechanic was explored too shallowly |
| "State of Design" mentions of mechanics that didn't work | Rosewater's retrospective on which mechanics failed and **what the exploration phase should have caught** |
| Individual mechanic deep-dives (energy, mutate, party, dungeons, etc.) | **The lifecycle of controversial mechanics**: what made them seem promising in exploration, what problems emerged later, what the exploration phase could have predicted |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories**: Which sets shipped with mechanics that should have been killed in exploration? What did the exploration phase miss? (e.g., Did exploration for Kamigawa: Neon Dynasty's "channel" foresee the play pattern problems? Did Ixalan's exploration phase know tribal would be too linear?) Find at least 5 specific examples.
- **The depth illusion**: What makes a mechanic *seem* deep during brainstorming but turn out to be shallow when you actually design 50 cards with it? Find the diagnostic signs that distinguish real depth from apparent depth.
- **The parasitism spectrum**: Energy, poison, and Dungeons are all parasitic to different degrees. What makes some parasitic mechanics succeed (poison in Phyrexia) and others stumble (energy in Kaladesh)? Find the actual framework — it's not binary.
- **When to kill a darling**: Exploratory teams fall in love with mechanics. How do experienced designers know when a beloved mechanic isn't working? What are the red flags? Find specific stories of mechanics that were killed and what the signal was.
- **The resonance shortcut**: Why did "flying" and "trample" and "lifelink" succeed instantly while "banding" and "phasing" confused everyone? Find the actual cognitive science behind mechanical resonance — what makes a mechanic intuitive.
- **Backwards from failure**: For every mechanic that was banned, restricted, or widely hated, trace it back to the exploration phase. What questions should have been asked? Build the "pre-mortem" checklist from real post-mortems.
- **The complexity trap**: How do exploration teams avoid the trap of designing mechanics that are fascinating to think about but miserable to play? (e.g., "the Ring tempts you" — conceptually rich, practically hard to track.) Find the distinction between interesting complexity and fun complexity.

**Pre-known lessons to verify and deepen:**
- Depth over breadth (50-card support vs. 10-card support)
- The parasitism test
- Backward compatibility
- The complexity budget (~3 new named mechanics at common)
- Resonance
- The "fun to lose to" test
- Linear vs. modular

**Deliverable:** A skill that takes a theme/world/concept and produces a ranked exploration of 8-15 mechanical directions with depth assessments, parasitism checks, and a recommended shortlist. The skill must evaluate each candidate mechanic against the full library of historical failures — effectively asking "is this mechanic going to have the same problem as X?"

---

### SKILL 3A: `mtg-worldbuilder` (for original Magic worlds)

**Why build third:** The worldbuilding track runs in parallel with Vision Design, but we need it before we build the Vision Designer skill because Vision Design references Creative's work constantly. **This skill is for original Magic worlds only.** For existing IPs (Universes Beyond), use Skill 3B (`mtg-ip-researcher`) instead — one or the other runs per set.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| "Worldbuilding Ikoria" (interview with Doug Beyer, Andrew Vallas, Jehan Choo) | How the creative lead coordinates worldbuilding with set design; **how visual identity feeds back into mechanics — and what happens when it doesn't** |
| "The Making of Kaladesh" (Magic Creative Team) | A full walkthrough of a concept push — **what surprised them, what didn't work, what they'd do differently** |
| "Theme-Driven Worldbuilding" (Doug Beyer, 2012) | The relationship between mechanical themes and world identity |
| Style guide excerpts (Ravnica, Zendikar, Innistrad — any publicly shared) | What a style guide actually contains; level of detail; visual vocabulary |
| "Nuts & Bolts #10: Creative Elements" (Rosewater, 2018) | How design and creative interact — **and where they historically clash** |
| Aaron Forsythe's Zendikar style guide reveal (Twitter, 2024) | Original style guide format and content |
| Vision design handoff documents (all) | **How worldbuilding elements are referenced by designers — what do they actually use vs. ignore?** |
| Cynthia Sheppard's "What does a Magic art director do?" | How the style guide gets translated into commissions — **what makes a style guide useful vs. decorative** |
| "Slime, Trials, and the Inner Garruk" (Adam Lee) | How characters are developed |
| Doug Beyer's "Savor the Flavor" / "A Voice for Vorthos" columns | Creative philosophy: how worlds are designed to be *felt*, not just seen |
| **"Lessons Learned" and "State of Design" for sets with worldbuilding praise vs. criticism** | **THE MOST IMPORTANT**: which worlds resonated (Innistrad, Ravnica, Eldraine) and which fell flat (Ixalan's first visit, Kaldheim's too-many-realms problem)? **Find the specific reasons — not "good world" but "here's why this world connected and that one didn't"** |
| Player reception data from Making Magic (market research mentions) | When Rosewater cites market research about what players loved/hated about a world — **these are the ground truth signals** |
| Comparison of first-visit vs. return-visit worlds | **What makes a world worth returning to?** Ravnica has been visited 4 times. Mercadia got one shot. Why? |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories**: Which Magic worlds fell flat creatively, and *why*? (e.g., Ixalan's first visit was criticized for shallow factions; Kaldheim tried to serve too many realms; Strixhaven's colleges felt more like Hogwarts houses than a Magic plane.) Find at least 5 specific worlds that underperformed creatively and extract the root cause.
- **The "world as argument" principle**: Doug Beyer and Rosewater both talk about worlds that make an argument. Innistrad argues "fear is a resource." Ravnica argues "civilization is guild-based governance." But what does it *actually mean* to build a world as an argument? Find the concrete methodology — how does Creative go from "this world is about X" to actual faction design, geography, and creature ecology?
- **When creative and mechanics diverge**: What happens when the world wants one thing and the mechanics want another? (e.g., Ikoria's strict creature-type-to-mutate mapping had to be loosened because it was preventing fun gameplay.) Find the decision framework for resolving creative-mechanical conflicts.
- **The faction trap**: Some sets have too many factions (Kaldheim's ten realms), some have the wrong factions (Ixalan's four tribes being too linear), some have the perfect number (Ravnica's ten guilds). What's the actual principle governing faction count and structure?
- **Visual identity that works**: Kaladesh's filigree, Innistrad's gothic architecture, Zendikar's hedrons — these are visual through-lines that make a world instantly recognizable. But other sets lack this. What makes a visual identity stick? Find the properties of successful visual through-lines.
- **Creature type ecology**: The mapping from creature types to colors to archetypes is where worldbuilding and gameplay intersect most directly. Bloomburrow's ten animals, Lorwyn's eight tribes, Innistrad's five monster types — each solved this problem differently. What's the actual design space, and what are the failure modes?
- **The character density question**: How many named characters does a set need? Too few and the world feels empty; too many and it feels crowded with legends that don't matter. Find the actual sweet spot and the reasoning behind it.
- **What makes a world replayable**: Some planes are evergreen (Ravnica, Innistrad, Dominaria). Others are one-and-done. What creative properties make a world worth returning to?

**Pre-known lessons to verify and deepen:**
- Worlds must be arguments
- The faction matrix (factions → color pairs → archetypes)
- Visual through-lines
- Creature type ecology serving both flavor and mechanics
- Top-down touchstones for resonance-driven sets
- The gray zones between factions
- Character density

**Deliverable:** A skill that takes mechanical themes and a concept and produces a world guide with factions, races, geography, key characters, creature type matrix, visual identity notes, and tone guide — all explicitly mapped to mechanical archetypes. The skill must encode the wisdom of *why* certain worlds succeeded and others didn't, using that wisdom as guardrails during generation.

---

### SKILL 3B: `mtg-ip-researcher` (for Universes Beyond)

**Why build third (parallel track):** About half of modern Magic sets are Universes Beyond adaptations (Lord of the Rings, Final Fantasy, Doctor Who, Fallout, Warhammer 40,000, etc.). These sets don't need worldbuilding — the world already exists. They need *exhaustive IP research and cataloging*, which is a fundamentally different skill. Without this, our pipeline can only produce in-universe Magic sets, which misses half the real-world output.

**This skill is mutually exclusive with Skill 3A.** For any given set, either `mtg-worldbuilder` runs (if the user wants an original world) or `mtg-ip-researcher` runs (if the user names an existing IP). Both produce downstream artifacts that feed the same Vision Design skill — but with different constraints.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| "Designing for Universes Beyond" (Rosewater, 2022) | **THE foundational article.** Rosewater lays out the advantages (resonance, new vantage points) and challenges (color pie mismatch, reprint constraints, earlier art commitment, locked flavor) of UB design. Every challenge is a constraint the IP researcher must surface. |
| "Magic's Voyages to Universes Beyond" (WotC, 2021) | The original announcement — understand the stated intent and how it has evolved |
| Lord of the Rings: Tales of Middle-earth design articles | **THE most detailed case study**: how did the design team identify which characters, factions, and moments to prioritize? What did they cut and why? |
| Final Fantasy set design articles (2024-2025) | The first Standard-legal UB set, spanning 16 games — **a huge cataloging challenge.** How did they handle that breadth? How did they decide which games got more representation? |
| Warhammer 40,000 Commander deck design articles (Ethan Fleischer-led) | **The color pie imbalance problem in action.** Warhammer 40K has more natural black and less natural green than Magic expects. How did the team handle this? |
| Doctor Who Commander deck design articles | The time-travel theming challenge — **how does a catalog handle an IP where chronology is non-linear?** |
| Fallout Commander deck design articles | A post-apocalyptic IP — **how does the team pick from a fragmented, franchise-wide catalog rather than a single tight story?** |
| Assassin's Creed design articles | A game franchise with many historical settings — **how do you catalog an IP that spans many time periods?** |
| Transformers insert cards in Brothers' War | The first "skinned inside a regular set" approach — **what didn't work about this, and why did WotC move to separated UB products afterward?** |
| "Universes Within" re-skins | **How WotC handles the inverse problem** — translating an IP-specific card into an in-universe Magic equivalent. Reveals what they consider "essentially the same" vs. "unique to the IP." |
| Commander precon lists for every UB product | **What made it into each product?** The final selection is the distilled output of the research/cataloging process. Compare against the source IP to see what got included vs. cut. |
| Interviews with Ethan Fleischer, Annie Sardelis, and other UB design leads | Design leads often discuss their process on podcasts and in interviews — **the actual workflow, not just the output** |
| Fan critiques of UB sets | **Where did the cataloging fail?** Which beloved characters got omitted? Which flavor decisions angered fans? Which color assignments were contested? Every fan complaint is a signal about what the research missed. |
| The existing `universes-beyond-patterns.md` in `mtg-set-designer` | The current skill's UB reference material — what's already been captured, what needs more depth |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — UB sets that missed the mark**: Spider-Man was considered a "dud" by many fans. Transformers inside Brothers' War was criticized enough that WotC changed its insert approach. Ninja Turtles had mixed reception. For each underperforming UB set, find the root cause: Was the IP a bad fit for Magic? Was the research incomplete? Were the color assignments contested? Were the iconic moments missed? Build the taxonomy of UB failure modes.
- **The "must-include" problem — identifying sacred cows**: Every IP has characters, moments, items, and locations that the fanbase *demands* be included. Miss one and you get a riot. But you can only fit so many cards. How do experienced UB designers identify the must-includes vs. the nice-to-haves? Find the methodology — it's not just "most popular." There are story-critical characters, fan-favorite minor characters, iconic objects, and "the obvious ones everyone expects."
- **Color pie mismatches — the hard cases**: Rosewater explicitly called out that Warhammer 40K skewed black and away from green. LotR has more whites and greens than blues and reds. Final Fantasy has wildly uneven color distribution across its 16 games. For each published UB set, find the color imbalance and how the team compensated (did they stretch characters into unusual colors? Did they accept uneven distribution? Did they invent new characters to fill gaps?).
- **The iconic ability problem**: Gandalf must feel like Gandalf. Cloud must feel like Cloud. But iconic abilities can conflict with game balance. How do UB designers navigate "this character is known for X, but X would be broken/weak as a Magic ability"? Find the specific examples and the decision framework.
- **Character density vs. variety**: Many IPs have a tight central cast and a loose extended universe. How many characters should come from the core cast vs. the extended universe? Spider-Man got criticized for having "five versions of Peter Parker" — what's the framework for avoiding that?
- **Reprint-as-adaptation**: Some existing Magic cards get reprinted in UB sets with the names/art changed to fit the IP. This only works if the mechanical effect makes sense in the IP context. What makes a good reprint candidate? What's the failure mode (reprints that feel forced)? Find examples of successful and failed reprints.
- **Naming convention extraction**: Each IP has its own naming patterns — Tolkien's languages, Final Fantasy's naming quirks, Warhammer's gothic Latin. The catalog must capture these so the downstream `mtg-creative-writer` can follow them. How do experienced UB teams codify an IP's naming conventions?
- **The "adaptation bandwidth" problem**: A full UB set has ~261 cards. How many of those should be character cards vs. spells/locations/events? Different IPs have different natural balances. Find the distribution choices and their justifications.
- **Scope decisions — which games/books/seasons to include**: Final Fantasy spans 16 mainline games plus spinoffs. Doctor Who spans 60+ years and many doctors. Fallout spans multiple games. How does the research team decide what's in scope? Find the criteria — it's not just "all of it."
- **What the fanbase will tolerate being changed**: Every adaptation requires some changes. Some are accepted (power level tweaks, minor visual changes). Others cause backlash (changing a character's color alignment, omitting a beloved figure, changing a signature ability). Find the line between acceptable and unacceptable change.
- **Earlier art commitment**: Rosewater noted that UB sets commit to art earlier because characters must be shown correctly. This locks in flavor before mechanics are finalized, which constrains Set Design. The IP Researcher must produce a catalog *decisive* enough to support early art commissioning. How is that decisiveness achieved?

**Pre-known principles to verify and deepen:**
- IP research, not invention: the job is to catalog what exists, not create
- Color pie mismatch is almost guaranteed — surface it early
- "Must-include" characters/items/locations drive the catalog priority
- Naming conventions and IP-specific terminology must be extracted
- Iconic abilities drive flavor more than they drive mechanics
- Earlier art commitment means the catalog must be decisive
- Candidate reprints should be identified during research, not during Set Design
- Locked flavor reduces Set Design's flexibility — surface the locked elements explicitly

**Process this skill must follow:**

1. **Scope definition**: Ask the user which parts of the IP to include (e.g., "Final Fantasy VII only" vs. "all 16 mainline games"; "original LotR trilogy" vs. "including The Hobbit and Silmarillion"). Establish the corpus.
2. **Deep research via web search**: Canonical sources (official wikis, author/creator statements, publisher guides), reputable fan references (large fan wikis, established encyclopedias), fan consensus discussions (for "must-include" identification). Use at least 10-15 searches to build adequate coverage.
3. **Character catalog**: Major characters, minor but iconic characters, antagonists, supporting cast. For each: name, role in IP, proposed MTG color(s) with reasoning, iconic abilities, visual description, story importance.
4. **Faction catalog**: Organizations, races, species, political groups. For each: description, color alignment, key members, mechanical archetype potential.
5. **Location catalog**: Iconic places that could become lands or appear in art. For each: description, associated characters, visual identity, land-type suggestion.
6. **Item catalog**: Weapons, artifacts, technology, magical objects that could become equipment, artifacts, or enchantments. For each: description, owner/origin, mechanical effect suggestion.
7. **Story beats catalog**: Iconic moments that could become sorceries, instants, or define the set's narrative arc. For each: description, participants, emotional weight.
8. **Color pie analysis**: Map every catalog entry to the WUBRG pie. Compute the distribution. **Flag imbalances prominently** so Vision Design can plan compensation.
9. **Must-include list**: From the catalog, identify the 30-50 sacred cows that MUST appear in the final set. Mark these prominently.
10. **Naming and terminology extraction**: Document the IP's naming conventions, signature terminology, and language/linguistic patterns for downstream use by Creative Writer and Art Director.
11. **Candidate reprint list**: Identify existing Magic cards whose names and effects would translate meaningfully into the IP context.
12. **Constraint document**: Produce a companion `ip_constraints.md` that explicitly tells Vision Design: here's what you CAN'T do (due to locked flavor), here's what you MUST include (sacred cows), here's where the color pie is lopsided (and by how much).

**Deliverable:** A skill that takes the name of an existing IP and produces `ip_catalog.md` (functionally equivalent to `world_guide.md` but research-derived) and `ip_constraints.md` (the hard limits imposed by the IP on downstream design). The skill must encode the hard-won wisdom of Universes Beyond design: which adaptation approaches work, which fail, and how to navigate the constraints that original Magic sets don't face.

---

### SKILL 4: `mtg-vision-designer`

**Why build fourth:** Now we have the exploratory output and worldbuilding to feed into Vision Design. This is the most creatively important skill — where sets get their identity.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| ALL published vision design handoff documents (~20+) | **THE most important source. These ARE the output of Vision Design.** Don't just read them — compare them. What do the great handoffs have that the weaker ones lack? How do different leads (Rosewater vs. Mooney vs. Beyer vs. Nieh) approach the same structural problems differently? Which handoff predictions were right vs. wrong about what Set Design would keep? |
| "Nuts & Bolts" #1-12 (the full annual series) | The complete design fundamentals: card codes, design skeletons, rarity distribution, creature-to-spell ratios, color balance |
| "Lessons Learned" series (Rosewater) — **every single one** | **THE WISDOM MOTHERLODE.** Post-mortem on every set: what vision design got right and wrong. These columns are Rosewater admitting his mistakes with 20/20 hindsight. Every lesson here is a guardrail for the skill. |
| "State of Design" columns (2005-2024) — **every single one** | Annual review: which sets succeeded, which failed, and why — **always traced back to vision decisions.** Cross-reference with Lessons Learned for the complete picture. |
| Drive to Work: "Vision Design" episodes | Rosewater's process for leading vision design — the daily and weekly rhythm |
| "Head-to-Head" design philosophy episodes | **When two design principles conflict, which wins?** These are the tiebreaker rules. |
| The "Three Pillar" framework across multiple sets | How pillars are chosen — **but more importantly, which pillar choices led to unfocused sets and which led to beloved ones** |
| "Vision Summit" references in handoff documents | **The feedback loop**: Vision Design presents to the broader R&D group mid-process. What kind of feedback changes direction? What gets pushed back on? |
| Handoff documents where Rosewater's annotations say "this didn't survive Set Design" | **The gap between vision and execution**: what kinds of ideas sound great in vision but don't survive contact with the realities of card design? |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — the sets that lost their identity**: Which sets arrived on shelves feeling unfocused or confused? (e.g., Battle for Zendikar losing the "adventure world" identity; Ixalan feeling too linear; Born of the Gods feeling like a filler set.) For each, trace the problem back to vision design: was the vision unclear? Was it clear but wrong? Was it clear and right but Set Design couldn't execute it? These are three fundamentally different failure modes.
- **The pillar paradox**: The three pillars are supposed to focus the set, but Rosewater has written about sets where the pillars were individually good but didn't cohere (pulling the set in three different directions instead of one unified direction). Find the examples and the diagnostic: how do you tell whether your pillars are *reinforcing* or *competing*?
- **The mechanic graveyard**: Every handoff document mentions mechanics that were tried and cut. These dead mechanics are incredibly valuable — they represent paths the experts explored and rejected. Build a taxonomy of *why* mechanics get cut: too complex, too parasitic, too similar to another mechanic, doesn't serve the set's theme, rules problems, play pattern problems, etc.
- **Overdelivery vs. overwhelming**: Vision Design is supposed to hand off *more* than Set Design needs. But how much more? Find examples where overdelivery was helpful (Set Design had options) vs. harmful (Set Design was overwhelmed and couldn't see the forest for the trees).
- **The archetype web — successes and failures**: The 10 two-color archetypes need to form a web where colors are coherent and drafters can pivot. Bloomburrow and Innistrad nailed this. Onslaught and original Ixalan didn't. Find the specific structural differences. What makes an archetype web flexible vs. rigid?
- **When to go top-down vs. bottom-up**: Rosewater has written extensively about this choice, but the real wisdom is in the *mismatches* — sets where the wrong orientation was chosen. Was there ever a set that should have been top-down but was built bottom-up, or vice versa? Find the diagnostic criteria.
- **The New World Order tightrope**: Commons must be simple, but they also must be interesting enough to make Limited fun. How do great vision designers navigate this tension? Find the specific tricks (French vanilla creatures, enters-the-battlefield triggers, simple modal choices) and the specific failures (commons that were too complex or too boring).
- **The handoff document as communication tool**: Some handoff documents are better than others at communicating the vision. What makes a handoff document *effective* — not just complete, but persuasive to the Set Design team that receives it?
- **Backup mechanic strategy**: How many backups, how different should they be from the primary mechanics, and how developed should they be? Find examples where backup mechanics saved a set and examples where the lack of backups caused problems.

**Pre-known lessons to verify and deepen:**
- The Three Pillars rule
- Mechanics must serve the set
- The archetype web
- Signpost uncommons
- As-fan management
- The "What's the set about?" test
- Backup mechanics
- New World Order
- Overdelivery

**Deliverable:** A skill that takes exploration results plus **either** a `world_guide.md` (original Magic worlds) **or** an `ip_catalog.md + ip_constraints.md` pair (Universes Beyond sets) and produces a vision design handoff document + draftable card file with all commons/uncommons and enough rares/mythics to draft. The skill must contain the distilled wisdom of every "Lessons Learned" column — functioning as a vision designer who has internalized 20 years of post-mortems.

**Special handling for Universes Beyond input:** When consuming `ip_catalog.md + ip_constraints.md`, the Vision Designer must treat the constraints as non-negotiable (must-include characters are fixed, color pie imbalances must be compensated for rather than "fixed," locked flavor elements cannot be redesigned). Research the specific ways WotC's Vision Design adapted to UB constraints for LotR, Final Fantasy, and Warhammer 40K — the wisdom here is distinct from original-set vision design.

---

### SKILL 5: `mtg-set-designer` (refactor existing)

**Why build fifth:** Now we have the vision handoff to feed into Set Design. This refactors the existing monolithic skill into a focused Set Design phase.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| Sam Stoddard's "Latest Developments" columns (2013-2017) | **The developer's perspective on what happens when vision's ideas meet reality** — specifically, what kinds of vision ideas consistently break when you try to build 261 real cards from them |
| Erik Lauer's design philosophy (via Rosewater's articles and Drive to Work) | The architect of modern Set Design: his principles on curve management, format speed, removal density — **and the specific problems he was solving when he invented the modern handoff system** |
| "Playtesting Constructed" (Sam Stoddard, 2014) | How Set Design tests for Constructed impact |
| Corey Bowen's DigiPen interview | A modern set design lead's perspective — **especially on managing 200+ card designs simultaneously and knowing when to ask for help vs. trust your own judgment** |
| Drive to Work: "Card Design" episodes | Individual card design principles — **the art of designing a common vs. uncommon vs. rare, and why getting this wrong ruins the Limited format** |
| "Making Magic" articles tagged "development" or "set design" | How mechanics get refined, cards get recosted, and archetypes get rebalanced |
| Play Booster era skeleton data | The exact numbers: how many creatures per color at common, how many removal spells, the modern Limited skeleton |
| Format speed analysis articles | How to calibrate whether a format is too fast, too slow, or just right |
| "How We Design Commons" (various) | The most constrained part of design: what makes a common good |
| BREAD analysis and its modern successors | How Limited players evaluate cards and how designers can use that knowledge |
| **"Lessons Learned" for sets with Limited format problems** | **THE KEY SOURCE**: which Limited formats were praised (Dominaria, Eldraine, MH2) and which were criticized (Born of the Gods, Avacyn Restored, Battle for Zendikar)? **For each, find the specific Set Design decisions that made the difference.** |
| **Banned card autopsies** | For every card banned from a Constructed format: what was the Set Design team trying to accomplish, where did the numbers go wrong, and what should the costing have been? |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — the broken Limited formats**: Which formats had unplayable archetypes, and *why*? (e.g., Avacyn Restored's "loner" mechanic killed aggro; BFZ's format was too slow and too bomb-dependent.) For each broken format, find the specific skeleton/curve/removal decisions that caused it. These become the validation checks in the skill.
- **The skeleton as diagnostic tool**: Experienced set designers can look at a design skeleton and predict whether the format will be fast or slow, whether aggro will exist, whether bombs will dominate. What are the specific numbers they check? (e.g., "If there are fewer than 3 common 2-power 2-drops per color, aggro is dead.") Find these diagnostic heuristics.
- **The removal calibration problem**: Too much removal → board-stall format where nothing sticks. Too little removal → bomb-dominated format where the rare you open determines the game. Every set designer has to calibrate this. Find the specific removal density targets and the sets that got it wrong in each direction.
- **The curve gap trap**: A missing common 2-drop in a color can destroy that color's viability in Limited. A missing common 5-drop means the color has no late game. Find the specific examples of curve gaps that ruined archetypes, and build the diagnostic checklist.
- **As-fan math — the real numbers**: "As-fan" (the average number of cards with a given property in a booster pack) is the single most important number for whether a theme feels present. What are the actual target numbers used at WotC? (Rosewater has mentioned specific targets in handoff documents.) Find them and catalog them.
- **The build-around trap**: Build-around uncommons are the soul of Limited, but they can also be traps if the payoff doesn't justify the setup. How do experienced designers calibrate build-around power? Find the specific framework: what rate should a build-around achieve when its condition is met vs. not met?
- **When to deviate from the vision**: Set Design sometimes cuts a mechanic that Vision Design loved. What's the framework for knowing when a mechanic is "not working" vs. "needs more time"? Find the specific stories of mechanics that were cut during Set Design and the reasoning.
- **The Constructed seed problem**: Set Design must plant cards that will matter in Standard, Pioneer, Modern, and Commander — without warping Limited. How do they balance this dual mandate? Find the specific techniques (pushed rares that are bad in Limited but great in Constructed, etc.).
- **Format speed as a deliberate choice**: The speed of a Limited format is not an accident — it's a design choice made through specific levers (2-drop quality, removal cost, average toughness). Find the lever settings for fast formats (Zendikar) vs. slow formats (Dominaria) vs. medium formats (Eldraine).

**Pre-known lessons to verify and deepen:**
- The skeleton is everything
- Creature-to-spell ratio by color
- The removal suite per color
- Curve is king
- As-fan is destiny
- Signpost cards teach
- Build-arounds at uncommon
- Format speed levers

**Deliverable:** A refactored skill that takes a vision handoff + card file (plus the creative reference — either `world_guide.md` or `ip_catalog.md + ip_constraints.md`) and produces a complete, balanced set through iterative card design, skeleton filling, curve management, and mechanical tuning. The skill must contain the embedded wisdom of every broken Limited format — effectively checking its own work against a catalog of "here's how past set designers got this wrong."

**Special handling for Universes Beyond input:** Set Design for UB sets has additional constraints: the must-include character list from `ip_constraints.md` is non-negotiable (those cards must exist in the final set regardless of format considerations), and power-level decisions for iconic characters may be driven by fan expectation rather than pure balance. Research how real UB set designers (particularly for LotR and Final Fantasy) navigated the tension between "this card must feel like X" and "this card must work in Limited."

---

### SKILL 6: `mtg-play-designer`

**Why build sixth:** With the set designed, we need to validate it. Play Design is the quality gate.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| Melissa DeTora's "Play Design" columns (2017-2019) | How Play Design was structured, what they test for, how they think about balance |
| Tom Ross's "From Player to Play Designer" (2017) | **The transition from competitive player to play designer — what intuitions transfer and which are wrong** |
| Dan Burdick's "On the Shoulders of Giants" (2017) | The founding of Play Design and its mandate — **why the team was created, what problems it was solving that development alone couldn't** |
| Play Design stream archives (2018-2019) | Live examples of play designers evaluating cards |
| Melissa DeTora on Casual Play Design (2021 Twitter/Discord) | **How Commander balance differs from competitive balance — a completely different mental model** |
| **Banned and Restricted announcements (ALL of them)** | **THE MOST IMPORTANT SOURCE FOR THIS SKILL.** Every ban is a Play Design failure story. For each ban: what was the card supposed to do, why was it too strong, what did Play Design miss, and what systemic problem does it reveal? Build the complete taxonomy of Play Design misses. |
| "State of Design" ban discussions | Rosewater's analysis of why certain cards escaped Play Design — **the meta-failures, not just individual card failures** |
| Format health articles by various R&D members | What "healthy" means for Standard, Draft, Commander |
| Andrew Brown / Dave Finseth B&R announcements (2024) | **Modern Play Design communication — how they explain what went wrong, which reveals what they're looking for** |
| Drive to Work: "Play Design" episodes | How the team structures its 3-month testing window |
| **The Oko / Hogaak / Uro / Omnath ban stories specifically** | **The most spectacular Play Design failures of the modern era.** Each one teaches a different lesson about what the testing process can miss. |
| **Energy mechanic retrospective** | Energy in Kaladesh had no opponent interaction — **a systemic design flaw that Play Design should have caught. Find out why they didn't.** |
| **Companion mechanic retrospective** | Companion was the biggest power-level miss in modern history. **What went wrong in testing?** |

**Wisdom to discover (research must find answers to all of these):**

- **The complete ban taxonomy**: Categorize every major ban by *root cause*. Some bans are simple mana-cost mistakes (card is 1 mana too cheap). Some are systemic (energy has no interaction). Some are combo-based (two cards interact in an unforeseen way). Some are metagame-based (card is fine in a vacuum but dominates with existing shell). Some are play-pattern-based (card is balanced by win rate but miserable to play against). Build the full taxonomy so the skill can check for each category.
- **The "why did testing miss this?" meta-analysis**: Play Design tests extensively, yet still misses things. Why? Find the systemic reasons: testing with incomplete card pools, testing in a metagame that doesn't match the real one, not testing enough Commander, underestimating synergies with older cards. Each systemic reason becomes a check in the skill.
- **The fun-vs-power distinction**: Some cards are banned not because they win too much, but because they make the game miserable (e.g., Nexus of Fate's infinite turns). How do play designers evaluate "fun to play against" separately from "balanced by win rate"? Find the specific framework.
- **Commander scaling problems**: Cards that say "each opponent" are 3x as powerful in Commander. "Target opponent" doesn't have this problem. "You gain life" scales with more opponents. These scaling effects are the #1 source of Commander problems. Build the complete list of effects that scale dangerously in multiplayer.
- **The rate baseline database**: For the skill to flag power-level outliers, it needs to know what "normal" looks like. For every major card category (2-mana creatures, 3-mana removal, 4-mana sweepers, etc.), find the historical baseline rate. What stats does a "fair" 2-mana creature get? What damage does a "fair" 3-mana removal spell do?
- **The two-card combo problem**: The most common Play Design miss is two-card infinite combos with cards from different sets. What's the actual methodology for checking this? It's combinatorially explosive — how do they prioritize what to check? Find the heuristics.
- **Limited format health diagnostics**: What specific metrics indicate a healthy vs. unhealthy Limited format? Win-rate spread across archetypes? Game length distribution? Bomb win-rate delta? Color pair drafting frequency? Find the actual metrics Play Design uses.
- **The Constructed push dilemma**: Play Design needs to make exciting cards that see Constructed play, but every pushed card is a ban risk. How do they balance this? Find the specific philosophy and the cases where they got it wrong in both directions (too conservative → boring format; too aggressive → ban).

**Pre-known lessons to verify and deepen:**
- The four format quadrants (aggro, midrange, control, synergy)
- Archetype win-rate bands (45-55%)
- The "best deck" test
- Removal must answer threats
- Mana efficiency curves
- The combo check
- Constructed rate baselines
- Commander considerations

**Deliverable:** A skill that takes a complete card file and runs balance analysis: simulated Limited win rates, rate comparisons against historical baselines, combo checking, and format health assessment. The skill must embed the *complete ban taxonomy* — every category of Play Design failure, derived from real bans — and check for each one.

---

### SKILL 7: `mtg-editor`

**Why build seventh:** Templating is the layer that makes cards *actually work as Magic cards*. It's highly rule-based and transformative for output quality.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| Magic Comprehensive Rules (current) | The authoritative source for how cards must be worded |
| "Dominaria Frame, Template, and Rules Changes" (Aaron Forsythe, 2018) | **The most significant recent templating overhaul — and WHY each change was made. The "why" is the wisdom.** |
| Oracle text database (Scryfall) | The canonical wording of every existing Magic card — the reference for how any effect should be templated |
| "Large Templating Change: Reducing Card Name Usage" (2025 rules blog) | **The most recent major change: understand the years-long debate that led to it, not just the result** |
| "The Name of the Rule" blog | Ongoing analysis of templating changes and their implications |
| History of templating changes (GitHub gist by fenhl) | Comprehensive history of every templating convention change |
| Del Laugel / editing team articles and mentions | How the editing team operates: what they check, common mistakes, their approval process |
| Jess Dunks (rules manager) mentions in handoff documents | **How the rules manager catches problems designers didn't see — the gap between "sounds right" and "works in the rules"** |
| Reminder text conventions across recent sets | When to include reminder text, how to word it, font size considerations |
| Text box fitting guidelines | Maximum rules text length, font size minimums, how text+flavor must fit |
| **Cards with errata / Oracle text corrections** | **Every erratum is a templating failure story.** Find cards where the printed text didn't match the intended rules behavior. What caused the gap? |
| **Comprehension-complexity research** | Rosewater talks about "comprehension complexity" vs. "board complexity" vs. "strategic complexity." Find how this taxonomy applies to rules text — **when does a card's text confuse players, and what templating fixes reduce confusion?** |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — errata archaeology**: Which cards needed errata because the rules text was ambiguous or wrong? (e.g., the Hostage Taker infinite-loop errata.) For each, what was the templating mistake, and what principle prevents it? Build a checklist of ambiguity patterns.
- **The templating evolution and its reasons**: Why did "enters the battlefield" become "enters"? Why did card-name self-reference become "this creature"? Each change had years of discussion behind it. **Find the actual arguments — what problem was each change solving? What player confusion or rules-corner-case was it addressing?**
- **The readability-precision tradeoff**: Perfect rules precision sometimes makes cards unreadable. Perfect readability sometimes creates rules ambiguity. How do editors navigate this tradeoff? Find the specific decision framework and the cases where they got it wrong in each direction.
- **The text box fitting crisis**: What happens when a card's rules text is too long to fit? The editor has to choose between: cutting reminder text, cutting flavor text, shrinking font, simplifying the mechanic, or splitting into two cards. Find the priority ordering and the cases where each solution was chosen.
- **New mechanic templating traps**: When a new mechanic is being templated for the first time, what are the common mistakes? (e.g., forgetting to specify "you control," creating unintended interactions with existing rules text patterns.) Build the first-time-templating checklist from real mistakes.
- **The "sounds right but isn't" problem**: Some rules text sounds natural in English but is ambiguous or wrong under the comprehensive rules. (e.g., "Destroy target creature. It can't be regenerated" vs. the correct "Destroy target creature. It can't be regenerated this turn.") Find the catalog of natural-language-vs-rules-language gaps.

**Pre-known lessons to verify and deepen:**
- Modern templating conventions ("enters" not "enters the battlefield", etc.)
- Keyword hierarchy (evergreen > deciduous > set-specific)
- Reminder text rules by rarity
- The text box budget (~7-9 lines)
- Ability ordering on cards
- Collector number ordering
- Name conflict checking
- The "this creature" / "this spell" / card name decision tree

**Deliverable:** A skill that takes a card file and applies rigorous templating, adds reminder text, corrects keyword usage, assigns collector numbers, checks name conflicts, and verifies text box fitting. The skill must contain the full catalog of templating mistakes from Magic's history — so it catches the same ambiguities and errors that real editors have caught before.

---

### SKILL 8: `mtg-creative-writer`

**Why build eighth:** With mechanically complete, templated cards, we can now name everything and add flavor.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| "Form of the Writer" (Doug Beyer, 2010) | How the name/flavor text process works from the creative lead's perspective |
| "Behind the Cardboard" (Matt Cavotta, 2007) | The naming process: how writers submit options, how the lead selects |
| "The Magic Style Guide" parts 1-2 (Matt Cavotta, 2005) | How the style guide informs naming and flavor writing |
| Flavor text analysis across recent sets | Patterns in length, attribution, tone, worldbuilding density |
| "Say My Name" (Matt Cavotta, 2005) | **The art and science of naming Magic cards — what makes a name memorable vs. forgettable, evocative vs. generic** |
| "Staging an Intervention" (Doug Beyer, 2010) | How creative gives feedback on names and flavor text |
| Card naming patterns by card type | Spells = verb phrases, creatures = noun phrases, legendaries = proper names |
| WotC Creative Writing team guidelines (as described in various articles) | Writer submission process, selection criteria, style constraints |
| Keyword naming history | How ability words and keyword abilities get their final names |
| Flavor text attributed quotes vs. unattributed narration | When to use each |
| **Sets praised for exceptional creative writing** (original Innistrad, Eldraine, Strixhaven) | **What specifically was better about the naming and flavor text in these sets?** Analyze patterns: word choice, rhythm, compression, worldbuilding density per word. |
| **Sets criticized for generic or forgettable naming** | **What makes card names feel generic?** Find the specific antipatterns: over-reliance on "[Adjective] [Noun]" formulas, names that don't evoke the world, names that could be in any set. |
| **The history of keyword naming successes and failures** | "Landfall" is a perfect keyword name — evocative, one word, sounds like Magic. "Forecast" and "haunt" are mediocre — they don't clearly communicate what the mechanic does. **Find what separates great keyword names from weak ones.** |
| **Rosewater on resonance in naming** | How names create "aha moments" when a player understands what a card does before reading the rules text. **This is the highest form of naming craft — find the principles.** |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — names that didn't work**: Which card names caused confusion (name didn't match function), felt generic (could be on any card in any set), or were forgettable? Find specific examples and the root cause for each.
- **The compression art**: The best flavor text says a lot in very few words. How? Find the specific techniques: implying a larger story through a single detail, using character voice to build personality, ending on a twist or reversal, leaving the audience to fill in the gaps. Analyze 20+ examples of acclaimed flavor text to extract the patterns.
- **The naming culture problem**: How do you create consistent naming conventions for a new plane without making every name sound the same? Innistrad pulls from Germanic roots. Kamigawa from Japanese. Ravnica from Slavic. But within each culture, there's variety. **Find the balance point between consistency and monotony.**
- **When flavor text hurts**: Sometimes flavor text actively damages a card by clashing with the mechanical identity, being tonally wrong for the set, or trying too hard to be clever. Find examples of bad flavor text and what made it bad.
- **The attribution strategy**: Across a set, which characters get attributed quotes, how many quotes each, and what voice does each character maintain? Find the actual planning methodology — it's not random. There's a strategy for using attribution to build narrative.
- **Keyword naming as communication design**: A keyword name is the first thing a player learns about a mechanic. "Deathtouch" instantly communicates what it does. "Bushido" does not. **Find the communication-design principles that separate self-explanatory keyword names from opaque ones.**
- **The legendary naming formula — and its exceptions**: [Given Name], [Title] is the standard, but the best legendary names break this formula meaningfully. Find the variations and when each is appropriate.
- **How naming interacts with card evaluation**: Players evaluate cards partly by name. A card named "Supreme Verdict" feels more powerful than a card named "Judicial Decree" even if they do the same thing. **Find the research/discussion on how naming affects perceived card quality.**

**Pre-known lessons to verify and deepen:**
- Names must work on three levels (mechanical, worldbuilding, Magic-belonging)
- The name length constraint (~25 chars)
- Naming cultures per plane
- Flavor text as microfiction
- Attribution builds character
- Flavor text worldbuilding across a set
- The em-dash convention
- Keyword naming principles
- Legendary naming formula

**Deliverable:** A skill that takes a card file plus **either** a `world_guide.md` **or** an `ip_catalog.md` and names every card and writes flavor text, following MTG naming conventions and building the world's story across the set. The skill must embody the compression craft of great flavor text writers and the naming instincts of experienced creative leads — not just following formulas, but understanding *why* certain names and flavor text resonate.

**Special handling for Universes Beyond input:** When working from an IP catalog, the skill must strictly follow the IP's established naming conventions (character names cannot be invented, locations have canonical names, terminology must match the source). Flavor text should quote or reference canonical material when possible. The skill must also research each IP's voice and tone — LotR's archaic register is different from Final Fantasy's melodrama, which is different from Warhammer 40K's grimdark Latin. Encode the wisdom of what makes IP adaptation voice feel authentic vs. tourist.

---

### SKILL 9: `mtg-art-director`

**Why build ninth:** With named, flavored cards, we can concept the art.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| Cynthia Sheppard's "What does a Magic art director do?" blog post | **The definitive inside look — especially the parts about volume (578 pieces/year), the feedback process, and what makes art direction fail** |
| "Anatomy of an Illustration Prompt: MTG Style" (Muddy Colors blog) | The exact structure of MTG art descriptions: Setting, Color, Action, Focus, Mood |
| Various concept art / style guide reveals | What concept pushes produce; level of detail in style guides |
| Art description examples from published articles | **Actual art descriptions that were used to commission specific cards — compare the description to the finished art to see what was communicated well vs. poorly** |
| "Rotation Season" (Doug Beyer, 2010) | How the creative team conceptualizes cards — deciding what each card represents |
| "Flavor Driven" (Doug Beyer, 2009) | How flavor drives art direction decisions |
| Artist interviews about working with WotC | **THE ARTIST'S PERSPECTIVE: what makes a good art description vs. a frustrating one? What information do artists need that ADs forget to include? What restrictions feel arbitrary vs. helpful?** |
| "The Making of Kaladesh" | How a concept push works from start to finish |
| Booster Fun / special treatment art direction | How alternate art treatments are conceived and directed |
| Card concepting examples (from R&D wiki articles) | How a card's mechanics get translated into a visual concept |
| **Cards where the art doesn't match the mechanics** | **Failure stories**: cards where a flying creature looks grounded, where a fire spell looks icy, where the art misleads about what the card does. **What went wrong in the concepting/description?** |
| **Cards praised for exceptional art direction** | Which individual cards and which sets are praised for art cohesion? Find what the art direction did differently. |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — art-mechanics mismatches**: Find cards where the art actively confuses players about what the card does. A creature with reach that looks like it should fly. A sorcery that looks like an instant. A white card that looks black. For each, what went wrong in the concepting/description process?
- **The concept as bridge**: The concept ("a reef guardian defending a coral city") is the critical bridge between mechanics and art. What makes a concept *good*? Find the properties: it must explain the mechanics visually, place the card in the world, and give the artist a clear subject. What are the failure modes? (Too vague, too prescriptive, too disconnected from mechanics.)
- **The art description that works for AI**: Since our pipeline will likely use AI image generation rather than human artists, **find what makes art descriptions work well as prompts — and how MTG art descriptions need to be adapted for AI generation.** The 5-field format (Setting, Color, Action, Focus, Mood) may need expansion or modification.
- **Visual storytelling across a set**: Great sets tell a visual story — you can see the world's conflict, culture, and characters playing out across the card art. How is this planned? Is there a visual narrative arc? Which cards carry key story moments?
- **The mechanical readability requirement**: Players need to be able to look at art and make reasonable guesses about a card's abilities. Flying creatures should be airborne. Walls should look defensive. Equipment should look like something a creature wears. **Find the complete list of mechanics-to-visual-identity mappings.**
- **Color identity in art**: White cards are bright, orderly, often featuring sunlight. Black cards are dark, featuring shadows and decay. But these are guidelines, not rules — and great art directors know when to subvert them. **Find the principles for when color identity in art is strict vs. flexible.**
- **Scale and composition for the card frame**: Card art appears in a small window. Art that works at full size may be illegible at card size. **Find the specific composition principles: subjects must be centered and large, backgrounds should be atmospheric rather than detailed, avoid fine details that disappear at card scale.**
- **Style guide utilization**: ADs reference the style guide in every description, but some references are more useful than others. **What information from the style guide do artists actually use, and what do they ignore?**

**Pre-known lessons to verify and deepen:**
- The 5-field art description format (Setting, Color, Action, Focus, Mood)
- Concepting bridges mechanics and flavor
- Composition must serve card function
- Style guide as law
- Color identity = visual identity
- Flying creatures must look like they fly
- Scale communication

**Deliverable:** A skill that takes named/flavored cards plus **either** a `world_guide.md` **or** an `ip_catalog.md` and produces card concepts and structured art descriptions for every card, ready for AI image generation or human commission. The skill must encode the art direction wisdom that prevents the common failures: art-mechanics mismatches, unclear composition at card scale, and visual incoherence across the set.

**Special handling for Universes Beyond input:** When working from an IP catalog, the skill must reference the IP's established visual identity (character designs, costumes, locations, signature visuals) rather than inventing appearances. Art descriptions for IP characters should specify "as depicted in [canonical source]" to anchor the artist/image generator to the correct visual reference. Research how MTG's real UB art direction handled iconic visual moments — the specific lessons learned from LotR (interpretive fidelity), Final Fantasy (cross-game stylistic unification), and Warhammer 40K (gritty realism vs. MTG's typical high-fantasy polish).

---

### SKILL 10: `mtg-product-architect`

**Why build tenth:** This is the least critical for card quality but important for a complete product.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| Gavin Verhey's product design articles and videos | **How Commander precons are designed — and the specific failures (underpowered precons that don't sell, overpowered precons that warp the format, precons that don't connect to the main set)** |
| "What Are Play Boosters?" (Rosewater, 2023) | The modern booster structure and its implications — **and the reasoning behind killing Draft Boosters (what was wrong with the old system)** |
| Commander precon design philosophy articles | How precon themes are chosen, power level targeting, new card design for precons |
| Mark Heggen / Mike Turian product architecture mentions | How the product suite is planned across a year |
| Collector Booster treatment philosophy | How special treatments are chosen |
| Secret Lair and special product design | How ancillary products extend a set's appeal |
| **Product failures — sets that underperformed commercially** | **THE KEY WISDOM SOURCE: which products flopped, and why? Was it the wrong product for the wrong audience? Wrong price point? Wrong power level? Lack of chase cards?** Find the specific commercial failures and extract what product architecture could have prevented them. |
| **The Commander precon power-level debate** | **Commander precons have a specific power-level target that has shifted over time.** Find the history: when precons were too weak (nobody bought them), when they were too strong (warped the format), and where the sweet spot is now. |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — products nobody wanted**: Which ancillary products (precons, bundles, special editions) underperformed? Why? Was the problem the product concept, the pricing, the power level, or the disconnect from the main set?
- **The Commander precon paradox**: Precons must be good enough to buy but not so good they obsolete deck-building. They must connect to the main set but not require main set cards. **Find the specific design framework for navigating these contradictions.**
- **Chase card psychology**: What makes a card a "chase card" that drives booster sales? Is it raw power, unique effect, beloved character, or beautiful art? Find the actual breakdown — it's probably a combination, but in what proportion?
- **The special treatment evolution**: Showcase frames, borderless art, extended art, serialized cards — each was introduced to solve a specific problem. **Find what problem each solved and whether it worked.**
- **Product fatigue signals**: How does WotC know when they're releasing too many products? Find the discussion around product fatigue and the principles for a healthy release calendar.

**Pre-known lessons to verify and deepen:**
- Commander precons complement, don't complete
- The "poster card" principle
- Collector Booster hooks
- Price point consciousness

**Deliverable:** A skill that defines Commander precon themes, identifies poster cards, suggests special treatments, and outlines the product suite. The skill must encode the wisdom of what makes products succeed or fail commercially — not just what they contain, but why players buy them.

---

### SKILL 11: `mtg-card-renderer` (already exists)

**No rebuild needed.** The existing skill is well-scoped and functional. May need minor updates to consume the new pipeline's output format, but no fundamental changes.

---

### SKILL 12: `mtg-set-pipeline` (orchestrator)

**Why build last:** This can only be built once all component skills exist and are tested.

**Research targets:**

| Source | What to extract |
|--------|----------------|
| The pipeline document we already created | The dependency graph and data flow |
| "Vision Design, Set Design, and Play Design" (Rosewater, 2017) | **The handoff process between teams — and the years of iteration it took to get the handoff point right. The history of getting it wrong IS the wisdom.** |
| All handoff documents | The structure and content of formal handoffs |
| Lessons from running the individual skills | What worked, what broke, where feedback loops are needed |
| **Erik Lauer's original question: "Are we handing off at the wrong time?"** | **The single most important insight in the modern pipeline's history.** The entire Vision/Set/Play restructuring came from recognizing the handoff point was wrong. Find the full reasoning. |
| **Sets that had production problems** | Sets where the pipeline broke down — where communication between teams failed, where handoffs were incomplete, where feedback loops didn't work. (e.g., Rivals of Ixalan was caught in the middle of the system transition.) |

**Wisdom to discover (research must find answers to all of these):**

- **Failure stories — pipeline breakdowns**: When has the WotC pipeline failed? Not individual card failures, but *process* failures: teams working at cross-purposes, handoffs that didn't communicate the vision, feedback that arrived too late to matter. Find at least 3 specific examples.
- **The handoff problem**: Erik Lauer's key insight was that the Design→Development handoff happened at the wrong point in the process. **Understand deeply why it was wrong, what the symptoms were, and how the new handoff points were chosen.** This is the most important pipeline wisdom because we're designing our own handoff points.
- **Feedback loop timing**: When Play Design flags a card, how far back does the fix need to go? Sometimes it's just a number change (Play Design fixes it). Sometimes the card needs a redesign (Set Design). Sometimes the mechanic is broken (back to Vision Design). **Find the framework for routing feedback to the right level.**
- **The art deadline constraint**: In the real pipeline, card concepts must be locked before art is commissioned, which happens mid-Set-Design. This creates a hard constraint: mechanics can change after art is commissioned, but only within the bounds of the existing art. **Find how this constraint shapes decision-making and what goes wrong when it's violated.**
- **The "two years ahead" problem**: WotC designs sets two years before release. This means Play Design is testing against a Standard format that doesn't exist yet. **How do they handle this uncertainty? What are the failure modes of testing against a predicted-but-wrong metagame?**
- **Communication bandwidth**: The handoff document is the primary communication artifact between Vision and Set Design. But it's a one-way document — it can't answer questions. **Find how teams handle the information that the handoff document doesn't cover.**

**Pre-known lessons to verify and deepen:**
- Feedback loops are essential
- The handoff document is the contract
- Checkpoint user interaction
- Fail gracefully

**Deliverable:** A master orchestrator skill that chains all other skills, manages handoffs, handles feedback loops, and produces the complete set. The skill must encode the pipeline wisdom — particularly the hard-won lessons about handoff timing, feedback routing, and communication between phases.

**Track selection logic:** At pipeline start, after intake but before Exploratory Design, the orchestrator asks the user: "Is this set based on an existing IP (book, game, film, TV show) or an original Magic world?" Based on the answer, the orchestrator branches: original sets run Skill 3A (`mtg-worldbuilder`) in parallel with Vision Design; IP sets run Skill 3B (`mtg-ip-researcher`) first (since IP constraints must be known before Vision Design can proceed meaningfully). The orchestrator must pass the correct creative artifact type downstream and instruct later skills (Vision Designer, Set Designer, Creative Writer, Art Director) to apply their UB-specific handling when the track is UB.

---

## Data Contracts Between Skills

To make skills composable, they need agreed-upon input/output formats:

| Artifact | Produced by | Consumed by | Format |
|----------|------------|-------------|--------|
| `exploration_doc.md` | Exploratory Designer | Vision Designer | Markdown |
| `world_guide.md` | Worldbuilder (Skill 3A, original worlds only) | Vision Designer, Set Designer, Creative Writer, Art Director | Markdown |
| `ip_catalog.md` | IP Researcher (Skill 3B, UB sets only) | Vision Designer, Set Designer, Creative Writer, Art Director | Markdown |
| `ip_constraints.md` | IP Researcher (Skill 3B, UB sets only) | Vision Designer (primarily) | Markdown |
| `vision_handoff.md` | Vision Designer | Set Designer | Markdown |
| `vision_cardfile.json` | Vision Designer | Set Designer | JSON (card array) |
| `set.json` | Set Designer | All downstream skills | JSON (card array) — THE canonical format |
| `color_pie_review.md` | Color Pie Reviewer | Set Designer (feedback) | Markdown |
| `play_design_report.md` | Play Designer | Set Designer (feedback) | Markdown |
| `editing_report.md` | Editor | — (terminal) | Markdown |
| `naming_guide.md` | Creative Writer | — (reference) | Markdown |
| `art_descriptions.json` | Art Director | Card Renderer | JSON |
| `card_images/*.png` | Card Renderer | — (terminal) | PNG files |

**Track selection:** At pipeline start, the user chooses one of two creative tracks. `mtg-worldbuilder` (Skill 3A) runs for original Magic sets; `mtg-ip-researcher` (Skill 3B) runs for Universes Beyond sets. The two skills produce different artifacts but serve the same downstream purpose: giving Vision Design the creative context it needs. Vision Design and later skills must be able to consume either `world_guide.md` OR `ip_catalog.md + ip_constraints.md` as their creative input.

The `set.json` card format should be standardized early and used by all skills. Proposed schema (extending the existing mtg-set-designer format):

```json
{
  "name": "Card Name",
  "mana_cost": "{2}{W}{U}",
  "type_line": "Creature — Human Wizard",
  "rules_text": "Flying\nWhen this creature enters, draw a card.",
  "flavor_text": "She saw the answer before the question was asked.",
  "power": 2,
  "toughness": 3,
  "rarity": "uncommon",
  "color_identity": ["W", "U"],
  "set_number": 42,
  "archetype_tags": ["WU_flyers", "card_draw"],
  "mechanic_tags": ["flying"],
  "concept": "An Azorius skymage consulting her law-scroll mid-flight",
  "art_description": { "setting": "...", "color": "...", "action": "...", "focus": "...", "mood": "..." },
  "design_notes": "Signpost uncommon for WU archetype",
  "color_pie_rating": 1,
  "play_design_flags": []
}
```

---

## Estimated Effort

| Skill | Research | Build | Test | Total |
|-------|----------|-------|------|-------|
| Color Pie Reviewer | 1 session | 1 session | 1 session | 3 sessions |
| Exploratory Designer | 1 session | 1 session | 1 session | 3 sessions |
| Worldbuilder (3A) | 1 session | 1 session | 1 session | 3 sessions |
| IP Researcher (3B) | 1.5 sessions | 1.5 sessions | 1 session | 4 sessions |
| Vision Designer | 2 sessions | 2 sessions | 1 session | 5 sessions |
| Set Designer (refactor) | 1 session | 2 sessions | 2 sessions | 5 sessions |
| Play Designer | 1 session | 2 sessions | 1 session | 4 sessions |
| Editor | 1 session | 1 session | 1 session | 3 sessions |
| Creative Writer | 1 session | 1 session | 1 session | 3 sessions |
| Art Director | 1 session | 1 session | 1 session | 3 sessions |
| Product Architect | 1 session | 1 session | 0.5 session | 2.5 sessions |
| Pipeline Orchestrator | 0.5 session | 2 sessions | 2 sessions | 4.5 sessions |
| **Total** | | | | **~43 sessions** |

A "session" = one focused conversation with Claude. Some research sessions may require multiple search passes. IP Researcher gets slightly more time because it needs extra testing across multiple different IP types (a fantasy novel series, a video game franchise, a TV show) to verify the skill generalizes.

---

## Next Step

The pipeline now has **12 skills to build** (Color Pie Reviewer, Exploratory Designer, Worldbuilder 3A, **IP Researcher 3B**, Vision Designer, Set Designer refactor, Play Designer, Editor, Creative Writer, Art Director, Product Architect, Pipeline Orchestrator) plus the existing Card Renderer.

The two creative-track skills (3A and 3B) are mutually exclusive per set but both must exist so the pipeline can handle both original Magic worlds and Universes Beyond adaptations.

Say **"Build Skill 1"** and I'll begin the deep research phase for `mtg-color-pie-reviewer`, pulling real lessons from the Council of Colors, the Mechanical Color Pie article, and Rosewater's 20+ years of color pie philosophy — then build the skill with those lessons encoded.
