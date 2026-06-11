# Limits, Honesty Ledger & Reproducibility

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## Why this document exists

An audit is only as credible as its weakest unstated assumption. Every preceding chapter labels its claims, but those labels are scattered across six documents and eight research files. This chapter pulls them into one place and does three things an outside reviewer should demand:

1. **One consolidated honesty ledger** — every major claim in the audit, with its label (VERIFIED / PARTIAL / UNVERIFIED) and, for each PARTIAL or UNVERIFIED claim, the **specific unlock path** that would raise its label.
2. **A reproducibility boundary** — what an outside reviewer can confirm *right now* from the published materials versus what requires access not yet granted (a clean checkout, an internal log, a live API key, a not-yet-run experiment).
3. **The known limits, stated plainly** — small-local-model immaturity, the solo-builder asymmetry, and the go-to-market / third-party-trust-proof gap.

The intent is not to soften the audit. It is the opposite: a reviewer who can see exactly where the evidence stops is far more likely to trust the evidence that exists. The platform's own materials already practice this — they down-label their own claims where the proof was not run (metrics.md §4) — and this chapter holds the audit itself to the same standard.

### How to read the labels

The labels are used exactly as the source research defines them (metrics.md §0):

| Label | Meaning |
|---|---|
| **VERIFIED** | The figure or claim was read directly from a machine-generated ledger, an inspectable artifact, or public code/registry data a reviewer can re-read or re-run. It is the raw datum, not an estimate. |
| **PARTIAL** | The claim is real but scoped — it depends on a configured rate, holds only for a stated subset, rests on a stated assumption, or lives in an internal artifact not bundled with the public materials. |
| **UNVERIFIED** | Described, planned, or projected; not independently confirmable from the materials examined. |

Two caveats sit underneath every cost figure in the whole audit and are not repeated at each line below (metrics.md §0, §1):

- **Cost is API-equivalent cost-to-serve, NOT cash.** The platform was operated largely under a flat-rate subscription. Dollar figures are token counts × published per-token list rates — "what this volume would cost a buyer on metered API access." That equivalence is the *point* (it is the cost-basis a bring-your-own-model customer would pay), but it is not money that left a bank account.
- **The asymmetry is weighted once, plainly.** This is the output of **one person with AI assistance over ~19 recorded days** (_DIGEST.md §8), not a funded team. Figures are evidence of throughput for a solo+AI operation, not parity with a staffed competitor. Competitor maturity is a roadmap to learn from, not a deficit to spin.

---

## 1. The consolidated honesty ledger

Every major claim the audit makes, grouped by chapter, with its label and the evidence source. This is the single table a skeptical reviewer should start from.

### 1.1 The structural thesis (the spine)

| # | Claim | Label | Source |
|---|---|---|---|
| T1 | The agent harness and the open `SKILL.md` capability format are now **commodities**; defensibility lives in the layers commodity harnesses lack by default. | **VERIFIED** (across three independent source files) | _DIGEST.md §1; openclaw.md §4; gpt-competitors.md §2.2 |
| T2 | The open `SKILL.md` standard is Anthropic-authored (published 2025-12-18); Microsoft (VS Code) and OpenAI (ChatGPT + Codex CLI) adopted it within ~48h; by ~2026-03 roughly 32 tools read the same format. | **VERIFIED** | openclaw.md §4; agentskills.io |
| T3 | The SUR's defensible edge is **structural, not architectural** — gate layer, least-privilege execution, sealed/audited boundaries, fail-closed quality guard, disciplined consumption. | **VERIFIED structurally** (layers present and inspectable) | _DIGEST.md §1, §9; consumption.md §6 |

### 1.2 The shipped public artifact (capabilities)

The audited public repo is **Apache-2.0**: a React front end over a **pure-stdlib Python** HTTP server on `127.0.0.1:8911`, same-origin, bring-your-own-model (_DIGEST.md §2).

| # | Capability | Label | Source |
|---|---|---|---|
| C1 | BYOM model router (OpenAI-compatible `/chat/completions`; one small ~216-line stdlib file + config; one disclosed system line, no hidden prompt). | **VERIFIED** | _DIGEST.md §2 row 1 |
| C2 | Context-pressure policy (measures pressure, verifies survival pins, checkpoints). | **VERIFIED** | _DIGEST.md §2 row 2 |
| C3 | A **distinct** context-discipline sandbox-execute primitive. | **UNVERIFIED in repo** | _DIGEST.md §2 row 2, §8 |
| C4 | Allow-listed action runner (closed `ACTIONS` dict; unknown name returns the allowed list, executes nothing; not a raw shell). | **VERIFIED** | _DIGEST.md §2 row 3 |
| C5 | A general MCP tool layer. | **UNVERIFIED in repo** | _DIGEST.md §2 row 3, §8 |
| C6 | Multi-agent orchestration **surface** (agent grid, org chart, process-table overlay, per-agent channels). | **VERIFIED** (surface) | _DIGEST.md §2 row 4 |
| C7 | A concurrent multi-agent **execution engine** (the orchestration *surface* is present; the engine is not). | **UNVERIFIED in repo** | _DIGEST.md §2 row 4, §8 |
| C8 | Human-in-the-loop gate layer (autonomy dial L0–L5 × 4–20 risk → act/report/queue; **even at L5 a high-risk action still queues** to an append-only `gate-queue.jsonl`). | **VERIFIED** | _DIGEST.md §2 row 5 |
| C9 | Mechanical safety hooks (allow-list + hard gate + byte-exact revert loop; contributor rules forbid weakening them). | **VERIFIED** | _DIGEST.md §2 row 6 |
| C10 | File-based memory (curated surface reads only declared files, never globs; a missing file surfaces honestly as "missing"). | **VERIFIED** | _DIGEST.md §2 row 7 |
| C11 | Audit surface + token meter (append-only audits; token tracker prices counts at configured rates; cost = API-equivalent, not cash). | **VERIFIED** | _DIGEST.md §2 row 8 |
| C12 | Quality-gated retention loop (KEEP only if no metric degrades, else byte-exact sha256-verified auto-revert; fail-closed). | **VERIFIED** | _DIGEST.md §2 row 9 |
| C13 | A broader **failure-pattern regression memory** (beyond the retention loop). | **UNVERIFIED in repo** | _DIGEST.md §2 row 9, §8 |
| C14 | Local server + reliability (stdlib-only, same-origin, every route degrades to a clean "unavailable" at HTTP 200, fail-closed health). | **VERIFIED** | _DIGEST.md §2 row 10 |

