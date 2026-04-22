# Templating Quick Reference for Vision Design

A pocket reference for writing rules text in `vision_cardfile.json`. The vision designer is producing a *prototype* — Set Design will revise, and the Editor skill will template every card before print. But your prototype text should still be readable, valid, and follow current conventions, or downstream readers will have to translate it before they can evaluate the design.

For the comprehensive templating manual (zone-based self-reference, ability ordering, text-box budgeting, collector-number assignment, the full per-card checklist), defer to the `mtg-editor` skill's `references/templating-framework.md`. This file covers only what you need at vision time.

---

## The single biggest 2024 change

**"Enters the battlefield" became "enters" (Bloomburrow, Aug 2024).**

Old: `When CARDNAME enters the battlefield, draw a card.`
New: `When this creature enters, draw a card.`

Two changes happened at once:
1. Self-reference by zone, not by name (`this creature` instead of `CARDNAME`).
2. Drop the redundant "the battlefield" because "enters" without qualification means battlefield (cards entering other zones are templated explicitly).

If you write old-template prototype text, the Editor will rewrite it. If you write a few hundred cards in old template, the Editor's output diff will be enormous and meaningless. Use the new template from the start.

---

## Self-reference by zone (the "this object" rule, Foundations 2024)

Cards no longer reference themselves by name on most templates. Use the zone the card is in:

