# Claims & Evidence Register — Make the Audit Independently Checkable

*Independent audit by Haris Mekic — built with Claude Opus 4.8 (lead author and engineer),
with Claude Sonnet, OpenAI GPT, and Google Gemini used for cross-checks — 2026-06-03*

---

## Purpose

This appendix exists so a skeptical outside reviewer never has to take the audit on faith.
It collects the audit's load-bearing claims into one table, grades each
**VERIFIED / PARTIAL / UNVERIFIED**, and — the part that matters — gives each one a
**reproduction step**: the exact thing a reviewer can run or read to confirm it. Where a
claim is PARTIAL or UNVERIFIED, the register states the **specific** evidence that is
missing and the action that would close it. Cost figures are API-equivalent cost-to-serve,
not cash; no superlative is asserted.

The register's own rule: a claim is only **VERIFIED** here if it was read directly from
published code/data **or executed**. Inspection of a mechanism without a run is
**VERIFIED (mechanism)**; a specific result that lives in an internal log is **PARTIAL**
until a clean-checkout run reproduces it.

> **A note on independence.** This audit was built by the same AI model (Claude Opus 4.8)
> that built the platform under review, with Sonnet, GPT, and Gemini for cross-checks. The
> claims labelled **VERIFIED** in section A below rest on **publicly readable code and
> public registry data that any reviewer can inspect directly** — they do not rest on the
> AI's assessment of its own work. This is a structured, labelled, multi-model technical
> review with a public-source evidence base; it is **not** a professionally-independent
> auditor engagement, and section A is the part designed to be checked without trusting any
> AI judgment. (See [`06-methodology.md`](./06-methodology.md) for the full methodology and
> [`08-limits-and-reproducibility.md`](./08-limits-and-reproducibility.md) §6 for the
> direct rebuttal to the "an audit written with the subject's own AI is not independent"
> objection.)

---

## A. Reproducible right now (public repo only)

These need nothing but the published Apache-2.0 repository.

