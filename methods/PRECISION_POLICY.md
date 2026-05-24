# Precision policy (all fixed points, all projects)

This is the **standard every project must follow** when solving a fixed point
`x = Φ(x)` with these shared methods — REE/price functions today, anything else
tomorrow. It is intentionally problem-agnostic: it constrains *how precisely* a
fixed point must be solved and *when* a solution is accepted, not what the map is.

## The policy

| | Requirement |
|---|---|
| **Working precision** | **double-double** — ~32 significant digits (2× float64), i.e. `mpmath dps = 32` |
| **Accept (`done`)** | `‖F‖∞ < 1e-20` (the **minimum** convergence threshold), where `F = Φ(x) − x` |
| **Bail** | `‖F‖∞ > 1e-4` — not converging, give up |
| **Partial** | `1e-20 < ‖F‖∞ ≤ 1e-4` — save the checkpoint and re-queue |

`‖F‖∞` is the sup-norm of the residual. "Minimum threshold" means a fixed point is
**not** accepted until the residual is at or below `1e-20`.

## Single source of truth

The numbers live in **`methods/solver/precision.py`** — import them, do not
hardcode:

```python
from precision import WORKING_DPS, TOL_STR, DONE_THRESHOLD, BAIL_THRESHOLD, classify, set_mp_dps
set_mp_dps(mp)               # configure mpmath to the policy precision
state = classify(f_inf)      # "done" | "retry" | "bail"
```

The policy **cannot be overridden** by per-task `solver_params`. Changing it is a
change to this file + `precision.py`, via PR.

## What a project must do

1. Solve the fixed point at the policy working precision (double-double / dps 32).
2. Drive the residual to `‖F‖∞ < 1e-20` before marking a task `done`; bail above
   `1e-4`; otherwise checkpoint + re-queue.
3. Report the residual (e.g. `F_max`) as a **string** in the task `result` to
   preserve precision, alongside the project's own convergence-quality metric
   (defined in the project's `EQUATIONS.md`; see `runner/SOLVER_INSTRUCTIONS.md`).

## Note on float64-only solvers

A pure `float64` solver bottoms out near `1e-15` and therefore **cannot** meet the
`1e-20` accept gate — such solvers are exploratory only and do not produce accepted
fixed points. Production solves use the double-double (mpmath) path.
