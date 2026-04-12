# Sources

Web references consulted during the creation of the mtg-set-pipeline skill.

## MTG Pipeline History and Handoff Process

- [Nuts & Bolts: Three Stages of Design (Rosewater, 2015)](https://magic.wizards.com/en/news/making-magic/nuts-bolts-three-stages-design-2015-03-30) — The transition from Design/Development to the three-stage pipeline, Erik Lauer's insight about wrong handoff timing
- [Stages of Design (Rosewater)](https://magic.wizards.com/en/news/making-magic/stages-of-design) — How Vision, Set, and Play Design work together in the modern pipeline
- [Innistrad Vision Design Handoff Document (Rosewater, 2021)](https://magic.wizards.com/en/articles/archive/making-magic/innistrad-design-handoff-document-2021-08-23) — A full real handoff document publicly shared, showing the contract between Vision and Set Design
- [March of the Machine Vision Design Handoff Part 1](https://magic.wizards.com/en/news/making-magic/march-of-the-machine-vision-design-handoff-document-part-1) — Modern handoff document showing current pipeline format
- [March of the Machine Vision Design Handoff Part 2](https://magic.wizards.com/en/news/making-magic/march-of-the-machine-vision-design-handoff-document-part-2) — Continuation of the MOM handoff
- [Lorwyn Eclipsed Vision Design Handoff Part 1](https://magic.wizards.com/en/news/making-magic/lorwyn-eclipsed-vision-design-handoff-document-part-1) — Recent handoff document example
- [Outlaws of Thunder Junction Vision Design Handoff Part 1](https://magic.wizards.com/en/news/making-magic/outlaws-of-thunder-junction-vision-design-handoff-document-part-1) — Another recent handoff example
- [Aetherdrift Vision Design Handoff Part 2](https://magic.wizards.com/en/news/making-magic/aetherdrift-vision-design-handoff-part-2) — Latest available handoff document
- [Khans of Tarkir Design Handoff Part 1](https://magic.wizards.com/en/news/making-magic/khans-of-tarkir-design-handoff-part-1) — Older handoff document from the Design/Development era for comparison

## Pipeline Failures and Lessons

- [Play Design: Lessons Learned (2019)](https://magic.wizards.com/en/news/feature/play-design-lessons-learned-2019-11-18) — Play Design team reflecting on missed feedback loops and cards that slipped through
- [State of Design 2016 (Rosewater)](https://magic.wizards.com/en/articles/archive/making-magic/state-design-2016-2016-08-29) — Rosewater's frank assessment of what went wrong and right, including Battle for Zendikar
- [State of Design 2022 (Rosewater)](https://magic.wizards.com/en/news/making-magic/state-of-design-2022) — Pipeline maturity assessment, lessons from modern three-stage process
- [Odds and Ends: Rivals of Ixalan (Rosewater, 2018)](https://magic.wizards.com/en/news/making-magic/odds-ends-rivals-ixalan-2018-01-29) — Rivals of Ixalan caught in the pipeline transition
- [Rosewater Ranks His Set Designs](https://icv2.com/articles/news/view/44730/magic-the-gathering-lead-designer-mark-rosewater-ranks-his-set-designs) — Rosewater's self-assessment of pipeline successes and failures
- [Burning the Midnight Oil Part 1](https://magic.wizards.com/en/news/making-magic/burning-the-midnight-oil-part-1) — Behind-the-scenes on pipeline pressure and set design timelines

## Orchestrator Agent Design Patterns

- [AI Agent Design Patterns (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Sequential, fan-out, routing, and orchestrator patterns for AI agent systems
- [Multi-Agent Orchestration Guide](https://gurusup.com/blog/multi-agent-orchestration-guide) — Comprehensive guide to coordinating multiple specialized agents
- [Agent Orchestration Patterns](https://gurusup.com/blog/agent-orchestration-patterns) — Named patterns: sequential chain, router, supervisor, collaborative
- [Multi-Agent Orchestration (Wikipedia-style)](https://artificial-intelligence-wiki.com/agentic-ai/agent-architectures-and-components/multi-agent-orchestration/) — Overview of orchestration architectures and state management
- [AWS Multi-Agent Orchestration Guidance](https://aws.amazon.com/solutions/guidance/multi-agent-orchestration-on-aws/) — AWS reference architecture for multi-agent systems with checkpoints

## Human-in-the-Loop and Checkpoint Design

- [Human-in-the-Loop AI with LangGraph](https://dev.to/sreeni5018/beyond-input-building-production-ready-human-in-the-loop-ai-with-langgraph-2en9) — Checkpoint design, when to pause for human review, how to present decisions
- [LangChain Human-in-the-Loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) — Patterns for human review checkpoints in agent workflows
- [LangGraph Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) — Sequential workflow design with state persistence

## Error Recovery and Feedback Loops

- [AI Agent Error Handling: Resilient Pipelines](https://agentcenter.cloud/blogs/ai-agent-error-handling-resilient-pipelines) — Error recovery patterns for multi-step agent workflows
- [AI Agent Error Handling and Fallback Strategies](https://agentmelt.com/blog/ai-agent-error-handling-fallback-strategies/) — Graceful degradation, retry vs. escalate decisions
- [Self-Healing AI Agent Pipeline](https://dev.to/miso_clawpod/how-to-build-a-self-healing-ai-agent-pipeline-a-complete-guide-95b) — Building pipelines that detect and recover from failures
- [AI Agent Crash Recovery Patterns](https://cipherbuilds.ai/blog/ai-agent-crash-recovery-patterns) — Session recovery, state persistence, and resumability
- [Why AI Agent Projects Fail](https://dev.to/varun_pratapbhardwaj_b13/i-tracked-why-ai-agent-projects-fail-80-of-the-time-its-not-the-agents-347f) — Common orchestration failures and how to prevent them

## Prompt Chaining and Context Management

- [Prompt Chaining Workflow (AWS)](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/workflow-for-prompt-chaining.html) — AWS prescriptive guidance on chaining prompts across specialized agents
- [AI SDK: Workflows and Agents](https://ai-sdk.dev/docs/agents/workflows) — Sequential and DAG-based workflow patterns for agent orchestration
- [Multi-Agent Systems with Context Engineering (Vellum)](https://vellum.ai/blog/multi-agent-systems-building-with-context-engineering) — Four context techniques: writing, selecting, compressing, isolating context between agents
- [Prompt Chaining and Orchestration Methods (Refonte)](https://www.refontelearning.com/blog/prompt-chaining-and-advanced-orchestration-methods) — Sequential prompt chaining patterns and context budgeting

## Anthropic-Specific Guidance

- [Building Agents with Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk) — Anthropic's guidance on multi-step agent workflows, subagent design principles
- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) — Coordinating multiple Claude agents: shared task lists, file locking, plan approval mode
- [How We Built Our Multi-Agent Research System (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) — Orchestrator-worker architecture, 90.2% improvement over single-agent, token usage patterns (~15x for multi-agent), parallel tool calling
- [5 Claude Code Agentic Workflow Patterns (MindStudio)](https://www.mindstudio.ai/blog/claude-code-agentic-workflow-patterns) — Sequential, orchestrator, parallel, agent teams, and headless patterns with when-to-use guidance

## Additional MTG Pipeline Sources

- [Strixhaven Vision Design Handoff Part 1](https://magic.wizards.com/en/news/making-magic/strixhaven-vision-design-handoff-document-part-1-2021-04-19) — Complete handoff document showing faction breakdowns, mechanic specifications, and design philosophy
- [Zendikar Rising Vision Design Handoff](https://magic.wizards.com/en/news/making-magic/zendikar-rising-vision-design-handoff-document-2020-09-28) — Another full handoff document example
- [HITL Best Practices for AI Agents (Permit.io)](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo) — Four checkpoint types: interrupt/resume, human-as-tool, approval flows, fallback escalation
- [Error Recovery in AI Agent Development (GoCodeo)](https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development) — Five failure categories: execution, semantic, state, timeout, dependency; escalate vs. retry decision logic
