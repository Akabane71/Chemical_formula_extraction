from app.tasks.ocr_process_pdf import process_pdf_with_ocr
from app.clients.azure_blob_client import blob_url_to_path


async def process_pdf_file_with_ocr(blob_url: str) -> str:
    """
    异步调用 OCR Celery 任务
    """
    blob_path = blob_url_to_path(blob_url)
    task = process_pdf_with_ocr.delay(blob_path)

    return task.id
