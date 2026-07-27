# 課程綱要 Syllabus

本頁分兩部分：**(a) 官方課綱**（忠實轉錄自 114-2 課程綱要；正式紀錄以 [NYCU timetable](https://timetable.nycu.edu.tw/?r=main/crsoutline&Acy=114&Sem=2&CrsNo=535417&lang=zh-tw) 為準）與 **(b) 操作性補充**（課堂實際運作細節）。實際進度以本網站與上課宣布為主（滾動式調整）。

## (a) 官方課綱

國立陽明交通大學 National Yang Ming Chiao Tung University
114 學年度 第 2 學期 最佳化理論與反向設計 Optimization Theory and Inverse Design 課程綱要

| 項目 | 內容 |
|------|------|
| 課程名稱 | （中文）最佳化理論與反向設計（英文）Optimization Theory and Inverse Design |
| 開課單位 | 光電碩 |
| 永久課號 | EEEO30135 |
| 上課時間/教室 | M567-EO115[GF] |
| 授課教師 | 吳致盛 |
| 學分數 | 3.00 |
| 必／選修 | 選修 |
| 開課年級 | * |
| 先修科目 | 微積分、線性代數 |
| 先備能力 | 有修過計算機概論、程式語言、或有程式經驗為佳 |

### 課程概述與目標

反向設計 (inverse design) 在量子、光學、電子元件等領域在近年來受到重視，反向設計的核心為最佳化理論，我們將介紹各種經典的最佳化方法（古典與量子），主要可分為梯度法與非梯度法，並介紹近年來於機器學習與量子計算的最新發展，最後介紹實際應用與專題實作。

1. 學習最佳化基礎理論
2. 最佳化問題建模與應用

### 教科書

1. Edwin K. P. Chong and Stanislaw H. Zak, "An Introduction to Optimization," Third Edition, Wiley-Interscience, New York, NY, 2008
2. Aarts, Emile and Korst, Jan, "Simulated Annealing and Boltzmann Machines: A Stochastic Approach to Combinatorial Optimization and Neural Computing," Chichester / John Wiley & Sons, 1989
3. Mykel J. Kochenderfer and Tim A. Wheeler, "Algorithms for Optimization," MIT Press, Cambridge, Massachusetts, United States, 2019

### 課程大網

| 單元主題 | 內容綱要 | 講授時數 |
|----------|----------|----------|
| Methods for Optimization | 1. Gradient method 2. Newton's method 3. Neural networks 4. Simulated annealing 5. Quantum annealing 6. Monte Carlo method | 24 |
| Applications | 1. 濾波器反向設計 2. 1D 光柵設計 | 6 |
| Projects | 最佳化方法實作 | 9 |
| Mathematical Review | Linear algebra, geometry concepts, calculus | 6 |

### 教學要點概述

1. 學期作業、考試、評量：評量方法：平時習作 40%、期中考試 30%、期末專題 30%。
2. 教學方法及教學相關配合事項：教材編選：以教科書為藍本，輔以參考資料及自編講義。

師生晤談：聯絡方式 email: <jwu@nycu.edu.tw>

### 每週進度表

| 週次 | 上課日期 | 課程進度、內容、主題 |
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

## (b) 操作性補充

- **師生晤談**：Office hour 週一 10:00–12:00，EO413（田家炳大樓）；其他時間 email 預約。
- **閱讀範圍**：主課本 Chong & Zak（3rd ed.）**Ch. 1–15，跳過 Ch. 12**（Solving Linear Equations）；Ch. 15（Intro to Linear Programming）簡要帶過。作者課程網站：<https://www.engr.colostate.edu/~echong/ece520/>。
- **課程結構週數配置**：Optimization Theory 講授 6–7 週；Inverse Design 講授 2–3 週；Coding Lab 1–2 週；Mini-Projects 4 週；Research presentations 1–2 週。
- **評量（操作版）**：平時作業 40%｜期中考 30%｜Mini-Projects 15%｜期末報告 Presentation 15%（＋課堂參與 bonus）。官方課綱之「期末專題 30%」＝ Mini-Projects 15% ＋ Presentation 15%。學到的能力才是重點！作業與考試以簡單與基礎為原則。
- **Coding 需求**：Python ＋ Linux ＋ 自備筆電；Windows 使用者請裝 WSL；安裝 Anaconda、JupyterLab、MEEP；Julia 選配。教學 notebooks 在 [`jhihsheng/OTID`](https://github.com/jhihsheng/OTID)（本站 Part II 完整收錄），環境安裝見[環境安裝頁](setup.md)。
- **進度政策**：滾動式調整——實際進度以本網站與上課宣布為主；上表為正式紀錄。
