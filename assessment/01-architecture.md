# 01 — The Architecture

**Apex Prime, described at pattern level.** This document specifies the design as an engineer would need it to evaluate or adopt it. It deliberately describes _what the architecture is_ and _why each part exists_; the private build-method (the specific iterative process that produced the implementation) is withheld by documented decision — see [doc 05](./05-limits.md).

---

## 1. The design stance: CONSUME

Every agentic platform must answer one question: **what is your relationship to the ecosystem around you?** The dominant answer in 2026 is the _harness_: ship an environment (configs, skills, hooks, rules) that installs onto coding agents and optimizes their behavior. The harness answer has a structural property its own license acknowledges: everything it publishes is consumable by anyone, including its competitors — MIT-licensed virality _is the business model_.

Apex Prime's answer — the architect's invention, and the word he insists on — is **CONSUME**:

> The ecosystem is raw material. Patterns flow **one way**: from the open world, through a gate, into owned modules. Nothing of the method flows back out.

Mechanically, CONSUME is a four-question intake gate applied to every candidate consumption:

| #   | Gate question                                                                                                | Rejects                                             |
| --- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| 1   | **License** — is the source permissively licensed (MIT/Apache/BSD/ISC)?                                      | copyleft contamination of a commercial composition  |
| 2   | **Value ÷ integration-overhead ≥ 3×?**                                                                       | dependency bloat; 50 MB frameworks for one function |
| 3   | **Framework conflict** — does it impose external state, cloud coupling, build-system mandates?               | architectural erosion by convenience                |
| 4   | **Paid-service drift** — would this default the platform onto a paid dependency where open raw material exists? | rent where ownership is available                   |

What passes the gate is not _imported_ — it is **re-implemented** in the platform's own stack (a deliberately boring one: standard-library Python, plain files), tested with a real run, and only then admitted. The public consumption ledger documents ~8 consumption families yielding ~12 owned capability modules this way — including a context-discipline/sandboxed-execute family where **one consumed open engine yielded four owned capabilities** — each entry license-checked and pattern-only. **VERIFIED (public ledger; structural inspection: the running code does not import the reference copies).**

The strategic consequence is quantified in [simulation 1](../simulations/sim_capability_growth.py): a tuning strategy saturates at its harness's ceiling; a gated-consumption strategy's intake scales with the _ecosystem_, bounded only by verification bandwidth. The faster the open ecosystem grows, the wider the gap — and the ecosystem is growing very fast.

## 2. The BYOM engine knob: the model is an engine, not a dependency

The second load-bearing decision: **no reasoning model is structural.** Models sit behind one OpenAI-compatible configuration surface — base URL, model name, key file — and the architecture's behaviors (its prompts-as-policy, gates, memory, seal) are engine-agnostic by construction. Three properties follow:

