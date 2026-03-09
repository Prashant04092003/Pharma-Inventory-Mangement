from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    return chat_service.process(
        message=request.message,
        role=request.role,
        store_id=request.store_id,
        session_id=request.session_id
    )