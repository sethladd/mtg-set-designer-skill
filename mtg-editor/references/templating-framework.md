# Templating Framework

Operational reference for rules text templating, reminder text, keyword conventions, text box fitting, and collector number assignment. This is the editor's handbook — consult it for every card.

---

## Modern Templating Conventions (2024+)

### Zone-Based Self-Reference

Cards no longer use their own name to self-reference (except in specific exceptions). Use the self-reference decision tree:

| Zone | Template | Example |
|------|----------|---------|
| Battlefield | "this creature" / "this artifact" / "this enchantment" | "When this creature enters, draw a card." |
| Battlefield (subtype) | "this Equipment" / "this Vehicle" / "this Aura" | "Equipped creature gets +2/+0." |
| Stack | "this spell" | "This spell costs {1} less to cast..." |
| Graveyard/Hand/Library/Exile | "this card" | "You may cast this card from your graveyard." |
| Cross-zone | Card name | Only when referencing from one zone to another |
| Legendary permanent | Character name (shortened if needed) | "Aragorn gets +1/+1 for each..." |
| Granted ability | Card name | "Equipped creature has '...'" |
| Transform DFC | Face name | Each face references itself by name |

### Current Verb and Phrase Standards

| Old | Current | Since |
|-----|---------|-------|
| "enters the battlefield" | "enters" | Bloomburrow (2024) |
| "Add {X} to your mana pool" | "Add {X}" | Dominaria (2018) |
| "he or she" | "they" | Dominaria (2018) |
| "Put a [token] onto the battlefield" | "Create a [token]" | Kaladesh (2016) |
| "Put top N cards into graveyard" | "Mill N" | Core Set 2021 (2020) |
| "removed from game" | "exiled" | M10 (2009) |
| "in play" | "on the battlefield" | M10 (2009) |
| "play a spell" | "cast a spell" | M10 (2009) |
| "is unblockable" | "can't be blocked" | M14 (2013) |
| "Leaves the battlefield" | Still "leaves the battlefield" | NOT shortened (cards leave other zones too) |

### Trigger Word Conventions

| Word | Usage | Expected frequency |
|------|-------|-------------------|
| "When" | One-time events | ETB, dies, single occurrence |
| "Whenever" | Repeatable events | Attacks, casts a spell, gains life |
| "At" | Phase/step events | "At the beginning of your upkeep" |

All three are functionally identical rules-wise; the distinctions communicate expected frequency to players.

### Replacement Effect vs. Triggered Ability

| Pattern | Type | Goes on stack? |
|---------|------|----------------|
| "If [event] would [occur], [effect] instead" | Replacement | No |
| "As [event]..." | Replacement | No |
| "When/Whenever/At [event], [effect]" | Triggered | Yes |

**Critical rule:** Damage modification, death prevention, entering-as-a-copy, and similar effects MUST be replacement effects. Using trigger templating for these creates rules errors.

### Targeting Conventions

| Template | Chosen when | Hexproof interaction |
|----------|-------------|---------------------|
| "Target [type]" | On announcement | Blocked by hexproof/shroud |
| "Choose [type]" | On resolution | Ignores hexproof |
| "Any target" | On announcement | Shorthand for "creature, player, or planeswalker" |

---

## Keyword Hierarchy

### Evergreen Keywords (always available, expected in most sets)

**Keyword Abilities:** Deathtouch, Defender, Double strike, Enchant, Equip, First strike, Flash, Flying, Haste, Hexproof, Indestructible, Lifelink, Menace, Reach, Trample, Vigilance, Ward

**Keyword Actions:** Activate, Attach, Cast, Counter, Create, Destroy, Discard, Exchange, Exile, Fight, Mill, Play, Reveal, Sacrifice, Scry, Search, Shuffle, Tap/Untap

### Deciduous Keywords (available in any set, not expected in every set)

Cycling, Kicker, Flashback, Sagas, Vehicles, Treasure tokens, Food tokens, Clue tokens/Investigate, Blood tokens, Hybrid mana, Double-faced cards, Protection, Prowess, Affinity, Surveil, Landfall, Split cards, Curses, Colored artifacts, Anchor words

### Ability Words (italicized, no rules meaning, flavor label)

Ability words are italicized and followed by an em-dash. They have NO rules meaning — removing them doesn't change the card's function. Current examples: landfall, delirium, constellation, domain, revolt, raid, morbid, threshold, metalcraft, heroic, magecraft, alliance, celebration, valiant, descend, eerie, survival, flurry, paradox, void...

### Set-Specific Keywords

Each set introduces 2-4 named mechanics. These get reminder text at common and uncommon. At rare/mythic, reminder text may be dropped if space is tight.

---

## Reminder Text Guidelines

### When to Include

