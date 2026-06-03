# Capabilities — The Capability Catalog of a Gate-First, BYOM Agentic Operating Layer

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## Purpose and scope of this document

This is the **capability catalog** for the system under review (SUR). Where the previous document described the SUR's architecture and the consumption audit described what it took from open source, this document answers a single question for each capability: **what does it do, how is it built, and why does it matter** — with every non-trivial claim labelled **VERIFIED**, **PARTIAL**, or **UNVERIFIED** so a reader can separate what was read in the published source from what is asserted in the wider platform documentation.

The evidence base is the SUR's **already-published, open-source repository** (Apache-2.0; `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `config.example.json`, the server module docstrings and route table, and the seed data directory) plus the public architecture overview. (capabilities.md; _DIGEST.md §2)

A terminology note carried throughout, because it is load-bearing. The SUR's relationship to the open-source ecosystem is **consumption**: it consumes patterns one-way into its own owned framework and re-implements them in its own stack. It does not ship a third-party harness and it is not itself a harness. Where the word "harness" appears below it describes *other, generic* tools for contrast — the category norm is to ship a harness; the SUR consumes patterns and rebuilds them as its own. (consumption.md §1–§4)

---

## How to read this catalog

Each of the ten capabilities below is described in three fixed subheads:

- **What it does** — the function, in plain operational terms.
- **How it is built** — the implementation at a high level, with the backing module(s) and routes named where the published code shows them.
- **Why it matters** — the engineering and trust significance, scoped honestly.

Two honesty rails span the whole catalog and are restated wherever they bite:

1. **Counts and surfaces are not the same as running engines.** Four capabilities the *wider* platform describes — a distinct context-discipline sandbox-execute primitive, a general Model Context Protocol (MCP) tool layer, a concurrent multi-agent *execution* engine, and a failure-signature regression memory — are **not present in the published repository**. They are catalogued here as roadmap / integration claims, never as shipped features. (capabilities.md "Auditor summary"; _DIGEST.md §2 honesty rail, §8)
2. **The defensible characterisation of the shipped artifact is a *verifiable, gate-first BYOM agent-OS shell*** — and on that scope it delivers what it claims. (_DIGEST.md §2, §9)

---

## Catalog at a glance

| # | Capability | What it is, in one line | Public-code status |
|---|---|---|---|
| 1 | BYOM model router | Routes chat to any operator-chosen model via the OpenAI-compatible request shape | **VERIFIED** |
| 2 | Context-discipline sandbox | Treats the context window as managed RAM; measures pressure, verifies survival pins, checkpoints | **VERIFIED** (policy); distinct sandbox-execute primitive **UNVERIFIED in repo** |
| 3 | Tool integration | Allow-listed action runner — named, vetted actions only, never a raw shell | **VERIFIED**; general MCP layer **UNVERIFIED in repo** |
| 4 | Parallel agent orchestration | A controllable workforce surface — grid, org chart, channels, briefs, autonomy dials | surface **VERIFIED**; concurrent execution engine **not in repo** |
| 5 | Human-in-the-loop gate layer | Autonomy dial L0–L5 × risk score → act / report / queue; high-risk always queues | **VERIFIED** |
| 6 | Mechanical safety hooks | Safety enforced by construction (allow-list + hard gate + revert loop) | **VERIFIED** |
| 7 | File-based memory | All state in plain inspectable files; curated, non-glob memory surface | **VERIFIED** |
| 8 | Audit surface + token meter | Append-only audit lines; token tracker prices counts at configured rates | **VERIFIED**; cost = API-equivalent, not cash |
| 9 | Regression memory | Quality-gated retention loop — KEEP only if no metric degrades, else byte-exact revert | retention loop **VERIFIED**; failure-signature memory **UNVERIFIED in repo** |
| 10 | Local server + reliability | Stdlib-only, same-origin, every route degrades to clean "unavailable", fail-closed health | **VERIFIED** |

*(Source: capabilities.md "Auditor summary"; _DIGEST.md §2.)*

---

## 1. BYOM model router

### What it does

