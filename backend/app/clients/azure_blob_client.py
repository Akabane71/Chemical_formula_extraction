from app.core.config import azure_blob_settings
from azure.storage.blob.aio import BlobServiceClient
import aiofiles
import asyncio

_container_client = None
_container_lock = asyncio.Lock()
_container_checked = False


async def get_container_client():
    CONNECTION_STRING = azure_blob_settings.AZURE_STORAGE_CONNECTION_STRING
    CONTAINER_NAME = azure_blob_settings.AZURE_STORAGE_CONTAINER_NAME
    global _container_client, _container_checked

    if _container_client is not None and _container_checked:
        return _container_client

    async with _container_lock:
        if _container_client is not None and _container_checked:
            return _container_client

        bsc = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container = bsc.get_container_client(CONTAINER_NAME)
        try:
            await container.get_container_properties()
        except Exception as e:
            raise RuntimeError(f"Container error: {e}")

        _container_client = container
        _container_checked = True
        return _container_client



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

async def upload_pdf_to_azure_blob(pdf_bytes: bytes, pdf_filename: str, upload_dir: str) -> str:
    """
    上传 PDF 文件到 Azure Blob 存储

    :param pdf_bytes: PDF 文件的字节内容
    :param pdf_filename: PDF 文件名
    :param upload_dir: Azure Blob 上的目标目录（容器内路径）
    :return: 上传后 PDF 文件的 URL
    """
    container = await get_container_client()
    blob_path = f"{upload_dir}/{pdf_filename}" if upload_dir else pdf_filename
    blob_client = container.get_blob_client(blob_path)
    await blob_client.upload_blob(pdf_bytes, overwrite=True)
    return blob_client.url