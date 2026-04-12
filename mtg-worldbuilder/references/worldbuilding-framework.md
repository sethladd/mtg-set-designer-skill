# Worldbuilding Framework

Canonical reference tables and design frameworks for inventing Magic: The Gathering planes. Read this before building any world. Use the templates as starting structures and the guidelines as constraints.

---

## Table of Contents

1. [World Argument Framework](#world-argument-framework)
2. [Faction Design Principles](#faction-design-principles)
3. [Creature Type Mapping Guide](#creature-type-mapping-guide)
4. [Visual Identity Checklist](#visual-identity-checklist)
5. [Character Density Targets](#character-density-targets)
6. [Geography Template](#geography-template)
7. [Archetype-to-Faction Mapping](#archetype-to-faction-mapping)

---

## World Argument Framework

Every great Magic plane makes an argument — a thesis about how the world works that generates every other creative decision. The argument is not a tagline; it is the structural principle from which factions, conflicts, geography, and visual identity emerge.

### Template

> On **[plane name]**, **[thesis about how this world works]**.

### Real examples

| Plane | World Argument | What it generates |
|-------|---------------|-------------------|
| Innistrad | Fear is a resource — the monsters feed on it, the humans weaponize it | Five monster tribes (Vampires, Werewolves, Zombies, Spirits, Humans), gothic visual identity, graveyard mechanics |
| Ravnica | Civilization requires guild-based governance — ten guilds divide all of society's functions | Ten two-color guilds, urban visual identity, guild mechanics as keywords |
| Zendikar | The land itself is alive and dangerous — adventure means surviving the terrain | Landfall mechanic, hedron visual identity, exploration/adventure tropes |
| Theros | Belief shapes reality — the gods exist because mortals believe in them | Devotion mechanic, enchantment creatures, Nyx visual identity |
| Kaladesh | Invention is art — aether powers creation, and creation is beautiful | Energy/artifact mechanics, filigree visual identity, optimistic tone |
| Eldraine | Fairy tales are real but have consequences — every story has a dark side | Adventure mechanic, Arthurian + fairy tale resonance, storybook visual identity |

### Argument quality test

A strong argument naturally produces:
- **Factions**: Different groups who relate to the argument differently (Innistrad: those who feed on fear vs. those who fight it)
- **Conflicts**: Inherent tensions arising from the argument (Ravnica: what happens when guilds disagree?)
- **Visual identity**: A look that expresses the argument (Theros: starfield patterns = divine presence)
- **Mechanics**: Gameplay that embodies the argument (Zendikar: Landfall = the land matters)

If the argument doesn't generate at least three of these four naturally, it needs sharpening or broadening.

---

## Faction Design Principles

### The four requirements (from Rosewater's "Faction Packed")

Every faction needs ALL FOUR of these. Missing any one produces a failing faction:

1. **Mechanical identity** — A keyword, mechanic, or play pattern that is uniquely theirs
2. **Creative identity** — A name, visual aesthetic, creature types, and philosophy that distinguishes them
3. **Relational definition** — Their relationships with other factions (ally, rival, trading partner, enemy) define the set's social fabric
4. **Emotional resonance** — Playing the faction should evoke a specific feeling (aggression, control, wonder, dread)

### Faction count targets

| Factions | Cards per faction (~270 card set) | Assessment |
|----------|----------------------------------|------------|
| 2 | ~135 | Deep but limited variety (e.g., Mirrodin vs. Phyrexia in Scars block) |
| 3 | ~90 | Very deep, good for strong triangular conflict |
| 4 | ~67 | Deep enough for mechanical identity; needs cross-faction glue (Ixalan's failure point) |
| 5 | ~54 | Sweet spot for most sets (Innistrad, Tarkir, Strixhaven) |
| 10 | ~27 | Only works if each faction is built on a two-color pair with inherent clarity (Ravnica). Typically split across 2+ sets. |

**Default recommendation: 3-5 factions.** Only exceed 5 if the world's argument demands it and you're willing to show a subset per set.

### Faction-to-color mapping

Each faction maps to one or two colors. The mapping must satisfy:

- **All five colors** are represented across all factions (no orphaned colors)
- **All ten two-color pairs** are covered by the archetype grid (even if some pairs are overlaps between factions rather than their own faction)
- **Philosophy matches color pie values** — a faction's beliefs must align with its colors' philosophical identity, not just its aesthetic. Map through philosophy, not aesthetics. (A "dark" faction is not automatically black. A "nature" faction is not automatically green.)

### Color pie philosophical mapping

| Color | Core values | Faction archetypes that fit |
|-------|------------|---------------------------|
| White | Order, community, law, protection, peace through structure | Military organizations, religious orders, civic governments, healer guilds |
| Blue | Knowledge, perfection, progress, logic, technology | Academic institutions, research guilds, artificer collectives, spy networks |
| Black | Power, ambition, self-interest, pragmatism, willingness to pay any price | Criminal organizations, necromancer cabals, merchant guilds, political schemers |
| Red | Freedom, emotion, impulse, chaos, passion, destruction/creation | Revolutionary movements, artistic communities, nomadic bands, berserker clans |
| Green | Nature, tradition, instinct, growth, acceptance of the natural order | Druidic circles, tribal societies, beast-bonded communities, growth cults |

### Cross-pollination design

For each faction, identify at least one element it shares with an adjacent faction:

- **Shared creature types**: Humans in Innistrad appear in all five colors. Bridge types connect factions.
- **Shared mechanics**: Blue's self-mill in Innistrad serves both UB Zombies and UG Flashback.
- **Shared geography**: Two factions occupying overlapping territory forces interaction.
- **Shared resources**: A resource both factions want creates conflict and draft flexibility.

### Faction relationship matrix template

| | Faction A | Faction B | Faction C | Faction D | Faction E |
|--|-----------|-----------|-----------|-----------|-----------|
| Faction A | — | [ally/enemy/rival/neutral] | | | |
| Faction B | | — | | | |
| Faction C | | | — | | |
| Faction D | | | | — | |
| Faction E | | | | | — |

For each relationship, write one sentence explaining WHY (rooted in the world argument).

---

## Creature Type Mapping Guide

### The creature-type-to-color matrix

This table maps which creature types appear in which colors and at what density. It is the bridge between worldbuilding and gameplay.

| Density | Cards in set | Meaning |
|---------|-------------|---------|
| **Primary (P)** | 3-5+ cards | This type is a core part of this color's identity in this set |
| **Secondary (S)** | 1-3 cards | This type appears but isn't central |
| **Tertiary (T)** | 1 card | Splash appearance, often at uncommon or rare |

### Design guidelines

1. **Every color needs 2-3 primary creature types** — these define what the color "is" in this world
2. **At least 2 "bridge types" must span 3+ colors** — these enable cross-faction drafting (e.g., Humans in Innistrad)
3. **Prefer existing creature types over invented ones** — players connect with familiar types. Consult the full 328-type catalog in `references/card-types.md`
4. **Creature type density must match faction identity** — if Vampires are your BW faction, the BW archetype needs enough Vampire cards at common/uncommon to draft reliably
5. **Consider a joiner type if tribal is tight** — Lorwyn's Changeling (counts as every creature type) prevented tribal payoffs from being too parasitic. If your creature types are narrowly distributed, consider whether you need a joiner

### Bloomburrow mapping as reference model

The most recent and deliberate creature-type-to-color mapping (2024):

| Color Pair | Creature Type | Why this assignment |
|-----------|--------------|-------------------|
| WU | Bird | Historically flying-focused in these colors |
| UB | Rat | Rogues/cunning maps to UB identity |
| BR | Lizard | Cold-blooded aggression fits BR |
| RG | Raccoon | Resourceful scrappiness fits RG |
| GW | Rabbit | "Go-wide" token strategy fits GW |
| WB | Bat | Flying + lifedrain fits WB |
| UR | Otter | Playful trickster/spells-matter fits UR |
| BG | Squirrel | Hoarding/recursion fits BG |
| RW | Mouse | Small heroes/equipment fits RW |
| GU | Frog | Growth/evolution fits GU |

Three selection criteria used:
1. Historical color identity of the creature type in existing Magic
2. Creature type availability (enough design space for 20+ cards)
3. Thematic fit between animal personality and color pair identity

---

## Visual Identity Checklist

### The through-line motif

Every world needs ONE visual motif that appears across all factions, in all regions, at all rarities. This is the "visual argument" — the image equivalent of the world argument.

**Requirements:**
- Describable in one phrase (passes the Hedron Test)
- Connected to the world's core concept (not arbitrary decoration)
- Expressible differently in each faction (the same motif, faction-flavored)
- Visible at card scale (not fine detail that disappears when printed)

**Examples:**

| Plane | Through-line motif | Why it works |
|-------|-------------------|-------------|
| Zendikar | Floating stone hedrons | Hedrons = ancient mystery civilization, inseparable from the world's concept |
| Kaladesh | Filigree brass metalwork | Filigree = invention as art, derived from jewelry not steampunk |
| Innistrad | Gothic arches + fog | Gothic architecture = civilization haunted by darkness |
| Theros | Nyx starfield patterns | Starfield = divine presence woven into the mortal world |
| Mirrodin | Hexagonal metallic surfaces | Metal landscape = artificial world |

### Set palette

Define these for the world:

| Element | What to specify |
|---------|----------------|
| **Sky** | Color, time of day, celestial bodies (two suns? perpetual twilight? aurora?) |
| **Dominant materials** | Stone, metal, wood, crystal, bone, living matter, etc. |
| **Light sources** | Sunlight, moonlight, bioluminescence, arcane glow, firelight, etc. |
| **Recurring shapes** | Geometric, organic, fractal, angular, flowing, etc. |
| **Color palette** | Warm/cool dominant, accent colors, per-faction color shifts |

### Per-faction visual variants

Each faction should express the world's through-line in its own way:

> **Example (Kaladesh filigree):**
> - Consulate: precise, symmetrical filigree in government buildings
> - Inventors: experimental, asymmetrical filigree in personal devices
> - Aetherborn: decorative filigree worn as personal adornment
> - Gremlins: broken/stolen filigree repurposed destructively

For art direction details, see `references/art-direction.md`.

---

## Character Density Targets

### Named characters per rarity

Based on analysis of successful modern sets (Innistrad, Ravnica, Eldraine, Bloomburrow):

| Rarity | Named characters | Role |
|--------|-----------------|------|
| Mythic rare | 3-6 | Protagonists, main villains, planeswalkers — the "poster" characters |
| Rare | 8-15 | Major supporting cast, faction leaders, secondary antagonists |
| Uncommon | 5-10 | Minor but recognizable figures, signpost uncommons (gold legendary creatures announcing each archetype) |
| Common | 0-2 | Almost never named; commons reference characters in flavor text instead |

**Total: ~15-25 named characters** for a modern in-universe premier set (trend is toward the lower end after legendary density inflation in 2022-2024).

### Character requirements

Each named character must have:
- **Name** (following the world's naming culture)
- **Faction** (which group they belong to)
- **Color identity** (1-3 colors matching their faction and personality)
- **Role in world** (their position, authority, goals)
- **Mechanical hook** (what the card should feel like — e.g., "rewards controlling many creatures")
- **At least one relationship** (ally, rival, mentor, enemy) with another character

### Character distribution rules

- Characters must span at least 3 different factions (not all from one faction)
- At least one character from every major faction
- At least one character who bridges or exists between factions (gray zone character)
- Protagonist and antagonist should be in different (ideally enemy) colors

---

## Geography Template

### Region structure

Define 3-5 major geographic regions, each associated with a faction or color.

For each region:

```markdown
### [Region Name]
**Terrain:** [landscape description — forests, caves, floating islands, etc.]
**Associated faction/color:** [which faction dominates or inhabits this region]
**Visual palette:** [dominant colors, materials, lighting specific to this region]
**Key landmarks:** [2-3 named locations that could be legendary lands or referenced in card art]
**Inhabitants:** [creature types found here]
**Mood/atmosphere:** [the feeling of being in this place]
```

### Geography design principles

- **Each region should be visually distinct** — a player should be able to identify the region from a card's art
- **Regions should border each other meaningfully** — border zones create faction interaction and gray zones
- **At least one region should be contested territory** — geography drives conflict
- **Landmark names become card names** — choose evocative names that work as land card titles

---

## Archetype-to-Faction Mapping

### The ten two-color archetype grid

Every Magic set needs ten two-color draft archetypes. In a faction-based set, each archetype maps to a faction, a faction overlap, or a sub-theme.

### Template

| Color Pair | Faction / Overlap | Archetype Strategy | Signature Creature Types | Signpost Design Direction | Visual Notes |
|-----------|------------------|-------------------|------------------------|--------------------------|-------------|
| WU | | | | | |
| WB | | | | | |
| WR | | | | | |
| WG | | | | | |
| UB | | | | | |
| UR | | | | | |
| UG | | | | | |
| BR | | | | | |
| BG | | | | | |
| RG | | | | | |

### Mapping rules

With 5 factions (each owning a color pair), you get 5 "core" archetypes directly owned by factions. The other 5 archetypes are "overlap" pairs — combinations of elements from adjacent factions.

**Core archetype** (faction-owned): Has its own faction identity, keyword mechanic, and dedicated signpost uncommon.

**Overlap archetype** (between factions): Borrows elements from two adjacent factions. The overlap archetype should feel like a natural blend, not a forced combination. This is where cross-pollination pays off — if factions share creature types or mechanics, the overlap archetypes draft smoothly.

### Speed distribution

The ten archetypes should span gameplay speeds:

| Speed | Archetypes | Characteristics |
|-------|-----------|----------------|
| Aggro (fast) | 2-3 | Low curve, cheap creatures, combat tricks |
| Midrange | 3-4 | Balanced curve, value creatures, removal |
| Control (slow) | 2-3 | High curve, card advantage, removal-heavy |
| Synergy/Combo | 1-2 | Build-around payoffs, engine-based |

Avoid making all archetypes the same speed — a format where everything is midrange is boring; a format where aggro doesn't exist punishes interaction.

For detailed archetype design guidance, see `references/archetypes.md`.
