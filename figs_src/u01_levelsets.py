"""u01_levelsets.py — level sets and gradient field of a quadratic f(x) = 1/2 x^T Q x.
The gradient is everywhere perpendicular to the level set through the point.
Output: assets/u01_levelsets.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, GREEN = "#0072B2", "#E69F00", "#009E73"

Q = np.array([[3.0, 1.0], [1.0, 2.0]])

x = np.linspace(-2.2, 2.2, 300)
X1, X2 = np.meshgrid(x, x)
F = 0.5 * (Q[0, 0] * X1**2 + 2 * Q[0, 1] * X1 * X2 + Q[1, 1] * X2**2)

fig, ax = plt.subplots(figsize=(6.6, 6.0))
cs = ax.contour(X1, X2, F, levels=[0.25, 0.75, 1.5, 2.5, 4.0, 6.0],
                colors=BLUE, linewidths=1.2)
ax.clabel(cs, fmt="%.2g", fontsize=8)

# gradient field on a coarse grid: grad f = Q x
xg = np.linspace(-2.0, 2.0, 9)
G1, G2 = np.meshgrid(xg, xg)
U = Q[0, 0] * G1 + Q[0, 1] * G2
V = Q[0, 1] * G1 + Q[1, 1] * G2
ax.quiver(G1, G2, U, V, color=ORANGE, alpha=0.85, width=0.004,
          scale=55, label=r"$\nabla f(\boldsymbol{x}) = \boldsymbol{Q}\boldsymbol{x}$")

# eigenvector axes of Q (principal axes of the elliptical level sets)
lam, W = np.linalg.eigh(Q)
for i, ls in enumerate(["--", ":"]):
    v = W[:, i]
    ax.plot([-2.2 * v[0], 2.2 * v[0]], [-2.2 * v[1], 2.2 * v[1]],
            ls=ls, color=GREEN, lw=1.6,
            label=rf"eigenvector, $\lambda={lam[i]:.2f}$")

ax.plot(0, 0, "k*", ms=11, label="minimizer $\\boldsymbol{x}^{*}=\\boldsymbol{0}$")
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.set_title(r"Level sets of $f=\frac{1}{2}\boldsymbol{x}^{\top}\boldsymbol{Q}\boldsymbol{x}$"
             r" and its gradient field")
ax.set_aspect("equal")
ax.legend(loc="lower right", fontsize=8, framealpha=0.9)

out = Path(__file__).resolve().parent.parent / "assets" / "u01_levelsets.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
