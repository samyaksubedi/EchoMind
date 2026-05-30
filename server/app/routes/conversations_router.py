from fastapi import APIRouter

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


# Upload video/audio → create conversation
@router.post("/from-upload")
async def create_from_upload():
    return {"message": "Upload video/audio"}


# YouTube link → create conversation
@router.post("/from-youtube")
async def create_from_youtube():
    return {"message": "YouTube link ingestion"}


# Get all conversations
@router.get("")
async def get_conversations():
    return {"message": "All conversations"}


# Get single conversation + messages
@router.get("/{id}")
async def get_conversation(id: str):
    return {"conversation_id": id}


# Delete conversation
@router.delete("/{id}")
async def delete_conversation(id: str):
    return {"message": f"Deleted {id}"}


# Processing status
@router.get("/{id}/status")
async def get_status(id: str):
    return {"conversation_id": id, "status": "processing"}
