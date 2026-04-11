# Rarity Structure

Rarity is not a power dial. Each rarity has a *job*. When a set respects those jobs, the set plays well; when rarities are treated as "same card but bigger," the set collapses into rare-matters, where the limited environment is driven entirely by which rares you opened.

## Card counts (Play Booster era, 2024+)

Starting with *Murders at Karnak Manor* (February 2024), Wizards replaced Draft Boosters and Set Boosters with a single **Play Booster** product. This changed the set composition significantly. Draft Boosters are discontinued.

A standard Play Booster era premier set:

- **81 commons** (down from 101)
- **100 uncommons** (up from 80)
- **60 rares**
- **20 mythic rares**
- **Total ~261 unique cards** (plus basic lands)

The shift moves 20 card slots from common to uncommon. The *purpose* of each rarity is unchanged, but the *weight* uncommons carry has increased dramatically — they now do a lot of the archetype-support work that commons used to shoulder.

Distribute by color roughly like this:

| Rarity | Per color | Gold/colorless/artifact/land |
|---|---|---|
| Common | 14-15 | ~6-11 |
| Uncommon | 16-18 | ~15-20 (includes ~20 gold signpost uncommons) |
| Rare | 9-12 | ~10-15 |
| Mythic | 3-4 | ~3-5 |

Per-color common creature counts (from Rosewater's Nuts & Bolts 16):
- White: ~11 creatures out of ~15 commons
- Blue: ~8 creatures out of ~15 commons
- Black: ~9 creatures out of ~14 commons
- Red: ~9 creatures out of ~14 commons
- Green: ~10 creatures out of ~14 commons

These are approximate. Don't obsess; the balance script checks the actual distribution.

## Play Booster pack structure

A Play Booster contains **14 playable cards**:

- Slots 1–6: commons (6 guaranteed)
- Slot 7: common (87.5%) or a Special Guest / The List card (12.5%)
- Slots 8–10: uncommons (3 guaranteed)
- Slot 11: rare or mythic rare (roughly 6:1 ratio favoring rare)
- Slot 12: basic or common land
- Slot 13: non-foil wildcard (any rarity — can be another rare)
- Slot 14: foil wildcard (any rarity)

This means ~41% of packs contain *two or more rares/mythics*. Rares show up in draft at a meaningfully higher rate than in the old Draft Booster system. This has a design consequence: **commons and uncommons need adequate answers to rare-level threats**, because drafters will face more rares per pod. Rosewater has noted that common removal efficiency has gone up in response (e.g., red common burn now reaches 6 damage where it used to cap at 5).

## The jobs

### Common

**Job:** carry the set's themes, teach the game, make limited work.

In the Play Booster era, commons are fewer (81 vs 101) but each one matters more. About half of every booster is still commons (~7 of 14 playable cards), and most of a limited deck is still commons. If your theme isn't present at common, your theme isn't present.

With fewer commons, there is less room for filler — every common should be purposeful. Rosewater has noted that Play Booster-era commons trend higher in power and utility than their Draft Booster-era equivalents, because "unplayable commons" waste scarcer slots.

Commons must:

- Support the ten archetypes — but now *shared with uncommons*. The archetype-support burden has shifted: commons carry the base, uncommons carry the payoffs and depth. See `archetypes.md`.
- Provide basic creature bodies across the curve in every color.
- Provide removal at the rate the format needs — and at higher efficiency than before, to answer the increased rate of rares in draft.
- Keep the complexity budget (see `new-world-order.md`).
- Include vanilla and French-vanilla creatures without apology.

Commons should not:

- Try to be "cool" by doing tricky things. Cool belongs at higher rarity.
- Enable combos or infinite loops. Commons should reward board play, not combo play.
- Have abilities that punish opponents for playing the game normally.
- Be filler. In 81 slots, every common earns its place.

### Uncommon

**Job:** archetype payoffs, format depth, signposts, the "meat" of drafting.

In the Play Booster era, uncommons are the *biggest rarity in the set* (100 cards, up from 80). They are where the set's strategic depth lives, and they carry significantly more archetype-support weight than before.

Uncommons are where a drafter starts feeling smart. The signpost gold uncommons live here (~20 gold uncommons, two per archetype). So do the French-vanilla-plus-twist creatures, the conditional removal, the card-draw engines, the key archetype payoffs. With 100 slots, there's now room for uncommons to do both archetype signaling *and* broad-use utility.

Each color gets roughly 16–18 uncommons (~10 creatures, ~6–8 noncreatures). Multicolor support nearly doubled vs. the old model — about 20 uncommon slots are multicolor.

Uncommons can have more complexity than commons — a triggered ability, a conditional, a second line of rules text. They can also have more power. A drafter who opens strong uncommons in their colors should feel like they're being rewarded.

### Rare

**Job:** bombs, build-arounds, constructed playability.

Rares are allowed to be powerful, complex, and occasionally weird. They are the cards that *define* decks. In limited, rares are the bombs — the cards that a drafter opens and immediately builds around. In constructed, rares are the backbone of competitive decks.

A rare can have three lines of rules text, two triggered abilities, and a conditional bonus. That's fine at rare. What rares should *not* do is replace commons and uncommons as the set's identity. If the only place your theme shows up is in rares, the theme isn't real — drafters without the rares won't feel it.

Rares must still respect the color pie. "It's rare" is never a license to break color pie.

### Mythic

**Job:** unique effects, memorable moments, flagship cards.

Mythics are the smallest category and the most carefully designed. The temptation is to treat mythic as "rare but bigger." Resist it. A mythic should do something a rare cannot — either because it's too unique, too complex, or too central to the set to be printed as a mere rare. Planeswalkers, multi-color legendary creatures, game-ending threats with unique effects, flagship cycles (the "gods" of Theros) — these are mythic territory.

Mythics are also where Wizards sells booster boxes. A mythic should feel like a moment when it's opened. Design for that feeling: something you'd want to show the person next to you.

**Mythic anti-patterns:**

- A mythic that is a rare with +1 power. This is why mythic exists; don't waste the slot.
- Five mythics that are all "big flying creature with protection." Differentiate.
- A mythic that is oppressive in limited. A mythic drafted by one player should be exciting for them, not instantly-winning.

## Rarity and complexity

Complexity *increases* with rarity, not linearly but definitely. A common should be readable in five seconds. An uncommon in ten. A rare in fifteen. A mythic can take longer — it's supposed to be a Thing you're reading carefully.

This is the *only* dial that scales monotonically with rarity. Power scales non-monotonically (a great uncommon can be stronger than a mediocre rare; that's fine, it's a feature). But comprehension complexity goes up.

## Counting and the balance check

`balance_check.py` reports rarity distribution and flags big imbalances. What it cannot check is whether each rarity is *doing its job*. That's on you. When you review the balance report, ask explicitly for each rarity: "does this rarity's card list carry the weight it needs to?"
