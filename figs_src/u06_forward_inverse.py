"""u06_forward_inverse.py — forward problem (structure -> response, a function)
vs inverse problem (response -> structure, one-to-many / possibly empty).
Output: assets/u06_forward_inverse.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

rng = np.random.default_rng(7)


def blob(ax, seed):
    r = np.random.default_rng(seed)
    a = r.random((12, 12))
    for _ in range(3):                       # smooth then threshold -> blobby
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0)
             + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
    ax.imshow(a > a.mean(), cmap="Blues", vmin=-0.4, vmax=1.6)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#888888")


def spectrum(ax, dashed=False):
    lam = np.linspace(0, 1, 200)
    T = 1 - 0.92 * np.exp(-((lam - 0.55) / 0.07) ** 2)
    ax.plot(lam, T, color=VERM if dashed else GREEN,
            ls="--" if dashed else "-", lw=1.8)
    ax.set_ylim(-0.08, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#888888")


fig = plt.figure(figsize=(9.4, 5.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

# ---------- forward row ----------
ax.text(5.0, 5.62, "Forward problem: structure $\\to$ response — a function",
        fontsize=12, ha="center", color=BLUE, weight="bold")
b1 = fig.add_axes([0.08, 0.60, 0.14, 0.24])
blob(b1, 3)
ax.text(1.5, 3.42, "structure $\\varepsilon(\\boldsymbol{r})$", fontsize=10,
        ha="center")
ax.add_patch(FancyArrowPatch((2.6, 4.55), (5.6, 4.55), arrowstyle="-|>",
                             mutation_scale=18, color=BLUE, lw=2.2))
ax.text(4.1, 4.8, "solve Maxwell\n(TMM / FDTD / FEM)", fontsize=9.5,
        ha="center", color=BLUE)
s1 = fig.add_axes([0.60, 0.60, 0.17, 0.24])
spectrum(s1)
ax.text(6.9, 3.42, "response $T(\\lambda)$", fontsize=10, ha="center")

# ---------- inverse row ----------
ax.text(5.0, 2.72, "Inverse problem: desired response $\\to$ structure — "
                   "not a function", fontsize=12, ha="center", color=VERM,
        weight="bold")
s2 = fig.add_axes([0.06, 0.06, 0.17, 0.24])
spectrum(s2, dashed=True)
ax.text(1.45, 0.12, "target $T^{\\mathrm{tgt}}(\\lambda)$", fontsize=10,
        ha="center")
for k, (bx, seed) in enumerate(zip([0.47, 0.63, 0.79], [11, 23, 41])):
    bax = fig.add_axes([bx, 0.06, 0.115, 0.20])
    blob(bax, seed)
    ax.add_patch(FancyArrowPatch((2.6, 1.15), (10 * bx - 0.12, 1.28),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=VERM, lw=1.5, ls="--",
                                 connectionstyle=f"arc3,rad={0.10 - 0.10 * k}"))
ax.text(6.55, 0.12, "...many structures fit (non-unique) — or none exactly (infeasible)",
        fontsize=9.5, ha="center", color=VERM)
ax.text(3.3, 1.62, "?", fontsize=17, color=VERM, weight="bold")

out = Path(__file__).resolve().parent.parent / "assets" / "u06_forward_inverse.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
