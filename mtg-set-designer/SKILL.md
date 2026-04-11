---
name: mtg-set-designer
description: Design a complete, balanced, draftable Magic&#58; The Gathering set (~261 cards) for the Play Booster era from a theme, idea, or world. Use this skill whenever the user wants to create, design, build, draft, prototype, or iterate on a Magic set, Magic block, custom MTG set, fan set, or homebrew Magic set — even if they just say "make me an MTG set about X" or "design a Magic expansion with Y mechanic" or "I have a theme, turn it into a set." Also trigger when the user mentions color pie, draft archetypes, mana curve, set mechanics, signpost uncommons, or limited format balance in a context that implies building a set rather than critiquing existing cards. Produces structured JSON files (cards, mechanics, archetypes) plus a markdown design document, and runs both heuristic and simulated balance checks so the output is a tested, balanced, limited-playable set rather than a list of cool-sounding cards.
---

# MTG Set Designer

Design a complete Magic: The Gathering set — mechanics, archetypes, ~261 cards across five colors and four rarities, worldbuilding, and balance — using the process real Wizards of the Coast set designers use, designed for the **Play Booster** format (which replaced Draft Boosters starting in 2024). The output is a *playable, draft-tested* set, not a wishlist of cards.

This skill is opinionated because good set design is opinionated. It is based on the published process and principles of Mark Rosewater (head designer), Erik Lauer, Aaron Forsythe, Ethan Fleischer, Melissa DeTora, and Doug Beyer, drawn from *Making Magic*, *Drive to Work*, and vision design handoff documents.

## What "done" means

A finished set consists of:

1. **`design_doc.md`** — the narrative design document: vision, three pillars, worldbuilding, mechanics, the ten archetypes, and open questions. This is the thing a human reads to *understand* the set.
2. **`set.json`** — the machine-readable set. Required top-level fields: `set_code`, `set_name`, `cards`. The `cards` array holds every card with name, mana cost, type, rules text, power/toughness, rarity, color, flavor, and archetype tags. Mechanics and archetypes may be inlined here *or* kept in sibling files (next two items); the validator accepts either pattern.
3. **`mechanics.json`** — each named mechanic with reminder text, color distribution, and rarity spread. Optional if mechanics are inlined in set.json.
4. **`archetypes.json`** — the 10 two-color archetypes with strategy, enablers, payoffs, and signposts. Optional if archetypes are inlined in set.json.
5. **`balance_report.md`** — heuristic checks plus simulated draft results, with any flags the designer should address.

Do not declare a set "done" until the balance report is clean or its warnings are explicitly acknowledged.

## The process

Set design is a pipeline with explicit phases. Do them in order. Do not skip phases because it feels faster — skipping is where parasitic mechanics, broken curves, and dead archetypes come from.

The phases mirror the real WotC split into Vision Design → Set Design → Play Design, compressed into a workflow one designer (you) can actually execute.

### Phase 0 — Intake

Before writing anything, confirm these with the user (or reason explicitly from what they gave you):

- **Theme / world** — what is this set *about*? A setting (Kamigawa, Theros), a mood (gothic horror), a concept (heists), or a mechanic (lands-matter)?
- **Top-down or bottom-up?** — Top-down starts from flavor and finds mechanics to fit (Innistrad). Bottom-up starts from a mechanical idea and dresses it in flavor (original Zendikar). Both are valid; state which you're doing so the later phases stay consistent.
- **Set size** — default is the modern Play Booster premier-set shape: **81 commons, 100 uncommons, 60 rares, 20 mythics** (total ≈ 261 unique cards, plus basic lands). This is the post-2024 standard; Draft Boosters are discontinued. Deviate only if the user asks.
- **Constraints** — returning mechanics? Existing world? Forbidden mechanics? Legality target (Standard-legal vs. Modern Horizons-style)?

If the user gave you a one-line prompt ("design a set about octopuses"), *do not* interview them to death. Make reasonable choices, state them explicitly in the design doc under "Assumptions," and proceed. The user can correct you on the output.

### Phase 0.5 — Theme Research

Read `references/theme-research.md` before this phase. It contains the full methodology. **If the set adapts an existing IP**, also read `references/universes-beyond-patterns.md` — it distills lessons from how WotC adapted LotR, Warhammer, Doctor Who, Fallout, and Final Fantasy into Magic cards, covering naming conventions, character density, flavor text strategy, mechanic design, and card type selection.