> **The honesty rail for this whole audit.** Four wider-platform capabilities — **C3, C5, C7, C13** — are **not present in the published repo**. They are catalogued as roadmap/integration claims, never as shipped. The published artifact is best characterised as a **verifiable, gate-first BYOM agent-OS shell**, and on that scope it delivers what it claims. The public shell should not be over-read as performing autonomous fan-out-and-merge. (_DIGEST.md §2 honesty rail, §8)

### 1.3 The numbers (metrics & evidence)

| # | Figure | Label | Source |
|---|---|---|---|
| M1 | ~10.53B total tokens / 19,333 messages / 556 transcript files / 19 calendar days (2026-05-16 → 2026-06-03). | **VERIFIED** (raw counts) | metrics.md §1 |
| M2 | Cache-read tokens = 10.07B ≈ **93%** of all volume, priced at the cheapest tier (~10× discount vs fresh input) — why blended cost is low. | **VERIFIED** | metrics.md §1, §1b |
| M3 | API-equivalent cost-to-serve = **$26,920.27**; blended ≈ $0.00256 / 1,000 tokens. | **PARTIAL** (rate-dependent; cost-to-serve, not cash) | metrics.md §1, §1b |
| M4 | The widely-quoted "~$10K" is the **stale** 2026-05-24 snapshot (8,004 msgs / $10,047.89); cite the current ~$26.9K. | **VERIFIED** (both snapshots in the history log) | metrics.md §1c |
| M5 | 165 capability modules (7 architectural-core). | **PARTIAL** (self-asserted, reconciler-guarded; not enumerated on disk this pass) | metrics.md §2 |
| M6 | Up to ~260 indexed build-and-verify iterations. | **PARTIAL** (internal log; upper-bound index) | metrics.md §3 |
| M7 | 14/14 multi-site generation acceptance (spec valid + 4/4 pages + working contact form + export-cleanliness scan + live HTTP 200). | **PARTIAL** (internal log; mechanism inspectable) | metrics.md §4 |
| M8 | Quality-evaluation harness: the original five categories pass at 100%; the full expanded suite clears its ≥70% gate at ~79% (failures concentrated in newer framing/discipline categories, not the original five). | **PARTIAL** (internal run; harness re-runnable) | metrics.md §4 |
| M9 | 26/28 aggregate health smoke-test on the current expanded suite (the older "19/19" denominator is a strict subset; honest denominator + failing checks shown). | **PARTIAL** | metrics.md §4 |
| M10 | 8/8 mechanical safety hooks present + parsing + running — with one "firing-but-blind" hook found and fixed in the same pass. | **PARTIAL** (internal self-audit) | metrics.md §4 |
| M11 | 12 tracked product claims: **4 VERIFIED / 8 PARTIAL / 0 UNVERIFIED** — the 4 VERIFIED were the ones actually run on the collection date. | **VERIFIED** (read from the register) | metrics.md §4; gpt-competitors.md §1.2 |
| M12 | Public reproducibility harness (`verify_all.py`): 8/8 PASS, exit 0 — stdlib-only, network-free, runnable on a fresh clone with no keys; verifies the gate hard-floor, fail-closed scoring, append-only queue, honest BYOM no-config, retention KEEP/REVERT, allow-listed runner, HTTP-200 routes, gitignored secrets. | **VERIFIED** (executed on the public repo) | scripts/verify_all.py; metrics.md §5 |
| M13 | Small-model fine-tune: 50 pairs → ≈ −20pp (regression, FAIL); ~150 pairs → +13.3pp (first positive, below the +15pp bar). | **PARTIAL** | metrics.md §6 |
| M14 | Fine-tune projection at ~5,900 pairs → predicted to clear the bar. | **UNVERIFIED** (not yet run) | metrics.md §6 |

### 1.4 Comparison & science

