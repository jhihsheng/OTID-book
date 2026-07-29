"""u07_adjoint_sources.py — forward vs adjoint simulation of a waveguide bend:
same geometry, same solver; only the source moves. The design gradient lives in
the overlap of the two fields. Schematic. Output: assets/u07_adjoint_sources.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"


def draw_domain(ax, title, src_at_input):
    ax.add_patch(Rectangle((0, 0), 10, 10, fc="#F5F8FB", ec="#888888", lw=1.2))
    # L-shaped waveguide: horizontal arm (input, left) + vertical arm (output, top)
    ax.add_patch(Rectangle((0, 3.8), 6.2, 1.6, fc="#BBD7EC", ec=BLUE, lw=1.2))
    ax.add_patch(Rectangle((4.6, 3.8), 1.6, 6.2, fc="#BBD7EC", ec=BLUE, lw=1.2))
    # design region at the corner
    ax.add_patch(Rectangle((3.4, 2.8), 4.0, 4.0, fc="none", ec=VERM, lw=1.8,
                           ls="--"))
    ax.text(7.65, 2.6, "design\nregion", fontsize=9, color=VERM, ha="center")
    if src_at_input:
        ax.add_patch(FancyArrowPatch((0.55, 4.6), (2.6, 4.6), arrowstyle="-|>",
                                     mutation_scale=16, color=GREEN, lw=2.6))
        ax.text(1.5, 5.75, "source:\ninput port", fontsize=9.5, color=GREEN,
                ha="center")
        ax.add_patch(Circle((5.4, 9.2), 0.42, fc="none", ec=ORANGE, lw=2.0))
        ax.text(6.9, 9.05, "monitor:\noutput port", fontsize=9.5, color="#B0721E",
                ha="center")
    else:
        ax.add_patch(FancyArrowPatch((5.4, 9.35), (5.4, 7.4), arrowstyle="-|>",
                                     mutation_scale=16, color=GREEN, lw=2.6))
        ax.text(7.7, 8.35, "source: placed by\nthe objective\n(radiates back)",
                fontsize=9.5, color=GREEN, ha="center")
    ax.set_xlim(-0.4, 10.4)
    ax.set_ylim(-0.4, 11.6)
    ax.set_title(title, fontsize=11)
    ax.axis("off")


fig, axes = plt.subplots(1, 2, figsize=(9.8, 5.0))
draw_domain(axes[0], "forward simulation", True)
draw_domain(axes[1], "adjoint simulation", False)

fig.text(0.5, 0.045,
         r"same geometry, same solver — only the source moves;   "
         r"$\delta J/\delta\varepsilon(\boldsymbol{r})\ \propto\ "
         r"\mathrm{overlap\ of\ the\ two\ fields\ in\ the\ design\ region}$",
         fontsize=10.5, ha="center", color="#333333")

out = Path(__file__).resolve().parent.parent / "assets" / "u07_adjoint_sources.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
