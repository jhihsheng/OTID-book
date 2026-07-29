"""u02_newton.py — Newton's tangent construction: (a) converging on g(x)=x^3-2,
(b) diverging on g(x)=arctan(x) from x0=1.5 (overshoot grows each step).
Output: assets/u02_newton.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"

fig, (axa, axb) = plt.subplots(1, 2, figsize=(11.0, 4.6))

# ---------- (a) converging: g(x) = x^3 - 2, from x0 = 2 ----------
g = lambda x: x**3 - 2
dg = lambda x: 3 * x**2
xs = np.linspace(0.85, 2.25, 300)
axa.plot(xs, g(xs), color=BLUE, lw=2, label="$g(x)=x^3-2$")
axa.axhline(0, color="k", lw=0.8)
x = 2.0
for k in range(3):
    x_new = x - g(x) / dg(x)
    t = np.linspace(min(x_new, x) - 0.12, max(x_new, x) + 0.12, 10)
    axa.plot(t, g(x) + dg(x) * (t - x), color=ORANGE, lw=1.4)      # tangent
    axa.plot([x, x], [0, g(x)], color="#999999", ls=":", lw=1.0)   # drop line
    axa.plot(x, g(x), "o", color=VERM, ms=6, zorder=5)
    axa.annotate(f"$x_{k}$", xy=(x, 0), xytext=(x + 0.02, -1.15 - 0.55 * k),
                 fontsize=10, color=VERM)
    x = x_new
axa.plot(2 ** (1 / 3), 0, "*", color=GREEN, ms=13, zorder=6,
         label=r"root $2^{1/3}\approx 1.26$")
axa.set_ylim(-2.9, 10.0)
axa.set_title("(a) Newton converging: digits double")
axa.set_xlabel("$x$")
axa.legend(loc="upper left", fontsize=9)

# ---------- (b) diverging: g(x) = arctan(x), from x0 = 1.5 ----------
g = np.arctan
dg = lambda x: 1 / (1 + x**2)
xs = np.linspace(-6.5, 6.5, 400)
axb.plot(xs, g(xs), color=BLUE, lw=2, label=r"$g(x)=\arctan x$")
axb.axhline(0, color="k", lw=0.8)
x = 1.5
for k in range(3):
    x_new = x - g(x) / dg(x)
    t = np.linspace(min(x_new, x), max(x_new, x), 10)
    axb.plot(t, g(x) + dg(x) * (t - x), color=ORANGE, lw=1.4)
    axb.plot([x, x], [0, g(x)], color="#999999", ls=":", lw=1.0)
    axb.plot(x, g(x), "o", color=VERM, ms=6, zorder=5)
    axb.annotate(f"$x_{k}$", xy=(x, 0),
                 xytext=(x - 0.25, 0.28 if g(x) < 0 else -0.38),
                 fontsize=10, color=VERM)
    x = x_new
axb.plot(0, 0, "*", color=GREEN, ms=13, zorder=6, label="root $0$")
axb.annotate("overshoot grows → divergence", xy=(-5.1, -1.05), xytext=(-6.1, -1.42),
             fontsize=10, color=VERM)
axb.set_xlim(-6.5, 6.5)
axb.set_ylim(-1.75, 1.75)
axb.set_title(r"(b) Newton diverging on $\arctan x$ from $x_0=1.5$")
axb.set_xlabel("$x$")
axb.legend(loc="upper left", fontsize=9)

out = Path(__file__).resolve().parent.parent / "assets" / "u02_newton.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
