from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..schemas.pairing import PairingCreate, PairingResponse
from ..schemas.counselor import CounselorResponse
from ..db.pairing_dao import PairingDAO
from ..db.counselor_dao import CounselorDAO
from ..models.pairing import Pairing


router = APIRouter()
dao = PairingDAO()
counselor_dao = CounselorDAO()

@router.post("/complainant", response_model=PairingResponse)
def create_pairing(pairing: PairingCreate):    
    pairing_obj: Pairing = dao.get_pairing_by_client_device_id(pairing.client_device_id)
    
    if pairing_obj is not None:
        is_updated: bool = dao.update_pairing(pairing)
        if not is_updated:
            raise HTTPException(status_code=400, detail="Failed to update pairing")
        return {"type": "update", "status": "success", "message": "Pairing updated successfully"}
    
    pairing_id = dao.insert_pairing(pairing)
    if not pairing_id:
        raise HTTPException(status_code=400, detail="Failed to create pairing")
    return {"type": "create", "status": "success", "message": "Pairing created successfully"}


@router.get("/{pairing_id}", response_model=PairingResponse)
def get_pairing(pairing_id: int):
    pairing = dao.get_pairing_by_id(pairing_id)
    if not pairing:
        raise HTTPException(status_code=404, detail="Pairing not found")    
    return pairing


@router.get("/counselor/{pairing_number}", response_model=CounselorResponse)
def get_paired_counselor(pairing_number: str):
    pairing = dao.get_pairing_by_pairing_code(pairing_code=pairing_number)
    counselor = counselor_dao.get_counselor_by_id(pairing.counselor_user_id)
    if not counselor:
        raise HTTPException(status_code=404, detail="Counselor not found with pairing code")
    
    return counselor


@router.put("/{pairing_code}")
def disconnect_pairing(pairing_code: str):
    success = dao.update_pairing_by_pairing_code(pairing_code)
    if not success:
        raise HTTPException(status_code=404, detail="Pairing not found or delete failed")
    return {"type": "update", "status": "success", "message": "Pairing disconnected successfully"}



@router.get("/", response_model=List[PairingResponse])
def get_all_pairings():
    pairings = dao.get_all_pairings()
    return pairings


@router.put("/{pairing_id}/status")
def update_pairing_status(pairing_id: int, status: str):
    success = dao.update_pairing_status(pairing_id, status)
    if not success:
        raise HTTPException(status_code=404, detail="Pairing not found or update failed")
    return {"message": "Pairing status updated successfully"}


@router.delete("/drop")
def drop_pairing_table():
    dao.drop_table()
    return {"message": "Pairing table dropped successfully"}
