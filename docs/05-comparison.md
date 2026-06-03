# Comparative Analysis — The System Under Review Against ECC, OpenClaw, Hermes, and Nous

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## How to read this comparison

This document places the system under review (SUR) against four reference points in the self-hosted, local-first agentic-runtime category: **ECC** (a cross-harness skill/config bundle), **OpenClaw** (the most-starred consumer-facing agent), **Hermes Agent** (the fastest-growing self-hosted agent framework), and **Nous Research** (the open-weight model line behind Hermes). It is structured as a property matrix, then a short honest section per competitor, then "What GPT said" and "What researchers say."

Three rails govern every line below, because auditor integrity is the deliverable:

1. **The asymmetry is weighted, once, plainly.** The SUR is built by **one person with AI assistance over ~19 recorded calendar days**, not a funded team. Competitor maturity (funding, headcount, reach, marketplaces) is a **roadmap to learn from, not a deficit to spin**. (_DIGEST.md §8)
2. **Every non-trivial claim carries VERIFIED / PARTIAL / UNVERIFIED.** No "beats frontier," "fully sovereign," "AGI," or unbacked superlative appears in the source research, and none is asserted here.
3. **The one differentiator that the evidence actually supports is structural, not architectural.** In this category the agent harness and the open `SKILL.md` capability format are **commodities** — so the contest is on the layers above them, not on the harness. (_DIGEST.md §1; openclaw.md §4)

A note on terminology used throughout. The reference projects ship a **harness** — a runtime you install and run. The SUR's stated posture is different in kind: it **consumes** open-source patterns one-way, consuming them into its own owned framework and keeping the method private. The differentiator row in the matrix below is exactly this: *they ship a harness; this one consumes.* The word "harness" is used only to describe the other tools, never the SUR. (consumption.md §6)

---

## 1. The property matrix

The matrix scores **properties** (rows) across the five reference points (columns). Cells state the position and a confidence label. "n/a" marks a property that does not apply to that project's shape (ECC, for example, is not a runtime, so runtime-level rows often do not apply to it).

