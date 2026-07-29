"""u06_parameterizations.py — the three parameterization families of inverse
design: (a) few-parameter shape, (b) level-set boundary, (c) density/freeform.
Output: assets/u06_parameterizations.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.9))

# ---------- (a) few-parameter shape: a multilayer stack ----------
ax = axes[0]
ths = [0.16, 0.30, 0.12, 0.24]
cols = ["#BBD7EC", "#7FB2D9", "#BBD7EC", "#7FB2D9"]
y = 0.08
for i, (t, c) in enumerate(zip(ths, cols)):
    ax.add_patch(plt.Rectangle((0.16, y), 0.56, t, fc=c, ec=BLUE, lw=1.2))
    ax.annotate("", xy=(0.80, y), xytext=(0.80, y + t),
                arrowprops=dict(arrowstyle="<->", color=VERM, lw=1.3))
    ax.text(0.84, y + t / 2, f"$t_{i+1}$", fontsize=11, color=VERM,
            va="center")
    y += t
ax.set_title("(a) shape parameters", fontsize=11)
ax.text(0.5, -0.06, "$\\boldsymbol{p}=(t_1,\\dots,t_4)$\na handful of DOF",
        fontsize=9.5, ha="center", va="top", transform=ax.transAxes)

# ---------- (b) level set: boundary as a zero contour ----------
ax = axes[1]
x = np.linspace(-1.6, 1.6, 300)
X, Y = np.meshgrid(x, x)
phi = X**2 + Y**2 - 1 - 0.35 * np.sin(3 * np.arctan2(Y, X))
ax.contourf(X, Y, phi, levels=[-10, 0], colors=["#BBD7EC"])
ax.contour(X, Y, phi, levels=[0], colors=[BLUE], linewidths=2.2)
ax.text(0, 0, "$\\phi<0$\nmaterial", fontsize=10, ha="center", va="center")
ax.annotate("boundary: $\\phi=0$", xy=(0.62, 0.96), xytext=(-0.35, 1.42),
            fontsize=10, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
ax.set_title("(b) level set", fontsize=11)
ax.text(0.5, -0.06, "the boundary curve evolves\ntopology can change",
        fontsize=9.5, ha="center", va="top", transform=ax.transAxes)
ax.set_xlim(-1.75, 1.75)
ax.set_ylim(-1.85, 1.85)

# ---------- (c) density / freeform ----------
ax = axes[2]
r = np.random.default_rng(5)
a = r.random((16, 16))
for _ in range(2):
    a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0)
         + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
a = (a - a.min()) / (a.max() - a.min())
ax.imshow(a, cmap="Blues", vmin=-0.15, vmax=1.15)
ax.set_title("(c) density / freeform", fontsize=11)
ax.text(0.5, -0.06, "$\\rho\\in[0,1]$ per pixel\nthousands of DOF",
        fontsize=9.5, ha="center", va="top", transform=ax.transAxes)

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
axes[0].set_xlim(0, 1)
axes[0].set_ylim(-0.02, 1.0)
axes[0].axis("off")

out = Path(__file__).resolve().parent.parent / "assets" / "u06_parameterizations.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
