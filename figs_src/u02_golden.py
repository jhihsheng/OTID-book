"""u02_golden.py — golden-section interval shrinkage on f(x)=(x-1)^2 over [0,4].
Top: the function; bottom: intervals of uncertainty per iteration (grey = discarded),
with the two interior evaluations per step — one always inherited from the previous step.
Output: assets/u02_golden.png (150 dpi)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"
RHO = (3 - np.sqrt(5)) / 2          # 0.382
TAU = 1 - RHO                       # 0.618


def f(x):
    return (x - 1.0) ** 2


# --- run golden-section, recording intervals and interior points ---
a, b = 0.0, 4.0
history = []
for _ in range(5):
    x1 = a + RHO * (b - a)
    x2 = a + TAU * (b - a)
    history.append((a, b, x1, x2))
    if f(x1) < f(x2):
        b = x2
    else:
        a = x1

fig, (ax0, ax1) = plt.subplots(
    2, 1, figsize=(8.2, 6.4), sharex=True,
    gridspec_kw={"hspace": 0.12, "height_ratios": [1.15, 1.6]})

xs = np.linspace(0, 4, 400)
ax0.plot(xs, f(xs), color=BLUE, lw=2)
ax0.axvline(1.0, color=GREEN, ls=":", lw=1.4)
ax0.text(1.06, 7.2, "$x^{*}=1$", color=GREEN, fontsize=10)
ax0.set_ylabel("$f(x)=(x-1)^2$")
ax0.set_title("Golden-section search: the interval of uncertainty shrinks by 0.618 per iteration")

prev_pts = set()
for k, (a_k, b_k, x1, x2) in enumerate(history):
    y = -k
    ax1.plot([0, 4], [y, y], color="#d9d9d9", lw=7, solid_capstyle="butt")
    ax1.plot([a_k, b_k], [y, y], color=ORANGE, lw=7, solid_capstyle="butt", alpha=0.9)
    for x in (x1, x2):
        reused = any(abs(x - p) < 1e-9 for p in prev_pts)
        ax1.plot(x, y, "o", ms=7,
                 color=GREEN if reused else BLUE,
                 zorder=5)
    prev_pts = {x1, x2}
    ax1.text(4.08, y, f"len {b_k - a_k:.3f}", va="center", fontsize=9, color="#444444")

ax1.plot([], [], "o", color=BLUE, label="new evaluation")
ax1.plot([], [], "o", color=GREEN, label="reused evaluation")
ax1.annotate("×0.618 per iteration", xy=(2.9, -2.5), fontsize=11, color=VERM)
ax1.axvline(1.0, color=GREEN, ls=":", lw=1.4)
ax1.set_yticks([-k for k in range(5)])
ax1.set_yticklabels([f"iter {k}" for k in range(5)])
ax1.set_ylim(-4.7, 0.7)
ax1.set_xlim(-0.15, 5.0)
ax1.set_xlabel("$x$")
ax1.legend(loc="lower right", fontsize=9, framealpha=0.9)

out = Path(__file__).resolve().parent.parent / "assets" / "u02_golden.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
