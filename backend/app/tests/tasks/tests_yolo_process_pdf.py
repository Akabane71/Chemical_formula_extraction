import pytest
import os
from app.core.config import MOCK_DIR,ENV_FILE_PATH
from app.tasks.yolo_process_pdf import process_pdf_with_yolo
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=ENV_FILE_PATH
)

@pytest.mark.asyncio
async def test_process_pdf_with_yolo():
    # 使用测试用的小PDF文件路径
    test_pdf_path = f'{MOCK_DIR}/pdfs/1.pdf'
    assert os.path.exists(test_pdf_path)
    result =  process_pdf_with_yolo(test_pdf_path)
    print("YOLO 处理结果:", result)
    for page in result["pages"]:
        assert "page" in page
        assert "detections" in page