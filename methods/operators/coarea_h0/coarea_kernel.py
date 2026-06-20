"""Kernel co-area learning (h > 0) -- IC SOURCE ONLY, never the FP-defining operator.

Per the h=0 rule in CLAUDE.md, the kernel is forbidden as the operator that DEFINES
the equilibrium; it is permitted solely as a one-off warm-start tool. Picard/Newton
on this smooth (Gaussian-band) operator lands quickly in the partially-revealing
basin, and that seed is then handed to the strict-h=0 operator (coarea_h0) for the
actual nail. The kernel over-smooths (deficit ~0.29 vs the true h=0 0.17), which is
exactly why it must not be the final operator.

Evidence is the Gaussian-band sum A_v(p) = sum_{cells} K_h(P-p) f_v(u_a) f_v(u_b),
bandwidth h = 0.45 * sqrt(du). Ported from fixed-point-factory contour_K3_halo.py
(phi_K3_halo_smooth), as a no-halo variant on the same inner grid as coarea_h0.
"""
import math

import numpy as np
from numba import njit, prange

from .signals import f_v
from .coarea_h0 import bayes


@njit(cache=True, fastmath=False)
def _kernel_evidence(S, ui, p_target, tauA, tauB, inv_2h2):
    """Gaussian-band evidence (A0, A1) over a full 2-D price slice S."""
    n = S.shape[0]
    A0 = 0.0
    A1 = 0.0
    for ia in range(n):
        f0a = f_v(ui[ia], 0, tauA)
        f1a = f_v(ui[ia], 1, tauA)
        for ib in range(n):
            diff = S[ia, ib] - p_target
            w = math.exp(-diff * diff * inv_2h2)
            A0 += w * f0a * f_v(ui[ib], 0, tauB)
            A1 += w * f1a * f_v(ui[ib], 1, tauB)
    return A0, A1


@njit(cache=True, fastmath=False, parallel=True)
def _learn_mu_kernel(P, ui, tau_vec, inv_2h2):
    G = ui.size
    mu = np.empty((G, G, G, 3))
    for i in prange(G):
        for j in range(G):
            for l in range(G):
                p = P[i, j, l]
                A0a, A1a = _kernel_evidence(P[i, :, :], ui, p, tau_vec[1], tau_vec[2], inv_2h2)
                mu[i, j, l, 0] = bayes(ui[i], tau_vec[0], A0a, A1a)
                A0b, A1b = _kernel_evidence(P[:, j, :], ui, p, tau_vec[0], tau_vec[2], inv_2h2)
                mu[i, j, l, 1] = bayes(ui[j], tau_vec[1], A0b, A1b)
                A0c, A1c = _kernel_evidence(P[:, :, l], ui, p, tau_vec[0], tau_vec[1], inv_2h2)
                mu[i, j, l, 2] = bayes(ui[l], tau_vec[2], A0c, A1c)
    return mu


def learn(P, grid, params, C=0.45):
    """Kernel-smoothed evidence -> posteriors mu (G,G,G,3). Bandwidth h = C*sqrt(du)."""
    h = C * math.sqrt(grid.h)
    inv_2h2 = 0.5 / (h * h)
    tau_vec = np.full(3, float(params.tau_eps))
    return _learn_mu_kernel(P, grid.nodes, tau_vec, inv_2h2)
