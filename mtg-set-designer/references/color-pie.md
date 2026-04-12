# The Color Pie

The color pie is the most important invariant in Magic design. Mechanics get retired and return; the color pie stays. Rosewater has written more words on it than on any other design topic because every time it gets bent the wrong way, the game's long-term health suffers.

Think of the pie as a *map of who's allowed to do what*. Each color has strengths it does often and cheaply, things it does occasionally, and things it basically never does. The *weaknesses* matter as much as the strengths — they are the reason players pick colors at all.

## Primary, secondary, tertiary

For any effect, each color has a position:

- **Primary** — the color(s) where the effect appears at common, at full efficiency, without apology. Red destroying artifacts is primary.
- **Secondary** — the color does it, but less often and usually at higher rarity or at a slight discount in power. Green destroying artifacts is secondary.
- **Tertiary** — the color does it rarely, conditionally, or only with a twist. White destroying artifacts tied to an enchantment is tertiary.

When you assign a mechanic in `mechanics.json`, declare the primary/secondary/tertiary split. This controls how many cards with that mechanic live in each color and at what rarity.

## The five colors: what they do, what they don't

### White

*Primary:* small efficient creatures, mass removal, exile-based creature removal, lifegain, protection effects, enchantment support, order and law flavor, flying at small sizes.

*Secondary:* board wipes at larger scale, tap effects, resurrecting creatures (mostly small/weak ones), evasion.

*Tertiary:* card draw (usually conditional or via lifegain/creature count), counterspells (very rarely, usually conditional).

*Weaknesses:* raw card draw, tutoring, unconditional single-target creature removal that doesn't involve combat or exile.

### Blue

*Primary:* card draw, counterspells, bounce, creature theft, scry/library manipulation, big flyers, knowledge and control flavor.

*Secondary:* card selection, evasion effects, small flyers, tempo effects, animating things (especially lands/artifacts).

*Tertiary:* creature removal (usually only via bounce or "lock down"), life gain (rare).

*Weaknesses:* efficient permanent creature removal, direct damage, artifact destruction, life gain.

### Black

*Primary:* unconditional single-target creature removal, discard, reanimation, sacrifice effects, life-as-resource, "pay any cost" flavor, swamp-walking horrors.

*Secondary:* creature tokens (often small/disposable), card draw (at a life cost), evasion (fear/menace).

*Tertiary:* artifact destruction (occasionally, often via a downside), counterspells (historically, rarely now).

*Weaknesses:* enchantment removal, unconditional artifact removal, flying (primary flyers are white and blue, black gets conditional or undead flyers).

### Red

*Primary:* direct damage, haste, artifact destruction, temporary effects, impulse draw ("exile the top card, play it this turn"), goblins, dragons, chaos.

*Secondary:* creature removal via damage (so it kills small things well, fails against big things), land destruction (mostly retired), treasure/ritual effects.

*Tertiary:* counterspells (very rare, usually red-only targets), enchantment removal (very limited).

*Weaknesses:* enchantment removal, "permanent" card advantage, flying (reds get dragons but at high cost), life gain.

### Green

*Primary:* mana ramp, big creatures, fight/trample, land tutoring, creature pumping, nature and growth flavor.

*Secondary:* artifact and enchantment destruction (green's "clean the board of non-creature stuff" role), creature-based card advantage, recursion for creatures.

*Tertiary:* flying (usually only on dragons/insects and at cost), direct damage (rare, creature-based fight effects only).

*Weaknesses:* card draw (gets creature-based card draw, not library draw), unconditional removal of non-creatures, evasion.

## Bending vs. breaking

Colors break their pie in ways that exist on a spectrum. Rosewater teaches this spectrum roughly as *bending is fine, breaking is forbidden*:

- **Flavor bleed** — a one-off card where the color does something off-pie because the flavor demands it. A white card that briefly steals a creature because its name is "Angelic Beguilement" or similar. Fine, in moderation.
- **Block bleed** — a mechanic for one set shifts some effect into a new color because the set is *about* that shift. Zendikar pushing mana ramp slightly harder into white was block bleed. Fine when the set justifies it.
- **Bending** — temporarily moving a secondary effect into primary slot, or a tertiary into secondary. Usually fine.
- **Breaking** — giving a color the thing it's supposed to be *bad* at, in a way that undoes its weakness. Blue getting an efficient unconditional creature destruction at common. Red getting cheap enchantment removal. This is what you must not do.

The test: does this card/mechanic *undo a color's weakness*? If yes, it's breaking. If no, it might be bending, which is a judgment call.

## Why weaknesses matter

Players pick colors in part because of what the colors *can't* do. A two-color deck works because the two colors cover each other's weaknesses. If every color can do everything, players stop needing two colors, and the whole shape of deckbuilding collapses. Keep the weaknesses sacred.

## Applying this in the skill

When you run `balance_check.py`, it looks at each card's rules text for common effect patterns and checks whether the color assignment is plausible against this document. It will flag probable color pie violations as warnings — not errors, because the tool can't tell the difference between a bend and a break. That judgment is yours. When you see a warning, ask: *does this card undo a core color weakness?* If yes, change the color or the effect. If no, document the bend in `balance_report.md` and move on.
