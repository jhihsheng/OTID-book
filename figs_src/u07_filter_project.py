"""u07_filter_project.py — the filter -> project chain on a 1-D density profile:
raw design, conic-filtered (imposes minimum feature), tanh-projected at
increasing beta (pushes toward binary). Real computation, fixed seed.
Output: assets/u07_filter_project.png."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, VERM, GREY = "#0072B2", "#E69F00", "#D55E00", "#999999"

rng = np.random.default_rng(4)
N = 400
x = np.linspace(0, 1, N)

# raw density: blocky segments + noise (what an optimizer mid-run might hold)
raw = np.zeros(N)
for a, b, v in [(0.05, 0.18, 0.9), (0.22, 0.27, 0.75), (0.34, 0.52, 1.0),
                (0.60, 0.62, 0.85), (0.70, 0.92, 0.95)]:
    raw[(x >= a) & (x < b)] = v
raw = np.clip(raw + 0.12 * rng.standard_normal(N), 0, 1)

# conic filter, radius R
R = 0.035
w = np.maximum(0, R - np.abs(np.arange(-N // 4, N // 4 + 1) / N))
w /= w.sum()
filt = np.convolve(raw, w, mode="same")


def project(rho, beta, eta=0.5):
    return (np.tanh(beta * eta) + np.tanh(beta * (rho - eta))) / (
        np.tanh(beta * eta) + np.tanh(beta * (1 - eta)))


fig, axes = plt.subplots(3, 1, figsize=(8.0, 6.4), sharex=True,
                         gridspec_kw={"hspace": 0.18})

axes[0].fill_between(x, raw, color=GREY, alpha=0.35, lw=0)
axes[0].plot(x, raw, color=GREY, lw=1.0)
axes[0].set_ylabel(r"raw $\rho$")
axes[0].set_title("filter → project: how a printable, binary design is enforced")

axes[1].fill_between(x, filt, color=BLUE, alpha=0.30, lw=0)
axes[1].plot(x, filt, color=BLUE, lw=1.6)
axes[1].set_ylabel(r"filtered $\tilde{\rho}$")
axes[1].annotate(f"conic kernel, radius $R={R}$\n= minimum feature size",
                 xy=(0.61, 0.45), fontsize=9, color=BLUE)

for beta, c, ls in [(8, ORANGE, "--"), (64, VERM, "-")]:
    axes[2].plot(x, project(filt, beta), color=c, ls=ls, lw=1.7,
                 label=f"$\\beta={beta}$")
axes[2].fill_between(x, project(filt, 64), color=VERM, alpha=0.18, lw=0)
axes[2].set_ylabel(r"projected $\bar{\rho}$")
axes[2].set_xlabel("position")
axes[2].legend(loc="center right", fontsize=9)
axes[2].annotate("raise $\\beta$ gradually:\ndesign hardens to 0/1\n($\\beta$-continuation)",
                 xy=(0.545, 0.38), fontsize=9, color=VERM)

for ax in axes:
    ax.set_ylim(-0.05, 1.1)
    ax.set_yticks([0, 1])

out = Path(__file__).resolve().parent.parent / "assets" / "u07_filter_project.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
