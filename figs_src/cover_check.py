"""Rasterize assets/cover.svg for visual verification (not part of the build).

Run:  python3 figs_src/cover_check.py
"""
import os

import cairosvg

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad/cover_check.png"
cairosvg.svg2png(url=os.path.join(HERE, "assets", "cover.svg"),
                 write_to=OUT, output_width=1600, output_height=1000)
print("wrote", OUT)
