# New World Order

In 2006 Wizards looked at their data and noticed that new players were bouncing off Magic because the game had become too complex to enter. The solution — instituted quietly at first, then named publicly in 2011 — is called **New World Order**. It is the single most important constraint on how commons get designed.

## The principle

Treat common complexity as a finite, scarce resource. Keep the *comprehension* and *board* complexity at common low, and push the strategic complexity (and the complicated mechanics) to uncommon and higher. The goal is that a brand-new player can understand almost every common in a pack on the first read, even if they can't yet tell which commons are strong.

The reason this matters: most of a booster pack is commons. If commons are dense and confusing, the first-time player drowns. If commons are clean, the first-time player can play a game and actually have a shot at enjoying it, while the experienced player still gets depth at uncommon and above.

## The three complexities

Rosewater splits complexity into three types, which matters because they trade off differently:

**Comprehension complexity.** How hard the card is to read and understand. "Deal 2 damage to any target" is low. "Whenever you cast a noncreature spell, if you control a creature with power 3 or greater, create a 1/1 token" is high.

**Board complexity.** How much mental effort the card's presence on the battlefield adds to every turn. A creature with a triggered ability that fires on opponents' spells adds board complexity even if its text is short, because every opponent action requires checking the trigger.

**Strategic complexity.** How hard the card is to play *well*. This is usually invisible to beginners — they don't know what they don't know — so strategic complexity is basically free to add. A lenticular card with a simple top-half and a deep skill-testing bottom-half spends zero comprehension complexity and rewards experts.

New World Order targets *comprehension* and *board* complexity at common. Strategic complexity is fine everywhere.

## The red-flag rule

Flag a common as "complex" if it meets any of these conditions:

- Has more than one ability (barring evergreen keywords like flying or first strike paired with a simple effect).
- References a mechanic the player can't evaluate by reading the card alone.
- Requires the player to track state across turns.
- Has a triggered ability that fires during the opponent's turn (adds board complexity).
- Has rules text longer than three lines.
- Uses a new named mechanic (these count toward the red-flag budget automatically).

**Target: no more than ~20% of commons should be red-flagged.** In a set with ~100 commons, that's 20 red-flag commons. Most should be clean, simple bodies and effects — the vanillas, French vanillas, and one-line utility spells that make the format legible.

Every red-flagged common should be making an important contribution. If it's red-flagged and it's also just a generic effect, unflag it by simplifying it.

## What counts as simple

A 2/2 creature for 2 mana with no abilities is simple. (A vanilla.) It's also *boring*, which is why sets can't be all vanillas — but they need some, and modern designers have gotten better at not apologizing for them.

A 2/2 creature for 2 mana with flying is simple. (A French vanilla.) Still extremely legible; the keyword is evergreen.

A 2/2 creature for 2 mana that becomes a 3/3 if you control another creature is on the edge — it's one conditional but it's a static effect, not a triggered one, and the condition is easy to check. Fine at common.

A 2/2 creature for 2 mana that triggers when you cast your second spell in a turn is not simple — it adds tracking state and a trigger in a non-obvious place. Probably should be uncommon.

## Lenticular design

The payoff for New World Order is lenticular design: cards that look simple on the top and are deep on the bottom. The classic example is Black Cat, which a new player reads as "small creature that makes opponent discard when it dies" but an experienced player reads as "sacrifice outlet enabler with death trigger value."

When you design a common, ask whether an expert and a novice would evaluate it differently. If yes, you've made a lenticular card. These are the best commons in the set — they teach the game while rewarding mastery. Aim for lenticularity wherever possible, especially on the support cards for each archetype.

## Applying it in the skill

`balance_check.py` tallies red-flagged commons automatically using the rules above. When it reports "24% red-flagged commons," either simplify some commons or move them to uncommon. It cannot do this automatically because the fix depends on which cards are load-bearing for archetypes, which is a judgment call.

When you choose which commons to simplify, prefer keeping the lenticular ones complex (they pay back the complexity with depth) and flattening the ones that are complex without being strategically interesting.
