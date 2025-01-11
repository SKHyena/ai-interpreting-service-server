from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.counseling_session import CounselingSessionCreate, CounselingSessionResponse
from ..db.counseling_session_dao import CounselingSessionDAO


router = APIRouter()
dao = CounselingSessionDAO()

@router.post("/", response_model=CounselingSessionResponse)
def create_session(session: CounselingSessionCreate):
    session_id = dao.insert_session(session)
    if not session_id:
        raise HTTPException(status_code=400, detail="Failed to create session")
    return dao.get_session_by_id(session_id)

@router.get("/{session_id}", response_model=CounselingSessionResponse)
def get_session(session_id: int):
    session = dao.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/", response_model=List[CounselingSessionResponse])
def get_all_sessions():
    sessions = dao.get_all_sessions()
    return sessions

@router.put("/{session_id}/status")
def update_session_status(session_id: int, status: str):
    success = dao.update_session_status(session_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found or update failed")
    return {"message": "Session status updated successfully"}

@router.delete("/{session_id}")
def delete_session(session_id: int):
    success = dao.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found or delete failed")
    return {"message": "Session deleted successfully"}

@router.delete("/drop")
def drop_session_table():
    dao.drop_table()
    return {"message": "Counseling sessions table dropped successfully"}
