# The System Under Review — Architecture of a Local-First, BYOM, Gated, Auditable Agentic Operating Layer

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## Purpose and scope of this document

This is the architectural description that the rest of the audit references: what the system under review (SUR) **is**, structurally, before any judgement about whether it is good, defensible, or finished. It describes the components, the data flow, the gate model, and the memory model in neutral engineering terms, and it labels every non-trivial claim **VERIFIED** / **PARTIAL** / **UNVERIFIED** so that a reader can separate what was read in the published source from what is asserted in the wider platform documentation.

The evidence base is the SUR's **already-published, open-source repository** (Apache-2.0; `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `config.example.json`, the server module docstrings and route table, and the seed data directory) plus the public architecture overview. Where the published code backs a claim, it is **VERIFIED**; where a claim appears only in wider-platform documentation and is not present in the published code, it is labelled **UNVERIFIED in repo** and catalogued as roadmap, not as a shipped feature. (capabilities.md; consumption.md; _DIGEST.md §2, §8)

A terminology note carried throughout: the SUR's relationship to the open-source ecosystem is described as **consumption** — it consumes patterns one-way into its own owned framework and re-implements them in its own stack. It does not ship a third-party harness and it is not itself a harness; where "harness" appears below it describes *other, generic* tools for contrast. The differentiator is the posture: generic tools ship a harness; the SUR consumes patterns and rebuilds them as its own. (consumption.md §1–§4)

---

## 1. What the system is, in one paragraph

The SUR is a **local-first AI operating-system shell**: a React front end over a small, dependency-free Python server that turns one or more operator-supplied language models into a controllable, gated agent workforce. The intelligence is brought by the operator — **bring-your-own-model (BYOM)** — and the SUR supplies the operating surface around it: a chat channel, an agent grid, an org chart, an approval queue, per-agent autonomy dials, and health / context / token panels. It runs on `127.0.0.1:8911`; the UI and the JSON API are served same-origin, so there is no CORS layer. (**VERIFIED** — `README.md`, `docs/ARCHITECTURE.md`, public overview.) (capabilities.md "What the SUR is")

The frame it implements is a **named, public paradigm** — the LLM-as-operating-system / "Software 3.0" idea articulated by Andrej Karpathy. The SUR does not claim to invent the paradigm; it implements one. Any defensibility therefore has to come from execution and discipline, not from architectural novelty — a point the audit returns to throughout. (**VERIFIED** — researchers.md; _DIGEST.md §5)

---

## 2. The three-layer shape

The published artifact has a clean three-layer separation. (**VERIFIED** — `docs/ARCHITECTURE.md`, `AGENTS.md`.) (capabilities.md "What the SUR is")

| Layer | What it is | Implementation | Status |
|---|---|---|---|
| **The face** | The operator-facing workspace | A Vite + React 18 + TypeScript single-page app | **VERIFIED** |
| **The spine** | The coordinator | A Python standard-library HTTP server that serves the SPA and a JSON API and coordinates the subsystems | **VERIFIED** |
| **The data** | Persistent state | Plain files (JSON / JSONL / Markdown) under a seed data directory | **VERIFIED** |

The defining property of the spine is that it is **pure standard library** — no `pip install` is required to run it. The server module is roughly 43 KB of stdlib Python with a path-traversal-guarded static handler for the built front end and a per-route, per-module defensive load: each backing subsystem is imported inside its own `try`/`except`, so one failing import never takes the server down. (**VERIFIED** — `servari_server.py`; `docs/ARCHITECTURE.md` reliability section.) (capabilities.md §10)

This shape matters for an auditor before any feature does: a stdlib-only, same-origin, file-backed server is exceptionally easy to read, run, and trust. There is no runtime supply chain to vet and no mandatory cloud backend, and "runnable by a stranger" is enforced — a fresh clone renders every panel from seed data. (**VERIFIED** — `docs/ARCHITECTURE.md`.)

---

## 3. Components and what each one owns

The spine is a set of small, single-responsibility stdlib modules, each fronted by one or more JSON routes. The table below is the component map as evidenced in the published repo. (**VERIFIED** unless noted.) (capabilities.md §1–§10)

