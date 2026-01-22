import hashlib
from fastapi import File, UploadFile
from app.clients.azure_blob_client import upload_pdf_to_azure_blob
from app.core.config import AZURE_BLOB_PDF_DIR
from loguru import logger
import fitz

from app.core import logging  # PyMuPDF

"""
    获取上传的文件并将内容审核
"""

def check_pdf_content(pdf_bytes: bytes) -> None:
    """
    检查 PDF 文件内容是否有效（能否打开、是否有页、是否有文本）
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
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



def build_pdf_hash_filename(pdf_bytes: bytes) -> str:
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    return f"{pdf_hash}.pdf"


async def upload_pdf_service(pdf_bytes: bytes) -> dict:
    filename = build_pdf_hash_filename(pdf_bytes)
    blob_url = await upload_pdf_to_azure_blob(
        pdf_bytes=pdf_bytes,
        pdf_filename=filename,
        upload_dir=AZURE_BLOB_PDF_DIR,
    )
    return {
        "filename": filename,
        "size": len(pdf_bytes),
        "blob_url": blob_url,
        "blob_path": f"{AZURE_BLOB_PDF_DIR}/{filename}",
    }
