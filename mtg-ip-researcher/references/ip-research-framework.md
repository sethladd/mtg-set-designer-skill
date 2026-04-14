# IP Research Framework

Canonical reference tables and design frameworks for cataloging existing IPs for Universes Beyond adaptation. Read this before starting any IP research. Use the templates as structures and the guidelines as constraints.

---

## Table of Contents

1. [The 5-Tier Priority System](#the-5-tier-priority-system)
2. [Knowledge Pyramid](#knowledge-pyramid)
3. [Color Pie Mapping Guide](#color-pie-mapping-guide)
4. [Catalog Templates](#catalog-templates)
5. [Scope Management](#scope-management)
6. [Naming Convention Extraction](#naming-convention-extraction)
7. [System Translation Inventory](#system-translation-inventory)
8. [Constraint Document Template](#constraint-document-template)

---

## The 5-Tier Priority System

Adapted from the Final Fantasy design process, where 600+ concepts were rated across all 16 games. Every element in the catalog gets a tier.

| Tier | Priority | Treatment | Example (LotR) |
|------|----------|-----------|-----------------|
| **5 — Mandatory** | Must appear as a card | Mythic/rare, multiple versions for Tier 1 characters | Gandalf, Frodo, Sauron, the One Ring |
| **4 — Preferred** | Should appear as a card if space allows | Rare/uncommon, single version | Faramir, Théoden, Shelob, Glamdring |
| **3 — Suggested** | Include if it enhances the set | Uncommon or spell art/flavor text | Tom Bombadil, Rosie Cotton, Palantír |
| **2 — Possible** | Nice-to-have, cut first if space is tight | Flavor text, card name reference | Bill Ferny, Butterbur, Barrow-wights |
| **1 — Backup** | Include only if nothing better exists for a slot | Deep-cut flavor text | Minor named locations, background events |

### Rating methodology

Rate each element using multiple inputs:
1. **Internal fan assessment** — team members who know the IP well
2. **IP partner input** — what does the rights holder consider essential?
3. **External fan data** — popularity polls, "most wanted" community threads, cosplay frequency, merchandise sales
4. **Cross-media presence** — does this element appear in adaptations, sequels, merchandise? If so, it's more widely known

### Must-include list

Extract all Tier 5 elements into a dedicated must-include list. This typically numbers **30-50 elements** for a full set (~261 cards). These are non-negotiable — if a must-include element is missing from the final set, fans will notice and complain (the Riot Test).

---

## Knowledge Pyramid

The knowledge pyramid determines how IP references are distributed across rarities.

```
        /\
       /  \  Top tier: deep cuts (die-hard fans)
      /    \  → uncommon, flavor text, card name references
     /──────\
    /        \  Middle tier: dedicated fans know
   /          \  → rare and uncommon slots
  /────────────\
 /              \  Bottom tier: everyone with basic awareness knows
/                \  → mythic and rare, maximum visibility
──────────────────
```

### Distribution rules

| Pyramid tier | Rarity placement | Card treatment |
|-------------|-----------------|----------------|
| Bottom (universally known) | Mythic, rare | Multiple versions for characters; standalone Sagas for story moments; Equipment for iconic items |
| Middle (fan-recognized) | Rare, uncommon | Single version for characters; spell art for moments; flavor text references |
| Top (deep cuts) | Uncommon, flavor text | Easter eggs that reward expert fans; referenced in names/art, not as their own card |

### The zero-generic-card standard

From LotR: every single card had an identifiable root in the source material. No card existed purely as mechanical filler. Even common creatures used IP-specific names, creature types, and flavor text. A common 2/2 soldier isn't "Gondorian Soldier" — it's "Guard of the Citadel" with Tolkien flavor text.

### Deep-cut budget

Deep cuts (Tier 2–3 elements in the 5-tier system, Top-tier in the knowledge pyramid) must be budgeted explicitly, not treated as leftovers.

- **Minimum: 15% of the set must represent deep cuts.** In a 261-card set that is ~40 cards worth of deep-cut representation. Target 15–25%.
- **What counts toward the budget:** standalone cards at uncommon/common (~40% of the budget), flavor-text callouts on otherwise mid-tier cards (~40%), and art/card-name cameos (~20%). A deep cut does not have to consume a full card slot.
- **Where deep cuts live:** uncommon and common. Almost never rare or mythic — those slots belong to Tier 5 mandatories. Deep cuts at rare are invisible to casual players and feel overcosted to fans.
- **Research intensity:** expect to spend *more* research time per deep cut than per must-include. Must-includes identify themselves; deep cuts require wiki diving, fan-poll review, and interview/behind-the-scenes research.
- **Protection during cuts:** when Phase 4 (set design) needs to trim cards, do not raid the deep-cut budget to make room for another version of a Tier 5 character. A third protagonist card adds less fan value than the only deep-cut card in the set.

---

## Color Pie Mapping Guide

### The philosophy-first principle

Map characters and factions to colors through their **values, motivations, and methods** — not their powers or aesthetics.

| Color | Map characters who value... | NOT characters who... |
|-------|-----------------------------|----------------------|
| **White** | Order, community, law, protection, selflessness, hierarchy | ...wear white or use light-based powers |
| **Blue** | Knowledge, perfection, progress, logic, patience, technology | ...are blue-skinned or use water magic |
| **Black** | Power, ambition, self-interest, pragmatism, willingness to pay any price | ...are villains or wear dark clothing |
| **Red** | Freedom, emotion, impulse, passion, action, chaos | ...use fire or have red coloring |
| **Green** | Nature, tradition, instinct, growth, acceptance, community | ...live outdoors or are animals |

### Multi-version color shifting

The same character at different story moments may have different colors:
- Gandalf the Grey (UR) → Gandalf the White (W) — philosophy shifted from cunning/impulsive to authoritative/protective
- Sephiroth, Fabled SOLDIER (front, certain colors) → One-Winged Angel (back, different colors)

When cataloging characters with transformative arcs, note the color shift and which story moment each version represents.

### The Green Problem

Green is underrepresented in almost every IP. Proactively identify:
- Nature-connected characters (druids, rangers, farmers, animal companions)
- Growth/evolution themes (leveling up, maturing, physically growing)
- Traditional/conservative factions (those who resist change, honor ancestry)
- Community-focused groups (villages, tribes, found-family units)
- Beast/animal creatures at various sizes
- Agricultural, forest, or wilderness settings

**If fewer than 15-20 elements map to green, flag this as a severe gap.**

### Color distribution audit

After mapping all catalog entries, compute:

| Color | Character count | Faction coverage | Creature count | % of total |
|-------|----------------|-----------------|----------------|-----------|
| W | | | | |
| U | | | | |
| B | | | | |
| R | | | | |
| G | | | | |
| Multicolor | | | | |
| Colorless | | | | |

Flag any color below 15% or above 30% of total catalog entries.

---

## Catalog Templates

### Character Catalog

For each character:

```markdown
### [Character Name]
**IP role:** [protagonist / antagonist / supporting / minor]
**Tier:** [5/4/3/2/1]
**Proposed color(s):** [WUBRG with reasoning]
**Iconic abilities/traits:** [what this character is known for]
**Visual description:** [appearance for art direction]
**Story importance:** [why this character matters to the IP]
**Card version(s):** [how many cards, at which story moments]
**Suggested rarity:** [mythic / rare / uncommon]
**Mechanical hook:** [what the card should feel like]
```

### Faction Catalog

For each faction/organization:

```markdown
### [Faction Name]
**Description:** [what this group is and does]
**Color alignment:** [WUBRG with philosophy-based reasoning]
**Key members:** [characters from the character catalog]
**Mechanical archetype potential:** [what Limited strategy this maps to]
**Creature types:** [MTG creature types that fit this faction]
**Visual identity:** [signature look, colors, symbols]
```

### Location Catalog

For each iconic location:

```markdown
### [Location Name]
**Description:** [what this place is]
**Associated characters:** [who is found here]
**Visual identity:** [what it looks like]
**Card type suggestion:** [legendary land / basic land art / spell setting]
**Tier:** [5/4/3/2/1]
```

### Item Catalog

For each weapon, artifact, or significant object:

```markdown
### [Item Name]
**Description:** [what it is and does]
**Owner/origin:** [who uses it, where it comes from]
**Card type suggestion:** [Equipment / Artifact / Enchantment]
**Mechanical effect suggestion:** [what it should do as a card]
**Tier:** [5/4/3/2/1]
```

### Story Beat Catalog

For each iconic moment/event:

```markdown
### [Story Beat Name]
**Description:** [what happens]
**Participants:** [which characters are involved]
**Emotional weight:** [why this moment matters]
**Card type suggestion:** [Saga / Instant / Sorcery / Enchantment]
**Tier:** [5/4/3/2/1]
```

---

## Scope Management

### For single-narrative IPs (one story, one cast)

Examples: Lord of the Rings, Harry Potter, The Princess Bride

- Scope is natural — the story defines the boundaries
- Catalog the full narrative; let the tier system handle prioritization
- Multiple versions of main characters show different story moments

### For multi-installment IPs (series of related stories)

Examples: Final Fantasy (16 games), Fallout (multiple games), Doctor Who (60+ years)

**The audience-era approach (Doctor Who model):** Divide by when fans started engaging, not by in-universe chronology. Each era gets its own mechanical identity.

**The breadth-with-anchors approach (Final Fantasy model):** Franchise-wide elements (Chocobos, Moogles, summons) form 30% of the set. Each installment gets targeted representation. Commander precons focus on the most popular installments.

**The scope question to ask the user:**
- "All installments or a specific subset?" (e.g., "FF7 only" vs. "all 16 mainline games")
- "Core story only or expanded universe?" (e.g., "original trilogy" vs. "including The Hobbit")
- "Which installments does the fanbase love most?" (prioritize those)

### For multi-era IPs (spanning historical periods)

Examples: Assassin's Creed, Doctor Who

Map each IP era to an existing Magic plane archetype as a conceptual anchor:
- Classical Greece → Theros
- Norse mythology → Kaldheim
- Egyptian setting → Amonkhet
- Renaissance Italy → Fiora/Ravnica
- Victorian era → Innistrad

This helps downstream designers understand the visual and tonal vocabulary for each era.

---

## Naming Convention Extraction

Each IP has distinctive naming patterns. Document these for downstream use by Creative Writer and Art Director.

### What to capture

| Element | What to document | Example (LotR) |
|---------|-----------------|-----------------|
| **Character naming pattern** | Cultural roots, syllable patterns, title conventions | Elvish names use Sindarin/Quenya roots; Hobbits use English pastoral names; "Name, Title" format |
| **Location naming pattern** | Language roots, compound conventions | Sindarin compounds (Minas Tirith = "Tower of Guard"); English for Shire locations |
| **Terminology** | IP-specific vocabulary that should appear on cards | "Middle-earth," "Mithril," "Palantír," not "continent," "magical metal," "seeing stone" |
| **Linguistic register** | Formal/informal, archaic/modern, technical/natural | Tolkien: archaic, formal. Fallout: retro-futuristic Americana. Warhammer: gothic Latin |
| **Flavor text voice** | Direct quotes vs. original in IP voice | LotR: exclusively Tolkien quotes. Warhammer: mix of quotes and original grimdark prose |

### Flavor text strategy decision

Choose one based on the IP's literary tradition:

| IP type | Strategy | Reasoning |
|---------|----------|-----------|
| Strong literary tradition with beloved prose | Direct quotes heavily | Fans revere the original text (LotR) |
| Iconic catchphrases but limited prose | Mix quotes with original in IP voice | Use what exists, fill gaps authentically (Warhammer) |
| Primarily visual/interactive (games, animation) | Original text using IP terminology and tone | Games have less quotable prose (Fallout, Final Fantasy) |

---

## System Translation Inventory

When the IP is a game, its interactive systems are prime candidates for mechanical translation.

### Template

| Source System | MTG Translation Candidate | Confidence | Notes |
|--------------|--------------------------|------------|-------|
| [IP system] | [proposed MTG mechanic] | [high/medium/low] | [why this translation works or doesn't] |

### Successful translations as reference

| IP | Source System | MTG Translation |
|----|-------------|-----------------|
| Fallout | VATS (time pause) | Split Second |
| Fallout | Bottle caps (currency) | Treasure tokens |
| Fallout | Radiation (persistent damage) | Rad counters |
| Fallout | Junk items | Junk tokens (sacrifice for card advantage) |
| Final Fantasy | Summons (multi-phase call) | Saga Creatures |
| Final Fantasy | Job system | Job Select Equipment |
| Final Fantasy | Leveling up | Tiered mechanic (kicker variant) |
| Doctor Who | Time travel | Time counters / Suspend variant |
| Doctor Who | Doctor-companion pairing | Doctor's Companion (partner variant) |
| Warhammer 40K | Military formations | Squad (enter with copies) |
| Warhammer 40K | Tyranid consumption | Ravenous (ETB counters based on mana paid) |

### Priority rule

Flag only the 2-3 most iconic systems for priority translation. Downstream designers have a limited complexity budget (~3 new mechanics at common). Catalog all translatable systems but mark which ones are essential vs. optional.

---

## Constraint Document Template

The `ip_constraints.md` companion document tells Vision Design what's locked. Use this structure:

```markdown
# IP Constraints: [IP Name]

## Scope
[What parts of the IP are in scope — which games/books/seasons/eras]

## Must-Include List (Tier 5 Elements)
[30-50 elements that MUST appear in the final set]

### Must-Include Characters
[List with proposed colors and rarity]

### Must-Include Items/Locations/Moments
[List with proposed card types]

## Color Pie Distribution
[The color audit table showing current distribution and gaps]

### Color Gaps
[Which colors are underrepresented and by how much]

### Compensation Suggestions
[Ideas for filling color gaps without breaking IP fidelity]

## Locked Flavor Elements
[Things that CANNOT be changed because the IP defines them]
- Character names (canonical, non-negotiable)
- Character relationships (cannot be altered)
- Visual appearances (must match IP)
- Signature abilities (characters must feel like themselves)

## Flexibility Zones
[Where Vision Design HAS creative freedom]
- Power level tuning
- Which story moment each character card represents
- Mechanical implementation of flavor concepts
- Creature type assignments (within reason)
- How to fill color gaps

## Naming Conventions
[Summary of the IP's naming patterns for Creative Writer]

## Flavor Text Strategy
[Which approach: direct quotes / mixed / original in IP voice]

## System Translation Candidates
[Top 2-3 IP systems flagged for mechanical translation]

## Product-Audience Notes
[Which Magic formats the IP's audience likely gravitates toward]
[Commander vs. Standard vs. Draft considerations]

## Tone Assessment
[How well the IP's tone fits Magic's fantasy frame — and any risks]

## Reprint Potential
[Assessment of how many existing Magic cards could be reprinted with IP re-skinning]
```
