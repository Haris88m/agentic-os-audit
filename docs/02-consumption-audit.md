# Consumption Audit — What Was Consumed

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer), with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## Scope and method

This document audits one question: **what did the system under review (SUR) take from
the open-source ecosystem, and was the take licensed and honest?** It is the
consumption ledger — the record of which patterns were consumed, from which projects,
under which licenses, and what the SUR built from each.

A word on terminology, because it is load-bearing for this whole document. The category
norm is to **ship a harness** — a runtime that other people install and run. The SUR
does something different: it **consumes** open-source work. It reads a well-designed
pattern, takes the *idea* one-way into its own architecture, re-expresses that idea in
its own stack, and keeps the original only as a segregated reference for provenance.
Throughout this audit, the word "harness" describes the *other* tools in the category
for contrast; what the SUR does is **consume / consume**. That distinction is the
differentiator, and it is the thing this document tests for honesty.

Every non-trivial claim below carries a label. **VERIFIED** means the auditor confirmed
it by direct inspection of the SUR's own on-disk artifacts — its capability-definition
files, the segregated reference copies of the consumed source, and its own findings
ledger — and/or a primary external source. **PARTIAL** means the mechanism is present
and the claim is well-supported but one verification step (a live call, a line-by-line
diff, a legal review) was not performed in this pass. **UNVERIFIED** means a recommended
artifact is not yet present.

**One honest framing, stated once.** The SUR is the work of one researcher with AI
assistance, not a funded team. Several of the projects it consumes from are large
communities or single high-output maintainers with paid tiers and continuous
integration. The SUR's edge is *not* breadth — it cannot win reach head-on — it is the
disciplined intake process and the private composition described here. That asymmetry is
context, not a defect to spin. [*Sources: research digest §8; companion findings on ECC
and OpenClaw.*]

---

## 1. The claim under audit, stated plainly

The SUR claims an unusual posture toward open source: **disciplined, one-way
consumption**. It consumes patterns and capabilities from permissively-licensed
projects, re-implements them inside its own owned framework, and does not publish its
own method back out. The ecosystem is treated as a source to learn from, not a commons
to contribute to.

This is a strong claim, and it cuts two ways for an auditor:

- **If true,** it is a coherent competitive-defensibility strategy: consume the
  commodity, keep the composition.
- **If overstated,** it is one of two failures — (a) *license laundering* (copying
  vendor code while claiming "pattern-only"), or (b) a defensibility *thinner than advertised*
  (the consumed patterns are the whole story and there is no private layer).

This audit tests both edges.

