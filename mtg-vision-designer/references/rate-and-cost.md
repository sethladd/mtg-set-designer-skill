# Rate and Cost Reference

A working sheet of what things "should" cost in modern Magic, scoped to the cards a vision designer writes for `vision_cardfile.json`. These are baselines, not laws — the whole point of design is to deliberately deviate from baselines for a reason. But when you're sketching 200+ prototype cards, defaulting to baseline keeps the file evaluable.

Sources: Mark Rosewater's design articles (Nuts & Bolts series, Limited Information), the *Mechanical Color Pie 2021* article, and decades of Limited reviews aggregated into convention. URLs in `sources.md`.

---

## The single rule that does most of the work

A creature's total stats (power + toughness) should be roughly **twice its mana value**.

| Mana value | Total stats | Common shapes |
|---|---|---|
| 1 | 2 | 1/1, 2/0 (rare) |
| 2 | 4 | 2/2, 3/1, 1/3 |
| 3 | 6 | 3/3, 2/4, 4/2 |
| 4 | 7–8 | 4/3, 3/4, 4/4 (green-only at common) |
| 5 | 9 | 4/5, 5/4, 5/5 (green-only at common) |
| 6 | 10–11 | 5/6, 6/5 |
| 7 | 12–13 | 6/7, 7/7 (green) |

This is the **vanilla baseline**. Every non-vanilla feature comes off this baseline.

- **A keyword costs roughly 1 stat.** A 2/1 flyer for {1}{W} is at curve. A 2/2 flyer for {1}{W} is above curve and either has a downside, costs more, or is uncommon+.
- **Multiple keywords cost more.** A 3/3 with flying and vigilance for 4 mana is fine; a 3/3 with flying, vigilance, and lifelink for 4 mana is uncommon-or-rare territory.
- **An ETB ability often costs 1 stat.** A 2/2 for {1}{W} that gains 2 life when it enters is at curve; a 3/3 for {1}{W} that gains 2 life is over.

**Per-color tilt:**
- Green is *biggest*. Green common 4-mana can be 4/4 vanilla. Green's 7-mana common can be 7/7.
- White and red are average; red leans *small* (more 2/1s and 3/1s).
- Blue and black are *smaller* on stats and *more on text*.

---

## Common removal — current pricing patterns

In Play Booster sets, common removal punches harder than it used to (because ~41% of packs have 2+ rares). Use these as starting points:

### Black

- **Unconditional kill at common:** {B}{B} for 2-mana sorcery-speed kill (e.g., Cut Down patterns), or {2}{B} for instant-speed kill, or {3}{B} for an instant that hits anything. Black gets the most range.
- **Conditional kill:** {B} or {1}{B} for "destroy target creature with [condition]" — power 2 or less, attacking creature, etc.
- **-N/-N:** {B} for -1/-1 to one creature; {2}{B} for -3/-3 to one creature.

### White

- **Exile (small):** {W} for "exile target creature with power 2 or less."
- **Exile (tapped/attacking):** {1}{W} or {W} for "exile target tapped creature" / "destroy target attacking creature."
- **Pacifism:** {1}{W} for "enchanted creature can't attack or block."

### Red

- **Burn to creature:** {R} for 2 damage; {1}{R} for 3 damage; {2}{R} for 4 damage. Red common burn now reaches 6 damage at higher cost (post-Play-Booster shift).
- **Burn to anything:** Same costs but roughly +1 mana for "any target" (player included).
- **Combat-only:** {R} for "deal 2 damage to attacking/blocking creature."

### Green

- **Fight:** {1}{G} for "target creature you control fights target creature you don't control." {2}{G} for instant-speed fight.
- **Bite:** {2}{G} for "target creature you control deals damage equal to its power to target creature you don't control."
- **Flying-only:** {G} for "destroy target creature with flying."

### Blue

- Blue doesn't kill — it bounces. **Bounce:** {U} for "return target creature to its owner's hand" (modern: usually requires a condition or only hits creatures up to a certain mana value at 1-mana cost). {1}{U} for unconditional bounce (Unsummon).
- **Soft removal:** {U} for "tap target creature; it doesn't untap during its controller's next untap step." {2}{U} for "transform target creature into a Frog" pattern.

