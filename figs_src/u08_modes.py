"""u08_modes.py — forward-mode and reverse-mode sweeps over one computational
graph: y = sin(x1*x2) + x1. Forward carries tangents left-to-right (one sweep
per INPUT); reverse caches values then carries adjoints right-to-left (one
sweep per OUTPUT). Output: assets/u08_modes.png."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

fig, ax = plt.subplots(figsize=(9.4, 5.2))
ax.set_xlim(0, 10)
ax.set_ylim(-1.4, 6.2)
ax.axis("off")

nodes = {
    "x1": (0.8, 4.6, "$x_1$", BLUE),
    "x2": (0.8, 2.2, "$x_2$", BLUE),
    "v1": (3.6, 3.4, "$v_1=x_1x_2$", ORANGE),
    "v2": (6.2, 3.4, "$v_2=\\sin v_1$", ORANGE),
    "y": (8.8, 4.0, "$y=v_2+x_1$", GREEN),
}
for x, y, lab, c in nodes.values():
    ax.add_patch(Circle((x, y), 0.62, fc="white", ec=c, lw=2.0, zorder=3))
    ax.text(x, y, lab, ha="center", va="center", fontsize=9.6, zorder=4)

edges = [("x1", "v1"), ("x2", "v1"), ("v1", "v2"), ("v2", "y"), ("x1", "y")]
for a, b in edges:
    xa, ya = nodes[a][:2]
    xb, yb = nodes[b][:2]
    rad = 0.35 if (a, b) == ("x1", "y") else 0.0
    ax.add_patch(FancyArrowPatch((xa + 0.55, ya + 0.12 if (a, b) == ("x1", "y") else ya),
                                 (xb - 0.55, yb + 0.32 if (a, b) == ("x1", "y") else yb),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color="#888888", lw=1.5, zorder=2,
                                 connectionstyle=f"arc3,rad={-rad}"))

ax.text(5.0, 6.0, "one graph, two sweeps", fontsize=12.5, ha="center",
        weight="bold", color="#333333")

ax.add_patch(FancyArrowPatch((0.6, 0.9), (8.9, 0.9), arrowstyle="-|>",
                             mutation_scale=15, color=BLUE, lw=2.2))
ax.text(4.75, 1.14, "FORWARD mode: push tangents $\\dot{v}$ along with values "
                    "— one sweep per input (JVP)", fontsize=9.8, color=BLUE,
        ha="center")
ax.text(4.75, 0.42, "$\\dot{v}_1=\\dot{x}_1x_2+x_1\\dot{x}_2"
                    "\\;\\to\\;\\dot{v}_2=\\cos(v_1)\\,\\dot{v}_1"
                    "\\;\\to\\;\\dot{y}=\\dot{v}_2+\\dot{x}_1$",
        fontsize=9.2, color=BLUE, ha="center")

ax.add_patch(FancyArrowPatch((8.9, -0.55), (0.6, -0.55), arrowstyle="-|>",
                             mutation_scale=15, color=VERM, lw=2.2))
ax.text(4.75, -0.32, "REVERSE mode: cache values, then pull adjoints "
                     "$\\bar{v}=\\partial y/\\partial v$ backwards — one sweep "
                     "per output (VJP; backprop)", fontsize=9.8, color=VERM,
        ha="center")
ax.text(4.75, -1.08, "$\\bar{v}_2=1\\;\\to\\;\\bar{v}_1=\\cos(v_1)"
                     "\\;\\to\\;\\bar{x}_1=\\bar{v}_1x_2+1,\\;\\;"
                     "\\bar{x}_2=\\bar{v}_1x_1$",
        fontsize=9.2, color=VERM, ha="center")

out = Path(__file__).resolve().parent.parent / "assets" / "u08_modes.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
