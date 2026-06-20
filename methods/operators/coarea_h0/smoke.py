"""Smoke test for the strict h=0 co-area operator.

Runs learn() end-to-end on a tiny G=5 price cube (no MIZN Grid needed -- a duck
namespace supplies .nodes/.edges and .Nq/.tau_eps/.sub) and checks the posteriors
are valid probabilities. Also exercises the warm-start kernel.

    cd methods && python -m operators.coarea_h0.smoke
"""
import types
import numpy as np

from .coarea_h0 import learn as learn_h0
from .coarea_kernel import learn as learn_kernel
from .signals import sigmoid


def _setup(G=5):
    u = np.linspace(-3.0, 3.0, G)
    grid = types.SimpleNamespace(nodes=u, edges=(u[0], u[-1]), h=float(u[1] - u[0]))
    params = types.SimpleNamespace(Nq=8, tau_eps=2.0, sub=4)
    P = np.empty((G, G, G))
    for i in range(G):
        for j in range(G):
            for l in range(G):
                P[i, j, l] = sigmoid(0.5 * (u[i] + u[j] + u[l]))
    return P, grid, params


def main():
    P, grid, params = _setup()

    mu = learn_h0(P, grid, params)
    assert mu.shape == P.shape + (3,), mu.shape
    assert np.all(np.isfinite(mu)), "non-finite posterior"
    assert mu.min() > 0.0 and mu.max() < 1.0, (float(mu.min()), float(mu.max()))

    muk = learn_kernel(P, grid, params)
    assert muk.shape == mu.shape and np.all(np.isfinite(muk)), "kernel IC broken"

    print("coarea_h0 smoke OK | shape", mu.shape,
          "| mu in (", round(float(mu.min()), 4), ",", round(float(mu.max()), 4), ")")


if __name__ == "__main__":
    main()
