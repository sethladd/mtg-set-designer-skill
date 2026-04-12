# How We Built This: A Guide to Creating Orchestrated Multi-Skill Pipelines

This document describes the end-to-end process used to build a 12-skill MTG set design pipeline. If you want to create your own multi-step, orchestrated set of skills for any domain, follow this workflow.

## What we built

A pipeline of 12 specialized skills that chain together to produce a complete Magic: The Gathering set — from a theme concept through rendered card images. Each skill mirrors a real role in a production pipeline, has its own wisdom and reference material, and can run standalone or as part of the orchestrated whole.

The same approach works for any complex, multi-step creative or technical process that you want to decompose into specialized, chainable skills.

---

## Phase 1: Map the real-world process

Before writing a single skill, we mapped the real-world process we were trying to replicate.

### Step 1: Research the domain's actual workflow

We started by studying how Wizards of the Coast actually designs Magic sets. This wasn't about inventing a process — it was about understanding the real one and then encoding it.

**What to do:**
- Research how professionals in your domain actually work (articles, interviews, conference talks, behind-the-scenes documentation)
- Identify the distinct ROLES involved (not tasks — roles, because each role has a distinct expertise and perspective)
- Map the timeline and handoff points between roles
- Identify where feedback loops exist (work going backward for revision)
- Identify where the process branches (mutual exclusivity, conditional paths)

### Step 2: Write the pipeline specification document

We produced `mtg_set_design_pipeline_roles.md` — a comprehensive document that defines every role in the pipeline, what it does, what it takes as input, and what it produces.

**What this document must contain for each role:**
- Real-world equivalent (who does this job in the actual industry?)
- Key responsibilities (bulleted list of everything this role is accountable for)
- Inputs (what artifacts does this role receive?)
- Outputs (what artifacts does this role produce?)
- Proposed skill name and one-paragraph description

**Also include:**
- A flow diagram showing how skills chain together
- Data flow contracts (which artifact flows from skill A to skill B)
- Where feedback loops exist and what triggers them
- Where branch decisions happen (e.g., original world vs. IP adaptation)

This document is your source of truth for the entire build. Every skill will be audited against it.

### Step 3: Write the skill development checklist

We produced `skill_development_checklist.md` — a per-skill checklist specifying what research to do, what wisdom to discover, and what the deliverable must contain.

**For each skill, the checklist defines:**
- **Why build it in this order** (dependency reasoning)
- **Research targets** (specific articles, talks, interviews to find — with descriptions of what to extract from each)
- **Wisdom to discover** (specific questions the research must answer — failure stories, counterintuitive insights, evolved thinking)
- **Pre-known lessons to verify and deepen** (things you already suspect are true, but need evidence for)
- **Deliverable** (one-paragraph description of what the finished skill must do)
- **Special handling** (any domain-specific concerns, like how IP adaptation differs from original creation)

**The checklist is NOT a template.** It's a research agenda. It tells you what questions each skill must answer, not what the answers look like.

---

## Phase 2: Establish the skill architecture pattern

Before building the first skill, we established a consistent architecture that every skill follows.

### The standard skill structure

```
mtg-{skill-name}/
├── SKILL.md                    # YAML frontmatter + process steps
├── CLAUDE.md                   # Sources policy (identical across skills)
├── references/
│   ├── wisdom-catalog.md       # Expert knowledge: failure stories, heuristics, insights
│   ├── {domain}-framework.md   # Operational handbook: decision trees, checklists, tables
│   ├── sources.md              # Every URL researched during skill creation
│   └── {copied references}     # Self-contained copies of any shared reference files
└── scripts/
    └── {audit}.py              # Automated validation checks
```

### Key architectural decisions

1. **Self-containment**: Every skill copies any shared reference files it needs into its own directory. Skills never depend on files in a sibling skill's directory. This means skills can be distributed, run independently, or used in different combinations.

2. **Sources policy**: Every skill has an identical `CLAUDE.md` that says: "Any URL used in the production of this skill must be recorded in `references/sources.md`." This ensures research provenance is always tracked.

3. **Wisdom, not checklists**: The `wisdom-catalog.md` doesn't contain rules — it contains expert knowledge. Failure stories with named examples, counterintuitive insights that contradict common assumptions, and named heuristics that encode years of experience. The framework file is where the operational checklists live.

4. **SKILL.md frontmatter**: Every skill has YAML frontmatter with `name` and `description` fields, including trigger phrases ("Also trigger when the user says things like...").

---

## Phase 3: Build skills sequentially

We built skills one at a time, in strict dependency order (the order specified in the checklist). Each skill followed the same build process:

### Step 1: Research (launch a background agent)

Before writing any content, launch a research agent to search the web for the specific topics the checklist demands. This is the most important step — **the quality of the skill is bounded by the quality of the research.**

