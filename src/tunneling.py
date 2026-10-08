import numpy as np

HB2M = 0.0381  # hbar^2 / (2 * electron mass), in eV*nm^2


def T_analytic(E, V0, a):
    """Transmission probability through a rectangular barrier.
    E  = particle energy (eV), must be less than V0
    V0 = barrier height (eV)
    a  = barrier width (nm)
    """
    kappa = np.sqrt((V0 - E) / HB2M)
    return 1 / (1 + (V0**2 * np.sinh(kappa * a)**2) / (4 * E * (V0 - E)))

def _transfer_matrix(E, V_profile, dx):
    """Total 2x2 transfer matrix for a barrier made of thin flat layers.
    The barrier sits between two flat regions with V = 0.
    E = particle energy (eV), V_profile = potential of each layer (eV),
    dx = width of each layer (nm).
    """
    V_profile = np.asarray(V_profile, dtype=float)
    V_all = np.concatenate(([0.0], V_profile, [0.0]))
    widths = np.concatenate(([0.0], np.full(len(V_profile), dx), [0.0]))
    k = np.sqrt((E - V_all) / HB2M + 0j)   # complex, so E < V works

    M = np.eye(2, dtype=complex)
    for j in range(len(V_all) - 1):
        P = np.diag([np.exp(1j * k[j] * widths[j]),
                     np.exp(-1j * k[j] * widths[j])])
        D_here = np.array([[1, 1], [1j * k[j], -1j * k[j]]])
        D_next = np.array([[1, 1], [1j * k[j + 1], -1j * k[j + 1]]])
        M = np.linalg.inv(D_next) @ D_here @ P @ M
    return M


def T_numeric(E, V_profile, dx):
    """Transmission probability T for any barrier shape."""
    M = _transfer_matrix(E, V_profile, dx)
    return float(1 / abs(M[1, 1]) ** 2)


def R_numeric(E, V_profile, dx):
    """Reflection probability R for any barrier shape."""
    M = _transfer_matrix(E, V_profile, dx)
    return float(abs(M[1, 0]) ** 2 / abs(M[1, 1]) ** 2)