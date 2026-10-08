import numpy as np
import matplotlib.pyplot as plt
from src.tunneling import T_numeric


def parabolic_barrier(N, V0=3.0, a=2.0):
    dx = a / N
    x = (np.arange(N) + 0.5) * dx
    return V0 * (1 - ((x - a / 2) / (a / 2)) ** 2), dx


V_ref, dx_ref = parabolic_barrier(20000)
T_ref = T_numeric(1.0, V_ref, dx_ref)

Ns = [10, 20, 50, 100, 200, 500, 1000, 2000]
errors = []
for N in Ns:
    V, dx = parabolic_barrier(N)
    errors.append(abs(T_numeric(1.0, V, dx) - T_ref) / T_ref)

plt.loglog(Ns, errors, "o-")
plt.xlabel("Number of layers N")
plt.ylabel("Relative error in T")
plt.title("Convergence: parabolic barrier (E = 1 eV, V0 = 3 eV, a = 2 nm)")
plt.grid(True, which="both")
plt.savefig("convergence_plot.png", dpi=200)
plt.show()