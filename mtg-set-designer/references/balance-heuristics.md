# Balance Heuristics

These are the numerical targets `balance_check.py` and `simulate_draft.py` check against, along with where they come from. Knowing *why* a heuristic exists lets you ignore one when you have a real reason and not when you're just attached to a card.

## Creature vanilla baselines

For reference when writing creatures:

| Mana value | Baseline power/toughness (vanilla) | Notes |
|---|---|---|
| 1 | 1/1 | White/green 2/1 at 1 if downside (dies to everything anyway) |
| 2 | 2/2 | 3/1 if aggressive-leaning |
| 3 | 2/3 or 3/3 | Green/white lean bigger, blue/black smaller |
| 4 | 4/3 or 3/4 | 4/4 in green (Grizzly Bears → Grizzled Veterans) |
| 5 | 4/5 or 5/4 | Bigger in green |
| 6 | 5/6 or 6/5 | |
| 7 | 6/7 or 7/7 | Green gets 7/7 vanilla (a real line) |

A French vanilla (one keyword) usually takes a hit of about 1 total stat for a good keyword (flying, first strike, lifelink). A 2/2 flyer for 2 mana is strong; a 2/1 flyer for 2 mana is more typical.

Cards *above* the curve must have a real downside. Cards *below* the curve need utility.

## Removal density

Per color, in a standard set, expect roughly:

- **2–4 common creature removal spells** per color (though not all colors get unconditional removal; blue gets bounce, green gets fight, etc.)
- **1–2 uncommon creature removal spells** per color
- **1–2 rare/mythic creature removal spells** per color

Total common creature-answering effects across all colors: ~12–18. This is the number that determines format speed — fewer answers, faster format; more answers, slower format.

Removal is not all created equal. Unconditional removal (black's specialty) is different from conditional removal (white's small-creature exile, red's damage-based). When you tally removal for balance, count conditional removal as half.

## Mana curve per limited deck

A typical limited deck (23 non-land cards, 17 lands) curves like:

- 1 mana: 0–2 creatures/spells
- 2 mana: 4–6
- 3 mana: 5–7
- 4 mana: 4–6
- 5 mana: 3–4
- 6+ mana: 1–3

Decks that can't reach this curve are unplayable. Your commons must provide enough playable creatures and spells at each mana value *in each color pair* to fill these slots. Count specifically: "can I draft a WU deck and get at least 4 two-drops?" If the answer is no, there aren't enough two-drops in WU's colors.

## Archetype win-rate bands

In `simulate_draft.py`:

- **Healthy band:** each archetype wins 46%–54% in a balanced format.
- **Acceptable band:** 42%–58%.
- **Warning:** outside 42–58.

One archetype winning 60% is a sign it's too strong, probably because it has a key common that's undercosted or a broken uncommon. Find and fix.

One archetype winning 38% is a sign it's not actually draftable — usually because it's missing supporting commons, has a mechanic that's parasitic without enough density, or its enablers cost too much mana.

## Card play-rate bands

A common that's in almost every deck that can legally run it (> 90% of eligible decks) is a warning. It's either a must-pick (too strong) or a format-warping mana fixer. Either way, investigate.

A common that's in almost no deck (< 8% of eligible decks) is a warning. It's either unplayable or its archetype is broken.

Mid-band: 15%–70% of eligible decks is healthy for most commons. Bombs (usually rares) are expected to be >80% in their color. That's fine because rares don't need to be balanced against each other; they need to be balanced against the commons and uncommons they live among.

## Format speed

Average turn the game ends, simulated:

- **Aggro format:** games end turns 6–8 on average. Short, decisive, often determined by mulligans and opening hands.
- **Midrange format:** games end turns 8–11. The most common target. Rewards drafting well and playing well at roughly equal weight.
- **Control format:** games end turns 10–14. Usually a sign that removal density is very high or there's a bomb race to the late game.

Your set's target speed comes from its pillars. "Aggressive burn set" should land in the aggro band; "graveyard control set" should land in the control band. If the simulated format speed doesn't match the target speed, the format is miscalibrated — usually removal density or mana curves are off.

## Color balance in limited

Each color should be reasonably equal in common card count (within a couple cards of the others) because color imbalance forces drafters into specific colors regardless of the signals at the table. `balance_check.py` warns if any color is more than 3 commons off from the average.

## Complexity at common

Target: **≤20% of commons red-flagged**. See `new-world-order.md` for what counts as red-flagged.

## Evergreen keyword distribution

No single set needs every evergreen, but a set should *choose*. If you're not using deathtouch at all, that's a deliberate choice ("this set has no death-punishers"), not an oversight. Write it down. Same for lifelink, reach, hexproof/ward, etc.

## The heuristics are wrong sometimes

Every heuristic here is a rule of thumb derived from many past sets. Your set might need to violate one because your three pillars demand it. That's fine — the balance report exists to *surface* violations, not to prohibit them. When you intentionally violate a heuristic, document the reason in `balance_report.md`. When the simulator disagrees with you, re-run and double-check. When the simulator agrees with you, ship it.
