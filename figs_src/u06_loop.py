"""u06_loop.py — the closed inverse-design loop: parametrize -> simulate ->
evaluate FoM -> update, with the two update routes (adjoint vs heuristic).
Output: assets/u06_loop.png."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

fig, ax = plt.subplots(figsize=(8.8, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")

boxes = {
    "param": (2.1, 5.6, "parametrize\n$\\boldsymbol{p}\\;\\to\\;\\varepsilon(\\boldsymbol{r})$", BLUE),
    "sim": (7.9, 5.6, "simulate\nMaxwell (TMM/FDTD)", ORANGE),
    "fom": (7.9, 2.1, "evaluate figure of merit\n$J(\\boldsymbol{p})$", GREEN),
    "upd": (2.1, 2.1, "update $\\boldsymbol{p}$\n(optimizer)", VERM),
}
for x, y, label, c in boxes.values():
    ax.add_patch(FancyBboxPatch((x - 1.55, y - 0.62), 3.1, 1.24,
                                boxstyle="round,pad=0.10", fc="white", ec=c,
                                lw=2.0, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=10.5, zorder=4)

arrows = [((3.75, 5.6), (6.25, 5.6)), ((7.9, 4.85), (7.9, 2.95)),
          ((6.25, 2.1), (3.75, 2.1)), ((2.1, 2.95), (2.1, 4.85))]
for (x0, y0), (x1, y1) in arrows:
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=17, color="#555555", lw=2.0))

ax.text(5.0, 3.85, "the inverse-design loop\n(iterate until $J$ converges)",
        fontsize=11, ha="center", color="#333333", style="italic")

ax.text(2.1, 0.86, "gradient route: adjoint gives $\\nabla J$ for TWO solves "
                   "(Unit 7)\nheuristic route: SA/QA sample $J$ directly (Unit 5)",
        fontsize=9.5, ha="center", color=VERM)

out = Path(__file__).resolve().parent.parent / "assets" / "u06_loop.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