| Property | SUR | ECC | OpenClaw | Hermes | Nous |
|---|---|---|---|---|---|
| **Shape / category** | Gate-first BYOM agent-OS shell (React + stdlib-Python server) — **VERIFIED** | Cross-harness skill/config/agent/hook bundle that installs *onto* a harness — **VERIFIED** | Self-hosted autonomous agent, messaging-app UI — **VERIFIED** | Self-hosted single-agent framework with sub-agent delegation — **VERIFIED** | Open-weight model line + decentralized-training research — **PARTIAL** |
| **License** | Apache-2.0 (public repo) — **VERIFIED** | MIT — **VERIFIED** | MIT — **VERIFIED** | MIT — **VERIFIED** | Open-weight (lab-published) — **PARTIAL** |
| **Open `SKILL.md` format** | Yes (shared open standard) — **VERIFIED** | Yes; cross-harness adapters — **VERIFIED** | Yes; authored against agentskills.io — **VERIFIED** | Yes — **VERIFIED** | n/a (model layer) |
| **Reach (stars, point-in-time)** | Not a popularity contestant; pre-distribution — **VERIFIED** | ~205K stars (4.5-mo-old, viral) — **VERIFIED** | ~247K → ~355K (date-dependent) — **VERIFIED snapshot / PARTIAL "largest"** | ~175K in <4 months — **VERIFIED** | Lab-scale, not star-driven — **PARTIAL** |
| **Consume-vs-ship posture** | **Consumes** patterns one-way; publishes a verifiable shell, withholds the method — **VERIFIED structurally** | Built to be **consumed + published** (open-core) — **VERIFIED** | Ships a harness + open skill registry — **VERIFIED** | Ships a harness; sub-agents seal "by omission" — **VERIFIED** | Ships open weights + training research — **PARTIAL** |
| **Human-in-the-loop gate that bites** | Autonomy dial L0–L5 × 4–20 risk → act/report/queue; **high-risk queues even at L5**; append-only queue — **VERIFIED** | Escalation + audit in the operator shell (Hermes/operator layer); oversight-gated crons — **PARTIAL** | Permissive default; per-command approval **disable-able** via API — **VERIFIED** | Oversight present; not a coded fail-closed floor — **PARTIAL** | n/a |
| **Least-privilege execution** | Closed allow-list action runner; **explicitly not a raw shell** — **VERIFIED** | Depends on the host harness — **n/a / PARTIAL** | Full user privileges by default; documented Docker-escape config — **VERIFIED** | Tool-capable agent; sandbox posture not fail-closed-by-default — **PARTIAL** | n/a |
| **Documented security failures** | None on record in the public shell; pre-publish housekeeping owed — **PARTIAL** | Security-*focus* (AgentShield) is a strength; claims vendor-stated — **PARTIAL** | Multiple CVEs incl. one-click RCE (CVSS 8.8); ~1.5M-token breach; "shadow superuser" demo — **VERIFIED** | Fewer public incidents; smaller blast surface by design — **PARTIAL** | n/a |
| **Append-only auditable boundary** | `gate-queue.jsonl` + retention audit, never rewritten — **VERIFIED** | CI/coverage hygiene; not a sealed audit boundary — **PARTIAL** | Audit not the default posture — **PARTIAL** | File memory over SQLite; not a sealed gate audit — **PARTIAL** | n/a |
| **File-based inspectable memory** | Plain files; curated surface reads **only declared files**, never globs — **VERIFIED** | SQLite session store + skill extraction — **PARTIAL** | Markdown files on disk — **VERIFIED** | Persona/memory/user files over full-text SQLite — **VERIFIED** | n/a |
| **Fail-closed quality/regression guard** | Retention loop: KEEP only if no metric degrades, else byte-exact sha256 revert — **VERIFIED** | "Instincts" skill-extraction + confidence scoring (not a sealed revert gate) — **PARTIAL** | Not a default — **UNVERIFIED** | Curated memory note-taking (not a revert gate) — **PARTIAL** | n/a |
| **Multi-agent orchestration** | Surface present (grid/org/channels); **concurrent execution engine not in public repo** — **VERIFIED surface / UNVERIFIED engine** | `/multi-plan` `/multi-execute` ("NanoClaw v2") commands — **PARTIAL** | Agent-per-channel; community skills — **PARTIAL** | Single-agent loop + isolated sub-agents (can't see each other's work) — **VERIFIED** | n/a |
| **BYOM / model-agnostic** | Yes; one ~250-line stdlib router + config; local-first path first-class — **VERIFIED** | Routes across harnesses/models — **PARTIAL** | Claude/GPT/Gemini/DeepSeek + local — **VERIFIED** | Hosted + local providers — **VERIFIED** | Produces the models others BYOM — **PARTIAL** |
| **Own-model production line** | None (BYOM only; ~0.5B fine-tune track unfinished) — **VERIFIED / UNVERIFIED projection** | None (config layer) — **VERIFIED** | None (uses external LLMs) — **VERIFIED** | None (uses Nous + others) — **VERIFIED** | **Yes** — open weights + decentralized training — **PARTIAL** |
| **Shipped paid go-to-market** | None yet (pre-distribution) — **VERIFIED** | **ECC Pro $19/seat/mo** (hosted GitHub App) — **VERIFIED** | Foundation-stewarded; no per-seat price — **PARTIAL** | No per-seat price on record — **PARTIAL** | Lab/research funding model — **PARTIAL** |
| **Public engineering hygiene (CI/coverage)** | Internal smoke/eval harness (17–19/19; 20/20); not a public CI badge — **PARTIAL** | ~1,000-test CI, 80% coverage gate — **VERIFIED** | Large contributor base; security CVE remediation cadence — **PARTIAL** | Active project; hygiene not independently measured here — **PARTIAL** | Research-grade, not product-CI — **PARTIAL** |
| **Self-down-labelling honesty artifact** | 12-claim register: **4 VERIFIED / 8 PARTIAL / 0 UNVERIFIED** — **VERIFIED** | Marketing-led README; vendor-stated metrics (60%/70%) — **PARTIAL** | Marketing-led README — **PARTIAL** | Marketing-led README — **PARTIAL** | Lab papers (peer-norm, not a claim register) — **PARTIAL** |
| **Bus factor (single-maintainer risk)** | HIGH (one builder + AI) — **VERIFIED** | HIGH (1,426 vs 47 commits, ~30:1) — **VERIFIED** | LOW (1,000+ contributors) — **PARTIAL** | Lab-backed team — **PARTIAL** | Lab-backed team — **PARTIAL** |

