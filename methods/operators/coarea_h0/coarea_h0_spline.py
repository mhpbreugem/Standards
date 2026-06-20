"""Natural cubic spline + smooth contour root-find for the strict-h=0 operator.

Split out of coarea_h0.py (the >250-line rule in MIZN_DESIGN.md). These are the
C2 building blocks that make the co-area evidence smooth in the price level p:

  - natural_spline_M : per-line second derivatives (the classic tridiagonal solve)
  - spline_eval      : value + derivative of the C2 interpolant at any coordinate
  - spline_roots     : ALL roots of spline(line) = p_target, plus |spline'| there
                       (fine sub-scan for sign changes, then Newton-polish)

All njit so the operator can call them from inside its compiled cube loop.
Ported verbatim from fixed-point-factory hfree_operator.py (78c27216).
"""
import math

import numpy as np
from numba import njit


@njit(cache=True, fastmath=False)
def natural_spline_M(y, h):
    """Second derivatives M at the n knots of a natural cubic spline (uniform h)."""
    n = y.size
    M = np.zeros(n)
    if n < 3:
        return M
    rhs = np.zeros(n)
    for i in range(1, n - 1):
        rhs[i] = 6.0 / (h * h) * (y[i - 1] - 2.0 * y[i] + y[i + 1])
    # Thomas algorithm on interior nodes, natural BC M[0]=M[n-1]=0; diag 4, off 1
    c = np.zeros(n)
    d = np.zeros(n)
    c[1] = 1.0 / 4.0
    d[1] = rhs[1] / 4.0
    for i in range(2, n - 1):
        m = 4.0 - c[i - 1]
        c[i] = 1.0 / m
        d[i] = (rhs[i] - d[i - 1]) / m
    for i in range(n - 2, 0, -1):
        M[i] = d[i] - c[i] * M[i + 1]
    return M


@njit(cache=True, fastmath=False, inline="always")
def spline_eval(y, M, h, u0, t):
    """Value and derivative of the natural cubic spline at coordinate t."""
    n = y.size
    x = (t - u0) / h
    i = int(math.floor(x))
    if i < 0:
        i = 0
    if i > n - 2:
        i = n - 2
    xi = u0 + i * h
    a = (xi + h - t) / h
    b = (t - xi) / h
    yi = y[i]; yi1 = y[i + 1]
    Mi = M[i]; Mi1 = M[i + 1]
    val = (a * yi + b * yi1
           + ((a * a * a - a) * Mi + (b * b * b - b) * Mi1) * (h * h) / 6.0)
    der = ((yi1 - yi) / h
           - (3.0 * a * a - 1.0) / 6.0 * h * Mi
           + (3.0 * b * b - 1.0) / 6.0 * h * Mi1)
    return val, der


@njit(cache=True, fastmath=False)
def spline_roots(y, M, h, u0, p_target, roots_u, roots_d, sub):
    """All roots of spline=p_target on [u0, u0+(n-1)h]; fill roots_u, |spline'| in
    roots_d. `sub` sub-intervals per cell for bracketing. Returns root count."""
    n = y.size
    nseg = (n - 1) * sub
    cnt = 0
    t_prev = u0
    v_prev, _ = spline_eval(y, M, h, u0, t_prev)
    step = (h * (n - 1)) / nseg
    for s in range(1, nseg + 1):
        t_cur = u0 + s * step
        v_cur, _ = spline_eval(y, M, h, u0, t_cur)
        dp = v_prev - p_target
        dc = v_cur - p_target
        if dp == 0.0 and dc == 0.0:
            t_prev = t_cur; v_prev = v_cur; continue
        if dp * dc <= 0.0:
            t = 0.5 * (t_prev + t_cur)
            for _ in range(40):
                val, der = spline_eval(y, M, h, u0, t)
                fval = val - p_target
                if der != 0.0:
                    tn = t - fval / der
                else:
                    tn = t
                if tn < t_prev or tn > t_cur or der == 0.0:
                    va, _ = spline_eval(y, M, h, u0, t_prev)
                    if (va - p_target) * fval <= 0.0:
                        tn = 0.5 * (t_prev + t)
                    else:
                        tn = 0.5 * (t + t_cur)
                if abs(tn - t) < 1.0e-14:
                    t = tn; break
                t = tn
                if abs(fval) < 1.0e-15:
                    break
            val, der = spline_eval(y, M, h, u0, t)
            if cnt < roots_u.size:
                roots_u[cnt] = t
                roots_d[cnt] = abs(der)
                cnt += 1
        t_prev = t_cur; v_prev = v_cur
    return cnt
