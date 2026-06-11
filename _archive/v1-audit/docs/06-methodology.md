# Methodology — Built With Claude

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## How to read this document

This document audits one narrow, often-skipped question: **how was the system under
review (the "SUR" or "the platform") actually built — and specifically, how was code
that was written by an AI model held to a standard worth trusting?** Most product
materials describe what a system *does*. Far fewer disclose *how it was constructed*,
and fewer still disclose that the construction itself leaned heavily on large language
models. That disclosure is the subject here.

Three rails run through every section, identical to the rest of this audit:

1. **Every non-trivial claim is labeled** **VERIFIED** / **PARTIAL** / **UNVERIFIED.**
   VERIFIED = the cited source, the on-disk artifact, or the arithmetic states it
   directly. PARTIAL = real and well-supported, but one verification step (a live run,
   a clean-checkout reproduction, a line-by-line diff) was not performed in this pass.
   UNVERIFIED = described or projected, not independently confirmable from the materials
   examined.
2. **Cost figures are API-equivalent cost-to-serve, NOT cash.** Where dollar figures
   appear, they are token counts multiplied by published per-token list rates — "what
   this volume *would* cost a buyer on metered API access." The platform was operated
   largely on a flat-rate subscription, so the figure is a cost-basis, not money that
   left a bank account. [*Source: `metrics.md` §1, caveat 1.*]
3. **The asymmetry is stated plainly, once.** This system is the work of one researcher
   with AI assistance over roughly nineteen recorded days, not a funded engineering
   team. That makes the throughput notable for a solo+AI operation and makes the
   un-finished edges expected. Competitor maturity, where it appears, is a roadmap to
   learn from, not a deficit to spin. [*Source: `_DIGEST.md` §8.1; `metrics.md` §0,
   caveat 2.*]

A terminology note carried from the consumption audit (`02-consumption-audit.md`): the
platform's relationship to open source is **consumption** — it consumes patterns one-way
into its own architecture and re-implements them in its own owned framework. It is not a
"harness" and it does not "harness" anything; the word *harness* below describes only the
generic class of competing tools, for contrast.

