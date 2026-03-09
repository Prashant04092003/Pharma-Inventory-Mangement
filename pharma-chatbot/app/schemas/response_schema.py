from pydantic import BaseModel
from typing import Any, Optional

class ChatbotResponse(BaseModel):
    status: str  # success | error | ambiguous
    data: Optional[Any] = None
    message: Optional[str] = None
    meta: Optional[dict] = None