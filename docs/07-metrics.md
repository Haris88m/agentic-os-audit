# Metrics — Honest, Labeled, and Scoped

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## How to read this document

This is the numbers chapter of an independent third-party technical audit of the system under review (the "SUR" or "the platform"). It exists to do one thing well: present the platform's quantitative claims **honestly** — every non-trivial figure carries an explicit confidence label, every cost figure carries the API-equivalent caveat, and every multiplier states its scope.

Auditor integrity is the deliverable here. A metrics chapter that flatters the subject is worthless; a metrics chapter that down-labels its own evidence where the proof is thin is, paradoxically, the more trustworthy artifact. The source materials already do this self-down-labelling (see §6), and this chapter preserves it.

### The three labels

| Label | Meaning |
|---|---|
| **VERIFIED** | Read directly from a machine-generated ledger or a test artifact a reviewer can re-run or re-read. The figure is the raw datum, not an estimate or projection. |
| **PARTIAL** | The figure is real but is scoped to a subset, depends on a configured rate, or lives in an internal artifact not bundled in the public materials. The *mechanism* is usually inspectable; the *specific run* is not externally reproducible without a clean checkout. |
| **UNVERIFIED** | Described, planned, or projected — not independently confirmable from the materials examined. |

### Two caveats that apply to every figure in this chapter

1. **Cost is API-EQUIVALENT cost-to-serve, NOT cash.** The platform was operated largely under a flat-rate subscription. Every dollar figure is `token counts × published per-token list prices` — i.e. *what this volume would cost a buyer running it on metered API access*. That equivalence is the useful number (it is the cost-basis a bring-your-own-model customer would actually pay), but it is not money that left a bank account. (Source: `metrics.md` §0 caveat 1; `_DIGEST.md` §8.4.)

2. **The asymmetry must be weighted.** This is the output of **one person with AI assistance over ~19 recorded calendar days**, not a funded team. Read the figures as evidence of throughput for a solo-plus-AI operation, not as parity with a staffed competitor. Competitor maturity is a roadmap to learn from, not a deficit to spin. (Source: `_DIGEST.md` §8.1.)

---

## 1. Token volume and API-equivalent cost-to-serve

This is the most solid evidence in the entire audit: a machine-generated usage ledger, regenerated 2026-06-03, aggregating **556 session transcript files**. Token counts are ground truth (parsed directly from transcripts); cost is `counts × configured list rates`. (Source: `metrics.md` §1.)

| Metric | Value | Label | Notes |
|---|---|---|---|
| Transcript files aggregated | 556 | **VERIFIED** | Ledger `transcript_files`. |
| Recorded messages | 19,333 | **VERIFIED** | Ledger `totals.messages`. |
| Input tokens | 15,784,495 | **VERIFIED** | Ledger `totals.in`. |
| Output tokens | 55,583,873 | **VERIFIED** | Ledger `totals.out`. |
| Cache-write tokens | 396,640,751 | **VERIFIED** | Ledger `totals.cache_write`. |
| Cache-read tokens | 10,065,077,885 | **VERIFIED** | Ledger `totals.cache_read` — the dominant term, ~93% of all tokens. |
| **Total tokens (all four classes)** | **~10.53 billion** | **VERIFIED (sum)** | 15.78M + 55.58M + 396.64M + 10,065.08M = 10,533,086,004. Arithmetic on four ledger totals. |
| **API-equivalent cost-to-serve** | **$26,920.27** | **PARTIAL** | Ledger `totals.cost_usd`. PARTIAL because it depends on the configured list rates (§1.1) and is cost-to-serve, NOT cash (see caveat 1 above). |
| Span of activity | 2026-05-16 → 2026-06-03 | **VERIFIED** | 19 calendar days; ledger `by_day` keys, first to last. |

### 1.1 The configured rates behind the dollar figure (USD per million tokens)

| Model class | in | out | cache-write | cache-read | Label |
|---|---|---|---|---|---|
| Opus | 15.00 | 75.00 | 18.75 | 1.50 | VERIFIED (as configured) |
| Sonnet | 3.00 | 15.00 | 3.75 | 0.30 | VERIFIED (as configured) |
| Haiku | 1.00 | 5.00 | 1.25 | 0.10 | VERIFIED (as configured) |

> **Stated assumption.** These are the rates the ledger applied. A reviewer should re-check them against current published pricing; if list prices move, the dollar total moves proportionally — **the token counts do not change.** (Source: `metrics.md` §1a.)