A scope boundary specific to this document: the audit does **not** claim to have
reverse-engineered the platform's private build method. That method is deliberately
withheld by the operator (see the consumption audit's "consume freely; publish a
verifiable shell; never publish the method" finding — `consumption.md` §5). What this
document describes is the *generic engineering practice* observable from the published
artifacts and the disclosed build records: the human-plus-AI loop, the discipline applied
to AI-written code, the verification habits, and the deterministic-versus-reasoned split.
The specifics of how the orchestration is composed are out of scope and are not revealed
here. [*Source: `consumption.md` §5; `_DIGEST.md` §7.*]

---

## The alignment frame this methodology answers to

One reason a build-methodology audit matters at all is that the public AI-safety literature
now names, explicitly, the failure class an autonomous agent system most needs to engineer
against. **AI 2027** — the scenario forecast from the AI Futures Project (Daniel Kokotajlo
and colleagues), published April 2025 — is the canonical public statement of
*autonomous-agent alignment risk*: systems that act over long horizons, improve themselves,
and take irreversible actions faster than a human can supervise them.
([AI 2027 — about](https://ai-2027.com/about); [project site](https://ai-2027.com)) —
**VERIFIED** (the project's own timeline has since been
[revised toward the early 2030s](https://www.hungarianconservative.com/articles/tech/ai-futures-project-ai-2027-apocalypse-timeline-superintelligence-daniel-kokotajlo/) — **PARTIAL**).

The honest framing — the one this audit can defend and the one this methodology section
exists to evidence — is **not** "the SUR is safer than frontier labs." That claim is
unprovable and is **UNVERIFIED** by construction; the audit makes it nowhere. The
defensible framing is narrower and stronger: **the SUR's methodology treats
autonomy-without-a-gate as the named risk and engineers against it by default.** Concretely,
the build process the rest of this document audits is *honest-by-design*: every irreversible
or outward action is composed through a mechanical, fail-closed, human-in-the-loop gate
(autonomy level × risk score → act / report / queue); AI-written code is held to a per-step
verification standard rather than trusted on output; and the audit trail is append-only.
These are not marketing postures — they are the methodology's direct response to a
*measured* failure law. The reliability science is independent and unambiguous on this
point: per-step error rates **rise** as a task progresses and compound into irreversible
failures ([arXiv 2509.09677](https://arxiv.org/abs/2509.09677);
[arXiv 2603.29231](https://arxiv.org/abs/2603.29231)), and the upside of multi-agent
parallelism comes with a documented fragility when context is not shared across agents
([Cognition, *Don't Build Multi-Agents*](https://cognition.ai/blog/dont-build-multi-agents)).
An architecture that externalizes memory, verifies each step, and gates the irreversible is
responding to that law — which is precisely why a methodology that bakes the gate into the
build loop, rather than bolting it on afterward, is the part worth auditing. (See
[References](./REFERENCES.md) for full sources.) — **VERIFIED** (framing); the SUR's *own*
gate-coverage completeness is examined in docs 03/08 and is **PARTIAL** there, not assumed
here.

---

## 1. The honest premise: this was built with AI, and says so

The most important methodological fact about the SUR is one many products would bury: it
was **written predominantly by large language models, under human direction.** The named
researcher and author is **Haris Mekic**; the lead author and engineer of the code and
the documents is **Claude Opus 4.8**, with **Claude Sonnet**, **OpenAI GPT**, and
**Google Gemini** used for cross-checks. This is stated in the header of every artifact
in the audited pack and is not framed as an embarrassment to be minimized. [*Source: the
header line on each of `capabilities.md`, `consumption.md`, `metrics.md`, and the
companion docs; `_DIGEST.md` lines 12–14.* — **VERIFIED.**]

For an auditor, AI-assisted authorship is neither a virtue nor a defect on its own. It
is a **risk profile** — a specific, well-documented set of failure modes that must be
engineered against:

- **Fabrication / hallucination.** A model can produce confident, well-formed code or
  prose that references functions, files, or facts that do not exist.
- **Silent drift.** Across many iterations, a model can quietly broaden scope, change a
  constant, or weaken a check while appearing to "just edit."
- **Stale or guessed context.** A model can edit a file using a remembered version
  rather than the current one, corrupting it without any error firing.
- **Plausible-but-wrong reasoning.** A model can choose an approach that compiles and
  reads well but is structurally incorrect for the task.

The methodological question is therefore not "did a human or an AI write this?" but
**"what mechanical and procedural discipline was placed between the AI's output and the
shipped artifact?"** The remainder of this document answers that. The short version: the
SUR's build practice treats AI-written code as **untrusted input that must pass gates**,
not as finished work — a stance directly continuous with the product's own runtime
philosophy of gating autonomous actions (see capabilities §5–§6, `03-capabilities.md`).
[*Source: `capabilities.md` §5–§6; `consumption.md` §2.* — **PARTIAL** (the continuity is
the auditor's structural reading of two verified layers).]

---

## 2. The human-plus-AI build loop

### 2.1 The shape of the loop

The platform records its construction history as a **numbered sequence of
build-and-verify iterations** — each iteration is a change, a self-test step, and a
logged outcome. The highest iteration index referenced in the internal records is in the
**~260 range.** [*Source: `metrics.md` §3.* — **PARTIAL** (internal log; an upper-bound
index, not a guarantee that every index 0..260 is an independently reproducible event).]

The observable loop, reconstructed from the disclosed records and the published
repository, has a consistent shape:

| Step | Actor | What happens |
|---|---|---|
| 1. Direction | Human (Haris Mekic) | Sets the goal, the scope boundary, and the acceptance bar for the iteration. |
| 2. Generation | AI (Claude Opus 4.8, lead) | Drafts the code, the script, or the document for that scoped change. |
| 3. Cross-check | AI (Sonnet / GPT / Gemini) | A different model reviews or stress-tests the draft where used. |
| 4. Verification | Deterministic script + human | A self-test runs; the human inspects the result against the acceptance bar. |
| 5. Decision | Human + mechanical gate | Keep, revise, or revert — never "ship because it looked done." |
| 6. Logging | System | The change and its pass/fail outcome are appended to the build record. |

The load-bearing property is **step 4 before step 5**: a verification step is paired
with each build step rather than deferred to the end. Sampling of the internal log shows
iterations "routinely paired with a pass/fail self-test line." [*Source: `metrics.md` §3,
"Iterations cited with an in-line self-test result."* — **PARTIAL** (the *practice* of
pairing is evident and consistent in the sampled records; the exact total of fully
reproducible iterations was not independently counted).]

> **Auditor reading.** The honest reading the source itself states is the right one: the
> *practice* of pairing each build step with a verification step is evident and
> consistent in the sampled records, but the full count of independently reproducible
> iterations was not audited. The discipline is demonstrated; the exhaustive census is
> not. [*Source: `metrics.md` §3 closing note.*]

### 2.2 Why multiple models

Using more than one model family is not redundancy theater; it is a deliberate
**de-correlation** strategy: a reviewer too similar to the author shares the author's blind
spots, while a reviewer from a different lineage catches what the author and a like-minded
checker both miss. The build practice operationalizes this by routing cross-checks (step 3
above) through Sonnet, GPT, and Gemini rather than only re-asking the lead model. [*Source:
header lines naming the four models.* — **PARTIAL** (the four models are named as used;
per-iteration cross-check routing is not exhaustively logged in the public pack).]

The verifiable form of "did the multi-model discipline actually hold the line?" is not an
internal transcript — it is the **public reproducibility harness** (`scripts/verify_all.py`,
8/8 PASS, exit 0). That harness lets any reviewer execute the audit's load-bearing safety
properties on the published code without trusting any model's word, including the lead's.
The harness is the externally-checkable artifact this methodology stands on; the per-review
internal cross-check records are not bundled and are not relied on here. [*Source:
`scripts/verify_all.py`; `metrics.md` §5.* — **VERIFIED** (executable on the public repo).]

> **Honesty rail.** This does **not** mean the system is "safe" or "verified beyond
> doubt." An 8/8 harness PASS proves *those eight public properties hold on the published
> code*, not a general guarantee. The multi-model loop reduces within-family blind spots; it
> is not a substitute for independent human review. [*Source: `metrics.md` §5 honesty
> limit.*]

---

## 3. The discipline applied to AI-written code

This is the core of the methodology and the part most directly relevant to a buyer
evaluating AI-built software. The SUR's build practice places **mechanical gates**
between AI output and the codebase. These are not prompt instructions ("please be
careful"); they are runnable checks with explicit pass/fail outcomes. The consumption
audit confirms several of these were themselves **consumed as patterns** from open
research and re-implemented in the platform's own Python standard-library stack.
[*Source: `consumption.md` §4.2–§4.6.* — **VERIFIED** (patterns present on disk with
their own scripts and recorded smoke-tests).]

### 3.1 The edit-safety stack

The most coherent example is a four-layer **edit-safety stack** assembled from consumed
patterns, each a guard against a distinct way AI-written edits go wrong:

| Layer | Guard | Failure mode it catches | Pattern source |
|---|---|---|---|
| Prevention | Read-before-edit invariant | An edit whose target text was drawn from the model's *memory* rather than from a current read of the file | A code-intelligence "lens" module (Pi.dev ecosystem); re-implemented in stdlib Python |
| Prevention | Symbol-boundary-aware edit | An edit that lands mid-statement or cuts a decorator because the model guessed the symbol's extent | A read-expansion module from the same lens; re-implemented using Python's stdlib AST parser |
| Prevention | Pre-commit syntax gate | An edit that introduces a *new* syntax error — checked before it lands, auto-reverted if it does | Agent-computer-interface (ACI) edit-safety pattern from **SWE-agent (MIT)** |
| Recovery | Seven-class failure classifier | A failed edit retried blindly instead of diagnosed and routed to the correct fix | Structured diagnostic-logger pattern from the same lens |

[*Source: `consumption.md` §4.2–§4.4 and the "edit-safety stack" synthesis.* —
**VERIFIED** (all four capabilities present and interlinked; each carries a recorded
smoke-test — 4/4 or 8/8 — in the findings ledger).]

The significance for AI-built code is direct. Two of the four layers (read-before-edit,
symbol-boundary-aware edit) exist **specifically** because a language model editing files
will, sooner or later, edit a stale or misremembered version and corrupt it silently —
no exception is raised, the file is simply wrong. Mechanizing the guard converts a silent
corruption class into a caught, fail-closed event. This is the AI-code analogue of the
product's runtime gate philosophy: *do not trust the autonomous actor on the actions that
bite.* [*Source: `consumption.md` §4.2–§4.4; `capabilities.md` §5.* — **VERIFIED** for
the mechanism; the analogy is the auditor's structural reading.]

### 3.2 Trajectory evaluation, not just output

A second consumed discipline grades an agent's **tool-call path** (the trajectory it
took), not only its final answer — with strict / unordered / subset match modes. It was
re-implemented in the Python standard library from the open **agentevals (MIT)** library.
[*Source: `consumption.md` §4.5.* — **VERIFIED** (capability + stdlib scorer present, 5/5
smoke-test recorded; the findings credit agentevals as the pattern source).]

Why this matters methodologically: a large fraction of agent failures are invisible if
you grade only the final output, because the agent can reach a plausible-looking answer
by a wrong path that will not generalize. Grading the path closes that blind spot. For a
system whose code is written by agents, evaluating *how* an iteration arrived at a result
is a stricter bar than evaluating *whether* the result looks right. [*Source:
`consumption.md` §4.5.*]

### 3.3 Gating dangerous operations at construction time

The build practice also mechanizes a **pre-execution gate that blocks dangerous
version-control commands before they run**, alongside a structured phase-locking
discipline (each phase has explicit entry conditions, exit criteria, and a checkpoint
artifact; the next phase verifies the previous phase's artifact before opening). Both were
consumed pattern-only from a permission-gate extension cluster in the coding-agent harness
ecosystem. [*Source: `consumption.md` §4.6.* — **VERIFIED** (phase-lock discipline
present; the dangerous-command gate present with recorded bite-tests; the source cluster
is named in the findings).]

The point is that an AI agent operating on a repository can, with one over-eager command,
do irreversible damage (a forced reset, a destructive clean). A pre-execution gate that
*blocks the command rather than trusting the agent not to issue it* is the same
construction-by-safety stance applied to the build environment itself. [*Source:
`consumption.md` §4.6.*]

### 3.4 The contributor rules as a soft layer

The published repository's own contributor rules forbid weakening the safety layers — no
raw shell, no weakening the gates, no hardcoded paths, no hardcoded secrets. [*Source:
`capabilities.md` §6, citing `AGENTS.md` "things to avoid."* — **VERIFIED** (read in the
public repo's contributor file).]

> **Auditor caution.** These rules are a **soft** layer — a written norm an AI agent or
> human contributor is asked to honor — that *complements but does not replace* the hard,
> server-side mechanical enforcement (the allow-listed action runner, the autonomy band
> that cannot auto-cross a hard gate, the append-only gate audit, the byte-exact revert
> loop). The source is explicit about this distinction, and an honest methodology must
> keep it: the credible safety property is the mechanical one; the contributor rule is a
> reinforcing convention. [*Source: `capabilities.md` §6 "Why it matters" note.*]

---

## 4. Verification practice

### 4.1 The quality-gated retention loop (the safety rail for unattended improvement)

The single most important verification mechanism for AI-written, self-modifying code is
the **quality-gated retention loop**, and it ships in the public repository. A change to
the system is **KEPT only if a metric suite does not degrade**; otherwise it is
**auto-reverted byte-exact** to the baseline, with the revert sha256-verified against the
original snapshot. It is **fail-closed**: if any metric fails even to *run* at
decide-time, the change reverts; a run can be decided only once; every decision is
appended to an audit. [*Source: `capabilities.md` §9, citing `retention.py` docstring and
routes `/api/retention`, `/api/retention-decide`.* — **VERIFIED** (retention loop present
and inspectable in the public repo).]

This is the mechanism that makes "let an AI improve the system unattended" a defensible
claim rather than a hopeful one. The flow is concrete: `baseline(targets)` takes byte
copies and records baseline metric scores → the loop (a job, a scheduler, or a human)
edits the targets → `decide(run_id)` re-runs the *same* metric suite and compares — KEEP
if no gating metric degraded (ties allowed, improvement welcome), REVERT (restore the
snapshot bytes exactly) if any gating metric degraded. [*Source: `capabilities.md` §9.* —
**VERIFIED.**]

> **Scope honesty.** The source is careful to distinguish this from a separate,
> wider-platform concept — a *failure-signature regression memory* (recording known
> failure patterns so they are recognized instantly on recurrence). That named subsystem
> is **NOT present as a distinct module in the public repo.** What is shipped and
> verifiable is the metric-gated KEEP/REVERT retention loop above. An auditor must not
> conflate the two. [*Source: `capabilities.md` §9, "Relation to a failure-pattern
> regression memory"; `_DIGEST.md` §2, capability 9.* — retention loop **VERIFIED**;
> failure-signature memory **UNVERIFIED in repo**.]

### 4.2 The acceptance-test tallies

The build practice produced several concrete, counted acceptance runs. These are the most
audit-friendly figures in the whole pack because each is a discrete pass/fail tally with
an inspectable mechanism:

| Test surface | Result | Label |
|---|---|---|
| Multi-site generation acceptance (each: spec valid + 4/4 pages + working contact form + export-cleanliness scan + live HTTP 200) | **14/14 PASS** | PARTIAL |
| Quality-evaluation harness: the original five categories (memory recall, capability selection, path resolution, security decision, document generation), deterministic graders, no human-in-the-loop | **5/5 categories at 100%**; the full expanded suite clears its ≥70% gate at **~79%** (failures concentrated in newer framing/discipline categories, not the original five) | PARTIAL |
| Aggregate health smoke-test across subsystems | **26/28** on the current expanded suite (the older "19/19" denominator is a strict subset) | PARTIAL |
| Mechanical safety hooks present + parsing + running | **8/8** (one "firing-but-blind" hook found and fixed in the same pass) | PARTIAL |

[*Source: `metrics.md` §4.* — every row **PARTIAL**: the *mechanisms* (deterministic
acceptance scripts, the re-runnable harness, the hook self-audit) are inspectable, but
most specific runs live in internal logs; full external reproducibility requires running
the bundled tests on a clean checkout.]

Two details in that table are themselves methodology signals worth naming:

- The health smoke-test is reported against its **real, larger denominator (26 of 28 on
  the current expanded suite), not the smaller, older "19/19" subset that would read
  cleaner.** Reporting the honest denominator and the failing checks rather than
  cherry-picking the flattering subset is a disclosure-discipline choice. [*Source:
  `metrics.md` §4.*]
- The hook self-audit found a hook that was **firing but blind** (running but scanning
  nothing) and **fixed it in the same pass** — an error left visible in the record rather
  than concealed. [*Source: `metrics.md` §4; `_DIGEST.md` §3.3.*]

### 4.3 The public claim register (verification of the verification)

The strongest single signal of verification discipline is the pack's own **claim
register**: of **12 publicly-tracked product claims, 4 are labeled VERIFIED, 8 PARTIAL,
0 UNVERIFIED.** Crucially, the four VERIFIED were the ones whose evidence was **actually
run** on the collection date:

1. File-based memory survives a restart.
2. The human-approval gate mechanism functions.
3. BYOM model routing works against a standard-shape stand-in.
4. The deterministic export/redaction gate bites — 3/3 fixtures flagged, zero leaks.

[*Source: `metrics.md` §4 auditor note; `_DIGEST.md` §3.4; `gpt-competitors.md` §1.2.* —
**VERIFIED** (read directly from the pack's claim register and verdict).]

The eight PARTIAL claims were **honestly down-labeled** rather than asserted. For an
auditor, a system that **down-labels its own claims** — reserving VERIFIED for what it
actually ran — is exhibiting the exact verification posture you want from AI-built
software, and it is the opposite of the over-claiming that AI-generated marketing tends
toward. [*Source: `metrics.md` §8, point 4.*]

---

## 5. Deterministic-scripted versus reasoned: the dividing line

A recurring engineering decision in an AI-built system is **what to leave to the model's
reasoning versus what to freeze into a deterministic script.** The SUR's practice draws
this line deliberately, and the line is visible in the published code.

### 5.1 The principle: code over tokens where determinism is possible

The build philosophy treats deterministic logic as **cheaper, faster, and repeatable**
than asking a model to reason it out each time, and pushes anything that *can* be
deterministic into a script. The published artifacts bear this out: the safety-critical
and the countable are scripted, while open-ended judgment is left to the model under a
gate. [*Source: `capabilities.md` throughout (the server modules are pure stdlib Python
scripts); `consumption.md` §3 (the running code is independent stdlib Python, not vendor
TypeScript).* — **VERIFIED** structurally.]

### 5.2 Where the line falls

| Concern | Implementation | Why this side of the line |
|---|---|---|
| The autonomy verdict (act / report / queue) | Deterministic — a small readable function composing level L0–L5 with a 4–20 risk score | A safety verdict must be **identical every time** and **auditable**; reasoning it out per-call would be both slower and non-reproducible. [*`capabilities.md` §5.*] |
| The gate queue | Deterministic — append-only `gate-queue.jsonl`, never rewritten | An audit trail's value is that it **cannot be re-reasoned after the fact.** [*`capabilities.md` §5.*] |
| Quality retention KEEP/REVERT | Deterministic — metric-suite comparison + sha256-verified byte revert | A revert that "decides" via reasoning could rationalize keeping a regression; a byte-exact comparison cannot. [*`capabilities.md` §9.*] |
| The token meter | Deterministic — counts are ground truth (parsed), priced at configured rates | Cost accounting must be **arithmetic, not estimated.** [*`capabilities.md` §8; `metrics.md` §1.*] |
| Edit safety (read-before-edit check, symbol boundary, syntax gate, classifier) | Deterministic — stdlib Python checkers and an AST parser | Catching a stale or malformed edit is a **mechanical invariant**, not a judgment call. [*`consumption.md` §4.2–§4.4.*] |
| The chat conversation itself | Reasoned — routed to the operator's chosen model with one disclosed system line | Open-ended dialogue is exactly the work a language model *should* do. [*`capabilities.md` §1.*] |
| Drafting / synthesis / design | Reasoned — the lead and cross-check models | Generative and analytic judgment is the model's proper domain, **under** the gates above. |

The pattern is consistent and is the methodological heart of the system: **reasoning is
used for what reasoning is good at (open-ended generation and judgment) and is fenced by
deterministic scripts for everything safety-critical, countable, or required to be
reproducible.** The single small (~216-line) BYOM router file — one disclosed system line, no
hidden prompt, a config edit to swap models — is the clean embodiment of "keep the
reasoned surface small and inspectable." [*Source: `capabilities.md` §1, §5, §8, §9;
`consumption.md` §3.* — **VERIFIED** structurally.]

> **Why this is the right line for AI-built software.** The known failure modes of
> AI-written code (§1) all live on the *reasoned* side — fabrication, drift, stale
> context, plausible-but-wrong logic. Moving every safety-critical and countable concern
> to the *deterministic* side removes those failure modes from exactly the places where
> they would do irreversible harm, and confines the model's reasoning to the places where
> a wrong answer is cheap to catch and revert. [*Auditor synthesis of `capabilities.md`
> §1, §5, §9; `metrics.md` §8.*]

---

## 6. The cost and scale of the build itself

For completeness, the build's own resource footprint — every figure API-equivalent
cost-to-serve, not cash:

| Metric | Value | Label |
|---|---|---|
| Total tokens across the build (all four classes) | **~10.53 billion** | VERIFIED (sum of four ledger totals) |
| Recorded messages | **19,333** | VERIFIED |
| Transcript files aggregated | **556** | VERIFIED |
| Span of activity | **2026-05-16 → 2026-06-03 (19 calendar days)** | VERIFIED |
| Cache-read tokens (the dominant term) | **10.07B ≈ 93% of all volume**, priced at the cheapest tier | VERIFIED |
| API-equivalent cost-to-serve | **$26,920.27** | PARTIAL (rate-dependent; cost-to-serve, NOT cash) |
| Blended rate | **≈ $0.00256 per 1,000 tokens** | VERIFIED (derived) |

[*Source: `metrics.md` §1.*]

Two honesty notes the source insists on, carried here verbatim in substance:

- **The widely-quoted "~$10K" figure is stale.** It is the 2026-05-24 snapshot (8,004
  messages / $10,047.89). The current cost-to-serve over the full window is **~$26.9K**.
  Cite the current figure; note the ~$10K is the older snapshot. [*Source: `metrics.md`
  §1c.* — **VERIFIED** (both snapshots present in the history log).]
- **Cache-read dominance is why the blended rate is low.** ~93% of the volume is
  re-reading a cached, stable context at roughly a 10× discount versus fresh input. This
  is a structural property of a long, iterative build session, not a special efficiency
  claim. [*Source: `metrics.md` §1b.* — **VERIFIED.**]

The methodological reading: a ~10.5-billion-token, 19-day, single-operator build is a
**high-throughput AI-assisted construction**, and the cost-to-serve figure is best
understood as the cost-basis a bring-your-own-model buyer would face running the same
volume on metered access — not as cash the operator spent on a subscription. [*Source:
`metrics.md` §0 caveat 1, §8 point 1.*]

---

## 7. Honest limits of this methodology audit

Carried into this document so the deliverable's integrity is visible:

1. **The private build method is not disclosed and was not reverse-engineered.** This
   audit describes the *generic* engineering practice (the loop, the gates, the
   verification, the deterministic/reasoned split). The orchestration intelligence and
   the private prompts are deliberately withheld by the operator and are out of scope.
   [*Source: `consumption.md` §5; `_DIGEST.md` §7.* — by design.]
2. **Most specific build runs live in internal logs.** The acceptance tallies (14/14
   sites; the original-five eval categories at 100% / full-suite ~79% gate-cleared; 26/28
   smoke; 8/8 hooks) and the ~260 iteration index are real and the mechanisms are inspectable,
   but full external reproducibility requires a clean-checkout run of the bundled tests.
   The auditor read the records; the auditor did not re-execute every run this pass.
   [*Source: `metrics.md` §3, §4, §8 point 2.* — **PARTIAL.**]
3. **"No vendor code" is verified structurally, not by a token-level diff.** The
   consumed-pattern build practice keeps vendor source as segregated reference and runs
   independent stdlib Python; a full clean-room diff of every script against every
   reference file was not performed. [*Source: `consumption.md` §7, first bullet.* —
   **PARTIAL.**]
4. **The cross-check routing is named, not exhaustively logged.** The four models are
   verified as *used*; per-iteration cross-check routing is not fully traceable in the
   public pack. [*Source: header lines; `gpt-competitors.md` Part 1.* — **PARTIAL.**]
5. **AI-assisted authorship is a risk profile, not a quality grade.** The gates and
   verification practice described here reduce the known failure modes; they do not
   eliminate them, and a "pass" is scoped to what was tested. [*Source: `metrics.md` §5
   honesty limit.*]
6. **The asymmetry, once more.** One person with AI assistance over ~19 days. The
   discipline is the finding; the breadth of a funded team's verification apparatus
   (large CI suites, coverage gates, a paid QA function) is not present and is not
   claimed. [*Source: `_DIGEST.md` §8.1; `metrics.md` §0 caveat 2.*]

---

## 8. Auditor's net assessment

The methodology survives audit at its stated scope. The system under review is
**AI-built, and honest about it** — the rarer and more trustworthy posture. The build
practice does not ask anyone to trust the AI's output; it places **deterministic,
fail-closed gates between AI output and the shipped artifact**, applies a **multi-model,
de-correlated cross-check** that reduces within-family blind spots, **publishes a stdlib-only
reproducibility harness (`verify_all.py`, 8/8 PASS) so a reviewer can execute the
load-bearing safety properties without trusting any model's word**, **pairs each build step
with a verification step**, and draws a **deliberate line** between what is left to reasoning (open-ended
generation and judgment) and what is frozen into deterministic scripts (everything
safety-critical, countable, or required to be reproducible). The verification posture is
visible in the published code (the byte-exact, fail-closed retention loop) and in the
disclosure discipline (a claim register that reserves VERIFIED for what was actually run
and down-labels the rest).

The honest limits are narrow and named: the private method is withheld by design, most
specific runs live in internal logs pending a clean-checkout reproduction, the "no vendor
code" property is structural rather than diff-proven, and the whole thing is the work of
one researcher with AI assistance — notable for throughput, expected to have un-finished
edges. Nothing in this methodology supports "beats frontier," "fully sovereign," "AGI,"
or any unbacked superlative, and none is claimed. The defensible statement is the precise
one: **this is a disciplined, gate-first, multi-model human-plus-AI build practice that
treats AI-written code as untrusted input and verifies before it trusts.** [*Sources:
`capabilities.md` §1, §5–§9; `consumption.md` §2–§7; `metrics.md` §1, §3–§6, §8;
`_DIGEST.md` §1–§3, §7–§9.*]

---

### Sources

- **`_DIGEST.md`** — the sealed synthesis: voice/honesty contracts (lines 9–22), the
  structural-defensibility spine (§1), the capability/verification register (§2–§3), the
  consumption posture (§7), and the honest-limits list (§8).
- **`capabilities.md`** — the published-repo capability inventory: BYOM router (§1),
  human-in-the-loop gates (§5), mechanical safety hooks (§6), file-based memory (§7),
  audit surface + token meter (§8), the quality-gated retention loop (§9), and the
  stdlib-only local server (§10), each with VERIFIED/PARTIAL/UNVERIFIED status and repo
  citations.
- **`consumption.md`** — the consumption audit: the four-question intake gate and six-step
  pattern (§2), the consumed-vs-built boundary (§3), the catalogue of consumed patterns
  including the edit-safety stack and trajectory-eval (§4.2–§4.6), the asymmetric outbound
  posture (§5), and the honest gaps (§7).
- **`metrics.md`** — the honest figure extraction: token volume + API-equivalent
  cost-to-serve and the stale-vs-current snapshot (§1), capability-module inventory (§2),
  build iterations (§3), acceptance-test tallies and the public claim register (§4), the
  public reproducibility harness (§5), the small-model fine-tune deltas (§6), and the
  buyer-facing summary (§8).
- **Open-source pattern sources named in the consumption audit and corroborated as real
  public projects:** SWE-agent (MIT, the ACI edit-safety pattern); agentevals (MIT,
  trajectory evaluation); the Pi.dev coding-agent harness ecosystem (context engine,
  code-intelligence "lens" modules, permission-gate cluster).
- **Build assistants disclosed in every header:** Claude Opus 4.8 (lead author and
  engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks.