| Component | Responsibility | Backing module(s) | Representative routes | Status |
|---|---|---|---|---|
| **BYOM model router** | Speak the OpenAI-compatible request shape to any operator-chosen provider or local server | `chat_byom.py` (~250 lines) | `/chat/completions` shape | **VERIFIED** |
| **Context-pressure policy** | Treat the context window as managed RAM; measure pressure, verify survival pins, checkpoint | `context_policy.py` (~31 KB) | `/api/context`, `/api/context-checkpoint` | **VERIFIED** (policy); distinct sandbox-execute primitive **UNVERIFIED in repo** |
| **Allow-listed action runner** | Invoke only named, vetted tools — never a raw shell | `servari_server.py` (`ACTIONS` dict) | `/api/run?action=...` | **VERIFIED**; general MCP layer **UNVERIFIED in repo** |
| **Workforce surface** | Present and coordinate many agents (grid, org chart, channels, briefs) | `servari_server.py` handlers | `/api/agents`, `/api/agent-channel`, `/api/org`, `/api/grid`, `/api/launch` | surface **VERIFIED**; concurrent execution engine **not in repo** |
| **Human-in-the-loop gate** | Compose autonomy level × risk score into act / report / queue; park high-risk actions | `autonomy.py`, `verify_queue.py` | `/api/autonomy`, `/api/set-autonomy`, `/api/verify-queue`, `/api/verify-decision` | **VERIFIED** |
| **File-based memory** | Persist all state as plain files; expose a curated, non-glob memory surface | `memory_surface.py` | `/api/memory-surface` | **VERIFIED** |
| **Audit surface + token meter** | Append-only audit lines; price logged token counts at configured rates | `tokens.py` | `/api/tokens`, `/api/tokens-sessions`, `/api/tokens-report` | **VERIFIED**; cost = API-equivalent, not cash |
| **Quality-gated retention loop** | KEEP a change only if no metric degrades, else byte-exact auto-revert | `retention.py` (~32 KB) | `/api/retention`, `/api/retention-decide` | **VERIFIED**; broader failure-signature memory **UNVERIFIED in repo** |
| **Health surface** | Fast, read-only, fail-closed health that never crashes | `health.py` | `/api/health` | **VERIFIED** |
| **Local voice (optional)** | Lazy-loaded speech-to-text / text-to-speech skeletons | `voice.py`, `voice_neural.py` | (background thread) | **VERIFIED** (optional; shell runs without it) |

A single honesty rail spans this table and is restated wherever it applies: four capabilities described by the **wider** platform — a distinct sandbox-execute primitive, a general MCP tool layer, a concurrent multi-agent *execution* engine, and a failure-signature regression memory — are **not present in the published repo**. They are catalogued as roadmap / integration claims, never as shipped. The published artifact is best characterised as a **verifiable, gate-first BYOM agent-OS shell**, and on that scope it delivers what it claims. (**UNVERIFIED in repo** — capabilities.md "Auditor summary"; _DIGEST.md §2 honesty rail, §8)

---

## 4. Data flow

The SUR's runtime is a small number of well-defined paths. Described generically, an operator interaction moves through the system as follows. (**VERIFIED** structurally from the route table + module docstrings; the concurrent fan-out path is the **UNVERIFIED** exception noted below.) (capabilities.md §1, §3, §4, §5, §8)

### 4.1 The conversational path (single agent)

1. The operator types into a channel in the React front end; the SPA posts to the same-origin JSON API.
2. The **BYOM router** reads a gitignored local config (`provider` / `api_key` / `model` / `base_url`), assembles the request from the **visible** channel history plus **one short, disclosed system line**, and calls the chosen endpoint over `urllib`. There is no hidden prompt beyond that one line, and the model key is transmitted only to the operator's chosen provider. (**VERIFIED** for the visible system line and single-endpoint call; the "key never goes anywhere else" property is a design claim consistent with the single `urllib` call but **PARTIAL** — not exhaustively traced.) (capabilities.md §1)
3. Missing or malformed config degrades to an honest "configure your model" message (`ok=False`) — it never crashes and never fabricates a reply. (**VERIFIED** — `load_config()` / `is_configured()`.)
4. The turn is appended to the agent's channel file and to the token-usage log; nothing is rewritten.

### 4.2 The action path (tool use)

