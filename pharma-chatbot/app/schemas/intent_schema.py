from pydantic import BaseModel
from typing import Optional

class IntentRequest(BaseModel):
    intent: str
    store_id: Optional[int] = None
    brand_name: Optional[str] = None
    threshold: Optional[int] = None