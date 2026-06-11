# References

*Consolidated external literature for this assessment (carried over from the v1 audit research,
where every URL was verified reachable and on-topic as of 2026-06-03). Labels follow the audit-wide convention —
**VERIFIED** (the source states the claim directly), **PARTIAL** (substance supported, a
figure/wording is paraphrased by a secondary outlet or revised since), **UNVERIFIED**
(repeated but not confirmed against a primary here). Cost/inference figures are
API-equivalent cost-to-serve, never cash.*

---

## 1. The paradigm — LLM-as-Operating-System / Software 3.0

- Andrej Karpathy, *Software Is Changing (Again)* — Y Combinator AI Startup School, 2025-06-17. Primary host: https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again — **VERIFIED**
- Video: https://www.youtube.com/watch?v=LCEmiRjPEtQ — **VERIFIED**
- Author confirmation (announcing the talk): https://x.com/karpathy/status/1935518272667217925 — **VERIFIED**
- Talk notes (LLM-OS analogy, 1960s-mainframe framing, Llama→Linux ecosystem split): http://ikyle.me/blog/2025/andrej-karpathy-software-is-changing-again — **VERIFIED** (faithful summary)
- Software 3.0 explainer: https://travis.media/blog/software-3-0-ai-changing-programming-karpathy/ — **VERIFIED** (summary)

## 2. AI safety / alignment context — AI 2027

- AI 2027 (project site), AI Futures Project — https://ai-2027.com — **VERIFIED**
- About / authors (Kokotajlo, Lifland, Larsen, Dean): https://ai-2027.com/about — **VERIFIED**
- Timeline revision toward the early 2030s (secondary): https://www.hungarianconservative.com/articles/tech/ai-futures-project-ai-2027-apocalypse-timeline-superintelligence-daniel-kokotajlo/ — **PARTIAL**

## 3. Multi-agent orchestration — the case FOR and AGAINST

- Anthropic, *How we built our multi-agent research system* (90.2% upside, ~15× tokens, ~80% variance): https://www.anthropic.com/engineering/multi-agent-research-system — **VERIFIED**
- Cognition, *Don't Build Multi-Agents* (the steel-man against parallel sub-agents): https://cognition.ai/blog/dont-build-multi-agents — **VERIFIED**
- Cognition-vs-Anthropic debate, same-day aggregation (2025-06-13): https://news.smol.ai/issues/25-06-13-cognition-vs-anthropic — **VERIFIED** (third-party)
- *The Orchestration of Multi-Agent Systems* (academic corroboration of gating conditions): https://arxiv.org/abs/2601.13671 — **VERIFIED**

## 4. Context engineering & long-horizon reliability

- Anthropic, *Effective context engineering for AI agents* (+29% / +39%; 84% token cut): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — **VERIFIED**
- Anthropic, *Effective harnesses for long-running agents*: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents — **VERIFIED**
- METR, *Measuring AI Ability to Complete Long Tasks* (~7-mo doubling): https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ ; paper https://arxiv.org/abs/2503.14499 — **VERIFIED**
- *The Illusion of Diminishing Returns: Measuring Long-Horizon Execution in LLMs* (per-step error rises): https://arxiv.org/abs/2509.09677 — **VERIFIED**
- *Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents* (domain-stratified decay): https://arxiv.org/abs/2603.29231 — **VERIFIED**

## 5. Inference economics

- Epoch AI, *LLM inference prices have fallen rapidly but unequally across tasks* (9×–900×/yr, median ~50×/yr): https://epoch.ai/data-insights/llm-inference-price-trends — **VERIFIED**
- Prompt caching / batching economics (caching ~90% cost / ~85% latency on long stable prefixes): https://www.prompthub.us/blog/prompt-caching-with-openai-anthropic-and-google-models — **VERIFIED** (secondary; reputable)

## 6. The open-source agentic-OS ecosystem (comparables)

- OpenClaw (MIT; local-first Markdown memory; ~377K stars as of 2026-06-03): https://github.com/openclaw/openclaw ; site https://openclaw.ai/ — **VERIFIED**
- OpenClaw — independent organizational-impact commentary (NVIDIA): https://blogs.nvidia.com/blog/what-openclaw-agents-mean-for-every-organization/ — **VERIFIED** (third-party)
- Nous Research (Hermes open-weights; primary org): https://nousresearch.com — **VERIFIED**
- Hermes 4.3 release (first model post-trained on the Psyche network): https://nousresearch.com/introducing-hermes-4-3 — **VERIFIED**
- Nous Research / Psyche decentralized-training deep-dive (independent): https://oakresearch.io/en/analyses/innovations/nous-research-psyche-open-source-decentralized-ai-revolution — **VERIFIED** (third-party); the ~$50M Paradigm round / ~$1B valuation figure is **PARTIAL** (secondary): https://www.gate.com/news/detail/nous-research-deep-dive-a-decentralized-ai-lab-that-paradigm-invested-in-at-20290685

## 7. The open SKILL.md standard (shared, cross-vendor layer)

- Canonical specification: https://agentskills.io/specification — **VERIFIED**
- Overview: https://agentskills.io/home — **VERIFIED**
- Origin — Anthropic, *Equipping agents for the real world with Agent Skills*: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — **VERIFIED**
- Public repo: https://github.com/anthropics/skills — **VERIFIED**

## 8. Pattern sources consumed (pattern-only, no vendor code)

- SWE-agent (MIT) — the agent-computer-interface (ACI) edit-safety / syntax-gate pattern: https://github.com/SWE-agent/SWE-agent — **VERIFIED** (real public MIT project)
- agentevals (langchain-ai, MIT) — the trajectory-evaluation pattern: https://github.com/langchain-ai/agentevals — **VERIFIED** (real public MIT project)

---

*Note on arXiv identifiers:* arXiv IDs use the `YYMM.NNNNN` convention (e.g. `2503.*` = Mar
2025, `2601.*` = Jan 2026). The `/abs/` form is the stable landing page. If any single ID
fails to resolve at read-time, treat that row as **PARTIAL** pending re-confirmation; the
substance is independently corroborated by the Anthropic / Cognition / METR / Epoch
primaries above.

---

*[Back to the assessment](./00-executive-assessment.md)*