| # | Claim | Label | Source |
|---|---|---|---|
| X1 | OpenClaw security events — CVE-2026-25253 (CVSS 8.8 one-click RCE), command-injection / indirect-prompt-injection CVEs, a companion-service breach exposing ~1.5M auth tokens, a "shadow superuser" demonstration. | **VERIFIED** (events) | openclaw.md; gpt-competitors.md §2 |
| X2 | A staged human-in-the-loop defense layer raised sandbox-escape defense from a ~17% baseline into the 19%–92% range (Claude ~91.5%) — the academic remedy that *is* the SUR's claimed differentiator. | **PARTIAL** (exact single-paper percentages) | openclaw.md; researchers.md |
| X3 | OpenClaw scale ~247K stars (2026-03-02 snapshot), reported ~355K by mid-2026; Hermes ~175K stars in <4 months; ECC 205,179 stars / 31,492 forks (2026-06-03 live API). | **VERIFIED** snapshots; "most-starred / beat React" framing **PARTIAL** (date-dependent) | openclaw.md; ecc.md; gpt-competitors.md §2 |
| X4 | ECC / SUR / OpenClaw all share the same solo or near-solo bus-factor; the real contrast is governance maturity (ECC ships Sponsors, a $19/seat/mo paid tier, ~1,000-test CI, an 80% coverage gate). | **VERIFIED** | ecc.md |
| X5 | There is **no on-record GPT (or external-AI) critique or endorsement** of the SUR; GPT/OpenAI appear only as a request-shape compatibility target and an optional backend; the external-model connector is a mock-driven shell with **no successful real call logged** ($0.00, zero tokens). | **VERIFIED** | gpt-competitors.md Part 1 |
| S1 | The SUR implements the named, public LLM-as-OS / "Software 3.0" paradigm (Karpathy) — it does not invent one. | **VERIFIED** | researchers.md; [Karpathy](https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again) |
| S2 | Multi-agent FOR: Anthropic's orchestrator-worker system outperformed single-agent by 90.2% on its internal eval at ~15× the tokens, token usage explaining ~80% of performance variance. | **VERIFIED** | researchers.md; [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) |
| S3 | Multi-agent AGAINST (steel-man): Cognition's "Don't Build Multi-Agents" — dispersed decisions across agents that don't share full context compound conflicting errors. The SUR is defensible **only insofar as it shares full traces + synthesizes** — an implementation property the audit must keep examining. | **VERIFIED** (the science); SUR's trace-sharing property is **PARTIAL** | researchers.md; [Cognition](https://cognition.ai/blog/dont-build-multi-agents); _DIGEST.md §8 item 7 |
| S4 | Context engineering: context editing alone = +29% lift; with a memory tool = +39%; in a 100-turn eval context editing cut tokens 84%. Degradation is universal across all major models. | **VERIFIED** | researchers.md |
| S5 | Long-horizon reliability: per-step error rate rises as a task progresses and compounds; reliability is domain-stratified — the empirical backbone for the gate + per-step-verification argument. | **VERIFIED** (a ~12-hour-horizon figure is PARTIAL) | researchers.md; [arXiv 2509.09677](https://arxiv.org/abs/2509.09677) |
| S6 | Inference economics: prompt caching cuts cost up to ~90% / latency up to ~85% on long stable prefixes; inference prices fall ~50×/yr (median, Epoch AI) — so the cheap-vs-frontier routing gap is a **depreciating** asset. | **VERIFIED** | researchers.md |

### 1.5 Scalability math (all `$` = API-equivalent at stated rates)

| # | Result | Label | Source |
|---|---|---|---|
| P1 | Per-turn cost: uncached representative turn (20K in / 2K out) = $0.090; cached (16K stable prefix / 4K delta, h=0.90) ≈ $0.0523 → ~42% off the whole turn, ~63% off the input bill. The "~90%" headline is the input-only, high-hit, large-prefix case. | **VERIFIED** arithmetic; splits are **stated assumptions** | scalability.md; _DIGEST.md §6 |
| P2 | The 15× multi-agent premium is **not cancelled** by caching: a shared-prefix 15-worker cached fan-out ≈ $0.755 vs $1.35 naive — caching ~halves it but it is still ~14× a single cached turn. | **VERIFIED** + **PARTIAL** (shared-prefix assumption) | scalability.md |
| P3 | Cost-tier routing ≈ ~3.0× cheaper on a routine-heavy mix (12 of 15 workers routine) — a **depreciating** advantage as prices fall ~50×/yr. | **VERIFIED** arithmetic (quote with date + tier mix + erosion note) | scalability.md |
| P4 | Concurrency saturates (Amdahl): at f=0.90, 10 workers ≈ 5.3×, 25 workers ≈ 6.9×. The observed ~8–10 effective-worker cap is over-determined by the synthesis tax, the shared-context failure mode, and context degradation — structural, not a tuning artifact. | **VERIFIED** | scalability.md; _DIGEST.md §6 |
| P5 | Reliability math: auto-restart buys ~2 nines; retry+backoff handles transient errors only (long-horizon errors compound → need checkpoint+gate); a circuit breaker cuts outage waste ~15×; caching at h=0.8 gives ~5× rate-limit headroom; multi-provider BYOM removes the model SPOF **only if independently configured**. | **VERIFIED** formulas; **stated** inputs | scalability.md |

### 1.6 Consumption posture

| # | Claim | Label | Source |
|---|---|---|---|
| K1 | The platform's posture is **disciplined, mostly-one-way consumption**: consume patterns from permissively-licensed projects, re-implement inside its own owned framework, keep the method private. Independence is visible — different language (stdlib Python vs vendors' TS/JS), segregated reference copies, running code that does not import the references. | **VERIFIED structurally** | consumption.md §6, §8; _DIGEST.md §7 |
| K2 | A four-question intake gate (license check → value÷overhead ≥ 3× → framework-conflict check → paid-service-drift check) + a six-step pattern ending in a real test and human review. | **VERIFIED** (gate applied per-item in the ledger) | consumption.md; _DIGEST.md §7 |
| K3 | Consumed sources are permissive (SWE-agent, agentevals — both MIT; OpenClaw/Hermes pattern-only, no vendor code), with one source-available exception correctly scoped to pattern-only. | **VERIFIED** | consumption.md §7, §8 |
| K4 | The corrected headline: "consume freely; publish a verifiable shell + interfaces; never publish the method" — asymmetric, not literally zero-outbound. | **VERIFIED** | _DIGEST.md §7; consumption.md §8 |
| K5 | "No vendor code" is verified **structurally**, not by a token-level clean-room diff. | **PARTIAL** | consumption.md §7, §8 |
| K6 | A public NOTICE / attributions file is owed before redistribution; one source's license is fair-use rather than classic-OSI (a lawyer's eye recommended before redistributing its reference copy). | **UNVERIFIED** (recommend adding before publish) / **PARTIAL** | consumption.md §7 |
| K7 | Per-item smoke-tests exist (4/4, 5/5, 8/8 across edit-safety + eval items) but no single aggregate regression run of the consumed layer is captured. | **PARTIAL** | consumption.md §7 |

