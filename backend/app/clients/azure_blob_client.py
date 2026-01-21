from app.core.config import azure_blob_settings
from azure.storage.blob.aio import BlobServiceClient
import logging
import aiofiles

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



async def upload_img_to_azure_blob(img_path: str, upload_dir: str) -> str:
    """
    上传图片到 Azure Blob 存储

    :param img_path: 本地图片的完整路径
    :param upload_dir: Azure Blob 上的目标目录（容器内路径）
    :return: 上传后图片的 URL
    """
    import os
    container = await get_container_client()
    # basename 将文件名从路径中提取出来
    img_name = os.path.basename(img_path)
    blob_path = f"{upload_dir}/{img_name}" if upload_dir else img_name
    blob_client = container.get_blob_client(blob_path)
    async with aiofiles.open(img_path, "rb") as f:
        data = await f.read()
    await blob_client.upload_blob(data, overwrite=True)
    return blob_client.url