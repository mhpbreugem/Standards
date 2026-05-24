"""
precision.py — Standards fixed-point precision policy (project-agnostic).

Single source of truth for the working precision and convergence thresholds that
EVERY project's fixed-point solver must follow. Import these constants instead of
hardcoding per-project numbers, so the policy is set in one place.

Policy
------
- Working precision: DOUBLE-DOUBLE (~32 significant digits, 2x float64;
  mpmath dps = 32).
- Minimum convergence threshold: ||F||inf < 1e-20  -> a fixed point is accepted.
- Bail threshold: ||F||inf > 1e-4  -> not converging, give up.
- In between (1e-20 < ||F|| <= 1e-4): partial — save checkpoint and re-queue.

Usage
-----
    from precision import WORKING_DPS, TOL_STR, DONE_THRESHOLD, BAIL_THRESHOLD, classify
    set_mp_dps(mp)                      # configure an mpmath context to the policy
    state = classify(f_inf)            # "done" | "retry" | "bail"
"""
from __future__ import annotations

# Working precision: double-double equivalent (mpmath decimal places).
WORKING_DPS: int = 32

# Convergence thresholds on ||F||inf (the fixed-point residual sup-norm).
DONE_THRESHOLD: float = 1.0e-20   # accept a fixed point at or below this
BAIL_THRESHOLD: float = 1.0e-4    # above this, bail (not converging)

# String form of the convergence target, for arbitrary-precision (mpmath) solvers
# that take a string tolerance to avoid float rounding of the target itself.
TOL_STR: str = "1e-20"


def classify(f_inf: float) -> str:
    """Classify a residual ||F||inf per the policy: 'done' | 'retry' | 'bail'."""
    if f_inf <= DONE_THRESHOLD:
        return "done"
    if f_inf > BAIL_THRESHOLD:
        return "bail"
    return "retry"


def set_mp_dps(mp) -> int:
    """Set an mpmath context to the policy working precision; return the dps used."""
    mp.dps = WORKING_DPS
    return WORKING_DPS