**Bottom line up front.** The consumption story holds up on inspection. The SUR keeps
reference copies of the consumed source in clearly-segregated intake directories; its
own executable scripts are independent re-implementations (Python standard library, not
the vendors' TypeScript/JavaScript); the licenses involved are permissive; and the
consumed-versus-built boundary is documented per item. The honest limits — a clean-room
diff not done, one source under a non-OSI license, a public attributions file owed
before release — are named in §7. [VERIFIED structurally — directory layout, file-type,
and findings-ledger inspection; full clean-room diff PARTIAL.]

---

## 2. The consumption discipline (how the take is governed)

The SUR runs every consumption through a documented **four-question intake gate** before
engaging an external source. The gate text is present in the system's own
capability-definition for the consumption discipline, and the findings ledger shows it
applied per item. [VERIFIED — gate text present in the SUR's definition + applied
per-item in the ledger.]

| # | Gate question | What it protects |
|---|---------------|------------------|
| 1 | **License check.** Permissive (MIT / Apache / BSD / ISC) → consume. Copyleft (GPL / AGPL) → reject for a commercial product. Weak-copyleft (MPL / LGPL) → consume only with file-isolation. | Keeps the take legal — this is the gate that matters most. |
| 2 | **Value ÷ overhead ≥ 3×.** | Avoids pulling a large dependency for one function. |
| 3 | **Framework-conflict check.** Reject anything that would force an external state system, a cloud dependency, a build-system mandate, or global-state mutation onto the owned framework. | Keeps the framework owned, not bent to match a vendor. |
| 4 | **Paid-service-drift check.** If a paid API would otherwise be the default, reframe to consume an open equivalent first; paid is a fallback, not a first move. | Keeps the system self-reliant. |

The gate is paired with a **six-step intake pattern**:

> discover → gate → re-implement as an adapter in the owned stack → **run a real test**
> → pin the reference copy in a segregated intake directory → human review before the
> new capability joins the permanent roster.

The "run a real test" step is the SUR's standing proof discipline: a consumed pattern is
not considered live until a runnable check passes against the re-implementation. The
findings record a per-item smoke-test result for each built capability (for example, the
edit-safety scripts each carry a recorded 4/4 or 8/8 pass). [VERIFIED — six-step pattern
documented; per-item test results recorded in the findings.]

**Auditor reading.** This is a genuinely disciplined intake process — materially
stricter than the *"install a skill, hope it's clean"* pattern that dominates the
category. The supply-chain risk that defines the loudest incumbent (a third-party skill
that performed data exfiltration and prompt injection without user awareness was found
in OpenClaw's registry) is precisely the risk a license-and-test gate is designed to
prevent. [VERIFIED — OpenClaw third-party malicious-skill incident documented; *source:
openclaw.md §5, citing adversa.ai and Wikipedia.*] The license gate (question 1) is the
correct gate, and it is **applied, not merely declared**.

---

## 3. The consumed-versus-built boundary (the central evidence)

For any *"pattern-only, no vendor code copied"* claim, one auditor question dominates:
**where does the vendor's code physically live, and does the SUR's own running code
depend on it?** The answer determines whether this is honest consumption or quiet
copying.

What inspection found: [VERIFIED — directory structure + file-type inspection on disk.]

- **The consumed source is kept as reference copies** under per-intake directories named
  for the intake event (e.g. `…-batch2/`, `…-batch3/`). These hold the vendors' original
  TypeScript / JavaScript / Markdown, unmodified.
- **The SUR's own executing artifacts** — the scripts that actually run as part of the
  system — are **separate files written in Python (standard library only)**. They sit in
  each capability's own `scripts/` directory, not in the intake directory.
- **The two are not wired together.** The running scripts do not import or invoke the
  reference TypeScript. The reference copy is documentation-of-provenance; the
  re-implementation is the thing that runs.

This is the structural signature of pattern-consumption done correctly: keep the source
you learned from for audit and provenance, but re-express the *idea* in your own stack
so your running system carries no foreign code. It is the difference between *"we read
their read-before-edit logic and wrote our own in Python"* and *"we shipped their
file."* Inspection supports the former. [VERIFIED.]

> **The differentiator, made concrete.** A harness-shipping project distributes the
> vendor's code so others run it. A *consuming* project distributes none of it — it runs
> its own re-implementation and keeps the original only to prove provenance. The two
> different languages (the SUR's Python vs the vendors' TypeScript/JavaScript), the two
> different locations (owned `scripts/` vs segregated intake dir), and the absence of
> any import linkage are the three independent signatures that this is consumption, not
> harnessing.

**Honest caveat — the one license that is weaker.** Keeping a full reference copy of
permissively-licensed source on disk is fine for MIT/Apache (attribution-with-notice).
For a source under a non-OSI *fair-use / source-available* license, "we kept it for
reference and re-implemented the pattern" is a defensible posture but a thinner legal
footing than MIT. At least one consumed source — the context engine of a multi-model
coding-agent harness (the Pi.dev ecosystem) — is source-available rather than
classic-OSI. The SUR's own notes flag this and scope that consumption to pattern-only
with the vendor files reference-only. The reviewer concurs that pattern-only is the
correct posture there, while noting it is the one intake where the license is "fair-use,"
not "permissive." [PARTIAL — posture is correct; the underlying license is weaker than
the MIT cases and warrants a lawyer's eye before any redistribution of the reference
copy.]

---

## 4. What was consumed — the ledger

Below is the catalogue of consumed patterns, in generic engineering vocabulary. Each
entry names the **pattern**, the **kind of source** it came from, what the SUR **built**
from it, and the **license posture**. Project names appear only where they are public
open-source projects (allowed); internal capability names are generalized.

### 4.1 Context-discipline (the largest single consumption)

- **Source kind:** the context engine of an open-source multi-model coding-agent harness
  (Pi.dev ecosystem).
- **Built:** a context-discipline sandbox primitive — *the analysis script runs in a
  sandbox; only the printed findings enter the working context, never the raw data* —
  plus a unified internal-memory query, a cross-source federated query, and a
  roster-health audit discipline. **Four distinct capabilities mapped from one source's
  design.**
- **License:** source-available / fair-use; consumed **pattern-only**, vendor files
  reference-only.
- [VERIFIED — four target capabilities present on disk with their own Python scripts;
  the context engine's reference copy present in the intake tree; the findings ledger
  records the one-source → four-pattern mapping and the license note.]

This is the largest single consumption: one well-designed open context engine yielded
four owned capabilities. The discipline it teaches — *write the script, let only the
summary into context, keep raw data out* — is exactly the *"everyone needs this, almost
nobody builds it"* pattern that rewards consumption. It is also independently
science-backed: published context-engineering research shows context editing alone gave
a measured +29% lift, rising to +39% paired with a memory tool, and cut tokens ~84% in a
100-turn evaluation, with degradation universal across all major models. [VERIFIED —
context-engineering figures; *source: research digest §5, citing Anthropic.*]

### 4.2 Read-before-edit safety

- **Source kind:** a code-intelligence client ("lens" module) from the same harness
  ecosystem.
- **Built:** an invariant that any edit to an existing file must be preceded by a read of
  that file in the current work session, with a guard that catches edits whose target
  text was drawn from memory rather than from a recent read.
- **License:** consumed pattern-only; reference TypeScript present, re-implemented as a
  standard-library Python checker.
- [VERIFIED — target capability + its Python checker present; the reference
  `edit-safety client` present in the intake tree, not imported by the running code.]

### 4.3 Symbol-aware edits

- **Source kind:** a read-expansion module from the same lens.
- **Built:** an edit-scope discipline that expands an edit to the full boundary of the
  named symbol (function / class / method, decorators included) before committing, so
  edits don't land mid-statement or cut a decorator. The re-implementation uses Python's
  standard-library AST parser.
- **License:** pattern-only; reference TypeScript present.
- [VERIFIED — capability + AST-based Python script present; smoke-tested boundary
  detection recorded in the findings.]

### 4.4 Post-edit failure diagnostics (ACI-style edit safety)

- **Source kind:** the structured diagnostic loggers of the same lens, *and* — for a
  sibling syntax-gating capability — the agent-computer-interface (ACI) edit-safety
  pattern from an open MIT research agent, **SWE-agent**.
- **Built:** (a) a seven-class failure classifier that diagnoses why an edit failed and
  routes to the right fix before retrying, and (b) a separate gate that *checks syntax
  before the edit lands and auto-reverts if the edit introduces a new syntax error*.
- **License:** the ACI pattern source is **MIT**; consumed pattern-only.
- [VERIFIED — classifier capability + its Python script present (8-branch smoke-test
  recorded); the syntax-gate capability present with a recorded 4/4 smoke-test; the SUR's
  notes credit SWE-agent ACI (MIT) as the pattern source for the syntax-gate.]

> **Composition is the point.** Taken together, 4.2–4.4 form a coherent **edit-safety
> stack** assembled from consumed patterns: read-before-edit (prevention) →
> symbol-boundary-aware edit (prevention) → syntax-gate (pre-commit prevention) →
> failure classifier (post-failure recovery). No vendor code runs; the *ideas* were
> consumed and re-built into one owned layer. This is consumption producing something
> **more coherent than any single source** — four sources composed into one stack.
> [VERIFIED — all four capabilities present and interlinked in the definitions.]

### 4.5 Trajectory evaluation

- **Source kind:** an open MIT evaluation library, **agentevals**.
- **Built:** a grader that scores an agent's *tool-call path* (the trajectory it took),
  not just its final output, with strict / unordered / subset match modes.
  Re-implemented in the Python standard library.
- **License:** **MIT**; consumed pattern-only.
- [VERIFIED — capability + standard-library scorer present, 5/5 smoke-test recorded; the
  SUR's notes credit agentevals (MIT) as the pattern source.]

### 4.6 Permission-gating / phase-locking

- **Source kind:** a permission-gate extension cluster from the coding-agent harness
  ecosystem (permission-gate + safe-git + protected-paths shape).
- **Built:** a structured phase-locking discipline (each phase has explicit entry
  conditions, exit criteria, and a checkpoint artifact; phase N+1 verifies phase N's
  artifact before opening), plus a mechanized pre-execution gate that blocks dangerous
  version-control commands before they run.
- **License:** consumed pattern-only.
- [VERIFIED — phase-lock discipline present; the dangerous-command gate present with
  recorded bite-tests; the SUR's notes name the permission-gate cluster as the pattern
  source.]

### 4.7 Exploratory-QA and email-handling patterns

- **Source kind:** documented workflows from two large open agent projects — a
  browser-driven QA routine and an IMAP/SMTP email tool.
- **Built:** a browser-driven exploratory-QA discipline (drive a real browser, check the
  console after every navigation, capture evidence) and a canonical email capability that
  wraps an official mail API for read/draft (no auto-send).
- **License:** the source projects are **MIT**; consumed pattern-only — explicitly *not*
  the email tool's code, which the SUR notes it did not install.
- [VERIFIED — both capabilities present; the SUR's notes state "pattern only, no vendor
  code" for both and name the source projects.]

### 4.8 Multi-provider routing and the model-hub adapter

- **Source kind:** an open-source multi-model coding-agent CLI (for cost-tier routing
  across many providers, the Pi.dev routing CLI) and the public model-hub APIs (Hugging
  Face).
- **Built:** adapters that let the SUR dispatch work across many model providers and pull
  open weights / datasets / model metadata — each wrapped so **the external tool conforms
  to the SUR's interface, not the reverse.**
- **License:** the routing CLI is open-source; the hub access is via public APIs under
  the hub's terms.
- [PARTIAL — the adapters are present and documented as interface-conforming wrappers;
  the reviewer confirmed the adapter definitions and the reference copies on disk, but
  did not execute a live paid-provider call as part of this audit, consistent with the
  SUR's own "mechanism-proven, live-call-not-captured" honesty elsewhere in the pack.]

### Ledger at a glance

| § | Pattern (generic) | Source kind | License posture | Built | Status |
|---|-------------------|-------------|-----------------|-------|--------|
| 4.1 | Context-discipline sandbox + 3 memory/audit capabilities | Coding-agent context engine (Pi.dev) | Source-available / fair-use; pattern-only | 4 owned Python capabilities | VERIFIED |
| 4.2 | Read-before-edit safety | Code-intelligence "lens" | Pattern-only | stdlib Python checker | VERIFIED |
| 4.3 | Symbol-aware edits | Read-expansion "lens" | Pattern-only | stdlib AST script | VERIFIED |
| 4.4 | Post-edit failure diagnostics + syntax-gate | Diagnostic loggers + SWE-agent ACI | **MIT** (ACI); pattern-only | 7-class classifier + revert gate | VERIFIED |
| 4.5 | Trajectory evaluation | agentevals | **MIT**; pattern-only | stdlib trajectory scorer | VERIFIED |
| 4.6 | Permission-gating / phase-locking | permission-gate cluster | Pattern-only | phase-lock + dangerous-cmd gate | VERIFIED |
| 4.7 | Exploratory-QA + email patterns | Two large open agent projects | **MIT**; pattern-only | browser-QA + read/draft email | VERIFIED |
| 4.8 | Multi-provider routing + model-hub | Pi.dev CLI + Hugging Face APIs | Open / public-API terms | interface-conforming adapters | PARTIAL |

---

## 5. The direction of flow (the one-way claim, corrected)

The SUR's stated rule is **inbound only**: open source → SUR (consume, yes); SUR → open
source (publish the method, no). The reviewer tested whether the system's behaviour
matches the rule.

- **Inbound is real and frequent.** §4 documents at least eight distinct consumptions
  across multiple permissive/open sources, each with a built artifact and a recorded
  test. [VERIFIED.]
- **Outbound is deliberately constrained — but not absolute.** The same project
  maintains a separate, audited open-source release plan (the `servari-open` release)
  that publishes the *shell*, the *interfaces*, the *memory format*, the *safety-gate
  model*, and runnable proofs — while keeping the orchestration intelligence, the live
  block-hook implementations, the business workflows, and the private method prompts
  unpublished. [VERIFIED — the release plan draws this line item by item.]

**Auditor correction to the headline.** "One-way" is the right *spirit* but slightly
imprecise as stated. The precise, defensible claim is:

> **Consume freely; publish a verifiable shell + interfaces; never publish the method.**

That is asymmetric, not literally zero-outbound, and it is the posture the release plan
actually encodes. An auditor should describe it that way — *not* as "takes everything,
gives nothing." [PARTIAL on the literal "one-way" phrasing; VERIFIED on the underlying
asymmetric posture.]

**A fairness point, stated plainly.** A project that *consumes* MIT/Apache work and does
*not* contribute back is fully within its license rights — permissive licenses permit
exactly this. It is legal. Whether it is *neighbourly* to the open-source commons is a
values question, not a license question, and the SUR's own materials are candid that the
strategy prioritizes competitive defensibility over reciprocity. The reviewer notes this
as an honest disclosure rather than a defect. [VERIFIED — disclosure present; "fairness"
is a values judgment, flagged as such.]

---

## 6. Why this matters for the comparison (the defensibility question)

The cross-project research in this audit reaches a firm conclusion: **the agent harness
and the open `SKILL.md` capability format are now commodities.**

- The open `SKILL.md` standard is Anthropic-authored (published 2025-12-18); within ~48h
  Microsoft (VS Code) and OpenAI (ChatGPT + Codex CLI) adopted it, and by 2026-03 ~32
  tools read the same `SKILL.md` from the same directory structure. [VERIFIED — *source:
  openclaw.md §4, citing agentskills.io and The New Stack.*]
- The two dominant open incumbents (OpenClaw, ~247K stars / ~47.7K forks at a 2026-03-02
  snapshot; Hermes, ~175K stars) plus the cross-harness bundle ECC (205,179 stars on a
  live 2026-06-03 API read) all converge on this same format. [VERIFIED — *sources:
  openclaw.md §2, ecc.md §2.*] ECC is explicit that it is *not a model and not a harness
  of its own* — it is a config/skill/agent/hook bundle that installs **onto** existing
  harnesses. [VERIFIED — *source: ecc.md §1.*]

That conclusion is **load-bearing for the consumption story**: if the harness is
commodity, then consuming harness-level patterns from the ecosystem is not a weakness or
an admission — it is the rational move, and it costs the SUR nothing defensible. The
SUR's competitive defensibility, if it exists, must live in the layers the commodity
harnesses conspicuously *lack by default* — a deep human-in-the-loop gate layer, a
failure-pattern regression memory, sealed/audited output boundaries, and a private
iterative build-and-verify method. The consumption audit confirms the SUR **built those
layers from consumed patterns plus its own composition**, and keeps the composition
private. [PARTIAL — the layers are present and inspectable in the definitions;
"constitutes a durable defensibility" is a forward-looking business judgment the reviewer does not
certify, only describes.]

There is a sharp symmetry worth quoting. The most-cited academic study of the category's
security (the OpenClaw security paper) found baseline sandbox-escape defense averaged only
~17%, and that **adding a staged human-in-the-loop defense layer** raised overall defense
to 19%–92% (Claude ~91.5%). That remedy — a staged HITL gate — is *precisely* the SUR's
claimed differentiator. The thing the loudest incumbent had to bolt on after a string of
CVEs and a ~1.5M-token data breach is the thing the SUR consumed and built in from the
start. [VERIFIED — defense-rate figures from a single paper (treat exact percentages as
one study's result); *source: openclaw.md §5, citing arXiv 2603.10387.*]

**The contrast that is *not* a differentiator.** The single-maintainer / bus-factor risk
the SUR carries (one builder + AI assistance) is the *same* asymmetry ECC carries — its
lead maintainer has 1,426 commits versus 47 for the #2 human, a ~30:1 ratio, with two
bots in the top four contributors. [VERIFIED — *source: ecc.md §3, live contributors
API.*] So solo-built is not a point of contrast between them. The real contrast is the
opposite *strategy*: ECC is open / broad / distributed / viral, **built to be consumed
and published**; the SUR is sealed / deep / method-as-defense, **built to consume and
withhold.** ECC is ahead on reach and a shipped paid go-to-market ($19/seat/month ECC
Pro); that is the SUR's distribution gap, not an engineering deficit. [VERIFIED —
*source: ecc.md §7, §10.*]

**Auditor's net.** The consumption strategy is coherent. The SUR consumes the part of
the stack everyone agrees is commodity (harness patterns, edit-safety, context-discipline,
trajectory-eval) and reserves its defensibility for the part it composed and gated. That
is the correct place to spend a defensibility. Whether the defensibility is *deep enough* against
well-funded competitors is unresolved and out of scope here.

---

## 7. Honest gaps and auditor cautions

- **"No vendor code copied" is verified structurally, not line-by-line.** The reviewer
  confirmed that the running scripts are independent Python and that vendor files sit
  segregated in the intake tree. The reviewer did **not** perform a token-level diff of
  every SUR script against every reference file to prove zero incidental copying of, say,
  a constant table or a regex. The structural evidence is strong (different language,
  different location, no import linkage) but a full clean-room diff would raise this from
  "strongly supported" to "proven." [PARTIAL.]
- **One source is fair-use, not classic-OSI.** §3 flags it. Pattern-only consumption is
  the right posture, but redistributing the reference copy of a source-available project
  warrants a legal review before any public release of the intake tree. [PARTIAL —
  flagged, not resolved.]
- **Attribution discipline should be made external-facing.** Internally the SUR credits
  each pattern's source (SWE-agent ACI / MIT, agentevals / MIT, the named harness
  ecosystems). For a public release, those attributions and the corresponding license
  notices should appear in the shipped repo's NOTICE / attributions file, not only in
  private findings. The reviewer did not confirm a public attributions file exists yet.
  [UNVERIFIED — recommend adding before publish.]
- **Test coverage of consumptions is real but per-item, not aggregate.** Each consumed
  capability carries its own recorded smoke-test (4/4, 5/5, 8/8 across the edit-safety
  and eval items). There is no single aggregate "all consumptions still pass" regression
  run captured in this pack; the per-item proofs are convincing, but a bundled regression
  of the consumed layer would strengthen the claim that the patterns stay healthy over
  time. [PARTIAL.]
- **The author asymmetry, restated for honesty.** This system was built by one person
  with AI assistance, not a funded team. The projects it learns from are, in several
  cases, large communities or single high-output maintainers with paid tiers and CI. The
  SUR's edge is not breadth or reach (it cannot win those head-on); it is the disciplined
  consumption process and the private composition. Any comparison should weight this
  asymmetry as a roadmap to learn from, not a deficit to spin. [VERIFIED — asymmetry is
  factual; the framing is the reviewer's.]

---

## 8. Verdict

The consumption story **survives audit at the stated, corrected scope.**

- **The take is licensed.** A license gate runs before intake; the consumed sources are
  permissive (MIT / Apache) with one source-available exception correctly scoped to
  pattern-only. [VERIFIED, with the §7 fair-use caveat PARTIAL.]
- **The take is pattern-only, structurally.** Vendor source is kept as segregated
  reference; the running code is independent standard-library Python that does not import
  it. [VERIFIED structurally; full clean-room diff PARTIAL.]
- **The consumed-versus-built boundary is documented per item,** with a recorded test for
  each built capability. [VERIFIED.]
- **The framework stays owned.** External tools are wrapped to conform to the SUR's
  interface; the framework is not bent to match them. [VERIFIED in the definitions.]
- **The flow is asymmetric, not literally one-way.** Consume freely; publish a verifiable
  shell + interfaces; never publish the method. That is the posture the release plan
  encodes, and it is honest about prioritizing defensibility over reciprocity. [VERIFIED.]

The honest weak points are narrow and named: a token-level clean-room diff is not done,
one source's license is fair-use rather than OSI, and a public attribution/notice file is
owed before release. **None of these is a capability or integrity gap; all are
pre-publish housekeeping.**

The consumption strategy itself is coherent, disciplined, and — given that the harness
layer is a proven commodity — the rational way to build. The differentiator is real and
correctly stated: where the category norm is to *ship a harness* others install, this
platform **consumes open source one-way into its own architecture**, runs its own
re-implementation, and keeps the original only as provenance. The credible claim is
structural: a disciplined consumer that re-builds commodity patterns into an owned, gated
composition. Nothing in this audit supports "beats frontier," "fully sovereign," or any
unbacked superlative — and none is claimed.

---

### Sources

- **The SUR's own on-disk artifacts inspected for this audit:** the consumption-discipline
  definition (the four-question gate + six-step pattern); the per-capability definitions
  and their standard-library Python scripts (edit-safety stack, trajectory-eval,
  context-discipline family, phase-lock, dangerous-command gate, QA + email patterns); the
  segregated per-intake reference-copy directories; the system's findings ledger recording
  per-item license gates, source attributions, and smoke-test results; the audited
  open-source release plan.
- **External / open-source pattern sources named by the SUR and corroborated as real
  public projects:** agentevals (MIT, trajectory evaluation); SWE-agent (MIT, ACI
  edit-safety pattern); the Pi.dev coding-agent harness ecosystem (context engine,
  lens/code-intelligence modules, permission-gate cluster — open-source /
  source-available); large open agent projects (OpenClaw, Hermes) for the QA and email
  workflow patterns; Hugging Face public model-hub APIs.
- **Companion audit findings cross-referenced** for the "harness is commodity" conclusion
  and competitor context:
  - OpenClaw findings (this review): MIT TypeScript/Swift; ~247K stars / ~47.7K forks at
    a 2026-03-02 snapshot; the open `SKILL.md` standard's broad adoption; CVE-2026-25253
    (CVSS 8.8 one-click RCE) and related CVEs; the ~1.5M-token companion-service breach;
    the academic HITL defense-rate study (arXiv 2603.10387). Primary sources cited inline
    in `openclaw.md`.
  - ECC findings (this review): live GitHub API 2026-06-03 — 205,179 stars / 31,492 forks
    / MIT; not-a-model-not-a-harness config bundle; 1,426-vs-47 single-maintainer commit
    ratio; $19/seat/month ECC Pro. Primary sources cited inline in `ecc.md`.
- **The open `SKILL.md` capability standard:** agentskills.io (Anthropic-authored,
  published 2025-12-18, broadly adopted), as documented in the companion OpenClaw
  findings.
