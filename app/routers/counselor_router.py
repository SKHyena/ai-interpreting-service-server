from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.counselor import CounselorCreate, CounselorResponse
from ..db.counselor_dao import CounselorDAO


router = APIRouter()
dao = CounselorDAO()

@router.post("/", response_model=CounselorResponse)
def create_counselor(counselor: CounselorCreate):
    counselor_id = dao.insert_counselor(counselor)
    if not counselor_id:
        raise HTTPException(status_code=400, detail="Failed to create counselor")
    return dao.get_counselor_by_id(counselor_id)


@router.get("/{counselor_user_id}", response_model=CounselorResponse)
def get_counselor(counselor_user_id: str):
    counselor = dao.get_counselor_by_id(counselor_user_id)
    if not counselor:
        raise HTTPException(status_code=404, detail="Counselor not found")
    return counselor


@router.get("/", response_model=List[CounselorResponse])
def get_all_counselors():
    counselors = dao.get_all_counselors()
    return counselors


@router.put("/{counselor_user_id}")
def update_counselor(counselor_user_id: str, updated_data: CounselorCreate):
    success = dao.update_counselor(counselor_user_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Counselor not found or update failed")
    return {"message": "Counselor updated successfully"}


@router.delete("/{counselor_user_id}")
def delete_counselor(counselor_user_id: str):
    success = dao.delete_counselor(counselor_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Counselor not found or delete failed")
    return {"message": "Counselor deleted successfully"}


@router.delete("/drop")
def drop_counselor_table():
    dao.drop_table()
    return {"message": "Counselor table dropped successfully"}
