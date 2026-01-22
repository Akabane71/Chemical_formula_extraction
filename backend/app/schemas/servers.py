from pydantic import BaseModel



class LLM_ProcessRequest(BaseModel):
    data: dict


class PdfBlobRequest(BaseModel):
    blob_url: str