1. An agent (or the operator) requests a named action via `/api/run?action=...`.
2. The **allow-listed action runner** looks the name up in a closed `ACTIONS` dictionary. A **known** name runs its small Python function; an **unknown** name returns `{allowed: [...]}` — the list of permitted actions — and executes nothing. This is the deliberate substitute for a raw shell. (**VERIFIED** — `ACTIONS = {...}`, `fn = ACTIONS.get(name)`.) (capabilities.md §3)

### 4.3 The gated path (high-risk action)

1. A proposed action carries an autonomy level (L0–L5) and a computed risk score (4–20).
2. The **gate** (`autonomy.py`) composes the two into one verdict — `act` / `report` / `queue`.
3. If the verdict is `queue`, the action is parked in the append-only `gate-queue.jsonl` and **does not execute**. The operator approves or rejects from the fast-verify queue; the decision is a separate append line. (**VERIFIED** — `verify_queue.py`.) The gate model is detailed in §5.

### 4.4 The workforce path (the scoping caveat)

The repo exposes the **orchestration surface and data shapes** — per-agent channels (append-only turn logs), an org structure, a grid view, and per-agent autonomy — each read fail-closed from the seed data directory (`agents.json`, per-agent channel files, a service/channel index). The React layer renders these as the agent grid, org chart, and process-table overlay. (**VERIFIED** — `servari_server.py` handlers; `docs/ARCHITECTURE.md` components.) (capabilities.md §4)

What the published repo does **not** include is the concurrent execution engine that fans real work out across many model-backed workers and merges their results. The shipped artifact is the controllable workforce *shell* over BYOM, populated from synthetic seed data and ready to be pointed at real backends — not a running fan-out-and-merge engine. (**PARTIAL / UNVERIFIED** — surface VERIFIED; concurrent engine not in public sources.) (capabilities.md §4; _DIGEST.md §8 limit 3)

### 4.5 Reliability properties along every path