| Rarity | Core Set | Expansion Set |
|--------|----------|---------------|
| Common | Always for ALL keywords | Always for set-specific; usually for evergreen |
| Uncommon | Always | Usually |
| Rare | Usually | When space allows |
| Mythic | When space allows | Can drop if tight |

### When to Drop

1. Card has too much rules text to fit reminder text
2. The keyword is evergreen AND the card is rare/mythic in an expansion
3. Multiple keywords on one card — drop the most familiar one's reminder text

### Reminder Text Format

Always in parentheses and italicized: *(Reminder text goes here.)*

Reminder text is always a complete sentence or clause within parentheses.

---

## Text Box Budget

### Line Counts

| Lines | Assessment | Allowed rarities |
|-------|-----------|-----------------|
| 1-3 | Simple card | All |
| 4-6 | Standard complexity | All |
| 7-8 | Complex | Common (if justified), Uncommon+ |
| 9-10 | Very complex | Rare and Mythic only |
| 11+ | Exceeds budget | Needs simplification |

### Font Size Rules

| Size | Name | Allowed |
|------|------|---------|
| 9pt | Standard | All cards |
| 8pt | Reduced | Rare and Mythic |
| 7.5pt | Microtext | Rare and Mythic only (absolute minimum) |

**If a common or uncommon needs smaller than 9pt font, the card is too complex for its rarity.** Either simplify the text, cut reminder text, or bump to rare.

### Fitting Rules Text + Flavor Text

Priority when text box is full:
1. Cut reminder text (most expendable)
2. Cut flavor text (second most expendable)
3. Shrink font to 8pt (rare/mythic only)
4. Shrink font to 7.5pt microtext (rare/mythic only, last resort)
5. Simplify the mechanic (if all else fails)

Flavor text is expected on: all rares/mythics, at least 30% of commons/uncommons.

---

## Ability Ordering on Cards

Standard sequence (top to bottom):

1. **Keyword abilities** — listed on one line, comma-separated: "Flying, vigilance"
2. **Static abilities** — passive effects that are always on
3. **Triggered abilities** — "When/Whenever/At..." in life-cycle order:
   - ETB triggers first
   - Battlefield-relevant triggers (attack, block, damage)
   - Leaves-the-battlefield / death triggers last
4. **Activated abilities** — "Cost: Effect" format
   - Mana-producing abilities go after other activated abilities
   - Multiple activated abilities follow WUBRG cost ordering

---

## Activation Cost Format

Correct ordering of costs before the colon:

```
{mana}, {T}, [other costs]: [effect]
```

1. Mana cost (in WUBRG order, colorless first)
2. Tap symbol ({T}) or untap symbol ({Q})
3. Other costs (sacrifice, discard, pay life) — separated by commas
4. Colon
5. Effect

Example: `{2}{B}, {T}, Sacrifice a creature: Draw two cards.`

---

## Collector Number Assignment

### Standard ordering:

1. **White** (alphabetical)
2. **Blue** (alphabetical)
3. **Black** (alphabetical)
4. **Red** (alphabetical)
5. **Green** (alphabetical)
6. **Multicolor** (alphabetical, with hybrid cards placed by their color identity)
7. **Artifacts** (alphabetical, colorless only)
8. **Lands** (alphabetical)

Within each section, cards are sorted alphabetically by name.

### Special cases:
- Double-faced cards: numbered by their front face's color
- Artifacts with colored mana in activation costs: still in artifact section (colorless identity)
- Artifacts with colored mana costs: placed in their color's section

---

## The Complete Templating Checklist (Per Card)

Run this on every card:

1. **Self-reference** — Uses correct zone-based template (this creature/spell/card)?
2. **Modern verbs** — "enters" not "enters the battlefield," "create" not "put a token," etc.?
3. **Trigger words** — Correct word for expected frequency (when/whenever/at)?
4. **Replacement effects** — Uses "if...would...instead" not "whenever" for replacements?
5. **"Another" check** — ETB targeting abilities include "another" to prevent self-loops?
6. **"You control" check** — Permanent-affecting abilities specify "you control" if intended?
7. **"May" check** — Optional actions include "may"?
8. **Type-line consistency** — Equipment has Equip, Vehicle has Crew, Aura has Enchant, Saga has chapters?
9. **Keyword formatting** — Lowercase in rules text, correct spelling, comma-separated?
10. **Ability ordering** — Keywords → static → triggered → activated?
11. **Activation cost ordering** — Mana → tap → other costs → colon → effect?
12. **Mana cost ordering** — Colorless first, then WUBRG?
13. **Reminder text** — Present where required by rarity guidelines?
14. **Text box budget** — Fits within line limit for rarity? Font size appropriate?
15. **Collector number** — Correct position in WUBRG → multi → artifact → land ordering?
16. **Name uniqueness** — No conflict with existing Magic card names?
17. **Duration specified** — Temporary effects include "until end of turn"?
18. **Conditional shuffle** — Library searches with "may" have conditional shuffle?
