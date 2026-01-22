from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.process_pdf.chain import process_pdf_chain
router = APIRouter()


@router.post("/workflow/pdf_workflow")
async def pdf_workflow(pdf_file: UploadFile = File(...)) -> JSONResponse:
    try:
        result = await process_pdf_chain(pdf_file)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    return JSONResponse(result)
