# Art Direction Framework

An operational handbook for concepting cards and writing art descriptions. This is the decision-making guide you work through for every card — from establishing the set's visual identity down to the five-field description for each individual piece of art.

---

## 1. Set Visual Identity Establishment

Before writing a single card description, define the visual identity for the entire set. This is the "style guide in miniature" that ensures visual coherence.

### Define These Before Anything Else

1. **Set palette** — The 3-5 dominant colors that define this world beyond MTG color identity. What does the SKY look like? What is the dominant LIGHT SOURCE? What MATERIALS are common?
2. **Recurring motifs** — Visual patterns that repeat across the set (spirals, fractals, geometric patterns, organic curves, specific architectural elements). These are the visual fingerprint of the world.
3. **Material vocabulary** — What are things MADE OF in this world? Stone, coral, bone, crystal, living wood, rusted iron, bioluminescent chitin? This affects every equipment, building, and creature.
4. **Light sources** — Sunlight, moonlight, bioluminescence, volcanic glow, arcane energy, dual suns? Lighting is the single most powerful mood-setter and must be consistent.
5. **Scale references** — What is the tallest thing in this world? The smallest? How big are the buildings? This calibrates the visual scale for all creatures.

### Visual Identity Document Template

```
SET VISUAL IDENTITY: [Set Name]

PALETTE: [3-5 dominant environmental colors]
SKY: [What does the sky look like in this world?]
LIGHT: [Primary and secondary light sources]
MATERIALS: [Common materials in order of prevalence]
MOTIFS: [2-3 recurring visual patterns]
SCALE: [Calibration — e.g., "tallest trees = 200ft, typical building = 3 stories"]
MOOD BASELINE: [The default emotional register of the world]
```

---

## 2. Card Concepting Process

The concept is the bridge between a card's mechanics and its place in the world. Every card gets a concept BEFORE it gets an art description.

### Concepting Decision Tree by Card Type

**Creatures:**
1. What creature type is it? → Reference the world guide's creature-to-faction mapping
2. What are its keywords? → Each keyword must be visually represented (see Mechanical Readability)
3. What is its P/T? → This determines visual scale and threat level
4. What rarity? → This determines visual complexity and narrative importance
5. Is it legendary? → Legendary creatures need unique visual identity, personality, and close framing

**Instants:**
1. What does this spell DO mechanically? → The art shows the effect HAPPENING, in the moment of impact
2. Is it a reaction or an initiation? → Reactions show interruption; initiations show sudden force
3. What color is it? → The visual effect should match color identity (red = fire/lightning, blue = water/arcane, etc.)

**Sorceries:**
1. What does this spell DO? → The art can show the buildup, the aftermath, or the effect at scale
2. Is it targeted or area-of-effect? → Targeted = focused composition; AoE = wide-shot showing scale of impact
3. Sorceries can be more contemplative than instants — show the weight of the magic, not just the flash

**Artifacts:**
1. What IS this object? → The art shows THE OBJECT ITSELF as the primary subject
2. Is it equipment? → Show it being worn/wielded, suggesting its function
3. Is it a vehicle? → Show it in motion or ready to move, with scale references

**Enchantments:**
1. What ongoing effect does this represent? → Show the EFFECT ON THE WORLD, not just a magical symbol
2. Auras show the effect on the enchanted permanent
3. Global enchantments show the world CHANGED by the enchantment's presence

**Lands:**
1. Which basic land type does it reference? → Maintain color associations
2. Is it a specific location in the world guide? → Use the described visual details
3. Lands have NO characters — show the environment as the subject
4. The land itself should feel like it could produce the mana it taps for

**Planeswalkers:**
1. This is a CHARACTER PORTRAIT with magical context
2. Show the planeswalker using their signature magic
3. The composition is tighter — closer to a portrait than a battle scene
4. Must convey personality through pose, expression, and magical style

---

## 3. The Art Description Formats

### WotC Official Format (for reference)

The standard fields used when WotC commissions from human illustrators:
- **Setting** — The plane and general location
- **Color** — The card's color identity and associated mood
- **Action** — A detailed narrative description of what's happening (longest field)
- **Focus** — The single most important visual element
- **Mood** — Short evocative phrase for emotional tone

The WotC format assumes a human artist who can ask clarifying questions, research the world on their own, and apply professional compositional instincts. **Our pipeline's primary target is a text-to-image LLM**, which has none of these affordances. The format below is adapted accordingly.

### Pipeline JSON Format (what we produce)

