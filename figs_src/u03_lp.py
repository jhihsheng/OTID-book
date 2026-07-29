"""u03_lp.py — linear programming in two variables: feasible polytope, iso-cost
lines, and the optimum at a vertex. Problem: max 2x1+3x2 s.t. x1+2x2<=8,
3x1+2x2<=12, x>=0 — vertices (0,0),(4,0),(2,3),(0,4), optimum (2,3).
Output: assets/u03_lp.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

verts = np.array([[0, 0], [4, 0], [2, 3], [0, 4]])

fig, ax = plt.subplots(figsize=(6.6, 5.4))
ax.fill(verts[:, 0], verts[:, 1], color="#E8F1F8", ec=BLUE, lw=2, zorder=2)

xs = np.linspace(-0.4, 5.2, 200)
ax.plot(xs, (8 - xs) / 2, color=BLUE, lw=1.2, alpha=0.8)
ax.plot(xs, (12 - 3 * xs) / 2, color=BLUE, lw=1.2, alpha=0.8)
ax.text(3.9, 2.25, "$x_1+2x_2=8$", fontsize=9, color=BLUE, rotation=-19)
ax.text(2.95, 2.3, "$3x_1+2x_2=12$", fontsize=9, color=BLUE, rotation=-49)

# iso-cost lines 2x1+3x2 = c
for c in (3, 6, 9, 13):
    ax.plot(xs, (c - 2 * xs) / 3, ls="--", color=ORANGE, lw=1.1, alpha=0.9)
ax.text(-0.32, 1.35, "$2x_1+3x_2=3$", fontsize=8.5, color=ORANGE, rotation=-28)
ax.text(1.7, 3.45, "$=13$", fontsize=9, color=ORANGE)

ax.annotate("", xy=(1.1, 2.15), xytext=(0.5, 1.25),
            arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.8))
ax.text(0.1, 2.15, "cost increases", fontsize=9, color=VERM)

for v in verts:
    ax.plot(*v, "o", color=BLUE, ms=6, zorder=5)
ax.plot(2, 3, "*", color=GREEN, ms=17, zorder=6)
ax.annotate("optimal vertex $(2,3)$", xy=(2, 3), xytext=(2.65, 3.6),
            fontsize=10, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))

ax.set_xlim(-0.5, 5.3)
ax.set_ylim(-0.5, 4.6)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title("An LP optimum sits at a vertex of the feasible polytope")
ax.set_aspect("equal")

out = Path(__file__).resolve().parent.parent / "assets" / "u03_lp.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