---

## 2. The PARTIAL → VERIFIED unlock paths

A PARTIAL label is not a dead end; it is a claim with a specified next step. This is the section a reviewer who wants to *raise* the audit's confidence should act on. Each row states the minimum action that would move the label.

| Claim | Current label | Unlock path — the exact action that raises the label |
|---|---|---|
| **M3 / M4** cost-to-serve $26.9K | PARTIAL | Re-check the configured per-token list rates (metrics.md §1a) against the providers' current published pricing. The **token counts are already VERIFIED**; only the dollar conversion is rate-dependent. Recomputing at confirmed current rates makes the figure VERIFIED-as-of-date. |
| **M5** 165 modules | PARTIAL | Enumerate the manifest files on a clean checkout (one directory-count command). The count becomes VERIFIED; note that count ≠ validation (see §4.2). |
| **M6** ~260 iterations | PARTIAL | Publish the iteration index with per-entry self-test outcomes so each can be re-read. Until then it stays an upper-bound index, not a per-entry guarantee. |
| **M7** 14/14 sites | PARTIAL | Run the bundled deterministic acceptance generator on a clean checkout. The **mechanism is already inspectable**; a clean-room re-run moves the *result* to VERIFIED. |
| **M8** eval (original-5 100% / full ~79%) | PARTIAL | Re-run the bundled quality-evaluation harness (deterministic graders, no human-in-the-loop). The harness and its grader self-test are inspectable; a fresh run moves the run to VERIFIED. Report the suite version with the score — the older "20/20" is the smaller 5-category suite. |
| **M9** 26/28 smoke | PARTIAL | Run the one-command health check on a clean checkout and report the snapshot against its real (28-check) denominator. |
| **M10** 8/8 hooks | PARTIAL | Re-run the hook self-audit on a clean checkout; the "firing-but-blind" fix is the kind of self-catch a re-run confirms. |
| **M12** reproducibility harness | VERIFIED | Already runnable: clone the repo and run `scripts/verify_all.py` on a fresh checkout (stdlib-only, no keys); expect `PASS (8/8)`, exit 0. This is the audit's strongest freshly-publishable proof and needs no further unlock. |
| **M13** fine-tune deltas | PARTIAL | Publish the training data, eval split, and run logs so the −20pp and +13.3pp deltas are independently reproducible against the open ~0.5B base. |
| **M14** ~5,900-pair projection | **UNVERIFIED** | **Run the experiment.** This is the only honest way to move it — it is currently a projection, not a measured result, and must never be quoted as if it were one. |
| **C3 / C5 / C7 / C13** roadmap capabilities | UNVERIFIED in repo | Ship them in the public repo (or a separately auditable component) with the same inspectable shape as the verified capabilities. Until then they are roadmap claims, not shipped facts. |
| **K5** "no vendor code" | PARTIAL | Run a token-level clean-room diff between the owned stdlib implementations and the segregated reference copies; publish the diff summary. Structural independence is already shown; the diff makes it conclusive. |
| **K6** NOTICE / attributions | UNVERIFIED / PARTIAL | Add a public NOTICE/attributions file naming the consumed sources and their licenses; obtain a license review for the one fair-use / source-available source before redistributing its reference copy. |
| **K7** aggregate consumption regression | PARTIAL | Add a single bundled regression run that executes all per-item consumption smoke-tests together, so "the consumed patterns stay healthy" is one re-runnable command. |
| **S3** SUR shares full traces | PARTIAL | Demonstrate, on the public shell, that multi-agent work shares full traces and synthesizes (rather than blind-concatenating) — the property that, per Cognition's steel-man, separates a defensible multi-agent design from a failure-prone one. (Bound by C7: the concurrent execution engine is not in the public repo.) |
| **X2** sandbox-escape defense percentages | PARTIAL | Cite the specific academic paper(s) and quote their exact reported intervals; the *events* and the *direction* are VERIFIED, the exact single-paper percentages are not yet pinned. |
| **Citations** (S-rows, X-rows) | VERIFIED with internal pointer | Follow the public URL now surfaced in [`docs/REFERENCES.md`](./REFERENCES.md); each external claim is checkable against its primary (Karpathy talk, Anthropic/Cognition posts, METR/Epoch/arXiv). No internal-pointer-only citation remains for an external claim. |

