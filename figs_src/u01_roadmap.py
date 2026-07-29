"""u01_roadmap.py — course roadmap: theory units (Part I) feeding hands-on modules (Part II).
Output: assets/u01_roadmap.png (150 dpi). Colorblind-safe Okabe–Ito palette."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BLUE, ORANGE, GREEN, GREY = "#0072B2", "#E69F00", "#009E73", "#999999"

units = [
    ("U1", "Mathematical preliminaries"),
    ("U2", "Basics & 1-D search"),
    ("U3", "Gradient / Newton / CG / QN"),
    ("U4", "Neural networks"),
    ("U5", "Heuristics: MC, GA/PSO/DE, SA/QA"),
    ("U6", "Inverse design concepts"),
    ("U7", "Adjoint & topology optim."),
    ("U8", "Automatic differentiation"),
]
mods = [
    ("env", "Environment setup"),
    ("python", "matplotlib"),
    ("opti", "scipy + metaheuristics"),
    ("tmm", "Mini-proj I: TMM filters"),
    ("meep", "FDTD with Meep"),
    ("eot", "Mini-proj II: EOT"),
    ("adjoint", "Adjoint inverse design"),
    ("qa", "QA mini-project: OPA"),
]
# theory unit -> lab module edges (§7 table)
edges = [
    ("U2", "opti"), ("U3", "opti"), ("U5", "opti"),
    ("U1", "tmm"), ("U3", "tmm"),
    ("U6", "meep"), ("U6", "eot"),
    ("U7", "adjoint"), ("U8", "adjoint"),
    ("U5", "qa"),
]

fig, ax = plt.subplots(figsize=(9.2, 6.4))
ax.set_xlim(0, 10)
ax.set_ylim(-0.6, 8.4)
ax.axis("off")

pos_u, pos_m = {}, {}
for i, (tag, label) in enumerate(units):
    y = 7.5 - i
    pos_u[tag] = (2.9, y)
    ax.add_patch(FancyBboxPatch((0.25, y - 0.32), 2.65, 0.68,
                                boxstyle="round,pad=0.06", fc="#E8F1F8", ec=BLUE, lw=1.4))
    ax.text(0.42, y, f"{tag}  {label}", va="center", ha="left", fontsize=9.2, color="#1a1a2e")
for i, (tag, label) in enumerate(mods):
    y = 7.5 - i
    pos_m[tag] = (6.6, y)
    ax.add_patch(FancyBboxPatch((6.6, y - 0.32), 2.9, 0.68,
                                boxstyle="round,pad=0.06", fc="#FDF3E3", ec=ORANGE, lw=1.4))
    ax.text(6.77, y, f"{tag}:  {label}", va="center", ha="left", fontsize=9.2, color="#1a1a2e")

for u, m in edges:
    (x0, y0), (x1, y1) = pos_u[u], pos_m[m]
    ax.annotate("", xy=(x1 - 0.05, y1), xytext=(x0 + 0.05, y0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3,
                                shrinkA=2, shrinkB=2, alpha=0.85,
                                connectionstyle="arc3,rad=-0.12"))

ax.text(1.55, 8.25, "Part I — Theory units", fontsize=11.5, ha="center", weight="bold", color=BLUE)
ax.text(8.05, 8.25, "Part II — Hands-on modules", fontsize=11.5, ha="center", weight="bold", color="#B0721E")
ax.text(5.0, -0.45, "Arrows: the theory a module draws on（模組使用的理論單元）",
        fontsize=9, ha="center", color=GREY)

out = Path(__file__).resolve().parent.parent / "assets" / "u01_roadmap.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
print(f"saved {out}")
