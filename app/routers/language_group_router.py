from fastapi import APIRouter, HTTPException, Depends
from app.schemas.language_group import LanguageGroupCreate, LanguageGroupResponse
from app.db.language_group_dao import LanguageGroupDAO
from typing import List

router = APIRouter()
dao = LanguageGroupDAO()

@router.post("/", response_model=LanguageGroupResponse)
def create_language_group(group: LanguageGroupCreate):
    language_group_id = dao.insert_language_group(group)
    if not language_group_id:
        raise HTTPException(status_code=400, detail="Failed to create language group")
    return dao.get_language_group_by_id(language_group_id)

@router.get("/{language_group_id}", response_model=LanguageGroupResponse)
def get_language_group(language_group_id: int):
    group = dao.get_language_group_by_id(language_group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Language group not found")
    return group

@router.get("/", response_model=List[LanguageGroupResponse])
def get_all_language_groups():
    groups = dao.get_all_language_groups()
    return groups

@router.put("/{language_group_id}")
def update_language_group(language_group_id: int, updated_data: LanguageGroupCreate):
    success = dao.update_language_group(language_group_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Language group not found or update failed")
    return {"message": "Language group updated successfully"}

@router.delete("/{language_group_id}")
def delete_language_group(language_group_id: int):
    success = dao.delete_language_group(language_group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Language group not found or delete failed")
    return {"message": "Language group deleted successfully"}

@router.delete("/drop")
def drop_language_group_table():
    dao.drop_table()
    return {"message": "Language group table dropped successfully"}
