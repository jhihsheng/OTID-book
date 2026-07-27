# Adjoint-Based Inverse Design with Meep

課程「濾波器反向設計——梯度路線」的終點站：**adjoint method**。兩次模擬（forward ＋ adjoint）就拿到對*所有*設計參數的梯度（理論推導見 [U7](../unit07/index.md)；與自動微分的關係見 [U8](../unit08/index.md)），配上 density-based 拓撲最佳化 pipeline（filter → project → β-continuation），讓 optimizer 自己長出結構。

- [Notebook 08：Adjoint Method with FDTD Solver Meep](../computing_lab/08_OTID_meep_adjoint.ipynb)
- [Notebook 09：Multi-Frequency Adjoint Optimization with Meep](../computing_lab/09_OTID_meep_adjoint_multi_freq.ipynb)（多頻 FoM——對應 U7 sec3 的 robust／multi-frequency formulation）

（Meep 系列，無 Colab——見 [meep 模組](meep.md)的說明。）

**成果影片**：

- [bend_waveguide.mp4](../computing_lab/bend_waveguide.mp4)／[bend_waveguide_id.mp4](../computing_lab/bend_waveguide_id.mp4)——波導彎折拓撲最佳化的演化過程。
- [filter_id.mp4](../computing_lab/filter_id.mp4)——濾波器反向設計（與 [tmm 模組](tmm.md)同一問題的 freeform 解）。

**先備需求**：[meep 模組](meep.md)；建議先讀 [U7](../unit07/index.md)。

**交付**：跑通 notebook 08；以 notebook 09 為基礎完成一個多頻設計實驗（結構、FoM 收斂曲線、最終頻譜）。