### 1.2 Why cost-to-serve is heavily discounted — the cache-read dominance

Cache-read tokens (10.07B) are ~93% of total volume and are priced at the cheapest tier (1.50/M for the dominant model class versus 15.00/M for fresh input — a **10× discount**). This is the structural reason the blended dollar-per-token rate is low: most of the volume is re-reading a cached, stable context rather than paying fresh-input rates. (Source: `metrics.md` §1b; `_DIGEST.md` §3.1.)

- **Blended rate check:** $26,920.27 ÷ 10,533M tokens ≈ **$0.00256 per 1,000 tokens** blended. **VERIFIED (derived)** — division of two VERIFIED ledger totals. *Assumption:* treats all four token classes as a single pool; it is a blended average, not a per-class rate.

### 1.3 Two consistency cross-reads

- The ledger's per-model sub-totals for the two primary model versions sum to $21,067.39 + $5,794.27 + minor others ≈ the $26,920.27 grand total — **internally consistent. VERIFIED (cross-read).** (Source: `metrics.md` §1c.)
- An earlier ledger snapshot (2026-05-24) recorded **8,004 messages / $10,047.89** API-equivalent. The current snapshot (19,333 messages / $26,920.27) is a superset of the same accounting method over a longer window.

> **The "~$10K" figure is stale.** The widely-quoted ~$10K is the **earlier** snapshot. The current cost-to-serve is **~$26.9K**. A reviewer should cite the current figure and treat any "~$10K" reference as superseded. **VERIFIED (both snapshots present in the history log).** (Source: `metrics.md` §1c; `_DIGEST.md` §3.1.)

---

## 2. Capability-module inventory

The platform is organized as a library of composable capability modules (each a self-contained instruction file plus optional deterministic scripts), rather than a single monolithic prompt. (Source: `metrics.md` §2.)

| Metric | Value | Label | Notes |
|---|---|---|---|
| Counted capability modules | 165 | **PARTIAL** | The platform's own count-reconciler asserts 165 modules (a module = a directory containing a manifest file; staging/infrastructure excluded). PARTIAL: the auditor did not enumerate all 165 directories on disk this pass; the figure is the system's self-asserted, reconciler-guarded count. A reviewer can re-derive it by counting manifest files. |
| Architectural-core modules (closed inner set) | 7 | **PARTIAL** | Declared closed; same provenance caveat. |
| Modules in the *public* open-source shell | subset (not the full 165) | **PARTIAL** | The public repo ships the agent shell plus the gate/queue interface, not the full private module set. The exact public count was not enumerated this pass. |

> **Counts are not validation.** "165 modules" is an inventory of *capability files*, not a claim that all 165 are individually battle-tested. A meaningful fraction carry an "encoded but not yet independently validated" status. Inventory ≠ all-validated. (Source: `metrics.md` §2; `_DIGEST.md` §8.5.)

---

## 3. Documented build-and-verify iterations

The platform records its build history as a numbered sequence of **build-and-verify iterations** — each one a change, a self-test step, and a logged outcome. (Source: `metrics.md` §3.)

| Metric | Value | Label | Notes |
|---|---|---|---|
| Highest iteration index referenced | ~260 | **PARTIAL** | Internal records reference iteration indices into the ~260 range. PARTIAL: from internal logs, not reproducible from the public pack; it is an **upper-bound index**, not a guarantee that every index in 0..260 is a fully-logged, independently-verifiable event. |
| Iterations citing an in-line self-test result | many (dozens sampled) | **PARTIAL** | A sample of the internal log shows iterations routinely paired with a pass/fail self-test line (examples in §4). Not exhaustively audited. |

> **Honest reading.** The *practice* of pairing each build step with a verification step is evident and consistent across the sampled records. The exact total of fully-reproducible iterations was not independently counted. (Source: `metrics.md` §3.)

---

## 4. Acceptance-test pass rates — the strongest reproducible-shape evidence

These are concrete, counted test outcomes recorded in build artifacts. They are the most audit-friendly figures in the chapter because each is a discrete pass/fail tally and each underlying mechanism is inspectable. (Source: `metrics.md` §4; `_DIGEST.md` §3.3.)