### Removal density target per color

In a Play Booster set:
- 2–3 common removal spells per color
- 2–3 uncommon removal spells per color
- 1–2 rare/mythic removal spells per color

Total common+uncommon answers: ~20–30 across all colors. Fewer answers = faster format.

---

## Card draw and selection

| Effect | Common cost | Notes |
|---|---|---|
| Cantrip ("draw a card" attached to a small spell) | +{1} on top of base spell | Opt: {U} for scry 1, draw a card. |
| Draw 1 (just draw) | {1}{U} for sorcery; {2}{U} for instant | Mostly blue. |
| Draw 2 | {2}{U}{U} for sorcery-speed; instant is harder. | Restrictive. |
| Looting (draw, then discard) | {U} for draw-then-discard one card; {1}{U} for two | Blue. |
| Rummaging (discard, then draw) | {R} for one card; {1}{R} for two | Red. |
| Surveil 1 / Scry 1 attached to a spell | "free" — built into other effects | Texture, not a slot. |
| Investigate attached to a creature | One stat off baseline | Common pattern: "When this creature enters, investigate." |
| Conditional "draw a card" trigger on creature | Often above curve at common | "Whenever this creature attacks, draw a card" is uncommon territory. |

White and green draw must be conditional or tied to creatures. Black trades life for cards: {1}{B} sorcery to "lose 2 life, draw 2 cards" (Sign in Blood / Night's Whisper rate).

---

## Combat tricks and pump

**The Giant Growth baseline:** {G} for +3/+3 until end of turn (the canonical green combat trick). Other colors offer narrower variants:

| Effect | Cost | Color |
|---|---|---|
| +3/+3 until end of turn | {G} | Green only at this rate |
| +2/+2 until end of turn | {1}{W} or {1}{R} | White/red common |
| +1/+1 to all your creatures until EOT | {1}{W} | White (Trumpet Blast/Glorious Charge variants) |
| +X/+0 (red), +0/+X (white/green) | {R} for +N/+0 where N ≈ 2–3 | Red leans P, white/green lean T |
| Indestructible until EOT | {1}{W}{W} | White |
| Hexproof until EOT | {G} | Green's classic anti-removal trick |
| Untap target creature | {U} as a piece of a 2-mana spell | Blue. |

The general rule: a combat trick gives roughly +N/+N where N×2 ≈ mana cost in stats granted, with a small premium for instant speed.

---

## Counterspells (blue only)

| Effect | Cost |
|---|---|
| Hard counter target spell | {U}{U} (hard but at least one set has had this at common; usually it's higher) |
| Counter unless they pay {N} | {1}{U} for {N=2}; {2}{U} for {N=3} |
| Counter target creature spell | {U} (Essence Scatter rate) |
| Counter target noncreature spell | {U} (Negate rate) |
| Counter spell with [condition] | {U} when the condition is restrictive |

White can have tax counters ("pay N or it's countered"), usually at uncommon. No other colors counter spells at common.

---

## Tokens and creation effects

| Effect | Cost |
|---|---|
| Create a 1/1 creature token | {W} or {1} on a non-creature spell as a side effect |
| Create a 2/2 creature token | {1}{W} or {2}{G} |
| Create two 1/1 tokens | {2}{W} sorcery |
| Create a Treasure | {R} as part of a 2-mana spell; {1}{R} on its own |
| Create a Food | {1} on a creature ETB; {2} for a Food maker |
| Create a Clue | {2}{U} for "Investigate" attached to a sorcery |
| Anthem (creatures get +1/+1 statically) | {2}{W}{W} for an enchantment; {3}{W} for a creature lord |

---

## Enchantments and artifacts

- **Anthem enchantment** (creatures get +1/+1): typically {2}{W}{W} or {3}{W}. Uncommon at the cheap end.
- **Aura that pumps** (+2/+2 to enchanted creature): {1}{G} or {1}{W} common.
- **Equipment with +1/+1**: {1} cost, equip {1}, common.
- **Equipment with +2/+1**: {2} cost, equip {2}, common.
- **Mana rock** (artifact tap for one mana): {2}, common; {3} taps for any color, uncommon. Watch interaction with set ramp pillars.

---

## Land ramp (green primary)

| Effect | Cost |
|---|---|
| Search for basic land, put it tapped onto battlefield | {2}{G} sorcery (Cultivate is {3}{G} for two lands; Rampant Growth is {1}{G} for one) |
| Search for basic land, put it into hand | {1}{G} sorcery |
| Mana dork ({T}: Add {G}) | {G} 1/1 creature, common |
| Treasure-creating spell | {R} or {1}{R} on a small spell |

Green's ramp at common is the fundamental "go bigger" enabler — a set that wants slow, big creatures needs ample green common ramp.

---

## Mechanic as-fan targets at common

A mechanic with reminder text needs to *appear* often enough to teach itself. Approximate as-fan (cards-per-pack) targets at common:

| Mechanic role | Target as-fan at common | Translates to common count |
|---|---|---|
| **Primary set mechanic** (the headline) | ~1.0+ per pack | 8–12 commons feature it |
| **Secondary mechanic** | 0.5–1.0 per pack | 4–8 commons feature it |
| **Tertiary or supporting** | 0.25–0.5 per pack | 2–4 commons feature it |

Rough math: a Play Booster has ~7 commons in a pack across 81 commons in the set, so each common appears at ~7/81 ≈ 8.6% per pack. To hit "1.0 per pack," you need 12 commons with the mechanic (12 × 8.6% ≈ 1.0).

If a new named mechanic appears on fewer than 4 commons, it'll feel under-supported in Limited. If it appears on more than 14 commons, it'll feel oppressive (every pack has it everywhere).

---

## Mana curve shape per drafted deck

A typical Limited deck (23 spells, 17 lands) curves roughly:

| MV | Cards |
|---|---|
| 1 | 0–2 |
| 2 | 4–6 |
| 3 | 5–7 |
| 4 | 4–6 |
| 5 | 3–4 |
| 6+ | 1–3 |

For each color pair, ask: can a drafter actually fill these slots from your common pool? If not, the set has structural holes. Concretely, each color pair needs ~6–8 playable common 2-and-3-drops in its colors so a drafter can build a real curve.

---

## Format speed targets

Set this in your vision document as a deliberate choice; check it later via simulation.

- **Aggro format:** games end turns 6–8. Lots of cheap creatures, efficient burn, low common toughness, weak common removal.
- **Midrange format:** games end turns 8–11. The default and the most common target. Balanced removal, balanced curves.
- **Control format:** games end turns 10–14. Heavy common removal, big creatures, expensive interactive spells.

If your pillars say "graveyard is your second hand" and your simulated format ends turn 7, the format isn't supporting the pillar — usually because removal is too cheap or curves are too low.

---

## Above-curve and below-curve markers

Use these when sketching a card to know whether it's "premium," "fair," or "filler":

- **Below curve (filler / French vanilla):** A 2/1 for {2}{W} with one keyword — fine common slot but unmemorable.
- **At curve (fair):** A 3/2 for {1}{W} with vigilance — exactly what white wants from a common 2-drop.
- **Above curve (premium / build-around):** A 3/3 for {1}{W} with vigilance and lifelink — too strong for common, fits uncommon or rare.

When a vision-design card looks above curve, ask: is this card carrying a pillar? If yes, push to uncommon. If no, bring it to baseline.

---

## When you're allowed to break these rates

These rates are derived from broad patterns. Your set might need to violate one because a pillar demands it:

- A "burn matters" set might let red common burn reach higher numbers.
- A "small creatures" set might compress the vanilla curve toward smaller bodies (the Bloomburrow approach).
- An "expensive spells matter" set might shift the mana curve up by 1.

That's fine. The point of these rates is to **make deliberate breaks visible**. If you cost a card off-rate by accident, it'll quietly break Limited. If you cost it off-rate on purpose, document why in the vision handoff so Set Design knows it's intentional and Play Design knows what to test.