Routes the operator's chat conversation to *any* model the operator chooses, by speaking the OpenAI-compatible `/chat/completions` request shape that nearly every provider exposes. The operator points the SUR at a hosted provider (OpenAI, OpenRouter, Together, Fireworks) or a fully local server (Ollama, LM Studio, vLLM) by editing one local config file. The intelligence is brought by the operator — *bring-your-own-model* — and the SUR supplies only the operating surface around it. (**VERIFIED** — `chat_byom.py` docstring, `README.md` wiring table, `config.example.json`.) (capabilities.md §1)

### How it is built

A single ~250-line standard-library module (`server/chat_byom.py`) reads a gitignored `config.json` (`provider` / `api_key` / `model` / `base_url`), builds the request from the visible channel history plus **one short neutral system line**, and calls the endpoint via `urllib`. There is no hidden prompt beyond that one disclosed system line — the `SYSTEM_LINE` constant is the entire system prompt and is visible in source — and there is no vendor lock-in, because swapping models is a config edit and nothing else. Missing or malformed config degrades to an honest "configure your model" message (`ok=False`) and never crashes or fabricates a reply. The model key is transmitted only to the chosen provider. (**VERIFIED** — `chat_byom.py` head, `load_config()`, `is_configured()`; the single-endpoint, single-provider transmission claim is **PARTIAL** — a design claim consistent with the single `urllib` call but not exhaustively traced.) (capabilities.md §1)

A caveat carried from the wider research: the SUR's *external-model connector for inter-agent dispatch* is a **mock-driven shell with no successful real call logged** ($0.00, zero tokens, only auth/rate-limit failures in the record). The chat-side BYOM router above is verified against a standard-shape stand-in; the broader provider connector is not. (**PARTIAL** — gpt-competitors.md Part 1; _DIGEST.md §4.4.)

### Why it matters

