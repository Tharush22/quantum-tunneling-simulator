import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import numpy as np
from src.tunneling import T_analytic, T_numeric, R_numeric


def parabolic_barrier(N, V0=3.0, a=2.0):
    """A curved barrier (no exact formula) split into N layers."""
    dx = a / N
    x = (np.arange(N) + 0.5) * dx          # middle of each layer
    return V0 * (1 - ((x - a / 2) / (a / 2)) ** 2), dx


def test_T_between_0_and_1():
    assert 0 < T_analytic(1.0, 3.0, 1.0) < 1


def test_thin_barrier_is_almost_transparent():
    assert T_analytic(1.0, 3.0, 0.001) > 0.99


def test_thicker_barrier_transmits_less():
    assert T_analytic(1.0, 3.0, 2.0) < T_analytic(1.0, 3.0, 1.0)


def test_numeric_matches_analytic_for_rectangle():
    for E, V0, a in [(1.0, 3.0, 1.0), (0.5, 2.0, 0.8), (2.0, 5.0, 0.3)]:
        V = np.full(50, V0)
        assert np.isclose(T_numeric(E, V, a / 50), T_analytic(E, V0, a), rtol=1e-8)


def test_T_plus_R_equals_one():
    for N in (20, 200):
        V, dx = parabolic_barrier(N)
        assert abs(T_numeric(1.0, V, dx) + R_numeric(1.0, V, dx) - 1) < 1e-9


def test_curved_barrier_converges():
    V_ref, dx_ref = parabolic_barrier(20000)
    T_ref = T_numeric(1.0, V_ref, dx_ref)
    errors = []
    for N in (50, 200, 1000):
        V, dx = parabolic_barrier(N)
        errors.append(abs(T_numeric(1.0, V, dx) - T_ref) / T_ref)
    assert errors[0] > errors[1] > errors[2]
    assert errors[2] < 0.01