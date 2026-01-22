from fastapi import File, UploadFile
import uuid
import aiofiles

from app.tasks.ocr_process_pdf import process_pdf_with_ocr
from app.core.config import TMP_UPLOAD_DIR
from app.services.process_pdf.yolo_actions import check_pdf_file


async def process_pdf_file_with_ocr(pdf_file_path: str) -> str:
    """
    异步调用 OCR Celery 任务
    """
    
    task = process_pdf_with_ocr.delay(str(pdf_file_path))

    return task.id