| Where the card is | What to write |
|---|---|
| Battlefield (creature) | `this creature` |
| Battlefield (artifact) | `this artifact` |
| Battlefield (enchantment) | `this enchantment` |
| Battlefield (Equipment / Vehicle / Aura — by subtype) | `this Equipment` / `this Vehicle` / `this Aura` |
| Stack (a spell as it's being cast) | `this spell` |
| Graveyard / hand / library / exile | `this card` |
| Granted to another permanent ("gains '...'") | Use the original card's name |
| Cross-zone reference (rare) | Use the original card's name |
| Legendary creature | The character name (often shortened) |

Examples:
- `When this creature enters, scry 1.`
- `This spell costs {1} less to cast if you control a Bird.`
- `You may cast this card from your graveyard for its flashback cost. Then exile it.`
- `Equipped creature has "Whenever this creature attacks, draw a card."` (granted ability uses card name pattern; here the granted ability is on the equipped creature, so use its zone reference — but the *granting* card's text is "equipped creature has...")

---

## Trigger words

All three are functionally equivalent rules-wise; the choice signals frequency to the reader.

- **`When [event], [effect]`** — one-time event. Most common: `When this creature enters, ...`, `When this creature dies, ...`
- **`Whenever [event], [effect]`** — recurring event. `Whenever this creature attacks, ...`, `Whenever you cast a spell, ...`
- **`At [phase/step], [effect]`** — phase-based. `At the beginning of your upkeep, ...`, `At the beginning of your end step, ...`

If a trigger could plausibly fire repeatedly (every attack, every spell cast), use `whenever`. If it can fire only once (entering the battlefield, dying), use `when`.

---

## Replacement effects vs. triggers

A replacement effect changes how an event happens; it doesn't go on the stack. A triggered ability fires when an event happens; it does go on the stack.

- **Triggered:** `When this creature enters, you gain 2 life.` → goes on stack, can be responded to.
- **Replacement:** `If this creature would deal damage to a player, instead it deals that much damage and you gain that much life.` (lifelink-shape) → does not go on stack.
- **Replacement (entry alteration):** `This creature enters with three +1/+1 counters on it.` → does not go on stack.

For damage modification, death prevention, "instead" effects, and "enters with counters" — write replacement, not trigger. Common shape: **`If [event] would [happen], instead [different thing happens].`**

If you write a replacement effect using "whenever" templating, the rules behave very differently than you intended. This is the most common templating bug in prototype card text.

---

## Targeting words

- **`target [type]`** — a target chosen on announcement; subject to ward/hexproof/protection.
- **`any target`** — shorthand for "creature, player, or planeswalker; or a battle"; also a target.
- **`choose [type]`** — chosen on resolution; *not* a target. Doesn't trigger ward, isn't blocked by hexproof.
- No "target" / "choose" word — affects everything in the description (e.g., `Each creature gets +1/+1 until end of turn`).

Use `target` by default for single-permanent effects. Use `choose` only when you specifically want to bypass ward/hexproof — and know you're doing it.

---

## Common 2024-current verb shifts

Use these forms in prototype text. The Editor will catch the rest.

| Don't write | Write |
|---|---|
| `enters the battlefield` | `enters` |
| `Add {X} to your mana pool` | `Add {X}` |
| `put a token onto the battlefield` | `create a token` |
| `put the top N cards into [their] graveyard` | `mill N` |
| `removed from game` | `exiled` |
| `in play` | `on the battlefield` |
| `play a spell` | `cast a spell` |
| `is unblockable` | `can't be blocked` |
| `he or she` | `they` |
| `CARDNAME` (self-reference on most cards) | `this creature` / `this card` / etc. |

Note: `leaves the battlefield` is *not* shortened — "leaves" alone is ambiguous because cards leave many zones.

---

## Activated ability cost ordering

Costs go before the colon, in this order:

1. Mana cost (colorless first, then WUBRG)
2. Tap symbol `{T}` or untap `{Q}`
3. Other costs (sacrifice, discard, pay life, exile from graveyard) — comma-separated

Then `:` then effect.

Example: `{2}{B}, {T}, Sacrifice a creature: Draw two cards.`

Mana cost ordering inside the curly braces: generic first, then WUBRG. So `{1}{W}{U}` not `{W}{U}{1}`.

---

## Ability ordering on a card

Top to bottom:

1. **Keyword abilities** — comma-separated on one line: `Flying, vigilance, lifelink`.
2. **Static abilities** — passive effects: `Other Goblins you control get +1/+0.`
3. **Triggered abilities** — life-cycle order: ETB triggers, then on-attack/block/damage, then leaves-battlefield/death triggers.
4. **Activated abilities** — `Cost: Effect`. Mana abilities last.

Don't worry about strict ordering at vision time, but get the keyword line correct (it should be one comma-separated line at the top).

---

## Reminder text

- Always in *italicized parentheses*: `(Reminder text.)` — written as `*(...)*` in markdown.
- At vision time, include reminder text for every set-specific named mechanic at every rarity. The Editor will trim later based on space.
- Don't write reminder text for evergreens at common — the player knows what flying does.

---

## The "another" trap

ETB abilities that target other things on the battlefield must say `another`, or the card targets itself and creates an infinite loop or weird interaction. The classic failure case: Hostage Taker (which had to be errata'd because it could exile itself).

- **Wrong:** `When this creature enters, exile target nonland permanent.`
- **Right:** `When this creature enters, exile another target nonland permanent.`

If your ETB targets the type of thing this card is, ask whether it should target *another*.

---

## "You control" check

Rules text that affects permanents needs to specify whose permanents. Default: the controller's.

- **Ambiguous:** `Whenever a creature dies, draw a card.` — fires for any creature owned by anyone.
- **Probably intended:** `Whenever a creature you control dies, draw a card.`

Include `you control` whenever you mean "yours."

---

## "May" for optional

Optional actions need `may`:

- **Wrong:** `When this creature enters, draw a card, then discard a card.` (mandatory)
- **Right (if optional):** `When this creature enters, you may draw a card. If you do, discard a card.`

The `may`/`if you do` pattern is common for optional drawback effects.

---

## Duration

Temporary effects always specify duration. Default for combat tricks: `until end of turn`.

- `Target creature gets +2/+2 until end of turn.`
- `Target creature gains flying until end of turn.`

Without `until end of turn`, the effect is permanent — usually not what you meant.

---

## Type-line consistency

The type line implies certain abilities; missing them is a templating bug:

| Type | Required ability |
|---|---|
| Equipment (Artifact — Equipment) | An `Equip {cost}` ability |
| Vehicle (Artifact — Vehicle) | A `Crew N` ability |
| Aura (Enchantment — Aura) | An `Enchant [type]` ability |
| Saga (Enchantment — Saga) | Roman-numeral chapter abilities |
| Battle (specifically Siege) | A defense counter number; a back face |

If the type line says Equipment, the rules text must include Equip. The Editor will catch missing pieces, but it's faster to write it right.

---

## Vision-time templating priorities

You don't need to be perfect; you need to be readable. In priority order:

1. **Use current verb forms** (`enters`, not `enters the battlefield`).
2. **Use zone-based self-reference** (`this creature`, not `CARDNAME`).
3. **Distinguish replacement effects from triggers** (`if X would Y, instead Z` vs. `whenever X`).
4. **Get keyword spelling and ordering right** (one comma-separated line).
5. **Include `another` and `you control` where they matter.**
6. **Include `may` and `until end of turn` where they apply.**

The Editor will fix everything else. But hitting these six saves Set Design and the Editor a lot of time, and makes your prototype card text actually evaluable as a design.

---

## When you need more

For anything more nuanced — text-box budget, specific keyword reminder text, collector numbering, microtext rules, granted-ability self-reference, planeswalker loyalty templating, MDFC templating, the full per-card checklist — defer to the `mtg-editor` skill's `references/templating-framework.md`. The vision designer doesn't need to ship print-ready text; it needs to ship designable text.
