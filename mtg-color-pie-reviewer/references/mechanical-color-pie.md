# Mechanical Color Pie Reference

Canonical primary/secondary/tertiary assignments for every major effect category. Based on Mark Rosewater's Mechanical Color Pie 2021 article, the 2021 Changes article, and subsequent updates through 2025.

Use this as a lookup during review. For each effect on a card, find the matching category below and check whether the card's color has the appropriate access level.

**Notation:** P = Primary, S = Secondary, T = Tertiary, — = Not in pie

---

## Table of Contents

1. [Creature Removal](#creature-removal)
2. [Card Draw and Selection](#card-draw-and-selection)
3. [Counterspells and Spell Interaction](#counterspells-and-spell-interaction)
4. [Direct Damage](#direct-damage)
5. [Enchantment and Artifact Removal](#enchantment-and-artifact-removal)
6. [Lifegain](#lifegain)
7. [Mana Production and Ramp](#mana-production-and-ramp)
8. [Creature Recursion and Reanimation](#creature-recursion-and-reanimation)
9. [Bounce (Return to Hand)](#bounce)
10. [Tokens](#tokens)
11. [+1/+1 Counters and Pump Effects](#counters-and-pump)
12. [Evasion Keywords](#evasion-keywords)
13. [Combat Keywords](#combat-keywords)
14. [Graveyard Interaction](#graveyard-interaction)
15. [Library Manipulation](#library-manipulation)
16. [Evergreen Keywords by Color](#evergreen-keywords-by-color)
17. [Deciduous Mechanics](#deciduous-mechanics)

---

## Creature Removal

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Destroy target creature (unconditional) | — | — | P | — | — |
| Destroy target creature (conditional) | S | — | P | — | — |
| Exile target creature | P | — | S | — | — |
| Deal damage to target creature | — | — | — | P | — |
| Target creature gets -N/-N | — | — | P | — | — |
| Fight (mutual combat) | — | — | — | S | P |
| Bite (one-sided fight) | — | — | — | — | P |
| Destroy target creature with flying | — | — | — | — | P |
| Pacifism effects (can't attack/block) | P | — | — | — | — |
| Tap/detain creature | P | S | — | — | — |
| Sacrifice a creature (forced) | — | — | P | S | — |
| Transform into another creature | — | P | — | — | T |
| Reduce power/toughness to 0 or base | — | S | — | — | — |
| Destroy tapped creature | P | — | — | — | — |
| Exile until leaves battlefield | P | — | — | — | — |

**Why this matters:** White removes via exile and conditions. Blue doesn't destroy — it bounces, taps, or transforms. Black kills unconditionally. Red burns. Green fights. When a card breaks this pattern, it's usually a problem.

**The efficiency trap:** Even when an effect is in-pie, efficiency matters. Blue can polymorph creatures (Pongify), but if blue has too many cheap polymorph effects, it functionally has better creature removal than black, which breaks the pie in practice.

---

## Card Draw and Selection

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Draw N cards (unrestricted) | — | P | — | — | — |
| Draw with life payment | — | — | P | — | — |
| Draw when creature enters/attacks | S | — | — | — | P |
| Draw once per turn (conditional) | S | — | — | — | — |
| Impulsive draw (exile, play this turn) | — | — | — | P | — |
| Looting (draw then discard) | — | P | — | — | — |
| Rummaging (discard then draw) | — | — | — | P | — |
| Wheel (discard hand, draw new) | — | — | — | P | — |
| Scry / library manipulation | — | P | — | — | — |
| Card filtering (look at top N, choose) | — | P | — | — | S |
| Tutor (search library) | — | — | P | — | S |
| Tutor for creature specifically | — | — | S | — | P |
| Tutor for land specifically | — | — | — | — | P |
| Card selection from graveyard | — | — | P | — | S |

**Critical distinction:** White's card draw MUST have restrictions — once-per-turn, tied to permanents entering, requires opponent action, etc. If white draws cards without conditions, that's a break. Green's card draw MUST be tied to creatures, lands, or board state. "Draw 3" with no creature/land condition in green is a break (the Harmonize problem).

**Red's draw is temporary:** Impulsive draw (exile top card, play it this turn or lose it) is red's primary draw mechanic. It fits red's philosophy — act now or lose the chance. Traditional "draw and keep" card draw is NOT red.

---

## Counterspells and Spell Interaction

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Counter target spell (hard) | — | P | — | — | — |
| Counter unless opponent pays N | S | P | — | — | — |
| Counter target noncreature spell | — | P | — | — | — |
| Counter target activated ability | — | P | — | — | T |
| Redirect spell | — | P | — | — | — |
| Copy spell | — | P | — | S | — |
| "Can't be countered" | — | — | — | S | S |

**The hard line:** Only blue gets hard counterspells. White gets tax-based counters (pay N more or the spell is countered) — these are functionally different from blue's unconditional counters. Red and black do NOT counter spells. Green does not counter spells (the old Avoid Fate exception is not precedent). Red Elemental Blast/Pyroblast are acknowledged breaks that exist only for eternal format balance.

---

## Direct Damage

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Deal N damage to any target | — | — | — | P | — |
| Deal N damage to creature only | — | — | — | P | — |
| Deal N damage to player only | — | — | — | P | — |
| Drain (damage + lifegain) | — | — | P | — | — |
| Damage equal to creature's power | — | — | — | S | S |
| Deal 1 damage to each creature | — | — | — | P | — |
| Board wipe via damage | — | — | — | P | — |

**Green's boundary:** Green can deal damage to creatures with flying (Plummet variants) and through fight/bite. Green NEVER deals direct damage to players (Hornet Sting is a break). Green NEVER deals non-combat damage to non-flying creatures outside of fight.

---

## Enchantment and Artifact Removal

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Destroy target enchantment | P | — | T | — | S |
| Destroy target artifact | S | — | T | P | P |
| Destroy target artifact or enchantment | P | — | — | — | P |
| Exile target enchantment | P | — | — | — | — |
| Exile target artifact | S | — | — | — | — |
| Destroy all artifacts | — | — | — | P | — |
| Destroy all enchantments | P | — | — | — | — |

**The red enchantment wall:** Red has ZERO enchantment interaction. This is one of the hardest lines in the color pie. Chaos Warp's ability to shuffle away enchantments is explicitly a break. Any red card that removes, exiles, bounces, or otherwise answers enchantments is a break.

**Black's limited access:** Black got tertiary enchantment destruction in 2021, but ONLY through sacrifice-based mechanics (e.g., "Sacrifice a creature: destroy target enchantment an opponent controls"). Unconditional black enchantment destruction is still a break.

---

## Lifegain

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Gain N life | P | — | — | — | S |
| Drain life (opponent loses, you gain) | — | — | P | — | — |
| Lifegain on creature ETB/attack | P | — | — | — | S |
| Lifelink | P | — | S | — | — |

**Red and blue don't gain life.** This is a core weakness for both. Any red or blue lifegain is a break (with extremely narrow exceptions for multicolor cards where the other color provides it).

---

## Mana Production and Ramp

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Mana dork (creature that taps for mana) | — | — | — | T | P |
| Search library for land, put on battlefield | — | — | — | — | P |
| Search library for land, put in hand | — | — | — | — | P |
| Treasure token creation | — | — | S | S | — |
| Ritual (temporary mana burst) | — | — | S | P | — |
| Cost reduction | — | S | — | S | — |
| Untap lands | — | — | — | — | S |

**The Treasure lesson:** Blue creating Treasures in Ixalan was explicitly called a mistake by Rosewater. Blue does not ramp. Green is primary in permanent mana acceleration; red is primary in temporary mana (rituals, Treasures).

---

## Creature Recursion and Reanimation

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Return creature from graveyard to battlefield | S | — | P | — | T |
| Return creature from graveyard to hand | S | — | P | — | S |
| Return instant/sorcery from graveyard | — | S | — | P | — |
| Flashback / cast from graveyard | — | S | P | S | — |
| Exile cards from graveyard | S | — | P | — | — |

**White's limits:** White can reanimate small creatures (low mana value) or creatures that just died this turn. Unrestricted reanimation is black's domain.

---

## Bounce

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Return permanent to hand | — | P | — | — | — |
| Return creature to hand | S | P | — | — | — |
| Return to owner's hand (defensive) | S | P | — | — | — |
| Flicker (exile, return immediately) | P | S | — | — | — |

---

## Tokens

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Create small creature tokens (1/1, 2/2) | P | — | S | S | S |
| Create large creature tokens (3/3+) | — | — | — | — | P |
| Go-wide token strategy | P | — | S | S | — |
| Token copying | — | P | — | — | — |

---

## Counters and Pump

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| +1/+1 counters | P | — | S | — | P |
| Temporary pump (+N/+N until EOT) | S | — | S | P | P |
| Team-wide anthem (+1/+1 to all) | P | — | — | — | — |
| -1/-1 counters | — | — | P | — | — |
| Power/toughness switching | — | P | — | — | — |
| Setting P/T to specific value | — | P | — | — | — |

---

## Evasion Keywords

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Flying | P | P | S | S | T |
| Menace | — | — | P | P | S |
| Trample | — | — | — | S | P |
| Unblockable | — | P | — | — | — |
| Fear/Intimidate (color-based evasion) | — | — | P | — | — |
| Shadow/skulk (power-based evasion) | — | — | S | — | — |
| Reach | — | — | — | — | P |

---

## Combat Keywords

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| First strike | P | — | S | P | — |
| Double strike | P | — | — | P | — |
| Vigilance | P | S | — | — | S |
| Haste | — | — | S | P | S |
| Deathtouch | — | — | P | — | S |
| Defender | P | P | — | — | S |
| Indestructible | P | — | — | — | S |
| Lifelink | P | — | S | — | — |
| Flash | — | P | — | — | S |
| Ward | S | P | — | — | S |
| Hexproof | — | P | — | — | S |

---

## Graveyard Interaction

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Self-mill (cards to own graveyard) | — | S | P | — | S |
| Mill opponent | — | P | S | — | — |
| Graveyard as resource | — | — | P | S | S |
| Exile from graveyard | P | — | P | — | — |

---

## Library Manipulation

| Effect | W | U | B | R | G |
|--------|---|---|---|---|---|
| Scry | S | P | S | S | S |
| Surveil | — | P | P | — | — |
| Look at top N, rearrange | — | P | — | — | S |
| Reveal top card | — | S | — | — | P |
| Play from top of library | — | — | — | S | P |

---

## Evergreen Keywords by Color

**White:** Flying, first strike, double strike, vigilance, lifelink, defender, indestructible, ward, flash (rare)
**Blue:** Flying, flash, ward, hexproof, defender
**Black:** Flying (secondary), menace, deathtouch, lifelink (secondary), haste (tertiary)
**Red:** First strike, double strike, haste, menace, trample (secondary)
**Green:** Trample, reach, deathtouch (secondary), vigilance (secondary), haste (secondary), hexproof (secondary), ward (secondary)

---

## Deciduous Mechanics

These appear when needed but aren't in every set:

- **Protection** — primarily white, secondary all colors
- **Prowess** — primarily blue/red
- **Cycling** — all colors
- **Kicker** — all colors
- **Sagas** — all colors (but primarily white, blue, green)
- **Modal double-faced cards** — all colors
- **Adventures** — all colors

---

## Sources

- [Mechanical Color Pie 2021](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021)
- [Mechanical Color Pie 2021 Changes](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021-changes)
- [Mechanical Color Pie 2017](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2017-2017-06-05)
- [The Council of Colors, Revisited](https://magic.wizards.com/en/news/making-magic/the-council-of-colors-revisited)