**Do not skip this phase.** Do not rely on your own knowledge of the theme, even if you think you know it well. Every theme gets researched — the depth varies, but the step is never optional.

The goal is to produce a **Theme Brief** section in `design_doc.md` that gives the Vision phase a solid factual and structural foundation to build pillars from.

**The workflow:**

1. **User interview (3–5 questions).** Ask about: which version/era of the IP, faithful vs. reinterpretation, the emotional hook (why this theme?), audience familiarity, and tone boundaries. Keep it focused — you're understanding intent, not extracting a design doc.

2. **Web research.** Search for the theme using the strategy in the reference doc. At minimum: one overview search, one structure/factions search, one iconic-elements search, and one fan-wiki search. For cultural themes, add scholarly and sensitivity searches. **Add every URL you consult to the "Research Sources" section of the Theme Brief in `design_doc.md`** — these are set-specific, not skill-level sources.

3. **Source material decomposition.** From your research, extract:
   - **Factions / groups / tribes** and a tentative color-pie mapping (based on *values*, not aesthetics)
   - **Resonance inventory** — characters, locations, objects, moments, and concepts that fans would be disappointed not to see
   - **Anti-resonance inventory** — elements that won't translate to MTG or should be avoided
   - **Power structure** — who has power, who doesn't, how is it contested
   - **Magic system** (if any) — how the source handles the supernatural, which often suggests mechanics

4. **Tone calibration.** Write 3–5 sentences establishing the set's violence level, humor/gravity balance, and nostalgia/novelty positioning.

5. **Existing MTG crossover check.** Search for Universes Beyond, Secret Lair, Un-set, or thematically adjacent MTG products. Note what they did, what worked, and what the community thought.

6. **Cultural sensitivity scan** (for real-world cultural themes). Identify sacred/sensitive elements, stereotyping risks, terminology considerations, and flag anything that needs extra care during Polish.

Write all of this into the **Theme Brief** section of `design_doc.md` using the template in the reference doc. The Theme Brief is a living document — update it as later phases reveal that mappings or resonance points need adjustment.

### Phase 1 — Vision

Read `references/vision.md` once before writing this phase. It explains the *three pillars* concept in detail.

Produce the opening of `design_doc.md` containing:

- **Elevator pitch** — one sentence.
- **The three pillars** — exactly three (occasionally four) load-bearing ideas that unify the set. Each pillar is one sentence of *mechanical or experiential* commitment, not a flavor noun. "Gothic horror" is not a pillar. "Creatures transform into bigger, scarier versions of themselves" is a pillar.
- **Tone & play feel** — aggressive? slow and grindy? combo-forward? What does a game *feel* like?
- **Set identity sentence** — the sentence you'd use to sell the set to a skeptical playtester in ten seconds.

The three pillars are the most important artifact in the whole process. Every later decision gets tested against them. If a mechanic doesn't serve a pillar, cut it or change the pillar.

### Phase 2 — Worldbuilding

This phase looks very different depending on whether the set adapts an existing world or invents a new one. Check the Theme Brief from Phase 0.5 — it tells you which case you're in.

**If the set adapts an existing world or IP** (My Little Pony, Lord of the Rings, Greek mythology, feudal Japan, etc.): the Theme Brief already contains the world — its factions, locations, characters, conflicts, tone, and power structure. Phase 2 becomes a short *synthesis* step, not a creative step. Write a brief section in `design_doc.md` that:

