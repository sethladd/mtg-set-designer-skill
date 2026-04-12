# Editor Wisdom Catalog

Errata failure stories, templating evolution, ambiguity patterns, and named checks for Magic card editing. Every erratum is a templating failure story — this catalog ensures the same mistakes are never repeated.

---

## Errata Failure Stories

### 1. Hostage Taker — Missing "another" creates infinite loop

**Printed:** Could target "a creature or artifact" — without "another," it could target itself. On an empty board, the ETB exiled Hostage Taker itself, which re-entered and re-triggered, creating a mandatory infinite loop forcing a draw.
**Fix:** Added "another" to the targeting text. One word fixed the problem.
**Principle:** Always include "another" or "other" when a permanent's ability could target itself. Test edge cases on empty boards.

### 2. Marath, Will of the Wild — Missing "X can't be 0"

**Printed:** Abilities paid X to deal damage, create tokens, or distribute counters. Without a minimum, X=0 activations were free, enabling infinite combos.
**Fix:** Day-zero errata adding "X can't be 0."
**Principle:** Any variable cost (X) must specify minimum values. Free activations are almost always broken.

### 3. Companion Mechanic — Entire mechanic errata

**Printed:** Cast companion directly from outside the game — a free extra card every game.
**Fix:** Changed to require 3 mana to move companion from sideboard to hand. First time an entire mechanic received power-level errata.
**Principle:** Mechanics that bypass fundamental game costs (drawing, mana) need safety valves built into the template, not bolted on after.

### 4. Don't Try This at Home — Trigger vs. replacement effect confusion

**Printed:** Used "whenever" for what should have been a replacement effect on damage modification.
**Problem:** As a trigger, the damage modification went on the stack and could be responded to.
**Fix:** Changed to "If a hot source you control would deal damage... it deals that much damage plus 1 instead."
**Principle:** Damage modification effects MUST use "if...would...instead" replacement templating. Never use "whenever" for replacements.

### 5. Oblivion Ring — Two-ability exploit

**Design:** Used two separate triggered abilities — one to exile, one to return. Players exploited this by flickering O-Ring with the exile trigger on the stack, permanently exiling the target.
**Fix:** Banishing Light combined both into a single ability: "for as long as ~ remains on the battlefield."
**Principle:** Exile-then-return effects should be single abilities with duration-based returns, not paired triggers.

### 6. Phyrexian Dreadnought — Power-level errata reversed

**What happened:** Power-level errata changed the card so creatures had to be sacrificed BEFORE it entered play, preventing Stifle tricks. In 2006, WotC reversed ALL power-level errata, establishing: "cards should do what they say."
**Principle:** Never use errata to fix power-level problems. Use the ban list instead.

### 7. Animate Dead — Oracle text nightmare

**Problem:** Original text was intuitive but incompatible with modern rules. Current Oracle text requires paragraphs to express what was originally a few sentences.
**Principle:** Design new cards to work within the current rules framework rather than fighting it. Some early Magic designs simply cannot be cleanly expressed in modern templating.

### 8. Guidelight Pathmaker — Conditional shuffle

**Printed:** "Then shuffle."
**Fix:** Changed to "If you search your library this way, shuffle" — because the shuffle should only happen if the search actually occurred.
**Principle:** Shuffle instructions must be conditional on whether a library search actually happened.

### 9. Ice Cauldron — Worst Oracle text

**Problem:** Original functionality requires Oracle text so convoluted it's considered the single worst Oracle text ever printed.
**Principle:** If a card's functionality cannot be expressed concisely, the design itself is the problem — not the templating.

### 10. "Unblockable" → "can't be blocked"

**What happened:** "Unblockable" was used informally as if it were a keyword, but it wasn't one. Cards varied between "is unblockable" and "can't be blocked," creating confusion about whether it was a keyword.
**Fix:** Standardized to "can't be blocked" (and variants like "can't be blocked by creatures with power 2 or less") starting with Magic 2014.
**Principle:** If something isn't a keyword, don't template it as if it were one.

---

## The Templating Evolution

### Major Changes and Their Reasons

| Era | Old templating | New templating | Why it changed |
|-----|---------------|----------------|----------------|
| M10 (2009) | "in play" | "the battlefield" | "In play" was ambiguous — did it include the stack? |
| M10 (2009) | "removed from game" | "exiled" | "Removed from game" implied permanence, but cards often returned |
| M10 (2009) | "play a spell" | "cast a spell" | "Play" was overloaded (play a land, play a spell, play the game) |
| M14 (2013) | "Indestructible" (adjective) | "Indestructible" (keyword) | Consistency with other keyword abilities |
| M14 (2013) | "is unblockable" | "can't be blocked" | "Unblockable" falsely read as a keyword |
| KLD (2016) | "Put a token onto the battlefield" | "Create a token" | Shorter, cleaner, consistent verb |
| KLD (2016) | "Æ" ligature | "Ae" | Digital compatibility |
| DOM (2018) | "Add {X} to your mana pool" | "Add {X}" | "Mana pool" confused new players |
| DOM (2018) | "he or she" | "they" | Inclusive language, saves space |
| DOM (2018) | "Card name" for self on stack | "this spell" | Clearer timing for stack-based abilities |
| DOM (2018) | Damage "redirected" to planeswalkers | "any target" | Redirect rule was unintuitive |
| M21 (2020) | "Put top N into graveyard" | "Mill N" | Consistently used effect deserved a keyword action |
| KTK (2014) | "Choose one —" (italicized) | Bullet-pointed modes | Visual clarity for modal spells |
| BLB (2024) | "enters the battlefield" | "enters" | Space savings; already proven in Saga reminder text |
| FDN (2024) | Card name self-reference | "this creature/spell/card" | Eliminated confusion about copies vs. the specific card |

