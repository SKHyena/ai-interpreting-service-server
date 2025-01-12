from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.counseling_type import CounselingTypeCreate, CounselingTypeResponse
from ..db.counseling_type_dao import CounselingTypeDAO

router = APIRouter()
dao = CounselingTypeDAO()


@router.post("/", response_model=CounselingTypeResponse)
def create_counseling_type(counseling_type: CounselingTypeCreate):
    counseling_type_id = dao.insert_counseling_type(counseling_type)
    if not counseling_type_id:
        raise HTTPException(status_code=400, detail="Failed to create counseling type")
    return dao.get_counseling_type_by_id(counseling_type_id)


@router.get("/{counseling_type_id}", response_model=CounselingTypeResponse)
def get_counseling_type(counseling_type_id: int):
    counseling_type = dao.get_counseling_type_by_id(counseling_type_id)
    if not counseling_type:
        raise HTTPException(status_code=404, detail="Counseling type not found")
    return counseling_type


@router.get("/", response_model=List[CounselingTypeResponse])
def get_all_counseling_types():
    return dao.get_all_counseling_types()


@router.put("/{counseling_type_id}")
def update_counseling_type(counseling_type_id: int, counseling_type: CounselingTypeCreate):
    success = dao.update_counseling_type(counseling_type_id, counseling_type.type_name, counseling_type.description)
    if not success:
        raise HTTPException(status_code=404, detail="Counseling type not found or update failed")
    return {"message": "Counseling type updated successfully"}


@router.delete("/{counseling_type_id}")
def delete_counseling_type(counseling_type_id: int):
    success = dao.delete_counseling_type(counseling_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Counseling type not found or delete failed")
    return {"message": "Counseling type deleted successfully"}


@router.delete("/drop")
def drop_counseling_type_table():
    dao.drop_table()
    return {"message": "Counseling types table dropped successfully"}
