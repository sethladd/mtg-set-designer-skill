# The Design Skeleton

The design skeleton is the slot-by-slot blueprint for a Magic set. Mark Rosewater introduced it in his "Nuts & Bolts" series — article #13 (2021) covered it for Draft Boosters, and **#16 (2024) updated it for Play Boosters**. The skill's `references/design_skeleton.json` contains the Play Booster version.

## What the skeleton is

A skeleton assigns every card in the set a **slot code** (like `CW01`, `UB05`, `RG03`) that identifies:

- **Rarity** — `C`ommon, `U`ncommon, `R`are, `M`ythic
- **Color** — `W`hite, `U`(blue), `B`lack, `R`ed, `G`reen, `A`rtifact/colorless, `M`ulticolor
- **Number** — sequential within that rarity+color bucket

Each slot also carries:

- **Mana value** — the CMC this card should cost (a range like "2–3" means pick one)
- **Type** — creature, removal, trick, card draw, etc.
- **Notes** — what role this card fills (e.g., "aggressive 1-drop," "unconditional kill spell," "signpost payoff for WU")

The skeleton does *not* contain names, flavor text, or rules text. Those come from the designer.

## Why it matters

Without a skeleton, designers tend to:

1. **Clump mana curves** — writing too many 3-drops and too few 1-drops or 6-drops
2. **Forget removal** — exciting mechanics crowd out the boring but essential removal spells
3. **Under-support archetypes** — designing cool signpost uncommons but not the commons that make the archetype draftable
4. **Break color balance** — giving one color 18 commons while another gets 12

The skeleton prevents all of this by making the structural requirements visible *before* you start writing card text. It is essentially a checklist that guarantees you hit every target the balance checker will later verify.

## Play Booster era slot counts

The Play Booster skeleton (2024+) differs from the old Draft Booster skeleton:

| Rarity | Old (Draft) | New (Play) | Key change |
|--------|-------------|------------|------------|
| Common | 101 | **81** | Fewer but higher-impact; no filler |
| Uncommon | 80 | **100** | Largest rarity; carries heavy archetype support |
| Rare | 53 | **60** | Slight increase |
| Mythic | 15 | **20** | Slight increase |

### Commons per color (81 total)

| Color | Creatures | Noncreatures | Total |
|-------|-----------|--------------|-------|
| W | 11 | 4 | 15 |
| U | 8 | 7 | 15 |
| B | 9 | 5 | 14 |
| R | 9 | 5 | 14 |
| G | 10 | 4 | 14 |
| Colorless/Artifact | 4 | 5 | 9 |

### Uncommons per color (100 total)

Each color gets ~16–18 mono-color uncommons. On top of those, there are **20 multicolor signpost uncommons** (2 per two-color pair: one enabler, one payoff) plus ~13 colorless utility slots. Uncommons now do much of the work that commons used to do for archetype support.

### Rares and mythics

60 rares (~10–12 per color + gold + lands) and 20 mythics (~3–4 per color + gold + planeswalkers). These are less tightly templated — the skeleton provides slot counts but leaves more creative freedom.

## How to use the skeleton in Phase 5

When Phase 5 (Card File) begins:

1. **Load the skeleton** from `references/design_skeleton.json`.
2. **Walk through commons color by color.** For each slot (CW01, CW02, ...), design a card that fits the slot's mana value, type, and notes. The notes tell you what *role* the card fills — your job is to express that role through the set's theme, mechanics, and flavor.
3. **Respect the keyword guidelines.** Each color section includes a `keywords` field listing roughly how many creatures should have each evergreen keyword. For example, white gets 2–3 flyers at common. This is a guideline, not a law — but if you deviate significantly, document why.
4. **Fill uncommons the same way**, paying special attention to the 20 multicolor signpost slots. These are the cards from your archetype grid (Phase 4) — the skeleton just reserves space for them.
5. **Rares and mythics** have fewer constraints from the skeleton. Use the slot counts to ensure color balance, but the specific designs come from your vision and mechanics.

### Mapping skeleton slots to set.json

When writing `set.json`, include the skeleton slot code in each card's `id` field (or a separate `skeleton_slot` field). This makes it easy to verify completeness — every slot in the skeleton should map to exactly one card in the set.

Example:
```json
{
  "id": "CW01",
  "name": "Watchfire Sentinel",
  "mana_cost": "{W}",
  "cmc": 1,
  "color": ["W"],
  "type": "Creature",
  "subtypes": ["Human", "Soldier"],
  "power": 2,
  "toughness": 1,
  "rules_text": "",
  "rarity": "common",
  "archetypes": ["WR", "WB"],
  "keywords": [],
  "notes": "Aggressive 1-drop per skeleton CW01"
}
```

## The skeleton is a starting point, not a straitjacket

The skeleton represents the *typical* structure of a set. Real sets deviate from it all the time — a set with a graveyard theme might trade a blue common counterspell slot for a self-mill card, or a set with an artifact subtheme might shift colorless common slots around. The point is to start from a known-good structure and deviate *intentionally*, not accidentally.

When you deviate, note it. The balance checker will catch structural anomalies either way, but documenting your reasoning in the design doc makes it easier to tell the difference between "deliberate choice" and "oops, forgot a removal spell."

## The CSV backup

`references/design_skeleton_2021.csv` contains the community-maintained "Bones" spreadsheet (by Wobbles) based on Nuts & Bolts #13. It uses the older Draft Booster counts (101 commons, 80 uncommons) and is kept as historical reference. **Always use `design_skeleton.json` for new sets** — it has the current Play Booster numbers.
