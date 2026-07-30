"""Compose the final course cover: Blender render (JPEG, base64-embedded) + minimal
journal-style vector typography, written to assets/cover.svg.

Run after figs_src/cover_blender.py:
    python3 figs_src/cover_compose.py
"""
import base64
import io
import os

RENDER = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad/cover_render.png"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "cover.svg")

from PIL import Image

img = Image.open(RENDER).convert("RGB")
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=86, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode("ascii")
print(f"render {img.size}, jpeg {buf.getbuffer().nbytes/1024:.0f} KB")

W, H = 1600, 1000

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {W} {H}" role="img" aria-labelledby="coverTitle">
  <title id="coverTitle">最佳化理論與反向設計 — 課程封面：Q 版教授在 3D 最佳化地形的全域最大值插旗</title>
  <!-- 背景：Blender (Cycles) 渲染，figs_src/cover_blender.py；本檔由 figs_src/cover_compose.py 合成 -->
  <defs>
    <style>
      .kai   {{ font-family: 'DFKai-SB','BiauKai','Noto Serif CJK TC','Noto Serif TC',serif; }}
      .serif {{ font-family: Georgia,'Times New Roman',serif; }}
      .sans  {{ font-family: 'Helvetica Neue',Arial,'Noto Sans CJK TC','Noto Sans TC',sans-serif; }}
    </style>
  </defs>

  <image x="0" y="0" width="{W}" height="{H}" xlink:href="data:image/jpeg;base64,{b64}"/>

  <!-- 場景小標籤 -->
  <text x="660" y="264" text-anchor="middle" class="sans" font-size="25" font-weight="bold"
        fill="#ffd98f" fill-opacity="0.9">SA</text>
  <text x="300" y="360" class="sans" font-size="25" font-weight="bold"
        fill="#ff8ba3" fill-opacity="0.95">QA</text>
  <text x="70" y="516" class="serif" font-size="25" font-style="italic"
        fill="#cfe6f2" fill-opacity="0.8">x<tspan dy="-10" font-size="18">(0)</tspan></text>

  <!-- 晶片元件標註 -->
  <g class="sans" font-size="17" fill="#6f93a8">
    <text x="96" y="836">拓撲最佳化波導 topology optimization</text>
    <text x="505" y="843">Ising 自旋陣列 quantum annealing</text>
    <text x="1252" y="964">1D 光柵 grating</text>
  </g>

  <!-- 標題區（期刊封面式，暗色） -->
  <text x="75" y="163" class="kai" font-size="84" font-weight="700" fill="#000000" opacity="0.5">最佳化理論與反向設計</text>
  <text x="72" y="160" class="kai" font-size="84" font-weight="700" fill="#fff7ea">最佳化理論與反向設計</text>
  <text x="75" y="218" class="sans" font-size="25" letter-spacing="5" fill="#9fd8e8">OPTIMIZATION THEORY AND INVERSE DESIGN</text>
  <rect x="77" y="244" width="180" height="5" rx="2.5" fill="#ee4466"/>
  <text x="75" y="288" class="sans" font-size="20" fill="#7e93a3">梯度與非梯度&#12539;古典與量子——從最佳化理論到光學反向設計</text>

  <!-- 右上資訊（避開旗子） -->
  <text x="1552" y="58" text-anchor="end" class="sans" font-size="20" fill="#8fa2b0">NYCU 114-2&#12539;光電碩</text>
  <text x="1552" y="88" text-anchor="end" class="sans" font-size="20" fill="#8fa2b0">EEEO30135</text>
  <text x="1552" y="118" text-anchor="end" class="sans" font-size="20" fill="#8fa2b0">吳致盛 Jhih-Sheng Wu</text>
</svg>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({os.path.getsize(OUT)/1024:.0f} KB)")
