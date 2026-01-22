from fastapi import UploadFile
from app.clients.azure_blob_client import upload_img_to_azure_blob

'''
    获取上传的文件并将内容审核
'''

async def upload_pdf_service(pdf_file: UploadFile)->str:
    try:
        contents = await pdf_file.read()
        file_size = len(contents)
        # 这里可以添加将文件上传到 Azure Blob 存储的逻辑
        # 例如，使用 Azure SDK 上传文件
        # blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        # container_client = blob_service_client.get_container_client(container_name)
        # blob_client = container_client.get_blob_client(pdf_file.filename)
        # await blob_client.upload_blob(contents)
    except Exception as e:
        raise e
    return f"File {pdf_file.filename} uploaded successfully with size {file_size} bytes."