from fastapi import APIRouter, HTTPException, Depends

from ..schemas.institution import InstitutionCreate, InstitutionResponse
from ..db.instituion_dao import InstitutionDAO


router = APIRouter()
dao = InstitutionDAO()

@router.post("/", response_model=InstitutionResponse)
def create_institution(institution: InstitutionCreate):
    institution_obj = dao.insert_institution(institution)  # DAO 메서드 호출
    if not institution_obj:
        raise HTTPException(status_code=400, detail="Institution creation failed")    
    return dao.get_institution_by_id(institution.institution_id)

@router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: str):
    institution = dao.get_institution_by_id(institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution
