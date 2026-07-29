# 符號表 Notation

全站符號表，隨 Part I 各單元完成逐步更新。慣例（依 C&Z）：向量粗體小寫、矩陣粗體大寫、純量斜體。

| 符號 | 意義 | 首次出現 |
|------|------|----------|
| $f:\mathbb{R}^n\to\mathbb{R}$ | 目標函數 objective function | [U1 sec1](unit01/sec1.md) |
| $\boldsymbol{x}=(x_1,\dots,x_n)^{\top}$ | 決策變數向量 decision vector | [U1 sec1](unit01/sec1.md) |
| $\Omega\subseteq\mathbb{R}^n$ | 可行集合 feasible set | [U1 sec1](unit01/sec1.md) |
| $\boldsymbol{x}^{*}$ | 最小點 minimizer | [U1 sec1](unit01/sec1.md) |
| $\boldsymbol{x}^{\top}\boldsymbol{y}$，$\|\boldsymbol{x}\|$ | 內積 inner product、歐氏範數 Euclidean norm | [U1 sec2](unit01/sec2.md) |
| $\lambda_i$，$\boldsymbol{u}_i$ | 對稱矩陣之特徵值／正交特徵向量 | [U1 sec2](unit01/sec2.md) |
| $\boldsymbol{Q}=\boldsymbol{U}\boldsymbol{\Lambda}\boldsymbol{U}^{\top}$ | 正交對角化 orthogonal diagonalization | [U1 sec2](unit01/sec2.md) |
| $\boldsymbol{Q}>0$，$\boldsymbol{Q}\ge 0$ | 正定 positive definite、半正定 positive semidefinite（C&Z 記號，指二次形） | [U1 sec2](unit01/sec2.md) |
| $\Delta_k$ | 第 $k$ 個 leading principal minor（Sylvester 判別） | [U1 sec2](unit01/sec2.md) |
| $\kappa=\lambda_{\max}/\lambda_{\min}$ | 條件數 condition number | [U1 sec2](unit01/sec2.md) |
| $S_c=\{\boldsymbol{x}:f(\boldsymbol{x})=c\}$ | 等高集 level set | [U1 sec3](unit01/sec3.md) |
| $\nabla f(\boldsymbol{x})$ | 梯度（行向量）gradient | [U1 sec3](unit01/sec3.md) |
| $\boldsymbol{F}(\boldsymbol{x})$ | Hessian 矩陣（依 C&Z 記號） | [U1 sec3](unit01/sec3.md) |
| $\mathrm{D}\boldsymbol{h}$ | Jacobian 矩陣（$m\times n$） | [U1 sec3](unit01/sec3.md) |
| $\boldsymbol{d}$ | 方向向量 direction；$\boldsymbol{d}^{\top}\nabla f$ 為方向導數 | [U1 sec3](unit01/sec3.md) |
| $\alpha$ | 步長 step size（line search） | [U2 sec1](unit02/sec1.md) |
| $\tau=\frac{\sqrt5-1}{2}$，$\rho=1-\tau$ | 黃金分割縮減率／內點位置比 | [U2 sec2](unit02/sec2.md) |
| $F_k$ | Fibonacci 數（$F_1=F_2=1$） | [U2 sec2](unit02/sec2.md) |
| $p$，$C$ | 收斂階 order of convergence 與 rate | [U2 sec3](unit02/sec3.md) |
| $c$ | Armijo 充分下降常數（典型 $10^{-4}$） | [U2 sec3](unit02/sec3.md) |
| $\boldsymbol{g}^{(k)}=\nabla f(\boldsymbol{x}^{(k)})$ | 第 $k$ 迭代的梯度（C&Z 記號） | [U3 sec1](unit03/sec1.md) |
| $V(\boldsymbol{x})=f(\boldsymbol{x})-f^{*}$ | 收斂分析用的誤差量 | [U3 sec1](unit03/sec1.md) |
| $\boldsymbol{M}$ | preconditioner（$\boldsymbol{M}\approx\boldsymbol{Q}$） | [U3 sec1](unit03/sec1.md) |
| $\mu_k$ | Levenberg–Marquardt 位移參數 | [U3 sec2](unit03/sec2.md) |
| $\beta_k$ | CG 方向修正係數（FR／PR） | [U3 sec3](unit03/sec3.md) |
| $\Delta\boldsymbol{x}^{(k)}$，$\Delta\boldsymbol{g}^{(k)}$ | quasi-Newton 之位移與梯度差 | [U3 sec3](unit03/sec3.md) |
| $\boldsymbol{H}_k$ | inverse-Hessian 近似（quasi-Newton） | [U3 sec3](unit03/sec3.md) |
| $\boldsymbol{\theta}$ | 神經網路全體參數向量 | [U4 sec1](unit04/sec1.md) |
| $\sigma(\cdot)$ | activation function（sigmoid／tanh／ReLU） | [U4 sec1](unit04/sec1.md) |
| $\boldsymbol{W}_l$，$\boldsymbol{b}_l$ | 第 $l$ 層權重矩陣與偏置 | [U4 sec1](unit04/sec1.md) |
| $J(\boldsymbol{\theta})$ | empirical risk（訓練目標函數） | [U4 sec1](unit04/sec1.md) |
| $\boldsymbol{\delta}_l$ | 第 $l$ 層 error signal（backprop） | [U4 sec2](unit04/sec2.md) |
| $\hat{\boldsymbol{g}}$ | minibatch 梯度估計 | [U4 sec3](unit04/sec3.md) |
| $\beta$；$\beta_1,\beta_2$ | momentum 係數；Adam 一、二階動量係數 | [U4 sec3](unit04/sec3.md) |
| $\boldsymbol{m}$，$\boldsymbol{v}$，$\varepsilon$ | Adam 動量估計與數值穩定項 | [U4 sec3](unit04/sec3.md) |
| $\odot$ | 逐元素（Hadamard）乘積 | [U4 sec3](unit04/sec3.md) |
| $E(\cdot)$，$T$ | 能量（目標）函數與溫度（Metropolis／SA） | [U5 sec1](unit05/sec1.md) |
| $w$，$c_1$，$c_2$ | PSO 慣性、認知、社會係數 | [U5 sec2](unit05/sec2.md) |
| $F$，$CR$ | DE 縮放因子與 crossover 率 | [U5 sec2](unit05/sec2.md) |
| $s_i\in\{-1,+1\}$，$x_i\in\{0,1\}$ | Ising 自旋與 QUBO 二元變數（$s=2x-1$） | [U5 sec4](unit05/sec4.md) |
| $h_i$，$J_{ij}$ | Ising 局域場與耦合 | [U5 sec4](unit05/sec4.md) |
| $A(s)$，$B(s)$；$\sigma^{x,z}_i$ | 退火時程之 driver／problem 幅度；Pauli 算符 | [U5 sec4](unit05/sec4.md) |
| $\varepsilon(\boldsymbol{r})$ | 介電常數分布（結構） | [U6 sec1](unit06/sec1.md) |
| $\boldsymbol{p}$ | 設計參數向量（$\boldsymbol{p}\mapsto\varepsilon(\boldsymbol{r})$） | [U6 sec1](unit06/sec1.md) |
| $J(\boldsymbol{p})$ | figure of merit（FoM，設計目標函數） | [U6 sec1](unit06/sec1.md) |
| $\phi(\boldsymbol{r})$ | level-set 函數（邊界＝$\phi=0$） | [U6 sec2](unit06/sec2.md) |
| $\rho_i\in[0,1]$ | density-based TO 之像素密度 | [U6 sec2](unit06/sec2.md) |
| $\boldsymbol{A}(\boldsymbol{p})\boldsymbol{x}=\boldsymbol{b}$ | 離散化後的狀態方程（field solve） | [U7 sec1](unit07/sec1.md) |
| $\boldsymbol{\lambda}$ | adjoint 變數（$\boldsymbol{A}^{\top}\boldsymbol{\lambda}=(\partial J/\partial\boldsymbol{x})^{\top}$） | [U7 sec1](unit07/sec1.md) |
| $\tilde{\rho}$，$\bar{\rho}$ | 濾波後／投影後密度 | [U7 sec3](unit07/sec3.md) |
| $R$；$\beta$，$\eta$ | 濾波半徑（最小特徵）；投影銳度與門檻 | [U7 sec3](unit07/sec3.md) |
| $\dot{v}$；$\bar{v}$ | forward-mode 切向量（JVP）；reverse-mode adjoint（VJP） | [U8 sec1](unit08/sec1.md) |
| $\epsilon$（$\epsilon^2=0$） | dual number 之冪零元 | [U8 sec1](unit08/sec1.md) |
| $\varepsilon_{\text{mach}}\approx2.2\times10^{-16}$ | 機器精度 machine epsilon（float64） | [U8 sec1](unit08/sec1.md) |
| $D_h f$ | 步長 $h$ 之有限差分 | [U8 sec1](unit08/sec1.md) |
