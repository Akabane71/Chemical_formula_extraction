from pathlib import Path
import cv2
import fitz  # PyMuPDF
from ultralytics import YOLO

PDF_PATH = "backend/muck/pdfs/1.pdf"
WEIGHTS_PATH = "backend/static/moldet_yolo11l_640_general.pt"
OUT_DIR = Path("tmp")

# 推理参数
DPI = 300
CONF_THRES = 0.25
IOU_THRES = 0.45

def render_pdf_page(page, dpi: int):
    # dpi -> 缩放矩阵
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    # pix.samples 是 RGB bytes
    img = cv2.imdecode(
        # 把 pixmap 转成 numpy 的简便方式：先写 png bytes 再 decode
        # 也可以直接 reshape，但要处理 stride，写法更繁琐
        __import__("numpy").frombuffer(pix.tobytes("png"), dtype="uint8"),
        cv2.IMREAD_COLOR,
    )
    return img

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    model = YOLO(WEIGHTS_PATH)

    doc = fitz.open(PDF_PATH)
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        img = render_pdf_page(page, DPI)
        h, w = img.shape[:2]

        # YOLO 推理（ultralytics 接受 BGR numpy）
        results = model.predict(
            source=img,
            conf=CONF_THRES,
            iou=IOU_THRES,
            verbose=False,
        )

        r = results[0]
        if r.boxes is None or len(r.boxes) == 0:
            continue

        # 导出每个 bbox 的裁剪图
        for det_idx, box in enumerate(r.boxes):
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            x1, y1, x2, y2 = xyxy.tolist()

            # 安全裁剪（防越界）
            x1 = max(0, min(x1, w - 1))
            y1 = max(0, min(y1, h - 1))
            x2 = max(0, min(x2, w))
            y2 = max(0, min(y2, h))

            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            conf = float(box.conf[0].cpu().numpy())
            cls = int(box.cls[0].cpu().numpy())

            # 文件名：页码 + 检测序号 + 类别 + 置信度
            out_path = OUT_DIR / f"p{page_idx+1:04d}_d{det_idx:03d}_c{cls}_conf{conf:.2f}.png"
            cv2.imwrite(str(out_path), crop)

    print("Done! Crops saved to:", OUT_DIR)

if __name__ == "__main__":
    main()
