from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..schemas.counseling_summary import CounselingSummaryCreate, CounselingSummaryResponse
from ..db.counseling_summary_dao import CounselingSummaryDAO


router = APIRouter()
dao = CounselingSummaryDAO()

@router.post("/", response_model=CounselingSummaryResponse)
def create_summary(summary: CounselingSummaryCreate):
    summary_id = dao.insert_summary(summary)
    if not summary_id:
        raise HTTPException(status_code=400, detail="Failed to create summary")
    return dao.get_summary_by_id(summary_id)

@router.get("/{summary_id}", response_model=CounselingSummaryResponse)
def get_summary(summary_id: int):
    summary = dao.get_summary_by_id(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

@router.get("/", response_model=List[CounselingSummaryResponse])
def get_all_summaries():
    summaries = dao.get_all_summaries()
    return summaries

@router.put("/{summary_id}")
def update_summary(summary_id: int, summary_text: str, conversation_log: Optional[str] = None):
    success = dao.update_summary(summary_id, summary_text, conversation_log)
    if not success:
        raise HTTPException(status_code=404, detail="Summary not found or update failed")
    return {"message": "Summary updated successfully"}

@router.delete("/{summary_id}")
def delete_summary(summary_id: int):
    success = dao.delete_summary(summary_id)
    if not success:
        raise HTTPException(status_code=404, detail="Summary not found or delete failed")
    return {"message": "Summary deleted successfully"}

@router.delete("/drop")
def drop_summary_table():
    dao.drop_table()
    return {"message": "Counseling summaries table dropped successfully"}
