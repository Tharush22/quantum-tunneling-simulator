import numpy as np
import matplotlib.pyplot as plt
from src.tunneling import T_numeric

dx = 0.05                      # layer thickness (nm)
V0 = 1.0                       # barrier height (eV)

barrier = np.full(10, V0)      # 10 layers = 0.5 nm wide
well = np.zeros(20)            # 20 layers = 1.0 nm wide
V = np.concatenate([barrier, well, barrier])

energies = np.linspace(0.01, 0.99, 3000)
T = [T_numeric(E, V, dx) for E in energies]

plt.semilogy(energies, T)
plt.xlabel("Electron energy (eV)")
plt.ylabel("Transmission probability T")
plt.title("Resonant tunneling: double barrier (0.5 nm / 1.0 nm / 0.5 nm, V0 = 1 eV)")
plt.grid(True)
plt.savefig("resonant_plot.png", dpi=200)
plt.show()