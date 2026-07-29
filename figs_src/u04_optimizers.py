"""u04_optimizers.py — GD vs momentum vs Adam trajectories on the Rosenbrock
function f = (1-x)^2 + 100(y-x^2)^2 from (-1.2, 1). Deterministic (full
gradients, fixed hyperparameters). Output: assets/u04_optimizers.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN = "#0072B2", "#E69F00", "#D55E00", "#009E73"


def f(p):
    x, y = p
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def grad(p):
    x, y = p
    return np.array([-2 * (1 - x) - 400 * x * (y - x ** 2),
                     200 * (y - x ** 2)])


P0 = np.array([-1.2, 1.0])
N = 3000


def run_gd(lr):
    p = P0.copy()
    path = [p.copy()]
    for _ in range(N):
        p = p - lr * grad(p)
        path.append(p.copy())
    return np.array(path)


def run_momentum(lr, beta):
    p = P0.copy()
    v = np.zeros(2)
    path = [p.copy()]
    for _ in range(N):
        v = beta * v - lr * grad(p)
        p = p + v
        path.append(p.copy())
    return np.array(path)


def run_adam(lr, b1=0.9, b2=0.999, eps=1e-8):
    p = P0.copy()
    m = np.zeros(2)
    v = np.zeros(2)
    path = [p.copy()]
    for k in range(1, N + 1):
        g = grad(p)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mhat = m / (1 - b1 ** k)
        vhat = v / (1 - b2 ** k)
        p = p - lr * mhat / (np.sqrt(vhat) + eps)
        path.append(p.copy())
    return np.array(path)


gd = run_gd(1.5e-3)
mom = run_momentum(1.5e-3, 0.9)
adam = run_adam(2e-2)

fig, ax = plt.subplots(figsize=(8.6, 5.6))
xs = np.linspace(-1.6, 1.6, 400)
ys = np.linspace(-0.6, 1.7, 400)
X, Y = np.meshgrid(xs, ys)
F = (1 - X) ** 2 + 100 * (Y - X ** 2) ** 2
ax.contour(X, Y, F, levels=np.geomspace(0.3, 400, 12), colors=BLUE,
           linewidths=0.8, alpha=0.55)

for path, color, ls, name in [
    (gd, VERM, "-", "gradient descent"),
    (mom, ORANGE, "-", "momentum ($\\beta=0.9$)"),
    (adam, GREEN, "-", "Adam"),
]:
    fin = f(path[-1])
    ax.plot(path[:, 0], path[:, 1], ls, color=color, lw=1.5,
            label=f"{name} — $f_{{final}}={fin:.1e}$")
    ax.plot(path[-1, 0], path[-1, 1], "o", color=color, ms=6, zorder=6)

ax.plot(*P0, "ks", ms=7, zorder=6)
ax.annotate("start $(-1.2, 1)$", xy=tuple(P0), xytext=(-1.55, 1.42),
            fontsize=9.5)
ax.plot(1, 1, "k*", ms=15, zorder=6)
ax.annotate("minimum $(1,1)$", xy=(1, 1), xytext=(0.52, 1.5), fontsize=9.5)

ax.set_title(f"Rosenbrock valley, {N} iterations each: GD crawls, momentum "
             "oscillates then converges, Adam steers smoothly")
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.legend(loc="lower right", fontsize=9, framealpha=0.92)

out = Path(__file__).resolve().parent.parent / "assets" / "u04_optimizers.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
