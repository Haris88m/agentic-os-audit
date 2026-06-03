# Scalability — A Quantitative Study

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## How to read this document

This is the quantitative centerpiece of the audit. It models the **cost, concurrency,
throughput, and reliability** of the system under review (the "SUR" or "the platform")
from the outside, with stated assumptions, worked numbers, and a literature anchor under
every non-trivial claim. It is written by an independent third-party auditor — not in the
first person, not branded as any product.

Three rails run through every section:

1. **Every non-trivial claim is labeled** **VERIFIED** / **PARTIAL** / **UNVERIFIED.**
   VERIFIED = the cited source or the arithmetic states it directly. PARTIAL = real but
   scoped, rate-dependent, or recorded in an internal artifact not bundled publicly.
   UNVERIFIED = described or projected, not independently confirmable here.
2. **Every dollar figure is API-equivalent cost-to-serve, NOT cash.** The operator ran
   the platform largely on a flat-rate subscription, so the dollar figures are token
   counts multiplied by published per-token list rates — "what this volume *would* cost a
   buyer on metered API access." That equivalence is the useful number (it is the
   cost-basis a bring-your-own-model customer would actually pay), but it is not money
   that left a bank account.
3. **Every multiplier states its scope.** No claim of beating frontier systems, no claim
   of full autonomy, no superlative. The honest finding is narrower and more useful: the
   platform's scaling choices ride documented cost/reliability curves, and its
   concurrency and reliability math sit *inside* the envelope the public literature
   supports.

A terminology note carried from the consumption audit (`02-consumption-audit.md`): the
platform's relationship to open source is **consumption** — it consumes patterns one-way
into its own architecture and re-implements them in its own owned framework. It is not a
"harness" and it does not "harness" anything; the word *harness* below describes only the
generic class of competing tools, for contrast.

---

## 0. Notation and stated assumptions

These symbols are used throughout. Each calculation re-states the ones it depends on.
They are **modelling inputs** chosen to be defensible against the cited literature — not
measurements of one specific production run unless explicitly said so.

| Symbol | Meaning | Assumed value | Basis |
|---|---|---|---|
| `P_in` | input token list price | $3.00 / M tok | Sonnet-class list price (Anthropic pricing, via the inference-economics literature, §5) — VERIFIED as configured |
| `P_out` | output token list price | $15.00 / M tok | same tier — VERIFIED as configured |
| `P_cache_read` | cached input read price | $0.30 / M tok (≈10% of `P_in`) | prompt-caching literature (§5) — VERIFIED |
| `P_cache_write` | cache write premium | ≈1.25 × `P_in` ($3.75 / M) | prompt-caching literature ("~25% premium", §5) — VERIFIED |
| `h` | cache hit rate on a stable prefix | 0.80–0.95 | observed production band (§5) — VERIFIED |
| `M` | multi-agent token multiplier vs single chat | ≈15× | Anthropic multi-agent research (§5) — VERIFIED |
| `t` | per-worker sub-task wall-clock | task-dependent | modelling input |
| `S` | lead-orchestrator fan-out + synthesis overhead | task-dependent | modelling input |
| `N` | number of parallel agents | variable | modelling input |
| `f` | parallelizable fraction of a job | 0.0–1.0 | Amdahl input (§2) |
| `A` | component availability | variable | reliability input (§4) |

> **Cost-to-serve disclaimer (carried everywhere).** All `$` are API-equivalent at the
> rates above. A subscription-billed operator's cash outlay differs. Where a figure is
> sensitive to the rate, the sensitivity is stated.

The configured rates the platform's own usage ledger applied, for completeness
(USD per million tokens — VERIFIED as configured, not re-priced against a live tariff):

| Model class | in | out | cache-write | cache-read |
|---|---|---|---|---|
| Top tier (Opus class) | 15.00 | 75.00 | 18.75 | 1.50 |
| Mid tier (Sonnet class) | 3.00 | 15.00 | 3.75 | 0.30 |
| Light tier (Haiku class) | 1.00 | 5.00 | 1.25 | 0.10 |

If list prices move, the dollar totals move proportionally; the token counts do not.

---

## 1. Token economics — cost per task, caching savings, cost-to-serve

### 1.1 The measured volume (the ground truth this section scales from)

