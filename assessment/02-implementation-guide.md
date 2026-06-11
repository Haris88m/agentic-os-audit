# 02 — Implementation Guide: How the Architecture Can Be Used

The CONSUME architecture is adoptable. This document is the engineering blueprint: what to build, in what order, with acceptance criteria — written for a team (or a single operator with AI assistance) implementing the pattern on their own stack. A working Apache-2.0 **reference shell** implementing the gate dial, BYOM router, file memory, and seal boundary exists and passes a stranger's full verification (8/8 verify, 160/160 tests); it is evidence that the blueprint below is buildable, and a legitimate starting point for teams that prefer code to specification.

**Scope note.** This guide transfers the _architecture_. The original's private build-method is not part of the transfer — adopters supply their own engineering process. That is the same deal every published architecture offers, stated openly.

---

## Adoption profiles

| Profile              | Who                                                | Build                                                                               |
| -------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **A — Operator**     | one person + AI assistance, personal/company fleet | stages 1–5, ~2–4 weeks of evenings                                                  |
| **B — Product team** | a team embedding agents in a product               | stages 1–6, with stage 4 (gates) non-negotiable before production                   |
| **C — Enterprise**   | platform group standardizing agent operations      | all stages; the seal (stage 5) and audit surface (stage 1) are the compliance story |

## Stage 1 — Files are the memory _(foundation; half a day)_

Put **all** durable state in plain files under one root: config, memory, queues, audit logs. Declared filenames only — no globs; a missing file surfaces as "missing," never as silently-empty. Append-only for anything evidentiary (audits, gate decisions).

**Acceptance:** kill the process mid-task; restart; the system resumes from files alone. `grep` answers "why did it do that?"

## Stage 2 — The BYOM engine knob _(1–2 days)_

One configuration surface for the reasoning engine: `base_url`, `model`, `key_file` (key read at call time from a file outside the repo — never env-printed, never logged, never in argv). Code to the OpenAI-compatible chat shape; treat _every_ provider, including the premium ones, as a guest behind the knob. Add `max_tokens` explicitly — one provider's metering pre-authorizes the model's full output window against your balance if you omit it (a real defect class, found by consuming the reference shell with a small-balance account; fixed 2026-06-11).

**Acceptance:** swap providers by editing config only — zero code changes; a canary task answers identically-shaped output on both engines. Per-agent engine assignment (`engine:agent1,agent2`) gives you staged rollout with instant rollback.

## Stage 3 — The CONSUME intake gate _(process, not code; institute immediately)_

Adopt the four questions verbatim — license / value÷overhead ≥ 3× / framework conflict / paid-service drift — as a written checklist applied to **every** external pattern, library, or tool you bring in. Re-implement what passes in your own stack (pattern-only, no vendor code), run a real test, and record one ledger line per consumption: source, license, what was taken (pattern), what was built (module), test result.

**Acceptance:** a reviewer can reconstruct from the ledger alone what entered the system, from where, under what license, with what proof. [Simulation 4](../simulations/sim_consume_leverage.py) prices the payoff: ~3× leverage per capability, ~3× yearly capability throughput at a fixed verification budget.

## Stage 4 — The autonomy dial and the floor _(the production gate; 2–4 days)_

Score every action the agent can take on irreversibility, blast radius, outward reach, credential touch (a 4–20 scale works). Set an autonomy dial L0–L5 per deployment. Wire the matrix: low-risk → act; medium → act + report; high → **queue, always, at every dial level**. The floor is the design: do not make it configurable. Queue to an append-only file with enough context to decide from the queue itself.

**Acceptance:** at L5, a high-risk action (delete, publish, pay, message a stranger) demonstrably queues. [Simulation 5](../simulations/sim_gate_safety.py) gives the rationale to your security review: the floor buys ≈47% fewer expected unsafe pass-throughs at maximum autonomy for ≈3 reviews/day.

## Stage 5 — The seal _(before anything outward-facing; 1–2 days)_

A deterministic, fail-closed export gate between your system and the world. Denylist your private layer: internal method vocabulary, key material, private paths, personal data. Every outbound artifact — published code, reports, agent messages — passes the gate or does not ship. Test it with planted leaks; it must bite all of them.

**Acceptance:** 3/3 planted fixtures blocked, zero leaks on real artifacts; the gate fails **closed** on error. Pair it with the boundary inverse: anything private simply is not in the public artifact, and the public code fails closed when the private part is absent — never degrades into an insecure approximation.

## Stage 6 — Fan-out + regression memory _(scale; ongoing)_

Parallel fan-out only for genuinely independent work; scoped briefs; the orchestrator keeps full traces and **synthesizes** (never concatenates). Budget honestly: the literature's ~15× token premium for multi-agent breadth is real, so route fan-outs through your cheap tier (stage 2 makes that a config line). And institute the regression bank from the first failure: classify → fix → record → consult-before-retry. Failures are capital; spend them once.

**Acceptance:** a previously-seen failure class is recovered mechanically (lookup, not re-diagnosis); fan-out runs land within your per-task cost envelope from [simulation 2](../simulations/sim_cost_per_task.py).

---

## What adopting teams get, in numbers

| Property                        | Without                          | With Apex Prime pattern                      | Source                     |
| ------------------------------- | -------------------------------- | -------------------------------------------- | -------------------------- |
| Provider shock response         | weeks of migration (14–60d band) | same-day engine swap (measured)              | sim 3, anchored            |
| Cost per task                   | $1.16 frontier-pinned            | $0.22 routed / $0.038 floor                  | sim 2, verified arithmetic |
| Capability growth               | saturating tuning curve          | gated-consumption compounding, 2× by month ~6 | sim 1, simulated           |
| Unsafe actions at full autonomy | 505/yr expected (no floor)       | 267/yr (floor on)                            | sim 5, simulated-anchored  |
| Audit story                     | tooling + faith                  | `grep` over append-only files                | stage 1, verified pattern  |

## Failure modes to engineer against (learned, real)

1. **Omitted `max_tokens`** → full-window pre-authorization → hard 402s on small balances. Set it explicitly (stage 2).
2. **Gate floor made configurable** → it will be configured off. The floor is load-bearing _because_ it is not a setting.
3. **Consumption without the ledger** → six months later nobody can answer the license question. The ledger line costs one minute.
4. **Fan-out on coupled tasks** → compounding divergence (the published multi-agent failure mode). Fan out only what is independent; synthesize centrally.
5. **Seal as policy instead of mechanism** → policy erodes under deadline pressure; a fail-closed gate does not.

---

_[← 01 — Architecture](./01-architecture.md) · [03 — The Numbers →](./03-simulations.md)_
