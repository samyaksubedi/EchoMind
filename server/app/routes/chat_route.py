from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["Chat"])


# Ask a question in a conversation
@router.post("/{conversation_id}")
async def ask_question(conversation_id: str):
    return {"conversation_id": conversation_id, "message": "Question received"}