**Reading the matrix.** Three patterns hold across the rows. First, the SUR and the reference projects **converge** on the commodity layers (open `SKILL.md`, BYOM, file memory) — none of those is a defensibility for anyone. Second, the SUR **leads** on the gate/least-privilege/audit/retention/honesty rows, which is precisely where the loudest incumbent (OpenClaw) is documented to be weakest. Third, the SUR **trails** on reach, paid go-to-market, public CI hygiene, and an own-model line — and on bus factor it is tied with ECC, so single-maintainer risk is *not* a differentiator either way. (ecc.md §3, §9; openclaw.md §5, §8; gpt-competitors.md §2.4)

---

## 2. Per-competitor honest sections

### 2.1 ECC ("Everything Claude Code") — same category, opposite strategy

**What it is.** ECC is **not a model, harness, runtime, or server.** It is a cross-harness *bundle* — skills, agents, hooks, rules, command shims — that installs **onto** existing harnesses (Claude Code, Cursor, Codex, OpenCode, Gemini, Zed, Copilot) and standardizes how they operate. It uses the open `SKILL.md` convention plus per-harness adapter folders. (ecc.md §1, §4) — **VERIFIED.**

**Scale, read honestly.** Live GitHub API (2026-06-03): **205,179 stars / 31,492 forks / 1,030 watchers / 66 open issues**, MIT, created 2026-01-18 — only ~4.5 months old. (ecc.md §2) — **VERIFIED.** The star count is genuine but **young and viral**: a 2026-03-18 write-up cited 82K stars, so the repo roughly **2.5×'d in ~2.5 months**, attributed to a ~900K-view social thread; the watchers-to-stars ratio (~0.5%) and thin Discussions are consistent with *starred-on-sight, not deeply adopted*. The honest reading is **attention, not verified active-deployment count**. (ecc.md §2 caveat) — **PARTIAL, triangulated.**

**Bundle counts (README, exactness drifts):** 63 agents, 249 skills, 79 legacy command shims, 34 rules, 15+ hook event types, 14 pre-wired MCP servers. (ecc.md §4) — **VERIFIED (README); PARTIAL on exactness.**

**Genuine strengths to respect.** Reach and mindshare (category-leading stars; it *is* the reference point builders cite); cross-harness breadth and portability; **real engineering hygiene** (~1,000-test CI, 80% coverage gate, regular release cadence, a merged-PR contribution process); a security focus (AgentShield) rare in the category; and a **shipped paid go-to-market** (ECC Pro, $19/seat/month, hosted GitHub App for private-repo PR audits). Its operator shell ("Hermes/operator shell," release-candidate) is the feature most directly comparable to the SUR's full operator ambition — newer and shallower, but **public, documented, and installable**, which is a distribution advantage the SUR currently lacks. (ecc.md §6, §7, §8) — **VERIFIED**, except AgentShield counts are **PARTIAL**.

