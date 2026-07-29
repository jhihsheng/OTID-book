"""u03_convergence.py — log-scale convergence of SD / CG / BFGS / Newton on one
quadratic in R^20 with kappa = 100 (eigenvalues log-spaced 1..100, b = ones).
All methods use exact line search, so the comparison isolates the DIRECTIONS.
Output: assets/u03_convergence.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

n = 20
lam = np.geomspace(1.0, 100.0, n)
Q = np.diag(lam)
b = np.ones(n)
x_star = b / lam
f_star = -0.5 * b @ x_star
FLOOR = 1e-16


def f_err(x):
    return max(0.5 * x @ (Q @ x) - b @ x - f_star, FLOOR)


def run_sd(x, iters):
    errs = [f_err(x)]
    for _ in range(iters):
        g = Q @ x - b
        a = (g @ g) / (g @ Q @ g)
        x = x - a * g
        errs.append(f_err(x))
    return errs


def run_cg(x, iters):
    errs = [f_err(x)]
    g = Q @ x - b
    d = -g
    for _ in range(iters):
        a = -(g @ d) / (d @ Q @ d)
        x = x + a * d
        g_new = Q @ x - b
        beta = (g_new @ g_new) / (g @ g)
        d = -g_new + beta * d
        g = g_new
        errs.append(f_err(x))
    return errs


def run_bfgs(x, iters):
    errs = [f_err(x)]
    H = np.eye(n)
    g = Q @ x - b
    for _ in range(iters):
        d = -H @ g
        a = -(g @ d) / (d @ Q @ d)      # exact line search on the quadratic
        s = a * d
        x = x + s
        g_new = Q @ x - b
        y = g_new - g
        sy = s @ y
        if sy > 1e-14:
            Hy = H @ y
            H = (H + (1.0 + (y @ Hy) / sy) * np.outer(s, s) / sy
                 - (np.outer(s, Hy) + np.outer(Hy, s)) / sy)
        g = g_new
        errs.append(f_err(x))
    return errs


x0 = np.zeros(n)
iters = 40
fig, ax = plt.subplots(figsize=(7.6, 4.9))
ax.semilogy(run_sd(x0.copy(), iters), color=VERM, lw=1.8,
            label="steepest descent")
ax.semilogy(run_cg(x0.copy(), iters), color=GREEN, lw=1.8, marker="s", ms=3.5,
            label="conjugate gradient")
ax.semilogy(run_bfgs(x0.copy(), iters), color=ORANGE, lw=1.8, ls="--",
            marker="o", ms=3, label="BFGS")
ax.semilogy([0, 1], [f_err(x0), FLOOR], color=BLUE, lw=1.8, marker="D", ms=5,
            label="Newton (one step)")
ax.axhline(FLOOR, color="#999999", lw=0.8, ls=":")
ax.text(29.5, 2.3e-16, "machine precision", fontsize=8.5, color="#777777")
ax.set_xlabel("iteration $k$")
ax.set_ylabel(r"$f(\boldsymbol{x}^{(k)})-f^{*}$")
ax.set_title(r"Same quadratic ($n=20$, $\kappa=100$), same line search — "
             "only the directions differ")
ax.set_ylim(1e-17, 1e3)
ax.legend(loc="upper right", fontsize=9)

out = Path(__file__).resolve().parent.parent / "assets" / "u03_convergence.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
