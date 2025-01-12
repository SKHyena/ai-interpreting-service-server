from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.counseling_type_group import CounselingTypeGroupCreate, CounselingTypeGroupResponse
from ..db.counseling_type_group_dao import CounselingTypeGroupDAO


router = APIRouter()
dao = CounselingTypeGroupDAO()


@router.post("/", response_model=CounselingTypeGroupResponse)
def create_counseling_type_group(group: CounselingTypeGroupCreate):
    group_id = dao.insert_group(group)
    if not group_id:
        raise HTTPException(status_code=400, detail="Failed to create counseling type group")
    return dao.get_group_by_id(group_id)


@router.get("/{group_id}", response_model=CounselingTypeGroupResponse)
def get_counseling_type_group(group_id: int):
    group = dao.get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Counseling type group not found")
    return group


@router.get("/", response_model=List[CounselingTypeGroupResponse])
def get_all_counseling_type_groups():
    return dao.get_all_groups()


@router.put("/{group_id}")
def update_counseling_type_group(group_id: int, group: CounselingTypeGroupCreate):
    success = dao.update_group(group_id, group.institution_id, group.group_name)
    if not success:
        raise HTTPException(status_code=404, detail="Counseling type group not found or update failed")
    return {"message": "Counseling type group updated successfully"}


@router.delete("/{group_id}")
def delete_counseling_type_group(group_id: int):
    success = dao.delete_group(group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Counseling type group not found or delete failed")
    return {"message": "Counseling type group deleted successfully"}


@router.delete("/drop")
def drop_counseling_type_group_table():
    dao.drop_table()
    return {"message": "Counseling type groups table dropped successfully"}
