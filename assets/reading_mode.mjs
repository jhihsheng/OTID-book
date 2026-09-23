// 閱讀模式按鈕：隱藏左側目錄欄與右側大綱，只留內文。
// 由 footer.md 的 {anywidget} 載入；按鈕掛在 document.body，跨頁導覽時保留同一顆。
const KEY = "otid-reading-mode";
const CLS = "otid-reading";

function load() {
  try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; }
}
function save(on) {
  try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* 私密視窗等情況：只是不記住 */ }
}

function render({ el }) {
  el.style.display = "none";
  if (document.getElementById("otid-reading-toggle")) return;

  const root = document.documentElement;
  const btn = document.createElement("button");
  btn.id = "otid-reading-toggle";
  btn.type = "button";

  const apply = (on) => {
    root.classList.toggle(CLS, on);
    btn.textContent = on ? "結束閱讀模式" : "閱讀模式";
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.title = on ? "顯示目錄與大綱" : "隱藏目錄與大綱，只留內文";
  };

  btn.addEventListener("click", () => {
    const on = !root.classList.contains(CLS);
    apply(on);
    save(on);
  });

  apply(load());
  document.body.appendChild(btn);
}

export default { render };
