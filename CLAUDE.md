Every skill contained in this directory should be itself self-contained.

When researching, if an article or resource is actually used in the
production of the skill, ensure that the full link to that article
or resource is recorded in that skill's own sources.md. Each skill
should have its own sources.md.

Each skill must have its own CLAUDE.md at its root. That file should
instruct anyone working on the skill to save any URL that was
identified and used in the production of that skill to the skill's
own references/sources.md.

When answering a question, first check the researched sources already
captured in this repo — each skill's `references/` directory and its
`sources.md` (or `sources/` directory) are the authoritative record of
what we've researched and cited. Prefer those over general knowledge,
since they reflect deliberate decisions about which material is
trustworthy for this project.

If the researched sources don't cover the question, next check any
`wisdom.md` files in the relevant skill(s). These capture distilled
knowledge, lessons learned, and context that aren't in the primary
source material but are still authoritative for this project.

Only after both researched sources and `wisdom.md` come up empty
should you fall back to general knowledge, and clearly mark answers
that rely on it. If the question warrants better grounding, perform
additional research (web search, fetching primary sources) and — if
the new material is used to produce or update a skill — record the
URL in that skill's `references/sources.md` per the rule above.
