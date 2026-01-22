from app.tasks.yolo_process_pdf import process_pdf_with_yolo
from app.clients.azure_blob_client import blob_url_to_path


async def process_pdf_file(blob_url: str) -> str:
    """
    处理上传的 PDF 文件，异步调用 Celery 任务
    """
    # 调用 Celery 任务
    blob_path = blob_url_to_path(blob_url)
    task = process_pdf_with_yolo.delay(blob_path)

    return task.id