Every route degrades gracefully: a missing module or data file returns a clean "unavailable" payload at **HTTP 200** rather than crashing, and the health surface is fail-closed — any unreadable sub-check degrades to `UNKNOWN` and the whole call still returns. Configuration is environment-driven (host, port, home directory, Python path, a no-voice flag) with **no hardcoded absolute paths**; home resolution is drive-independent (an env var → repo root → current working directory). (**VERIFIED** — `servari_server.py`, `health.py`, `AGENTS.md`, each module's `_home()` helper.) (capabilities.md §10)

---

## 5. The gate model

The gate is the SUR's central architectural stance, so it is described here in its own section. The stance, stated plainly: **autonomy is a dial, and irreversible actions always pass a human gate.** (**VERIFIED** — `autonomy.py` + `verify_queue.py` docstrings; `AGENTS.md` "do not weaken the gates".) (capabilities.md §5)

### 5.1 The two inputs

- **Autonomy level (L0–L5).** Each agent has a level from **L0 (suggest only)** to **L5 (full auto)**. The dial widens what an agent may do *silently*. The level→band mapping is **monotonic** — a higher level yields a wider `act` band. (**VERIFIED** — the `LEVELS` table and band constants in `autonomy.py`.)
- **Risk score (4–20).** A proposed action is scored on four factors — reversibility × blast-radius × data-loss × certainty. The higher the score, the more consequential the action. (**VERIFIED** — risk model in `autonomy.py`.)

### 5.2 The composition rule and the hard floor

The two inputs compose into one verdict: `act` (do it silently), `report` (do it but surface it), or `queue` (hold for human approval). The load-bearing property is the **hard floor**: **even at L5 — maximum autonomy — a high-risk score still produces `queue`, not `act`.** High-consequence operations (deploy, real-send, spend, publish, merge, secret access) cannot be auto-crossed at any autonomy level. (**VERIFIED** — band logic in `autonomy.py`; the same rule is restated in plain language in the agent operating persona file.) (capabilities.md §5)

### 5.3 The queue as an append-only audit

`verify_queue.py` is the queue itself. A gated action is enqueued as an append line to `gate-queue.jsonl`; the operator's decision (approve / reject) is a **separate** append line; nothing executes until approved; the audit is never rewritten. Because the queue is append-only and the level→verdict logic is a small, readable function, the safety property is **auditable rather than asserted** — a reviewer can read the entire gate model in two short modules. (**VERIFIED** — `verify_queue.py`: `enqueue` / `list_pending` / `decide` / `history`.) (capabilities.md §5, §8)

### 5.4 Defense in two layers

The gate is enforced in **two complementary places**: the server-side band logic (the hard layer, which an agent cannot talk its way past) and the agent's operating persona file (a soft layer that restates the same rule for the terminal session). The soft layer complements but does not replace the hard layer — a useful distinction for an auditor, because prompt-level rules alone would not be a credible safety claim, whereas a small server-side function that mechanically refuses to cross the floor is. (**VERIFIED** — server logic + persona file both present.) (capabilities.md §5, §6)

### 5.5 Mechanical safety hooks (enforcement by construction)

Beyond the gate, safety is enforced by structure rather than convention: the action runner is allow-listed rather than a raw shell (§4.2), high-risk operations are intercepted before they execute (§5.2–§5.3), the retention loop byte-exactly reverts degrading changes (§6.3), and the repository's own contributor rules forbid weakening any of these (`AGENTS.md` "things to avoid": no raw shell, no weakening the gates, no hardcoded paths, no hardcoded secrets). In an internal health pass, **8/8** mechanical hooks were present, parsing, and running — and one "firing-but-blind" hook was caught and fixed in the same pass, an honest self-catch. (Hooks/runner present: **VERIFIED**; the 8/8 self-catch is a **PARTIAL** internal-log datum.) (capabilities.md §6; _DIGEST.md §3.3)

> **Why the gate model is the spine of the audit.** The category's cautionary tale is precisely the failure this layer targets: the most-adopted open-source incumbent (OpenClaw) carries a documented one-click RCE (CVE-2026-25253, CVSS 8.8), command-injection and prompt-injection CVEs, a companion-service breach exposing ~1.5M auth tokens, and a "shadow superuser" demonstration. The published academic remedy for that class of failure is a **staged human-in-the-loop defense layer** — which is exactly the SUR's claimed differentiator. The audit therefore weights the gate model heavily, while noting that a gate that *bites in the published code* is the verifiable claim, not "the system is safe" in the absolute. (Events **VERIFIED**; exact single-paper defense percentages **PARTIAL** — openclaw.md; researchers.md; _DIGEST.md §4.1)

---

## 6. The memory model

The SUR's memory stance is "**files are the memory**": all state lives in plain files so the system boots into a known state, resumes where it left off, and survives a restart with no database to stand up. (**VERIFIED** — public overview; the seed data directory of JSON / JSONL / Markdown files.) (capabilities.md §7)

### 6.1 What is stored, and in what shape

State files under the seed data directory (or an operator-pointed home) hold the agent channels, autonomy levels, the gate-queue audit, the token-usage log, retention runs, context / active-work markers, and human-readable memory notes and decisions. Concretely: `autonomy-levels.json`, `gate-queue.jsonl`, `token-history.jsonl`, a `retention/` directory, a `context/` directory, `active-work.json`, `memory/decisions.md`, and `memory/notes.md`. (**VERIFIED** — seed directory listing.) (capabilities.md §7)

### 6.2 The curated, non-glob memory surface

The UI does not scan the disk. The memory surface (`memory_surface.py`) reads **only the exact files a curator declares in a registry** — it does **not** glob or walk directories — and it surfaces a missing declared file honestly as `updated: "missing"` rather than fabricating freshness. This is a deliberate **least-privilege** choice: the interface shows only what a human declared, never an arbitrary disk scan. For an auditor, it means the memory surface is a finite, declared set, not an open window onto the filesystem. (**VERIFIED** — `memory_surface.py` docstring.) (capabilities.md §7)

### 6.3 The quality-gated retention loop (regression guard)

The retention loop is how an improvement loop can run unattended **without quality silently eroding**. `retention.py` runs a three-step flow:

1. `baseline(targets)` takes byte copies of the target files and records baseline metric scores.
2. The loop — a job, a scheduler, or a human — edits the targets.
3. `decide(run_id)` re-runs the **same** metric suite and compares: **KEEP** if no gating metric degraded (ties allowed, improvement welcome), or **REVERT** — restore the snapshot bytes exactly, **sha256-verified** — if any gating metric degraded.

It is **fail-closed**: if any metric fails to *run* at decide-time, it reverts; a run can be decided only once; every decision is appended to an audit. Metrics are defined in a registry with `exit_code` or `regex` parse modes. (**VERIFIED** — `retention.py` docstring invariants.) (capabilities.md §9)

The retention loop is the quality-regression guard that the public repo actually ships. The wider platform also describes a separate **failure-pattern regression memory** (recording known failure signatures so a recurrence is recognised and fixed instantly); that named subsystem is **not present as a distinct module in the public repo**. What is shipped and verifiable is the metric-gated KEEP/REVERT loop above. (Retention loop **VERIFIED**; failure-signature memory **UNVERIFIED in repo**.) (capabilities.md §9; _DIGEST.md §2 row 9)

### 6.4 The audit surface and the token meter

Two subsystems make the SUR's activity reviewable — the precondition for an external audit like this one. The **gate queue** (§5.3) and the **retention loop** (§6.3) both write append-only audit lines that are never rewritten, one JSON object per event. The **token meter** (`tokens.py`) reads a JSONL usage log, prices it at configurable per-million rates, and produces per-session / per-day / all-time reports; it is **read-only** against the source and writes only reports. (**VERIFIED** — `tokens.py` docstring.) (capabilities.md §8)

A cost-honesty note belongs in the architecture description because it is a property of the meter itself: the meter's own docstring is explicit that **the token counts are ground truth (logged per message) while the dollar figure is the API-equivalent at the configured rates** — i.e. **cost-to-serve, not cash spent**, since a subscription-billed operator pays differently. Any dollar figure derived from this meter must be read as **API-equivalent cost-to-serve**, with the assumed rates stated. (**VERIFIED** — `tokens.py` docstring; the published repo ships only synthetic seed usage, so this architecture document records no specific dollar figure here — a real figure requires the operator's real log and rate assumptions.) (capabilities.md §8; _DIGEST.md §3.1)

