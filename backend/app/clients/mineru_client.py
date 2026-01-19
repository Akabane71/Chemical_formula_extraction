from app.core.config import mineru_config_settings
from fastapi import UploadFile


async def pulish_mineru_task(pdf_file: UploadFile) -> str:
    """
    调用后端的 MinerU 服务，调用后端的处理
    """
    pass

