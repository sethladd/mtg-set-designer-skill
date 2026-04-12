# Product Architecture Framework

An operational handbook for defining the product suite around a Magic: The Gathering set. This is the decision-making guide for determining what products the set appears in, how Commander precons complement the main set, and how to identify the marketing hooks that drive sales.

---

## 1. Modern Product Suite Definition

A standard premier Magic set (as of 2024) includes:

| Product | Audience | Contents | Price Range |
|---------|----------|----------|-------------|
| **Play Boosters** | Drafters, casual openers, competitive players | 14 cards: 1+ rare/mythic, 1 foil, 6 commons, 3 uncommons, 1 wildcard, 1 land, 1 art/token/List card | ~$5-6 per pack |
| **Collector Boosters** | Collectors, whales, premium seekers | 15 cards: multiple foils, showcase/borderless/extended art treatments, guaranteed foil rare+ | ~$25-30 per pack |
| **Commander Decks** | Commander players, new-to-Commander players | 100-card ready-to-play deck, 10-15 new cards, 2-card collector booster sample | ~$45-55 per deck |
| **Bundle** | Gift buyers, casual collectors | 9 Play Boosters, foil promo, alt-art lands, dice, storage box | ~$50 |
| **Starter Kit** | New players | 2 ready-to-play 60-card decks, learn-to-play guide | ~$15-20 |

### Product Suite Decision Tree

1. **Is this a premier set?** → Full suite (Play Boosters, Collector Boosters, Commander decks, Bundle)
2. **Is this a supplemental set?** (Masters, Horizons) → Play Boosters + Collector Boosters only (no precons)
3. **Is this a Commander-focused product?** → Commander decks only (possibly with Collector Boosters)
4. **Is this a UB set?** → Full suite, with IP-themed precons and IP-themed treatments

---

## 2. Commander Precon Design

### Theme Selection Process

1. **Identify the main set's mechanical axes** — What are the set's 3-5 pillar mechanics and 10 draft archetypes?
2. **Find complementary themes** — Which mechanical axes can support a 100-card singleton deck? Look for themes that are:
   - Deep enough (25+ on-theme cards available between set + existing Magic cards)
   - Color-pair or three-color focused (not mono-color, not five-color)
   - Distinct from each other (no two precons fighting over the same cards)
3. **Choose 2-4 themes** per premier set (2 for smaller sets, 4 for major releases)
4. **Ensure color coverage** — The combined precons should touch all five colors. Avoid putting two precons in the same color pair

### Power Level Targeting

The Commander precon power level sweet spot:

| Power Scale | Description | Target? |
|-------------|-------------|---------|
| 1-3 | Kitchen table jank | Too weak — frustrating out of box |
| 4-5 | Casual but unfocused | Too weak — loses to upgraded precons |
| **6-7** | **Focused casual** | **YES — wins at casual tables, upgradeable** |
| 8 | Optimized | Too strong — individual cards warp format |
| 9-10 | cEDH | Far too strong — creates must-buy obligations |

### Precon Commander Design Rules

1. **Color identity** — 2-3 colors matching the precon's theme
2. **Build-around ability** — The commander should clearly signal what the deck does ("+1/+1 counters matter," "spells from graveyard," "artifact tokens")
3. **Not format-breaking** — The commander should be exciting for the precon but not become the #1 commander in the format
4. **Legendary creature** — Always a creature (not a planeswalker commander) for maximum accessibility
5. **Backup commander** — Include a second legendary creature in the precon's colors that offers an alternative strategy

### New Card Design Constraints

Each precon includes 10-15 new cards. These must:
- Support the precon's theme without being format staples outside it
- NOT include free spells, zero-mana value engines, or scaling effects that break in multiplayer
- Include at least 1 splashy mythic-feel card (even if technically rare) for excitement
- Be specific enough to the theme that they're not auto-includes in every deck of their colors

### Mana Base Quality Floor

