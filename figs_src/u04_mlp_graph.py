"""u04_mlp_graph.py — computational graph of a tiny MLP (2 inputs, 3 hidden ReLU
units, 1 output) with the forward pass (left to right) and the backward pass
(gradient signals, right to left) annotated. Output: assets/u04_mlp_graph.png."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

fig, ax = plt.subplots(figsize=(9.0, 5.0))
ax.set_xlim(-0.7, 10.2)
ax.set_ylim(-2.6, 2.9)
ax.axis("off")

xin = [(0, 0.9), (0, -0.9)]
hid = [(3.4, 1.6), (3.4, 0.0), (3.4, -1.6)]
out = [(6.8, 0.0)]
loss = (9.0, 0.0)

for (x, y), lab in zip(xin, ["$x_1$", "$x_2$"]):
    ax.add_patch(Circle((x, y), 0.42, fc="#E8F1F8", ec=BLUE, lw=1.6, zorder=3))
    ax.text(x, y, lab, ha="center", va="center", fontsize=11, zorder=4)
for i, (x, y) in enumerate(hid):
    ax.add_patch(Circle((x, y), 0.42, fc="#FDF3E3", ec=ORANGE, lw=1.6, zorder=3))
    ax.text(x, y, f"$h_{i+1}$", ha="center", va="center", fontsize=11, zorder=4)
ax.add_patch(Circle(out[0], 0.42, fc="#E6F4EE", ec=GREEN, lw=1.6, zorder=3))
ax.text(*out[0], "$\\hat{y}$", ha="center", va="center", fontsize=11, zorder=4)
ax.add_patch(Circle(loss, 0.42, fc="#FBE9E2", ec=VERM, lw=1.6, zorder=3))
ax.text(*loss, "$\\ell$", ha="center", va="center", fontsize=12, zorder=4)

for (x0, y0) in xin:
    for (x1, y1) in hid:
        ax.add_patch(FancyArrowPatch((x0 + 0.44, y0), (x1 - 0.44, y1),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color="#7a7a7a", lw=1.1, zorder=2))
for (x0, y0) in hid:
    ax.add_patch(FancyArrowPatch((x0 + 0.44, y0), (out[0][0] - 0.44, out[0][1]),
                                 arrowstyle="-|>", mutation_scale=11,
                                 color="#7a7a7a", lw=1.1, zorder=2))
ax.add_patch(FancyArrowPatch((out[0][0] + 0.44, 0), (loss[0] - 0.44, 0),
                             arrowstyle="-|>", mutation_scale=11,
                             color="#7a7a7a", lw=1.1, zorder=2))

ax.text(1.7, 2.35, "$\\boldsymbol{z}_1=\\boldsymbol{W}_1\\boldsymbol{x}+\\boldsymbol{b}_1"
                   ",\\;\\; \\boldsymbol{h}=\\sigma(\\boldsymbol{z}_1)$",
        fontsize=10.5, ha="center", color="#333333")
ax.text(5.1, 2.35, "$\\hat{y}=\\boldsymbol{w}_2^{\\top}\\boldsymbol{h}+b_2$",
        fontsize=10.5, ha="center", color="#333333")
ax.text(7.9, 2.35, "$\\ell=\\frac{1}{2}(\\hat{y}-y)^2$", fontsize=10.5,
        ha="center", color="#333333")

# forward / backward ribbons
ax.add_patch(FancyArrowPatch((0.0, -2.45), (8.9, -2.45), arrowstyle="-|>",
                             mutation_scale=14, color=BLUE, lw=2.0))
ax.text(4.4, -2.28, "forward pass: evaluate, store intermediates",
        fontsize=10, color=BLUE, ha="center")
ax.add_patch(FancyArrowPatch((8.9, -2.85), (0.0, -2.85), arrowstyle="-|>",
                             mutation_scale=14, color=VERM, lw=2.0))
ax.text(4.4, -3.25, "backward pass: one sweep delivers "
                    "$\\partial\\ell/\\partial(\\mathrm{every\\ weight})$",
        fontsize=10, color=VERM, ha="center")
ax.set_ylim(-3.6, 2.9)

ax.text(1.7, -0.05, "$\\boldsymbol{W}_1,\\boldsymbol{b}_1$", fontsize=10,
        color="#7a7a7a", ha="center", rotation=0)
ax.text(5.1, -1.15, "$\\boldsymbol{w}_2,b_2$", fontsize=10, color="#7a7a7a",
        ha="center")

out_path = Path(__file__).resolve().parent.parent / "assets" / "u04_mlp_graph.png"
out_path.parent.mkdir(exist_ok=True)
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"saved {out_path}")
