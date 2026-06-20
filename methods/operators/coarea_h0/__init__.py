"""Strict h=0 co-area learning operator (REE step-2 evidence -> Bayes posteriors).

This is the fixed-point-defining operator: an exact h=0 co-area integral
(cubic spline + Gauss-Legendre + partition-of-unity + smooth contour root-find).
No smoothing bandwidth, ever -- a positive bandwidth over-smooths and destroys the
partially-revealing equilibrium.

Public API:
    learn(P, grid, params)         -- the strict h=0 operator (use this as the FP map)
    learn_kernel(P, grid, params)  -- a one-off h>0 kernel, warm-start IC ONLY
    bayes(...)                     -- shared posterior helper

See README.md for the invariant and provenance.
"""
from .coarea_h0 import learn, bayes
from .coarea_kernel import learn as learn_kernel

__all__ = ["learn", "bayes", "learn_kernel"]
