import asyncio
import hashlib
from datetime import datetime, timezone

from app.services.process_pdf.upload_pdf import (
    check_pdf_content,
    check_pdf_file,
    upload_pdf_service,
)
from app.tasks.yolo_process_pdf import process_pdf_with_yolo
from app.tasks.ocr_process_pdf import process_pdf_with_ocr
from app.services.process_pdf.llm_actions import llm_process_pdf_action
from app.clients.mongo_client import get_pdf_results_collection


def _build_pdf_hash(pdf_bytes: bytes) -> str:
    return hashlib.sha256(pdf_bytes).hexdigest()


def _merge_ocr_yolo(ocr_pages: list[dict], yolo_result: dict) -> list[dict]:
    ocr_by_page = {page["page_id"]: page.get("text", "") for page in ocr_pages}
    yolo_by_page = {}
    for page in yolo_result.get("pages", []):
        page_id = page.get("page", 0) + 1
        yolo_by_page[page_id] = page.get("detections", [])

    url_by_img_path = {
        item["img_path"]: item["blob_url"] for item in yolo_result.get("blob_urls", [])
    }

    page_ids = sorted(set(ocr_by_page.keys()) | set(yolo_by_page.keys()))
    merged_pages = []
    for page_id in page_ids:
        detections = []
        for det in yolo_by_page.get(page_id, []):
            img_path = det.get("img_path")
            blob_url = url_by_img_path.get(img_path, "")
            detections.append(
                {
                    "url": blob_url,
                    "bbox": det.get("bbox", []),
                    "conf": det.get("conf", 0.0),
                }
            )
        merged_pages.append(
            {
                "page_id": page_id,
                "text": ocr_by_page.get(page_id, ""),
                "images": detections,
            }
        )
    return merged_pages


async def _get_cached_result(pdf_hash: str):
    collection = get_pdf_results_collection()
    return await asyncio.to_thread(collection.find_one, {"_id": pdf_hash})


async def _save_cached_result(pdf_hash: str, data: dict):
    collection = get_pdf_results_collection()
    payload = dict(data)
    payload["_id"] = pdf_hash
    payload["updated_at"] = datetime.now(timezone.utc)
    if "created_at" not in payload:
        payload["created_at"] = payload["updated_at"]
    await asyncio.to_thread(
        collection.replace_one,
        {"_id": pdf_hash},
        payload,
        True,
    )


async def process_pdf_chain(pdf_file) -> dict:
    check_pdf_file(pdf_file)
    pdf_bytes = await pdf_file.read()
    check_pdf_content(pdf_bytes)

    pdf_hash = _build_pdf_hash(pdf_bytes)
    cached = await _get_cached_result(pdf_hash)
    if cached:
        cached["cached"] = True
        cached.pop("_id", None)
        cached.pop("created_at", None)
        cached.pop("updated_at", None)
        return cached

    upload_info = await upload_pdf_service(pdf_bytes)
    blob_path = upload_info["blob_path"]

    yolo_task = asyncio.to_thread(process_pdf_with_yolo, blob_path)
    ocr_task = asyncio.to_thread(process_pdf_with_ocr, blob_path)
    yolo_result, ocr_pages = await asyncio.gather(yolo_task, ocr_task)

    merged_pages = _merge_ocr_yolo(ocr_pages, yolo_result)
    llm_result = await llm_process_pdf_action(merged_pages)

    result = {
        "cached": False,
        "pdf_hash": pdf_hash,
        "pdf_blob_url": upload_info["blob_url"],
        "pages": merged_pages,
        "extracted": llm_result,
    }
    await _save_cached_result(pdf_hash, result)
    return result