Each card in `set.json` gets an `art_description` object optimized for LLM image generation:

```json
{
  "art_description": {
    "scene": "60-140 word LLM-optimized rich description of the specific moment",
    "focus": "The single primary visual element (one noun phrase, 3-8 words)",
    "mood": "2-8 words capturing emotional register — evocative shorthand preferred",
    "palette": "3-5 specific colors with modifiers, aligned to color identity",
    "frame": "Shot type + camera angle + composition directive",
    "style_anchor": "Consistent style phrase used across every card in the set",
    "negative_prompt": "What the model must NOT produce"
  }
}
```

The first five fields are the art-direction intent. The last two are the generation-layer specifications that turn intent into a reliable LLM prompt. **All seven fields are required.** The image generator (`mtg_card_maker/scripts/generate_art.py`) flattens these into the final model prompt at generation time — that script's `_compose_body` is the canonical assembler, so do not write a pre-flattened `prompt` field into `set.json`.

**Field-by-field guidance:**

- **scene**: 60-140 words. Describe a SPECIFIC MOMENT, *thick with observable detail that an image model can render*. Vague text yields vague images. Every scene must contain seven required elements in roughly this order (subject-first ordering works best for diffusion models):

  1. **Subject specifics** — pose, expression, posture, clothing/equipment, distinguishing physical detail (scars, feathers, armor patterns, scale texture) that make this being or object singular rather than a generic token
  2. **Action verb in the present participle** — what is happening *right now*, mid-motion when possible. LLMs lock onto gerunds and present-tense clauses. Not "a knight fights a dragon" but "the knight driving her lance into the dragon's shoulder-plate, mid-twist to avoid the jaws"
  3. **Environment with concrete features** — the specific location with at least two named or described features (the toppled obelisk, the canal-gate's iron teeth, the salt pans cracking underfoot). Reference world-guide locations by name when available
  4. **Lighting direction, source, and quality** — specify where the light comes from and what it does to the subject. "Backlit by the red dwarf star low on the horizon, face in deep shadow, rim-light on the left cheekbone, ember glow under-lighting her chin." Never write "well-lit," "dramatic," or "atmospheric" unqualified — LLMs ignore these
  5. **Materials and textures (at least two, named precisely)** — not "armor" but "lacquered bamboo lamellar laced with blood-red silk." Not "robes" but "sea-silk stained with tide-gold dye." Not "stone" but "wet basalt veined with fossilized coral." LLMs excel at materials; give them exact nouns
  6. **Atmospheric detail implying before/after** — one element that creates a micro-story: drifting embers from an already-collapsed roof, rain still falling from a passing storm, footprints in ash, a banner mid-fall. This tells the LLM the scene is mid-event, not a static pose
  7. **World anchor** — at least one proper noun, faction name, species name, or world-specific term from the world guide or ip_catalog. "A swamp" is not anchored; "the Mirefen's tidal swamp, at the edge of Veth-Kalor's fish-scale quarter" is

- **focus**: 3-8 words, ONE noun phrase. The viewer's eye lands here first. Never use "and." The focus is NOT a summary of the scene — it is the single point of highest contrast. LLMs use this to decide what to render sharpest.

- **mood**: 2-8 words. Prefer WotC-style evocative shorthand ("you're in deeper trouble than you first realized," "placid, pretty, and frightening") over dry descriptors ("dark and scary"). Mood drives lighting saturation, color temperature, and atmospheric density in the generation.

- **palette**: 3-5 specific color names with descriptive modifiers. "Bruise-purple, bone-white, smoke-grey with cold blue rim-highlights" — not "purple, white, and grey." Must align with card color identity (at least 60% by visual weight) and work within the set palette. LLMs treat color names literally; "amber" and "orange" produce different results.

- **frame**: Shot type (close-up, medium, wide, extreme wide) + camera angle (eye level, low, high, bird's eye, worm's eye, Dutch) + what is cropped or included at the frame edge. Example: "Medium shot, low angle from the temple floor, dragon's wings cropped at frame edge to suggest scale beyond the image." Vary across the set.

- **style_anchor**: The same phrase on every card in the set. Ensures visual cohesion across the 200+ generations. Template: `"Magic: The Gathering card art, painterly digital illustration in the style of [reference artist or set style keyword], 4:3 landscape aspect ratio, cinematic composition"`. Pick the reference style during Set Visual Identity (Step 3) and never vary it.

- **negative_prompt**: Standard exclusions every generation should reject. Baseline: `"no text, no watermarks, no card borders, no UI elements, no signatures, no frames, no captions, no extra fingers, no distorted faces, no modern clothing, no photography, no 3d render, no low detail backgrounds"`. Add card-specific exclusions as needed (e.g., a flying creature's negative_prompt should include "not standing on ground").

---

## 4. Mechanical Readability Checklist

Before finalizing any art description, verify mechanical readability using this checklist.

### Keyword → Visual Requirement

For each keyword on the card, the art description MUST include at least one of the associated visual elements:

| Keyword | Must Include One Of |
|---------|-------------------|
| Flying | Airborne, wings spread, mid-flight, aerial view, clouds, sky |
| Reach | Ground-based + long limbs, extended weapons, webs above, vines reaching up |
| First strike | Lunging forward, weapon prominent, striking pose, speed of attack |
| Double strike | Dual weapons, blurred-motion dual attack, two-phase assault |
| Vigilance | Alert stance, eyes scanning, armor at-ready, guarding position, no rest |
| Deathtouch | Venom dripping, toxic aura, withering contact, necrotic energy, sickly glow |
| Lifelink | Radiant energy, life-drain visible, vitality flowing, healing light |
| Trample | Massive scale, unstoppable momentum, ground shaking, crushing through |
| Haste | Motion blur, explosive speed, burst of energy, urgency in pose |
| Menace | Multiple threats, terrifying aspect, looming over viewer, fearsome presence |
| Ward | Protective barrier, magical shield, rune circles, deflection visible |
| Flash | Sudden arrival, surprise element, burst-in, mid-materialization |
| Defender | Immovable stance, wall-like form, rooted, shield-forward, blocking posture |
| Indestructible | Unyielding surface, divine glow, reality-bending solidity, unbreakable |
| Hexproof | Shimmering aura, untouchable presence, magic sliding off, ethereal barrier |
| Prowess | Arcane energy building with each spell, magical amplification visible |

### P/T Visual Scale Guide

| P/T Range | Visual Scale |
|-----------|-------------|
| 0/1 – 1/1 | Small — fits in a hand, or humanoid but diminished |
| 2/2 – 3/3 | Medium — human-sized to horse-sized |
| 4/4 – 5/5 | Large — elephant to house-sized, dominates the scene |
| 6/6 – 7/7 | Huge — towers over buildings, fills the frame |
| 8/8+ | Colossal — landscape-scale, the environment IS the creature |

---

## 5. Color Identity in Art

### Strict Adherence (Default)

Most cards should have art that clearly reinforces their color identity. A player should be able to guess the card's color from the art alone at least 60% of the time.

**Color → Lighting and Atmosphere:**
- **White**: Bright, warm, open. Golden hour, sunlit, radiant. Clean compositions.
- **Blue**: Cool, mysterious, intellectual. Moonlit, arcane glow, underwater light. Controlled compositions.
- **Black**: Dark, threatening, ambitious. Shadow, sickly light, fire-lit underground. Dramatic contrast.
- **Red**: Hot, dynamic, passionate. Firelight, volcanic, sunset. Energetic compositions.
- **Green**: Natural, lush, primal. Dappled forest light, verdant glow. Organic compositions.

**Multicolor**: Blend the visual languages. UB = cold shadows with arcane glow. RG = volcanic forests with primal energy. WB = divine light with dark edges.

### Justified Subversion

Subvert color identity in art ONLY when:
1. The world guide defines a faction that recontextualizes a color (white undead, green artifice)
2. The subversion is CONSISTENT across all cards in that faction
3. The subversion is flagged in the set visual identity document
4. At least one other visual element (lighting, composition style) still reads as the correct color

---

## 6. Composition for Card Scale

Card art appears at roughly 2.1 x 1.5 inches on printed cards, and often smaller on screens.

### The Four Rules of Card-Scale Composition

1. **Strong silhouettes** — The main subject must be recognizable from its outline alone. If you covered the interior detail, could you still identify what it is? If not, simplify.
2. **One focal point** — The area of highest contrast (lightest vs. darkest, or most saturated color) must be the focus. Two competing high-contrast areas create visual noise.
3. **Big shapes over fine detail** — Build from large readable shapes. Fine detail is a bonus for zoom-in, not a requirement for comprehension.
4. **Value contrast hierarchy** — Focus gets highest contrast. Secondary elements get medium contrast. Background gets lowest contrast. This reads clearly at any size.

### Rarity-Specific Complexity

| Rarity | Composition Complexity | Reasoning |
|--------|----------------------|-----------|
| Common | One subject, one action, clean background | Seen most often; establishes visual baseline |
| Uncommon | One subject in an interactive environment | Shows world texture; archetype signposting |
| Rare | Dynamic scene, dramatic lighting, environmental storytelling | Memorable showcase piece |
| Mythic | Maximum visual ambition — epic scale, dramatic composition | The set's visual peak moments |

---

## 7. Visual Storytelling Arc

### Planning the Visual Narrative

Before writing individual descriptions, map the set's story across card art:

1. **Identify 5-8 key story moments** from the world guide
2. **Assign each to a specific card** at appropriate rarity (climaxes at mythic, turning points at rare)
3. **Plan character appearances** — if a character appears on multiple cards, define visual consistency rules
4. **Distribute world details** — commons and uncommons carry the environmental storytelling

### Cross-Card Continuity Rules

- Characters who appear on multiple cards must have the same silhouette, color scheme, and signature features
- Locations that appear on multiple cards must show the same architecture, lighting, and environmental details
- Factions must have internally consistent aesthetics (armor style, weapon types, magical effects)
- Time progression: if the story has a timeline, earlier events should be on lower-numbered collector numbers

---

## 8. AI Image Generation Adaptation

### Expanding Descriptions for AI

When the art will be generated by AI tools, add these to each description:

1. **Style anchor**: "Magic: The Gathering card art, painterly fantasy illustration" (or reference a specific artist's style)
2. **Negative guidance**: "No text, no card borders, no UI elements, no watermarks"
3. **Aspect ratio**: "4:3 landscape format" (standard MTG art box)
4. **Explicit materials**: Name every visible material ("polished steel" not "armor")
5. **Lighting specifics**: "Lit from above-left by warm sunlight, rim-lit from behind by cool sky"
6. **Hand/limb specification**: For humanoids, specify hand positions to avoid generation artifacts

### Style Consistency Techniques

To maintain visual cohesion across an AI-generated set:
- Use the SAME style anchor phrase for every card
- Reference the same lighting conditions for the same environments
- Use consistent color temperature across cards in the same faction
- Apply the same level of detail/abstraction to backgrounds throughout

---

## 9. UB Art Direction

### Referencing Canonical Visual Identity

When working from an `ip_catalog.md`, art descriptions must:

1. **Anchor to canonical appearances** — "as depicted in [source]" for named characters
2. **Respect signature visuals** — Gandalf's hat, Cloud's Buster Sword, a Space Marine's power armor
3. **Blend IP and MTG styles** — The art should feel like Magic card art OF this IP, not screenshot reprints

### Lessons from Published UB Sets

- **Lord of the Rings**: Interpretive fidelity — characters must FEEL like their canonical selves even in a new art style. The most praised cards captured the emotional truth of the characters.
- **Final Fantasy**: Cross-source unification — combining characters from multiple games into one visual language required establishing a shared art style that honored each source while feeling cohesive.
- **Warhammer 40K**: Tone calibration — 40K's gritty darkness had to be balanced against MTG's typical high-fantasy polish. The most successful cards found the middle ground.

### UB-Specific Description Additions

- Reference the specific source moment being depicted ("Gandalf at the Bridge of Khazad-dum")
- Note if the character has multiple canonical appearances and which version to use
- Flag visual elements that are legally/contractually significant (logos, specific costume details that must be accurate)

---

## 10. Per-Card Art Description Checklist

Run this checklist on every card's art description before finalizing:

- [ ] **Scene specificity**: Does the scene describe a SPECIFIC moment, not a generic concept?
- [ ] **Focus singularity**: Is there exactly ONE focal point? No "and" in the focus field?
- [ ] **Mechanical readability**: Does the art support every keyword on the card?
- [ ] **Color identity**: Does the palette align with the card's color (≥60% visual weight)?
- [ ] **Scale accuracy**: Does the visual scale match the P/T?
- [ ] **Type coherence**: Does the art match the card type's conventions? (creatures = beings, spells = effects, lands = locations)
- [ ] **World anchoring**: Does the description reference at least one world-specific element?
- [ ] **Squint test**: Would this read clearly at thumbnail size?
- [ ] **Duplicate check**: Is this scene distinct from all other cards in the set?
- [ ] **Frame variety**: Does this use a different framing than the previous cards in its color?
- [ ] **Mood alignment**: Does the mood serve the card's gameplay identity?
- [ ] **AI readiness**: Is the description detailed enough for single-pass AI generation?
