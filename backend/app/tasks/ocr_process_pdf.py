from app.tasks.celery_app import celery_app
from app.clients.azure_document_client import get_document_intelligence_client
from app.core.config import azure_document_intelligence_settings


@celery_app.task
def process_pdf_with_ocr(pdf_path: str) -> dict:
    '''
    使用 Azure 文档智能服务处理 PDF 文件，并返回结构化结果
    '''
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    client = get_document_intelligence_client()
    model_id = azure_document_intelligence_settings.AZURE_DOCUMENT_INTELLIGENCE_MODEL
    poller = client.begin_analyze_document(
        model_id,
        document=pdf_bytes,
        content_type="application/pdf",
    )
    result = poller.result()

    def _points(polygon):
        if not polygon:
            return []
        return [{"x": float(p.x), "y": float(p.y)} for p in polygon]

    def _bounding_regions(regions):
        if not regions:
            return []
        return [
            {"page_number": r.page_number, "polygon": _points(r.polygon)}
            for r in regions
        ]

    def _spans(spans):
        if not spans:
            return []
        return [{"offset": s.offset, "length": s.length} for s in spans]

    pages = []
    for page in result.pages or []:
        pages.append(
            {
                "page_number": page.page_number,
                "width": float(page.width) if page.width is not None else None,
                "height": float(page.height) if page.height is not None else None,
                "unit": page.unit,
                "lines": [
                    {
                        "text": line.content,
                        "polygon": _points(line.polygon),
                        "spans": _spans(line.spans),
                    }
                    for line in (page.lines or [])
                ],
                "words": [
                    {
                        "text": word.content,
                        "confidence": word.confidence,
                        "polygon": _points(word.polygon),
                        "spans": _spans(word.spans),
                    }
                    for word in (page.words or [])
                ],
            }
        )

    tables = []
    for table in result.tables or []:
        tables.append(
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "bounding_regions": _bounding_regions(table.bounding_regions),
                "spans": _spans(table.spans),
                "cells": [
                    {
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "row_span": cell.row_span,
                        "column_span": cell.column_span,
                        "kind": cell.kind,
                        "content": cell.content,
                        "bounding_regions": _bounding_regions(cell.bounding_regions),
                        "spans": _spans(cell.spans),
                    }
                    for cell in (table.cells or [])
                ],
            }
        )

    key_value_pairs = []
    for kv in result.key_value_pairs or []:
        key_value_pairs.append(
            {
                "key": {
                    "content": kv.key.content if kv.key else None,
                    "bounding_regions": _bounding_regions(
                        kv.key.bounding_regions if kv.key else None
                    ),
                    "spans": _spans(kv.key.spans if kv.key else None),
                },
                "value": {
                    "content": kv.value.content if kv.value else None,
                    "bounding_regions": _bounding_regions(
                        kv.value.bounding_regions if kv.value else None
                    ),
                    "spans": _spans(kv.value.spans if kv.value else None),
                },
            }
        )

    paragraphs = []
    for paragraph in result.paragraphs or []:
        paragraphs.append(
            {
                "content": paragraph.content,
                "role": paragraph.role,
                "bounding_regions": _bounding_regions(paragraph.bounding_regions),
                "spans": _spans(paragraph.spans),
            }
        )

    return {
        "model_id": model_id,
        "content": result.content,
        "pages": pages,
        "tables": tables,
        "key_value_pairs": key_value_pairs,
        "paragraphs": paragraphs,
    }
