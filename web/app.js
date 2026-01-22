const btn = document.getElementById("uploadBtn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const extractList = document.getElementById("extractList");
const imageGrid = document.getElementById("imageGrid");
const fileInput = document.getElementById("pdfFile");

let pond = null;
if (window.FilePond && fileInput) {
  pond = FilePond.create(fileInput, {
    allowMultiple: false,
    labelIdle: "拖拽 PDF 到这里或 <span class='filepond--label-action'>点击选择</span>",
  });
  FilePond.setOptions({ credits: false });
}

const setStatus = (text, kind = "") => {
  statusEl.textContent = text;
  statusEl.classList.remove("busy", "ok", "fail");
  if (kind) {
    statusEl.classList.add(kind);
  }
};

const renderExtracted = (items) => {
  if (!items.length) {
    extractList.innerHTML = "<div class='field'>未发现结构化结果</div>";
    return;
  }
  extractList.innerHTML = items.map((item) => {
    const img = item.image_url
      ? `<img src="${item.image_url}" alt="formula">`
      : `<img src="" alt="formula" style="visibility:hidden">`;
    return `
      <div class="extract-card">
        ${img}
        <div class="field"><span>名称:</span> ${item.name || "-"}</div>
        <div class="field"><span>功能:</span> ${item.function || "-"}</div>
        <div class="field"><span>描述:</span> ${item.description || "-"}</div>
      </div>
    `;
  }).join("");
};

const renderImages = (pages) => {
  const allImages = pages.flatMap((p) => (p.images || []).map((i) => i.url).filter(Boolean));
  if (!allImages.length) {
    imageGrid.innerHTML = "<div class='field'>未发现图片</div>";
    return;
  }
  imageGrid.innerHTML = allImages.map((url) => `<img src="${url}" alt="img">`).join("");
};

btn.addEventListener("click", async () => {
  const file = pond ? (pond.getFile() ? pond.getFile().file : null) : fileInput.files[0];
  if (!file) {
    alert("请先选择 PDF 文件");
    return;
  }
  const form = new FormData();
  form.append("pdf_file", file);
  setStatus("处理中...", "busy");
  resultEl.querySelector("code").textContent = "{}";
  if (window.Prism) {
    Prism.highlightElement(resultEl.querySelector("code"));
  }
  extractList.innerHTML = "";
  imageGrid.innerHTML = "";
  try {
    const res = await fetch("/api/v1/workflow/pdf_workflow", { method: "POST", body: form });
    const data = await res.json();
    setStatus(res.ok ? "完成" : "失败", res.ok ? "ok" : "fail");
    resultEl.querySelector("code").textContent = JSON.stringify(data, null, 2);
    if (window.Prism) {
      Prism.highlightElement(resultEl.querySelector("code"));
    }
    if (res.ok) {
      const extracted = Array.isArray(data.extracted) ? data.extracted : [];
      renderExtracted(extracted);
      const pages = Array.isArray(data.pages) ? data.pages : [];
      renderImages(pages);
    }
  } catch (e) {
    setStatus("失败", "fail");
    resultEl.querySelector("code").textContent = String(e);
    if (window.Prism) {
      Prism.highlightElement(resultEl.querySelector("code"));
    }
  }
});