---

## 7. How the SUR's components were obtained (consumption, in brief)

A full treatment is in the companion consumption audit; this section records only the architecturally-relevant fact. Several of the SUR's owned layers were built by **consuming** patterns from permissively-licensed open-source projects and **re-implementing them in the SUR's own stdlib-Python stack** — not by shipping any third-party code. The structural signature is visible on disk: the consumed source sits as segregated reference copies in per-intake directories (the vendors' original TypeScript / JavaScript / Markdown), while the SUR's running scripts are separate Python files that **do not import the references**. (**VERIFIED** structurally — different language, segregated location, no import linkage.) (consumption.md §3, §4)

The intake is governed by a four-question gate (license check → value ÷ overhead ≥ 3× → framework-conflict check → paid-service-drift check) and a six-step pattern that ends in a **real test** plus human review. The consumed patterns include a context-discipline family, a read-before-edit safety invariant, symbol-aware edits (via Python's stdlib AST), a post-edit failure classifier and a syntax-gate (the ACI pattern from **SWE-agent**, MIT), trajectory evaluation (from **agentevals**, MIT), permission-gating / phase-locking and a dangerous-command pre-execution gate, and exploratory-QA + email-handling patterns (from OpenClaw + Hermes, **pattern-only, no vendor code**). The multi-provider routing adapter and the model-hub adapter are present and documented as interface-conforming wrappers, with the live paid-provider call **not** executed in this audit. (**VERIFIED** for the pattern-only re-implementations; **PARTIAL** for the paid-provider adapter — mechanism present, live call not run.) (consumption.md §4; _DIGEST.md §7)

The architecturally-relevant consequence: the components in §3 are an **owned composition**. The SUR consumes the part of the stack the category agrees is commodity (harness-level patterns, edit-safety, context-discipline, trajectory-eval) and reserves its composition — the gate layer, the audit boundaries, the retention guard, and the private build-and-verify method — for the part that is potentially defensible. (**PARTIAL** — the layers are present and inspectable; "constitutes a durable defensibility" is a forward-looking business judgement the auditor describes but does not certify.) (consumption.md §6)

---

## 8. The architecture in one diagram (described)

A reader can hold the whole system in mind as four concentric concerns:

1. **The operator's model** sits outside the SUR entirely (BYOM) — the SUR never owns or hides the intelligence.
2. **The BYOM router** is the single, ~250-line doorway between the operator's model and the shell, carrying one disclosed system line and nothing hidden.
3. **The control plane** — the allow-listed action runner, the autonomy × risk gate with its hard floor, the mechanical hooks — surrounds every action so the blast radius of an over-eager agent is bounded by a hand-curated list and a queue that cannot be auto-crossed.
4. **The record plane** — file-based memory, the curated non-glob memory surface, the append-only gate and retention audits, the read-only token meter, the fail-closed health surface — makes everything the SUR did inspectable after the fact.

The spine (a stdlib HTTP server) wires all four together and degrades every route to a clean "unavailable" rather than failing. (**VERIFIED** — composition of §3–§6.) The single most important thing this picture says is **where the trust lives**: not in a hidden orchestration black box, but in a small, readable control plane and an append-only record plane that an outsider can read in full. (capabilities.md §4 "Why it matters", §10)

---

## 9. Auditor's architectural summary

| Concern | What the published repo provides | Status |
|---|---|---|
| **Model coupling** | One small BYOM router; one disclosed system line; config-edit to swap providers; local model is first-class | **VERIFIED** |
| **Execution surface** | Allow-listed action runner (closed dict; unknown → returns allowed list; not a raw shell) | **VERIFIED**; general MCP layer **UNVERIFIED in repo** |
| **Autonomy & gates** | L0–L5 × 4–20 risk → act / report / queue; hard floor (L5 + high-risk still queues); append-only queue | **VERIFIED** |
| **Memory** | Plain files; curated non-glob surface; honest "missing"; drive-independent home | **VERIFIED** |
| **Quality guard** | Metric-gated KEEP/REVERT; byte-exact sha256-verified revert; fail-closed | **VERIFIED**; failure-signature memory **UNVERIFIED in repo** |
| **Audit & cost** | Append-only audits; read-only token meter; cost = API-equivalent, not cash | **VERIFIED** |
| **Reliability** | Stdlib-only; same-origin; per-module defensive load; HTTP-200 degrade; fail-closed health | **VERIFIED** |
| **Concurrency engine** | Orchestration *surface* + data shapes only | surface **VERIFIED**; execution engine **not in repo** |
| **Sandbox-execute primitive** | Context-pressure *policy* present | policy **VERIFIED**; distinct primitive **UNVERIFIED in repo** |

**Asymmetry note (stated once, plainly).** This system is the work of one researcher with AI assistance, not a funded engineering team. Its strengths — a small, readable, stdlib-only, fail-closed surface with mechanical gates and append-only audits — are real and directly verifiable in the open repo. Its limits are equally honest: four wider-platform capabilities (a distinct sandbox-execute primitive, a general MCP tool layer, a concurrent multi-agent execution engine, a failure-signature regression memory) are **not present in the published repository** and are catalogued here as roadmap, not shipped. Competitor maturity is a roadmap to learn from, not a deficit to spin. (capabilities.md "Asymmetry note"; _DIGEST.md §8)

The accurate one-line characterisation of the architecture: a **verifiable, gate-first, bring-your-own-model agentic operating-system shell** — local-first, file-backed, mechanically gated, and append-only auditable — built from an owned stdlib composition that consumes commodity patterns and reserves its defensibility for the control and record planes. Nothing in this description supports "beats frontier," "fully sovereign," or any unbacked superlative, and none is claimed.

---

### Sources

- The SUR's published open-source repository (Apache-2.0): `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `config.example.json`, the server module docstrings + route table, and the seed data directory — as inventoried in capabilities.md.
- The consumption / consumption evidence (intake gate, segregated reference copies, per-item tests): consumption.md.
- The sealed research synthesis (capability table, honesty rails, the cautionary-tale comparison, cost labelling): _DIGEST.md, drawing on metrics.md, openclaw.md, and researchers.md.
- External / open-source pattern sources named and corroborated as real public projects: agentevals (MIT, trajectory evaluation); SWE-agent (MIT, ACI edit-safety pattern); the Pi.dev coding-agent harness ecosystem (context engine, code-intelligence modules, permission-gate cluster); OpenClaw and Hermes (QA + email workflow patterns); Hugging Face public model-hub APIs. The LLM-as-operating-system / "Software 3.0" paradigm (Andrej Karpathy), per researchers.md.
