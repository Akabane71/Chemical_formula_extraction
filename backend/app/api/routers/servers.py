from fastapi import APIRouter, UploadFile, File


router = APIRouter()

@router.post("/process_pdf")
async def process_pdf_endpoint(pdf_file: UploadFile = File(...)):
    """
    API 端点，处理上传的 PDF 文件
    """
    pass