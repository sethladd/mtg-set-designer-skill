# Vision

Vision design is the first phase of a real set's 20-month lifecycle. It answers one question: *what is this set?* Everything downstream — mechanics, archetypes, cards, worldbuilding — is a consequence of the vision. A fuzzy vision produces a fuzzy set.

## Top-down vs. bottom-up

Every set sits somewhere on a spectrum between two poles.

**Top-down** starts with a world, mood, or flavor concept and looks for mechanics that embody it. Innistrad began with "gothic horror" and asked: what mechanic says *werewolf*? The answer was the transform card, and the set's mechanical identity flowed from there. Theros began with "Greek mythology and heroes touched by gods" and produced Devotion and Bestow. Top-down sets live or die by whether the mechanics feel *inevitable* given the flavor. If a player can't name the tone of the set within two cards, the top-down attempt has failed.

**Bottom-up** starts with a mechanical idea — a lever in the game's design space nobody has pulled yet — and asks what world would justify it. Original Zendikar started with "we want a set where lands matter" and ended up inventing an adventure world full of ruins because ruins are where explorers find lands. Bottom-up sets can feel mechanically elegant but risk feeling flavorless if the world is just a costume over the mechanics.

Decide which you're doing before you start and say it out loud in the design doc. The two modes require different kinds of discipline: top-down designers have to resist *forcing* mechanics to fit a flavor beat; bottom-up designers have to resist *neglecting* the world once the mechanics feel tight.

Most real sets end up somewhere in the middle. That's fine. What matters is that you're intentional.

## The three pillars

The pillars are the most important idea in vision design. A set has **exactly three** (occasionally four) load-bearing commitments that everything else hangs from. The point of writing them down is that they become a test: for every mechanic, archetype, and card, you can ask "does this serve a pillar?" and if the answer is no, you either cut the thing or you change a pillar.

A good pillar is:

- **Specific enough to constrain.** "Graveyard matters" is weaker than "cards in your graveyard return to your hand or battlefield throughout the game." The first rules nothing out; the second tells you every card should interact with the graveyard as a resource being *mined*, not as a trash bin.
- **Mechanical or experiential, not flavorful.** "Horror" is a tone, not a pillar. "Every turn the board gets scarier as creatures transform into larger versions of themselves" is a pillar because it tells you something about the *play experience*.
- **Load-bearing.** If you deleted the pillar, would the set still make sense? If yes, it's not a pillar — it's a preference.

Three is the right number because four pillars is usually a sign you couldn't decide which idea was actually central, and two pillars is usually a sign the set is under-specified and will feel thin. When you have a fourth idea you love, ask whether it's really a sub-component of one of the three or whether one of the three is actually weak and should be replaced.

## Writing the vision doc

The vision lives at the top of `design_doc.md`. Keep it short — a page or less. Structure:

1. **Elevator pitch** — one sentence that would sell the set to someone who has never heard of it.
2. **Origin** — top-down from what? bottom-up from what mechanical itch?
3. **The three pillars** — each one a full sentence, each one specific, each one mechanical.
4. **Tone and play feel** — aggressive? slow? combo-forward? high interaction? low interaction?
5. **Set identity sentence** — the sentence you'd use to sell the set to a skeptical playtester in ten seconds.
6. **Assumptions** — anything you made up because the user didn't say, so they can correct you.

This is the spec. When Phase 5 gets noisy and card decisions start feeling arbitrary, come back here.

## Anti-patterns

**Pillar as flavor noun.** "Pirates." "Samurai." "Dragons." These are *subjects*, not pillars. A pillar tells you what the set *does* to its subjects.

**Too many big ideas.** If the set has five mechanics, four tribes, a graveyard theme, and a lands-matter subtheme, there is no room left for the actual cards. Cut until it fits on one page.

**Pillars invented to justify mechanics you already wrote.** Vision should come before mechanics. If you find yourself writing a pillar to rationalize a mechanic, the mechanic is the real vision and the pillar is decoration — which means your vision is actually "this mechanic is cool" and the rest of the set has no spine.

**Ignoring the pillars later.** The pillars only do their job if you reference them. Every mechanic definition in `mechanics.json` has a `serves_pillar` field for this reason. Use it. If a mechanic doesn't serve one, ask yourself why it's in the set.