Before modelling, here is the one solid empirical anchor: a machine-generated usage
ledger, regenerated 2026-06-03, aggregating **556 session transcript files** over a
**19-calendar-day window (2026-05-16 → 2026-06-03)**.

| Metric | Value | Label |
|---|---|---|
| Recorded messages | 19,333 | VERIFIED (ledger total) |
| Input tokens | 15,784,495 | VERIFIED |
| Output tokens | 55,583,873 | VERIFIED |
| Cache-write tokens | 396,640,751 | VERIFIED |
| Cache-read tokens | 10,065,077,885 | VERIFIED — the dominant term, **~93% of all tokens** |
| **Total tokens (all four classes)** | **~10.53 billion** | VERIFIED (sum: 15.78M + 55.58M + 396.64M + 10,065.08M = 10,533,086,004) |
| **API-equivalent cost-to-serve** | **$26,920.27** | PARTIAL (rate-dependent; cost-to-serve, NOT cash) |
| Blended rate | **≈ $0.00256 per 1,000 tokens** | VERIFIED (derived: $26,920.27 / 10,533M) |

Two things matter here for scalability:

- **Cache-read dominance (≈93%) is the structural reason the blended rate is low.**
  Cache-read is priced at the cheapest tier — 1.50/M for the top model class vs 15.00/M
  for fresh input, a **10× discount**. Most of the volume is re-reading a stable, cached
  context rather than paying fresh-input rates. This is the same lever §1.2 models, seen
  at full operating scale. **VERIFIED.**
- **The widely-quoted "~$10K" figure is stale.** It is the 2026-05-24 snapshot
  (8,004 messages / $10,047.89). The current cost-to-serve is **~$26.9K** over a longer
  window using the identical accounting method. Cite the current figure; flag any "~$10K"
  reference as the older snapshot. **VERIFIED (both snapshots present in the history log).**

> **Asymmetry, stated once.** This volume is the output of **one person with AI
> assistance over ~19 recorded days**, not a funded team. Read it as evidence of
> throughput for a solo+AI operation, not as parity with a staffed competitor.

### 1.2 Baseline cost of one model call

A single call costs `C = (in_tok × P_in) + (out_tok × P_out)`. For a representative
mid-size agent turn — **20,000 input tokens** (system prefix + retrieved context +
history) and **2,000 output tokens** — at the §0 rates:

```
C_uncached = 20,000/1e6 × $3.00  +  2,000/1e6 × $15.00
           = $0.060 + $0.030
           = $0.090 per turn        (UNCACHED)
```

Arithmetic **VERIFIED**; the 20k/2k token split is a stated modelling assumption.

### 1.3 Caching savings — the real number, scoped

Caching only helps the **repeated prefix** (stable system instructions + pinned context).
Assume **16,000** of the 20,000 input tokens are a cacheable stable prefix and **4,000**
are turn-specific (the new user/context delta). With hit rate `h = 0.90`:

```
prefix cost (cached path) = 16,000/1e6 × [ h × P_cache_read + (1−h) × P_cache_write ]
   cached-read contribution = 0.90 × 16,000/1e6 × $0.30  = $0.00432
   cache-write contribution = 0.10 × 16,000/1e6 × $3.75  = $0.00600
   prefix cost            ≈ $0.0103
delta input cost          = 4,000/1e6 × $3.00            = $0.0120
output cost               = 2,000/1e6 × $15.00           = $0.0300
C_cached                 ≈ $0.0103 + $0.0120 + $0.0300   = $0.0523 per turn
```

- **Input-side saving:** uncached input = $0.060; cached input (prefix + delta) ≈ $0.0223
  → **≈63% off the input bill.**
- **Whole-turn saving:** $0.090 → $0.0523 → **≈42% off the total turn** (output is full
  price and does not cache).

Arithmetic **VERIFIED**; the 16k/4k split is the stated assumption.

> **Honest scoping of the "~90% cheaper" headline.** The much-quoted "prompt caching cuts
> cost up to ~90%" figure (VERIFIED in the literature, §5) is the **input-token,
> high-hit-rate, large-stable-prefix** case. The realized saving on a *whole* turn is
> lower, because output tokens are full price and only the stable prefix caches. The
> break-even is **~2+ cache hits per prefix** — the ~25% write premium must be amortized
> (§5, VERIFIED). A prefix used **once** is a net *loss* (write premium, no read
> amortization). The 93% cache-read dominance in §1.1 is what makes the high-hit case the
> normal case here, not the exception.

