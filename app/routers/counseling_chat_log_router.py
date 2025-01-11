from fastapi import APIRouter, HTTPException

from typing import List

from ..schemas.counseling_chat_log import CounselingChatLogCreate, CounselingChatLogResponse
from ..db.counseling_chat_log_dao import CounselingChatLogDAO

router = APIRouter()
dao = CounselingChatLogDAO()

@router.post("/", response_model=CounselingChatLogResponse)
def create_chat_log(chat_log: CounselingChatLogCreate):
    chat_id = dao.insert_chat_log(chat_log)
    if not chat_id:
        raise HTTPException(status_code=400, detail="Failed to create chat log")
    return dao.get_chat_log_by_id(chat_id)

@router.get("/{chat_id}", response_model=CounselingChatLogResponse)
def get_chat_log(chat_id: int):
    chat_log = dao.get_chat_log_by_id(chat_id)
    if not chat_log:
        raise HTTPException(status_code=404, detail="Chat log not found")
    return chat_log

@router.get("/", response_model=List[CounselingChatLogResponse])
def get_all_chat_logs():
    chat_logs = dao.get_all_chat_logs()
    return chat_logs

@router.put("/{chat_id}")
def update_chat_log(chat_id: int, final_message: str):
    success = dao.update_chat_log(chat_id, final_message)
    if not success:
        raise HTTPException(status_code=404, detail="Chat log not found or update failed")
    return {"message": "Chat log updated successfully"}

@router.delete("/{chat_id}")
def delete_chat_log(chat_id: int):
    success = dao.delete_chat_log(chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat log not found or delete failed")
    return {"message": "Chat log deleted successfully"}

@router.delete("/drop")
def drop_chat_log_table():
    dao.drop_table()
    return {"message": "Counseling chat logs table dropped successfully"}
