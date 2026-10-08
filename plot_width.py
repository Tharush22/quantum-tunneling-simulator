import numpy as np
import matplotlib.pyplot as plt
from src.tunneling import T_analytic

widths = np.linspace(0.1, 3, 200)   # barrier widths in nm
T = T_analytic(1.0, 3.0, widths)    # E = 1 eV, V0 = 3 eV

plt.semilogy(widths, T)
plt.xlabel("Barrier width (nm)")
plt.ylabel("Transmission probability T")
plt.title("Tunneling vs barrier width (E = 1 eV, V0 = 3 eV)")
plt.grid(True)
plt.savefig("width_plot.png", dpi=200)
plt.show()