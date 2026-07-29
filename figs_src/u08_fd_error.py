"""u08_fd_error.py — the classic finite-difference total-error-vs-step-size
analysis, computed for real in float64: forward and central differences of
f(x)=sin(x) at x=1 vs the exact derivative cos(1). Truncation error falls with
h, roundoff error grows as eps/h; the V-shaped total has an optimal h.
Output: assets/u08_fd_error.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN, GREY = "#0072B2", "#E69F00", "#D55E00", "#009E73", "#999999"

x0 = 1.0
exact = np.cos(x0)
hs = np.logspace(-16, -0.5, 400)

fwd = np.abs((np.sin(x0 + hs) - np.sin(x0)) / hs - exact)
cen = np.abs((np.sin(x0 + hs) - np.sin(x0 - hs)) / (2 * hs) - exact)

fig, ax = plt.subplots(figsize=(7.8, 5.2))
ax.loglog(hs, fwd, color=BLUE, lw=1.4, label="forward difference")
ax.loglog(hs, cen, color=ORANGE, lw=1.4, label="central difference")

eps = np.finfo(float).eps
ax.loglog(hs, hs / 2 * abs(np.sin(x0)), ls=":", color=BLUE, lw=1.1)
ax.loglog(hs, hs**2 / 6 * abs(np.cos(x0)), ls=":", color=ORANGE, lw=1.1)
ax.loglog(hs, eps / hs, ls="--", color=GREY, lw=1.2)

ax.annotate("truncation $\\sim h$", xy=(3e-4, 1.1e-4), fontsize=9.5, color=BLUE,
            rotation=25)
ax.annotate("truncation $\\sim h^2$", xy=(2.5e-3, 3e-7), fontsize=9.5,
            color="#B0721E", rotation=45)
ax.annotate("roundoff $\\sim\\varepsilon_{\\mathrm{mach}}/h$", xy=(2e-12, 3e-4),
            fontsize=9.5, color=GREY, rotation=-25)
ax.axhline(1e-16, color=GREEN, lw=1.2, ls="-.")
ax.annotate("automatic differentiation: exact to machine precision, no $h$",
            xy=(3e-9, 3.2e-16), fontsize=9.5, color=GREEN)

ax.annotate("best $\\approx\\sqrt{\\varepsilon}\\sim10^{-8}$",
            xy=(1.5e-8, 8e-9), xytext=(4e-14, 2e-9), fontsize=9,
            color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
ax.annotate("best $\\approx\\varepsilon^{1/3}\\sim10^{-5}$",
            xy=(6e-6, 3e-11), xytext=(2e-3, 2e-13), fontsize=9,
            color="#B0721E", arrowprops=dict(arrowstyle="->", color="#B0721E", lw=1.0))

ax.set_xlabel("step size $h$")
ax.set_ylabel(r"total error $|D_h f - f'(x_0)|$")
ax.set_title(r"Finite differences of $\sin$ at $x_0=1$ (float64, computed): "
             "smaller $h$ is NOT always better")
ax.set_ylim(1e-17, 1e0)
ax.legend(loc="upper center", fontsize=9)

out = Path(__file__).resolve().parent.parent / "assets" / "u08_fd_error.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