> **The pattern across every unlock path:** almost all of them are a **clean-checkout re-run** or a **publish-the-artifact** step — not new engineering. The exception is **M14**, which genuinely requires running an experiment that has not been run. That distribution is itself a finding: the gap between PARTIAL and VERIFIED here is mostly *packaging and disclosure*, not capability.

---

## 3. Reproducibility — what an outside reviewer can do now vs not

### 3.1 Reproducible now, from the published materials

These require nothing beyond the public Apache-2.0 repo and public registry/API data. A reviewer can confirm them today.

- **Inspect the shipped shell directly.** The BYOM router (~216-line stdlib file + config, one disclosed system line), the allow-listed action runner (closed `ACTIONS` dict; unknown name → returns the allowed list, executes nothing), the file-based memory (declared-files-only, never globs), the audit surface + token meter, and the local stdlib server (same-origin, every route degrades to a clean "unavailable" at HTTP 200) are all **present and readable in the repo**. (_DIGEST.md §2)
- **Run the public reproducibility harness.** The published shell ships a stdlib-only,
  network-free `scripts/verify_all.py`; a reviewer clones the repo and runs it on a fresh
  checkout with no API keys to get `PASS (8/8)`, exit 0 — verifying the gate hard-floor,
  fail-closed scoring, the append-only queue, honest BYOM no-config, retention KEEP/REVERT,
  the allow-listed runner, HTTP-200 routes, and gitignored secrets. This is the audit's
  strongest **executed** proof against published code, with no AI judgment in the loop.
  (scripts/verify_all.py; metrics.md §5)
- **Verify the gate model bites.** The autonomy dial (L0–L5) × risk score (4–20) routing, and the property that **even at L5 a high-risk action still queues** to the append-only `gate-queue.jsonl`, are inspectable in the published code — and executed directly by `verify_all.py` checks V001/V002. (_DIGEST.md §2 row 5)
- **Read the safety hooks.** The allow-list + hard gate + byte-exact revert loop, and the contributor rule forbidding their weakening, are in the repo. (_DIGEST.md §2 row 6)
- **Re-read the public claim register.** The 4 VERIFIED / 8 PARTIAL / 0 UNVERIFIED tally is read directly from the pack's own register and verdict. (metrics.md §4)
- **Re-derive the blended cost rate.** $26,920.27 ÷ 10,533M tokens ≈ $0.00256 / 1,000 tokens is division of two figures present in the ledger. The **token counts are VERIFIED**; only the rate behind the dollar figure needs a current-pricing check. (metrics.md §1, §1b)
- **Confirm the competitor facts.** OpenClaw/Hermes/ECC star counts and the ECC live GitHub API numbers (205,179 stars / 31,492 forks at 2026-06-03), the `SKILL.md` standard's provenance and cross-vendor adoption, and the OpenClaw CVE/breach events are all from public sources a reviewer can re-pull. (openclaw.md; ecc.md; gpt-competitors.md)
- **Check the consumption independence structurally.** Different implementation language from the vendors, segregated reference-copy directories, and running code that does not import those references are observable in the repo layout. (consumption.md §6, §8)
- **Re-run every scalability calculation.** The per-turn cost, the 15× fan-out premium, the Amdahl saturation curve, and the reliability formulas are arithmetic on stated assumptions — re-computable by hand. (scalability.md)

### 3.2 Reproducible only with a clean checkout + a run (not in the public pack yet)

The *mechanisms* are inspectable; the specific *results* live in internal logs. A reviewer with a clean checkout can re-produce these, but they cannot be confirmed from the bundled materials alone:

- The **14/14** site-generation acceptance run, the quality-eval suite (original-five categories at 100% / full-suite ~79% gate-cleared), the **26/28** smoke-test snapshot, and the **8/8** hook self-audit. (Run the bundled tests on a fresh checkout — metrics.md §4, §8 item 2.) *(Note: the eight public gate/queue/retention/runner properties from this set are already executable today via `scripts/verify_all.py` — §3.1.)*
- The **per-item consumption smoke-tests** as a single aggregate regression. (Add one bundled regression command — consumption.md §7.)

### 3.3 Not reproducible from public materials at all (yet)

These require access not granted, an artifact not published, or an experiment not run:

- The **~260 build-iteration log** and the **165-module inventory** as individually-validated items — internal logs; the public repo ships a subset, not the full private module set. (metrics.md §2, §3)
- The **fine-tune deltas** (−20pp, +13.3pp) until the training data + eval split + run logs are published; and the **~5,900-pair projection (M14)**, which has **not been run** and cannot be confirmed by any amount of re-reading. (metrics.md §6)
- A **successful real external-model (e.g. GPT) call** — the connector is a mock-driven shell with no successful live call logged; until a live call is captured, the cross-provider path is interface-only. (gpt-competitors.md Part 1)
- The four **roadmap capabilities (C3/C5/C7/C13)** — not in the public repo, so not reproducible as shipped behaviour. (_DIGEST.md §8)
- A **token-level clean-room diff (K5)** — an owed artifact, not yet published.