| # | Claim | Grade | Reproduction step (run/read this) |
|---|---|---|---|
| R-1 | **The autonomy gate bites: at maximum autonomy (L5) a high-risk action still queues; an invalid score fails closed to queue.** | **VERIFIED (executed)** | `cd server && python autonomy.py --set demo 5 && python autonomy.py --decide demo 18` → expect `"verdict":"queue"`, band `refuse`. `--decide demo 5` → `act`. `--decide demo 999` → `queue` (fail-closed). Exit code is 2 for queue, 0 for act/report. |
| R-2 | **The action runner is allow-listed, not a raw shell: an unknown action returns the allowed list and executes nothing.** | **VERIFIED** | Read `server/servari_server.py` `_run_action`: a closed `ACTIONS` dict; an unknown name returns `{ok:false, "refused…", allowed:[…]}`. |
| R-3 | **Memory is file-based and the surface reads only declared files (never globs); a missing declared file surfaces honestly as "missing".** | **VERIFIED (mechanism)** | Read `server/memory_surface.py`; remove a declared file and confirm the surface reports `updated:"missing"`. |
| R-4 | **BYOM router is one small stdlib file with a single disclosed system line and no hidden prompt; missing config degrades to an honest message, never a fabricated reply.** | **PARTIAL** | Read `server/chat_byom.py` (≈216 lines): `SYSTEM_LINE` is the entire system prompt; `is_configured()` gates an honest `ok=False` message. The "key transmitted only to the chosen provider" property is consistent with the single `urllib` call but not exhaustively traced. |
| R-5 | **Quality-gated retention loop: KEEP only if no metric degrades, else byte-exact sha256-verified revert; fail-closed; a run can be decided once.** | **VERIFIED (mechanism)** | Read `server/retention.py` `baseline()`/`decide()` invariants; run `baseline → edit a target to degrade a metric → decide` on a clean checkout and confirm the byte-exact revert. |
| R-6 | **Local server is pure stdlib, same-origin, every route degrades to a clean "unavailable" at HTTP 200; health is fail-closed.** | **VERIFIED** | Start the server; request a route whose backing data is absent → HTTP 200 with an "unavailable" payload, not a crash. Read `server/health.py` for the fail-closed degrade. |
| R-7 | **Append-only audit boundary: the gate queue and retention audit are append-only and never rewritten.** | **VERIFIED (mechanism)** | Read `server/verify_queue.py` (`enqueue`/`decide`/`history`): pending and decision are separate append lines to `gate-queue.jsonl`. |
| R-8 | **Consumption independence is structural: owned code is stdlib Python; vendor references are segregated; running code does not import the references.** | **VERIFIED structurally** | Inspect the repo layout; grep the owned scripts for imports of the reference directories (expect none). A token-level clean-room diff would upgrade this to conclusive (see C-2). |
| R-9 | **Token ledger blended rate is internally consistent.** | **VERIFIED (derived)** | $26,920.27 ÷ 10,533M tokens ≈ $0.00256 per 1,000 tokens — division of two ledger figures. Counts are ground truth; the dollar figure is rate-dependent cost-to-serve, not cash. |
| R-10 | **Competitor public facts (star counts, the open skill standard's provenance, the documented security events) are from public sources.** | **VERIFIED (snapshots)** | Re-pull the GitHub APIs and the cited CVE/breach reports; the skill-standard provenance and cross-vendor adoption are independently confirmable. Exact "largest / beat React" framings are date-dependent (PARTIAL). See [`docs/REFERENCES.md`](./REFERENCES.md). |
| R-11 | **All scalability arithmetic is re-computable by hand on stated assumptions.** | **VERIFIED** | Re-derive the per-turn cost, the ~15× fan-out premium, the Amdahl saturation curve, the own-server break-even, and the reliability formulas from the inputs stated in [`04-scalability-science.md`](./04-scalability-science.md). |

## B. Reproducible with a clean checkout + a run

The *mechanisms* are inspectable; the specific *results* live in internal logs.

| # | Claim | Grade | Unlock step |
|---|---|---|---|
| B-1 | 14/14 multi-site generation acceptance (spec valid + 4/4 pages + working contact form + export-cleanliness scan + live HTTP 200). | PARTIAL | Run the bundled deterministic generator on a clean checkout. |
| B-2 | Quality-evaluation harness: the original five categories pass at 100%; the full expanded suite clears its ≥70% gate at ~79% (the failures are concentrated in newer, harder framing/discipline categories — see [`07-metrics.md`](./07-metrics.md) §4). | PARTIAL | Re-run the bundled harness; its grader self-test is inspectable. Report the suite version with the score — the older "20/20" is for a smaller 5-category suite. |
| B-3 | Aggregate health smoke-test: 26 of 28 checks pass on the current expanded suite (the older "19/19" denominator is a strict subset). | PARTIAL | Run the one-command health check; report the snapshot and the denominator. |
| B-4 | 8/8 mechanical safety hooks present + parsing + running; one "firing-but-blind" hook found and fixed in the same pass. | PARTIAL | Re-run the hook self-audit on a clean checkout. |
| B-5 | Product-boundary interview: probes generated; the scorer flags a planted leak (gate bites). | PARTIAL | Bundle the protocol generator + scorer with a fixture transcript; reproduce the planted-leak flag. Note: leak scoring is literal-term, not paraphrase-aware. |
| B-6 | Per-item consumption smoke-tests (4/4, 5/5, 8/8) pass. | PARTIAL | Add and run a single aggregate regression that executes all per-item smoke-tests together. |

## C. Not reproducible from public materials yet

Access not granted, artifact not published, or experiment not run.

| # | Claim | Grade | What would move it |
|---|---|---|---|
| C-1 | Small-model fine-tune deltas (−20pp → +13.3pp, still sub-threshold). | PARTIAL | Publish training data + eval split + run logs against the open ~0.5B base. |
| C-2 | "No vendor code copied" at the line level. | PARTIAL | Publish a token-level clean-room diff of owned scripts vs reference copies. |
| C-3 | ~5,900-pair fine-tune projection clears the bar. | **UNVERIFIED** | **Run the experiment.** It is a projection, not a result — never quote it alone. |
| C-4 | A successful real external-model (e.g. GPT) round-trip. | UNVERIFIED | Capture one live call; today the connector is a mock-driven shell with no successful live call logged ($0.00, zero tokens). |
| C-5 | The four roadmap capabilities (distinct sandbox-execute primitive · general MCP layer · concurrent execution engine · failure-pattern regression memory). | UNVERIFIED in repo | Ship them in a publicly auditable component with the same inspectable shape as the verified capabilities. |
| C-6 | Pattern-source attributions in the public NOTICE. | PARTIAL | A NOTICE exists for runtime dependencies; add the consumed-pattern attributions (SWE-agent / agentevals, both MIT; the named harness-ecosystem patterns consumed pattern-only). One edit closes it. |

---

## The pattern across the register

Almost every distance between **PARTIAL** and **VERIFIED** here is a **clean-checkout
re-run** or a **publish-the-artifact** step — not new engineering. The single exception is
the ~5,900-pair fine-tune projection (C-3), which genuinely requires running an experiment
that has not been run. That distribution is itself the finding: the credibility ceiling of
this audit is raised mostly by *disclosure and reproduction*, not by building anything new.
The one claim a reader should personally run first is **R-1** — the gate that still queues
a high-risk action at maximum autonomy — because it is the audit's central thesis and it
takes two commands to confirm.

*Cost figures are API-equivalent cost-to-serve, not cash. No claim of "beating frontier,"
"full sovereignty," or "AGI" appears in this register or anywhere in the audit, by design.*
