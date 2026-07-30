"""Generate the artifact preview page for the Blender cover (scratchpad output).

Run:  python3 figs_src/cover_preview_page.py
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = "/tmp/claude-1000/-home-jwu-OTID-book/689a37ca-f036-4c23-b387-17c9e73f49ab/scratchpad"

with open(os.path.join(HERE, "assets", "cover.svg"), encoding="utf-8") as f:
    svg = f.read()

html = """<meta charset="utf-8">
<title>OTID 課程封面預覽（Blender 3D）</title>
<style>
  :root {
    --bg: rgb(255, 252, 242); --ink: #1e1e1e; --muted: #6b7280; --faint: #8a8f98;
    --card-bg: #fffdf6; --card-border: #ddd6c6;
    --shadow: 0 12px 34px rgba(60, 55, 40, 0.16);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #17181a; --ink: #e8e6de; --muted: #a8adb6;
            --card-bg: #202226; --card-border: #3a3d42;
            --shadow: 0 12px 34px rgba(0, 0, 0, 0.5); }
  }
  :root[data-theme="light"] {
    --bg: rgb(255, 252, 242); --ink: #1e1e1e; --muted: #6b7280;
    --card-bg: #fffdf6; --card-border: #ddd6c6;
    --shadow: 0 12px 34px rgba(60, 55, 40, 0.16); }
  :root[data-theme="dark"] {
    --bg: #17181a; --ink: #e8e6de; --muted: #a8adb6;
    --card-bg: #202226; --card-border: #3a3d42;
    --shadow: 0 12px 34px rgba(0, 0, 0, 0.5); }
  body { background: var(--bg); color: var(--ink); margin: 0; padding: 2.5rem 1.25rem 4rem;
         font-family: Georgia, 'Times New Roman', 'DFKai-SB', 'BiauKai',
                      'Noto Serif CJK TC', 'Noto Serif TC', serif; line-height: 1.65; }
  main { max-width: 1120px; margin: 0 auto; }
  h1 { font-family: 'DFKai-SB', 'BiauKai', 'Noto Serif CJK TC', 'Noto Serif TC', serif;
       font-size: clamp(1.5rem, 3.5vw, 2.1rem); margin: 0 0 0.25rem; text-wrap: balance; }
  .sub { color: var(--muted); font-size: 0.95rem; margin: 0 0 1.75rem; }
  .cover-card { background: var(--card-bg); border: 1px solid var(--card-border);
                border-radius: 14px; box-shadow: var(--shadow);
                padding: clamp(0.5rem, 1.5vw, 1rem); }
  .cover-card svg { display: block; width: 100%; height: auto; border-radius: 8px; }
  h2 { font-family: 'DFKai-SB', 'BiauKai', 'Noto Serif CJK TC', 'Noto Serif TC', serif;
       font-size: 1.15rem; margin: 2.25rem 0 0.75rem; }
  ul.pts { margin: 0; padding-left: 1.3em; font-size: 0.95rem; }
  ul.pts li { margin: 0.35em 0; }
  .note { color: var(--faint); font-size: 0.88rem; margin-top: 2rem;
          border-top: 1px solid var(--card-border); padding-top: 1rem; }
</style>
<main>
  <h1>OTID 課程封面 v4 草圖 — 全息地形 × 光子晶片</h1>
  <p class="sub"><b>草圖版</b>（1600×1000、128 samples；定稿將以 3200×2000、320 samples 重渲）。深夜藍科技場景：發光的全息等高線地形（設計空間）懸浮在光子晶片上方，金色最佳化軌跡從晶片上的元件一路爬向 ∇f = 0。Q 版老師依系網照片重製：斜瀏海、方框眼鏡、深藍西裝、粉紫領帶。</p>
  <div class="cover-card">
__SVG__
  </div>
  <h2>畫面裡的反向設計內容</h2>
  <ul class="pts">
    <li><b>全息設計空間</b>：等高線＋方格的霓虹曲面懸浮在晶片上方（四角有投影器光束），邊緣淡出像一塊有界的全息面板 —— 抽象設計空間 ↔ 實體元件的正反向對映。</li>
    <li><b>最佳化敘事</b>：金色發光軌跡從晶片上的 TO 元件「躍上」全息面，x⁽⁰⁾ 起步、爬上局部極大、<b style="color:#c9a227">SA</b> 弧線跳過鞍部、<b style="color:#b03052">QA</b> 箭頭直接穿隧半透明山體，最後在全域最大值插旗 ∇f = 0。</li>
    <li><b>晶片三元件</b>（對應課程三條實作線）：拓撲最佳化波導彎（青色 blob＋光路）、Ising 自旋陣列（金／桃紅立柱，QA mini-project）、1D 光柵（金色繞射光束扇）。</li>
    <li><b>角色 v3</b>：依系網照片重製 —— 斜瀏海、方框眼鏡、眼神光、腮紅、深藍西裝、白襯衫粉紫領帶；一手歡呼、一手扶旗。</li>
    <li><b>排版</b>：暗色期刊封面式 —— 象牙白標題＋青色副標＋桃紅色條，晶片元件加小字標註。</li>
  </ul>
  <p class="note">產生流程全部進 repo：<b>figs_src/cover_blender.py</b>（場景＋渲染，含 --preview / --draft / --closeup 模式）→ <b>figs_src/cover_compose.py</b>（合成 assets/cover.svg）。可再調：霓虹濃淡、全息面透明度、視角、元件佈局、人物大小。</p>
</main>
"""

html = html.replace("__SVG__", svg)
out = os.path.join(SCRATCH, "otid-cover-preview.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", out, f"({os.path.getsize(out)/1024:.0f} KB)")