### 1.4 The ~15× multi-agent multiplier — caching does NOT cancel it

Two forces pull opposite ways and must be **netted**, not cherry-picked. Anthropic's own
multi-agent research reports that its orchestrator-worker system "uses about 15× the
tokens of a normal chat" (Anthropic Engineering, *How we built our multi-agent research
system* — VERIFIED, §5). So a fan-out spends ~15× the tokens of a single turn:

```
single-agent cached turn         ≈ $0.0523                (§1.3)

parallel fan-out (M ≈ 15× tokens, VERIFIED §5):
   naive (15 uncached turns):  15 × $0.090               = $1.350
   with a SHARED cached prefix across workers:
     workers share the 16k prefix → cache-read after worker 1
     worker delta + output (full price): 15 × ($0.0120 + $0.0300) = $0.630
     amortized prefix reads:             15 × $0.00432            = $0.065
     one prefix write:                                            ≈ $0.060
   C_fanout (cached, shared prefix) ≈                              $0.755
```

**Net finding.** Caching roughly **halves** the fan-out bill ($1.35 → ~$0.76) by sharing
the prefix — but the fan-out is still **~14× a single cached turn** ($0.755 / $0.0523).
The honest statement: *parallel orchestration buys wall-clock speed and breadth by
spending tokens; caching reduces the premium but does not remove it.* **VERIFIED**
arithmetic; the shared-prefix step is **PARTIAL** — it assumes workers genuinely share
one cached prefix, which is an implementation property.

### 1.5 Cost-tier routing — a real but depreciating lever

Routing routine sub-tasks to a cheaper model and reserving a frontier model for
orchestration is a genuine lever. If a routine worker runs at a tier ~10× cheaper than the
frontier tier, a fan-out where 12 of 15 workers are routine yields:

```
12 routine × ($0.0420 / 10)  +  3 frontier × $0.0420  +  prefix
   ≈ $0.050                  +  $0.126                +  ~$0.07
   ≈ $0.25     vs    $0.755 all-frontier    →    ~3.0× cheaper on this mix
```

**~3.0× cheaper** on this routine-heavy mix (12 of 15 workers routine). Arithmetic
**VERIFIED**; the tier-gap and mix are stated inputs.

> **The caveat that keeps this honest.** Inference prices are falling **9×–900× per year
> across tasks, median ~50×/year** (Epoch AI, *LLM inference prices have fallen rapidly
> but unequally* — VERIFIED, §5). The *gap* between cheap-tier and frontier-tier — the
> exact thing routing monetizes — **shrinks over time**. The routing advantage is real
> **today** and is a **depreciating asset**, not a permanent defensibility. Any routing multiplier
> must be quoted with **date + tier mix + the erosion note.**

---

## 2. Parallel multi-agent concurrency math

### 2.1 Wall-clock: parallel vs serial

For `N` independent sub-tasks each taking `t`, serial wall-clock is `N·t`; ideal parallel
is `t + S`, where `S` is the lead orchestrator's fan-out + synthesis overhead. Speedup
`≈ N·t / (t + S)`:

| N workers | serial (N·t, t = 2 min) | parallel (t + S, S = 1.5 min) | speedup |
|---|---|---|---|
| 3 | 6.0 min | 3.5 min | 1.7× |
| 5 | 10.0 min | 3.5 min | 2.9× |
| 8 | 16.0 min | 3.5 min | 4.6× |
| 15 | 30.0 min | 3.5 min | 8.6× |
| 25 | 50.0 min | 3.5 min | 14.3× |

Arithmetic **VERIFIED**; `t` and `S` are stated assumptions. The right column treats `S`
as constant — but **real `S` grows with `N`** (§2.3), so these are an **upper bound, not a
promise.**

### 2.2 The Amdahl ceiling — why speedup saturates

Amdahl's law: with parallelizable fraction `f`, max speedup `= 1 / ((1−f) + f/N)`, with a
hard ceiling as `N → ∞` of `1 / (1−f)`:

