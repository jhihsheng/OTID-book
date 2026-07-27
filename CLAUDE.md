# CLAUDE.md — OTID Course Book（Jupyter Book 2 / MyST）· v2

> **Mission.** Build a complete Jupyter Book 2 (MyST engine) course website for
> **「最佳化理論與反向設計」 Optimization Theory and Inverse Design (OTID)**,
> NYCU 114-2, 當期課號 **535417**, 永久課號 **EEEO30135**, instructor **Jhih-Sheng Wu 吳致盛**
> (Dept. of Photonics 光電碩).
>
> The site lives in a **new repo `jhihsheng/OTID-book`** and deploys to GitHub Pages at
> **`https://jhihsheng.github.io/OTID-book/`**（decided — §2.2）.
>
> Structure: **Part I = theory, organized by UNIT（單元）, not by week — 老師 sets the pacing
> himself.** Eight units, authored from scratch by you following §10. **Part II = hands-on labs and
> mini-projects — the existing notebooks from the `jhihsheng/OTID` repo, mirrored into this repo
> (§2.3) and integrated, never rewritten.**
>
> The look, feel, config conventions, and deployment pipeline **must mirror the instructor's existing
> JB2 site** `jhihsheng/eeqt30001` (https://jhihsheng.github.io/eeqt30001/). Clone it read-only and
> copy the files listed in §3.

---

## 1. Ground-truth sources（priority order）

1. **This file.** Where it conflicts with anything else, this file wins; where it is silent, ask 老師.
2. **Appendix A** — the official NYCU course outline（課程綱要）, transcribed verbatim from 老師's
   DOCX. Authoritative for official facts（課號、教室、學分、教科書、官方每週進度、官方評量）.
3. **The course PPT syllabus** — facts transcribed in §1.1（authoritative for operative grading
   detail, presentation rules, resources, coding requirements）.
4. **Template repo** `https://github.com/jhihsheng/eeqt30001` — authoritative for style/config/deploy.
5. **`jhihsheng/OTID`** — authoritative for Part II content（single source of truth for notebooks）.

Where the PPT and the official outline differ（e.g., grading granularity）, present the PPT's
operative version on the site and note the official wording — they are compatible（§7.3）. Schedule
policy everywhere: 進度以上課宣布為準（滾動式調整）; the official weekly table is the formal record.

### 1.1 Facts from the syllabus PPT（authoritative for operations）

- Instructor: 吳致盛 Jhih-Sheng Wu ｜ jwu@nycu.edu.tw ｜ Office EO413 (TKP building)
  ｜ Office hour Mon 10:00–12:00, appointment by email.
- Semester 114-2: 16 weeks, 2026-02-23 → 2026-06-08; **Midterm = Week 9, 2026-04-20**.
- Course structure: Optimization Theory lectures 6–7 wks; Inverse Design lectures 2–3 wks;
  Coding Lab 1–2 wks; Mini-Projects 4 wks; Research presentations 1–2 wks.
- Textbook emphasis: **Chong & Zak, *An Introduction to Optimization*, 3rd ed., Wiley, 2008**
  (e-book via NYCU library). **Reading scope: Ch. 1–15, with Ch. 12（Solving Linear Equations）
  excluded**（老師裁定）; Ch. 15（Intro to LP）covered briefly. Author's course site:
  https://www.engr.colostate.edu/~echong/ece520/
- Operative grading: **Homework 40% ｜ Midterm 30% ｜ Mini-Projects 15% ｜ Presentation 15%** +
  in-class participation bonus. 學到的能力才是重點！作業與考試以簡單與基礎為原則。
- Final presentation: groups of 2–4（視修課人數）; paper chosen **before midterm**; report = PPT/PDF
  slides 8–15 pages (45%); talk 10 min + 5 min Q&A (50%); everyone must ask questions (5%).
  Suggested directions: quantum optics, nano optics, silicon photonics, machine learning,
  metasurfaces, 自己實驗室的題目, 自己的興趣. Trend keywords: Transformers, PINN, FNO, Quantum Algorithms.
- Coding requirements: Python + Linux + laptop; Windows 用 WSL; install Anaconda, JupyterLab, MEEP;
  optional Julia. Tutorials live in `jhihsheng/OTID`.
- Reference list from the PPT（core of the **citation whitelist**, §13）:
  - Molesky, Lin, Piggott et al., "Inverse design in nanophotonics," *Nature Photonics* **12**, 659–670 (2018).
  - S. G. Johnson, "Notes on adjoint methods," MIT 18.336: https://math.mit.edu/~stevenj/18.336/adjoint.pdf
  - Hammond, Oskooi, Chen, Lin, Johnson, Ralph, "High-performance hybrid time/frequency-domain topology optimization…," *Opt. Express* **30**, 4467–4491 (2022).
  - Deep learning for inverse design review: *Photonics Research* **9**(5), B182–B200 (2021).
  - PhD theses: Jan Petykiewicz (Stanford), *Active nanophotonics*; Logan W. Su (Stanford), *Computational nanophotonic design* (2020).
  - Example applications: *Phys. Rev. Lett.* **122**, 213902 (2019); *IEEE Trans. Antennas Propag.* **70**(4), 2841–2854 (2022).
  - Software: MEEP (https://meep.readthedocs.io — incl. the Adjoint Solver tutorial), spins-b (https://github.com/stanfordnqp/spins-b), angler (https://github.com/fancompute/angler).

### 1.2 Facts from the official outline（see Appendix A for the full text）

- 開課單位 光電碩；學分 3.00；選修；上課時間/教室 **M567-EO115[GF]**（週一 5–7 節，光復校區 EO115）。
- 先修：微積分、線性代數；先備：有修過計概/程式語言或程式經驗為佳。
- 官方教科書共三本：C&Z（同上）；**Aarts & Korst, *Simulated Annealing and Boltzmann Machines*,
  Wiley, 1989**；**Kochenderfer & Wheeler, *Algorithms for Optimization*, MIT Press, 2019**。
  → 後兩本加入引用白名單，並列入 `resources.md`。
- 官方課程大網單元：Methods for Optimization（gradient, Newton, NN, SA, QA, **Monte Carlo**）、
  Applications（**濾波器反向設計、1D 光柵設計**）、Projects（最佳化方法實作）、Mathematical Review。
  → Monte Carlo 必須有明確的單元位置（U5 sec1，§10）; the two application themes frame Part II（§11.1）.
- 官方評量：平時習作 40%、期中考 30%、期末專題 30%。

---

## 2. Architecture decisions（already made — do not relitigate）

### 2.1 Repo split
- **`jhihsheng/OTID-book`（this repo, new）** = the website. Create it fresh.
- **`jhihsheng/OTID`** = the students' hands-on repo. **Do not commit website files there; do not
  modify it at all.** Any fix its notebooks need is *proposed to 老師*, applied upstream by him.

### 2.2 URL（decided by 老師, 2026-07-27）
Site URL = **`https://jhihsheng.github.io/OTID-book/`**. GitHub Pages project URLs are fixed by repo
name; 老師 has confirmed keeping `OTID-book`（no repo renaming to obtain `/OTID/`）. The deploy
workflow's `BASE_URL: /${{ github.event.repository.name }}` resolves this automatically.

### 2.3 Notebook mirroring（single source of truth stays in `OTID`）
`computing_lab/` in this repo is a **committed mirror** of `OTID`'s `computing_lab/`, refreshed by
`sync_labs.sh`（§4.1）— the same dev-repo→public-site sync pattern 老師 already uses in
`eeqt30001/build_jbook.sh`. Rules: **never hand-edit anything under `computing_lab/`**; to update,
run the script and commit the diff. CI needs no network step because the mirror is committed.

### 2.4 Everything else
- Engine: Jupyter Book 2 = MyST (`mystmd`). No JB1, no Sphinx.
- **Part I is organized by unit（unit01–unit08）, not weeks.** No dates on unit pages; pacing 由老師
  上課宣布. The official 16-week table lives only in `syllabus.md` as the formal record.
- Notebooks render **from stored outputs**; CI never executes anything（node + mystmd + typst only）.
- Part I figures = pre-rendered PNGs committed to the repo, generated by scripts in `figs_src/`
  (matplotlib only). Never rely on build-time execution.
- Language policy（mirror eeqt30001）: technical prose and headings in **English**; course-logistics
  text in **繁體中文 or bilingual**; inline 中文 in English prose where natural.

---

## 3. Copy these from `eeqt30001`（clone it read-only first）

```bash
git clone --depth 1 https://github.com/jhihsheng/eeqt30001 /tmp/eeqt30001
cp /tmp/eeqt30001/style.css        ./style.css        # keep verbatim（em 配色：象牙白底、Tangerine＋標楷體標題、深灰側欄）
cp /tmp/eeqt30001/JLW_icon.png     ./JLW_icon.png     # favicon（老師個人 icon）
cp -r /tmp/eeqt30001/.github       ./.github          # deploy.yml — keep typst pinned at 0.13.1 + Noto CJK step
```

- `deploy.yml` works verbatim（BASE_URL auto-resolves; typst 0.13.1 釘版：mystmd 產出的符號名在
  typst 0.15 已移除；`fonts-noto-cjk` install kept）.
- Follow the template's file-anatomy patterns: `intro.md` frontmatter carries the whole-book typst
  export + a `downloads:` list; content pages open with an English H1, a meta line, a
  ```` ```{note} Learning objectives ```` admonition, **Reading**, and an **Opening puzzle**.
- Whole-book typst PDF export includes **Part I pages only**（intro + syllabus + unit01–unit08）—
  notebooks break typst export; exclude them.
- Remind 老師 once at P0: new repo **Settings → Pages → Source = GitHub Actions**（一次性手動設定）.

---

## 4. Target repository layout（`OTID-book`）

```
OTID-book/
├─ myst.yml                    # §5
├─ intro.md                    # landing page（§7）
├─ syllabus.md                 # 官方課綱＋操作性補充（§8.1）
├─ resources.md                # textbooks + papers + software + how-to-read-papers（§8.2）
├─ setup.md                    # environment guide（§8.3）
├─ project.md                  # 期末專題與報告規則（§8.4）
├─ notation.md                 # global notation table（§9.6）
├─ question_bank.md            # 期中題庫公布位（placeholder, template pattern）
├─ footer.md                   # © 2026 Jhih-Sheng Wu（吳致盛）· NYCU 最佳化理論與反向設計（EEEO30135）
├─ style.css  /  JLW_icon.png
├─ sync_labs.sh                # §4.1 — mirrors computing_lab/ from jhihsheng/OTID
├─ unit01/ … unit08/           # Part I，每單元 index.md + sec1–sec3.md（§10；U3、U5 另有 sec4）
├─ labs/                       # Part II module index pages（§11）— thin .md pages only
│   ├─ index.md  ├─ env.md  ├─ python.md  ├─ opti.md  ├─ tmm.md
│   ├─ meep.md   ├─ eot.md  ├─ adjoint.md └─ qa.md
├─ figs_src/                   # python scripts generating Part I figures（uNN_*.py）
├─ assets/                     # committed PNGs + future scanned-notes PDFs（assets/unitNN.pdf）
├─ computing_lab/              # COMMITTED MIRROR of jhihsheng/OTID（§2.3）— never hand-edit
└─ .github/workflows/deploy.yml
```

### 4.1 `sync_labs.sh`

```bash
#!/usr/bin/env bash
# 鏡像 jhihsheng/OTID 的 computing_lab/ 進本 repo（唯讀鏡像；來源真相在 OTID repo）
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
git clone --depth 1 https://github.com/jhihsheng/OTID "$TMP/OTID"
rsync -av --delete --exclude '.git' "$TMP/OTID/computing_lab/" "$HERE/computing_lab/"
rm -rf "$TMP"
echo "computing_lab/ synced from jhihsheng/OTID — review 'git status', then commit."
```

Run at P0（initial mirror）and whenever 老師 updates the upstream repo.

## 5. `myst.yml`（starting skeleton — adapt, keep structure）

```yaml
version: 1
project:
  title: 最佳化理論與反向設計 Optimization Theory and Inverse Design
  authors:
    - name: Jhih-Sheng Wu 吳致盛
  github: https://github.com/jhihsheng/OTID-book
  numbering:
    headings: true
  toc:
    - file: intro.md
    - file: syllabus.md
    - file: resources.md
    - file: setup.md
    - title: "Part I — Theory（單元制）"
      children:
        - file: unit01/index.md
          children:
            - file: unit01/sec1.md
            - file: unit01/sec2.md
            - file: unit01/sec3.md
        # …repeat identically for unit02 … unit08（unit03 and unit05 additionally have sec4.md）
    - title: "Part II — Hands-On Labs & Mini-Projects"
      children:
        - file: labs/index.md
        - file: labs/env.md
          children:
            - file: computing_lab/00_connection_ssh.md
            - file: computing_lab/00_OTID_lab1.ipynb
        - file: labs/python.md
          children:
            - file: computing_lab/01_OTID_plot.ipynb
        - file: labs/opti.md
          children:
            - file: computing_lab/02_OTID_opti_tutorial_1.ipynb
            - file: computing_lab/03_OTID_opti_tutorial_2.ipynb
        - file: labs/tmm.md
          children:
            - file: computing_lab/04_OTID_transmission_TMM.ipynb
        - file: labs/meep.md
          children:
            - file: computing_lab/05_OTID_meep_tutorial_1.ipynb
            - file: computing_lab/06_OTID_meep_lab_1.ipynb
        - file: labs/eot.md
          children:
            - file: computing_lab/07_OTID_Trans_Ag_film.ipynb
        - file: labs/adjoint.md
          children:
            - file: computing_lab/08_OTID_meep_adjoint.ipynb
            - file: computing_lab/09_OTID_meep_adjoint_multi_freq.ipynb
              title: Multi-Frequency Adjoint Optimization with Meep
        - file: labs/qa.md
          children:
            - file: computing_lab/QA_lab_mini_project/quantum_annealing_lab_FULL.ipynb
            - file: computing_lab/QA_lab_mini_project/binary_OPA_SA_QA.ipynb
    - file: project.md
    - file: notation.md
    - file: question_bank.md
site:
  template: book-theme
  options:
    folders: true
    favicon: JLW_icon.png
    logo_text: 最佳化理論與反向設計
    style: style.css
  parts:
    footer: footer.md
```

Notes: notebook 09 has no title cell — the TOC `title:` override above fixes its display name with
**zero notebook edits**. If `myst build` warns about repo files not in the TOC（helper `.py`, media,
`README.md`）, silence via `project.exclude` patterns, never by adding them to the TOC.

## 6. Deployment

Push to `main` → Actions builds `myst build --all`（typst whole-book PDF, Part I only）then
`myst build --html` → deploy Pages. Local checks（§12）never require Pages.

---

## 7. Landing page `intro.md`

Frontmatter: typst whole-book export（articles = intro, syllabus, unit01/*…unit08/*）with
`id: otid-book`, plus `downloads:`（the book PDF now; per-unit scanned handwritten-notes PDFs
`assets/unitNN.pdf` are added **only when 老師 provides scans** — never link nonexistent files）.

Body（繁中為主）:

1. **H1 + course pitch.** Use the PPT framing: 重理論與實戰、滾動式調整、目標是理論基礎、coding
   skills、研究能力；三大主軸（Optimization Theory / Inverse Design / Hands-on coding + projects +
   presentations）；三個 objectives（common methods and their properties / hands-on experience in
   optics / catch the research trends）。加一句官方課程概述的精神：反向設計近年在量子、光學、電子元
   件領域受到重視，其核心即最佳化理論（古典與量子、梯度與非梯度法）。
2. **Part I unit overview table**（no dates — 進度以上課宣布為準）:

| 單元 | 主題 | C&Z 章節 | 頁面 |
|----|--------------------------------------------|--------|--------|
| U1 | Mathematical preliminaries 數學複習 | 1–5 | unit01 |
| U2 | Optimization basics & one-dimensional search | 6–7 | unit02 |
| U3 | Gradient, Newton, CG & quasi-Newton（＋LP 簡介） | 8–11, 15 | unit03 |
| U4 | Neural networks & optimization for deep learning | 13 | unit04 |
| U5 | Heuristics: Monte Carlo, GA/PSO/DE, simulated & quantum annealing | 14 | unit05 |
| U6 | Inverse design: concepts and landscape | — | unit06 |
| U7 | Adjoint method & density-based topology optimization | — | unit07 |
| U8 | Automatic differentiation & modern numerical computing | — | unit08 |

3. **Part II module overview table**:

| 模組 | 內容 | 對應理論單元 |
|------|------|------|
| env | 環境建置：VPN/SSH、conda、JupyterLab | — |
| python | matplotlib 科學繪圖 | — |
| opti | scipy 最佳化＋metaheuristics 實作 | U2, U3, U5 |
| tmm | Mini-project I：多層膜濾波器（TMM） | U1, U3 |
| meep | FDTD with Meep 入門與實驗 | U6 |
| eot | Mini-project II：EOT 電漿子晶格 | U6 |
| adjoint | Adjoint 反向設計實作（含多頻） | U7, U8 |
| qa | QA mini-project：量子退火與 binary OPA | U5 |

4. **關鍵日期**: 2026-02-23 開學｜2026-04-20 期中考（Week 9）｜2026-06-08 期末專題報告。
   官方每週進度見 [syllabus.md]；實際進度以上課宣布為準。
5. **評量**（§7.3 wording）+ pointers to `project.md` 與 `question_bank.md`。
6. Contact / office-hour / classroom block（M567-EO115[GF], Mon 5–7 節；office hour Mon 10:00–12:00
   EO413, email appointment）.

### 7.3 Grading wording（use everywhere grading appears）
平時作業 40%｜期中考 30%｜Mini-Projects 15%｜期末報告 Presentation 15%（＋課堂參與 bonus）。
註明：官方課綱之「期末專題 30%」＝ Mini-Projects 15% ＋ Presentation 15%。

---

## 8. Course-information pages

### 8.1 `syllabus.md`
Two parts. **(a) 官方課綱** — transcribe Appendix A faithfully（可重排為 MyST 表格；文字不改），
including the official 16-week schedule table, 教科書三本, 官方評量, 課程大網, 備註（智財權宣導）.
**(b) 操作性補充** — the PPT-level detail: office hour/location; reading scope Ch. 1–15 skip 12;
course-structure breakdown（theory/ID/lab/mini-projects/presentations 週數）; coding requirements;
schedule policy（以本網站與上課宣布為主，timetable 為正式紀錄）.

### 8.2 `resources.md`
Four sections. (a) **Textbooks**: C&Z（主課本, e-book via library, author course-site link）;
Aarts & Korst 1989（SA 專書）; Kochenderfer & Wheeler 2019（現代演算法視角；免費線上版可自行查證後
連結，不確定就只列書目）. (b) **Inverse-design reading list** = §1.1 whitelist items, each with 1–2
sentences of your own annotation. Open with the PPT's message: 最新的發展通常沒有教科書！需要自己整
理脈絡：論文、講義、線上資源——這是高手必經之路（well-known 的知識代表落後）。
(c) **Software**: MEEP（＋adjoint tutorial link）, spins-b, angler, scipy/nlopt, D-Wave Ocean.
(d) **如何找論文**（PPT slide 15）: 關鍵字 → Google Scholar / Web of Science → 判斷期刊（IF、老字
號、專家推薦）→ 判斷文章（摘要→介紹→結論→方法）。

### 8.3 `setup.md`
Environment guide: laptop + Linux/WSL requirement（Windows 在家先裝 WSL）, Anaconda, JupyterLab,
MEEP install pointers, optional Julia; link `computing_lab/00_connection_ssh.md`（VPN + MobaXterm +
container SSH — that file stays the detailed page in the TOC）; note the QA labs use
`dwave_env.yml`（link the file for download）.

### 8.4 `project.md`（期末專題與報告）
Merge official framing + PPT rules. Official: Projects = 最佳化方法實作（9 hr）; dedicated sessions
for problem/method/schedule 規劃 and troubleshooting/writing（見官方週次表）; 期末專題 30%（＝
mini-projects + presentation）. PPT rules: groups 2–4; paper chosen before midterm; report = slides
8–15 pages (45%); talk 10 min + 5 min Q&A (50%); everyone asks questions (5%); topic directions and
trend keywords（§1.1）. Placeholder line: 近期論文清單由老師於期中前公布於此頁。

---

## 9. Part I — global authoring standards（applies to every unit）

### 9.1 Page anatomy
- `unitNN/index.md`: English H1 title; meta line
  `**Unit N**｜Reading: C&Z Ch. …｜進度以上課宣布為準`;
  a ```` ```{note} Learning objectives (Unit N) ```` with 3–4 numbered, testable objectives;
  a **Reading** line; an **Opening puzzle** — one concrete paradox/question the unit resolves（see
  template `eeqt30001/week07/index.md` for the register: precise, slightly provocative, resolved by
  the material）.
- `sec1–sec3.md`（U3 and U5 also `sec4.md`）: the notes proper. Each section 600–1200 words of prose + math.
  **Prose carries the argument; equations are derived, not dumped.** Every nontrivial claim is either
  derived inline or explicitly pointed at a whitelist source.
- End of the last section: **Exercises** — 3–4 problems, 以簡單與基礎為原則, each with a hidden
  solution: ```` ```{dropdown} Solution ```` … ```` ``` ````.
- Where a unit connects to a Part II module, add a ```` ```{seealso} ```` admonition linking it.

### 9.2 Math conventions
- Display math `$$ … $$ (eq-uN-shortname)`; reference with `` {eq}`eq-uN-shortname` ``. Label every
  equation you reference; don't label ones you never reference.
- Notation follows C&Z where the book covers the topic（$f:\mathbb{R}^n\to\mathbb{R}$,
  iterates $\boldsymbol{x}^{(k)}$, $\boldsymbol{g}^{(k)}=\nabla f(\boldsymbol{x}^{(k)})$, Hessian
  $\boldsymbol{F}(\boldsymbol{x})$）. For ML/AD/photonics topics not in C&Z, use standard field
  notation and record every symbol in `notation.md`.
- Vectors bold lowercase, matrices bold uppercase, scalars italic. Consistency beats taste.

### 9.3 Figures
Each unit needs 2–4 figures. Scripts `figs_src/uNN_*.py` → PNG（150 dpi, matplotlib defaults,
colorblind-safe）in `assets/`; embed with ```` ```{figure} ```` + caption + `:name:`. Commit both
script and PNG. No decorative images.

### 9.4 Admonition palette（sparingly, purposefully）
`note` = learning objectives; `important` = the one idea of the section; `tip` = computational
advice; `warning` = classic pitfalls; `seealso` = lab links; `dropdown` = solutions & long details.

### 9.5 Depth calibration
簡要地介紹 — lecture notes, not a monograph. Target reader: first-year photonics MSc with
undergraduate 微積分＋線性代數（the official prerequisites）, reading each unit in 60–90 minutes.
Derive the load-bearing results fully（SD convergence rate on quadratics, the adjoint two-solve
argument, backprop on a two-layer net）; state-and-cite the rest.

### 9.6 `notation.md`
One table: symbol ｜ meaning ｜ first appears（link）. Updated as the final task of every unit phase.

---

## 10. Part I — unit-by-unit content specifications

> For each unit: `index.md` per §9.1, then the sections below. Bullets are **required content**, not
> suggestions; add connective tissue, don't remove items. No dates anywhere in Part I.

### Unit 01 — Mathematical Preliminaries 數學複習（C&Z Ch. 1–5）
- **sec1 — What is optimization?** Standard form $\min f(\boldsymbol{x})$ s.t.
  $\boldsymbol{x}\in\Omega$; objective/decision variables/feasible set; taxonomy（unconstrained vs
  constrained, continuous vs discrete, convex vs nonconvex, local vs global; gradient-based vs
  gradient-free — the course's organizing fork）. Three photonics motivating examples foreshadowing
  the labs: multilayer filter design（TMM, labs/tmm）, EOT plasmonic lattice（labs/eot）,
  waveguide-bend topology optimization（labs/adjoint — mention the `bend_waveguide.mp4` result）.
  Course roadmap figure: units feeding the hands-on modules.
- **sec2 — Linear algebra review.** Vector spaces, linear independence, rank; inner products & norms;
  eigenvalues/eigenvectors of symmetric matrices, orthogonal diagonalization; quadratic forms;
  positive (semi)definiteness — eigenvalue test and Sylvester/leading-principal-minor test（worked
  2×2 and 3×3 examples）.
- **sec3 — Geometry & calculus.** Line segments, hyperplanes, convex sets（definition + pictures）;
  level sets; sequences/limits/continuity（brisk）; differentiability: gradient, Jacobian, Hessian,
  chain rule, directional derivative $\boldsymbol{d}^{\!\top}\nabla f$; **Taylor's theorem to second
  order** — flagged as the engine of everything after（label it; every later unit cites it）.
- Figures: level sets + gradient field of a quadratic; convex vs nonconvex set.
- Exercises: PD test on a given matrix; compute gradient+Hessian; second-order Taylor expansion of a
  2-D function; classify its stationary point.

### Unit 02 — Optimization Basics & One-Dimensional Search（C&Z Ch. 6–7）
- **sec1 — Problem formulation & optimality conditions.** 最佳化問題建模（official course goal #2）:
  from an engineering wish to $\min f$, choosing variables/objective/constraints — one worked
  modeling example. Local/global minimizers; feasible directions; **FONC**（interior:
  $\nabla f=\boldsymbol{0}$）, **SONC**（Hessian PSD）, **SOSC**（PD ⇒ strict local min）; worked
  example including a saddle where FONC holds and SONC fails; why every later algorithm's stopping
  criterion comes from these conditions.
- **sec2 — Bracketing methods.** Unimodality; golden-section（derive the ratio）; Fibonacci search
  (statement of optimal reduction); reduction-factor comparison table.
- **sec3 — Derivative-based 1-D + line search.** Bisection on $f'$; Newton's 1-D method（derive from
  Taylor; quadratic convergence; divergence example）; secant method; **order of convergence**
  definitions; modern supplement: **backtracking/Armijo line search**（condition, pseudocode）—
  bridge to how multi-D methods actually choose step sizes.
- Figures: golden-section interval shrinkage; Newton tangent construction incl. a failure case.
- Exercises: two golden-section iterations by hand; Newton on $f(x)=x^4$ vs $x^2$（compare rates）;
  check an Armijo condition numerically.

### Unit 03 — Gradient, Newton, CG & Quasi-Newton Methods（C&Z Ch. 8–11, 15; Ch. 12 skipped）
- **sec1 — Steepest descent.** $\boldsymbol{x}^{(k+1)}=\boldsymbol{x}^{(k)}-\alpha_k\boldsymbol{g}^{(k)}$;
  exact line search on quadratics; **full derivation of the convergence-rate bound via the condition
  number $\kappa$** and the zig-zag phenomenon; preconditioning as the fix（pays off in U4's Adam
  discussion）.
- **sec2 — Newton's method in $\mathbb{R}^n$.** Derivation from second-order Taylor; quadratic
  convergence（statement + conditions）; what breaks（indefinite Hessian, cost）;
  **Levenberg–Marquardt modification**; one-line pointer to Gauss–Newton for least squares.
- **sec3 — CG and quasi-Newton.** Conjugate directions; why a quadratic in $\mathbb{R}^n$ solves in
  $n$ steps; the CG algorithm; Fletcher–Reeves vs Polak–Ribière; restarts for non-quadratics.
  Quasi-Newton: secant condition; rank-one; **DFP and BFGS**（update formulas exactly as in C&Z;
  PD preservation; BFGS as the workhorse; mention L-BFGS — used by `nlopt`/scipy in the labs）.
- **sec4 — A glance at linear programming（short, Ch. 15）.** LP standard form; feasible polytope
  and vertex optima（picture）; that simplex and interior-point methods exist（no algorithms）; where
  LP shows up in engineering; pointer to C&Z Part III. One `note` records that Ch. 12（linear
  equations/least squares）is deliberately skipped.
- Figures: **SD zig-zag vs CG path on an ill-conditioned quadratic**（the signature figure）;
  log-scale convergence comparison SD/CG/Newton/BFGS on one quadratic; LP polytope sketch.
- Exercises: two SD steps by hand; verify conjugacy of given directions; one BFGS update on a 2×2
  problem.

### Unit 04 — Neural Networks & Optimization for Deep Learning（C&Z Ch. 13 + modern supplements）
- **sec1 — Architecture.** Single neuron → MLP; activations（sigmoid/tanh/ReLU, why ReLU won）;
  universal approximation（statement only）; loss functions; an NN is a parametrized function and
  training is unconstrained optimization — the explicit bridge from U2–U3.
- **sec2 — Backpropagation & depth.** Forward pass as a computational graph; **derive backprop for a
  two-layer MLP explicitly**（the unit's load-bearing derivation）; vanishing/exploding gradients;
  initialization（Xavier/He, one paragraph）; **residual connections** — identity path, gradient
  highway, why depth becomes trainable（cite He et al., CVPR 2016）; batch norm in one paragraph.
- **sec3 — Optimizers.** SGD and minibatching（noise as a feature, not only a bug）; momentum/heavy
  ball; Nesterov（statement）; AdaGrad → RMSProp → **Adam**（full update equations + bias correction;
  cite Kingma & Ba 2015）; AdamW/weight decay in brief; LR schedules（warmup, cosine — brief）;
  unifying view: **Adam ≈ SD with an adaptive diagonal preconditioner**（tie back to U3 sec1）.
- Figures: computational graph of a small MLP; optimizer trajectories（SD vs momentum vs Adam）on
  Rosenbrock.
- Exercises: backprop by hand on a 1-hidden-unit net; one Adam step numerically; show how a residual
  block changes the gradient of a deep composition.
- `seealso`: presentation-topic trends（PINN, FNO, Transformers）live in `project.md`.

### Unit 05 — Heuristic Methods: Monte Carlo, Population-Based Algorithms, SA & QA（C&Z Ch. 14 + supplements; four sections）
- **sec1 — Monte Carlo methods & global search.** Why gradient methods fail on nonconvex/discrete
  landscapes; naive/uniform random search and multistart; **Monte Carlo as a computational
  principle** — random sampling for estimation and for search; the **Metropolis algorithm**
  （accept/reject, detailed-balance intuition, cite Metropolis et al. 1953）and the MCMC idea in one
  page; no-free-lunch in one sentence. This section covers the official outline's「Monte Carlo
  method」unit.
- **sec2 — Population-based metaheuristics: GA, PSO, DE（taught content, not asides）.**
  **Genetic algorithms**: encoding/representation, fitness, selection（roulette/tournament）,
  crossover, mutation, elitism; schema intuition in one paragraph（C&Z Ch. 14 treatment; K&W
  population-methods chapters as the modern companion）. **Particle swarm optimization**: the
  velocity/position updates with inertia $w$ and cognitive/social coefficients $c_1,c_2$ — give the
  update equations explicitly; global-best vs local-best topology in one remark; cite Kennedy &
  Eberhart 1995. **Differential evolution**: mutant vector
  $\boldsymbol{v}=\boldsymbol{x}_{r_1}+F(\boldsymbol{x}_{r_2}-\boldsymbol{x}_{r_3})$（DE/rand/1）,
  binomial crossover with rate $CR$, greedy selection; why DE is a strong default for continuous
  black-box problems; cite Storn & Price 1997. Close the section with a **comparison table**
  （mechanism ｜ continuous/discrete suitability ｜ key hyperparameters ｜ when to reach for it）
  covering random search, GA, PSO, DE, SA.
- **sec3 — Simulated annealing.** Physical annealing analogy; SA = Metropolis + a cooling schedule;
  acceptance $\min\{1, e^{-\Delta E/T}\}$（cite Kirkpatrick, Gelatt & Vecchi 1983; book treatment:
  Aarts & Korst 1989）; logarithmic guarantee vs geometric practice; full pseudocode; hyperparameter
  guidance（initial $T$ from acceptance ratio, stopping）.
- **sec4 — Quantum annealing.** **Ising Hamiltonian**
  $H=\sum_i h_i s_i+\sum_{i<j}J_{ij}s_i s_j$ and **QUBO** form; exact Ising↔QUBO conversion;
  formulating problems as QUBO with the course's own example — **binary-phase optical phased array**
  （the QA mini-project）; adiabatic computation: transverse-field driver,
  $H(t)=A(t)\sum_i\sigma^x_i+B(t)H_{\text{problem}}$, adiabatic theorem（statement）; tunneling vs
  thermal hopping picture; **D-Wave practicalities**: minor embedding, chains & chain strength,
  annealing time, sampling; sober SA-vs-QA comparison（when QA helps, what's open）. Cite Kadowaki &
  Nishimori, *Phys. Rev. E* **58**, 5355 (1998).
- Figures: rugged landscape with thermal-hop vs tunnel arrows; annealing schedule $A(t),B(t)$;
  **best-so-far convergence curves of GA/PSO/DE/SA on a multimodal test function（e.g., Rastrigin）**
  — the unit's signature figure（`figs_src`, fixed seed, honest about run-to-run variance）.
- Exercises（4）: QUBO for 4-node max-cut（or number partitioning）; one Metropolis accept/reject
  computation; one combined by-hand step of PSO（velocity+position）and DE（mutant+crossover）;
  Ising↔QUBO conversion of a given instance.
- `seealso`: `labs/opti` — **notebook 03 implements PSO with exercises**（direct companion to sec2）
  — and `labs/qa`（sec4's mini-project）.

### Unit 06 — Inverse Design: Concepts and Landscape（no textbook; whitelist refs only）
- **sec1 — Forward vs inverse.** Forward: structure → response（Maxwell solvers）; inverse: desired
  response → structure; design space, **figure of merit (FoM)**, constraints; ill-posedness &
  non-uniqueness; why photonics inverse design matured（linear Maxwell physics, accurate fast
  solvers, adjoint efficiency, fabrication advances）— framed via Molesky et al. 2018.
- **sec2 — Parameterizations.** Taxonomy with a comparison table:（a）few-parameter/shape,
  （b）level-set,（c）**density-based / freeform topology optimization**; fabrication constraints
  （minimum feature size, binarization, connectivity）; the course's organizing fork made explicit:
  **continuous parameterization → gradients/adjoint（U7）; discrete/binary → heuristics SA/QA
  （U5）**.
- **sec3 — Method families & exemplars.** Adjoint-based TO; heuristic pipelines; ML approaches in
  brief（surrogates, tandem/generative nets — cite the Photonics Research 2021 review）; what a good
  FoM looks like（differentiable, well-scaled, physically meaningful）; local-minima reality and
  restarts; exemplars from the syllabus: PRL **122**, 213902 (2019); IEEE TAP **70**, 2841 (2022);
  the two Stanford theses as further reading. Tie to the official Applications themes: 濾波器反向設計
  （gradient/adjoint route → labs/tmm, labs/adjoint）與 1D 光柵設計（annealing route → labs/qa）.
- Figures: forward-vs-inverse schematic; parameterization taxonomy; the closed ID loop
  （parametrize → simulate → FoM → update）.
- Exercises: write an FoM for a specified filter target; classify parameterizations of two described
  devices; short-answer conceptual questions.

### Unit 07 — Adjoint Method & Density-Based Topology Optimization
- **sec1 — Discrete adjoint（the punchline unit）.** Setting: $J(\boldsymbol{x}(\boldsymbol{p}))$
  with constraint $\boldsymbol{A}(\boldsymbol{p})\boldsymbol{x}=\boldsymbol{b}$. Naive
  $\mathrm{d}J/\mathrm{d}\boldsymbol{p}$ needs one solve per parameter; **derive the adjoint system**
  $\boldsymbol{A}^{\!\top}\boldsymbol{\lambda}=(\partial J/\partial\boldsymbol{x})^{\!\top}$ and the
  gradient formula — **two solves total, independent of the number of parameters**. Do it both ways
  （chain rule and Lagrangian）following Johnson's 18.336 notes; forward-pointer: this *is*
  reverse-mode AD through a solver（U8）.
- **sec2 — Electromagnetic adjoint.** Frequency-domain Maxwell/Helmholtz operator as
  $\boldsymbol{A}(\varepsilon)$; the adjoint simulation = a second simulation with a source placed by
  the objective; role of Lorentz reciprocity; physical picture — the gradient
  $\delta J/\delta\varepsilon(\boldsymbol{r})$ from the overlap of forward and adjoint fields
  （present the interference interpretation; keep signs/conventions consistent with the Meep adjoint
  documentation, since the labs use it）.
- **sec3 — Density-based TO pipeline.** Design density $\rho\in[0,1]$ on a grid → **filtering**
  （conic/Gaussian radius = minimum feature）→ **projection**（tanh with steepness β）→ material
  interpolation $\varepsilon(\tilde\rho)$ → forward solve → FoM → adjoint gradient → optimizer
  （CCSA/MMA or L-BFGS via nlopt, as in the notebooks）→ **β-continuation** toward binary; robust /
  multi-frequency formulations（min over a frequency set — exactly notebook 09）; cite Hammond et al.
  OE 2022 as the modern reference implementation.
- Figures: block diagram of the TO loop; filter→project chain on a 1-D density profile; forward vs
  adjoint source placement schematic.
- Exercises: full adjoint derivation on a 2×2 linear system; count solves（naive vs adjoint）for
  $10^4$ parameters; predict the sign of a density update from a given field overlap.
- `seealso`: notebooks 08 & 09; Meep Adjoint Solver tutorial.

### Unit 08 — Automatic Differentiation & Modern Numerical Computing
- **sec1 — AD fundamentals.** Computational graphs; **forward mode**（dual numbers; JVP）;
  **reverse mode**（VJP; backprop as the special case）; cost asymmetry — forward scales with
  #inputs, reverse with #outputs, hence reverse mode for scalar losses; AD vs symbolic vs finite
  differences, **with the classic FD total-error-vs-step-size analysis and figure**（truncation vs
  roundoff）.
- **sec2 — AD through physics.** Differentiating through a linear solve — implicit-function-theorem
  view; **theorem-level statement: the adjoint method of U7 = reverse-mode AD applied to the
  solver**（close the loop explicitly）; checkpointing for time-stepping（why FDTD gradients are
  memory-hungry）; the ecosystem the labs actually use: `autograd` + Meep adjoint + `nlopt`; JAX and
  PyTorch in one paragraph each; failure modes（non-differentiable ops, truncated iterative solves）.
- **sec3 — Numerical-computing literacy.** Floating point: machine epsilon, catastrophic cancellation
  （one worked example）; vectorization/array programming（why the labs' numpy style matters）; a
  short GPU-parallelism paragraph; reproducibility（seeds）; ecosystem map of the course's stack
  （numpy/scipy/matplotlib/nlopt/meep/Ocean）. Close Part I with a half-page synthesis: **the modern
  inverse-design stack = U7 adjoint + U8 AD + U3 quasi-Newton + U5 global search for the discrete
  parts** — one paragraph, one diagram.
- Figures: forward vs reverse sweep on one graph; FD error vs $h$ log-log; the closing stack diagram.
- Exercises: dual-number forward-mode by hand; solve-count comparison; identify the failure mode in a
  described pipeline.

---

## 11. Part II — integrating the `computing_lab/` mirror

### 11.1 Module index pages（`labs/*.md`, thin — 150–300 words each）
`labs/index.md` presents Part II under the **official Applications framing**: two application
threads（濾波器反向設計 — gradient/adjoint route；1D 光柵設計 — annealing route）plus Projects
（最佳化方法實作）, and reproduces the module↔unit table from §7. Each module page contains: 1–2
paragraph orientation（what it does, which theory unit it uses — link it）; prerequisites;
deliverables; a **Colab link** where applicable（§11.3）; downloads for associated helper files.

| page | notebooks / files | theory link | notes |
|---|---|---|---|
| `labs/env.md` | `00_connection_ssh.md`, `00_OTID_lab1.ipynb` | — | VPN/SSH/conda; 3-hour setup lab |
| `labs/python.md` | `01_OTID_plot.ipynb` | — | matplotlib visualization |
| `labs/opti.md` | `02…tutorial_1`, `03…tutorial_2` | U2, U3, U5 | scipy optimize; metaheuristics — notebook 03 implements **PSO**（link U5 sec2） |
| `labs/tmm.md` | `04_OTID_transmission_TMM.ipynb` | U1, U3 | Mini-project I: multilayer filters; link `04_OTID_trans_TMM_zoa.py` as download |
| `labs/meep.md` | `05…tutorial_1`, `06…lab_1` | U6 | FDTD basics; note `meep_plot_style.py`, `mycmapls.py` |
| `labs/eot.md` | `07_OTID_Trans_Ag_film.ipynb` | U6 | Mini-project II: EOT; downloads `opt_eot.py`, `Trans_Ag_film.py`; media `trans_ag_film.mp4` |
| `labs/adjoint.md` | `08…adjoint`, `09…multi_freq` | U7, U8 | show `bend_waveguide.mp4`, `filter_id.mp4` on this page |
| `labs/qa.md` | `quantum_annealing_lab_FULL.ipynb`, `binary_OPA_SA_QA.ipynb` | U5 | D-Wave Ocean; download `dwave_env.yml` |

### 11.2 Rendering rules
- Notebooks render **from stored outputs**; do not configure execution anywhere.
- After the first full build, open every notebook page and verify: images under
  `computing_lab/img/` resolve; the `.mp4` files play or are at least downloadable — if MyST doesn't
  render a raw video reference inside a notebook, surface that video on the module page instead with
  a proper `{video}`/HTML embed or a download link. Report anything unfixable to 老師.

### 11.3 Colab links
Pattern（the template's assignment page uses the same trick）— **point at the source repo `OTID`,
not at this book repo**, since that is where students obtain runnable files:
`https://colab.research.google.com/github/jhihsheng/OTID/blob/main/computing_lab/<name>.ipynb`
Add for pure-Python notebooks only: 01, 02, 03, 04, and the two QA notebooks（note: D-Wave Ocean
installs via pip; hardware access needs a token）. **No Colab links** for Meep notebooks（05–09）—
Meep is conda-only; say so on `labs/meep.md`.

### 11.4 Notebook edits: none, ever
`computing_lab/` is a mirror（§2.3）. Zero edits — the notebook-09 title problem is solved by the
TOC `title:` override（§5）. Any genuine upstream fix（typos, broken paths）is written up and
proposed to 老師 to commit in `jhihsheng/OTID`, then pulled here via `sync_labs.sh`.

---

## 12. Workflow, phases, and definition of done

Local commands（match template）:
```bash
npm install -g mystmd        # once
./sync_labs.sh               # refresh the computing_lab/ mirror（P0, and after upstream changes）
myst start                   # live preview while authoring
myst build --site            # syntax + cross-reference check（CI-parity）
myst build --html            # full static build before pushing
```

Phases — **stop at the end of each phase and report**（build status, files touched, open issues）:

- **P0 Scaffold.** Create `OTID-book`; §3 copies; `sync_labs.sh` + initial mirror commit; `myst.yml`;
  skeleton pages（every TOC file exists with an H1 and a one-line placeholder）; local build clean;
  push; Pages deploy green. Remind 老師 of the one-time Settings→Pages→Actions setting.
- **P1 Course pages + Part II.** Full `intro.md`, `syllabus.md`（incl. Appendix A transcription）,
  `resources.md`, `setup.md`, `project.md`, `question_bank.md`, all `labs/*.md`; notebooks in TOC
  with the 09 title override; §11.2 media audit done.
- **P2 Theory U1–U3.** One unit per working session.
- **P3 Theory U4–U5.**
- **P4 Theory U6–U8.**
- **P5 Polish.** Cross-links both directions（units `seealso` labs; labs link units）; `notation.md`
  complete; every figure captioned and `:name:`-d; whole-book typst PDF builds; final read-through;
  `myst build --site` warning-clean or each warning justified.

**Definition of done, per unit**: index + all required sections per §9.1/§10; every referenced
equation labeled and resolving; 2–4 committed figures with scripts; exercises with dropdown
solutions; `myst build --site` clean; notation table updated.

Commits: small, scoped, imperative — `unit03: CG and quasi-Newton notes`, `labs: module index
pages`, `p0: scaffold + deploy`.

---

## 13. Guardrails

1. **Mathematical correctness outranks coverage.** Derive rather than assert; check every formula
   against C&Z's conventions for C&Z topics. If you cannot verify a formula, mark it
   `TODO(老師確認)` rather than guessing.
2. **Citation whitelist.** You may cite: the three official textbooks（C&Z 3rd ed. 2008; Aarts &
   Korst 1989; Kochenderfer & Wheeler 2019）; everything in §1.1; official docs（Meep, scipy, nlopt,
   D-Wave Ocean, MyST）; and these classics: Metropolis et al., *J. Chem. Phys.* **21**, 1087
   (1953); Kirkpatrick, Gelatt & Vecchi, *Science* **220**, 671 (1983); Kadowaki & Nishimori, *PRE*
   **58**, 5355 (1998); Kennedy & Eberhart, Proc. IEEE ICNN, 1995 (PSO); Storn & Price, *J. Global
   Optim.* **11**, 341–359 (1997) (DE); Kingma & Ba, ICLR 2015 (Adam); He et al., CVPR 2016 (ResNet).
   **Nothing else without asking.** Never invent DOIs, page numbers, or author lists.
3. **Never edit anything under `computing_lab/`**（mirror; §2.3, §11.4）. Never touch the upstream
   `jhihsheng/OTID` repo. Never delete media.
4. CI stays notebook-execution-free and Python-free（node + mystmd + typst only）.
5. Do not link files that don't exist yet（scanned notes PDFs, the presentation paper list — marked
   placeholders instead）.
6. 滾動式調整 is course policy: Part I carries **no dates**; the only schedule tables are the key
   dates on `intro.md` and the official weekly table in `syllabus.md`.
7. When this spec is ambiguous, ask 老師 in your phase report; don't improvise silently.

---

## 14. Open questions for 老師（defaults applied until answered）

已裁定（2026-07-27）：URL = `/OTID-book/`；鏡像策略、Part II 模組切分、Colab 連結、語言比例均照
本文件預設執行。剩餘：

1. **手寫筆記掃描檔**：之後會提供 `assets/unitNN.pdf` 放進下載選單嗎？（default: 先留 placeholder，
   檔案到了才加連結）

---

## Appendix A — 官方課綱全文（114-2，course 535417 / EEEO30135）

> Claude Code: transcribe this into `syllabus.md` §(a) faithfully（版面可改為 MyST 表格，文字不改）。

國立陽明交通大學 National Yang Ming Chiao Tung University
114學年度 第2學期 最佳化理論與反向設計 Optimization Theory and Inverse Design 課程綱要

- 課程名稱：（中文）最佳化理論與反向設計（英文）Optimization Theory and Inverse Design
- 開課單位：光電碩｜永久課號：EEEO30135｜上課時間/教室：M567-EO115[GF]
- 授課教師：吳致盛｜學分數：3.00｜必／選修：選修｜開課年級：*
- 先修科目或先備能力：先修科目：微積分、線性代數；先備能力：有修過計算機概論、程式語言、或有程式
  經驗為佳。
- 課程概述與目標：反向設計 (inverse design) 在量子、光學、電子元件等領域在近年來受到重視，反向設
  計的核心為最佳化理論，我們將介紹各種經典的最佳化方法（古典與量子），主要可分為梯度法與非梯度
  法，並介紹近年來於機器學習與量子計算的最新發展，最後介紹實際應用與專題實作。
  1. 學習最佳化基礎理論 2. 最佳化問題建模與應用
- 教科書：
  1. Edwin K. P. Chong and Stanislaw H. Zak, "An Introduction to Optimization," Third Edition,
     Wiley-Interscience, New York, NY, 2008
  2. Aarts, Emile and Korst, Jan, "Simulated Annealing and Boltzmann Machines: A Stochastic Approach
     to Combinatorial Optimization and Neural Computing," Chichester / John Wiley & Sons, 1989
  3. Mykel J. Kochenderfer and Tim A. Wheeler, "Algorithms for Optimization," MIT Press, Cambridge,
     Massachusetts, United States, 2019

課程大網（單元主題｜內容綱要｜講授時數）：
- Methods for Optimization｜1. Gradient method 2. Newton's method 3. Neural networks
  4. Simulated annealing 5. Quantum annealing 6. Monte Carlo method｜24
- Applications｜1. 濾波器反向設計 2. 1D 光柵設計｜6
- Projects｜最佳化方法實作｜9
- Mathematical Review｜Linear algebra, geometry concepts, calculus｜6

教學要點概述：
1. 學期作業、考試、評量：評量方法：平時習作 40%、期中考試 30%、期末專題 30%。
2. 教學方法及教學相關配合事項：教材編選：以教科書為藍本，輔以參考資料及自編講義。
師生晤談：聯絡方式 email: jwu@nycu.edu.tw

每週進度表（週次｜上課日期｜課程進度、內容、主題）：
| 週 | 日期 | 主題 |
|----|------------|------------------------------|
| 1 | 2026-02-23（一）| Mathematical Review |
| 2 | 2026-03-02（一）| Basics of optimization problems |
| 3 | 2026-03-09（一）| One-dimension search |
| 4 | 2026-03-16（一）| Gradient related methods I |
| 5 | 2026-03-23（一）| Gradient related methods II |
| 6 | 2026-03-30（一）| Newton related methods |
| 7 | 2026-04-06（一）| Neural networks |
| 8 | 2026-04-13（一）| Heuristic methods |
| 9 | 2026-04-20（一）| 期中考週 |
| 10 | 2026-04-27（一）| Quantum annealing |
| 11 | 2026-05-04（一）| Monte Carlo method |
| 12 | 2026-05-11（一）| adjoint method 濾波器反向設計：梯度法 |
| 13 | 2026-05-18（一）| 專題實作：problem、method、schedule |
| 14 | 2026-05-25（一）| 1D 光柵設計：退火法 |
| 15 | 2026-06-01（一）| 專題實作：trouble shooting and writing |
| 16 | 2026-06-08（一）| 期末專題報告 |

備註：1. 請遵守智慧財產權觀念及勿使用不法影印教科書。2. 其他欄包含參訪、專題演講等活動。