> **The reproducibility verdict.** The *architecture and the gate/audit/memory/consumption disciplines* are reproducible **now**. The *performance and acceptance tallies* are reproducible **with a clean checkout**. The *fine-tune wins, the autonomous multi-agent execution, and the live cross-provider call* are **not yet reproducible** — and the audit labels them accordingly. An honest buyer's checklist: trust the shell as readable today; require a clean-checkout test run before trusting the tallies; treat the fine-tune and roadmap items as in-progress.

---

## 4. The honest known limits

Three limits matter most for anyone deciding what the platform is. None is concealed; each is stated with its evidence and its honest framing.

### 4.1 Small-local-model maturity — a capability-in-progress, not a shipped win

The fine-tune track targets specializing a small open **~0.5B-parameter** instruct model against a **pre-registered** pass bar (format-compliance ≥ +20pp OR category-accuracy ≥ +15pp) (metrics.md §6). The measured record is:

- **50 training pairs → ≈ −20pp.** The first attempt made the small model *worse* — a regression, honestly left in the record. Loss converged high (~3.05), consistent with undertraining (3 epochs / 50 pairs / 0.5B / CPU). **PARTIAL.**
- **~150 pairs → +13.3pp category accuracy.** The first end-to-end *positive* result — it proves the pipeline works (train → adapter → chat-template → local conversion) but **does not clear** the pre-registered bar. Pipeline-validated, target-not-yet-met. **PARTIAL.**
- **~5,900-pair projection → predicted to clear.** A plan, **not a measured result. UNVERIFIED.**

The credibility signal *is* the −20pp and the sub-threshold +13.3pp left in the record. A vendor spinning this would quote only the projection (metrics.md §6). The honest reading: small-local-model specialization here is a **capability-in-progress**, never to be presented as shipped.

This sits inside the broader, independently-grounded reality that small-model maturity is hard everywhere: long-horizon per-step error compounds (S5), and the model layer is the part of the stack the platform most clearly does **not** lead. The sovereignty / run-your-own-model path is validated as a *direction* by peers who ship open weights (Nous/Hermes), but that is roadmap context, not a present SUR capability. (researchers.md; gpt-competitors.md §2.1, §2.3)

A second, narrower limit in the same family: the public reproducibility harness
(`scripts/verify_all.py`, 8/8 PASS — §5 / M12) is the audit's strongest **executed** proof,
but a PASS means *those eight public properties hold on the published code*, **not** "the
system is safe" in the absolute. It checks the gate hard-floor, fail-closed scoring, the
append-only queue, honest BYOM no-config, retention KEEP/REVERT, the allow-listed runner,
HTTP-200 routes, and gitignored secrets — it is a verifiable floor, not a safety
certification.

### 4.2 The solo-builder asymmetry — throughput is notable, edges are expected

The entire platform is the output of **one person with AI assistance over ~19 recorded calendar days** (_DIGEST.md §8 item 1; metrics.md §0). This asymmetry is weighted honestly in both directions:

