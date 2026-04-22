# Mechanics Catalog

A working reference of MTG keywords, ability words, and named mechanics for vision-design-time decisions about which mechanics to use, return, or invent against.

This file is **descriptive** — it tells you what currently exists. The companion file `mechanics.md` is **prescriptive** — it tells you how to think about choosing mechanics. Read them together: use this to know the inventory; use `mechanics.md` to spend the budget.

Reminder text is sourced from official Wizards mechanics articles where possible, and paraphrased only where noted. Always re-check current templating against the comprehensive rules before shipping a card design — see `templating.md`.

---

## Table of contents

1. [Evergreen keyword abilities](#evergreen-keyword-abilities)
2. [Evergreen keyword actions](#evergreen-keyword-actions)
3. [Deciduous keywords](#deciduous-keywords)
4. [Recent set mechanics (2024–2025)](#recent-set-mechanics-20242025)
5. [Static mechanic concepts to know](#static-mechanic-concepts-to-know)
6. [How to use this catalog](#how-to-use-this-catalog)

---

## Evergreen keyword abilities

These appear in essentially every premier set. Reach for them as the texture of your set without spending complexity budget on a "new mechanic." Choose which ones to *emphasize* — that choice changes play feel.

| Keyword | Reminder text (canonical short form) | Notes |
|---|---|---|
| Deathtouch | Any amount of damage this deals to a creature is enough to destroy it. | Combat math eraser. Stacks awkwardly with double strike and trample — be aware. |
| Defender | This creature can't attack. | Cheap toughness. White/blue mostly; some artifact creatures. |
| Double strike | This creature deals both first-strike and regular combat damage. | Heavy red/white. Strong with +1/+1 effects. |
| Enchant [type] | Auras have this; designates what they go on. | Card-text plumbing, not a "spend a slot" keyword. |
| Equip [cost] | [cost]: Attach to target creature you control. Equip only as a sorcery. | Pillar of equipment subthemes. |
| First strike | This creature deals combat damage before creatures without first strike. | White/red mainly. |
| Flash | You may cast this spell any time you could cast an instant. | Blue primary; some white/green. Watch interaction with attack triggers. |
| Flying | This creature can't be blocked except by creatures with flying or reach. | The most-emphasized evergreen. White/blue/black get most of it. |
| Goad | Until your next turn, target creature attacks each combat if able and attacks a player other than you if able. | Multiplayer-flavored; rare in 1v1. Used sparingly outside Commander products. |
| Haste | This creature can attack and {T} as soon as it comes under your control. | Red/black primary; green has been getting more (color-pie shift). |
| Hexproof | This creature can't be the target of spells or abilities your opponents control. | Officially evergreen but **largely retired in favor of Ward** since 2021. Use Ward unless the set explicitly wants un-targetable creatures. |
| Indestructible | Damage and effects that say "destroy" don't destroy this. | High-rarity mostly. Watch interaction with –X/–X removal. |
| Lifelink | Damage dealt by this creature also causes you to gain that much life. | White primary; black secondary. |
| Menace | This creature can't be blocked except by two or more creatures. | Black/red primary. The "soft evasion." |
| Protection from [quality] | This can't be blocked, targeted, dealt damage, enchanted, or equipped by anything matching [quality]. (DEBT abbreviation: Damage prevented, Enchant/equip blocked, Blocking blocked, Target blocked.) | Demoted to deciduous, returned to evergreen in 2021. Use sparingly; very feels-bad if mis-targeted. |
| Reach | This creature can block creatures with flying. | Green primary. |
| Trample | This creature can deal excess combat damage to the player or planeswalker it's attacking. | Green/red primary. |
| Vigilance | Attacking doesn't cause this creature to tap. | White/green primary. |
| Ward [cost] | Whenever this becomes the target of a spell or ability an opponent controls, counter it unless that player pays [cost]. | Replaced hexproof as the preferred protection since Strixhaven (2021). Cost can be mana or non-mana ("pay 2 life," "discard a card"). |

**Recent change:** **Prowess** was demoted from evergreen to deciduous around Foundations (Nov 2024). Use it when red/blue spell-matters is core; don't assume it'll appear in your set just because it once was evergreen.

**Recent change:** **Tribal** the card type was renamed **Kindred** in 2024 (started phasing in late 2023; canonized in Modern Horizons 3, June 2024).

---

## Evergreen keyword actions

These show up in any set without explanation needed. They are *verbs* the rules text uses, not abilities a creature has.

| Action | Meaning |
|---|---|
| Activate | Pay an activated ability's cost to put it on the stack. |
| Attach | Put an Aura/Equipment/Fortification onto a permanent. |
| Cast | Pay a spell's costs and put it on the stack. |
| Counter | Remove a spell or ability from the stack without effect. |
| Create | Put a token onto the battlefield. |
| Destroy | Move a permanent to its owner's graveyard. |
| Discard | Move a card from a hand to that player's graveyard. |
| Exchange | Swap two things (life totals, controllers, zones). |
| Exile | Move a card to the exile zone. |
| Fight | Two creatures deal damage to each other equal to their power. |
| Mill | Put the top N cards of a library into that player's graveyard. |
| Play | Cast a spell or play a land. |
| Reveal | Show a card to all players. |
| Sacrifice | Move a permanent you control to its owner's graveyard. |
| Scry N | Look at the top N cards of your library; put any number on the bottom and the rest back on top in any order. |
| Search | Look through a zone for cards matching a description. |
| Shuffle | Randomize a library. |
| Tap / Untap | Rotate a permanent 90° / return it upright. |

---

## Deciduous keywords

Available to any set, used when the design calls for them. Returning a deciduous keyword spends much less complexity budget than inventing a new mechanic.

Most-used in modern Magic:

- **Cycling [cost]** — `[cost], Discard this card: Draw a card.` Universally beloved. Smooths draws and adds modality. Color-shifts: cycling has a default color but lands of any color can have it.
- **Kicker [cost]** — `You may pay an additional [cost] as you cast this spell.` Modal-without-modes; the kicked effect appears in the rules text.
- **Flashback [cost]** — `You may cast this card from your graveyard for its flashback cost. Then exile it.` Graveyard-as-second-hand pillar enabler.
- **Surveil N** — `Look at the top N cards of your library, then put any number of them into your graveyard and the rest back on top in any order.` Slightly stronger scry; black/blue. Effectively evergreen since 2023.
- **Convoke** — `Your creatures can help cast this spell. Each creature you tap while casting it pays for {1} or one mana of that creature's color.` Token/wide strategies.
- **Prowess** — `Whenever you cast a noncreature spell, this creature gets +1/+1 until end of turn.` Was evergreen; now deciduous. Spell-matters indicator.
- **Disturb [cost]** — `You may cast this card from your graveyard transformed for [cost].` Innistrad return (2021). Transforms-from-graveyard. Pairs with double-faced cards.
- **Adventure** — Creature card with a separate adventure (instant/sorcery) half. Cast the adventure first, exile the card, then later cast the creature from exile. Eldraine/Wilds of Eldraine signature; returned in Final Fantasy.
- **Investigate** — `Create a Clue token. (It's a colorless artifact with "{2}, Sacrifice this artifact: Draw a card.")` Cards-as-tokens design space.
- **Treasure / Food / Blood / Map / Powerstone** — predefined artifact tokens that recur. Treasure in particular is now the universal "ramp/fix" token.
- **Modified** — Game term: a creature is modified if it has a counter on it, an Equipment attached, or an Aura you control attached. Used as a payoff condition (NEO, MH3).
- **Energy / {E}** — Resource counters players hold separately from life. Generated and spent. Returned in Modern Horizons 3 after Kaladesh.
- **Devoid** — `This card has no color.` Eldrazi-flavored colorless-but-with-mana-cost.

Other deciduous keywords that recur every few sets: Bestow, Dredge, Embalm, Eternalize, Fading, Echo, Madness, Morph, Manifest, Mutate (rare to return), Ninjutsu, Persist, Proliferate, Rebound, Replicate, Storm, Suspend, Threshold, Transmute, Unearth, Wither. Each carries baggage; check Storm Scale (`sources.md`) before reusing.

---

## Recent set mechanics (2024–2025)

A working summary of mechanics introduced in recent premier sets, so you can avoid re-treading recent ground or knowingly draw on it.

### Murders at Karlov Manor (Feb 2024) — mystery / detective

- **Disguise [cost]** — Cast face-down for {3} as a 2/2 colorless creature with ward {2}. Turn face up by paying [cost]. Morph evolved with built-in protection.
- **Cloak** — Same effect as disguise but as an instruction (e.g., "cloak the top card of your library"). Resulting face-down creature has ward {2}.
- **Suspect** — A suspected creature has menace and can't block. Ability word; appears on triggers like "Whenever this creature deals combat damage, suspect target creature."
- **Collect evidence N** — Cost: exile any number of cards from your graveyard with total mana value N or more.
- **Cases** — A new enchantment subtype with three lines: a static, a "to solve" condition that triggers each end step, and a "solved" payoff that activates only after solving.
- **Investigate** (returning) — see deciduous list above.

**Pillar lesson:** Detective fiction wanted the *play pattern* of "uncovering" — Cases and Disguise both deliver hidden information that gradually reveals. Mechanics matched flavor.

### Outlaws of Thunder Junction (Apr 2024) — Wild West heist

- **Outlaw** — A characteristic, not a keyword. A permanent is an outlaw if it has any of these creature types: Assassin, Mercenary, Pirate, Rogue, Warlock. Lets cards reference "outlaws you control" without listing five subtypes.
- **Committed a crime** — A trigger condition: you commit a crime when you cast a spell, activate an ability, or put a triggered ability on the stack that targets an opponent, an opponent's spell/ability, an opponent's permanent, or a card in an opponent's graveyard. Game-state ability word; cards say "Whenever you commit a crime, ..."
- **Spree** — Modal spell with multiple add-on modes, each with its own additional cost; you must choose at least one as you cast.
- **Plot [cost]** — `If this card is in your hand, you may pay [cost] and exile it: You may cast it as a sorcery on a later turn without paying its mana cost. Plot only as a sorcery.` Suspend without time counters.
- **Saddle N** — Tap any number of untapped non-Mount creatures you control with total power N or more. The Mount becomes saddled until end of turn. Activate only as a sorcery. (Mount is the new creature type, like Vehicle is for crew.)

### Bloomburrow (Aug 2024) — animal kindred

- **Offspring [cost]** — `As you cast this spell, you may pay an additional [cost]. If you do, when this creature enters, create a 1/1 token copy of it.`
- **Gift** — Optional promise made when casting. `As you cast this spell, you may promise a gift to an opponent. When [resolution condition], if a gift was promised, the chosen opponent [gift effect].` Triggers a different bonus for you than for them.
- **Valiant** — Ability word. Triggered abilities that fire whenever a creature you control becomes the target of a spell or ability you control for the first time each turn.
- **Forage** — Keyword action. To forage: either exile three cards from your graveyard, or sacrifice a Food.
- **Expend N** — Threshold tracker. Expend abilities trigger once per turn when you've spent N mana to cast spells that turn.
- **Pawprints** — Modal spell costing system: each mode costs a number of pawprints; choose modes summing to a stated max.

### Duskmourn: House of Horror (Sep 2024) — survival horror

- **Rooms** — A new enchantment subtype with two halves like split cards. Cast one half (a "door"); later, unlock the second door by paying its mana cost as a special action (sorcery speed, doesn't use the stack). Triggers fire on enter and on full-unlock.
- **Manifest dread** — Look at the top two cards of your library. Manifest one (face-down 2/2 creature) and put the other into your graveyard.
- **Eerie** — Ability word for triggers that fire whenever an enchantment you control enters and whenever you fully unlock a Room.
- **Survival** — Triggered ability. Triggers at the beginning of your second main phase if the creature is tapped.
- **Impending N — [cost]** — Alternative cost. The card enters as a non-creature with N time counters; remove one at each end step; becomes a creature when the last is removed.
- **Glimmer** — A cycle/group identifier in flavor; rules-light.
- **Overlord** — A cycle of mythic enchantment-creatures designed around impending.

### Foundations (Nov 2024) — evergreen revisit set

Foundations is a "core-set-style" product that re-introduces many older mechanics in a beginner-friendly context. Notable returns: **Cycling, Flashback, Flash, Kicker, Threshold**. Foundations is also where **Prowess was demoted from evergreen to deciduous**. Use Foundations as a reference for what feels classic and beginner-readable.

### Aetherdrift (Feb 2025) — racing

- **Start your engines!** — State-based ability. The first time you control a permanent with this, your speed becomes 1. Speed is a per-player resource (like life).
- **Speed N** — Tracking number. Speed increases by 1 (max 4) once per turn when an opponent loses life on your turn. Cards reference your speed for scaling effects.
- **Exhaust** — Activated abilities marked as exhaust can be activated only once per game (per object). If the permanent leaves and returns, it's a new object with a fresh exhaust.
- **Saddle** (returning, see OTJ).
- **Crew N** (returning evergreen for Vehicles) — Tap any number of other untapped creatures you control with total power N or more: this Vehicle becomes a creature until end of turn.
- **Pilot** — A creature subtype/static helper: pilots crew/saddle as if their power were 2 greater.

### Tarkir: Dragonstorm (Apr 2025) — clan-based dragon-storm return

Each clan gets a mechanic:

- **Endure N** (Abzan / WBG) — Choose: put N +1/+1 counters on the creature, OR create an N/N white Spirit creature token.
- **Flurry** (Jeskai / WUR) — Triggered ability. Triggers when you cast your second spell each turn.
- **Renew** (Sultai / UBG) — Activated graveyard ability that exiles the card as part of the cost; sorcery speed; usually puts counters on a creature.
- **Mobilize N** (Mardu / WBR) — Triggered ability. Whenever this creature attacks, create N tapped attacking 1/1 red Warrior tokens.
- **Harmonize [cost]** (Temur / URG) — Like flashback but specifically lets you tap creatures to reduce the harmonize cost.
- **Behold a [type]** — Choose a permanent you control of [type] OR reveal a card of [type] from your hand. Used as a trigger condition for big payoffs ("Whenever you behold a Dragon, ...").
- **Twobrid mana** — A monocolor hybrid: mana symbol can be paid with one mana of the indicated color OR with {2} generic mana.
- **Omens** — Spell cards with a creature face and an instant/sorcery face accessible from the same card (related to MDFC space).
- **Surveil** (returning).

### Final Fantasy (Jun 2025) — Universes Beyond

- **Job select** — Triggered ability on Equipment: when this Equipment enters, create a 1/1 colorless Hero creature token, then attach this Equipment to it.
- **Tiered** — Modal spell with three escalating modes; choose one as you cast and pay its additional cost. The mana value is fixed regardless of tier.
- **Saga creatures** — Saga subtype that is also a creature. Enters with a lore counter; gains a lore counter on the precombat main phase; sacrificed after the final chapter.
- **Adventures** (returning).
- **Landcycling** (returning).
- **Transforming DFCs** (returning).

---

## Static mechanic concepts to know

These aren't keywords but recur across recent sets and are worth designing fluently with.

- **Modal Double-Faced Cards (MDFCs)** — Two non-transforming faces; one is typically a land. From Zendikar Rising (2020) onward. Mulligan/flood insurance. MH3 expanded to cards that transform into planeswalkers.
- **Sagas** — Enchantments that gain lore counters and trigger chapter abilities, then are sacrificed. Three or four chapters typical.
- **Battles / Sieges** — Card type introduced in March of the Machine (2023). Has defense counters; opponent can attack it. Sieges have a back face you transform into when defense reaches 0.
- **Class enchantments** — Tiered enchantments you can pay to "level up." From Adventures in the Forgotten Realms.
- **Vehicles** — Artifact subtype with crew. Become creatures temporarily.
- **Mounts** — Creature type; saddle is the activation pattern.
- **Predefined artifact tokens** — Treasure ({T}, sac: add one mana), Food (2, T, sac: gain 3 life), Clue ({2}, sac: draw), Blood ({1}, T, sac, discard: draw), Map ({1}, T, sac: target creature explores), Powerstone ({T}: add {C}, can't be spent on nonartifact). Use these instead of inventing one-off tokens for the same job.
- **Counters as resources** — +1/+1 (everywhere), -1/-1 (Amonkhet, Hour, NEO), Charge (artifacts), Loyalty (planeswalkers), Lore (Sagas), Time (Suspend / Impending), Energy ({E}), Defense (Battles), Stun, Shield, Oil, Ki, Verse, Rad, Finality. Don't invent a new counter type unless your set's mechanic genuinely requires it.

---

## How to use this catalog

When choosing your set's named mechanics:

1. **Inventory the evergreens you want to emphasize.** You don't need all of them; pick the 4–6 that give the set its feel.
2. **Check the deciduous list for cheap options.** A returning mechanic costs less complexity than a new one; if the set's pillars are served by Cycling or Flashback, you've saved a slot.
3. **Read the recent-set list to avoid recent territory.** If you're considering "graveyard exile costs," note that Collect Evidence (MKM) just did that. If you're considering "alt-cost from hand," note Plot (OTJ) and Impending (DSK) recently did variations.
4. **Spend your new-mechanic slots on what isn't covered.** New mechanics earn their cost when they unlock design space the deciduous list can't reach.

Cross-check every named mechanic candidate against `mechanics.md` for parasitism, complexity budget, and pillar alignment. Cross-check templating against `templating.md` (if present) and the Comprehensive Rules cited in `sources.md`.
