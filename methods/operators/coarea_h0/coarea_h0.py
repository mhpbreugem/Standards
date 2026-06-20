"""The hard one: strict h=0 co-area learning, ported from the old hfree_smooth
operator (cubic spline + Gauss-Legendre + partition-of-unity + smooth contour
root-find). This is what pins the partially-revealing fixed point. No smoothing
bandwidth, ever.

For agent 0 the evidence integral over the other two signals (u2, u3) is the
co-area form  A_v(p) = int_{P=p} f_v(u2) f_v(u3) / |grad P| dsigma, evaluated as a
partition-of-unity over the two parameterization directions with FIXED
Gauss-Legendre nodes (decoupled from the grid -> smooth in p). Bayes then turns
(A_0, A_1) into the agent's posterior mu. learn() returns mu for all three agents
at every cell; clearing those mu into a price is step5_clearing.crra.

Math ported verbatim from fixed-point-factory hfree_operator.py (78c27216); the
spline/root helpers live in coarea_h0_spline.py.
"""
import numpy as np
from numba import njit, prange

from .signals import f_v, gauss_legendre
from .coarea_h0_spline import natural_spline_M, spline_eval, spline_roots

EPS_PRICE = 1.0e-12


@njit(cache=True, fastmath=False, inline="always")
def bayes(u_own, tau_own, A0, A1):
    """Posterior P(v=1 | own signal, co-area evidence A0/A1)."""
    f0 = f_v(u_own, 0, tau_own)
    f1 = f_v(u_own, 1, tau_own)
    num = f1 * A1
    den = f0 * A0 + num
    if den <= 0.0:
        return 0.5
    mu = num / den
    if mu < EPS_PRICE:
        return EPS_PRICE
    if mu > 1.0 - EPS_PRICE:
        return 1.0 - EPS_PRICE
    return mu


@njit(cache=True, fastmath=False)
def slice_evidence(S, h, u0, p_target, gnodes, gweights, tauA, tauB,
                   sub, Mcols_buf, Mrows_buf):
    """Co-area evidence (A0, A1) at level p_target for a 2-D price slice S."""
    n = S.shape[0]
    Nq = gnodes.size
    A0 = 0.0
    A1 = 0.0
    maxroots = 2 * n + 4
    roots_u = np.empty(maxroots)
    roots_d = np.empty(maxroots)

    # ---- term over axis B: fix uA at GL nodes, root-find along axis B ----
    colM = Mcols_buf
    for ib in range(n):
        colM[ib, :] = natural_spline_M(S[:, ib], h)
    rowvals = np.empty(n)
    rowdA = np.empty(n)
    for q in range(Nq):
        uA = gnodes[q]
        wA = gweights[q]
        fA0 = f_v(uA, 0, tauA)
        fA1 = f_v(uA, 1, tauA)
        for ib in range(n):
            v, d = spline_eval(S[:, ib], colM[ib, :], h, u0, uA)
            rowvals[ib] = v
            rowdA[ib] = d
        Mrow = natural_spline_M(rowvals, h)
        MrowdA = natural_spline_M(rowdA, h)
        ncnt = spline_roots(rowvals, Mrow, h, u0, p_target, roots_u, roots_d, sub)
        for r in range(ncnt):
            uB = roots_u[r]
            dB = roots_d[r]
            dAval, _ = spline_eval(rowdA, MrowdA, h, u0, uB)
            denom = dAval * dAval + dB * dB
            if denom <= 0.0 or dB <= 0.0:
                continue
            wB = dB * dB / denom
            A0 += wA * wB * fA0 * f_v(uB, 0, tauB) / dB
            A1 += wA * wB * fA1 * f_v(uB, 1, tauB) / dB

    # ---- term over axis A: fix uB at GL nodes, root-find along axis A ----
    rowM = Mrows_buf
    for ia in range(n):
        rowM[ia, :] = natural_spline_M(S[ia, :], h)
    colvals = np.empty(n)
    coldB = np.empty(n)
    for q in range(Nq):
        uB = gnodes[q]
        wB_node = gweights[q]
        fB0 = f_v(uB, 0, tauB)
        fB1 = f_v(uB, 1, tauB)
        for ia in range(n):
            v, d = spline_eval(S[ia, :], rowM[ia, :], h, u0, uB)
            colvals[ia] = v
            coldB[ia] = d
        Mcol = natural_spline_M(colvals, h)
        McoldB = natural_spline_M(coldB, h)
        ncnt = spline_roots(colvals, Mcol, h, u0, p_target, roots_u, roots_d, sub)
        for r in range(ncnt):
            uA = roots_u[r]
            dA = roots_d[r]
            dBval, _ = spline_eval(coldB, McoldB, h, u0, uA)
            denom = dA * dA + dBval * dBval
            if denom <= 0.0 or dA <= 0.0:
                continue
            wA = dA * dA / denom
            A0 += wB_node * wA * f_v(uA, 0, tauA) * fB0 / dA
            A1 += wB_node * wA * f_v(uA, 1, tauA) * fB1 / dA

    return A0, A1


@njit(cache=True, fastmath=False, parallel=True)
def _learn_mu(P, ui, gnodes, gweights, tau_vec, sub):
    """Posteriors mu[i,j,l,k] for the three agents k at every cell of the cube."""
    G = ui.size
    h = ui[1] - ui[0]
    u0 = ui[0]
    mu = np.empty((G, G, G, 3))
    for i in prange(G):
        Mc = np.empty((G, G))
        Mr = np.empty((G, G))
        for j in range(G):
            for l in range(G):
                p = P[i, j, l]
                A0a, A1a = slice_evidence(P[i, :, :], h, u0, p, gnodes, gweights,
                                          tau_vec[1], tau_vec[2], sub, Mc, Mr)
                mu[i, j, l, 0] = bayes(ui[i], tau_vec[0], A0a, A1a)
                A0b, A1b = slice_evidence(P[:, j, :], h, u0, p, gnodes, gweights,
                                          tau_vec[0], tau_vec[2], sub, Mc, Mr)
                mu[i, j, l, 1] = bayes(ui[j], tau_vec[1], A0b, A1b)
                A0c, A1c = slice_evidence(P[:, :, l], h, u0, p, gnodes, gweights,
                                          tau_vec[0], tau_vec[1], sub, Mc, Mr)
                mu[i, j, l, 2] = bayes(ui[l], tau_vec[2], A0c, A1c)
    return mu


def learn(P, grid, params):
    """Strict h=0 co-area evidence -> Bayes posteriors mu, shape (G, G, G, 3)."""
    ui = grid.nodes
    gnodes, gweights = gauss_legendre(params.Nq, grid.edges[0], grid.edges[1])
    tau_vec = np.full(3, float(params.tau_eps))
    return _learn_mu(P, ui, gnodes, gweights, tau_vec, params.sub)
