"""Zoomed crops of collision-risk zones for cover QC.

Run:  python3 figs_src/cover_crop.py
"""
from PIL import Image

SCRATCH = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad"
img = Image.open(f"{SCRATCH}/cover_check.png")
zones = {
    "zone_title_to": (0, 60, 720, 560),
    "zone_flag": (900, 140, 1350, 430),
    "zone_formula": (1000, 500, 1600, 1000),
}
for name, box in zones.items():
    crop = img.crop(box)
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
    crop.save(f"{SCRATCH}/{name}.png")
print("crops saved")
