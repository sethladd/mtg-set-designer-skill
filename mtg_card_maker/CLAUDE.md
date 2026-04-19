# Working on the MTG Card Maker skill

This skill is self-contained. Everything needed to render (and optionally
generate art for) MTG cards lives under this directory:

- `SKILL.md` — the user-facing skill definition
- `scripts/render_cards.py` — PNG renderer (Pillow only)
- `scripts/generate_art.py` — Google Imagen art generator + art-box cropper
- `assets/` — frame PNGs, mana SVG symbols, fonts
- `references/sources.md` — provenance for every external resource used

## Source tracking rule

**Any time you identify or use an external URL while producing work in
this skill — a docs page, a spec, an API reference, an image asset, a
library README, a blog post with a cited technique — append it to
`references/sources.md` under an appropriate heading before you finish.**

Record the full URL. One-line annotation describing *why* this source
mattered (what measurement, parameter, or asset it contributed) is
encouraged. Do not rely on the memory system for this — the sources file
is the canonical record so anyone maintaining the skill later can
verify claims against the originals.
