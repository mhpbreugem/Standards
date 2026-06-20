# `coarea_h0` — strict h=0 co-area learning operator

The REE step-2 operator that turns a price conjecture `P` into agents' Bayesian
posteriors `mu`, using an **exact h=0 co-area integral** — cubic spline +
Gauss-Legendre + partition-of-unity + smooth contour root-find. This is the
operator whose fixed point **is** the partially-revealing equilibrium.

## The invariant (do not break)

- **Strictly h = 0 for the FP-defining operator.** Never let an h>0 kernel define
  the fixed point. A positive bandwidth over-smooths and destroys the
  partially-revealing equilibrium (a deficit of ~0.29 vs the true ~0.17). If you
  reach for a bandwidth to regularize the Morse-critical topology jumps, stop —
  that non-smoothness is the hard part of the problem, not a bug to smooth away.
- **The kernel is a warm-start only.** `learn_kernel` (h>0) exists solely to nail a
  quick IC; hand its seed to `learn` (h=0) and report only the h=0 result.
- **Precision floor is discretization, not arithmetic.** Don't raise precision to
  beat a worst-cell residual; the lever is a larger `G`. See `../../PRECISION_POLICY.md`.

## API

```python
from operators.coarea_h0 import learn, learn_kernel, bayes

mu = learn(P, grid, params)          # strict h=0 — use as the fixed-point map
mu0 = learn_kernel(P, grid, params)  # h>0 kernel — warm-start IC ONLY
```

- `P` — price cube, shape `(G, G, G)`, values in (0, 1).
- `grid` — anything exposing `.nodes` (G u-nodes), `.edges` (`(a, b)` quadrature
  bounds), and `.h` (u-spacing; kernel only). Decoupled from the operator by design.
- `params` — `.Nq` (Gauss-Legendre points), `.tau_eps` (signal precision), `.sub`
  (root-find subdivisions).
- returns `mu`, shape `(G, G, G, 3)` — posterior for each of the 3 agents at every cell.

## Provenance

Math ported verbatim from `fixed-point-factory hfree_operator.py @ 78c27216`, by
way of `MIZN/src/mizn/step2_learning/` (`coarea_h0.py`, `coarea_h0_spline.py`,
`coarea_kernel.py`, and the `signals.py` helpers `f_v`/`gauss_legendre`). Vendored
here as a self-contained unit; the only change from MIZN is the relative import
path (`..signals` → `.signals`). Back-ported per "back-port, don't fork" so MIZN
can be archived.

## Smoke test

```
cd methods && python -m operators.coarea_h0.smoke
```

Runs `learn` and `learn_kernel` end-to-end on a G=5 cube; checks the posteriors are
finite and strictly inside (0, 1). Requires `numba` (in `requirements.txt`).
