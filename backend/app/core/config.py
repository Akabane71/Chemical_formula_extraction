from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AliasChoices
from pathlib import Path
from urllib.parse import quote_plus

ENV_FILE_PATH = Path(Path(__file__).parent.parent, ".env")


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
    RABBITMQ_USER: str = Field(
        default="guest",
        validation_alias=AliasChoices("RABBITMQ_USER", "RABBITMQ_DEFAULT_USER"),
    )
    RABBITMQ_PASSWORD: str = Field(
        default="guest",
        validation_alias=AliasChoices("RABBITMQ_PASSWORD", "RABBITMQ_DEFAULT_PASS"),
    )
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_VHOST: str = Field(default="/")

class MongoDBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    MONGODB_USER: str = Field(
        default="",
        validation_alias=AliasChoices("MONGODB_USER", "MONGO_INITDB_ROOT_USERNAME"),
    )
    MONGODB_PASSWORD: str = Field(
        default="",
        validation_alias=AliasChoices("MONGODB_PASSWORD", "MONGO_INITDB_ROOT_PASSWORD"),
    )
    MONGODB_HOST: str = Field(default="localhost")
    MONGODB_PORT: int = Field(default=27017)
    MONGODB_DBNAME: str = Field(default="pdf_workflow")


STATIC_DIR = Path(Path(__file__).parent.parent.parent, "static")
WEB_DIR = Path(Path(__file__).parent.parent.parent.parent, "web")
TMP_DIR = Path(Path(__file__).parent.parent.parent, "tmp")
MOCK_DIR = Path(Path(__file__).parent.parent.parent, "mock")
TMP_UPLOAD_DIR = TMP_DIR / "uploads"
TMP_PDF_IMGS_DIR = TMP_DIR / "pdf_imgs"

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


def build_mongo_uri() -> str:
    user = mongodb_settings.MONGODB_USER
    password = mongodb_settings.MONGODB_PASSWORD
    host = mongodb_settings.MONGODB_HOST
    port = mongodb_settings.MONGODB_PORT
    dbname = mongodb_settings.MONGODB_DBNAME
    if user and password:
        auth = f"{quote_plus(user)}:{quote_plus(password)}@"
        return f"mongodb://{auth}{host}:{port}/{dbname}?authSource=admin"
    return f"mongodb://{host}:{port}/{dbname}"
