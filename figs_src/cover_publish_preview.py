"""Copy the latest preview artifacts into the tunnel-served directory.

Run:  python3 figs_src/cover_publish_preview.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad"
SERVE = os.path.join(SCRATCH, "serve")

shutil.copy(os.path.join(SCRATCH, "otid-cover-preview.html"), os.path.join(SERVE, "index.html"))
shutil.copy(os.path.join(HERE, "assets", "cover.svg"), os.path.join(SERVE, "cover.svg"))
shutil.copy(os.path.join(SCRATCH, "cover_render.png"), os.path.join(SERVE, "cover_render.png"))
print("serve/ updated")