**What the research agent does:**
- Searches for every research target in the checklist (specific articles, interviews, retrospectives)
- Extracts key wisdom: failure stories with named examples, quantitative data, specific quotes
- Collects full URLs for every source consulted
- Reports findings in a structured format

**Critical rule: Research first, write second.** Never write the wisdom catalog from memory alone. The research agent finds things you don't know, corrects things you thought you knew, and provides the specific named examples that make wisdom catalogs valuable.

### Step 2: Create the directory structure and static files

While research runs in the background, create:
- The skill's directory structure
- `CLAUDE.md` (identical sources policy)
- Copy any shared reference files from `old-references/` into the skill's `references/` directory

### Step 3: Write the wisdom catalog

Using the research findings, write `references/wisdom-catalog.md`:

**Structure:**
- **Failure stories** (5-10): Real examples of when this domain went wrong. Each story has: what happened, what went wrong, why it went wrong, and the extracted lesson. Use specific names — "Energy in Kaladesh" not "a resource mechanic in a set." Failure stories are the most valuable content in the catalog.
- **Counterintuitive insights** (3-5): Things that are true but surprising. "The best exploration rejects the obvious theme." "Parasitic mechanics are sometimes worth it." These challenge assumptions.
- **Named heuristics** (5-10): Quick tests or rules of thumb. "The Squint Test," "The Counterplay Surface Test," "The Two-Pass Limit." Naming them makes them memorable and referenceable.

**The philosophy:** You're encoding an expert, not writing a manual. The wisdom catalog should read like a conversation with someone who's been doing this job for 20 years and has strong opinions backed by hard experience.

### Step 4: Write the framework

Write `references/{domain}-framework.md`:

**Structure:**
- Decision trees (if X, do Y)
- Checklists (verify these N things before proceeding)
- Tables (mappings, thresholds, categorizations)
- Templates (what the output format looks like)

The framework is the operational counterpart to the wisdom catalog. The catalog tells you WHY; the framework tells you HOW.

### Step 5: Write the SKILL.md

Write the main skill file:

**Structure:**
1. YAML frontmatter (`name`, `description` with trigger phrases)
2. Role statement ("You are the [role] on a Magic set...")
3. Excellence vs. failure framing ("The best [role] produces... The worst produces...")
4. "Why this phase exists" section
5. "Before you begin" section (list reference files to read)
6. The process (8-12 steps, each as an H3)
7. Output format section
8. Reference files section
9. Scripts section
10. Guiding principles (4-6 beliefs that guide the skill's philosophy)

**Each process step should:**
- State what to do clearly
- Reference specific wisdom from the catalog (named heuristics, failure warnings)
- Specify validation criteria (how to know the step is done correctly)

### Step 6: Write the audit script

Write `scripts/{audit}.py` following a consistent pattern:

- `#!/usr/bin/env python3` with docstring listing all checks
- `argparse` CLI: takes the skill's primary output file, optional `--out` for report
- Individual `check_*` functions, each returning `list[str]` of flag strings
- An `audit_*` orchestrator function that runs all checks and produces a markdown report
- Statistics section and summary with categorized flag counts

**Always run `python3 -c "import py_compile; py_compile.compile('script.py', doraise=True)"` to verify syntax.**

### Step 7: Write the sources file

Compile all URLs from the research agent into `references/sources.md`:

- Organize by category (H2 headers)
- Format: `- [Title](URL) — Short description of what was extracted or learned`
- Include EVERY URL that informed the skill's content

### Step 8: Verify and commit

Before committing:
1. List all files — confirm nothing is missing
2. Check line counts — ensure files are substantive (not stubs)
3. Verify Python syntax on all scripts
4. Verify YAML frontmatter parses correctly
5. Confirm copied references match originals (diff check)
6. Count source URLs — ensure the research was thorough

Commit with a clear message: `Add Skill N: mtg-{name} ({what it does})`

### Step 9: Ask "what's the next skill?" and repeat

After committing, explicitly ask or verify what the next skill in the dependency order is, then repeat from Step 1.

---

## Phase 4: Handle session breaks

Context windows have limits. When a session runs out of context mid-build:

### What works

- **Artifact-based state**: Because all work is committed to disk (git commits), a new session can pick up where the old one left off by reading the files
- **Summary-based continuity**: When a session is continued, a summary of prior work is provided. This summary should include: what skills are built, what's next, key decisions made, and any pending work
- **The checklist is the roadmap**: A new session can read `skill_development_checklist.md` to understand what's been built and what's next

### What to tell the new session

- Which skills are already committed (git log)
- What the next skill is
- Any decisions made that affect downstream work
- The consistent architecture pattern to follow

### The key insight

Session breaks are not a problem if your state lives in files, not in conversation. Every piece of knowledge we produced — research findings, wisdom catalogs, framework docs, audit scripts — is committed to disk. A new session reads those files and continues. Nothing lives only in the conversation.

---

## Phase 5: Audit the pipeline

After all skills are built, run a comprehensive audit. This is not optional — it's where you catch the gaps that accumulate across skills built in different sessions.

### The audit process

1. **Re-read the pipeline specification document** (the source of truth)
2. **For each skill, verify conformance:**
   - Does it accept all inputs the spec requires?
   - Does it produce all outputs the spec requires?
   - Does its process cover every key responsibility listed in the spec?
   - Does the wisdom catalog address the failure stories the checklist demanded?
   - Does the audit script check for the issues the checklist specified?
   - Is the skill self-contained (all needed reference files copied)?
   - Does it have a sources.md with URLs?
3. **Verify pipeline-level data flow:**
   - Does every output artifact get consumed by at least one downstream skill?
   - Do feedback loops work in both directions (the sending skill, the receiving skill, and the orchestrator)?
   - Do all downstream skills handle both pipeline branches (if applicable)?
   - Are there dangling outputs nobody consumes or missing inputs nobody produces?
4. **Quality gap analysis:**
   - What could still go wrong even if every skill executes perfectly?
   - What emergent quality issues might the pipeline miss?

### Prioritize findings

Rate every finding:
- **P0 (Critical)**: Blocks pipeline execution — fix immediately
- **P1 (High)**: Impacts output quality — fix before production use
- **P2 (Medium)**: Documentation gap — fix for clarity
- **P3 (Low)**: Cosmetic/organizational — fix when convenient

### Fix findings and re-commit

Address findings in priority order. Each fix gets its own commit with a clear message referencing the audit finding.

---

## Phase 6: Write documentation

After the audit is clean, update the project documentation:

- **README.md**: Pipeline overview, skill table, architecture pattern, how to run
- **This document** (how-we-built-this.md): The process guide for replication

---

## Principles that guided the build

### 1. Research first, write second
Never write wisdom from memory alone. Launch a research agent, find real sources, extract specific named examples, and record every URL. Memory-based content is plausible but unverifiable. Research-based content is specific, correctable, and traceable.

### 2. Encode experts, not procedures
The wisdom catalog should read like a conversation with a 20-year veteran, not like a process manual. Failure stories are more valuable than rules. Named heuristics are more memorable than numbered steps. Counterintuitive insights are more useful than obvious truths.

### 3. Self-containment over DRY
Each skill carries its own copies of reference files. This violates DRY (Don't Repeat Yourself) but enables independence. A skill can be extracted, shared, modified, or run alone without worrying about broken dependencies. For skills that humans and AI agents will use in unpredictable combinations, self-containment wins.

### 4. Artifact-based state
All pipeline state lives in files on disk, not in conversation context. This makes the pipeline resumable across sessions, inspectable by humans, and debuggable when things go wrong. If it's not in a file, it doesn't exist.

### 5. Audit against the spec
The pipeline specification document is the contract. Every skill is audited against it, not against "does it seem good." The spec says what inputs, outputs, and responsibilities each skill must have. The audit verifies compliance. This catches gaps that feel-based review misses.

### 6. Fix what the audit finds
An audit that finds problems but doesn't lead to fixes is theater. Every finding gets a priority, every P0 and P1 gets fixed before the pipeline ships, and every fix gets its own commit with a message referencing the finding.

### 7. Record your sources
Every URL that informed a skill's content goes in `sources.md`. This is not bookkeeping — it's quality assurance. When a future contributor questions a claim in the wisdom catalog, the source URL lets them verify it. When new information emerges, the source list tells you which skills need updating.

---

## Timeline

This pipeline was built across multiple Claude sessions:

- **Session 1**: Built Skills 1-4 (exploratory designer, worldbuilder, IP researcher, vision designer)
- **Session 2**: Built Skills 5-8 (set designer, play designer, editor, creative writer)
- **Session 3**: Built Skills 9-12 (art director, product architect, card renderer already existed, orchestrator)
- **Session 3 continued**: Full pipeline audit, P0/P1/P2 fixes, README rewrite

Each session picked up from the previous one's commits. The checklist and pipeline roles document served as the persistent roadmap across sessions.

---

## Adapting this for your domain

This process works for any multi-step expert workflow:

1. **Map the real process** — study how professionals actually do it
2. **Identify the roles** — each role becomes a skill
3. **Write the spec** — inputs, outputs, responsibilities for each role
4. **Write the checklist** — what research each skill needs, what wisdom to find
5. **Build sequentially** — respect dependencies, research before writing
6. **Audit against the spec** — don't trust that it's right, verify it
7. **Fix what you find** — audit without action is theater

The domain doesn't matter. The process does.
