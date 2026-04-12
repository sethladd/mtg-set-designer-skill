# Pipeline Orchestration Wisdom Catalog

The orchestrator's job is deceptively simple: run skills in order, pass outputs forward, and present checkpoints. The wisdom is in knowing when the pipeline is working and when it's broken — and what to do about it. This catalog encodes failures from both Magic's real production pipeline and from multi-agent orchestration design.

---

## MTG Pipeline Breakdown Failures

### 1. The Wrong Handoff Point (Pre-2017)

Before 2017, Magic's pipeline had two phases: **Design** (led by Mark Rosewater) and **Development** (led by Erik Lauer). The handoff between them was the single most important moment in a set's production — and for years, it happened at the wrong time.

**The problem:** Design handed off a complete card file to Development, but the handoff was too late for Development to make fundamental changes. Development received finished work and either had to make cosmetic changes (insufficient) or discard/rebuild large portions (wasteful). The accelerated release schedule made it worse — Rosewater was co-leading Kaladesh and Amonkhet simultaneously, and exploratory design got compressed from one year to six months.

**Erik Lauer's insight:** Lauer questioned whether the handoff occurred at the optimal moment. His core insight: Development should not receive finished design work but instead should begin shaping the vision during the formative stages. The handoff should happen when the VISION is set but the DETAILS aren't.