**Honest gaps.** Star count outruns engagement; **single-maintainer bus factor is HIGH** (`affaan-m` 1,426 commits vs #2 human 47, ~30:1, two bots in the top 4); the loudest community critique is *"most people just need a good config file, not an entire ecosystem"*; install/uninstall friction is acknowledged in open issues. And its headline performance numbers — **"60% cost reduction" (Opus→Sonnet routing)** and **"70% reduction in thinking tokens"** — are **config-default deltas with no published methodology**: vendor-stated, scope = its own defaults. They must **not** be restated as benchmarks. (ecc.md §3, §5, §9) — **VERIFIED** (bus factor, critique); **PARTIAL** (the metrics).

**The honest contrast.** ECC = **open, broad, distributed, viral, one-person breadth, $19/seat open-core, built to be consumed and published.** The SUR = **sealed, deep, method-as-defense, human-gated, also one-person — but trading reach for a private iterative build-and-verify loop, a failure-pattern regression memory, and a gate layer.** The same solo asymmetry on both sides means **bus factor is not a differentiator**; the real contrast is *governance maturity* (ECC has it shipped) versus *defensibility method* (the SUR's claimed edge). ECC is **ahead on reach and a shipped paid seat price** — that is the SUR's go-to-market gap, **not an engineering deficit.** The SUR must never claim it "beats" ECC on adoption; it does not. (ecc.md §10; gpt-competitors.md §2.5) — **VERIFIED framing.**

### 2.2 OpenClaw — the category's reach leader and its cautionary tale

**What it is.** A free, MIT-licensed, self-hosted autonomous assistant that executes tasks via external LLMs, using **consumer messaging platforms** (Signal/Telegram/Discord/WhatsApp) as its primary UI rather than an IDE or terminal. Created by Peter Steinberger; written in TypeScript/Swift; ships the runtime plus connectors, persistent memory, a skills engine, and first-class tools (browser, canvas, cron, sessions). (openclaw.md §1) — **VERIFIED.**

**Scale.** By ~2026-03-02 it reported ~247,000 stars / ~47,700 forks; reported at ~355K by mid-2026; at one point the most-starred project on GitHub. (openclaw.md §2) — **VERIFIED snapshot; "beat React" framing PARTIAL (date-dependent).** Governance churn is real: renamed twice in early 2026 (a trademark complaint drove the "Moltbot"→"OpenClaw" change), the creator joined OpenAI 2026-02-14, and an "OpenClaw Foundation" now stewards it. (openclaw.md §2) — **VERIFIED.**

**Why it is the load-bearing comparison — security is the central finding.** The pattern is consistent: extreme capability + minimal default guardrails + exposure to untrusted input = a broad, repeatedly-exploited surface.
- Default permission model is **permissive** (full user privileges; per-command approval can be **disabled** via API; a documented config enables a Docker escape; credentials stored **plaintext** under `~/.openclaw/`). (openclaw.md §5) — **VERIFIED.**
- **CVE-2026-25253 (CVSS 8.8): one-click RCE** via token exfiltration through an unvalidated `gatewayUrl`; plus command-injection CVEs (CVE-2026-24763, CVE-2026-25157) and indirect-prompt-injection via web (CVE-2026-22708). (openclaw.md §5) — **VERIFIED.**
- A companion-service breach exposed **~1.5M API auth tokens, ~35K emails, and plaintext model keys**; a named researcher demonstrated a **"shadow superuser"** — obtaining keys, sending messages as the user, executing admin commands. (openclaw.md §5) — **VERIFIED (reported).**
- Independent academic measurement: baseline sandbox-escape defense averaged **~17%**; adding a **staged human-in-the-loop defense layer** (allowlist → semantic judge → risk-pattern rules → sandbox guard) raised overall defense to **19%–92% (Claude ~91.5%)**. (openclaw.md §5) — **VERIFIED (events); PARTIAL (exact single-paper percentages).**

**The symmetry that defines the comparison.** OpenClaw's own academic remedy — *a staged human-in-the-loop defense layer* — **is precisely the SUR's claimed differentiator.** The SUR ships a coded autonomy floor (high-risk actions queue for human approval even at maximum privilege) and an append-only approval queue with named gate classes: inspectable mechanism, not policy prose. (openclaw.md §8; capabilities.md §5) — **VERIFIED structurally.**

**Honest both ways.** OpenClaw has **scale, contributors, reach, and a low-friction messaging UX** a solo-plus-AI effort cannot match — genuine assets. (openclaw.md §6) The SUR's credible edge against it is **safety posture and method, not capability or community size**, and that edge is only real if the SUR's public shell and gate evidence are shipped and reproducible. (openclaw.md §8) — **PARTIAL judgment, well-supported.**

### 2.3 Hermes Agent — the architecture contrast

**What it is.** MIT, Python, self-hosted, launched 2026-02-25; **~175K GitHub stars in under four months** — widely described as the fastest-growing open-source agent framework of 2026 (popularity, **not** usage or quality — flag carried). (gpt-competitors.md §2.1) — **VERIFIED.**

**Architecture (the contrast that matters).** A **single-agent synchronous loop with isolated sub-agent delegation** — sub-agents **cannot see each other's in-progress work**; per its own docs, sealing is *"by omission, not by mechanism."* A multi-adapter gateway makes one daemon appear across ~14–20 messaging surfaces; file memory (persona + memory + user files) over a full-text SQLite index; BYOM. Critically, its **"self-improvement" = autonomous skill-writing + curated memory, NOT weight updates** — independent reviewers characterise it as structured note-taking with retrieval. (gpt-competitors.md §2.1) — **VERIFIED.**

**Audit relevance.** Hermes is the cleanest **architecture** comparison. Its "sealing by omission" is the inverse of what the multi-agent literature recommends (Cognition: *share full traces*; see §4 below) — but for *scoped, read-only* sub-tasks that omission is defensible. The SUR's claimed differentiation is not "more agents" but a **gate + audit + retention** wrapper around whatever orchestration runs; on the orchestration mechanism itself, Hermes is a mature, public reference the SUR's *engine* (not in the public repo) has not yet matched in the open. (gpt-competitors.md §2.1, §2.4) — **VERIFIED.**

### 2.4 Nous Research — the sovereignty / model-layer line

**What it is.** The lab behind Hermes also ships **open-weight models** (function-calling, hybrid reasoning, low-refusal alignment; one variant advertises a **512K-token context**) and pursues **decentralized training over the internet** (volunteer-GPU coordination reportedly cutting inter-GPU communication by orders of magnitude; a multi-tens-of-billions-parameter distributed pretraining run claimed). (gpt-competitors.md §2.3) — **PARTIAL** (weights and decentralized-training research are real and published; specific scale/quality claims are the lab's own and were not re-benchmarked here).

**Audit relevance.** Nous is **not a runtime competitor** — it is the **model production line** the others (and the SUR) BYOM against. Its relevance is twofold: (1) it **validates the BYOM / run-your-own-model strategy** the SUR is built on; (2) it points at a credible **long-horizon path to producing the model layer without hyperscaler compute.** For the SUR, this is a **roadmap to learn from, not a present capability**: the SUR's own model line is a ~0.5B fine-tune track that is **unfinished** (−20pp regression → +13.3pp sub-threshold → an unrun projection). The SUR should never imply it has Nous's model line; it has the BYOM wiring that *consumes* such a line. (gpt-competitors.md §2.3; metrics.md §6) — **PARTIAL.**

---

## 3. The consume-vs-harness differentiator, examined

This is the matrix row that most distinguishes the SUR's *strategy* (as opposed to its *capabilities*, which converge with everyone on the commodity layers). It deserves its own treatment because it is easy to over-claim.

**The reference projects ship a harness.** ECC ships a bundle to install onto harnesses; OpenClaw and Hermes ship harnesses you run. Their value flows **outward** — published, MIT, copyable, built to be adopted. (ecc.md §10; openclaw.md §1) — **VERIFIED.**

**The SUR consumes.** Its stated posture is **disciplined, mostly-one-way consumption**: consume patterns from permissively-licensed projects, re-implement them inside its own owned framework, keep the method private. This is **VERIFIED structurally** — the SUR is written in a different language (stdlib Python) from the vendors' TS/JS, keeps **segregated reference copies**, and its **running code does not import the references**. A four-question intake gate (license check → value÷overhead ≥ 3× → framework-conflict check → paid-service-drift check) plus a six-step pattern ending in a real test and human review governs each intake. Documented consumption targets include a context-discipline family, a read-before-edit safety invariant, symbol-aware edits (Python stdlib AST), a post-edit failure classifier + syntax gate (ACI pattern from **SWE-agent, MIT**), trajectory evaluation (**agentevals, MIT**), permission-gating/phase-locking, and exploratory-QA/email patterns (from OpenClaw + Hermes, **pattern-only, no vendor code**). (consumption.md §6) — **VERIFIED structurally; PARTIAL for the paid-provider adapter (mechanism present, live call not run).**

**The honest correction, carried from the source.** "One-way" is the right *spirit* but **imprecise**. The precise claim is **"consume freely; publish a verifiable shell + interfaces; never publish the method."** A separate audited release plan publishes the shell, interfaces, memory format, and safety-gate model **while withholding** the orchestration intelligence, live block-hook implementations, and private prompts. So the posture is **asymmetric, not literally zero-outbound.** (_DIGEST.md §7) — **VERIFIED.**

**Pre-publish housekeeping (named, not buried).** "No vendor code" is verified *structurally*, not by a token-level clean-room diff; one source is fair-use / source-available (not classic-OSI) and warrants a lawyer's eye before redistributing its reference copy; a public NOTICE/attributions file is owed; per-item smoke-tests exist but no single aggregate regression run of the consumed layer. These are housekeeping items, not integrity gaps. (_DIGEST.md §7) — **PARTIAL / UNVERIFIED as noted.**

**Net.** The consume-vs-harness distinction is a **real strategic differentiator** and the SUR's posture is structurally evidenced — but it is a *strategy* claim, not a *quality* claim. It does not, by itself, make the SUR better; it makes the SUR's value-flow direction (inward, sealed) the opposite of the incumbents' (outward, open). Whether that is an advantage depends entirely on whether the method it withholds proves to be worth withholding.

---

## 4. What GPT said

The honest answer is the most important sentence in this section: **there is no on-record GPT (or external-AI) critique of the SUR or its audit approach.** (gpt-competitors.md Part 1) — **VERIFIED.**

- **No stored GPT/external-AI critique of the SUR exists on disk.** The internal audit pack is internally authored and internally adversarially re-read; it does not cite an external-AI reviewer. (gpt-competitors.md §1.1) — **VERIFIED.**
- **GPT/OpenAI appears only as a *routing target*, never a commentator** — i.e., the OpenAI-compatible `/chat/completions` request shape and an optional terminal backend. These are integration references, not opinions. (gpt-competitors.md §1.1) — **VERIFIED.**
- **The SUR's external-model connector is an unproven shell.** Its stored metadata self-labels as a mock-driven shell with real-provider integration deferred; the only logged calls are an authentication failure and a rate-limit failure, with **$0.00 recorded and zero tokens exchanged**. No real GPT inference round-trip is on record. Any "cross-model council" framing was, at the dates examined, **wired-but-not-executed design**, not evidence of a GPT review. (gpt-competitors.md §1.1) — **VERIFIED.**
- **The only captured external-model review used a different model family** (not GPT): a less-correlated reviewer **broke a claim the first reviewer had blessed**, and the SUR persona **conceded and corrected** rather than doubling down. That concede-and-fix under adversarial pressure is the **most load-bearing external-review datapoint on file** — and it is behavioural, not a benchmark. (gpt-competitors.md §1.1, Part 1 bottom-line) — **PARTIAL.**

**Auditor's bottom line.** Do **not** imply a GPT endorsement exists. The SUR does not hide behind a borrowed external seal of approval, and the materials do not pretend there is one — which is itself an integrity-positive signal. If GPT commentary was ever offered in an un-exported chat, it is **not recoverable** and is left explicitly **UNVERIFIED**. (gpt-competitors.md §1.2)

---

## 5. What researchers say

The independent literature grounds the comparison in science rather than vendor marketing. Five findings bear directly on where the SUR honestly stands.

- **The paradigm is borrowed, not invented.** The SUR implements Karpathy's **LLM-as-OS / "Software 3.0"** pattern (model as swappable compute core, context window as working memory, tools as resources, human gates) — a *named, public* paradigm. Defensibility must come from **execution and discipline**, not from claiming the paradigm. (researchers.md §1) — **VERIFIED.**
- **Multi-agent: real upside, real cost, real failure mode.** Anthropic's orchestrator-worker research system **outperformed single-agent by 90.2%** on its internal eval — at **~15× the tokens**, with **token usage explaining ~80% of performance variance.** (researchers.md §3) — **VERIFIED.** The steel-man against it (Cognition, *"Don't Build Multi-Agents"*): dispersed decision-making across agents that **don't share full context** produces compounding, conflicting errors; default to single-threaded, use sub-agents only for **scoped, read-only** work. (researchers.md §4) — **VERIFIED.** *The implication for the comparison:* the SUR (and Hermes, which seals "by omission") sit in the defensible zone **only insofar as they share full traces and synthesize rather than blind-concatenate** — an implementation property an auditor must examine, not assume. Pair every speed claim with the **15× token cost.**
- **Context discipline + external memory are independently validated as correct.** Anthropic: context editing alone = **+29%**, with a memory tool = **+39%**, and in a 100-turn eval context editing **cut tokens 84%**. Degradation is **universal across all major models**; bigger windows shift but do not eliminate it. The SUR's context-discipline and file-based external memory are **textbook-correct.** (researchers.md §5) — **VERIFIED.**
- **Long-horizon reliability is a measured, compounding problem.** METR's 50%-task horizon doubles ~7 months, but **per-step error rate *rises* as a task progresses and compounds**, and reliability is domain-stratified (SWE 0.90→0.44 over duration; hard benchmarks <20% pass). This is the **empirical backbone for the gate + per-step-verification argument** — and it equally **discounts any SUR claim of reliable fully-autonomous long-horizon execution.** (researchers.md §6) — **VERIFIED** (a later ~12-hour-horizon figure is **PARTIAL**).
- **The safety framing the science supports.** AI-2027 (Kokotajlo et al.) is the canonical public statement of autonomous-agent alignment risk. The strongest *honest* framing of the SUR's posture is **not** "we are safer than frontier labs" (UNVERIFIED, unprovable) but **"the architecture treats autonomy-without-a-gate as the named risk and engineers against it."** (researchers.md §2) — **VERIFIED** (the AI-2027 timeline has since been revised toward the early 2030s — **PARTIAL**).
- **Inference economics favor the approach but are a moving target.** Prompt caching cuts cost up to **~90%** / latency up to **~85%** on long stable prefixes; batching 32 requests ≈ **85%** cheaper per token. But Epoch AI: inference prices fall **9×–900×/yr, median ~50×/yr** — so the cheap-vs-frontier **routing advantage is a depreciating asset**, and the net cost story is **caching/batching savings *minus* the ~15× fan-out spend.** (researchers.md §7) — **VERIFIED.**

---

## 6. Synthesis — where the comparison lands

1. **On commodity layers, everyone converges.** The harness and the open `SKILL.md` format are shared, cross-vendor, and copyable. No project in this matrix — including the SUR — has a defensibility *there*. (openclaw.md §4) — **VERIFIED.**
2. **The SUR's only evidence-backed edge is structural.** A mechanical, fail-closed, human-in-the-loop gate layer; least-privilege execution; append-only audit; a sha256-verified retention guard; and a self-down-labelling claim register — against a category whose reach leader has shipped a **documented "shadow superuser" failure** whose *own academic remedy is a staged human-gate.* That symmetry is the single strongest comparative argument. (openclaw.md §5, §8) — **VERIFIED structurally.**
3. **The consume-vs-harness posture is a real strategic differentiator, not a quality claim.** It is structurally evidenced and asymmetric (consume freely; publish a shell; withhold the method) — but it makes the SUR *different in direction*, not *better by default.* (_DIGEST.md §7) — **VERIFIED.**
4. **The SUR is behind on exactly what the asymmetry predicts.** Reach (incumbents at 175K–355K stars), funding, team, a shipped paid go-to-market (ECC's $19/seat), public CI hygiene (ECC's ~1,000-test gate), and an own-model line (Nous). **The gap is distribution and third-party trust-proof, not engineering.** Competitor maturity is a roadmap, not a deficit. (ecc.md §10; gpt-competitors.md §2.4) — **VERIFIED.**
5. **No external endorsement, and none claimed.** There is no on-record GPT review; the strongest external-review datapoint is behavioural (concede-and-correct under scrutiny). The science supports the SUR's *architectural choices* (context discipline, external memory, gates against a measured failure law) but supports **no** claim of beating frontier systems, full autonomy, or superiority — and none is made. (gpt-competitors.md Part 1; researchers.md §8) — **VERIFIED.**

**The one-line verdict.** Against ECC, OpenClaw, Hermes, and Nous, the system under review is **not the most-adopted, the best-funded, or the model-producing** project in the category — and it does not claim to be. It is the one whose **default posture is the safety remedy the rest of the category has had to bolt on after the fact**, built by one person with AI assistance, defensible on **method and discipline** rather than reach, and honest enough to grade its own claims down. That is a structural edge to defend and prove in distribution — not a finished product to oversell.

---

### Sources

- `_research/_DIGEST.md` — sealed synthesis (spine, capabilities, numbers, competitor points, science, consumption posture, honest limits)
- `_research/ecc.md` — ECC live API metrics, bundle counts, bus factor, GTM, honest gaps
- `_research/openclaw.md` — OpenClaw scale, the open `SKILL.md` standard, the security incident record, comparative takeaways
- `_research/gpt-competitors.md` — "What GPT said" (Part 1), the competitor landscape incl. Hermes/Nous/ECC (Part 2)
- `_research/researchers.md` — Karpathy LLM-OS, AI-2027, multi-agent for/against, context engineering, long-horizon reliability, inference economics
- `_research/capabilities.md` — the SUR's verifiable capabilities from the published Apache-2.0 repo
