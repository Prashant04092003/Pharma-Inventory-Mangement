from pydantic import BaseModel
from typing import Optional



class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"
    role: Optional[str] = None
    store_id: Optional[int] = None


class ChatResponse(BaseModel):
    success: bool
    data: dict | list | None = None
    error: str | None = None