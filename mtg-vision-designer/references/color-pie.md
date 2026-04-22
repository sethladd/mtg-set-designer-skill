# Color Pie for Vision Design

A working color-pie reference scoped to the questions a vision designer asks: *which color does this mechanic belong in?* and *which colors can carry it as secondary?* For deeper per-card review (breaks vs. bends, the Council of Colors framework), the `mtg-color-pie-reviewer` skill has the comprehensive treatment — this file is the vision-time pocket version.

Sources: Mark Rosewater's *Mechanical Color Pie 2021* and *2021 Changes* articles, *Let's Talk Color Pie*, and subsequent Rosewater rulings via Blogatog. URLs in `sources.md`.

---

## Color identity in one paragraph each

**White** — order, community, justice. Wants peace, but will fight for it. Mechanically: small creatures, anthems, lifegain, exile-based removal (often conditional), pacifism, equal distribution, taxes, board wipes that re-establish order.

**Blue** — knowledge, perfection, control of the future. Mechanically: card draw, scry/surveil, counterspells, bounce, transformation, evasion via flying and unblockability, denial, copying spells.

**Black** — power at any cost, ambition. Mechanically: unconditional removal (kill), drain (damage that gains life), tutoring, reanimation, sacrifice payoffs, hand attack, "draw 2, lose 2 life," parasitism (-1/-1 counters).

**Red** — freedom, impulse, emotion. Mechanically: direct damage to any target, haste, rituals (temporary mana), impulsive draw (exile, play this turn), discard-and-draw, copy your own spells, artifact destruction, "can't block."

**Green** — nature, growth, interdependence. Mechanically: big creatures, ramp (mana acceleration), creature tutors, fight, trample, reach, draw-tied-to-creatures, +1/+1 counters, artifact/enchantment destruction.

If a mechanic doesn't map cleanly to one of these identities, color-assignment will feel arbitrary and will need to be defended.

---

## Hard "no" lines (don't break these)

These aren't shifting — they're load-bearing. If a vision-design mechanic forces a card to break one of these, the mechanic needs reworking, not the color pie.

- **Only blue gets hard counterspells.** Other colors can have tax-counters (white) or counter-creature-spells (green, narrowly), but unconditional "Counter target spell" is blue's monopoly.
- **Only red gets unrestricted "deal damage to any target."** Green can deal damage to flying creatures (Plummet) and via fight; black can drain. Direct damage to a player from any non-red source is a break.
- **Red has zero enchantment interaction.** No destroy, exile, bounce, or counter targeting enchantments.
- **Red and blue can't gain life.** Lifelink, "you gain N life" — both colors cannot. Multicolor cards can if the other color provides it.
- **Green can't deal direct damage to players** and can't deal non-combat damage to non-flying creatures outside fight/bite.
- **White card draw must have restrictions** — once-per-turn, on creatures entering, requires opponent action. Unconditional "draw N" is a white break.
- **Green draw must be tied to creatures, lands, or board state.** "Draw 3" with no condition (the Harmonize problem) is a break.
- **Black gets unconditional creature destruction; other colors don't.** White exiles conditionally. Green fights. Red burns. Blue transforms or bounces.
- **Treasure tokens are red and black.** Blue creating Treasures (Ixalan) was Rosewater-confirmed as a mistake; do not repeat it.

---

## Quick-lookup tables for vision-time mechanic placement

Notation: **P** = primary, **S** = secondary, **T** = tertiary, **—** = not in pie. (Rare/mythic exceptions exist; vision-time, plan against the canonical column.)