- Confirms which elements from the Theme Brief will carry into the set (not everything needs to be represented — a set can't hold an entire IP)
- Decides the **creature types** that will define the set's tribes and carry its mechanical identity, mapped from the source material's factions
- Identifies the **central conflict** the set will dramatize (an IP may have many conflicts; pick the one that produces the best gameplay)
- Notes any **MTG-specific worldbuilding** the source doesn't provide — what does mana look like in this world? Are there planeswalkers? How does the source's magic system translate to MTG's spell structure?
- Flags any **gaps** where the source material is thin and original invention is needed (e.g., the IP doesn't have enough villain factions to fill all 10 archetypes)

Also establish a **set palette** — the dominant colors, light sources, materials, and recurring visual motifs that will give the set visual coherence. See `references/art-direction.md` for what to include. This palette guides every card's art description in Phase 5.

This should be half a page to a page. The Theme Brief did the heavy lifting; this phase just shapes it for MTG.

**If the set invents a new world** (original concept, mechanical premise, mood-first design): Phase 2 is where the actual creative worldbuilding happens, and it needs to be *substantially more detailed*. The Theme Brief's research into analogues and adjacent fiction gave you raw material; now build a world from it.

Write 1–3 pages in `design_doc.md` covering:

- **The world** — name it, describe its physical nature, explain what makes it distinctive. "A plane where..." is your opening.
- **Factions or regions** (typically 3–5) — these are the groups that will become your color pairs or tribes. Each faction needs: a name, a philosophy (mapped to the color pie), a home territory, a signature creature type, and a relationship to the other factions. Factions that don't create *conflict* with each other won't produce interesting gameplay.
- **Central conflict** — what is the world's core tension? The best set conflicts are ones where both sides have a point (Mirrodin vs. Phyrexia, civilization vs. wilderness, tradition vs. progress). One-sided conflicts ("good guys vs. evil") tend to produce flat archetypes.
- **History and lore** — just enough to justify the current conflict and give cards evocative names. You don't need a creation myth; you need to know why these factions are fighting *now*.
- **The magic system** — how does magic work here? This often suggests mechanics directly. A world where magic comes from singing produces different mechanics than a world where magic comes from consuming memories.
- **Creature ecology** — what lives here? Name the creature types that will populate the set's commons. These need to span all five colors and feel native to the world, not imported from generic fantasy.
- **Locations** — name 5–10 places that could become named lands, anchor cycles, or appear in flavor text. Good locations tell you something about the world's conflict.

Finally, establish a **set palette** — the dominant colors, light sources, materials, and recurring visual motifs that will give the set visual coherence. See `references/art-direction.md` for what to include. This palette guides every card's art description in Phase 5.

The more original the concept, the more this phase matters. A set built on "deep-sea horror" needs the designer to invent the specific horrors, the specific depths, and the specific reasons anyone would go down there. Don't leave this vague — vague worldbuilding produces generic cards.

### Phase 3 — Mechanics

Read `references/mechanics.md` before designing mechanics. It covers keyword vs. ability word vs. named mechanic, parasitic vs. modular, complexity budget, and evergreen usage.

Design **2–4 named new mechanics** for the set. Not more. More named mechanics than that is a symptom of not having decided what the set is.

**For IP-based sets:** At least one new mechanic should be a **system translation** — a direct mechanical recreation of something the IP does, not just a thematic reskin. The Ring Tempts You (LotR) mechanically recreates the One Ring's progressive corruption. Rad counters (Fallout) mechanically recreate radiation damage. Saga Creatures (Final Fantasy) mechanically recreate summon sequences. Before designing mechanics, make a two-column list of the IP's distinctive systems (left column) and proposed MTG translations (right column). See `references/universes-beyond-patterns.md`, Lesson 4.

For each mechanic, write (in `mechanics.json` and narratively in the design doc):

```
{
  "name": "Kindle",
  "type": "keyword|ability_word|named",
  "reminder_text": "When this creature enters, deal 1 damage to any target.",
  "serves_pillar": "pillar 2 - fire spreads",
  "colors": {"primary": ["R"], "secondary": ["W"], "tertiary": []},
  "rarity_spread": {"common": 6, "uncommon": 4, "rare": 2, "mythic": 1},
  "parasitic_risk": "low - works without other Kindle cards",
  "design_space": "short description of the lever this mechanic gives you"
}
```

The **parasitic risk** field is non-negotiable. If a mechanic only functions with other cards that have the same mechanic, it is parasitic and you must either (a) kill it, (b) give it a universal trigger (like Landfall), or (c) accept it and design an archetype that owns it *entirely* in one color pair. Splice-onto-Arcane (Kamigawa, infamous) is the warning.

Also decide which **evergreen** and **deciduous** keywords the set uses: flying, first strike, haste, vigilance, lifelink, deathtouch, trample, reach, menace, ward, etc. These are the background texture of the set and carry huge weight — they should not be afterthoughts.

### Phase 4 — Archetype grid

Read `references/archetypes.md` once before this phase.

A standard set is built around **10 two-color draft archetypes**, one for each pair (WU, UB, BR, RG, GW, WB, UR, BG, RW, GU). Each archetype gets an identity, a gameplan, enablers, and payoffs. This is where your mechanics meet the draft table.

Build `archetypes.json`:

```
{
  "WU": {
    "name": "Skybound Scholars",
    "strategy": "tempo flyers that bank card draw",
    "speed": "medium",
    "key_mechanic": "Kindle (secondary)",
    "signpost_uncommons": [
      {"role": "enabler", "sketch": "2W/U - 1/3 flyer, when it ETBs scry 1"},
      {"role": "payoff",  "sketch": "WU gold - whenever you draw your second card each turn, put a 1/1 flyer onto the battlefield"}
    ],
    "commons_needed": ["cheap evasive bodies", "a conditional counterspell", "a 4-drop finisher flyer", "card selection"],
    "enemy_archetypes": ["BR aggro (too fast)"]
  },
  ...
}
```

**Every** archetype must:

- Have a clear gameplan a drafter can learn in one pack.
- Be supported at common with enough cards to actually draft the deck 8-player pod.
- Have two signpost uncommons (one enabler, one payoff) that together announce the archetype.
- Have a believable interaction with the set's three pillars.

If an archetype doesn't fit, fix it — don't print it broken. A half-supported archetype poisons the draft environment because drafters who try it lose to drafters in the supported archetypes.

### Phase 5 — Card file

Now write the actual cards into `set.json`. **Start from the design skeleton** in `assets/design_skeleton.json` — it contains every slot code with its target mana value, card type, and role notes, based on Rosewater's Nuts & Bolts #16 (Play Booster update). Read `references/design-skeleton.md` for how the skeleton works and how to map slots to cards.

The skeleton is your checklist: walk through it slot by slot, filling each with a card that fits the slot's structural role while expressing your set's theme and mechanics. When you deviate from the skeleton (swapping a removal slot for a self-mill card, etc.), note the deviation in `design_doc.md` so the balance checker's flags can be read as "intentional" rather than "forgot."

The card schema is in `assets/set_template.json`. Include the skeleton slot code in each card's `id` field (e.g., `CW01`, `UB05`).

**Consult the card type catalog.** Read `references/card-types.md` before writing cards — it contains every card type and mechanically significant subtype in the game, with guidance on when to use each one. Do not default to creatures for every permanent slot. Before filling each skeleton slot, ask whether a Saga, Battle, Vehicle, Equipment, Class, Case, Room, or other type would better express the card's theme and role. If your set has zero Battles, zero Sagas, zero Equipment, and zero Vehicles, verify that's a deliberate choice, not an oversight.

**Every card gets an art description.** Read `references/art-direction.md` before writing cards — it covers the WotC art brief format, what makes art read at card size, and how to write descriptions by rarity. Write the art description alongside each card's mechanical design, not as a separate pass. Each art description has five fields: `scene` (1–3 sentences of what's in the image), `focus` (the single primary visual element), `mood` (2–5 words of emotional register), `palette` (dominant colors), and `frame` (camera angle / shot type). The description should work as an image search query or AI image generation prompt with minimal editing.

Do this in this order, not randomly:

1. **Commons first, all five colors in parallel.** Commons are the foundation of limited — if the theme isn't at common, it isn't your theme. Target roughly **14–15 commons per color** plus ~6–11 colorless/artifact/land commons (totaling 81). In the Play Booster era, commons are fewer but higher-impact — there are no "filler" commons. The skeleton provides exact slot counts per color. Per-color breakdown from Rosewater's Nuts & Bolts article:
   - White: ~15 commons (~11 creatures, ~4 noncreatures)
   - Blue: ~15 commons (~8 creatures, ~7 noncreatures)
   - Black: ~14 commons (~9 creatures, ~5 noncreatures)
   - Red: ~14 commons (~9 creatures, ~5 noncreatures)
   - Green: ~14 commons (~10 creatures, ~4 noncreatures)
   - Plus ~9 colorless/artifact commons
   Make sure each color has a creature on-curve at every mana value from 2 to 5, at least one common removal-or-answer, and cards that support both archetypes the color participates in.

2. **Uncommons.** In the Play Booster era, uncommons carry *much* more weight — **100 total** (up from 80). Target ~16–18 per color plus **~20 gold uncommons** (the signpost uncommons from Phase 4 go here, two per archetype). Per color expect ~10 creatures and ~6–8 noncreatures. Uncommons now do much of the heavy lifting for archetype support that commons used to do. This is where your archetype payoffs, removal variety, and signpost cards live.

3. **Rares.** ~12 per color plus gold rares and a few utility lands (60 total). Rares are bombs and built-around effects — they can be more complex, but they still must respect the color pie. In the Play Booster era, ~41% of packs have two or more rares, so rares show up in draft *much more frequently* — design your commons and uncommons to include adequate answers to rare-level threats.

4. **Mythics.** ~4 per color plus gold and planeswalkers / legendary centerpieces (20 total). Mythics are the "wow" moments and often anchor constructed archetypes. Do not use mythic as "rare but bigger." Mythics should do something the rare slot cannot.

5. **Cycles.** Once the main file is drafted, look for **cycles** — a card per color, a card per two-color pair, a card per archetype. Cycles are a cheap way to make a set feel cohesive and to hit your rarity counts. But unique cards beat forced cycle members. See `references/cycles.md`.

6. **Basic lands.** 20 slots, 4 per basic. Usually just art variants unless your set has a reason to reimagine them.

**Character-rich IP sets: use the character roster.** If the Theme Brief contains a character roster (Phase 0.5), use it as a binding assignment list during card creation, not a nice-to-have reference. Work through the roster and assign each character to a specific card slot *before* filling the remaining slots with original designs. Characters should be the *first* thing placed into the set, not an afterthought sprinkled on top of generic creatures.

Targets for character-rich IPs:
- Mythics: at least 4–8 named characters (protagonists, main villains)
- Rares: at least 10–20 named characters (supporting cast, secondary villains, fan favorites)
- Uncommons: at least 5–15 named characters, especially as signpost uncommons when a character fits an archetype naturally
- Commons: generally not individual named characters, but reference characters heavily in card names (e.g., "Twilight's Study," "Fluttershy's Songbird"), flavor text, and art descriptions

A character-rich IP set should have **20–40 cards that ARE specific named characters** plus another **30–50 cards that reference characters** indirectly. If your set file has fewer than 20 named-character cards for a character-rich IP, something went wrong — go back to the roster and assign more characters to slots. Every rare and mythic creature slot should be checked against the roster: is there a named character from the IP who fits this slot better than a generic creature would?

**IP naming conventions.** For sets based on existing IPs, follow the naming patterns from `references/universes-beyond-patterns.md`:

- **Named characters use "Name, Title/Descriptor" format.** The descriptor captures the character's role or state at a *specific story moment*, not a generic adjective. Multiple versions of the same character coexist by representing different moments in their arc (e.g., "Aragorn, Company Leader" vs. "Aragorn, King of Gondor"). Major characters (tier 1) get 2–3 versions; supporting cast get 1.
- **Non-character cards use direct IP terminology.** Spells are named after iconic quotes or events ("You Cannot Pass!", "Nuclear Fallout"). Locations, items, and game systems use their IP names directly. Never invent a generic Magic name when an IP-specific name exists — a removal spell in a LotR set is "Isildur's Fateful Strike," not "Heroic Smite."
- **Zero generic cards.** Even common creatures use IP terminology for names, type lines, and flavor text. A soldier in a Warhammer set is "Ultramarines Honour Guard," not "Elite Soldier." Every card should be identifiable as belonging to this IP. If a card could exist in any generic Magic set, it needs an IP-specific name.
- **Knowledge pyramid distribution.** Base-tier elements (the most iconic — the Ring, Gandalf, the main villain) go at mythic and rare for maximum visibility. Mid-tier elements (major characters, key locations) fill rare and uncommon. Top-tier deep cuts (minor characters beloved by dedicated fans) go at uncommon or appear in flavor text. This ensures casual fans recognize the splashy cards while dedicated fans find rewarding deep cuts.

**Flavor text strategy.** During Phase 0.5, the Theme Brief should have identified which flavor text approach fits the IP. Apply it consistently across the set:

- **Literary IPs with beloved prose** (Tolkien, etc.) → use direct quotes from the source material heavily; minimize original text
- **IPs with iconic catchphrases but limited prose** (Warhammer, Star Wars, etc.) → mix direct quotes with original text written in the IP's voice
- **Game or visual IPs** (video games, animation, etc.) → write original flavor text using the IP's terminology, tone, and worldview; use game-specific jargon where fans would expect it

In all cases, flavor text should sound like it *comes from* the IP's world, never from generic fantasy. If a piece of flavor text could appear on any Magic card, rewrite it.

While writing cards, obey the **New World Order** complexity budget. Details in `references/new-world-order.md`, but the short version: at most ~20% of commons may be "red-flagged" as complex, and new named mechanics should appear sparingly at common. If you find yourself adding a second ability to a common creature, ask whether it belongs at uncommon instead.

Use the color pie in `references/color-pie.md` as a hard check, not a suggestion. *Bending* the pie is fine when it serves a set pillar. *Breaking* it (undoing a color's core weakness) is the single most damaging thing you can do to the long-term game.

### Phase 6 — Balance: heuristic pass

Once `set.json` is drafted, run the heuristic balance checker:

```
python scripts/balance_check.py set.json
```

It outputs a report with:

- Per-color card counts by rarity
- Creature curves per color
- Removal density
- Keyword distribution
- Mechanic spread vs. target
- Archetype support counts (how many commons actually support each archetype)
- Color pie violations (flagged, not auto-corrected — judgment calls are yours)
- Vanilla/French-vanilla ratios
- Mana curve shape warnings

Read the report. Fix anything it flags. Then run it again. Do not proceed until this is clean or every remaining warning is documented in `balance_report.md` with a deliberate justification.

### Phase 7 — Balance: simulated draft pass

Now run the simulated draft:

```
python scripts/simulate_draft.py set.json --pods 200
```

This runs thousands of simulated 8-player drafts, builds decks for each drafter according to the archetype definitions, and plays games. It reports:

- Win rate by archetype
- Average deck composition
- Cards that appear in almost every deck (may be overpowered)
- Cards that appear in almost no deck (may be unplayable)
- Mana curve and removal-to-threat ratios per archetype
- Format speed (average turn the game ends)

Healthy bands:
- No archetype win rate below 42% or above 58%.
- No common goes below ~8% play rate or above ~95%.
- Format speed between turn 7 and turn 11 average for most sets.

Anything outside these bands is a call to revise. When you revise, revise *the card* not the simulator. And re-run. Iterate until the bands are met or you've documented why a given deviation is intentional.

### Phase 8 — Polish

Final pass on the file:

- Every card has flavorful, lore-consistent naming.
- Every card has flavor text at rare and mythic, and at least 30% of commons/uncommons.
- Reminder text is present where New World Order requires it (new mechanics, unfamiliar effects).
- Cycles are visually complete (no off-by-one).
- Archetype signposts read clearly.
- **Every card has an art description** with all five fields (scene, focus, mood, palette, frame). Check for: visual redundancy (two cards with near-identical scenes), palette consistency with the set palette from Phase 2, power/toughness plausibility (a 1/1 shouldn't be described as towering), and framing variety (not every card should be a medium shot).
- The design doc's "open questions" section is either resolved or handed forward as known issues.

**IP-specific polish checks.** For sets based on existing IPs, run these additional verifications before declaring the set done (see `references/universes-beyond-patterns.md` for the full checklist):

- **Zero generic names.** Scan every card name in the set. If any name could appear in a generic Magic set with no connection to this IP, replace it with an IP-specific name. Every card — even common 2/2s — should use IP terminology in its name, creature type, or both.
- **Character density.** Named characters should represent 20–30% of the set. Count the named-character cards. If the count is below 20% for a character-rich IP, assign more characters from the roster to card slots.
- **Character versions.** Verify that tier-1 characters (protagonists, main villains) have 2–3 versions showing different story moments, each mechanically distinct (different colors, abilities, or strategies).
- **Naming format.** All named characters should follow "Name, Title/Descriptor" format where the descriptor reflects a specific story moment, not a generic adjective.
- **Flavor text strategy consistency.** Verify the set uses the flavor text approach chosen in Phase 0.5 (direct quotes / mixed / original in IP voice) consistently. Check that no flavor text sounds like generic fantasy when it should sound like it comes from the IP.
- **System translation mechanic.** Verify at least one new mechanic is a genuine *system translation* from the IP — a mechanic that mechanically recreates something the IP does — not just a thematic reskin of an existing Magic mechanic.
- **Knowledge pyramid.** Verify base-tier IP elements (the most iconic) appear at mythic and rare, mid-tier at rare and uncommon, and deep cuts at uncommon or in flavor text. No deep-cut reference should occupy a mythic slot; no base-tier icon should be buried at common.
- **Card type matching.** Verify that Sagas retell specific iconic stories/episodes from the IP, Equipment represents iconic items, Vehicles represent iconic transportation, and double-faced cards represent character transformations or reveals.

Then present the finished files to the user.

## References

Read these when the current phase calls for them. They are larger than SKILL.md on purpose so SKILL.md can stay lean.

- `references/card-types.md` — comprehensive catalog of every card type and subtype (Battle, Saga, Vehicle, Equipment, Class, Case, Room, etc.) with thematic and mechanical guidance on when to use each
- `references/art-direction.md` — the WotC art brief format, what makes MTG art work at card size, how to write art descriptions by rarity, set palette guidance
- `references/theme-research.md` — the full theme exploration methodology: user interview, web research, source decomposition, resonance inventories, tone calibration, cultural sensitivity
- `references/vision.md` — the three pillars concept, top-down vs. bottom-up, how to write a vision document
- `references/color-pie.md` — detailed mechanical color pie, primary/secondary/tertiary, bending vs. breaking
- `references/mechanics.md` — keyword vs. ability word vs. named, parasitic vs. modular, complexity budget, evergreen list
- `references/archetypes.md` — the ten two-color archetypes, signpost design, how commons carry an archetype
- `references/new-world-order.md` — complexity at common, red-flag rules, lenticular design
- `references/rarity-structure.md` — what each rarity is *for*, rarity counts, the role of mythic
- `references/cycles.md` — cycle types, when to use them, when they become busywork
- `references/balance-heuristics.md` — the numerical targets the scripts check against and where they come from
- `references/design-skeleton.md` — the official WotC design skeleton concept, slot codes, Play Booster slot counts, and how to use it
- `references/universes-beyond-patterns.md` — lessons from how WotC adapted LotR, Warhammer 40K, Doctor Who, Fallout, and Final Fantasy into Magic cards: naming conventions, character density, flavor text strategy, system translation mechanics, knowledge pyramid, zero-generic-card standard
- `references/case-studies.md` — Innistrad, Ravnica, Theros, Lorwyn, Kamigawa (cautionary), Zendikar as worked examples

## Scripts

- `scripts/balance_check.py` — fast heuristic pass over `set.json`. Run it as many times as you need; it's cheap.
- `scripts/simulate_draft.py` — stochastic draft-and-play simulator for balance testing. Slower; run it once per iteration.
- `scripts/set_schema.py` — JSON Schema validator for `set.json`, `mechanics.json`, `archetypes.json`.

## Assets

- `assets/design_skeleton.json` — the official WotC design skeleton adapted for the Play Booster era (81C / 100U / 60R / 20M). Every slot code with mana value, type, and role notes. **This is your starting template for Phase 5.**
- `assets/design_skeleton_2021.csv` — the community "Bones" spreadsheet (Draft Booster era, historical reference only).
- `assets/set_template.json` — a minimal skeleton of the JSON *schema* with one example card/mechanic/archetype filled in. Shows the data format.

## Guiding principles (Rosewater-adjacent)

These are the principles to fall back on when a judgment call comes up.

**The set is more important than any one card.** A cool card that hurts the format gets cut. This is the hardest principle to follow because every card is somebody's darling.

**Find the fun first, then the elegance.** A mechanic that is elegant on paper but miserable to play against is a failed mechanic. Play it before defending it.

**Commons carry the set.** If your theme only shows up at rare, you don't have a theme; you have a bunch of cool rares.

**Parasitism is the default failure mode.** Every new mechanic should be interrogated with "what if this is the only card with this mechanic in a draft deck — is it still playable?"

**Bleed to serve the set, never to fix a color's weakness.** Blue can get light creature removal in a set *about* creature-removal-for-blue. Blue cannot get unconditional efficient creature removal *because it would be useful*. The weaknesses are the point.

**Complexity is finite.** Spend it where it matters. Every common you make complex is complexity you can't spend on the rare doing the actually interesting thing.

**Design, then test, then design again.** The balance scripts exist so you can be wrong quickly and cheaply. Use them. A set is never done on the first pass.