- **In the platform's favour:** the throughput (~10.53B tokens of build-and-verify work, the breadth of inspectable disciplines) is genuinely notable for a solo+AI operation, and the disclosure discipline (down-labelling its own claims) is auditor-grade. (metrics.md §1, §4)
- **Against it:** **counts are an inventory, not a validation.** The ~165 modules is a self-asserted, reconciler-guarded figure; a meaningful fraction carry an "encoded but not yet independently validated" status. Acceptance tallies are real and their mechanisms inspectable, but most specific runs live in internal logs (metrics.md §2, §4, §8). Unfinished edges are *expected* from a 19-day solo build and should be read as such, not spun as completeness.
- **Bus-factor is a shared category trait, not a unique weakness.** ECC carries the same near-solo asymmetry (`affaan-m` = 1,426 commits vs the #2 human's 47, ~30:1) (ecc.md). So solo-build is **not a differentiator either way** — what differs is governance maturity, which the next limit addresses.

The disciplined rule throughout this audit: **competitor maturity is a roadmap to learn from, not a deficit to spin** (consumption.md §7; _DIGEST.md §8 item 1).

### 4.3 The go-to-market / third-party-trust-proof gap — behind on reach, not on engineering

The clearest place the platform is **behind** is not the code; it is distribution and external validation (_DIGEST.md §8 item 2):

- **Reach / ecosystem.** Incumbents sit at **175K–355K stars** with large skill marketplaces (OpenClaw ~247K–355K; Hermes ~175K; ECC 205,179) (openclaw.md; ecc.md; gpt-competitors.md §2). The SUR has no comparable public footprint.
- **Shipped paid go-to-market.** ECC already ships a **$19/seat/mo** tier, GitHub Sponsors, a ~1,000-test CI suite, and an 80% coverage gate (ecc.md). The SUR's commercialization is not yet a shipped, externally-purchasable product.
- **Third-party trust proof.** There is **no on-record external-AI critique or endorsement** of the SUR, and **no successful live external-model call** is logged (gpt-competitors.md Part 1). What the SUR *does* offer a third party today is the **public reproducibility harness** (`scripts/verify_all.py`, 8/8 PASS, exit 0): anyone can clone the open repo and execute the gate/queue/retention/runner properties for themselves, with no AI judgment and no keys (§5 / M12). That is verifiable, but it is self-published code a reviewer runs — not an independent third-party endorsement, which the SUR does not have.
- **Open-model-production line.** The platform has no shipped open-weight model; peers in the category do (gpt-competitors.md §2.3).

The honest conclusion the source research converges on: **the gap is distribution and third-party trust-proof, not engineering** (_DIGEST.md §8 item 2). The remedy is reach, independent verification, and a shipped paid offering — exactly the unlock paths in §2 (publish artifacts, enable clean-checkout reruns) plus a go-to-market motion the competitor landscape already demonstrates is achievable.

---

## 5. What this ledger lets a reviewer conclude

Pulling the labels together gives a precise, defensible verdict — and nothing beyond it.

- **The shipped public artifact delivers what it claims on its actual scope:** a verifiable, gate-first, BYOM agentic operating-system shell. The gate layer, least-privilege runner, inspectable memory, audit surface, fail-closed retention, and stdlib reliability are **VERIFIED and readable today**. (_DIGEST.md §2, §9)
- **The defensible edge is structural, not architectural** — and that is a *stronger* claim than a harness-uniqueness claim would be, because in this category no harness uniqueness is available to anyone (T1–T3). The most load-bearing finding is the human-in-the-loop gate that still queues high-risk actions at maximum autonomy — precisely the remedy the category's worst documented security failures call for (X1, X2).
- **The numbers sit inside the public envelope.** Caching saves real money but does not cancel the ~15× fan-out premium (P1, P2, S2); concurrency saturates near ~8–10 effective workers (P4); the cheap-routing edge is depreciating (P3, S6). No figure exceeds what the independent literature supports.
- **The unfinished parts are labelled, not hidden:** four roadmap capabilities not in the repo (C3/C5/C7/C13), a fine-tune track that is genuinely in-progress (M13/M14), and a go-to-market gap that is real (§4.3). The single UNVERIFIED-and-unrunnable item is the fine-tune projection (M14) — and it is flagged as such.
- **Most of the distance between PARTIAL and VERIFIED is disclosure, not engineering** (§2). That is the most actionable conclusion in this chapter: the credibility of this audit can be materially raised by clean-checkout reruns and published artifacts, with one genuine experiment (M14) outstanding.

No part of this audit asserts that the platform "beats frontier," is "fully sovereign," or approaches "AGI." None of those is claimed in any source, and the labels above are the reason a reader can trust that restraint: where the evidence was not run, it is marked — by the platform's own materials first, and by this audit second. That self-down-labelling is the single most reassuring property in the entire body of evidence.

---

## 6. Strongest counterarguments — pre-empted, not hidden

This section exists because a hostile reader should encounter the strongest objections
*with* their honest responses, not discover them independently and conclude the audit was
hiding them. Each attack below is mounted at full force; the response is given only where one
genuinely exists. Where a point requires a concession, it is conceded.

---

### 6.1 "Consume-not-harness is just rebranding"

**The attack:** The SUR uses the same open `SKILL.md` format as its competitors, took
patterns from the same ecosystem tools they build on, and re-implemented those patterns in
its own language — which every derivative tool also does. The word "consume" is a narrative
choice, not an observable engineering distinction.

**Honest response (partial concession):** The attack correctly identifies that "consume"
carries more implication than the evidence directly supports. The falsifiable claim behind
the terminology is narrower: the SUR's **running code carries no imported dependency on any
consumed reference source.** That is a real property — it means no supply-chain coupling, no
GPL contamination risk, no runtime reliance on a vendor's release cadence — and it is
structurally verifiable (different implementation language, segregated reference
directories, no import linkage; consumption.md §3). The narrative framing is defensively
weak. The engineering property is real.

**Concession:** "Consume" as a differentiating brand should be read as shorthand for that
specific falsifiable property, not as a claim of broader architectural distinctiveness at
the harness level, which the audit explicitly concedes is commodity.

---

### 6.2 "The defensibility is overstated"

**The attack:** Every described architectural component — the HITL gate, the retention loop,
the allow-listed action runner — is simple enough that a team reading this audit could
reproduce any of them in a day. The audit describes how to copy the SUR's differentiators
while claiming those differentiators are defensible.

**Honest response (qualified concession):** The attack is correct that no individual
component is a permanent, copy-proof advantage, and this audit explicitly does not claim
otherwise. The honest claim throughout is a **current-state structural advantage**, not a
permanent one: the VERIFIED shipped capabilities constitute an advantage specifically over
the documented failure modes of the most-adopted category incumbents (CVE-2026-25253, the
~1.5M-token breach, the "shadow superuser" demonstration — openclaw.md;
gpt-competitors.md §2). A team that reads this audit and then builds the equivalent of
`autonomy.py` and `verify_queue.py` would be closing the exact gap the CVE record
evidences — and the existence of that gap today, among the most-adopted tools, is what the
current-state claim rests on.

**Concession:** The docs use "current-state structural advantage" rather than any
permanent-advantage framing throughout; informal reads of the word "defensible" should be
understood in the bounded sense above. The four UNVERIFIED roadmap capabilities
(C3/C5/C7/C13) contribute nothing to this claim and should not be read as if they do.

---

### 6.3 "The metrics are cherry-picked"

**The attack:** The strongest acceptance tallies are PARTIAL because the specific runs are
internal. The only independently verifiable quantitative figures are the token counts
(machine-generated) and the fine-tune deltas — and the fine-tune deltas show a regression
(−20pp) and a sub-threshold result (+13.3pp). The headline numbers are internal; the
verifiable numbers are the failures.

**Honest response:** The distribution of labels in the metrics chapter is not
cherry-picking — it is the evidence structure. The −20pp regression, the corrected
eval/smoke figures, the stale-vs-current cost correction, and the 8 PARTIAL claims are all
present and labeled. A cherry-picked metrics chapter would quote only the clean tallies and
omit the regression; this audit calls the −20pp "the credibility signal" (metrics.md §6).

**Presentation fix applied:** The Executive Summary (doc 00) now carries the PARTIAL labels
co-located with every quoted acceptance tally ("14/14 (PARTIAL — internal log)", the eval
shown as original-five 100% / full-suite ~79% gate-cleared, "26/28 (PARTIAL)") rather than
quoting them bare. The labels that lived downstream in doc 07 are now carried upstream to
where the figures first appear.

---

### 6.4 "Single-operator means this is not real engineering"

**The attack:** No CI, no peer review, no coverage gate, no external test suite, no paying
customers, no third-party security audit. Four capabilities unshipped. A fine-tune track with
a net regression. A smoke test that fails some checks. This is a prototype, not a production
engineering artifact.

**Honest response:** Every item in that list is already stated in this audit at the
locations cross-referenced throughout; no part of it is hidden. The accurate framing of the
asymmetry: **this is engineering at prototype/MVP scale with verification debt outstanding**,
not "not real engineering." The stdlib-only Python server, the inspectable gate logic, the
byte-exact retention loop — these are verifiable engineering artifacts with provably correct
properties independent of team size. "Even at L5 a high-risk action still queues" is either
true or false and is checkable by reading the gate function in `autonomy.py`. Team size does
not change that property.

**The gap is specific and documented:** ECC ships ~1,000 tests, an 80% coverage gate, and a
$19/seat/mo paid tier (ecc.md). The SUR does not. That gap is distribution and verification
infrastructure, not a category gap in engineering correctness on the shipped components.
Both can be true simultaneously.

**Unlock:** Publish the bundled tests; enable clean-checkout reruns. Most of the distance
from "prototype" to "verified" is disclosure, not new engineering (§2 of this document).

---

### 6.5 "An audit written with the subject's own AI is not independent"

**The attack:** The primary build tool (Claude Opus 4.8) also authored this audit. The same
model that built the SUR evaluated it. The multi-model cross-check is three other AI models,
not independent humans. "Independent" in any professional audit sense requires no prior
involvement, no stake, and human accountability — none of which applies here. This is
structurally a self-review.

**Concession (significant):** This attack is **substantially correct on the terminology.**
The audit does not use "independent" in the professional-audit sense. The README abstract and
the executive-summary header have been changed to "structured technical audit built with AI
assistance, applying a labeled-evidence standard (VERIFIED / PARTIAL / UNVERIFIED) to
primary sources," and a methodology note states the AI-authorship limitation up front.

**What survives the attack:** The VERIFIED claims in this audit rest on **publicly readable
code and public registry data**, not on the AI's assessment of its own work. A reviewer who
has never seen Claude can read `autonomy.py`, `verify_queue.py`, `retention.py`, and the
public OpenClaw CVE advisories, and confirm every section-A VERIFIED claim
([`09-claims-register.md`](./09-claims-register.md) §A) without trusting a single AI
judgment. That is the honest meaning of "independently verifiable" here — the evidence is
public-source, not AI-attested. The AI's role was to read the public sources and structure
the labeling; the labels themselves can be re-derived by any reviewer from the same sources.

**The multi-model cross-check** is not a substitute for human peer review. It is a
de-correlation mechanism that catches within-family blind spots — useful, but it does not
constitute an independent human audit. What the audit offers a reviewer *instead* of an
internal cross-check record is the **public reproducibility harness** (`scripts/verify_all.py`,
8/8 PASS, exit 0): the load-bearing safety properties are executable on the published code
by anyone, with no model judgment in the loop (§5 / M12).

**The honest bounded claim:** This is a structured, labeled, multi-model-cross-checked
review of a shipped codebase, where the evidence for VERIFIED claims is independently
readable public code. It is not a Big Four audit, a NIST assessment, or an ISO
certification. It is more transparent — with labeled evidence grades, explicit
down-labeling, and a stated reproducibility boundary — than most product documentation in
this category. It is not, and does not claim to be, professionally independent.

---

### 6.6 Summary verdict table

| Attack | Concession required? | Where it is handled |
|--------|----------------------|---------------------|
| "Consume-not-harness is rebranding" | PARTIAL — tighten terminology | §6.1 above; consumption.md §3, §5 |
| "Defensibility is overstated" | YES — "current-state structural advantage", not a permanent copy-proof advantage | §6.2 above; doc 00 "A note on 'defensibility'" |
| "Metrics are cherry-picked" | NO on substance; YES on presentation | §6.3 above; doc 00 PARTIAL labels co-located |
| "Single-operator = not real engineering" | YES on scale; NO on category | §6.4 above; §4.2 of this document |
| "Audit written with own AI is not independent" | YES — language concession | §6.5 above; README + doc 00 header + methodology note |

---

*All figures carry VERIFIED / PARTIAL / UNVERIFIED labels per the source research. Cost figures are API-equivalent cost-to-serve, not cash. Every multiplier states its scope. This document is sealed for outward publication and asserts no unbacked superlatives. The platform consumes open-source patterns one-way into an owned framework; it does not ship a harness and is not described as one.*
