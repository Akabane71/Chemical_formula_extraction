import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.logging import setup_loguru
from app.core.config import TMP_PDF_IMGS_DIR, settings
from pathlib import Path
from app.api.api import router


# setup_loguru(
#     level=getattr(settings, "LOG_LEVEL", "INFO"),
#     json=getattr(settings, "LOG_JSON", True),
#     log_dir=getattr(settings, f"{Path(__file__).resolve().parent.parent}/logs", None),  # 可选
#     app_name=getattr(settings, "PROJECT_NAME", "app"),
# )

# 标准 logging 也会进 loguru
logger = logging.getLogger("app")  
app = FastAPI()

app.mount("/static", StaticFiles(directory=TMP_PDF_IMGS_DIR), name="static")


# 包含路由
app.include_router(router)