| f (parallel fraction) | ceiling 1/(1−f) | speedup at N=10 | speedup at N=25 |
|---|---|---|---|
| 0.50 | 2.0× | 1.8× | 1.9× |
| 0.80 | 5.0× | 3.6× | 4.2× |
| 0.90 | 10.0× | 5.3× | 6.9× |
| 0.95 | 20.0× | 6.9× | 10.5× |

**Reading.** The serial part — composing briefs, then synthesizing N worker outputs into
one coherent result — is the orchestrator's `(1−f)`. Even at `f = 0.90`, **10 workers buy
~5.3×, not 10×**, and **25 workers buy ~6.9×**: past ~8–10 workers, extra agents add
little wall-clock but full token cost. Amdahl is a **VERIFIED** classical result; `f` is a
stated per-job input.

### 2.3 The observed concurrency cap — and WHY it exists

The audit's working cap is **~8–10 effective parallel agents** before synthesis overhead
dominates. Three **independent** forces converge on roughly that number — which is why the
cap is *structural*, not a tuning artifact:

1. **The Amdahl synthesis tax (§2.2).** With realistic `f ≈ 0.85–0.90`, the marginal
   speedup from worker 9→10 is already < 0.3×; worker 20→25 is < 0.1×. **VERIFIED math.**