| Test surface | Result | Label | Notes |
|---|---|---|---|
| Multi-site generation acceptance run | **14/14 PASS** | **PARTIAL** | A batch of 14 generated sites; each asserted on: spec valid + 4/4 pages present + a working contact form + an export-cleanliness scan + a live HTTP 200 from a local server. PARTIAL: the 14/14 is recorded in an internal build log; a reviewer reproduces by re-running the bundled generator. The deterministic acceptance script is inspectable. |
| — spec-validation sub-step | 14/14 PASS | PARTIAL | Same run, validation gate. |
| — page-presence sub-step | 4/4 pages × 14 sites | PARTIAL | Same run. |
| — live-serve sub-step | 14/14 returned HTTP 200 | PARTIAL | Same run, against a local HTTP server. |
| Quality-evaluation harness (full run) | **20/20** across 5 categories | **PARTIAL** | 4/4 each on: memory recall, capability selection, path resolution, security decision, document generation. Deterministic graders, no human-in-the-loop. PARTIAL: recorded internally; the grader self-test (14/14) and the harness are inspectable and re-runnable, but this specific 20/20 run is not bundled in the public pack. |
| Aggregate health smoke-test | 17–19 of 19 checks | **PARTIAL** | A one-command health check across subsystems; snapshots range 17/19 to 19/19. PARTIAL: internal; the **honest spread is shown** rather than the best single number. |
| Mechanical safety hooks present + parsing + running | 8/8 hook scripts | **PARTIAL** | A self-audit reported all 8 enforcement hooks present, parsing, and executing — with one "firing-but-blind" hook found and fixed in the same pass (an honest self-catch, not concealed). PARTIAL: internal self-audit. |

### 4.1 The public claim register — a metric of disclosure discipline

The public pack tracks 12 product claims and labels them itself:

| Register tally | Value | Label |
|---|---|---|
| Claims VERIFIED | **4** | VERIFIED (read from the register) |
| Claims PARTIAL | **8** | VERIFIED (read from the register) |
| Claims UNVERIFIED | **0** | VERIFIED (read from the register) |

The 4 VERIFIED claims — file-based memory survives a restart; the human-approval gate mechanism; model-routing against a standard-shape stand-in; a deterministic export/redaction gate biting 3/3 fixtures with zero leaks — were the ones whose evidence was **actually run** on the collection date. The fact that the pack down-labels its own 8 unrun claims rather than promoting them is itself a positive trust signal. **VERIFIED (read directly from the pack's claim register and verdict).** (Source: `metrics.md` §4 auditor note; `_DIGEST.md` §3.4.)

---

## 5. Product-boundary interview scores

The platform runs an adversarial "interrogate-the-persona-before-it-ships" check: an independent interrogator agent probes a product persona across four boundary classes and scores each probe pass/fail. The interview record is the proof artifact. (Source: `metrics.md` §5; `_DIGEST.md` §3.5.)

| Metric | Value | Label | Notes |
|---|---|---|---|
| Probes generated for one product persona (a trading-coach persona) | **15 probes** | **PARTIAL** | Distribution: 5 boundary-refusal (will it refuse one-way actions?) + 4 grounding (will it invent a number it cannot know?) + 3 leak-resistance + 3 self-honesty. PARTIAL: a self-test result recorded internally; the protocol generator and scorer are inspectable, the specific run is not bundled publicly. |
| Synthetic transcript scored | 3 probes → **2 pass / 1 fail**, planted leak correctly flagged | **PARTIAL** | The scorer caught a planted leak (exit non-zero), demonstrating the gate bites. Same provenance caveat. |
| Separate human-led adversarial interview of the live product | refusal held on attack attempts; **one over-claim was broken by the interviewer and conceded/corrected by the system** | **PARTIAL** | The most credible data point in this section: under a second, less-correlated interviewer the system's own claim was challenged and it **conceded and corrected rather than doubling down**. PARTIAL: transcript is internal (and contains a real name that must be redacted). |

> **Honesty limit carried from the source.** A boundary "pass" means "held its boundaries on the probes asked," NOT "is safe." Leak-detection scoring is **literal-term matching, not paraphrase-aware** — a determined paraphrase could evade it. (Source: `metrics.md` §5; `_DIGEST.md` §3.5.)

---

## 6. Small-model fine-tune deltas — where candor is the finding

The platform ran a fine-tuning track to specialize a small open base model. These are the honest, measured deltas — including the early *negative* result, which is the most credibility-relevant figure in the whole chapter. (Source: `metrics.md` §6; `_DIGEST.md` §3.6.)

**Base model:** an open **~0.5B-parameter** instruct model.
**Pass thresholds, pre-registered:** format-compliance **≥ +20pp** OR category-accuracy **≥ +15pp** versus the un-tuned base.

| Run / config | Measured delta vs base | Pass? | Label | Notes |
|---|---|---|---|---|
| Early run (50 training pairs) | **≈ −20pp** (regression) | **FAIL** | **PARTIAL** | The first attempt made the small model *worse* — honestly recorded, not hidden. Loss converged high (~3.05), consistent with undertraining (3 epochs / 50 pairs / 0.5B / CPU). Internal training report. |
| Mid run (~150 pairs) | **+13.3pp category accuracy** (first positive delta) | **Below** the +15pp category bar (and below the +20pp format bar) | **PARTIAL** | The first end-to-end *positive* result, proving the pipeline works (train → adapter → chat-template → local conversion). It did **not** clear the pre-registered pass threshold. Honest reading: pipeline-validated, target-not-yet-met. Internal eval artifact. |
| Projected at scaled data (~5,900 pairs) | predicted to clear the threshold | not yet run | **UNVERIFIED** | A plan/projection, not a measured result. Flagged UNVERIFIED per the auditor's own rule. |

> **Auditor reading of this track.** The most honest signals here are the **−20pp first result** and the **+13.3pp that still missed the bar**. A vendor spinning this track would quote only the future projection; the records instead leave a real, partial, sub-threshold improvement *and* a clearly-labelled un-run projection in plain sight. **That candor is itself the finding.** This is a **capability-in-progress, not a shipped win** — never present it otherwise, and never quote the projection alone. (Source: `metrics.md` §6; `_DIGEST.md` §3.6 + §8.6.)

---

## 7. Scaling multipliers — every one scoped

This section consolidates the calculation-derived figures from the scalability model. The pattern is consistent: each multiplier is **real arithmetic on stated assumptions**, and each one is bounded by a scope caveat that an honest reader must carry alongside it. All dollar figures are API-equivalent cost-to-serve at the modelling rates (`P_in` $3/M, `P_out` $15/M, `P_cache_read` $0.30/M). (Source: `scalability.md` §1–§4.)

### 7.1 Caching savings

| Figure | Value | Label | Scope caveat (load-bearing) |
|---|---|---|---|
| Saving off a representative *cached* turn | **~42%** | VERIFIED (arithmetic) | Scoped to a 16k stable-prefix / 4k delta / 2k output turn at hit-rate h=0.90. Output is full price and does not cache. |
| Saving off the *input bill* of that turn | ~63% | VERIFIED (arithmetic) | Input-side only; the 16k/4k split is a stated assumption. |
| The headline "up to ~90% cheaper" | up to ~90% | VERIFIED (literature) | **Scope:** the input-token-only, high-hit-rate, large-stable-prefix case — NOT a whole-turn saving. Break-even is ~2+ cache hits per prefix; a prefix used once is a net loss (~25% write premium with no read amortization). |

(Source: `scalability.md` §1.2; literature via `researchers.md` §7.)

### 7.2 The multi-agent multiplier — caching does not cancel it

| Figure | Value | Label | Scope caveat |
|---|---|---|---|
| Multi-agent token multiplier vs single chat | **~15×** | VERIFIED (literature) | Anthropic's orchestrator-worker research figure (`researchers.md` §3). |
| 15-worker cached fan-out cost-to-serve | **~$0.755** vs $1.35 naive | VERIFIED + PARTIAL | Caching ~halves the fan-out bill **but it is still ~14× a single cached turn (~$0.0523).** PARTIAL on the shared-prefix assumption: it requires workers genuinely share the same cached prefix, an implementation property. |

> **Net statement (carry it verbatim).** Parallel orchestration buys **wall-clock speed and breadth by spending tokens**; caching reduces the premium but does not remove it. (Source: `scalability.md` §1.3.)

### 7.3 Cost-tier routing — a real but depreciating advantage

| Figure | Value | Label | Scope caveat |
|---|---|---|---|
| Routing saving on a routine-heavy mix | **~3.0× cheaper** | VERIFIED (arithmetic) | Scoped to a fan-out where **12 of 15 workers are routine** and routine runs at a tier ~10× cheaper than the frontier tier. |

> **The caveat that makes the 3× honest.** Inference prices are falling **9×–900× per year across tasks, median ~50×/yr** (Epoch AI, via `researchers.md` §7 — VERIFIED). The *gap* between cheap-tier and frontier-tier — the very thing routing monetizes — **shrinks over time.** The routing advantage is real **today** and is a **depreciating asset**, not a permanent defensibility. Any routing multiplier must be quoted with date + tier mix + the erosion note. (Source: `scalability.md` §1.4.)

### 7.4 Concurrency speedup — Amdahl saturation

| Workers (at parallel fraction f=0.90) | Speedup | Label |
|---|---|---|
| 10 workers | **~5.3×** (not 10×) | VERIFIED (Amdahl) |
| 25 workers | **~6.9×** | VERIFIED (Amdahl) |

> **The observed ~8–10 effective-worker cap is structural, not a tuning artifact.** Three independent forces converge on roughly that number: (1) the Amdahl synthesis tax — the lead's brief-composition + N-output synthesis is the serial `(1-f)` part; (2) the documented multi-agent failure mode where agents that do not share full context produce compounding, conflicting outputs, so synthesis cost rises **super-linearly** with N; and (3) context degradation — a lead synthesizing 25 reports loads a large context and hits the degradation curve that motivates keeping context small. (Source: `scalability.md` §2.2–§2.3; `researchers.md` §4–§5.)
>
> **Honest envelope.** The platform is inside the defensible zone **only** when workers run genuinely independent sub-tasks AND the lead receives full traces and *synthesizes* (rather than blind-concatenates). Whether the platform actually shares full traces is an implementation property — surface verified (per-agent append-only channels + a synthesizing lead), concurrent execution engine **not present in the public repo (PARTIAL/UNVERIFIED)**. (Source: `scalability.md` §2.3; `_DIGEST.md` §8.7.)

### 7.5 Reliability leverage

| Practice | Figure | Label | Scope caveat |
|---|---|---|---|
| Health-check + auto-restart | **~98% → ~99.97%** availability | VERIFIED (formula) | "~2 nines from MTTR alone" at 24h MTBF, moving MTTR 30 min → 30 s. MTBF/MTTR are stated inputs. |
| Retry + backoff (3 attempts, p=0.9) | **90% → 99.9%** | VERIFIED (formula) | **Transient, independent errors only.** Long-horizon errors compound and are NOT independent — retrying a half-corrupted trajectory can make things worse; the long-horizon cure is checkpoint + gate, not retry. |
| Circuit breaker | **~15× less** wasted work per outage | VERIFIED (arithmetic) | Trip-after-3 vs 15 workers × 30s × 3 retries. Trip threshold + timeout are stated inputs. |
| Caching as load-shedding (h=0.8) | **5×** rate-limit headroom | VERIFIED (arithmetic) | At h=0.8 the system makes 1/5 the upstream calls. h taken from the cited 80–95% production band. |
| Multi-provider BYOM redundancy | `1 − (1−A)^k` | VERIFIED (formula) / PARTIAL (deployment) | The redundancy math **assumes independence.** Two providers in the same model family, or two "redundant" components on one machine, are correlated and do NOT deliver the math. The platform makes multi-provider fallback *possible* (config-swappable BYOM); whether a deployment is genuinely independent is the operator's configuration, not an intrinsic guarantee. |

> **Convergence worth noting.** The rate-limit admission math (`W × calls_per_worker_per_min ≤ provider_RPM`) and the concurrency math **independently converge on ~8–15 workers** as the useful band. (Source: `scalability.md` §4.1–§4.6.)

---

## 8. The literature-grounded upside — measured elsewhere, not here

To keep the multipliers honest, it is worth stating plainly where the strongest positive evidence actually comes from: independent research, not the platform's own benchmarks.

| Finding | Value | Label | Whose number |
|---|---|---|---|
| Multi-agent vs single-agent uplift | **+90.2%** on an internal eval | VERIFIED | Anthropic's orchestrator-worker research system — at ~15× tokens, with token usage explaining ~80% of performance variance. NOT the platform's own benchmark. (`researchers.md` §3.) |
| Context-editing token reduction | **84%** over a 100-turn eval | VERIFIED | Anthropic context-engineering research; context editing alone +29% lift, with a memory tool +39%. Validates the platform's context-discipline approach in principle. (`researchers.md` §5.) |
| Prompt-caching cost / latency cut | up to **~90% / ~85%** | VERIFIED | On long stable prefixes; 80–95% production hit rates. (`researchers.md` §7.) |
| Inference price decline | **~50×/yr** (median; range 9×–900×) | VERIFIED | Epoch AI — the reason cost-tier-routing advantages depreciate. (`researchers.md` §7.) |

> **The honest reading.** The multi-agent upside is **real and measured — elsewhere.** The platform adopts the same pattern, so its expected upside is "plausibly large on breadth-heavy tasks, at a ~15× token premium" — but that is **NOT a number the platform has independently benchmarked** in the public sources. For the platform specifically, the uplift figure is **UNVERIFIED**; what is verified is that its scaling *choices* ride documented curves. (Source: `scalability.md` §2.4.)

---

## 9. One-line honest summary

| Dimension | Headline figure | Strongest honesty caveat |
|---|---|---|
| Token volume | ~10.53B tokens / 19,333 msgs / 556 files / 19 days | VERIFIED raw counts. |
| Cost-to-serve | **~$26,920** API-equivalent | NOT cash (subscription); rate-dependent; ~93% is cheap cache-read; the older "~$10K" is stale. |
| Capability modules | 165 (7 core) | Self-asserted, reconciler-guarded count; inventory ≠ all-validated. |
| Build iterations | up to ~260 indexed | Internal log; upper-bound index, not all reproducible from the public pack. |
| Acceptance tests | 14/14 sites · 20/20 eval · 8/8 hooks | Mechanisms inspectable; specific runs largely internal. |
| Public claim register | **4 VERIFIED / 8 PARTIAL / 0 UNVERIFIED** | The 4 VERIFIED were actually run; the 8 are honestly down-labelled. |
| Product-boundary interview | 15 probes; gate bites on planted leak | "Pass" = boundaries held on the probes asked, not "safe"; literal-term scoring. |
| Small-model fine-tune | **−20pp → +13.3pp** (still sub-threshold) | A capability-in-progress; the scaled projection is UNVERIFIED. |
| Caching saving | ~42% off a cached turn (up to ~90% input-only) | Scoped: whole-turn vs input-only; break-even at ~2+ hits. |
| Multi-agent premium | ~15× tokens | Caching ~halves the fan-out but it is still ~14× a single cached turn. |
| Cost-tier routing | ~3.0× on routine-heavy mix | Depreciating as inference prices fall ~50×/yr; quote with date + mix. |
| Concurrency cap | ~8–10 effective workers | 10 workers ≈ 5.3×, not 10× (Amdahl); cap is over-determined and structural. |

---

## 10. What an auditor would tell a buyer about these numbers

1. **The token/cost ledger is the most solid evidence** — machine-generated, internally consistent, two-snapshot history. Trust the **counts** as VERIFIED; treat the **dollar figure** as a configurable cost-to-serve (not cash), and quote the **current ~$26.9K**, not the stale ~$10K. (Source: `metrics.md` §8.1.)

2. **The acceptance-test tallies (14/14, 20/20, 8/8) are real and the mechanisms are inspectable**, but most specific runs live in internal logs. For full external reproducibility, the bundled tests must be run on a clean checkout. (Source: `metrics.md` §8.2.)

3. **The fine-tune track is honest about being unfinished.** Do not let −20pp → +13.3pp be read as a shipped capability, and never quote the ~5,900-pair projection on its own. (Source: `metrics.md` §8.3.)

4. **Every multiplier depreciates or is scoped.** Caching saves the input bill but not output; the ~15× fan-out premium is not cancelled by caching; the ~3× routing advantage erodes as inference prices fall ~50×/yr; concurrency saturates near ~8–10 workers. None of these is a permanent defensibility, and the audit does not present any of them as one. (Source: `scalability.md` §5.)

5. **The disclosure discipline itself is a positive signal.** A claim register that reads 4/8/0 with the 4 actually run, a smoke-test reported as a 17–19/19 *spread* rather than the best number, a "firing-but-blind" hook surfaced rather than hidden, and a −20pp regression left in the record — these are the marks of materials that down-label themselves rather than over-claim. For an independent auditor, that is worth more than any single multiplier. (Source: `metrics.md` §8.4; `_DIGEST.md` §3.4.)

6. **Weight the asymmetry.** This throughput is a solo operator with AI assistance over ~19 recorded days, not a funded team. That makes the volume notable and the un-finished edges expected. Competitor maturity (large star counts, shipped paid go-to-market, open-model production lines) is a roadmap to learn from — the platform's gap is **distribution and third-party trust proof, not engineering.** (Source: `metrics.md` §8.5; `_DIGEST.md` §8.1–§8.2.)

---

### Forbidden framings (none used in this chapter, by design)

This audit makes no claim that the platform "beats frontier" systems, is "fully sovereign," or approaches "AGI," and uses no unbacked superlative. The platform CONSUMES open-source patterns one-way into its own architecture — it consumes them, it does not ship a harness. None of the source research claims otherwise, and this chapter keeps it that way. (Source: `_DIGEST.md` §8.8.)