1. **Price becomes a menu.** [Simulation 2](../simulations/sim_cost_per_task.py) prices the same representative task across engines: $1.16 (frontier) → $0.23 (standard) → $0.077 (light) → **$0.038** (DeepSeek V4 Pro, the production fleet's actual engine since 2026-06-11). A 9-agent fleet's month: $12,539 frontier-pinned vs. $406 at the BYOM floor. **VERIFIED arithmetic on list prices.**
2. **Provider shocks become operations, not crises.** When a provider changes terms — as one did in June 2026 — the response is an engine swap, not a migration. The measured event: the full 9-agent fleet moved providers **same-day**, verified live 9/9. [Simulation 3](../simulations/sim_provider_shock.py) generalizes this: mean fleet degradation under a random shock falls from ~31 days (coupled architecture, assumed band) to ~1.2 days (engine-knob, anchored) — **26× fewer lost tasks**. **SIMULATED, anchored to the measured swap.**
3. **Per-bot staged rollout.** The knob supports per-agent engine assignment (`engine:agent1,agent2`), so a fleet migrates one agent at a time with instant rollback — risk management built into the configuration grammar. **VERIFIED (published config surface).**

## 3. The autonomy-gate layer: autonomy with a mechanical conscience

The architect describes the platform as "in a way autonomous, because of the full design" — and the qualifier is the engineering. Autonomy here is not a model given permission; it is a **composition** with a mechanical conscience:

- An **autonomy dial (L0–L5)** sets how much the system may do without asking, per deployment.
- Every action carries a **risk score** (irreversibility, blast radius, outward reach, credential touch).
- The dial × score matrix decides: act silently / act and report / **queue for a human**.
- **The hard floor:** at L5 — maximum autonomy — a high-risk action _still queues_. There is no configuration in which the system may take an irreversible, outward-facing action unreviewed. The queue is append-only (`gate-queue.jsonl`), so the decision trail is itself an audit artifact. **VERIFIED (published shell implements the dial, the scoring, and the floor).**

The floor is not free — it costs operator attention — and the design's bet is that the price is small and the payoff large. [Simulation 5](../simulations/sim_gate_safety.py) prices it with the category's own published security measurements as anchors (a staged human-review layer measured at ~91.5% catch rate with the strongest reviewer): at L5, the floor costs **≈3 human reviews/day** and prevents **≈238 expected unsafe pass-throughs/year** versus the same dial without the floor (267 vs. 505). **SIMULATED, anchored.** Against the category's documented failure modes — a CVSS 8.8 one-click RCE, a credential breach exposing ~1.5M tokens, a demonstrated "shadow superuser" — the gate layer is the design's answer _in mechanism rather than in policy_.

Autonomy's other half is **survival**: the system is built to wake up knowing where it was. State lives in files (§4); every loop checkpoint is recoverable; a restart is a resume, not an amnesia event. Continuous loops + gates + persistent memory is what "in a way autonomous" cashes out to — and each of the three is independently inspectable.

## 4. Files are the memory

All durable state — configuration, memory, queues, audit trails, the regression bank — is **plain files**: human-readable, diff-able, grep-able, versionable. No database server, no opaque store, no vendor format. The published shell reads a _declared_ memory surface (named files, never globs) and surfaces a missing file honestly as "missing" rather than silently empty. **VERIFIED.**

Three consequences: audits need no tooling (the audit surface _is_ the filesystem); persistence has no moving parts to fail; and the operator can always answer "why did it do that?" by reading the same files the system read. This is the unglamorous decision that makes the autonomy claim governable.

## 5. Sealed boundaries

The inverse of CONSUME's one-way intake is a one-way **seal** on the way out. Anything outward-facing — published code, reports, messages, this assessment — passes a deterministic, fail-closed export/redaction gate that strips the private layer: the build-method, internal vocabulary, key material, private paths. The published shell demonstrates the same principle in miniature: the private engine is not in the open repo, and the open code _fails closed_ when the engine is absent rather than degrading into an insecure approximation. **VERIFIED (published repo: fail-closed engine boundary; the redaction gate measured biting 3/3 planted fixtures with zero leaks).**

The seal is why this document can be public at all: the architecture is describable at pattern level — and is, here — while the method that produced it remains property. That asymmetry (_consume freely; publish a verifiable shell and interfaces; never publish the method_) is the precise form of the "one-way" claim. **VERIFIED structurally.**

## 6. The fan-out: parallel orchestration with synthesis

For work wider than one context window, the architecture fans out: N parallel agents agents, each briefed with identity + role + a self-contained task, results synthesized centrally — never blind-concatenated. The design respects the published failure mode for multi-agent systems (dispersed decision-making over partial context produces compounding errors): workers run **scoped** tasks, the orchestrator holds the full trace, and synthesis is a first-class step. The public literature's envelope — parallel fan-out buys wall-clock speed and breadth at a ~15× token premium; ~8–10 effective workers before synthesis overhead dominates — matches the architecture's own operating numbers. **VERIFIED literature; PARTIAL (internal operating logs).**

The June 2026 proof event used exactly this: the engine-swap was executed as a parallel multi-worker operation (design, implementation, seal-verification, live roll-call) compressed into one day.

## 7. The regression memory: failures become mechanism

Every classified failure — a tool that hangs, an encoding that corrupts, a provider quirk — is written into a permanent, structured bank and consulted _before_ retries: recover once, never re-diagnose. Over time the bank converts operational pain into mechanical immunity; the platform's measured recovery from a known failure class is sub-second (a lookup), versus the original diagnosis cost (minutes to hours). The published shell ships the same idea as a quality-gated retention loop: a change is kept only if no metric degrades, else **byte-exact, hash-verified auto-revert** — fail-closed. **VERIFIED (shell); PARTIAL (the wider bank lives in private logs).**

---

## The composition is the invention

None of the seven patterns is individually novel — the literature names most of them, and doc 04 credits it. The invention is the **stance plus the composition**: one-way intake (CONSUME) + engine-agnostic core (BYOM) + mechanical conscience (the gate floor) + inspectable persistence (files) + one-way outbound (seal) + synthesized parallelism + compounding immunity (regression memory) — operated continuously by a single architect, and now carrying measured proof events. Doc 02 turns the composition into an adoption blueprint; doc 03 prices it.

---

_[← Executive Assessment](./00-executive-assessment.md) · [02 — Implementation Guide →](./02-implementation-guide.md)_
