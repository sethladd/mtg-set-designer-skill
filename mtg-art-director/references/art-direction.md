# Art Direction

Every card in the set needs an **art description** — a structured prompt that drives a text-to-image LLM to produce the card's art. The art description is the bridge between game design and visual identity.

**Primary target: text-to-image LLM generation.** Secondary: image search or handoff to a human illustrator. Every field is written for a diffusion model that renders literally, has no cross-card memory, cannot ask clarifying questions, and needs every material, light source, and compositional choice specified explicitly.

This reference covers the official WotC art brief format (for historical reference), what makes MTG art work at card size, and how to write descriptions that produce usable LLM-generated results.

## The WotC art brief format

Wizards of the Coast uses a standardized format when commissioning card art from illustrators. The format was publicly shared in articles like "You Make the Card 4" (2013) and the Ultimate Masters art descriptions (2018), and analyzed in detail by MTG artist Winona Nelson.

The standard fields are:

- **Setting** — the plane or world (e.g., "Lorwyn," "Innistrad," "Equestria")
- **Color** — the card's color identity (e.g., "Red creature," "Blue and black spell")
- **Intent** — (optional) narrative context explaining what the card represents in the set's story or mechanical identity. Helps the artist understand *why* this image matters.
- **Location** — the specific environment within the setting (e.g., "A moonlit cemetery on a hilltop," "The interior of a bustling market stall")
- **Action** — a detailed narrative description of what's happening in the image. This is the longest field and describes composition, character poses, visual effects, and key details.
- **Focus** — the single most important visual element (e.g., "The glowing sword," "The warrior's face as she realizes what she's done"). This is what the viewer's eye should land on first.
- **Mood** — a short evocative phrase capturing the emotional tone (e.g., "Eerie calm before the storm," "Triumphant but costly," "You're in deeper trouble than you first realized")

## Adapting the format for LLM generation

Unlike a human illustrator, a text-to-image LLM cannot read between the lines. It needs more specification, not less. Each card's art description must be rich enough to produce a usable image in **one generation pass** — if the description leaves materials, lighting, or composition ambiguous, the generator will fill those gaps randomly and the result will be inconsistent across the set.

Each card in `set.json` gets an `art_description` field structured as:

```json
{
  "art_description": {
    "scene": "A towering reef-guardian serpent — its armored skull wrapped in coral plates and mother-of-pearl scales the length of a forearm — coils through the flooded colonnade of a sunken Tidecaller temple, mid-uncoiling toward the viewer as schools of lantern-fish scatter in panic through shafts of cyan bioluminescent light falling from cracked ceiling stones. Its left eye — a vertical amber slit ringed in veined gold — fixes directly on the camera. Basalt columns slick with white barnacles and threaded with glowing blue kelp frame the scene; silt drifts across the temple floor where a single bronze ceremonial trident lies half-buried, embers of disturbed phosphorescence trailing its length. Backlit from above-right by the bioluminescent shafts, the serpent's face in deep cold shadow with rim-light catching the scale ridges of its jaw.",
    "focus": "The serpent's amber eye",
    "mood": "Ancient, patient, you have already been seen",
    "palette": "Deep indigo, drowned-teal, cyan bioluminescence, pearl-white, veined gold",
    "frame": "Wide shot, low-angle worm's-eye from the temple floor, serpent's coils cropped at upper frame edge to suggest mass continuing beyond view",
    "style_anchor": "Magic: The Gathering card art, painterly digital illustration in the style of Seb McKinnon, atmospheric chiaroscuro, 4:3 landscape aspect ratio, cinematic composition",
    "negative_prompt": "no text, no watermarks, no card borders, no UI elements, no signatures, no frames, no captions, no extra fingers, no distorted faces, no modern clothing, no photography, no 3d render, no low-detail backgrounds, no surface water, not above water"
  }
}
```

The fields:

- **scene** — 60–140 words. The core description. It must name specific materials, lighting direction, and environmental features. "A warrior fights a dragon" is useless to an LLM. "A wounded Tidecaller knight, half her lacquered-copper scalemail shattered down the left flank, drives her whale-bone lance up into the soft underbelly of a rearing Salt-Drake, both silhouetted against the burning terraces of Veth-Kalor, ash falling like snow, firelight underlighting the dragon's gullet" tells the model everything it needs.
- **focus** — the single visual element where the eye lands. 3-8 words, no "and." LLMs use this to decide what to render sharpest.
- **mood** — 2–8 words capturing emotional register. Evocative shorthand ("you're in deeper trouble than you first realized") beats dry descriptors ("dark and scary").
- **palette** — 3-5 specific color names with modifiers. A red card shouldn't have predominantly blue art unless deliberate. LLMs treat "amber" and "orange" as distinct — pick precisely.
- **frame** — shot type + camera angle + what's cropped. Variety across the set prevents visual monotony.
- **style_anchor** — a set-wide style phrase repeated verbatim on every card. This is the primary mechanism for cross-card visual cohesion when generations are produced independently.
- **negative_prompt** — explicit exclusions. LLMs fail predictably (text artifacts, extra fingers, modern anachronisms); the negative prompt short-circuits these.

