"""Run the full Apex Prime simulation suite and regenerate every result file.

Usage:  python run_all.py
Stack:  Python 3.10+ standard library only. Deterministic (fixed seeds).
Output: results/*.csv, results/*.json, results/*.svg
"""

from __future__ import annotations

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # portable/embeddable Python lacks script-dir on sys.path


import json

import sim_capability_growth
import sim_cost_per_task
import sim_provider_shock
import sim_consume_leverage
import sim_gate_safety


def main():
    print("=" * 72)
    print("SIM 1 - capability growth (CONSUME vs harness-native)")
    print("=" * 72)
    s1 = sim_capability_growth.main()
    print("=" * 72)
    print("SIM 2 - BYOM cost per task")
    print("=" * 72)
    s2 = sim_cost_per_task.main()
    print("=" * 72)
    print("SIM 3 - provider-shock resilience")
    print("=" * 72)
    s3 = sim_provider_shock.main()
    print("=" * 72)
    print("SIM 4 - consumption leverage")
    print("=" * 72)
    s4 = sim_consume_leverage.main()
    print("=" * 72)
    print("SIM 5 - autonomy-gate safety")
    print("=" * 72)
    s5 = sim_gate_safety.main()
    print("=" * 72)
    print("SUITE COMPLETE - 5/5 simulations, results/ regenerated")
    return {"sim1": s1, "sim2": s2, "sim3": s3, "sim4": s4, "sim5": s5}


if __name__ == "__main__":
    main()
