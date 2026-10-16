# Apex Prime — The CONSUME Architecture

### Historical architecture studies and reproducible scenarios

This is an architect-directed, AI-assisted research notebook from June 2026, preserved as part of [MEKreflect's development history](https://mekreflect.com/). It is not an independent audit. Its simulations explore stated assumptions; they do not measure a capability advantage over another product, realised savings, organisational adoption or general safety.

The historical usage and fleet statements below come from the original owner's records and assessment. They have not been independently revalidated in this publication review. Provider-equivalent prices are hypothetical arithmetic, not paid expenditure. For current, separately scoped operational experiments, see [MEKreflect evaluations](https://mekreflect.com/evaluations/).

[![Built with Claude](<https://img.shields.io/badge/built%20with-Claude%20(Anthropic)-d97757>)](https://claude.com/claude-code)
[![Simulations](https://img.shields.io/badge/simulations-5%2F5%20reproducible-2da44e)](./simulations/)
[![Stack](https://img.shields.io/badge/stack-Python%20stdlib%20only-3776AB?logo=python&logoColor=white)](./simulations/run_all.py)
[![Evidence](https://img.shields.io/badge/claims-VERIFIED%20%2F%20PARTIAL%20%2F%20SIMULATED-1f6feb)](./assessment/05-limits.md)
[![License](https://img.shields.io/badge/license-CC--BY--4.0-blue.svg)](./LICENSE)

> **Architecture & design: [Haris Mekic](https://ai.mekreflect.com)** (MEKreflect) · **Assessment & simulations: Claude (Anthropic)** · 2026-06

---

**The thesis, in the architect's words: _"It's not a harness. It's CONSUME."_**

A _harness_ ships an environment and optimizes agents inside it. The **CONSUME architecture** inverts the relationship: harnesses, models, frameworks and the open-source ecosystem are **raw material** — consumed one-way through a license/value intake gate, re-implemented as owned modules, run behind a mechanical human-gate layer with a hard safety floor, and sealed on the way out. The model is a replaceable engine behind one knob. The memory is plain files. The autonomy is an architectural property with a mechanical conscience — not a model behavior.

This repository records that design and examines it through a [deterministic, standard-library simulation suite](./simulations/). The numerical outputs show what follows from the chosen parameters. To evaluate an actual implementation, a reader would also need comparable observed tasks, resource use and independently reviewed outcomes. Reproducing a scenario does not validate its assumptions.

---

## Historical scenario outputs and recorded usage

|             | Finding                                                                                                                                                                                                               | Evidence                                                                                                                         |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **4.5×**    | capability growth advantage of gated ecosystem consumption over harness-native optimization at 36 months (base scenario; 3.1–5.8× across sweeps)                                                                      | [SIMULATED](./assessment/03-simulations.md#study-1--capability-growth-consume-vs-harness-native--simulated)                      |
| **30.9×**   | per-task cost spread harvested by the BYOM engine knob — $1.16 frontier-pinned vs. $0.038 on the fleet's actual engine                                                                                                | [VERIFIED arithmetic](./assessment/03-simulations.md#study-2--byom-cost-per-task--verified-arithmetic)                           |
| **26×**     | fewer fleet tasks lost under a provider shock vs. a coupled architecture (1.2 vs. 30.6 mean days degraded)                                                                                                            | [SIMULATED, anchored](./assessment/03-simulations.md#study-3--provider-shock-resilience--simulated-anchored-to-a-measured-event) |
| **3.0×**    | engineering leverage per owned capability via the consume intake gate (15h vs. 44h); ~3× yearly capability throughput                                                                                                 | [SIMULATED](./assessment/03-simulations.md#study-4--consumption-leverage--simulated)                                             |
| **−47%**    | expected unsafe pass-through at _maximum_ autonomy, bought by the design's always-gate-high-risk floor for ≈3 human reviews/day                                                                                       | [SIMULATED, anchored](./assessment/03-simulations.md#study-5--the-autonomy-dials-floor--simulated-anchored-to-a-published-study) |
| **10.533B** | tokens the real system processed in 19 recorded build days (95.6% cache-read; ≈$26.9K API-equivalent, not cash) — one operator, with AI; plus 165 skills, 247 logged iterations, 91 failure immunities, measured live | [MEASURED](./assessment/06-the-real-system.md)                                                                                   |

The original assessment also describes two events dated 11 June 2026: a provider change in the owner's private agent fleet and a clean-checkout verification of the public reference shell. These remain historical reported events. The public repository does not reproduce the private fleet, and a current shell test should be run against its own exact commit rather than inferred from these dated counts.

![Provider shock resilience](./simulations/results/provider_shock.svg)

---

## The assessment

| #   | Document                                                                                                                                                                                    | What it answers                                                                                                                                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 00  | [**Executive Assessment**](./assessment/00-executive-assessment.md)                                                                                                                         | The design, the numbers, the proof events, the verdict — in four pages                                                                                                                                                                               |
| 01  | [**The Architecture**](./assessment/01-architecture.md)                                                                                                                                     | Apex Prime at pattern level: the CONSUME gate, the BYOM knob, the autonomy floor, file memory, the seal, the fan-out, the regression bank                                                                                                            |
| 02  | [**Implementation Guide**](./assessment/02-implementation-guide.md)                                                                                                                         | How a team adopts the architecture: six stages with acceptance criteria, three adoption profiles, the real failure modes                                                                                                                             |
| 03  | [**The Numbers**](./assessment/03-simulations.md)                                                                                                                                           | The five-study simulation report: models, anchors, results, honest readings                                                                                                                                                                          |
| 04  | [**CONSUME vs. Harness**](./assessment/04-consume-vs-harness.md)                                                                                                                            | The founder thesis tested against the category's 213K-star harness flagship — with the asymmetry that decides the argument                                                                                                                           |
| 05  | [**Limits & Reproducibility**](./assessment/05-limits.md)                                                                                                                                   | Everything that bounds these claims, in one honest place                                                                                                                                                                                             |
| 06  | [**The Real System — Full Data**](./assessment/06-the-real-system.md)                                                                                                                       | The veil off, at the architect's order: the real system (ALFRED, the Apex architecture), its self-improvement loop, and every number measured live from its own substrate — 165 skills, 247 logged iterations, 91 failure immunities, 10.533B tokens |
| 07  | [**Fable, Unsealed**](./assessment/07-fable-unsealed.md)                                                                                                                                    | The engine speaks for itself: the model's own unsoftened opinion of the system it runs inside — what is real, what is weak, where it can go — published exactly as written                                                                           |
| —   | [References](./assessment/REFERENCES.md) · [Simulation suite](./simulations/README.md) · [Measured snapshot](./data/real_system_metrics.json) · [v1 audit (archived)](./_archive/v1-audit/) |                                                                                                                                                                                                                                                      |

## Run the numbers yourself

```bash
git clone https://github.com/Haris88m/agentic-os-audit
cd agentic-os-audit/simulations
python run_all.py     # Python 3.10+, standard library only, deterministic
```

Five studies, ~3 seconds, every chart and table in this repository regenerated.

---

## Evidence standard

Every non-trivial claim is labeled **VERIFIED** (public artifact or re-runnable computation), **PARTIAL** (supported, bounded), **SIMULATED** (stated model; anchored parameters cited, assumptions sensitivity-swept), or **MEASURED** (live walk of the real system's own substrate, method published). No claim of outperforming frontier models, of full sovereignty, or of "AGI" appears anywhere, by standing policy. Docs 00–05 describe the architecture at pattern level; [doc 06](./assessment/06-the-real-system.md) drops the veil **at the architect's explicit order** and assesses the real running system with its real names and measured numbers — only credentials and personal data stay out, as basic security. [Doc 05](./assessment/05-limits.md) carries the full honesty ledger, including what this assessment is _not_ (it is not an independent third-party audit, and says so).

## Built with Claude

The architecture, the CONSUME stance, the autonomy-policy design and the engineering direction are the work of **Haris Mekic**. The implementation, this assessment, and the simulation suite were written, tested and mechanically verified by **[Claude](https://claude.com/claude-code)** (Anthropic) operating under the architect's human-gated workflow — the same gate-layer discipline the assessment describes. The relationship is disclosed everywhere it matters: this is an architect-directed AI-authored assessment with a public evidence standard, not an independent audit.

**Related:** the architecture's published reference shell — a verifiable, gate-first, BYOM agent-OS — lives at [Haris88m/servari-open](https://github.com/Haris88m/servari-open) (Apache-2.0).

## License

[CC-BY-4.0](./LICENSE) — share and adapt with attribution. The simulation code in [`simulations/`](./simulations/) is yours to re-run, modify and extend under the same terms.
