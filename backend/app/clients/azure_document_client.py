from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from app.core.config import azure_document_intelligence_settings

_client = None


def get_document_intelligence_client() -> DocumentIntelligenceClient:
    global _client
    if _client is None:
        _client = DocumentIntelligenceClient(
            endpoint=azure_document_intelligence_settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
            credential=AzureKeyCredential(
                azure_document_intelligence_settings.AZURE_DOCUMENT_INTELLIGENCE_API_KEY
            ),
        )
    return _client
