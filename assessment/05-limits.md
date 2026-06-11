# 05 — Limits, Honesty Ledger & Reproducibility

An assessment is worth exactly as much as its limits section. These are carried in full, deliberately, in one place.

---

## 1. What this assessment is, and is not

- It **is** a professional engineering assessment of an architecture and design stance, with a reproducible numeric study, authored by Claude (Anthropic) under the architect's direction.
- It is **not** an independent third-party audit: the assessing AI also built much of the implementation under the architect's gated workflow. The mitigation is the evidence standard, not the relationship — every load-bearing claim is labeled, VERIFIED claims rest on public artifacts and re-runnable code, and the simulation suite re-executes on any machine. Readers should weight PARTIAL and SIMULATED claims accordingly.
- The **private build-method is withheld by documented decision** in docs 00–05, which describe the architecture at pattern level. **Dated change (2026-06-11):** the architect explicitly raised the disclosure dial — [doc 06](./06-the-real-system.md) names the real system, publishes its self-improvement loop, and carries live-measured numbers with the measurement script. What remains excluded there is basic security (credentials, live security parameters) and personal data — not strategy. This bullet is kept, dated, as the record of the boundary moving by owner decision rather than by leak.

## 2. Honest limits of the architecture (carried unchanged from the v1 research)

1. **Built by one person with AI assistance** over a recorded window of weeks, not by a funded team. The throughput is notable; unfinished edges are expected and several exist.
2. **Behind on reach and go-to-market.** The harness incumbents hold 175K–355K-star ecosystems, marketplaces, and (in ECC's case) a shipped paid product. The gap is **distribution and third-party trust, not engineering** — but it is a real gap, and naming it does not close it.
3. **Not everything described is in the public shell.** The published reference implements the gate dial, BYOM router, file memory, allow-listed runner, and seal boundary; a distinct sandbox-execute primitive, a general MCP layer, the concurrent multi-agent engine, and the full failure-signature memory live in the private layer and are **PARTIAL** from a public-evidence standpoint — pattern-described here, not publicly re-runnable.
4. **Counts are inventories, not validations.** Internal tallies (capability-module counts, iteration counts) are reconciler-guarded but self-asserted; acceptance tallies (8/8 verify, 160/160 tests, 14/14 generation runs, 20/20 eval harness) are real and the mechanisms inspectable, but most runs live in internal logs.
5. **Cost figures are API-equivalent cost-to-serve**, not necessarily cash (subscription seats change the cash picture), and the cheap-vs-frontier routing gap is a **depreciating asset** (published median decline ~50×/year). The architecture harvests the spread; it does not own it.
6. **The small-model fine-tune track is unfinished** and is reported as such in the v1 research (a regression at 50 training pairs; first positive but sub-threshold at ~150; the scaled projection unrun). It is a capability-in-progress and appears nowhere in this assessment as a result.
7. **Multi-agent orchestration is defensible only with full-trace synthesis.** The published failure mode (compounding divergence over partial context) applies to any implementation that drops that property; the architecture's defense is procedural and partially private (PARTIAL).
8. **Forbidden phrasings remain forbidden.** Nothing here claims to outperform frontier models, to possess full sovereignty, or to approach "AGI" — no unbacked superlative survives review. If a future version of these documents ever does, this section is the standing instruction to disbelieve it.

## 3. Limits of the simulations, specifically

- **Study 1 (capability growth)** is an _illustrative dynamical model_. Its anchored inputs are real (the consumption ledger; ecosystem growth rates); its functional forms (logistic ceiling, intake-times-compounding) are modeling choices. It demonstrates the structural argument's shape and sensitivity — not a forecast.
- **Study 2 (cost)** is arithmetic and therefore solid, but it prices **tokens, not quality**. Engine quality differences are deliberately out of scope; the routed mix exists because they are real.
- **Study 3 (provider shock)** has one measured input (the same-day swap) and one assumed band (coupled-architecture migration time, swept 7–90 days). The 26× headline moves with that band (≈11× at the most charitable sweep); the _sign and order of magnitude_ are robust, the exact multiple is not the claim.
- **Study 4 (consumption leverage)** uses assumed effort bands; its consistency with the ≥3× intake gate is a design-coherence check, not independent confirmation.
- **Study 5 (gate safety)** anchors reviewer effectiveness to a published category study but assumes the action mix and harm priors. The transferable result is the _trade-off curve and the floor's marginal value_, not the absolute counts.
- All Monte Carlo studies use fixed seeds (20260611) — change the seed and the third significant digit moves; nothing structural does.

## 4. Reproducibility — what a stranger can re-run today

| Claim                                                                       | How to reproduce                                                                                                                                                              |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The five studies, every figure and chart                                    | `cd simulations && python run_all.py` (Python 3.10+, stdlib only)                                                                                                             |
| The reference shell passes a stranger's verification                        | clone the published Apache-2.0 repo; run its verify + test suites (8/8, 160/160 expected)                                                                                     |
| The consume-found defect and same-day fix                                   | public commit history of the reference shell, 2026-06-11 (`max_tokens` metering fix)                                                                                          |
| ECC scale + posture figures                                                 | GitHub API, repo `affaan-m/ECC` (this assessment's pull: 2026-06-11, 213,216 stars)                                                                                           |
| The category security study, multi-agent and context-engineering literature | [REFERENCES](./REFERENCES.md)                                                                                                                                                 |
| The 2026-06-11 fleet engine swap                                            | dated event in the operator's private fleet logs — **PARTIAL** for outside readers, by the seal; the simulation suite treats only its _timing class_ (same-day) as the anchor |

## 5. Standing corrections policy

This repository inherits the v1 audit's discipline: claims found wrong get corrected in place with a dated note, never silently. The strongest credibility artifact in the v1 research was a regression left honestly in the record; this assessment intends to earn the same standard.

---

_[← 04 — CONSUME vs. Harness](./04-consume-vs-harness.md) · [References →](./REFERENCES.md)_
