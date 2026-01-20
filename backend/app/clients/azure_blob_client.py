from gradio_client import file
from app.core.config import azure_blob_settings
from app.utils.rename import rename_file
from azure.storage.blob.aio import BlobServiceClient
import logging
import io

async def get_container_client():
    CONNECTION_STRING = azure_blob_settings.AZURE_STORAGE_CONNECTION_STRING
    CONTAINER_NAME = azure_blob_settings.AZURE_STORAGE_CONTAINER_NAME
    
    logging.info(f"Using Azure Blob Storage with container: {CONTAINER_NAME}")
    logging.info(f"Connection String: {CONNECTION_STRING}")

    bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container = bsc.get_container_client(CONTAINER_NAME)
    try:
        await container.get_container_properties()
    except Exception as e:
        raise RuntimeError(f"Container error: {e}")
    return container



async def upload_img_to_azure_blob(img_path: str, upload_path: str) -> str:
    """
    上传图片到 Azure Blob 存储
    """
    new_name = rename_file(img_path.split('/')[-1])
    
    container = await get_container_client()
    blob_client = container.get_blob_client(f"{upload_path}/{new_name}")
    blob_path = await blob_client.upload_file(
        local_path = img_path,
        overwrite=True)
    return blob_path