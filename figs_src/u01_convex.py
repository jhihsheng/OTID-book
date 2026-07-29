"""u01_convex.py — a convex set vs a nonconvex set, illustrated by the chord test:
a set is convex iff the segment between ANY two of its points stays inside.
Output: assets/u01_convex.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM = "#0072B2", "#E69F00", "#D55E00"

fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.4))
th = np.linspace(0, 2 * np.pi, 400)

# --- (a) convex: an ellipse ---
ax = axes[0]
a, b = 1.5, 1.0
ax.fill(a * np.cos(th), b * np.sin(th), color="#E8F1F8", ec=BLUE, lw=1.8)
p, q = np.array([-1.05, -0.55]), np.array([1.2, 0.45])
ax.plot(*zip(p, q), color=ORANGE, lw=2.2)
ax.plot(*p, "o", color=ORANGE, ms=6)
ax.plot(*q, "o", color=ORANGE, ms=6)
ax.text(0.0, -1.35, "every chord stays inside → convex", ha="center", fontsize=10)
ax.set_title("(a) Convex set")

# --- (b) nonconvex: three-lobed blob r = 1 + 0.45 cos 3θ ---
ax = axes[1]
r = 1.0 + 0.45 * np.cos(3 * th)
ax.fill(r * np.cos(th), r * np.sin(th), color="#FDF3E3", ec=ORANGE, lw=1.8)
p = np.array([1.2, 0.0])                                # inside lobe at θ=0
q = 1.2 * np.array([np.cos(2 * np.pi / 3), np.sin(2 * np.pi / 3)])  # inside lobe at θ=120°
t = np.linspace(0, 1, 400)
seg = p[None, :] + t[:, None] * (q - p)[None, :]
rad = np.hypot(seg[:, 0], seg[:, 1])
ang = np.arctan2(seg[:, 1], seg[:, 0])
inside = rad <= 1.0 + 0.45 * np.cos(3 * ang)
ax.plot(seg[inside, 0], seg[inside, 1], color=BLUE, lw=2.2, ls="none", marker=".", ms=3)
ax.plot(seg[~inside, 0], seg[~inside, 1], color=VERM, lw=2.8, ls="none", marker=".", ms=4)
ax.plot(*p, "o", color=BLUE, ms=6)
ax.plot(*q, "o", color=BLUE, ms=6)
ax.text(0.0, -1.62, "this chord leaves the set → not convex", ha="center", fontsize=10, color=VERM)
ax.set_title("(b) Nonconvex set")

for ax in axes:
    ax.set_aspect("equal")
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.8, 1.8)
    ax.axis("off")

out = Path(__file__).resolve().parent.parent / "assets" / "u01_convex.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