### Removal

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Destroy creature (unconditional) | — | — | **P** | — | — |
| Destroy creature (conditional, e.g., tapped/attacking) | **S** | — | **P** | — | — |
| Exile creature | **P** | — | **S** | — | — |
| Damage to creature | — | — | — | **P** | — |
| -N/-N to creature | — | — | **P** | — | — |
| Fight / bite | — | — | — | **S** | **P** |
| Pacifism (can't attack/block) | **P** | — | — | — | — |
| Bounce to hand | — | **P** | — | — | — |
| Tap/detain | **P** | **S** | — | — | — |
| Forced sacrifice | — | — | **P** | **S** | — |

### Card advantage

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Draw N (unrestricted) | — | **P** | — | — | — |
| Draw with life payment | — | — | **P** | — | — |
| Draw conditional on creatures/board | **S** | — | — | — | **P** |
| Impulsive draw (exile, play this turn) | — | — | — | **P** | — |
| Looting (draw, then discard) | — | **P** | — | — | — |
| Rummaging (discard, then draw) | — | — | — | **P** | — |
| Scry / Surveil | **S** | **P** | **S** (surveil) | **S** | **S** |
| Tutor (any card) | — | — | **P** | — | — |
| Tutor for creature | — | — | **S** | — | **P** |
| Tutor for land | — | — | — | — | **P** |

### Resource production

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Mana dork (creature taps for mana) | — | — | — | **T** | **P** |
| Land ramp (search to battlefield) | — | — | — | — | **P** |
| Land ramp (search to hand) | — | — | — | — | **P** |
| Treasure tokens | — | — | **S** | **S** | — |
| Ritual (one-shot mana burst) | — | — | **S** | **P** | — |
| Cost reduction | — | **S** | — | **S** | — |
| Untap lands | — | — | — | — | **S** |

### Permanent answers (artifact/enchantment removal)

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Destroy enchantment | **P** | — | **T** | **—** | **S** |
| Destroy artifact | **S** | — | **T** | **P** | **P** |
| Destroy artifact OR enchantment | **P** | — | — | — | **P** |
| Destroy all artifacts | — | — | — | **P** | — |
| Destroy all enchantments | **P** | — | — | — | — |

### Lifegain and combat

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Gain life | **P** | — | — | — | **S** |
| Drain (opponent loses, you gain) | — | — | **P** | — | — |
| Lifelink | **P** | — | **S** | — | — |
| First strike | **P** | — | **S** | **P** | — |
| Double strike | **P** | — | — | **P** | — |
| Vigilance | **P** | **S** | — | — | **S** |
| Haste | — | — | **S** | **P** | **S** |
| Deathtouch | — | — | **P** | — | **S** |
| Trample | — | — | — | **S** | **P** |
| Reach | — | — | — | — | **P** |
| Flying | **P** | **P** | **S** | **S** | **T** |
| Menace | — | — | **P** | **P** | **S** |
| Flash | — | **P** | — | — | **S** |
| Ward | **S** | **P** | — | — | **S** |
| Hexproof (legacy; prefer Ward) | — | **P** | — | — | **S** |

### Tokens, counters, manipulation

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Small creature tokens (1/1, 2/2) | **P** | — | **S** | **S** | **S** |
| Large creature tokens (3/3+) | — | — | — | — | **P** |
| Token copying | — | **P** | — | — | — |
| +1/+1 counters | **P** | — | **S** | — | **P** |
| -1/-1 counters | — | — | **P** | — | — |
| Anthem (team-wide +N/+N) | **P** | — | — | — | — |
| Temporary pump | **S** | — | **S** | **P** | **P** |
| Power/toughness switching | — | **P** | — | — | — |

### Spell interaction and graveyard

| Effect | W | U | B | R | G |
|---|---|---|---|---|---|
| Hard counter | — | **P** | — | — | — |
| Tax counter ("unless they pay N") | **S** | **P** | — | — | — |
| Counter creature only | — | **P** | — | — | **T** |
| Copy spell | — | **P** | — | **S** | — |
| Self-mill | — | **S** | **P** | — | **S** |
| Mill opponent | — | **P** | **S** | — | — |
| Reanimate creature to battlefield | **S** | — | **P** | — | **T** |
| Reanimate creature to hand | **S** | — | **P** | — | **S** |
| Cast instant/sorcery from graveyard | — | **S** | — | **P** | — |

---

## Recent color pie shifts (2017 → 2025)

Use these to avoid violating yesterday's pie when the actual pie has moved.

- **Green gets some haste.** Up from "almost never" — green can have haste on creatures with a built-in trigger or a tribal/landfall payoff (post-2021).
- **White can draw cards under restrictions.** Conditional draw (creature ETB, once-per-turn) is now solidly white-secondary (post-2021, "make white great again").
- **Black got tertiary enchantment destruction**, but only via sacrifice cost (post-2021).
- **Ward replaced Hexproof** as the default protection keyword (Strixhaven 2021 onward). Both are still in the pie; Ward is now strongly preferred.
- **Treasure became cross-color** (red/black primary, others as one-off rares). Avoid putting Treasure generation in blue/green/white at common.
- **Prowess fell from evergreen to deciduous** (Foundations 2024). When you reach for "spells matter at common," you now choose Prowess; you don't get it for free.
- **Tribal type became Kindred** (2024). Doesn't affect color but affects card-type templating.
- **Blue lost rituals.** "Add {U}{U}{U}" is no longer in blue; it briefly was. Blue's mana acceleration is cost-reduction, not adding mana.

For the full list of changes between 2017 and 2021, see Rosewater's *Mechanical Color Pie 2021 Changes* article (URL in `sources.md`). Keep an eye on annual State-of-Design columns for newer shifts.

---

## How to color-assign a *new* mechanic

When you're inventing a mechanic, work through this in order:

1. **Identify the mechanic's character.** Write one sentence: "This mechanic is about ____." Aggression? Patience? Cleverness? Sacrifice? Discovery? Growth?
2. **Match character to color identity.** Patience and trickery → blue. Aggression and impulse → red. Growth and inevitability → green. Sacrifice and ambition → black. Order and protection → white.
3. **Choose ONE primary color.** Resist the urge to put a mechanic in two colors equally. The primary color is the one whose identity the mechanic *is* — without it, the mechanic doesn't make sense.
4. **Choose 1–2 secondary colors.** The secondary should share *some* identity overlap. Example: "rituals" are primary red, secondary black — both want to spend resources for short-term gain.
5. **Stop there.** Three primary colors for a single mechanic almost always means the mechanic isn't doing color identity work.
6. **Define the rarity gradient.** Primary color gets the most cards with the mechanic, including at common. Secondary gets fewer, often at higher rarity. Tertiary gets a single signpost card.

### Worked example: "Endure" (Tarkir Dragonstorm 2025)

- **Character:** Resilience under attack — taking a hit and growing stronger or leaving a successor behind.
- **Identity match:** Growth/protection mix. Counters → green/white. Spirit tokens → white. Resilience → green/white.
- **Primary:** White and green (Abzan-aligned, since the mechanic was wedge-clan in execution).
- **Tertiary touch:** Black (the third Abzan color) — enough to feel wedge but not enough to feel like the mechanic is everywhere.

This is roughly how WotC arrived at Endure. The lesson: a mechanic with two genuinely-equal primaries usually maps to a *clan/faction* in a multicolor set, not a mono-color identity.

---

## UB color pie compensation

Universes Beyond sets often have IPs that don't map evenly to WUBRG (e.g., Warhammer 40,000 is heavy on black and short on green). Vision design must compensate, not "fix":

1. **Identify the gap.** From `ip_constraints.md`, find which color is under-represented.
2. **Find IP-plausible elements that fit the missing color.** Don't recolor villains green; find the IP's natural-aligned, growth-aligned, or community-aligned elements and use those for green.
3. **Lean on color-pie-flexible mechanics.** Mechanics like Adventures, Sagas, and predefined-token effects don't have rigid color homes and can fill gaps without breaking the pie.
4. **Document the compensation strategy.** The vision handoff should state explicitly: "Green is short by ~6 commons; we're using druidic-faction-equivalents and a Forage-style mechanic to fill."

The IP shouldn't break the pie. The pie shouldn't break the IP. Find the overlap.

---

## How to use this file

- **Every named mechanic** in the vision handoff should have a `colors` field with primary/secondary/tertiary. Cross-check against the lookup tables above.
- **Every archetype** should be expressible within its two colors' pie. If WU has to do something only red does, the archetype is misdesigned.
- **Every signpost uncommon** should be doable within the gold-card overlap of its two colors. If your WU signpost requires something only blue does *and* something only red does, it's not really a WU card.
- **When in doubt, escalate to the color-pie-reviewer skill.** Vision design is allowed bends; breaks should be deliberate and documented in "What We Tried and Cut" so the reviewer knows it was intentional.