### The Self-Reference Decision Tree (post-Foundations 2024)

| Zone | Template | Example |
|------|----------|---------|
| Battlefield (permanent) | "this [type]" | "When this creature enters..." |
| Stack (spell) | "this spell" | "This spell costs {1} less..." |
| Graveyard/hand/library/exile | "this card" | "You may cast this card from your graveyard" |
| Cross-zone (multiple zones) | Card name | Necessary for clarity |
| Legendary permanent | Character name | "Aragorn gets +1/+1..." |
| Granted ability (aura/equipment) | Card name | "Equipped creature has 'Whenever ~ attacks...'" |
| Transform DFC | Face name | Specific face reference needed |

---

## Common Templating Mistakes

### The Dirty Dozen

1. **Missing "another" on self-targeting** — Any ETB exile/target ability needs "another" to prevent self-targeting loops.

2. **"Whenever" for replacement effects** — Damage modification, death replacement, and similar effects MUST use "if...would...instead" templating. "Whenever" creates triggers that go on the stack.

3. **Missing "may" on optional abilities** — If an ability forces an undesirable action (sacrifice, discard), it needs "may" unless the downside is intentional design.

4. **Forgetting "you control"** — "Creatures get +1/+1" boosts ALL creatures. "Creatures you control get +1/+1" is almost always what you mean.

5. **Redundant "from your hand"** after "discard" — "Discard" already means "from your hand." Writing both is redundant and violates modern templating.

6. **Capitalizing keywords in rules text** — Keywords are lowercase in rules text ("flying" not "Flying"). Card names are capitalized. Zones are lowercase ("the battlefield," "the graveyard").

7. **Conflicting abilities** — Giving a creature "can't be blocked" AND trample serves no purpose (trample only matters when blocked).

8. **Wrong activation cost ordering** — Correct: mana cost, then {T}, then other costs (sacrifice, discard, pay life), separated by commas, then colon, then effect.

9. **Missing duration** — Effects without specified duration are permanent. Forgetting "until end of turn" on pump effects makes them last forever.

10. **Using "destroy" when "sacrifice" is meant** — "Destroy target creature you control" is worse than "Sacrifice a creature" — the first can be prevented by indestructible, the second cannot.

11. **"Put into graveyard" instead of "dies"** — Since M14, "dies" means "is put into a graveyard from the battlefield." Using the longer form is outdated.

12. **Unconditional shuffle after optional search** — If a library search uses "you may," the shuffle must be conditional: "If you do, shuffle."

---

## Named Checks

### 1. The Self-Reference Audit

For every card, verify the self-reference template matches the zone:
- On battlefield → "this [type]" (or character name if legendary)
- On stack → "this spell"
- In other zones → "this card"
- Cross-zone → card name (only when necessary)

### 2. The Trigger Word Check

- "When" → one-time trigger (ETB, dies)
- "Whenever" → repeatable trigger (attacks, casts a spell)
- "At" → phase/step trigger (beginning of upkeep, end of turn)

Verify each card uses the right trigger word for the expected frequency.

### 3. The Replacement Effect Audit

Any effect that modifies damage, prevents death, changes how something enters, or replaces drawing must use "if...would...instead" templating. Flag any "whenever" that describes a replacement.

### 4. The "Another" Check

Every ETB ability that targets a creature, artifact, enchantment, or permanent must include "another" if self-targeting would be problematic. Especially critical for exile effects.

### 5. The Type-Line Consistency Check

- Equipment → must have Equip cost in rules text
- Vehicle → must have Crew cost and P/T
- Aura → must have "Enchant [target]" in rules text
- Saga → must have chapter abilities (I, II, III)
- If rules text references subtypes, the type line must include them

### 6. The Keyword Hygiene Check

- Evergreen keywords: lowercase in rules text, no quotation marks
- Ability words: italicized, followed by em-dash, no rules meaning
- Set-specific keywords: include reminder text at common/uncommon
- Verify no made-up keywords (check against evergreen + deciduous + set-mechanic lists)

### 7. The Text Box Budget Check

- Count lines of rules text (7 lines = comfortable, 9 = maximum at rare/mythic)
- If rules text exceeds 9 lines, the card needs: cut reminder text, simplify, or bump rarity
- Only rare/mythic may use microtext (7.5pt minimum)
- Verify flavor text fits after rules text (at rare/mythic especially)

### 8. The Collector Number Assignment

Order: W → U → B → R → G → Multicolor (alphabetical within) → Artifacts → Lands
Within each color/section: alphabetical by card name.

### 9. The Name Conflict Check

Every card name must be unique across the entire history of Magic. Search Scryfall for exact name matches. Names that are too similar to existing cards (differing by one word) should also be flagged.

### 10. The Mana Cost Ordering Check

Verify mana costs follow WUBRG ordering:
- Colorless first: {2}{W}{U} not {W}{U}{2}
- Allied pairs: {W}{U}, {U}{B}, {B}{R}, {R}{G}, {G}{W}
- Enemy pairs: {W}{B}, {U}{R}, {B}{G}, {R}{W}, {G}{U}