A precon mana base must be FUNCTIONAL, not optimal:
- At minimum: the relevant tri-land or check/fast lands for the color pair
- Command Tower (always)
- 3-5 dual lands that enter untapped conditionally
- The rest basics — but with a reasonable split (not 30 of one color in a three-color deck)
- Sol Ring (always — it's expected)

---

## 3. Poster Card Identification

### How to Find the 3-5 Cards That Sell the Set

Run each mythic and premium rare through these filters:

1. **Tournament impact** — Will this see play in Standard, Pioneer, Modern, or Legacy? Tournament-playable mythics drive competitive pack-cracking
2. **Commander appeal** — Is this a potential commander or auto-include in popular strategies? Commander drives the plurality of Magic sales
3. **Character recognition** — Is this a beloved character (planeswalker, legendary creature)? Familiar names drive pre-orders
4. **Unique effect** — Does this do something no other card does? Novelty drives discussion and previews
5. **Visual impact** — Is the art memorable? Will this look stunning in premium treatment?

A card that passes 3+ filters is a poster card. A set needs at least 3 poster cards, ideally spread across different colors and different filter categories.

### Poster Card Distribution Rule

- At least 1 poster card should be a legendary creature (Commander hook)
- At least 1 poster card should be a powerful non-creature spell (competitive hook)
- At least 1 poster card should be at mythic in a color that ISN'T the set's "headline color" — every color needs a reason to buy

---

## 4. Special Treatment Selection

### Which Cards Get Treatments

| Treatment Type | Allocation | Selection Criteria |
|---------------|------------|-------------------|
| **Showcase frame** | All mythics + selected rares + selected uncommons | Cards that exemplify the set's theme; the showcase frame itself should reinforce the set's visual identity |
| **Borderless art** | All planeswalkers + selected mythics | Cards with art that benefits from full-bleed display; often poster cards |
| **Extended art** | All rares + all mythics (Collector Booster only) | Universal — every rare/mythic gets this for collectors |
| **Full-art lands** | Basic lands | Every set should have some form of enhanced basic lands |
| **Textured foil** | 2-5 cards per set (Collector Booster only) | The most iconic cards — ultra-premium chase |
| **Serialized** (if used) | 1-2 cards per set | Only for truly special cards — overuse cheapens the mechanic |

### Treatment Theme Design

The showcase frame should reinforce the set's identity:
- Eldraine → storybook frames with aged paper texture
- Kamigawa: Neon Dynasty → ukiyo-e/cyberpunk soft-glow frames
- Innistrad: Midnight Hunt → classic horror movie poster frames
- Lord of the Rings → Tolkien-inspired manuscript/illuminated frames

A generic "fancy border" is not a showcase. The frame itself must tell you which set the card is from.

---

## 5. Collector Booster Architecture

### Value Proposition

A Collector Booster must contain content that CANNOT be obtained from Play Boosters:
- **Exclusive treatments** — Textured foils, serialized cards, Collector Booster-only showcase variants
- **Guaranteed premium density** — Multiple foils, guaranteed showcase/borderless cards
- **The List / Special Guests** — Curated reprints from Magic's history

### Collector Booster Slot Structure (typical)

1. Foil rare/mythic
2. Non-foil borderless/showcase rare/mythic
3. Non-foil extended art rare/mythic
4. Foil uncommon (showcase variant)
5. Foil common
6-10. Assorted foils and treatments
11. Traditional foil land
12-15. Filler (foil commons/uncommons, art cards)

### The Collector Booster Box EV Rule

The expected value of a Collector Booster box should be at least 40-50% of the purchase price for a healthy product. Below 30%, repeat customers stop buying. This means the set needs enough high-value cards at mythic/rare to sustain box EV.

---

## 6. Marketing Hook Extraction

### Audience Segmentation

Every set has three core audiences. Each needs at least one dedicated hook:

| Audience | What They Care About | Hook Type |
|----------|---------------------|-----------|
| **Competitive players** | Tournament-viable cards, meta impact | "This set introduces [card] that will reshape Standard" |
| **Casual/Commander players** | Fun commanders, synergy pieces, reprints | "Build around [commander] with [mechanic]" |
| **Collectors** | Premium treatments, serialized/rare variants, art | "Featuring [showcase style] with [exclusive treatment]" |

### The Selling Sentence Test

Can you describe the set's appeal in one sentence for each audience?
- If you can't, the set's hooks aren't clear
- If all three sentences say the same thing, the set lacks audience differentiation
- If one audience has no sentence, the product suite has a gap

---

## 7. UB Product Considerations

### How IP Sets Change the Product Suite

| Aspect | Original Set | UB Set |
|--------|-------------|--------|
| **Precon themes** | Based on set mechanics/archetypes | Based on IP characters/factions |
| **Showcase frames** | Set-themed design | IP-themed design (LotR manuscript, FF pixel art) |
| **Poster cards** | Powerful mythics | Iconic IP characters at mythic |
| **Collector hooks** | Art treatments, serialized | IP-specific treatments (scene cards, character variants) |
| **Marketing hooks** | Mechanical innovation | IP recognition + mechanical innovation |

### UB-Specific Commander Precon Rules

- Precon commanders should be recognizable IP characters
- Each precon should represent a distinct faction/group within the IP
- Flavor text and card names must align with IP voice
- The IP's most iconic character should be in the MAIN SET, not locked in a precon

---

## 8. Product Suite Checklist

Run this checklist before finalizing the product architecture:

- [ ] **Poster cards identified**: 3-5 cards that will drive previews and pre-orders
- [ ] **Color coverage**: Poster cards span at least 3 different colors
- [ ] **Precon themes chosen**: 2-4 themes that complement the main set's mechanics
- [ ] **Precon commanders designed**: Legendary creatures that signal their strategy clearly
- [ ] **Precon power level**: All precons at 6-7 on the casual scale
- [ ] **Precon independence**: No precon requires main set rares/mythics to function
- [ ] **Showcase frame designed**: A unique frame that reinforces the set's visual identity
- [ ] **Collector hooks**: At least 1 exclusive treatment type for Collector Boosters
- [ ] **Marketing hooks**: One selling sentence per audience (competitive, casual, collector)
- [ ] **Product fatigue**: Every product in the suite passes the "would anyone notice?" test
