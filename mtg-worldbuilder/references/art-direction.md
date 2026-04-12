# Art Direction

Every card in the set needs an **art description** — a structured prompt that can be used to either find existing artwork (via image search and cropping) or generate an image using an AI image generator. The art description is the bridge between game design and visual identity.

This reference covers the official WotC art brief format, what makes MTG art work at card size, and how to write descriptions that produce usable results.

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

## Adapting the format for this skill

For set design purposes, the art description on each card doesn't need to be as long as a professional art brief. But it needs to contain enough information to either:

1. **Guide an image search** — someone looking for existing art to proxy the card needs to know what to search for
2. **Prompt an AI image generator** — the description should work as an image generation prompt with minimal editing

Each card in `set.json` gets an `art_description` field structured as:

```json
{
  "art_description": {
    "scene": "A massive serpent coils around a sunken temple, its scales glowing with bioluminescent patterns. Schools of fish scatter in terror as one enormous eye regards the viewer.",
    "focus": "The serpent's glowing eye",
    "mood": "Ancient, patient menace",
    "palette": "Deep blues and teals with bioluminescent cyan and green accents",
    "frame": "Wide shot from below, looking up at the serpent's mass"
  }
}
```

The fields:

- **scene** — 1–3 sentences describing what's in the image. This is the core prompt. It should describe a specific moment, not a generic concept. "A warrior fights a dragon" is weak. "A wounded knight drives her lance into the underbelly of a rearing dragon, both silhouetted against a burning city" is strong.
- **focus** — the primary visual element the eye should land on. Keep it to one thing. If you can't pick one focus, the composition is too busy.
- **mood** — 2–5 words capturing the emotional register. This guides color choices, lighting, and atmosphere.
- **palette** — the dominant colors. This helps maintain visual consistency across the set and ensures the art feels right for the card's color identity. A red card shouldn't have predominantly blue art unless there's a deliberate reason.
- **frame** — the camera angle and shot type (close-up, medium shot, wide shot, bird's eye, worm's eye, etc.). Variety in framing across the set prevents visual monotony.

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
