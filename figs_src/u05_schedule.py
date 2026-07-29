"""u05_schedule.py — schematic quantum-annealing schedule: driver amplitude A(s)
decreasing, problem amplitude B(s) increasing, versus normalized anneal time
s = t/t_a. Shapes are illustrative, not device data. Output: assets/u05_schedule.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM = "#0072B2", "#E69F00", "#D55E00"

s = np.linspace(0, 1, 300)
A = 6.0 * (1 - s) ** 2.4          # driver: starts dominant, dies out
B = 6.0 * s ** 1.6                # problem: grows to dominance

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot(s, A, color=BLUE, lw=2.4)
ax.plot(s, B, color=ORANGE, lw=2.4)
ax.text(0.16, 3.55, r"$A(s)$ — driver $\sum_i \sigma_i^x$" + "\n(tunnelling term)",
        fontsize=10, color=BLUE, ha="center")
ax.text(0.80, 3.35, r"$B(s)$ — problem" + "\n" + r"$H_{\mathrm{problem}}$ (Ising)",
        fontsize=10, color="#B0721E", ha="center")

s_cross = s[np.argmin(np.abs(A - B))]
ax.axvline(s_cross, color="#999999", lw=1.0, ls=":")
ax.annotate("crossover:\nquantum fluctuations fade,\nproblem takes over",
            xy=(s_cross, A[np.argmin(np.abs(A - B))]),
            xytext=(0.44, 4.3), fontsize=9.5, color="#555555",
            arrowprops=dict(arrowstyle="->", color="#999999", lw=1.0))

ax.text(0.03, 6.15, "start: ground state of driver (uniform superposition)",
        fontsize=9.5, color=BLUE)
ax.text(0.42, 0.25, "end: ground state of problem = the answer (if slow enough)",
        fontsize=9.5, color="#B0721E")

ax.set_xlabel(r"normalized anneal time $s = t/t_a$")
ax.set_ylabel("energy scale (schematic)")
ax.set_title(r"Annealing schedule: $H(s) = A(s)\sum_i\sigma_i^x + B(s)\,H_{\mathrm{problem}}$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 6.6)

out = Path(__file__).resolve().parent.parent / "assets" / "u05_schedule.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