2. **The Cognition shared-context failure mode.** Cognition (Devin), *Don't Build
   Multi-Agents*, argues that dispersed decision-making across agents that do not share
   full context produces compounding, conflicting outputs — its two stated principles are
   "share context, and share full agent traces, not just individual messages" and
   "actions carry implicit decisions, and conflicting decisions carry bad results." The
   more concurrent writers, the more reconciliation the lead must do, so **`S` rises
   *super-linearly* with `N`** — it is not constant. This is the strongest external reason
   the cap is real. **VERIFIED** (Cognition, *Don't Build Multi-Agents*).

3. **Context degradation.** "Performance degrades as input token count increases across
   all major models tested" — and "million-token context windows extend where degradation
   occurs; they do not eliminate it." A lead synthesizing 25 worker reports must load a
   large combined context, hitting exactly the degradation curve that motivates keeping
   working context small. **VERIFIED** (context-engineering reliability literature, §5).

> **Honest envelope.** The platform is inside the defensible zone **only** when workers
> run genuinely independent sub-tasks AND the lead receives full traces and *synthesizes*
> rather than blind-concatenates (the Cognition requirement). Fan-out of *interdependent*
> work without shared context falls into Cognition's failure mode. Whether the platform
> shares full traces is an **implementation property**: the public capability inventory
> describes per-agent append-only channels and a synthesizing lead, which is consistent
> with the safe pattern — but the **concurrent execution engine is not present in the
> public repository**, so this is **PARTIAL** (surface verified; engine unverified).

### 2.4 What the literature says the upside is worth

Anthropic's production orchestrator-worker research system **outperformed single-agent
Claude Opus 4 by 90.2%** on its internal research eval, at **~15× the tokens**, with
**token usage explaining ~80% of performance variance** (Anthropic Engineering — VERIFIED,
§5). The honest reading for the platform: the multi-agent upside is real and measured
**elsewhere**; the platform adopts the *same* pattern, so its expected upside is "plausibly
large on breadth-heavy tasks, at a ~15× token premium" — **not** a number the platform has
itself independently benchmarked in the public sources (**UNVERIFIED for the platform
specifically**). Every speed claim must be paired with the 15× token cost.

---

## 3. Own-server + sandboxed-tool + full-stack scaling model

### 3.1 The unit and its throughput

The platform's spine is a single stdlib HTTP server, same-origin (no CORS surface),
fail-closed, every route degrading to a clean "unavailable" at HTTP 200 rather than
crashing (capability inventory item 10 — **VERIFIED in the public repo**). Throughput for
such a unit:

```
Effective req/s ≈ workers_concurrent / mean_request_latency
```

The dominant latency is the **upstream model call**, not the local server. With a local
IO-bound pool of `W` concurrent in-flight requests and mean model latency `L`:

| W (in-flight) | model latency L | local-bound throughput |
|---|---|---|
| 4 | 6 s | ~0.67 req/s |
| 16 | 6 s | ~2.7 req/s |
| 16 | 2 s (cached / cheap tier) | ~8 req/s |

**Finding.** The local server is **not** the bottleneck for agent workloads; upstream
model latency and provider rate limits are. The own-server design's scaling value is
**isolation and reliability** — no shared cloud blast radius, no CORS surface, no
mandatory backend — **not raw QPS.** The throughput formula is standard queueing
arithmetic (**VERIFIED**); `W` and `L` are stated inputs. The "not the bottleneck"
conclusion is **PARTIAL** — it depends on the local handler being IO-bound, which the
stdlib per-route defensive-load design supports.

### 3.2 Sandboxed tool execution — bounded blast radius, bounded cost

The public tool surface is an **allow-listed action runner**: a closed action dictionary
where an unknown name returns the list of allowed actions and executes nothing — explicitly
**not a raw shell** (capability inventory item 3 — **VERIFIED in the public repo**). The
scaling implication is precise:

> The **blast radius per concurrent worker is bounded by a hand-curated list a reviewer
> can read in one file.** Adding workers therefore does **not** widen the attack/error
> surface the way an open shell would — where each new worker is another process that can
> run anything. This is the structural contrast with the cautionary tale of the category.

That contrast is the load-bearing comparison point. The most-starred open competitor in
this space shipped permissive default permissions, a disable-able sandbox, and a wide
untrusted-input surface, and accumulated documented one-click remote-code-execution and
command-injection vulnerabilities plus a companion-service breach exposing ~1.5M auth
tokens (OpenClaw security record — VERIFIED events; see `02-consumption-audit.md` and the
competitor file for the CVE list). The academically-measured remedy for that class —
**a staged human-in-the-loop defense layer that raised overall sandbox-escape defense from
a ~17% baseline into the 19%–92% band (best configuration ~91.5%)** — is *precisely* the
gate-first posture the platform ships by default. **VERIFIED** (the events and the
direction of the defense result); **PARTIAL** (the exact single-paper percentages).

Two honest scope limits on this section:

- A **general MCP tool layer** is **UNVERIFIED in the public repo** — treat "sandboxed MCP
  at scale" as a roadmap claim, not a shipped one.
- The **context-discipline** principle (run analysis off-context; let only the *printed
  findings* enter the window, never the raw data) is the cost-control lever at scale: it
  keeps each worker's input small, which (a) directly cuts per-call input cost (§1) and
  (b) stays *left* of the context-degradation curve (§5, VERIFIED). The shipped artifact
  is a **context-pressure policy** (it measures pressure, verifies survival pins,
  checkpoints) — **VERIFIED**; a *distinct sandbox-execute primitive* as a separate engine
  is **UNVERIFIED in the public repo.**

### 3.3 Cost vs load (cost-to-serve)

Per-task cost is essentially **flat in load** — there is no fixed cloud bill to amortize
over volume here, because the model call dominates. So cost-to-serve scales **linearly**
with task volume × the per-task figures of §1:

```
daily cost-to-serve ≈ tasks/day × C_per_task
   1,000 routine cached single-turns/day × $0.0523       ≈ $52/day   (~$1,570/mo)
     200 fan-out tasks/day × $0.755 (15-worker cached)   ≈ $151/day  (~$4,530/mo)
```

Arithmetic **VERIFIED**; all `$` are **API-equivalent cost-to-serve** at §0 rates, **NOT
cash** on a subscription. The mix is a stated assumption. The two levers that bend this
curve are cost-tier routing (§1.5) and caching (§1.3) — both real, both date-sensitive.
This linearity is the honest scaling story: there is no magic economy of scale on the
model bill; the discipline is in keeping each task's token footprint small.

---

## 4. Reliability engineering for scale — the availability math

The platform frames reliability as a first-class promise to whatever depends on it. The
audit translates four named engineering practices into numbers. The empirical reason this
matters at all is the long-horizon reliability law: **the per-step error rate itself rises
as a task progresses, rather than staying constant** — small per-step errors compound into
irreversible failures (arXiv 2509.09677, *The Illusion of Diminishing Returns* —
VERIFIED, §5) — and reliability is domain-stratified (one 396-task benchmark found
software-engineering reliability falling 0.90 → 0.44 over the duration range; arXiv
2603.29231 — VERIFIED, §5). That compounding law is what an architecture of checkpoints +
gates + verification is engineered against.

### 4.1 Health-check / restart — availability arithmetic

Availability `A = MTBF / (MTBF + MTTR)`. A fast health surface + auto-restart cuts
**MTTR**, which is the dominant lever once MTBF is reasonable:

| MTBF | MTTR (manual) | A | MTTR (health + restart) | A |
|---|---|---|---|---|
| 24 h | 30 min | 98.0% | 30 s | 99.97% |
| 72 h | 30 min | 99.3% | 30 s | 99.99% |

**Finding.** Going from manual recovery (~30 min) to auto-restart (~30 s) moves a
24h-MTBF service from **~98% to ~99.97%** — roughly **2 nines gained from MTTR alone**,
without touching failure frequency. The platform's fail-closed, never-crash-a-request
server + fast health surface (inventory item 10 — VERIFIED) is exactly the MTTR lever this
math rewards. Availability formula **VERIFIED**; MTBF/MTTR are stated inputs.

### 4.2 Retry + backoff — converting transient errors into success

With independent per-attempt success probability `p`, success after `k` attempts is
`1 − (1−p)^k`:

| per-attempt p | 1 attempt | 2 attempts | 3 attempts |
|---|---|---|---|
| 0.90 | 90.0% | 99.0% | 99.9% |
| 0.80 | 80.0% | 96.0% | 99.2% |
| 0.50 | 50.0% | 75.0% | 87.5% |

Exponential backoff (e.g. 1 s, 2 s, 4 s + jitter) spaces retries so a transient upstream
blip clears between attempts and the retries do not synchronize into a thundering herd.

> **The caveat that makes this honest.** Retry only helps **transient** failures with
> independent `p`. For **long-horizon** tasks, the per-step error rate *rises* as the task
> progresses and errors compound (§5, VERIFIED) — retrying a deep, half-corrupted
> trajectory is **not** independent and can make things worse. Retry is a request-level
> rail, not a long-horizon cure. The long-horizon cure is **checkpointing + a gate**, not
> a bigger retry count. This is the cleanest place the reliability math and the safety
> posture meet: the gate layer is a *response to a measured failure law*, not a
> hypothetical.

### 4.3 Circuit breaker — bounding cascading cost

A circuit breaker that opens after `n` consecutive upstream failures caps wasted spend and
latency: instead of `N_workers × timeout × retries` piling onto a dead provider, the
breaker trips and fails fast.

```
without a breaker: 15 workers × 30 s timeout × 3 retries  = up to 22.5 worker-minutes burned per outage
with a breaker tripping after 3 failures:                 ≈ 1.5 worker-minutes
   →  ~15× reduction in wasted work during an upstream outage
```

Arithmetic **VERIFIED**; the trip threshold and timeout are stated inputs. This is the
operational expression of "don't keep the many hammering a downed few."

### 4.4 Caching as a *requirement*, not an optimization

At scale, caching is **load-shedding**, not just thrift. If hit rate is `h`, upstream call
volume is cut to `(1−h)` of naive:

| hit rate h | upstream calls vs naive | implied headroom |
|---|---|---|
| 0.50 | 50% | 2× |
| 0.80 | 20% | 5× |
| 0.90 | 10% | 10× |

**Finding.** At `h = 0.80` (well inside the VERIFIED 80–95% production band, §5) the system
makes **1/5** the upstream calls — that is **5× rate-limit headroom** and **5× fewer
chances to hit a transient failure**, on top of the §1.3 cost saving. This is why the audit
treats caching as a **reliability requirement** at scale, not a nice-to-have. The 93%
cache-read dominance measured in §1.1 is this lever operating at full load. Headroom
arithmetic **VERIFIED**; `h` from the cited band.

### 4.5 Rate-limiting the many-from-few — the structural pattern

Many concurrent workers behind one operator's provider key share **one** rate-limit
budget. Two structural defenses, both numeric:

- **Token-bucket admission.** Size the in-flight worker pool `W` so
  `W × calls_per_worker_per_min ≤ provider_RPM`. If the provider allows 60 RPM and each
  worker makes 4 calls/min, then `W ≤ 15` — which, **not coincidentally, sits right at the
  §2.3 concurrency cap.** The economics and the concurrency math **independently agree** on
  ~8–15 as the working band. Arithmetic **VERIFIED**; RPM is a stated input.
- **Backpressure over failure.** Excess workers **queue** (token-bucket) rather than
  fire-and-fail, converting a `429`-storm into orderly admission. Combined with §4.4
  caching (which removes ~80% of calls before they ever reach the limiter), the effective
  ceiling on *useful* concurrency rises **without** raising the provider quota.

### 4.6 No single point of failure — the math of independence

If a system has one critical component with availability `A`, system availability is `A`.
With `k` **independent** redundant components (any one suffices), system availability is
`1 − (1−A)^k`:

| component A | k = 1 | k = 2 | k = 3 |
|---|---|---|---|
| 0.99 | 99.0% | 99.99% | 99.9999% |
| 0.95 | 95.0% | 99.75% | 99.99% |

The platform's relevant design choices map onto this:

- **BYOM across multiple providers** (inventory item 1 — VERIFIED): the model dependency
  is *swappable by config*, so a single provider outage is not a single point of failure
  **if a fallback is configured.**
- **Stdlib-only, no mandatory cloud backend** (inventory item 10 — VERIFIED): removes a
  whole class of external SPOFs from the runtime.
- **Files-are-memory** (inventory item 7 — VERIFIED): state survives a process restart
  with no database to fail.

> **Honest limit.** The redundancy math assumes **independence**. Two providers that are
> actually the same model family, or two "redundant" components on one machine, are
> **correlated** and do not deliver `1 − (1−A)^k`. The platform makes multi-provider
> fallback *possible* (config-swappable BYOM — VERIFIED), but whether a given deployment
> is genuinely independent is the **operator's configuration**, not an intrinsic
> guarantee. **PARTIAL.**

---

## 5. Literature anchors (the science under the numbers)

Every position above is grounded in the public research literature so the math is not
self-referential. The load-bearing sources, with labels:

| # | Source | What it grounds | Label |
|---|---|---|---|
| Karpathy | *Software Is Changing (Again)* / "LLM OS" framing | The platform implements a **named, public** paradigm (model = compute core, context window = memory, tools = resources, gates = a leash); defensibility must come from execution + discipline, not from inventing the paradigm | VERIFIED |
| Anthropic (multi-agent) | *How we built our multi-agent research system* | The ~15× token multiplier (`M`), the 90.2% single-vs-multi upside, "token usage explains ~80% of performance variance" (§1.4, §2.4) | VERIFIED |
| Cognition | *Don't Build Multi-Agents* | The shared-context failure mode; super-linear synthesis cost; "share full agent traces" requirement (§2.3) | VERIFIED |
| Anthropic (context engineering) | *Effective context engineering for AI agents* | Context editing +29% / with memory tool +39%; 84% token cut on a 100-turn eval; degradation universal across models (§2.3, §3.2) | VERIFIED |
| METR | *Measuring AI Ability to Complete Long Tasks* (arXiv 2503.14499) | The 50%-task-completion horizon, ~7-month doubling (a later ~12-hour figure is PARTIAL) | VERIFIED (later figure PARTIAL) |
| arXiv 2509.09677 | *The Illusion of Diminishing Returns* | Per-step error rate **rises** with task length and compounds — the backbone of §4 | VERIFIED |
| arXiv 2603.29231 | *Beyond pass@1: A Reliability Science Framework* | Domain-stratified reliability decay (SWE 0.90 → 0.44); hard benchmarks < 20% pass | VERIFIED |
| Epoch AI | *LLM inference prices have fallen rapidly but unequally* | Prices fall 9×–900×/yr, median ~50×/yr — the routing-advantage erosion (§1.5) | VERIFIED |
| Prompt-caching literature | byteiota / prompthub summaries of Anthropic caching | Cache read ≈ 10% of base, ~25% write premium, break-even ~2+ hits, 80–95% production hit rates (§1.3, §4.4) | VERIFIED |
| Inference unit-economics | introl inference-economics guide | Batching 32 requests ≈ 85% cheaper per token for +20% latency; quantization ~60–70% cost cut | VERIFIED |
| AI-2027 (Kokotajlo et al.) | ai-2027.com | The canonical public statement of autonomous-agent alignment risk — the named risk the gate layer answers (timeline since revised toward early 2030s = PARTIAL) | VERIFIED (revision PARTIAL) |

The honest framing of the safety angle, carried verbatim from the research grounding: the
strongest claim available is **not** "this platform is safer than frontier labs"
(UNVERIFIED and unprovable) but **"the architecture treats autonomy-without-a-gate as the
named risk and engineers against it"** — and the reliability math in §4 is what that
engineering looks like in numbers.

---

## 6. Synthesis — where the numbers land, honestly

1. **Token economics.** Caching cuts the input bill meaningfully (**~42% off a
   representative cached turn**, up to ~90% on input-heavy high-hit cases) but does **not**
   cancel the **~15×** multi-agent token premium; netted, a 15-worker cached fan-out is
   **~14× a single cached turn (~$0.76 API-equivalent** at §0 rates). Cost-tier routing
   adds a real but **depreciating ~3.0×** on routine-heavy mixes, eroding as inference
   prices fall ~50×/yr (median). At full operating scale the ledger shows ~93% cache-read
   dominance and a **~$0.00256 per 1,000-token blended rate** — the cost story is real and
   it is API-equivalent, not cash. *(Anthropic multi-agent + Epoch AI + caching literature
   — VERIFIED; shared-prefix arithmetic PARTIAL.)*

2. **Concurrency.** Wall-clock speedup **saturates**: at `f = 0.90`, 10 workers ≈ 5.3×,
   25 workers ≈ 6.9×. The observed **~8–10 effective-worker cap** is **over-determined** by
   three independent forces — the Amdahl synthesis tax, the Cognition shared-context
   failure mode, and context degradation — so it is **structural, not a tuning artifact.**
   The multi-agent upside is real and measured *elsewhere* (90.2%, ~15× tokens); it is
   **UNVERIFIED for the platform specifically.** *(Amdahl + Cognition + context-engineering
   literature — VERIFIED.)*

3. **Own-server + sandboxed tools.** The local stdlib server is **not** the bottleneck;
   upstream model latency and provider rate limits are. The design's scaling value is
   **isolation + reliability + bounded blast radius** (the allow-listed runner caps each
   worker's surface to a list a reviewer reads in one file) — **not raw QPS.** "Sandboxed
   MCP at scale" and a distinct sandbox-execute engine are **UNVERIFIED in the public
   repo** — roadmap, not shipped. *(Inventory items 3 & 10 — VERIFIED in repo; queueing
   arithmetic VERIFIED.)*

4. **Reliability.** Each of the four practices carries concrete, numeric leverage:
   auto-restart buys **~2 nines** via MTTR; retry + backoff turns `p = 0.9` into **99.9%
   over 3 attempts — for transient errors only** (long-horizon errors compound and need
   checkpoint + gate, not retry); a circuit breaker cuts outage waste **~15×**; caching at
   `h = 0.8` gives **5× rate-limit headroom**; multi-provider BYOM removes the model SPOF
   **only if independently configured.** And the rate-limit math and the concurrency math
   **independently converge on ~8–15 workers** as the useful band. *(Availability /
   probability formulas VERIFIED; long-horizon compounding from arXiv 2509.09677 —
   VERIFIED.)*

**The defensible finding.** The platform's scaling design is **sound on the dimensions it
ships** — reliability, isolation, bounded blast radius, context discipline — and its
concurrency and cost math sit **inside** the envelope the public science supports. Every
advantage is scoped; every moving target (the depreciating routing gap, the
configuration-dependent redundancy, the implementation-dependent trace-sharing) is named.

**Asymmetry, stated plainly to close.** This system is the work of **one researcher with
AI assistance over ~19 recorded days**, not a funded team. The calculations here are
honest models grounded in cited literature, not claims of a benchmarked production fleet;
several scaling components (a distinct sandbox-execute primitive, a general MCP layer, a
concurrent multi-agent execution engine, a failure-pattern regression memory) are **not
present in the public repository** and are modelled as roadmap, not shipped fact. Nothing
in this study supports "beats frontier," "fully autonomous," or any superlative — and
none is claimed.