Decoupling the shell from the model is the SUR's central commercial and trust stance: the operator's data and credentials stay where they put them, cost and provider are operator choices, and a fully local model is a first-class path rather than a fallback. The strategy is validated by the broader landscape — multiple incumbents (OpenClaw, Hermes) are likewise model-agnostic across Claude / GPT / Gemini / DeepSeek and local backends, and one research lab in the field ships open-weight models and pursues decentralized training, confirming that a run-your-own-model posture is a live, defensible direction rather than a niche. (**VERIFIED** for the incumbent landscape; **PARTIAL** for the open-weight lab's own scale/quality claims — gpt-competitors.md §2.1–§2.3; _DIGEST.md §4.2.) For an auditor, the decisive property is verifiability: the entire BYOM surface is one small, readable file. (capabilities.md §1)

---

## 2. Context-discipline sandbox (context-pressure policy)

### What it does

Treats the model's context window as a managed resource — *"the context window IS the agent's RAM; a compaction is a swap to disk"* — and makes the eviction/survival policy first-class rather than implicit. It (a) **measures** context pressure from real signals, (b) **verifies a swap-file contract** (that everything which must survive a compaction is already on disk — the "survival pins"), and (c) **checkpoints** by repairing what it mechanically can and honestly reporting what only a human can fix. (**VERIFIED** — `context_policy.py` docstring; routes `/api/context`, `/api/context-checkpoint`.) (capabilities.md §2)

### How it is built

`server/context_policy.py` (~31 KB, the largest server module) reads real signals — live transcript size and age, active-work staleness, and work-log entries newer than the last checkpoint — to compute a pressure verdict. `survival_check()` reports *real* missing pins, where a missing pin is the tool working, not failing; `checkpoint()` refreshes the active-work marker and appends an audit line. The broader context-discipline principle the public docs describe — *findings into context, never raw data* — is made explicit here as a written policy. (**VERIFIED** — module docstring plus the `pressure()` / `survival_check()` / `checkpoint()` / `policy()` function list.) (capabilities.md §2)

The honesty rail bites here: a *separate sandboxed-execute primitive* that runs analysis scripts off-context and returns only their printed findings is a documented design discipline of the wider platform but is **not present as a distinct module in the public repo**. What ships is the context-pressure *policy* as a first-class artifact; the sandbox-execute primitive is a roadmap claim, and the action surface that exists in the published repo is the allow-listed action runner described in §3. (**PARTIAL** for the policy-as-artifact; **UNVERIFIED in repo** for the distinct sandbox-execute primitive — capabilities.md §2; scalability.md §3.2.)

### Why it matters

Long-running agents fail quietly when a compaction drops in-flight work or an open high-risk item. The independent literature backs the design: context-editing alone gives roughly a +29% lift, rising to +39% with a memory tool, and in a 100-turn evaluation context editing cut token use ~84%; degradation as input grows is universal across all major models, and bigger windows shift but do not eliminate it. Making the survival contract explicit and checkable converts a silent failure mode into a visible, fail-closed check, and keeps each worker's working context small — which both cuts per-call input cost and stays left of the degradation curve. (**VERIFIED** — researchers.md §5; _DIGEST.md §5; scalability.md §3.2.) (capabilities.md §2)

---

## 3. Tool integration (the allow-listed action runner)

### What it does

Lets an agent invoke tools — but only named, vetted ones. The published repo ships an **allow-listed action runner**: `/api/run?action=...` can invoke only one of a few named, harmless demo actions (echo, list agents, disk-free, Python version). It is explicitly *not a raw shell*; operators add their own safe actions to a single `ACTIONS` dictionary. (**VERIFIED** — `servari_server.py` `ACTIONS` dict + `/api/run` route; `docs/ARCHITECTURE.md`; `AGENTS.md` "do not introduce a raw shell".) (capabilities.md §3)

### How it is built

`ACTIONS` is a Python dict mapping a string name to a function; the runner looks up the name and returns `{allowed: [...]}` for an unknown name **rather than executing anything**. The closed `fn = ACTIONS.get(name)` lookup is the SUR's deliberate substitute for arbitrary command execution: the tool surface is a closed, reviewable set, not an open shell. (**VERIFIED** — `ACTIONS = {...}` and the unknown-name path at `servari_server.py`.) (capabilities.md §3)

**On MCP.** The published repository does **not** ship an MCP server or MCP client; the model wiring is OpenAI-compatible chat (§1) and the tool surface is the allow-listed runner above. A general MCP tool-integration capability is therefore **UNVERIFIED in the published sources** — it is not present in the open repo as audited, and an auditor should treat it as a roadmap/integration claim, not a shipped feature. (**UNVERIFIED in repo** — capabilities.md §3; scalability.md §3.2.)

### Why it matters

An allow-listed runner is a strong, simple safety posture: the blast radius of an over-eager agent is bounded by a hand-curated list a reviewer can read in one file, so adding concurrent workers does not widen the attack/error surface linearly the way an open shell would. This is the direct structural answer to the category's cautionary tale — the most prominent open-source incumbent's documented failures (a one-click remote-code-execution CVE, command-injection CVEs, a "shadow superuser" demonstration, and a companion-service breach exposing ~1.5M auth tokens) trace to permissive defaults and a disable-able sandbox over a wide untrusted-input surface. A closed action set is the opposite stance. (**VERIFIED** for the documented incumbent events; **PARTIAL** on exact single-paper percentages — openclaw.md; _DIGEST.md §4.1.) (capabilities.md §3)

---

## 4. Parallel agent orchestration (the workforce surface)

### What it does

Presents and coordinates a *workforce* of agents rather than a single chat: a multi-pane grid of agent channels, an org chart, a process-table-style overlay, and a launch ladder. Each agent's autonomy is a dial the human controls (see §5). (**VERIFIED** — `README.md`, `docs/ARCHITECTURE.md` UI section; routes `/api/agents`, `/api/agent-channel`, `/api/org`, `/api/grid`, `/api/launch`, `/api/agent-brief`, `/api/agent-say`.) (capabilities.md §4)

### How it is built

The server exposes per-agent channels (append-only turn logs), an org structure, and a grid view, each read fail-closed from the seed data directory (`agents.json`, per-agent channel files, a service/channel index). The React layer renders these as the agent grid, org chart, and process-table overlay. (**VERIFIED** — `servari_server.py` route handlers; `docs/ARCHITECTURE.md` components list.) (capabilities.md §4)

**Scoping for an auditor.** The public repo provides the *orchestration surface and data shapes* (channels, org, grid, briefs, per-agent autonomy), populated from synthetic seed data. The actual parallel *execution engine* that fans work out across many concurrent model-backed workers is part of the wider platform and is **not included as a running engine in the open repo** — what ships is the controllable workforce *shell* over BYOM, ready to be pointed at real backends. (**PARTIAL / UNVERIFIED**: surface **VERIFIED**; concurrent execution engine **not in repo** — capabilities.md §4; scalability.md §2.3.)

### Why it matters, and what the literature bounds

The differentiator the docs claim is *the shell plus the gates*: a polished, inspectable workspace where many agents are coordinated and every agent's autonomy is a human-controlled dial — value in the control model (§5, §6), not in a hidden black box. The independent science both supports and bounds the multi-agent pattern, and the audit reports both sides:

- **The case for.** A production orchestrator-worker research system outperformed a single agent by **90.2%** on its internal evaluation — at **~15× the token cost**, with token usage explaining ~80% of performance variance. The upside is real and measured *elsewhere*; the SUR adopts the same pattern, so its expected upside is "plausibly large on breadth-heavy tasks, at a ~15× token premium," not a number the SUR has independently benchmarked in the public sources. (**VERIFIED** for the cited system; **UNVERIFIED for the SUR specifically** — researchers.md §3; scalability.md §2.4.)
- **The case against (steel-man).** A widely-cited counter-position warns that dispersed decision-making across agents that do not share full context produces compounding, conflicting errors, and recommends defaulting to single-threaded work with scoped read-only sub-agents. The SUR is defensible **only insofar as** its workers run genuinely independent sub-tasks *and* the lead receives full traces and *synthesizes* rather than blind-concatenates. The per-agent append-only channels and a synthesizing lead are consistent with the safe pattern, but whether the SUR genuinely shares full traces is an implementation property the published shell does not by itself prove. (**VERIFIED** for the counter-position; **PARTIAL** for the SUR's adherence — researchers.md §4; scalability.md §2.3.)

Concurrency also **saturates**, for three independent reasons that converge on a working cap of roughly **8–10 effective parallel agents**: the Amdahl synthesis tax (at a 0.90 parallel fraction, 10 workers buy ~5.3× and 25 workers ~6.9×), the shared-context failure mode above, and universal context degradation as the lead loads many worker reports to combine them. Past that band, extra agents add little wall-clock but full token cost. (**VERIFIED** — scalability.md §2.2–§2.3; _DIGEST.md §6.) (capabilities.md §4)

---

## 5. Human-in-the-loop gate layer (autonomy dial + fast-verify queue)

### What it does

This is the SUR's core stance: **autonomy is a dial, and irreversible actions always pass a human gate.** Each agent has an autonomy level from **L0 (suggest only)** to **L5 (full auto)**. The dial widens what an agent may do *silently* — but a high-risk action (deploy, real-send, spend, publish, merge, secret) *always* parks in a fast-verify queue for one-click human approval. The gates hold at every autonomy level. (**VERIFIED** — `autonomy.py` + `verify_queue.py` docstrings; persona file "the gates — your one hard rule"; `AGENTS.md` "do not weaken the gates".) (capabilities.md §5)

### How it is built

Two standard-library modules:

- **`autonomy.py`** composes the agent's level L0–L5 with a **4–20 risk score** (modelled as reversibility × blast-radius × data-loss × certainty) into one verdict — `act` / `report` / `queue`. The level→band mapping is monotonic (higher L = wider act-band), and the decisive property is that **even at L5 a high-risk score still queues**. (**VERIFIED** — `LEVELS` table and band constants; routes `/api/autonomy`, `/api/set-autonomy`.)
- **`verify_queue.py`** is the gate queue itself: gated actions are parked as an **append-only audit** (`gate-queue.jsonl`); the operator approves or rejects; nothing executes until approved; the pending entry and every decision are separate append lines and the audit is never rewritten. (**VERIFIED** — module docstring + `enqueue` / `list_pending` / `decide` / `history`; routes `/api/verify-queue`, `/api/verify-decision`.)

(capabilities.md §5)

### Why it matters

This is the product's explicit promise and its safety wedge: move fast on reversible/local work, never act silently on the actions that bite. Because the queue is append-only and the level→verdict logic is a small readable function, the safety property is **auditable rather than asserted**. The framing is independently grounded: the empirical backbone for a gate is that per-step error rate *rises* as a long-horizon task progresses and compounds — so retrying a deep trajectory is not the cure; checkpointing plus a gate is. And the strongest honest safety claim available is not "we are safer than frontier labs" (unprovable) but the narrower one the gate actually delivers: **the architecture treats autonomy-without-a-gate as the named risk and engineers against it.** Notably, the most prominent incumbent's *own* proposed remedy — a staged human-in-the-loop defense layer that raised measured sandbox-escape defense from a ~17% baseline into the 19%–92% range (one model class ~91.5%) — is precisely this differentiator. (**VERIFIED** for the long-horizon error backbone and the staged-defense direction; **PARTIAL** on exact single-paper percentages — researchers.md §6; openclaw.md; _DIGEST.md §4.1, §5.) (capabilities.md §5)

---

## 6. Mechanical safety hooks (enforcement by construction)

### What it does

Safety is enforced by the system's *structure*, not by convention or prompt instruction: the action runner is allow-listed rather than a raw shell (§3), high-risk operations are intercepted before they execute (§5), and the repository's own contributor rules forbid weakening either. (**VERIFIED** — `docs/ARCHITECTURE.md`; `AGENTS.md` "things to avoid": no raw shell, no weakening the gates, no hardcoded paths, no hardcoded secrets.) (capabilities.md §6)

### How it is built

The enforcement points are concrete and readable: the closed `ACTIONS` dict, the autonomy band that cannot auto-cross a hard gate, the append-only gate audit, and a quality-gating retention loop (§9) that byte-exactly reverts changes that degrade metrics. The wider platform's internal health pass reported **8/8 mechanical safety hooks present, parsing, and running** — and, with auditor candor, found and fixed one *firing-but-blind* hook in the same pass, an honest self-catch rather than a clean-only result. (**VERIFIED** across `servari_server.py`, `autonomy.py`, `verify_queue.py`, `retention.py`; the 8/8 tally is **PARTIAL** — an internal run, mechanism inspectable — capabilities.md §6; metrics.md §4; _DIGEST.md §3.3.)

### Why it matters

"Gates over trust" is only credible if the gates are mechanical. The SUR's safety claims are backed by code paths an auditor can read, not by prompt instructions alone — with the honest note that the persona-level rules (§5) are a *soft* layer that complements, not replaces, the *hard* server-side enforcement. In a category whose loudest incumbent's failures are precisely soft-default failures (permissive permissions, disable-able sandbox), enforcement-by-construction is the structurally correct posture, and the contributor-rule prohibition on weakening it is what keeps the posture from eroding over time. (**VERIFIED** — capabilities.md §6; openclaw.md.)

---

## 7. File-based memory (persistent state in plain files)

### What it does

All state lives in plain files, so the system boots into a known state and resumes where it left off; memory survives a restart. A curated **memory surface** lets the UI show which memory files exist, with live-derived freshness, *without scanning the disk*. (**VERIFIED** — public overview; the seed data directory of JSON / JSONL / Markdown files; `memory_surface.py` docstring; route `/api/memory-surface`.) (capabilities.md §7)

### How it is built

State files under the seed data directory (or a home directory the operator points at) hold agent channels, autonomy levels, the gate-queue audit, the token-usage log, retention runs, context/active-work markers, and human-readable memory notes and decisions. `memory_surface.py` reads only the exact files a curator declares in a registry — it does **not** glob or walk directories — and surfaces a missing declared file honestly as `updated: "missing"` rather than fabricating. Home resolution is drive-independent (home env → repo root → cwd), with no hardcoded absolute paths. (**VERIFIED** — the seed listing: `autonomy-levels.json`, `gate-queue.jsonl`, `token-history.jsonl`, `retention/`, `context/`, `active-work.json`, `memory/decisions.md`, `memory/notes.md`; `memory_surface.py` docstring; each module's home helper.) (capabilities.md §7)

### Why it matters

"Files are the memory" means there is no database to stand up, the full state is human-inspectable and diffable, and an auditor can read exactly what the system remembers. The curated, non-glob memory surface is a notable least-privilege choice: the UI shows only what a human declared, never an arbitrary disk scan — the same restraint that distinguishes the gate layer. The independent literature reinforces the value: pairing a memory tool with context discipline produced a measured +39% lift versus context editing alone, so externalized file memory is not just operationally tidy but performance-relevant. And "files-are-memory" removes a whole class of failure: state survives a process restart with no database to fail (a point that returns in the reliability analysis, §10). (**VERIFIED** — capabilities.md §7; researchers.md §5; scalability.md §4.6.)

---

## 8. Audit surface + token meter (structured, append-only, fail-closed)

### What it does

Activity is recorded in structured logs a reviewer can read — which is precisely what makes an external audit like this one possible. A **proof-of-work token tracker** records usage and prices it at the operator's published rates, so running cost is visible. (**VERIFIED** — public overview; the append-only `gate-queue.jsonl` and `retention/audit.jsonl`; `tokens.py`; routes `/api/tokens`, `/api/tokens-sessions`, `/api/tokens-report`.) (capabilities.md §8)

### How it is built

The gate queue (§5) and the retention loop (§9) both write **append-only** audit lines that are never rewritten — one JSON object per decision or event. `tokens.py` reads a JSONL usage log (`token-history.jsonl`), prices it at configurable per-million rates, and produces per-session / per-day / all-time reports; it is **read-only** against the source and writes only reports. (**VERIFIED** — `verify_queue.py` / `retention.py` invariants; `tokens.py` docstring.) (capabilities.md §8)

### Cost-figure honesty (auditor note)

The token tracker's docstring is explicit that **the counts are ground truth (logged per message) while the cost is the API-equivalent at the configured rates** — i.e. **cost-to-serve, not necessarily cash spent**, since a subscription-billed operator pays differently. Any figure derived from this tracker must be read as **API-equivalent cost-to-serve**, with the assumed per-million rates stated. For grounding scale: the wider platform's own usage log records **~10.53 billion total tokens across 19,333 messages over 19 calendar days**, of which **~10.07 billion (≈93%) are cache-read** tokens priced at the cheapest tier — which is *why* the blended cost is low, at an **API-equivalent ~$26,920 cost-to-serve** (rate-dependent; the older, widely-quoted "~$10K" figure is a stale 2026-05-24 snapshot and should not be cited as current). (**VERIFIED** for the raw counts and the cache-read share; **PARTIAL** for the dollar total — it is rate-dependent cost-to-serve, not cash — tokens.py docstring; capabilities.md §8; metrics.md §1; _DIGEST.md §3.1.)

### Why it matters

Append-only audits plus a transparent cost tracker turn opaque agent activity into a reviewable record — the foundation for trust, compliance, and this very audit. The self-disclosed labelling discipline is itself a positive trust signal: the platform's own public claim register tracks **12 product claims as 4 VERIFIED / 8 PARTIAL / 0 UNVERIFIED**, with the four verified claims being the ones whose evidence was *actually run* on the collection date — a system that down-labels its own unproven claims is a system whose audit surface is doing its job. (**VERIFIED** read from the register — metrics.md §4; _DIGEST.md §3.4.)

---

## 9. Regression memory (the quality-gated retention loop)

### What it does

Lets improvement loops run unattended *without quality silently eroding*: a change to the system is **KEPT only if a metric suite does not degrade**, otherwise it is **auto-reverted byte-exact** to the baseline. (**VERIFIED** — `retention.py` docstring; routes `/api/retention`, `/api/retention-decide`.) (capabilities.md §9)

### How it is built

`retention.py` (~32 KB) runs a three-step flow. `baseline(targets)` snapshots the target files (byte copies) and records baseline metric scores; the loop (a job, a scheduler, or a human) edits the targets; `decide(run_id)` re-runs the *same* metric suite and compares — **KEEP** if no gating metric degraded (ties allowed, improvement welcome), **REVERT** (restore snapshot bytes exactly, sha256-verified) if any gating metric degraded. It is **fail-closed**: if any metric fails to *run* at decide-time, it reverts; a run can be decided only once; every decision is appended to an audit. Metrics are defined in a registry (`retention_metrics.json`) with `exit_code` or `regex` parse modes. (**VERIFIED** — `retention.py` docstring invariants.) (capabilities.md §9)

### Relation to a failure-pattern regression memory

This is the quality-regression guard the public repo ships. The wider platform also describes a *separate* **failure-pattern regression memory** — recording known failure signatures so they are recognised and fixed instantly on recurrence — but that named subsystem is **not present as a distinct module in the public repo**. What is shipped and verifiable is the metric-gated KEEP/REVERT retention loop above. (**PARTIAL**: the retention loop is **VERIFIED**; a broader failure-signature memory is **UNVERIFIED in public sources** — capabilities.md §9; _DIGEST.md §8.)

### Why it matters

Unsupervised self-improvement is only safe if regressions cannot land silently. A byte-exact, fail-closed revert gate is the safety rail that makes "let it run on its own" a *defensible* claim rather than a hopeful one — the same gate-first philosophy as §5, applied to the system improving itself. It is also the right rail for the long-horizon reality the literature documents: because per-step error rates rise and compound, an unattended loop without a regression gate is exactly the place silent degradation accumulates. The retention loop ties off that risk mechanically. (**VERIFIED** — capabilities.md §9; researchers.md §6.)

---

## 10. Local server + reliability posture

### What it does

A single tiny local server is the spine: it serves the SPA and the JSON API on `127.0.0.1:8911`, same-origin (no CORS). Every route degrades gracefully — a missing module or data file returns a clean "unavailable" payload at HTTP 200 instead of crashing — and the health surface is fail-closed. (**VERIFIED** — `servari_server.py`; `health.py`; `docs/ARCHITECTURE.md`; `AGENTS.md`.) (capabilities.md §10)

### How it is built

`servari_server.py` (~43 KB) is a **pure standard-library** HTTP server (no `pip install` needed to run), with a path-traversal-guarded static handler for the built front end and a per-route, per-module defensive load: each backing module loads inside a `try`/`except`, so one failing import never takes the server down. `health.py` is a fast, file-read-only, fail-closed surface: any unreadable sub-check degrades to UNKNOWN and the whole call never crashes. Configuration is environment-driven (host / port / home / Python / no-voice). Optional local voice (speech-to-text plus neural text-to-speech skeletons) loads lazily in a background thread so the port binds first; the shell runs fine without it. (**VERIFIED** — `servari_server.py`; `health.py` docstring; route `/api/health`; `voice.py` / `voice_neural.py`.) (capabilities.md §10)

### Why it matters, and what the reliability math shows

A stdlib-only, fail-closed local server is exceptionally easy to audit, run, and trust: no runtime supply chain to vet, no mandatory cloud backend, and "runnable by a stranger" is enforced (a fresh clone renders every panel from seed data). The audit's quantitative finding is that **the own-server is not the scaling bottleneck** — upstream model latency and provider rate limits are; the design's scaling value is **isolation, reliability, and bounded blast radius**, not raw QPS. Each named reliability practice carries concrete leverage, all grounded in standard formulas with stated inputs:

| Practice | Effect | Status |
|---|---|---|
| Fast health surface + auto-restart (MTTR 30 min → 30 s) | ~98% → ~99.97% availability at 24 h MTBF — ~2 nines from MTTR alone | **VERIFIED** (formula; inputs stated) |
| Retry + exponential backoff | turns p=0.9 into 99.9% over 3 attempts — **transient errors only** (long-horizon errors compound; need checkpoint + gate) | **VERIFIED** (formula); caveat **VERIFIED** |
| Circuit breaker | caps wasted spend during an upstream outage — ~15× reduction in wasted work | **VERIFIED** (arithmetic; thresholds stated) |
| Caching as load-shedding (h=0.8) | makes 1/5 the upstream calls — 5× rate-limit headroom | **VERIFIED** (arithmetic; h from cited 80–95% band) |
| Multi-provider BYOM | removes the model single-point-of-failure — **only if independently configured** | **VERIFIED** (math); independence is **PARTIAL** (operator config) |

*(Source: scalability.md §4; _DIGEST.md §6.)*

A noteworthy convergence the audit highlights: the **rate-limit math and the concurrency math independently land on ~8–15 workers** as the useful band — token-bucket admission (e.g. 60 RPM ÷ 4 calls/worker/min ⇒ ~15 workers) sits right beside the §4 Amdahl/synthesis cap. The reliability posture is the operational expression of the SUR's promise to whatever depends on it: never crash a request, degrade to "unavailable", fail closed. (**VERIFIED** formulas; inputs stated — scalability.md §4.5, §2.3.) (capabilities.md §10)

---

## Auditor summary

The capability catalog separates cleanly into **what is shipped and verifiable in the open repository** and **what the wider platform describes as roadmap**:

| # | Capability | Public-code status |
|---|---|---|
| 1 | BYOM model router | **VERIFIED** (one stdlib file + config); inter-agent provider connector **PARTIAL** (mock-driven, no live call logged) |
| 2 | Context-discipline sandbox | Context-pressure policy **VERIFIED**; distinct sandbox-execute primitive **UNVERIFIED in repo** |
| 3 | Tool integration | Allow-listed action runner **VERIFIED**; general MCP layer **UNVERIFIED in repo** |
| 4 | Parallel agent orchestration | Surface + data shapes **VERIFIED**; concurrent execution engine **not in repo** |
| 5 | Human-in-the-loop gate layer | **VERIFIED** (autonomy dial + append-only queue; high-risk queues even at L5) |
| 6 | Mechanical safety hooks | **VERIFIED** (allow-list + hard gate + revert loop); 8/8 internal tally **PARTIAL** |
| 7 | File-based memory | **VERIFIED** (plain files + curated, non-glob memory surface) |
| 8 | Audit surface + token meter | **VERIFIED**; cost = API-equivalent cost-to-serve, **not cash** |
| 9 | Regression memory | Retention loop **VERIFIED**; failure-signature memory **UNVERIFIED in repo** |
| 10 | Local server + reliability | **VERIFIED** (stdlib, same-origin, fail-closed); reliability math **VERIFIED** with stated inputs |

**The honest characterisation.** Six of the ten capabilities are **VERIFIED in full** against the published code (BYOM router, gate layer, mechanical hooks, file memory, audit surface, local server). The other four ship a **verifiable surface or policy** while their deeper engine — a distinct sandbox-execute primitive, a general MCP layer, a concurrent execution engine, a failure-signature memory — is **roadmap, not shipped**, and is catalogued as such. The published artifact is best described as a **verifiable, gate-first, bring-your-own-model agentic operating-system shell**, and on that scope it delivers what it claims. (capabilities.md "Auditor summary"; _DIGEST.md §2, §9)

**Asymmetry, stated plainly.** This system is the work of **one researcher with AI assistance over ~19 recorded days**, not a funded engineering team. Its strengths — a small, readable, stdlib-only, fail-closed surface with mechanical gates and append-only audits — are real and directly verifiable in the open repo. Its honest limits are equally on the record: several wider-platform capabilities are not in the published repository; the cost figures are API-equivalent cost-to-serve rather than cash; an inventory count is not the same as full external validation; and the differentiator is **structural, not architectural** — in a category where the harness and the open skill format are commodities and the loudest incumbents have documented security failures, the SUR's defensible edge is the gate layer, the auditable boundaries, the inspectable memory, the fail-closed retention guard, and the disciplined one-way consumption that rebuilds commodity patterns into an owned composition. Nothing here supports "beats frontier," "fully sovereign," or any superlative — and none is claimed. (_DIGEST.md §8, §9)
