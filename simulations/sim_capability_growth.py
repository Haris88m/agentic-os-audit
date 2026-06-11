"""SIMULATION 1 — Capability growth: CONSUME vs. harness-native optimization.

THE QUESTION
    Two strategies start from the same point. Strategy H ("harness-native")
    grows capability by optimizing within one harness's feature surface.
    Strategy C ("CONSUME", the Apex Prime stance) grows capability by
    consuming patterns from the whole open ecosystem through a license/value
    intake gate and re-implementing them as owned modules. Which curve wins,
    and when?

THE MODEL (discrete monthly steps, 36 months)
    Harness-native:  C_h' = C_h + a * (1 - C_h / K_h)
        Classic logistic saturation: tuning a fixed surface has a ceiling
        K_h set by the host harness's API/feature space.

    CONSUME:         C_c' = C_c + a * (1 - C_c / K_c)            (native work continues)
                          + min(V_max, rho * E(t)) * g(C_c)      (consumption intake)
        E(t)   — ecosystem candidate pool, growing e_g %/month.
        rho    — fraction of the pool that survives the 4-question intake
                 gate (license, value/overhead >= 3x, framework conflict,
                 paid-service drift) and gets consumed per month.
        V_max  — verification bandwidth cap: every consumed pattern must be
                 re-implemented and pass a real test, so intake is bounded
                 by review/verify capacity, not by ambition.
        g(C)   — mild compounding, 1 + gamma*ln(1+C)/ln(1+C_ref): consumed
                 primitives make the next consumption cheaper (documented
                 one-to-four fan-out: one consumed context engine yielded
                 four owned capabilities).

PARAMETER ANCHORS (public evidence; everything else is swept)
    - The public consumption ledger documents ~8 consumption families
      yielding ~12 owned capability modules in the recorded window, each
      passing the value/overhead >= 3x admission gate.   [ledger, VERIFIED]
    - The ecosystem side grows fast: the category's flagship bundle grew
      ~82K -> 205K GitHub stars in ~2.5 months (2026); the open SKILL.md
      capability format reached ~32 reader tools in ~3 months.  [VERIFIED]
    - Native cadence a: ~2 validated modules/month for a disciplined
      solo-plus-AI operation.                            [ASSUMPTION, swept]

HONESTY LABEL
    SIMULATED — an illustrative dynamical model with anchored parameters.
    It quantifies the structural argument (unbounded intake surface vs.
    bounded tuning surface); it does not measure the future.
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # portable/embeddable Python lacks script-dir on sys.path


import csv
import json
import math
import os

import _svg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
MONTHS = 36

SCENARIOS = {
    # name: (a, K_h, K_c, E0, e_g, rho, V_max, gamma)
    "conservative": (1.5, 60.0, 400.0, 30.0, 0.02, 0.04, 2.0, 0.10),
    "base": (2.0, 80.0, 600.0, 40.0, 0.04, 0.06, 4.0, 0.20),
    "aggressive": (2.5, 100.0, 900.0, 50.0, 0.06, 0.08, 6.0, 0.30),
}
C_REF = 50.0


def run(a, K_h, K_c, E0, e_g, rho, V_max, gamma):
    ch, cc, E = 10.0, 10.0, E0  # both strategies start with 10 modules
    rows = [(0, ch, cc)]
    for m in range(1, MONTHS + 1):
        ch = ch + a * (1 - ch / K_h)
        g = 1 + gamma * math.log(1 + cc) / math.log(1 + C_REF)
        intake = min(V_max, rho * E) * g
        cc = cc + a * (1 - cc / K_c) + intake
        E = E * (1 + e_g)
        rows.append((m, ch, cc))
    return rows


def main():
    os.makedirs(OUT, exist_ok=True)
    all_rows, summary = {}, {}
    for name, params in SCENARIOS.items():
        rows = run(*params)
        all_rows[name] = rows
        cross = next((m for m, h, c in rows if c >= 2 * h), None)
        summary[name] = {
            "harness_native_36mo": round(rows[-1][1], 1),
            "consume_36mo": round(rows[-1][2], 1),
            "advantage_36mo": round(rows[-1][2] / rows[-1][1], 2),
            "month_consume_reaches_2x": cross,
        }

    with open(os.path.join(OUT, "capability_growth.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month"] + [f"{n}_{k}" for n in SCENARIOS for k in ("harness_native", "consume")])
        for i in range(MONTHS + 1):
            row = [i]
            for n in SCENARIOS:
                row += [round(all_rows[n][i][1], 2), round(all_rows[n][i][2], 2)]
            w.writerow(row)

    with open(os.path.join(OUT, "capability_growth.json"), "w", encoding="utf-8") as f:
        json.dump({"label": "SIMULATED", "months": MONTHS, "scenarios": SCENARIOS, "summary": summary}, f, indent=2)

    base = all_rows["base"]
    _svg.line_chart(
        os.path.join(OUT, "capability_growth.svg"),
        "Capability growth: CONSUME vs. harness-native optimization",
        "Base scenario, 36 months. Both strategies start at 10 validated modules with identical native cadence.",
        "SIMULATED - illustrative dynamical model, parameters anchored to the public consumption ledger and ecosystem growth data. Apex Prime assessment, 2026-06.",
        "Month",
        "Validated capability modules",
        [
            ("Harness-native (logistic, harness ceiling)", [(m, h) for m, h, _ in base]),
            ("CONSUME (gated ecosystem intake)", [(m, c) for m, _, c in base]),
        ],
    )

    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
