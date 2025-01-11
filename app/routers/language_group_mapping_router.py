from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.language_group_mapping import LanguageGroupMappingCreate, LanguageGroupMappingResponse
from ..db.language_group_mapping_dao import LanguageGroupMappingDAO


router = APIRouter()
dao = LanguageGroupMappingDAO()

@router.post("/", response_model=LanguageGroupMappingResponse)
def create_mapping(mapping: LanguageGroupMappingCreate):
    mapping_id = dao.insert_mapping(mapping)
    if not mapping_id:
        raise HTTPException(status_code=400, detail="Failed to create mapping")
    return dao.get_mapping_by_id(mapping_id)

@router.get("/{mapping_id}", response_model=LanguageGroupMappingResponse)
def get_mapping(mapping_id: int):
    mapping = dao.get_mapping_by_id(mapping_id)
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return mapping

@router.get("/", response_model=List[LanguageGroupMappingResponse])
def get_all_mappings():
    mappings = dao.get_all_mappings()
    return mappings

@router.put("/{mapping_id}")
def update_mapping(mapping_id: int, updated_data: LanguageGroupMappingCreate):
    success = dao.update_mapping(mapping_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Mapping not found or update failed")
    return {"message": "Mapping updated successfully"}

@router.delete("/{mapping_id}")
def delete_mapping(mapping_id: int):
    success = dao.delete_mapping(mapping_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mapping not found or delete failed")
    return {"message": "Mapping deleted successfully"}

@router.delete("/drop")
def drop_mapping_table():
    dao.drop_table()
    return {"message": "Mapping table dropped successfully"}
