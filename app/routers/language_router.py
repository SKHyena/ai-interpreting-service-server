from typing import List

from fastapi import APIRouter, HTTPException, Depends

from ..schemas.language import LanguageCreate, LanguageResponse
from ..db.language_dao import LanguageDAO

router = APIRouter()
dao = LanguageDAO()

@router.post("/", response_model=LanguageResponse)
def create_language(language: LanguageCreate):
    language_id = dao.insert_language(language)
    if not language_id:
        raise HTTPException(status_code=400, detail="Failed to create language")
    return dao.get_language_by_id(language_id)

@router.get("/{language_id}", response_model=LanguageResponse)
def get_language(language_id: int):
    language = dao.get_language_by_id(language_id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language

@router.get("/", response_model=List[LanguageResponse])
def get_all_languages():
    languages = dao.get_all_languages()
    return languages

@router.put("/{language_id}")
def update_language(language_id: int, updated_data: LanguageCreate):
    success = dao.update_language(language_id, updated_data)
    if not success:
        raise HTTPException(status_code=404, detail="Language not found or update failed")
    return {"message": "Language updated successfully"}

@router.delete("/{language_id}")
def delete_language(language_id: int):
    success = dao.delete_language(language_id)
    if not success:
        raise HTTPException(status_code=404, detail="Language not found or delete failed")
    return {"message": "Language deleted successfully"}

@router.delete("/drop")
def drop_language_table():
    dao.drop_table()
    return {"message": "Language table dropped successfully"}
