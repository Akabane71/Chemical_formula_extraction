from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.process_pdf.yolo_actions import process_pdf_file
from app.services.process_pdf.ocr_actions import process_pdf_file_with_ocr
from app.services.process_pdf.upload_pdf import upload_pdf_service,check_pdf_file,check_pdf_content
from app.tasks.celery_app import get_task_result_action
from app.schemas.servers import PdfBlobRequest

router = APIRouter()

@router.post("/uploads/pdf")
async def upload_pdf_endpoint(pdf_file: UploadFile = File(...))->JSONResponse:
    """
    API 端点，上传 PDF 文件, 并将文件上传到 azuer blob 存储
    """
    try:
        check_pdf_file(pdf_file)
        contents = await pdf_file.read()
        check_pdf_content(contents)
        result = await upload_pdf_service(contents)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse(result)


@router.post("/tasks/yolo_process_pdf")
async def process_pdf_endpoint(data: PdfBlobRequest)->JSONResponse:
    """
    API 端点, 使用 YOLO 处理上传的 PDF 文件
    """
    try:
        res = await process_pdf_file(data.blob_url)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse({"task_id": res})


@router.post("/tasks/ocr_process_pdf")
async def ocr_process_pdf_endpoint(data: PdfBlobRequest)->JSONResponse:
    """
    API 端点，使用 OCR 处理上传的 PDF 文件
    """
    try:
        res = await process_pdf_file_with_ocr(data.blob_url)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse({"task_id": res})


@router.post("/tasks/llm_process")
async def llm_process_endpoint(data: dict)->JSONResponse:
    """
    API 端点，使用 LLM 处理数据
    """
    try:
        res = 1
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse({"task_id": res})


@router.get("/tasks/task_result/{task_id}")
async def get_task_result(task_id: str)->JSONResponse:
    """
    获取 Celery 任务结果的 API 端点
    """
    try:
        result = await get_task_result_action(task_id)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse(result)
