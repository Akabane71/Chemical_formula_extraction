from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

dir_path = Path(__file__).resolve().parent

# General settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{dir_path}/../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"


# Azure Blob Storage settings
class AzureBlobSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{dir_path}/../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_CONTAINER_NAME: str


# MinerU config instances
class MinerUConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{dir_path}/../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    MINERU_API_BASE_URL: str


# Azure OpenAI settings instances
class AzureOpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{dir_path}/../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_VERSION: str = "2024-06-01-preview"

settings = Settings()
azure_blob_settings = AzureBlobSettings()
mineru_config_settings = MinerUConfigSettings()
azure_openai_settings = AzureOpenAISettings()