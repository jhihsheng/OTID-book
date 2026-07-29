"""u08_stack.py — the closing synthesis diagram of Part I: the modern
inverse-design stack, with the continuous (adjoint) and discrete (annealing)
routes rising from shared numerical foundations to designed devices.
Output: assets/u08_stack.png."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BLUE, ORANGE, VERM, GREEN, PURPLE = "#0072B2", "#E69F00", "#D55E00", "#009E73", "#CC79A7"


def box(ax, x, y, w, h, label, c, fs=9.8):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.09", fc="white", ec=c,
                                lw=2.0, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, zorder=4)


fig, ax = plt.subplots(figsize=(9.6, 6.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8.6)
ax.axis("off")

box(ax, 5.0, 0.8, 8.8, 1.0,
    "numerical foundations: floating point · vectorized arrays · "
    "reproducibility  (U8)", "#666666")
box(ax, 5.0, 2.35, 6.6, 1.0,
    "fast forward solvers: TMM · FDTD (Meep) · FEM  (labs)", BLUE)

box(ax, 2.55, 4.05, 4.0, 1.15,
    "adjoint gradients (U7)\n= reverse-mode AD (U8)", ORANGE)
box(ax, 2.55, 5.75, 4.0, 1.15,
    "quasi-Newton / CCSA (U3)\nline searches (U2)", ORANGE)
box(ax, 7.45, 4.05, 4.0, 1.15,
    "Ising / QUBO encoding (U5)\nof discrete designs (U6)", GREEN)
box(ax, 7.45, 5.75, 4.0, 1.15,
    "global search (U5):\nSA · QA hardware · GA/PSO/DE", GREEN)

box(ax, 5.0, 7.65, 7.0, 1.05,
    "designed devices: filters · bends · gratings · phased arrays\n"
    "(labs: tmm · adjoint · eot · qa)", VERM)

for x0, y0, x1, y1, c in [
    (3.6, 1.32, 3.4, 1.82, "#666666"), (6.4, 1.32, 6.6, 1.82, "#666666"),
    (2.55, 2.88, 2.55, 3.44, BLUE), (7.45, 2.88, 7.45, 3.44, BLUE),
    (2.55, 4.65, 2.55, 5.14, ORANGE), (7.45, 4.65, 7.45, 5.14, GREEN),
    (3.3, 6.35, 4.3, 7.10, ORANGE), (6.7, 6.35, 5.7, 7.10, GREEN),
]:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=13, color=c, lw=1.9))

ax.text(0.22, 4.9, "continuous route", fontsize=9.5, color="#B0721E",
        ha="center", va="center", style="italic", rotation=90)
ax.text(9.78, 4.9, "discrete route", fontsize=9.5, color=GREEN,
        ha="center", va="center", style="italic", rotation=90)
ax.text(5.0, 8.45, "the modern inverse-design stack (Part I in one picture)",
        fontsize=11.5, ha="center", weight="bold", color="#333333")

out = Path(__file__).resolve().parent.parent / "assets" / "u08_stack.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
