from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.process_pdf.actions import process_pdf_file, get_task_result_action

router = APIRouter()

@router.post("/tasks/process_pdf")
async def process_pdf_endpoint(pdf_file: UploadFile = File(...))->JSONResponse:
    """
    API 端点，处理上传的 PDF 文件
    """
    try:
        res = await process_pdf_file(pdf_file)
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