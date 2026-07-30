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
  <h1>OTID 課程封面 v7 草圖 — 星空版（高俯角、無人物）</h1>
  <p class="sub"><b>草圖版</b>（1600×1000、128 samples；定稿 3200×2000、320 samples）。本輪依指示：俯視角拉高、移除背景假光斑改為<b>程序化星場＋星雲</b>（兩層星點、電藍紫絲狀星雲）、人物移除（峰頂留 ∇f = 0 小旗）、文字全部上移不壓圖、三個反向設計範例改為<b>懸浮在地形後方的背景展品</b>。</p>
  <div class="cover-card">
__SVG__
  </div>
  <h2>自審清單（畫完後逐項檢查）</h2>
  <ul class="pts">
    <li>✓ 俯視角：相機抬至 30° 俯角，整片地形面板入鏡。</li>
    <li>✓ 背景：近黑靛藍＋細密星點（少數亮星）＋藍紫星雲絲，對齊您給的太空參考。</li>
    <li>✓ 無人物：峰頂只留白色光暈＋∇f = 0 小旗（面朝左避開光柵）。</li>
    <li>✓ 文字不壓圖：副標縮窄避開 OPA 光束扇、tagline 上移避開 TO 板、SA/QA/x⁽⁰⁾ 與三個展品標籤逐一核對過位置。</li>
    <li>✓ 反向設計展品在背景：左「拓撲最佳化」矽板（有機孔洞＋熱橙導光彎）、中「binary OPA」相位陣列（光束扇收束成垂直主瓣射向星空＋波前弧）、右「1D 光柵」（繞射光束扇）。</li>
    <li>✓ 光束維持亮核＋柔暈的雷射感。</li>
  </ul>
  <p class="note">尚未 build／未上線 —— 您點頭我才跑 3200×2000 定稿，定稿再過目一次，明確同意才部署。可調：星雲濃淡、星點密度、展品大小位置、旗子樣式、標籤文字。</p>
</main>
"""

html = html.replace("__SVG__", svg)
out = os.path.join(SCRATCH, "otid-cover-preview.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", out, f"({os.path.getsize(out)/1024:.0f} KB)")
