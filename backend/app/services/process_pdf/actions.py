import logging
import uuid
import shutil
from fastapi import File, UploadFile
from app.tasks.yolo_process_pdf import process_pdf_with_yolo
from app.core.config import TMP_UPLOAD_DIR
from pathlib import Path
from loguru import logger
import aiofiles

import fitz  # PyMuPDF

def check_pdf_content(pdf_path: Path) -> None:
    """
    检查 PDF 文件内容是否有效（能否打开、是否有页、是否有文本）
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logger.error(f"无法打开 PDF 文件: {e}")
        raise ValueError("无法打开 PDF 文件，文件可能已损坏")
    
    if doc.page_count == 0:
        logger.error("PDF 文件没有任何页面")
        raise ValueError("PDF 文件没有任何页面")
    
    has_text = False
    for page in doc:
        text = page.get_text().strip()
        if text:
            has_text = True
            break
    if not has_text:
        logger.warning("PDF 文件没有可识别的文本内容")
        # 你可以选择抛出异常或仅警告
        raise ValueError("PDF 文件没有可识别的文本内容")


def check_pdf_file(pdf_file: UploadFile = File(...))->None:
    """
    检查上传的文件是否为 PDF 格式
    """
    # 格式检查
    if pdf_file.content_type != "application/pdf":
        logging.error("上传的文件不是 PDF 格式")
        raise ValueError("上传的文件不是 PDF 格式")
    
    # 文件检查
    if not pdf_file.filename.lower().endswith(".pdf"):
        logging.error("上传的文件扩展名不是 .pdf")
        raise ValueError("上传的文件扩展名不是 .pdf")
    
    

async def process_pdf_file(pdf_file: UploadFile = File(...)) -> str:
    """
    处理上传的 PDF 文件，异步调用 Celery 任务
    """
    # 检查文件是否为pdf文件
    check_pdf_file(pdf_file)

    # 保存上传的 PDF 文件
    file_id = str(uuid.uuid4())
    pdf_path = TMP_UPLOAD_DIR / f"{file_id}.pdf"
    
    data = pdf_file.file.read()
    async with aiofiles.open(pdf_path, "wb") as buffer:
        await buffer.write(data)
        
    # 调用 Celery 任务
    task = process_pdf_with_yolo.delay(str(pdf_path))

    return task.id


async def get_task_result_action(task_id: str):
    """
    获取 Celery 任务结果
    """
    from app.tasks.yolo_process_pdf import celery_app
    result = celery_app.AsyncResult(task_id)
    if result.ready():
        res = result.result
        # 如果是异常对象，返回字符串
        if isinstance(res, Exception):
            return {"error": str(res)}
        return res
    else:
        return None