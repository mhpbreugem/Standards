"""Little numerical helpers the steps share: the Gaussian signal density, the
logit/sigmoid pair we use to move between probabilities and log-odds, and
Gauss-Legendre nodes/weights for the co-area quadrature.

The scalar helpers are numba njit so the h=0 operator can call them from inside
its own compiled kernels; they also work fine from plain Python on scalars.
"""
import math

import numpy as np
from numba import njit


# --- the signal density ---

@njit(cache=True, fastmath=False, inline="always")
def f_v(u, v, tau):
    """Gaussian signal density N(m_v, 1/tau) at u, with m_1=+1/2, m_0=-1/2."""
    mean = 0.5 if v == 1 else -0.5
    d = u - mean
    return math.sqrt(tau / (2.0 * math.pi)) * math.exp(-0.5 * tau * d * d)


# --- moving between probabilities and log-odds ---

@njit(cache=True, fastmath=False, inline="always")
def logit(p):
    """Log-odds log(p/(1-p))."""
    return math.log(p) - math.log(1.0 - p)


@njit(cache=True, fastmath=False, inline="always")
def sigmoid(z):
    """Logistic 1/(1+e^-z), written to avoid overflow for large |z|."""
    if z >= 0.0:
        e = math.exp(-z)
        return 1.0 / (1.0 + e)
    e = math.exp(z)
    return e / (1.0 + e)


# --- quadrature ---

def gauss_legendre(n, a, b):
    """n-point Gauss-Legendre nodes/weights mapped from [-1,1] to [a, b]."""
    x, w = np.polynomial.legendre.leggauss(n)
    nodes = 0.5 * (b - a) * x + 0.5 * (a + b)
    weights = 0.5 * (b - a) * w
    return nodes, weights
