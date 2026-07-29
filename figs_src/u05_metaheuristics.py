"""u05_metaheuristics.py — the unit's signature figure: best-so-far convergence
of random search, GA, PSO, DE, SA on the 10-D Rastrigin function, equal
evaluation budgets, 20 seeds each; median with interquartile band (honest about
run-to-run variance). Deterministic given the fixed seed list.
Output: assets/u05_metaheuristics.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREEN, PURPLE = "#0072B2", "#E69F00", "#D55E00", "#009E73", "#CC79A7"

DIM = 10
LO, HI = -5.12, 5.12
POP = 30
GENS = 200
BUDGET = POP * GENS          # 6000 evaluations for every method
SEEDS = range(20)


def rastrigin(X):
    X = np.atleast_2d(X)
    return 10 * DIM + np.sum(X**2 - 10 * np.cos(2 * np.pi * X), axis=1)


def run_random(rng):
    best = np.inf
    curve = []
    for _ in range(GENS):
        f = rastrigin(rng.uniform(LO, HI, (POP, DIM)))
        best = min(best, f.min())
        curve.append(best)
    return curve


def run_ga(rng):
    pop = rng.uniform(LO, HI, (POP, DIM))
    fit = rastrigin(pop)
    best = fit.min()
    curve = [best]
    for _ in range(GENS - 1):
        new = [pop[fit.argmin()].copy()]                     # elitism
        while len(new) < POP:
            # tournament selection (size 3), blend crossover, gaussian mutation
            i = min(rng.integers(POP, size=3), key=lambda k: fit[k])
            j = min(rng.integers(POP, size=3), key=lambda k: fit[k])
            w = rng.uniform(-0.25, 1.25, DIM)
            child = w * pop[i] + (1 - w) * pop[j]
            m = rng.random(DIM) < 0.1
            child[m] += rng.normal(0, 0.5, m.sum())
            new.append(np.clip(child, LO, HI))
        pop = np.array(new)
        fit = rastrigin(pop)
        best = min(best, fit.min())
        curve.append(best)
    return curve


def run_pso(rng):
    x = rng.uniform(LO, HI, (POP, DIM))
    v = np.zeros((POP, DIM))
    f = rastrigin(x)
    pbest, pf = x.copy(), f.copy()
    g = x[f.argmin()].copy()
    gf = f.min()
    curve = [gf]
    for _ in range(GENS - 1):
        r1, r2 = rng.random((POP, DIM)), rng.random((POP, DIM))
        v = 0.7 * v + 1.5 * r1 * (pbest - x) + 1.5 * r2 * (g - x)
        x = np.clip(x + v, LO, HI)
        f = rastrigin(x)
        imp = f < pf
        pbest[imp], pf[imp] = x[imp], f[imp]
        if pf.min() < gf:
            gf = pf.min()
            g = pbest[pf.argmin()].copy()
        curve.append(gf)
    return curve


def run_de(rng):
    pop = rng.uniform(LO, HI, (POP, DIM))
    fit = rastrigin(pop)
    best = fit.min()
    curve = [best]
    F, CR = 0.5, 0.9
    for _ in range(GENS - 1):
        for i in range(POP):
            r1, r2, r3 = rng.choice([k for k in range(POP) if k != i], 3,
                                    replace=False)
            mutant = pop[r1] + F * (pop[r2] - pop[r3])
            cross = rng.random(DIM) < CR
            cross[rng.integers(DIM)] = True
            trial = np.clip(np.where(cross, mutant, pop[i]), LO, HI)
            ft = rastrigin(trial)[0]
            if ft < fit[i]:
                pop[i], fit[i] = trial, ft
        best = min(best, fit.min())
        curve.append(best)
    return curve


def run_sa(rng):
    x = rng.uniform(LO, HI, DIM)
    fx = rastrigin(x)[0]
    best = fx
    curve = []
    T = 20.0
    for k in range(BUDGET):
        y = np.clip(x + rng.normal(0, 0.6, DIM), LO, HI)
        fy = rastrigin(y)[0]
        if fy < fx or rng.random() < np.exp(-(fy - fx) / T):
            x, fx = y, fy
        best = min(best, fx)
        T *= 0.9988                      # geometric cooling over the budget
        if (k + 1) % POP == 0:
            curve.append(best)
    return curve


methods = [
    ("random search", run_random, "#999999", ":"),
    ("GA", run_ga, ORANGE, "-"),
    ("PSO", run_pso, BLUE, "-"),
    ("DE", run_de, GREEN, "-"),
    ("SA", run_sa, VERM, "-"),
]

fig, ax = plt.subplots(figsize=(8.2, 5.2))
evals = (np.arange(GENS) + 1) * POP
for name, fn, color, ls in methods:
    runs = np.array([fn(np.random.default_rng(s)) for s in SEEDS])
    med = np.median(runs, axis=0)
    q1, q3 = np.percentile(runs, [25, 75], axis=0)
    ax.semilogy(evals, med, color=color, ls=ls, lw=2.0,
                label=f"{name} — median {med[-1]:.1f}")
    ax.fill_between(evals, q1, q3, color=color, alpha=0.16, lw=0)

ax.set_xlabel("function evaluations")
ax.set_ylabel("best $f$ so far (10-D Rastrigin, $f^{*}=0$)")
ax.set_title("Equal budgets, 20 seeds each: median best-so-far with interquartile band")
ax.legend(loc="lower left", fontsize=9, framealpha=0.92)

out = Path(__file__).resolve().parent.parent / "assets" / "u05_metaheuristics.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
