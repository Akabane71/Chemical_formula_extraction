import os
from app.tasks.celery_app import celery_app
from ultralytics import YOLO
from app.core.config import STATIC_DIR,TMP_PDF_IMGS_DIR,AZURE_BLOB_PDF_IMG_DIR
import fitz  # PyMuPDF
import cv2
import numpy as np
from pathlib import Path

import asyncio
DPI = 300
CONF_THRES = 0.25
IOU_THRES = 0.45

yolo_model = YOLO(f'{STATIC_DIR}/moldet_yolo11l_640_general.pt')  # 加载预训练的 YOLOv8 模型

def abs_path_to_web_path(abs_path: Path) -> str:
    """
    将绝对路径转换为 Web 可访问的相对路径
    """
    abs_path = str(abs_path)
    tmp_dir = str(TMP_PDF_IMGS_DIR)
    return abs_path.replace(tmp_dir, "/static").replace("\\", "/")


def render_pdf_page(page, dpi: int):
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = cv2.imdecode(
        np.frombuffer(pix.tobytes("png"), dtype="uint8"),
        cv2.IMREAD_COLOR,
    )
    return img


async def publish_imgs_to_azure_blob(
    img_paths: list[Path],
    azure_dir_name: str,
    max_concurrency: int = 8,
) -> list[str]:
    """
    将图片上传到 Azure Blob 存储，并返回其 URL 列表
    """
    from app.clients.azure_blob_client import upload_img_to_azure_blob

    if not img_paths:
        return []

    semaphore = asyncio.Semaphore(max_concurrency)

    async def _upload_one(img_path: Path) -> dict:
        async with semaphore:
            blob_url = await upload_img_to_azure_blob(
                img_path=str(img_path),
                upload_dir=azure_dir_name,
            )
            return {"img_path": img_path, "blob_url": blob_url}

    tasks = [_upload_one(img_path) for img_path in img_paths]
    return await asyncio.gather(*tasks)


@celery_app.task
def process_pdf_with_yolo(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    results = []
    pdf_dir_name = os.path.basename(pdf_path).replace(".pdf", "")
    out_dir = os.path.join(TMP_PDF_IMGS_DIR, pdf_dir_name)
    os.makedirs(out_dir, exist_ok=True)
    imgs_paths = []
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        img = render_pdf_page(page, DPI)
        h, w = img.shape[:2]

        # YOLO 推理
        yolo_results = yolo_model.predict(
            source=img,
            conf=CONF_THRES,
            iou=IOU_THRES,
            verbose=False,
        )
        r = yolo_results[0]
        page_result = []
        if r.boxes is not None and len(r.boxes) > 0:
            for det_idx, box in enumerate(r.boxes):
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = xyxy.tolist()
                x1 = max(0, min(x1, w - 1))
                y1 = max(0, min(y1, h - 1))
                x2 = max(0, min(x2, w))
                y2 = max(0, min(y2, h))
                crop = img[y1:y2, x1:x2]
                if crop.size == 0:
                    continue
                conf = float(box.conf[0].cpu().numpy())
                cls = int(box.cls[0].cpu().numpy())
                out_path = os.path.join(
                    out_dir, f"p{page_idx+1:04d}_d{det_idx:03d}_c{cls}_conf{conf:.2f}.png"
                )
                cv2.imwrite(out_path, crop)
                page_result.append({
                    "det_idx": det_idx,
                    "class": cls,
                    "conf": conf,
                    "crop_path": abs_path_to_web_path(out_path),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                })
                imgs_paths.append(out_path)
        results.append({"page": page_idx, "detections": page_result})
        
    # 上传到azure blob存储中
    blob_urls = asyncio.run(publish_imgs_to_azure_blob(imgs_paths, AZURE_BLOB_PDF_IMG_DIR + "/" + os.path.basename(pdf_path)))
    # blob_urls格式：list[{"img_path":..., "blob_url":...}]
    
    return {
        "pages": results,
        "blob_urls": blob_urls,
        "origin_pngs_dir": imgs_paths,
    }