**The fix:** The modern three-phase pipeline — Vision Design (4 months), Set Design (9 months with a 3-month gap), Play Design (3 months overlapping Set Design's final segment) — totaling ~20 months from exploratory start to Play Design completion. Vision hands off DIRECTION and a draftable card file, not a finished product.

**The Innistrad Green Curse Incident:** The canonical handoff failure. Lauer, leading development of original Innistrad, cut the green Curse from the set because Rosewater's handoff document failed to state that every color except white was supposed to get a Curse. Lauer had no way to know the cycle was intentional. The cycle was eventually completed in Dark Ascension. Rosewater acknowledged it was his failure of communication — the handoff must state not just WHAT is in the file but WHY it's there and what constraints must be preserved.

**Orchestrator lesson:** In our pipeline, each skill should hand off at the appropriate level of completion. Exploratory Design hands off POSSIBILITIES, not decisions. Vision Design hands off a BLUEPRINT, not a finished set. And every handoff artifact must explain the WHY, not just the WHAT.

### 2. The Transition Casualties (Rivals of Ixalan, 2018)

When WotC restructured from Design/Development to Vision/Set/Play, sets already in production were caught between systems. Rivals of Ixalan was particularly affected — it was designed under the old system but finalized under the new one. The result: a set that felt rushed and underdeveloped, with mechanics that didn't have enough depth.

**Orchestrator lesson:** Pipeline transitions are dangerous. If you change the pipeline mid-run, acknowledge that the current set may suffer. Don't try to retrofit a half-completed set to a new process — either commit to the old process for this run or restart.

### 3. The Missed Feedback Loop (Oko, Throne of Eldraine)

Oko, Thief of Crowns was released in Throne of Eldraine at a power level that warped every format. Over a series of late redesigns, the team lost sight of the card's raw power. Earlier versions had power tied to a broader stealing ability; iterative changes made the card stronger while the team focused on individual changes rather than cumulative impact.

**What went wrong:** The feedback loop had insufficient severity criteria AND suffered from late-redesign cascade blindness. Play Design announced it would subsequently take a wider variety of less-aggressive shots at format safeguards. The Kaladesh block's Saheeli/Felidar Guardian combo was a similar miss that directly led to the CREATION of the Play Design team.

**Orchestrator lesson:** Feedback loops need clear escalation triggers. "Flagged" is not enough — the loop must distinguish between "adjust numbers" (minor), "redesign card" (moderate), and "this breaks the format, stop the pipeline" (critical). Late-stage cascading changes are especially dangerous because each individual change looks small but the cumulative effect is unmeasured.

### 3b. The Transition Casualties (Rivals of Ixalan, Battle for Zendikar)

Rivals of Ixalan had a combined Vision/Set Design team because it fell between the old Two-Block Paradigm and the new Three-and-One Model. Rosewater was not part of the team. Dominaria (2018) is considered the first set fully built under the new system.

Battle for Zendikar had SIX mechanics (Landfall, Awaken, Ingest, Rally, Converge, Devoid) — too many. Rosewater calls it the biggest design failure of the modern era. The pipeline wasn't catching complexity overload; Kaladesh started the ratcheting down to only three mechanics per set.

**Orchestrator lesson:** Pipeline transitions are dangerous. If you change the process mid-run, acknowledge that the current set may suffer. Also: the orchestrator should track mechanic count and flag complexity overload early — don't let a set accumulate six mechanics before anyone notices.

### 4. The Art Commitment Constraint

In WotC's real pipeline, card concepts must be locked and art commissioned approximately three months into Set Design — long before the set is finalized. This creates a hard constraint: after art is commissioned, card mechanics can change BUT the card's visual identity is locked. A creature concepted as "a reef guardian" cannot become "a fire elemental" without recommissioning art (expensive, time-consuming).

**Orchestrator lesson:** In our pipeline, the Art Director skill runs AFTER Creative Writer, which runs AFTER Editor, which runs AFTER Play Design. This means art direction happens last, which is actually better than the real pipeline — we don't have the art commitment constraint. But it means any feedback loop that sends cards back to Set Design after art direction has run will invalidate art descriptions. The orchestrator should warn the user if a late-stage feedback loop would undo art direction work.

### 5. The Handoff Document Gap

Vision Design produces a handoff document that is the PRIMARY communication between Vision and Set Design. But handoff documents can't answer questions. When Set Design encounters a situation the handoff didn't cover (e.g., "the vision says 'the set should feel fast' but doesn't define what P/T curve 'fast' means"), they have to make judgment calls that may diverge from the original vision.

**Orchestrator lesson:** Our handoff artifacts should be as specific as possible. The orchestrator should validate that each artifact contains the fields the downstream skill expects. If an artifact is incomplete, flag it BEFORE invoking the downstream skill — not after the downstream skill discovers the gap mid-process.

---

## Orchestrator Agent Design Wisdom

### The Sequential Pipeline Pattern

This pipeline is fundamentally SEQUENTIAL — each skill depends on the output of the previous one. Microsoft's Azure Architecture Center identifies five orchestration patterns; ours is "Sequential Orchestration" with two "Maker-Checker Loops" (Color Pie Review and Play Design feedback).

**Strengths:**
- Clear dependencies — no ambiguity about execution order
- Each stage can validate its inputs before proceeding
- Checkpoints are naturally placed between stages

**Pitfalls:**
- A failure at any stage blocks all downstream work
- Context accumulates — later stages need outputs from much earlier stages
- Feedback loops can create cycles if not bounded

### Anthropic Multi-Agent Insights

Anthropic's own multi-agent research system provides directly relevant lessons:

- **Orchestrator-worker pattern** accounts for ~70% of production multi-agent deployments
- Multi-agent systems use ~15x more tokens than single-agent chat — context budgeting matters
- Each subagent needs: an objective, an output format, guidance on tools/sources, and clear task boundaries
- Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information
- **Core feedback loop:** Gather context → take action → verify work → repeat
- For long sessions: save plans to persistent storage, summarize completed phases before proceeding, spawn fresh subagents with clean contexts
- **Error recovery:** Classify failures (semantic vs. execution), retry transient errors, escalate structural problems to human review
- **Scale effort appropriately:** Simple queries = 1 agent with few tool calls; complex work = multiple specialized subagents

### Failure Classification for Recovery

Not all failures should be retried. A critical principle from agent error handling research: "Retrying a rate limit works. Retrying a hallucination makes it worse."

| Failure Type | Example | Response |
|-------------|---------|----------|
| **Execution** | Tool/API failure | Retry with backoff |
| **Semantic** | Valid output but wrong content | Re-invoke with clarified prompt |
| **State** | Agent's output contradicts prior artifacts | Halt, reconcile with user |
| **Timeout** | Skill takes too long | Re-invoke with simplified scope |
| **Dependency** | Required input artifact missing | Halt, identify which stage should have produced it |

### State Management: Artifact-Based

The pipeline uses an **artifact-based state management** pattern: state is encoded in files on disk (`set.json`, `vision_handoff.md`, etc.), not in memory or conversation context. This is the right choice because:

- Artifacts are inspectable — the user can review them between stages
- Artifacts survive session breaks — the pipeline can be resumed
- Each skill reads its inputs from artifacts, not from conversational context
- The orchestrator's job is to ensure artifacts exist and are well-formed, not to carry state

### Human-in-the-Loop Checkpoints

Best practices for checkpoints in agent pipelines:

1. **Present, don't summarize** — Show the user the ACTUAL artifact (or key excerpts), not a summary. Summaries lose critical details
2. **Ask specific questions** — "Does this vision match your intent?" is vague. "The set's three pillars are X, Y, Z — do these capture your vision?" is actionable
3. **Make approval binary** — "Approve and proceed" or "Revise" — don't offer partial approvals that create ambiguous state
4. **Include a preview of what's next** — Tell the user what will happen if they approve, so they understand the consequences

### Feedback Loop Protocol

Feedback loops in agent pipelines must be:

1. **Bounded** — Maximum iteration count (2 passes in our pipeline). Unbounded loops risk infinite cycles
2. **Severity-routed** — Minor issues stay within the current stage. Major issues escalate to earlier stages. Critical issues halt the pipeline for user review
3. **Convergent** — Each iteration should reduce the number of flags. If iteration 2 has MORE flags than iteration 1, something is systematically wrong — escalate to user
4. **Documented** — Each iteration's changes are recorded so the user can see what was adjusted and why

### Context Management

Each skill invocation needs context, but not ALL context:

- **Always pass:** The current `set.json` (or equivalent primary artifact), the world guide / IP catalog
- **Pass on demand:** Reports from previous stages (only if the current skill references them)
- **Never pass raw:** Full conversation history from previous stages — this bloats context and confuses the current skill
- **Summarize when needed:** If a prior stage produced a 500-line report, pass a summary to the current skill with a note that the full report is available on disk

### Error Recovery and Graceful Degradation

When a skill produces incomplete or problematic output:

| Severity | Example | Response |
|----------|---------|----------|
| **Recoverable** | Set.json has 250 cards instead of 261 | Flag to user, proceed with note |
| **Blocking** | Set.json is not valid JSON | Halt pipeline, ask user to fix |
| **Degraded** | Art descriptions written for 90% of cards | Proceed, flag remaining 10% for manual attention |
| **Critical** | Vision handoff has no mechanics defined | Halt pipeline, re-run Vision Design |

The orchestrator should always prefer PROCEEDING WITH FLAGS over HALTING, unless the issue would cause downstream skills to produce garbage output.

---

## Named Heuristics

### 1. The Handoff Completeness Test
Before invoking a downstream skill, check: does the handoff artifact contain every field the downstream skill expects? If the vision handoff is missing archetypes, Set Design can't build the draft format. Catch this BEFORE invocation, not after.

### 2. The Feedback Severity Router
When a feedback loop fires, route by severity:
- **Number change** (P/T, mana cost) → The flagging skill (Play Design) adjusts directly
- **Card redesign** (new ability, different role) → Send back to Set Design
- **Mechanic is broken** (core mechanic doesn't work) → Escalate to user, potentially re-run Vision Design
- **Identity crisis** (the set lost its pillars) → Stop the pipeline, re-run from Vision Design

### 3. The Checkpoint Readiness Test
At each checkpoint, ask: "Is the user equipped to make a MEANINGFUL decision?" Present specific artifacts, specific questions, and specific consequences of approval. "Does this look good?" is never an acceptable checkpoint prompt.

### 4. The Artifact Chain Test
Verify the complete chain: every output artifact from skill N is consumed as input by at least one downstream skill. If an artifact is produced but never consumed, it's either dead weight or a sign that a skill is missing a dependency.

### 5. The Two-Pass Limit
Feedback loops run at most twice. If the second pass produces more flags than the first, the problem is systemic — don't loop again, escalate to user. If the second pass reduces flags to acceptable levels, proceed. This prevents infinite loops and forces convergence.

### 6. The Context Window Budget
Each skill invocation should include ONLY the artifacts it directly needs. Don't pass the full pipeline history to every skill. Set Design needs the vision handoff and world guide — it doesn't need the exploratory design document. Art Direction needs the named card file and world guide — it doesn't need the play design report.

### 7. The Graceful Degradation Principle
If a skill produces partial output (90% of cards have art descriptions), the orchestrator should FLAG but PROCEED. Downstream skills can work with partial input and the gaps can be filled later. Only halt for issues that would cause downstream skills to produce garbage.

### 8. The Pipeline Resume Test
At any point, the pipeline should be resumable from the last completed stage. All state lives in artifacts on disk, not in conversation context. If a session ends mid-pipeline, the orchestrator should be able to assess which stages are complete and resume from the next pending stage.
