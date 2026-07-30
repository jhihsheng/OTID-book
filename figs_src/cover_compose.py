"""Compose the final course cover: Blender render (JPEG, base64-embedded) + flag and
journal-style typography, written to assets/cover.svg.

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
  <title id="coverTitle">最佳化理論與反向設計 — 課程封面：星空下的最佳化地形與反向設計元件</title>
  <!-- 背景：Blender (Cycles) 渲染，figs_src/cover_blender.py；本檔由 figs_src/cover_compose.py 合成 -->
  <defs>
    <style>
      .kai   {{ font-family: 'DFKai-SB','BiauKai','Noto Serif CJK TC','Noto Serif TC',serif; }}
      .serif {{ font-family: Georgia,'Times New Roman',serif; }}
      .sans  {{ font-family: 'Helvetica Neue',Arial,'Noto Sans CJK TC','Noto Sans TC',sans-serif; }}
    </style>
  </defs>

  <image x="0" y="0" width="{W}" height="{H}" xlink:href="data:image/jpeg;base64,{b64}"/>

  <!-- ∇f = 0 小旗（面朝左，插在全域最大值） -->
  <g stroke="#12141c" stroke-width="2.5" stroke-linejoin="round">
    <line x1="1080" y1="332" x2="1080" y2="215" stroke="#4a5468" stroke-width="5.5" stroke-linecap="round"/>
    <line x1="1078" y1="330" x2="1078" y2="218" stroke="#7a86a0" stroke-width="1.5" stroke-linecap="round" opacity="0.8"/>
    <path d="M 1076,221 C 1043,214 1013,228 977,220 L 977,265 C 1013,273 1043,259 1076,266 Z" fill="#ee4466"/>
    <path d="M 1076,221 C 1043,214 1013,228 977,220 L 977,229 C 1013,237 1043,223 1076,230 Z" fill="#cf3355" stroke="none"/>
    <circle cx="1080" cy="212" r="4.5" fill="#7a86a0"/>
  </g>
  <text x="1026" y="252" text-anchor="middle" class="serif" font-size="20" font-style="italic"
        font-weight="bold" fill="#fff7ea">&#8711;f = 0</text>

  <!-- 場景小標籤 -->
  <text x="598" y="352" text-anchor="middle" class="sans" font-size="24" font-weight="bold"
        fill="#ff9585" fill-opacity="0.95">SA</text>
  <text x="548" y="472" class="sans" font-size="24" font-weight="bold"
        fill="#7ab8ff" fill-opacity="0.95">QA</text>
  <text x="1268" y="556" class="sans" font-size="24" font-weight="bold"
        fill="#7ce8a0" fill-opacity="0.95">SD</text>


  <!-- 最佳化公式（SD 起點旁） -->
  <text x="1120" y="790" class="serif" font-size="27" font-style="italic"
        fill="#fff7ea" fill-opacity="0.92">x<tspan dy="-11" font-size="18">(n+1)</tspan><tspan dy="11"> = x</tspan><tspan dy="-11" font-size="18">(n)</tspan><tspan dy="11"> &#8722; &#945;&#8711;f(x</tspan><tspan dy="-11" font-size="18">(n)</tspan><tspan dy="11">)</tspan></text>

  <!-- 背景展品標註 -->
  <g class="sans" font-size="17" fill="#8b96c8">
    <text x="340" y="398">拓樸最佳化</text>
    <text x="340" y="424" font-size="14">topology optimization</text>
    <text x="640" y="196">binary OPA</text>
    <text x="640" y="220" font-size="14">quantum annealing</text>
    <text x="1560" y="300" text-anchor="end">多層膜濾波器 10-layer filter</text>
  </g>

  <!-- 標題區 -->
  <text x="75" y="113" class="kai" font-size="84" font-weight="700" fill="#000000" opacity="0.5">最佳化理論與反向設計</text>
  <text x="72" y="110" class="kai" font-size="84" font-weight="700" fill="#fff7ea">最佳化理論與反向設計</text>
  <text x="75" y="162" class="sans" font-size="21" letter-spacing="2.5" fill="#9fd8e8">OPTIMIZATION THEORY AND INVERSE DESIGN</text>
  <rect x="77" y="186" width="180" height="5" rx="2.5" fill="#ee4466"/>
  <text x="75" y="220" class="sans" font-size="20" fill="#8b98c9">梯度與非梯度&#12539;古典與量子——從最佳化理論到光學反向設計</text>

  <!-- 右上資訊 -->
  <text x="1560" y="34" text-anchor="end" class="sans" font-size="20" fill="#93a0c8">NYCU 114-2&#12539;光電碩</text>
  <text x="1560" y="60" text-anchor="end" class="sans" font-size="20" fill="#93a0c8">EEEO30135</text>
  <text x="1560" y="86" text-anchor="end" class="sans" font-size="20" fill="#93a0c8">吳致盛 Jhih-Sheng Wu</text>
</svg>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({os.path.getsize(OUT)/1024:.0f} KB)")
