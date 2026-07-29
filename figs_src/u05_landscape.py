"""u05_landscape.py — asymmetric double-well energy landscape: escaping the
local minimum by a thermal hop OVER the barrier (simulated annealing) vs a
quantum tunnel THROUGH it (quantum annealing). Schematic.
Output: assets/u05_landscape.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"


def E(x):
    return (x**2 - 4) ** 2 / 8 - 0.6 * x


xs = np.linspace(-3.15, 3.3, 500)
fig, ax = plt.subplots(figsize=(8.0, 4.8))
ax.plot(xs, E(xs), color=BLUE, lw=2.4)

x_loc, x_glo = -1.92, 2.06            # near the two well bottoms (tilted well)
ax.plot(x_loc, E(x_loc) + 0.22, "o", color="#444444", ms=14, zorder=6)
ax.text(x_loc, E(x_loc) + 0.85, "stuck in a\nlocal minimum", fontsize=10,
        color="#444444", ha="center")
ax.plot(x_glo, E(x_glo), "*", color=GREEN, ms=17, zorder=6)
ax.text(x_glo + 0.12, E(x_glo) - 0.52, "global minimum", fontsize=10,
        color=GREEN, ha="center")

# thermal hop: dashed arc over the barrier (top near x=-0.15, E~2.06)
th = np.linspace(0, np.pi, 80)
arc_x = x_loc + (x_glo - x_loc) * (1 - np.cos(th)) / 2
arc_y = E(x_loc) + 0.35 + (2.75 - E(x_loc)) * np.sin(th)
ax.plot(arc_x[:-6], arc_y[:-6], color=VERM, lw=2.0, ls="--")
ax.annotate("", xy=(x_glo, E(x_glo) + 0.35), xytext=(arc_x[-6], arc_y[-6]),
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=2.0, ls="--"))
ax.text(0.05, 3.45, "thermal hop over the barrier\n"
                    "$P\\sim e^{-\\Delta E/T}$  (simulated annealing)",
        fontsize=10.5, color=VERM, ha="center")

# quantum tunnel: straight arrow through the barrier at the well energy
yt = E(x_loc)
ax.annotate("", xy=(1.55, yt), xytext=(x_loc + 0.28, yt),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.6))
ax.text(-0.15, yt - 0.62, "quantum tunnelling through the barrier\n"
                          "(quantum annealing)", fontsize=10.5, color=GREEN,
        ha="center")

ax.set_xlabel("configuration")
ax.set_ylabel("energy $E$")
ax.set_title("Two ways past a barrier: hop over it, or tunnel through it")
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-3.3, 3.5)
ax.set_ylim(E(x_glo) - 1.1, 4.35)

out = Path(__file__).resolve().parent.parent / "assets" / "u05_landscape.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
