from pydantic import BaseModel



class LLM_ProcessRequest(BaseModel):
    data: dict