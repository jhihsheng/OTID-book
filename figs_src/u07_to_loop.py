"""u07_to_loop.py — the density-based topology-optimization pipeline as a block
diagram: design density -> filter -> project -> material -> forward solve -> FoM,
with the adjoint solve feeding the gradient back to the optimizer.
Output: assets/u07_to_loop.png."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BLUE, ORANGE, VERM, GREEN, GREY = "#0072B2", "#E69F00", "#D55E00", "#009E73", "#777777"

fig, ax = plt.subplots(figsize=(10.6, 5.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.4)
ax.axis("off")

top = [
    (1.15, "design density\n$\\rho\\in[0,1]^{N}$", BLUE),
    (3.45, "filter\n(radius $R$ =\nmin. feature)", BLUE),
    (5.75, "project\n(tanh, sharpness $\\beta$)", BLUE),
    (8.05, "material\n$\\varepsilon(\\bar{\\rho})$", BLUE),
    (10.55, "forward solve\n$\\boldsymbol{A}(\\varepsilon)\\boldsymbol{x}=\\boldsymbol{b}$", ORANGE),
]
for x, label, c in top:
    ax.add_patch(FancyBboxPatch((x - 0.95, 4.35), 1.9, 1.5,
                                boxstyle="round,pad=0.08", fc="white", ec=c,
                                lw=1.8, zorder=3))
    ax.text(x, 5.1, label, ha="center", va="center", fontsize=9.3, zorder=4)
for (x0, _, _), (x1, _, _) in zip(top[:-1], top[1:]):
    ax.add_patch(FancyArrowPatch((x0 + 0.98, 5.1), (x1 - 0.98, 5.1),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=GREY, lw=1.7))

bot = [
    (10.55, "FoM $J$\n+ adjoint solve\n$\\boldsymbol{A}^{\\top}\\boldsymbol{\\lambda}=(\\partial J/\\partial\\boldsymbol{x})^{\\top}$", ORANGE),
    (6.35, "gradient $\\nabla_{\\rho}J$\n(chain rule back\nthrough project & filter)", GREEN),
    (2.35, "optimizer update\n(CCSA/MMA or L-BFGS)", VERM),
]
for x, label, c in bot:
    ax.add_patch(FancyBboxPatch((x - 1.35, 0.85), 2.7, 1.6,
                                boxstyle="round,pad=0.08", fc="white", ec=c,
                                lw=1.8, zorder=3))
    ax.text(x, 1.65, label, ha="center", va="center", fontsize=9.3, zorder=4)

ax.add_patch(FancyArrowPatch((10.55, 4.30), (10.55, 2.52), arrowstyle="-|>",
                             mutation_scale=13, color=GREY, lw=1.7))
ax.add_patch(FancyArrowPatch((9.15, 1.65), (7.75, 1.65), arrowstyle="-|>",
                             mutation_scale=13, color=GREY, lw=1.7))
ax.add_patch(FancyArrowPatch((4.95, 1.65), (3.75, 1.65), arrowstyle="-|>",
                             mutation_scale=13, color=GREY, lw=1.7))
ax.add_patch(FancyArrowPatch((1.7, 2.52), (1.15, 4.30), arrowstyle="-|>",
                             mutation_scale=13, color=VERM, lw=2.0))
ax.text(0.62, 3.42, "new $\\rho$", fontsize=9.5, color=VERM)

ax.text(6.0, 3.6, "TWO simulations per iteration — forward + adjoint —\n"
                  "deliver $J$ AND its full gradient; $\\beta$-continuation "
                  "sharpens the design toward binary",
        fontsize=10, ha="center", color="#333333", style="italic")

out = Path(__file__).resolve().parent.parent / "assets" / "u07_to_loop.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