The image generator (`mtg_card_maker/scripts/generate_art.py`) flattens these fields into the final prompt string at generation time — do not hand-write a `prompt` field into `set.json`.

## What makes good MTG art

MTG art has constraints that most illustration doesn't:

### It must read at tiny sizes

A printed Magic card's art box is roughly 2.1 × 1.5 inches. Digital play can be even smaller. This means:

- **Strong silhouettes.** The main subject should be recognizable from its outline alone. Complex, detailed subjects that rely on interior detail to be understood will turn into muddy blobs at card size.
- **Limited focal points.** One primary focus, at most one secondary element. Three or more competing focal points create visual noise.
- **High value contrast.** The focus should be the area of highest contrast (lightest light against darkest dark, or most saturated color against neutral). Low-contrast art disappears at card size.
- **Big shapes over fine detail.** Composition should be built from large, readable shapes. Fine detail is a bonus for people who zoom in, not a requirement for understanding the image.

### It must convey the card's identity instantly

A player glancing at their hand should be able to tell cards apart by art alone. This means:

- **Each card's art should be visually distinct** from other cards in the set. Two swamp creatures lurking in identical murky water are hard to distinguish. Give each one a different pose, environment, or dominant color.
- **Creatures should look like their type.** If the card is a 1/1 Soldier, the art shouldn't show a towering giant. If it's a 7/7 Wurm, it should feel massive. Power/toughness should be visually intuitive.
- **Spells should show the spell happening**, not just a person casting it. "Bolt of Lightning" should show the lightning, not a wizard with glowing hands.

### It must serve the card's color identity

MTG's colors have strong visual associations that players internalize:

- **White** — bright light, open skies, organized structures, clean lines, warm golds and whites. Angels, soldiers, castles, plains.
- **Blue** — water, air, arcane energy, crystalline structures, cool blues and silvers. Merfolk, sphinxes, towers, oceans.
- **Black** — darkness, death, decay, shadows, purples and sickly greens. Zombies, demons, swamps, crypts.
- **Red** — fire, chaos, passion, destruction, warm reds and oranges. Goblins, dragons, mountains, volcanoes.
- **Green** — nature, growth, primal force, deep greens and browns. Beasts, elves, forests, overgrown ruins.

Multicolor cards should blend the visual language of their colors. A blue-red card might show arcane fire or a storm at sea. A green-black card might show nature reclaiming a graveyard.

These associations can be subverted by the set's theme (a white-aligned undead faction, a green-aligned technological society), but the subversion should be deliberate and consistent across the set.

### It should tell a micro-story

The best MTG art captures a moment with implied before and after. Not a portrait, but a scene. Not a landscape, but a landscape where something is happening or about to happen. A creature mid-leap, a spell at the moment of impact, a character making a decision — these create narrative interest that a static pose doesn't.

## Writing art descriptions by rarity

Different rarities have different visual needs:

**Commons** — clean, simple compositions. One subject, one action, one mood. Commons are the bread and butter of the set's visual identity — they appear most often and should establish the set's visual baseline. Don't overcomplicate them.

**Uncommons** — slightly more complex scenes. Can show interaction between two elements (a creature in an environment, a spell affecting a target). Signpost uncommons should visually hint at their archetype's strategy.

**Rares** — showcase pieces. More dramatic compositions, more dynamic action, more environmental storytelling. These are the cards players remember — their art should be memorable.

**Mythics** — the most visually ambitious descriptions. Mythics are the set's wow moments — the art should match. Epic scale, dramatic lighting, powerful subjects. A mythic creature should look like the most important thing on the battlefield.

## Writing art descriptions during Phase 5

Art descriptions are written alongside the card's mechanical design, not as a separate pass. When you design a card, immediately write its art description. This ensures:

- The art concept flows naturally from the card's mechanical identity
- You catch visual redundancy early (if two cards would have nearly identical art, one needs to change)
- The set's visual variety is built in from the start, not retrofitted

When writing the scene, ask yourself:

1. **What is this card's main subject?** A creature? A spell effect? A location? An event?
2. **What is this card *doing* in the game?** A removal spell should show destruction or containment. A draw spell should show discovery or insight. A pump spell should show empowerment or transformation.
3. **What moment tells the best story?** Not the beginning, not the end — the turning point. The moment of highest tension or transformation.
4. **What makes this card visually different from similar cards in the set?** If you have three black common creatures, they need three distinct visual identities even if they're mechanically similar.
5. **Does the art serve the set's theme?** Every card's art should feel like it belongs in this world. A generic fantasy warrior doesn't belong in a deep-sea horror set — but a pressure-suited diver wielding a harpoon does.

## Palette consistency across the set

Before writing individual card descriptions, establish a **set palette** in the design doc during Phase 2 (Worldbuilding). This is a short list of the dominant colors and visual motifs that define the set's world:

- What does the sky look like? (Affects every outdoor scene)
- What materials are common? (Stone, wood, metal, crystal, bone, coral — affects architecture and equipment)
- What light sources exist? (Sunlight, moonlight, bioluminescence, fire, arcane glow — affects mood across the set)
- What visual motifs recur? (Spirals, fractals, geometric patterns, organic curves — gives the set visual coherence)

Individual card palettes should work within this set palette while still being distinct enough to differentiate cards.
