from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE_PATH = Path(Path(__file__).parent.parent, ".env")
print(ENV_FILE_PATH)


# General settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"


# Azure Blob Storage settings
class AzureBlobSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_CONTAINER_NAME: str


# MinerU config instances
class MinerUConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    MINERU_API_BASE_URL: str


# Azure OpenAI settings instances
class AzureOpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_VERSION: str = "2024-06-01-preview"


class AzureDocumentIntelligenceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: str
    AZURE_DOCUMENT_INTELLIGENCE_API_KEY: str
    AZURE_DOCUMENT_INTELLIGENCE_MODEL: str = "prebuilt-document"


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_VHOST: str

class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_DBNAME: str


STATIC_DIR = Path(Path(__file__).parent.parent.parent, "static")
TMP_DIR = Path(Path(__file__).parent.parent.parent, "tmp")
MOCK_DIR = Path(Path(__file__).parent.parent.parent, "mock")
TMP_UPLOAD_DIR = TMP_DIR / "uploads"
TMP_PDF_IMGS_DIR = TMP_DIR / "pdf_imgs"
# ENV_FILE_PATH = Path(Path(__file__).parent.parent.parent, ".env")

TMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
TMP_PDF_IMGS_DIR.mkdir(parents=True, exist_ok=True)

AZURE_BLOB_PDF_DIR = "pdfs"
AZURE_BLOB_PDF_IMG_DIR = "pdf_imgs"


settings = Settings()
azure_blob_settings = AzureBlobSettings()
mineru_config_settings = MinerUConfigSettings()
azure_openai_settings = AzureOpenAISettings()
azure_document_intelligence_settings = AzureDocumentIntelligenceSettings()
rabbit_mq_settings = RabbitMQSettings()
mongodb_settings = MongoDBSettings()
