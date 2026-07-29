"""u03_sdcg.py — the signature figure: steepest-descent zig-zag vs conjugate-gradient
path on an ill-conditioned quadratic f = (x1^2 + 9 x2^2)/2 (kappa = 9).
Start (9,1) matches Exercise 1 of unit03. Output: assets/u03_sdcg.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

Q = np.diag([1.0, 9.0])
x0 = np.array([9.0, 1.0])


def sd_path(x, n):
    pts = [x.copy()]
    for _ in range(n):
        g = Q @ x
        a = (g @ g) / (g @ Q @ g)
        x = x - a * g
        pts.append(x.copy())
    return np.array(pts)


def cg_path(x):
    pts = [x.copy()]
    g = Q @ x
    d = -g
    for _ in range(2):                       # n = 2: CG terminates exactly
        a = -(g @ d) / (d @ Q @ d)
        x = x + a * d
        g_new = Q @ x
        beta = (g_new @ g_new) / (g @ g)     # Fletcher–Reeves
        d = -g_new + beta * d
        g = g_new
        pts.append(x.copy())
    return np.array(pts)


sd = sd_path(x0, 12)
cg = cg_path(x0)

fig, ax = plt.subplots(figsize=(8.6, 4.8))
xs = np.linspace(-1.5, 10.0, 400)
ys = np.linspace(-2.6, 2.6, 300)
X, Y = np.meshgrid(xs, ys)
F = 0.5 * (X**2 + 9 * Y**2)
ax.contour(X, Y, F, levels=np.geomspace(0.4, 45, 9), colors=BLUE,
           linewidths=0.9, alpha=0.65)

ax.plot(sd[:, 0], sd[:, 1], "o-", color=VERM, ms=4, lw=1.6,
        label="steepest descent (12 steps, still going)")
ax.plot(cg[:, 0], cg[:, 1], "s-", color=GREEN, ms=5, lw=2.0,
        label="conjugate gradient (exact in 2 steps)")
ax.plot(0, 0, "k*", ms=13, zorder=6)
ax.annotate("$\\boldsymbol{x}^{(0)}=(9,1)$", xy=(9, 1), xytext=(7.6, 1.9),
            fontsize=10)
ax.annotate("zig-zag: each step $\\perp$ the last", xy=(sd[3, 0], sd[3, 1]),
            xytext=(4.3, -2.2), fontsize=10, color=VERM,
            arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
ax.set_title(r"Ill-conditioned quadratic ($\kappa=9$): "
             r"error shrinks only by $(\kappa-1)/(\kappa+1)=0.8$ per SD step")
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_aspect("equal")
ax.legend(loc="upper left", fontsize=9, framealpha=0.92)

out = Path(__file__).resolve().parent.parent / "assets" / "u03_sdcg.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
