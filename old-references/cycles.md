# Cycles

A cycle is a group of cards that share a template and vary along some axis — usually color. Cycles are a cheap way to make a set feel cohesive, to teach players your mechanics in parallel across colors, and to fill rarity slots in a structured way. They also become crutches if overused. Design rule: use cycles when they earn their keep, not just to hit a count.

## Types

**Five-card color cycle.** One card per color. The classic cycle. Titans, Commands, Charms, the "hate cards" against each color, basic creature-type lords, the five-color signpost creatures. These work because each card is the color's take on the same idea.

**Ten-card pair cycle.** One card per two-color pair. The Ravnica signets. Dual lands. Guildmages. The ten signpost uncommon enablers and the ten signpost uncommon payoffs. Designing ten cards that are templatically similar but mechanically distinct is twice as much work as designing five, not just 2x — it's something like 3x because the ten cards have to avoid stepping on each other's toes while still belonging to the same cycle.

**Five-card wedge/shard cycle.** One card per three-color combination. Rare in normal sets; common in sets about three-color combinations (Shards of Alara, Khans of Tarkir).

**Rarity cycle.** The same design at different rarities — common → uncommon → rare, each better than the last. Useful for teaching newer drafters how power scales.

**Mechanic cycle.** One card per color (or per pair) all showcasing a new mechanic. The clearest way to introduce a mechanic in a set where the mechanic needs to feel pan-color.

## When cycles earn their keep

- When the set needs to telegraph that something is *symmetric* across colors or pairs. Dual lands cycle because duals are the same idea in every pair.
- When teaching a mechanic. A five-card cycle at common where each card is a minimal expression of the new mechanic helps the mechanic land in players' heads.
- When filling slots in a structured way at uncommon or rare. If you need twenty uncommons in a specific niche and ten of them can be a pair cycle, that's efficient.
- When building a thematic "cast" (the five Gods of Theros, the ten Guildmages of Ravnica). These become iconic.

## When cycles hurt

- When they're forced to exist. A five-card cycle where one of the five cards is clearly worse than the others because the color couldn't support the template is a failed cycle — the weakest card will be unplayable and the whole cycle feels compromised.
- When they replace unique design. If your set's commons are mostly cycles, drafters learn the set in a pack and then have nothing to discover.
- When they eat color-identity slots. A gold ten-card cycle is appealing but it uses up ten of your uncommon gold slots, which might be better spent on varied archetype signposts.

## Cycle sanity checks

When you design a cycle, apply these:

- Does each member pull weight *in its color*? A cycle member whose color can't actually use the effect has failed — either the color is wrong or the effect doesn't belong in a cycle.
- Is there power variation? Some cycles want the same power level; some want the weakest to be weak and the strongest to be the color's specialty. Pick one and be explicit.
- Does the cycle step on the color pie? A five-card cycle that gives every color a universal effect is bending the pie hard — that might be fine once or twice in a set, but not three times.
- Does the cycle use up a slot another card could have used better? Opportunity cost is real.

## Cycles and the balance check

The balance script doesn't know what's a cycle; it just sees cards. But it will catch the common failure mode — the weakest member of a forced cycle shows up as "underplayed" in the draft sim. If you see a cycle where one member is hitting ~2% play rate while the others hit ~20%, either fix the weak member or break the cycle and let it be four cards instead of five.
