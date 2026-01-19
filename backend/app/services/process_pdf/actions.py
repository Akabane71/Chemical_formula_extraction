from fastapi import File, UploadFile


async def process_pdf_file(pdf_file: UploadFile=File(...)) -> str:
    """
    处理上传的 PDF 文件
    """
    pass