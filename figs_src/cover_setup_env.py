"""Temporary helper: install bpy (Blender-as-Python-module) for cover rendering.

Run:  python3 figs_src/cover_setup_env.py
Not part of the Part I figure pipeline; safe to delete after the cover is rendered.
"""
import subprocess
import sys

pkgs = sys.argv[1:] or ["bpy"]
r = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--no-input", *pkgs],
    text=True,
)
sys.exit(r.returncode)
