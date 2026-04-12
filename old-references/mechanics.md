# Mechanics

Mechanics are the levers you pull to differentiate your set from every other set. They're also the easiest way to break a set, because a bad mechanic poisons every card it touches and warps the draft environment. Spend your complexity budget here carefully.

## Three kinds of mechanic

There is a rules-and-marketing hierarchy that matters:

**Keyword.** A named ability with a formal rules definition. "Flying." "Lifelink." "Bestow." Other cards can reference it by name, which makes it composable. Keywords are the most expensive kind of mechanic because they cost comprehension from every player. Use keywords for your big load-bearing ideas.

**Ability word.** An italicized label that groups similar abilities thematically but has *no rules weight*. "Landfall." "Raid." "Heroic." You can tell an ability word apart from a keyword by whether removing the label would change the card: if it wouldn't, it's an ability word. Ability words are cheap because they cost no new rules vocabulary — the card is just doing its thing, and the label is flavor.

**Named mechanic (no keyword, no ability word).** An effect that recurs in a recognizable shape with a marketing name. Devotion is like this: it has a definition but isn't a keyword in the usual sense. Prowess started as a named mechanic and was later promoted.

A set usually has **2–4 named new mechanics**. More than that is almost always a sign the designer couldn't decide. Each named mechanic buys you identity at the cost of complexity. Three is a comfortable number. Four stretches. Five is a warning.

Beyond those, your set uses evergreen keywords (flying, haste, lifelink…) as texture. These don't count against the "2–4 new mechanics" budget but they *do* matter: choose which evergreens the set emphasizes, because the mix of evergreens dramatically changes play feel.

## Parasitic vs. modular

This is the single most important distinction in mechanic design.

A **modular** mechanic works on its own. Landfall cares about lands, which every deck has. A creature with Landfall is playable in any deck that plays lands (all of them). A card with a modular mechanic pulls its weight whether or not the rest of your deck engages with the mechanic.

A **parasitic** mechanic needs other cards with the same or complementary mechanic to function. Splice-onto-Arcane (Kamigawa) required Arcane spells. If you didn't have Arcane spells in your deck, your Splice cards did nothing. This produced a draft environment where the "Splice deck" was a narrow corner of the format; players who ended up with one Splice card and no Arcane spells had a dead card.

Parasitism isn't always fatal. A strongly parasitic mechanic in *one color pair* can be the identity of that archetype — as long as the cards are clearly telegraphed as "draft these together or not at all" and there are enough of them in the right colors that the archetype is buildable in a normal draft pod. But the *default* for a new mechanic should be "works without support."

The test: imagine the mechanic is on one random card in a 45-card limited deck with no other cards that synergize with it. Is the card still playable? If yes, modular. If no, parasitic — and you need to either fix the card or own the parasitism deliberately.

## Complexity budget

Every mechanic spends some of the set's complexity budget. Spend is proportional to:

- How new the mechanic is (brand new > returning familiar)
- How many lines of rules text per card it adds
- How much it warps normal play patterns (stack interactions, replacement effects, unusual zones)
- How often it requires reminder text

The "New World Order" framework (see `new-world-order.md`) caps complexity at common especially hard. A new named mechanic should appear sparingly at common — usually on 4–8 commons across the set — and the common instances should be the *simplest possible version* of the mechanic. Save the weird interactions for uncommon and rare.

## Evergreen and deciduous keywords

Evergreens appear in basically every set: flying, first strike, double strike, deathtouch, defender, haste, hexproof (now mostly retired in favor of ward), indestructible, lifelink, menace, reach, trample, vigilance, ward.

Deciduous keywords appear when the set calls for them: flash, protection, prowess, scry, surveil, cycling, kicker, flashback, equip, convoke, etc.

Your set has to *choose* which of these to lean on. A set that emphasizes flying is a different set from one that emphasizes lifelink, even if the actual new mechanics are the same. Write this choice down in the design doc — "evergreen texture" — so it's deliberate rather than emergent.

## Returning mechanics

Bringing back an old mechanic is cheaper than inventing a new one, because players already know the rules. It's also flavorful — returning to Innistrad brought back Transform because the world demanded it. The downside is loss of novelty; if a set has *only* returning mechanics, it feels like a retread.

A typical standard set uses one or two returning mechanics and one or two new ones. Modern Horizons-style sets take more liberties with returning mechanics because their audience expects depth over accessibility.

## Writing the mechanic definition

For each mechanic, fill out the `mechanics.json` schema:

```
{
  "name": "Ember",
  "type": "keyword",
  "reminder_text": "Whenever this creature deals combat damage, create a Fire token.",
  "serves_pillar": "pillar 1: fire spreads between turns",
  "colors": {"primary": ["R"], "secondary": ["W", "G"], "tertiary": []},
  "rarity_spread": {"common": 6, "uncommon": 5, "rare": 3, "mythic": 1},
  "parasitic_risk": "medium - Fire tokens are used by other cards but also have intrinsic value",
  "design_space": "caring about whether your creatures connected; pushes combat-oriented play",
  "notes": "Ember should not appear at common alongside any other new named mechanic to respect NWO budget"
}
```

The `serves_pillar` field is a deliberate guardrail — if you can't name the pillar, the mechanic probably doesn't belong in the set. The `parasitic_risk` field forces you to think about playability in isolation before the card file grows.

## Common mechanic failure modes

**Too many new mechanics.** Dilutes every one. Players remember none. Draft becomes a puzzle of "which mechanic am I in" instead of a game.

**Mechanic with no home color pair.** If every color has a sprinkle, no archetype gets to *own* it, and the mechanic is flavor without strategic weight.

**Mechanic with only one home.** The opposite: the mechanic lives entirely in one archetype, and the other nine archetypes never see it. This is fine if the mechanic is small; dangerous if it's load-bearing.

**Stack interactions nobody playtested.** New triggered abilities in particular. If the mechanic creates a new timing question, write down the answer in the design doc and check it against existing rules, because rules team will ask later and "I didn't think about it" is not a reassuring answer.

**Reminder text longer than the card.** A sign the mechanic is too complex for common. Move it up a rarity or simplify.
