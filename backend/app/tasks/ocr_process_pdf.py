from app.tasks.celery_app import celery_app
from app.clients.azure_document_client import get_document_intelligence_client
from app.core.config import azure_document_intelligence_settings
from azure.core.exceptions import ResourceNotFoundError
from loguru import logger


@celery_app.task
def process_pdf_with_ocr(blob_path: str) -> dict:
    '''
    使用 Azure 文档智能服务处理 PDF 文件，并返回结构化结果
    '''
    from app.clients.azure_blob_client import download_blob_bytes

    pdf_bytes = download_blob_bytes(blob_path)

    client = get_document_intelligence_client()
    model_id = azure_document_intelligence_settings.AZURE_DOCUMENT_INTELLIGENCE_MODEL
    try:
        poller = client.begin_analyze_document(
            model_id,
            body=pdf_bytes,
            content_type="application/pdf",
        )
    except ResourceNotFoundError as e:
        if "ModelNotFound" not in str(e):
            raise
        fallback_model_id = "prebuilt-read"
        logger.warning(
            "Model not found: {}. Falling back to {}.",
            model_id,
            fallback_model_id,
        )
        poller = client.begin_analyze_document(
            fallback_model_id,
            body=pdf_bytes,
            content_type="application/pdf",
        )
    result = poller.result()

    pages = []
    for page in result.pages or []:
        lines = [line.content for line in (page.lines or []) if line.content]
        pages.append(
            {
                "page_id": page.page_number,
                "text": "\n".join(lines).strip(),
            }
        )

    return pages
