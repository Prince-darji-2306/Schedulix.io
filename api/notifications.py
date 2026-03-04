from fastapi import APIRouter, HTTPException, Depends, Request
from services.auth_service import decode_token
from repos.task_repo import get_user_notifications, mark_note_as_read

router = APIRouter(prefix="/api")

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    return decode_token(token)

@router.get("/notifications")
async def get_notifications(payload: dict = Depends(get_current_user)):
    user_id = payload.get("id")
    return get_user_notifications(user_id)

@router.post("/notifications/{note_id}/read")
async def mark_read(note_id: int, payload: dict = Depends(get_current_user)):
    mark_note_as_read(note_id)
    return {"status": "success"}
