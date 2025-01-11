from typing import List

from fastapi import APIRouter, HTTPException

from ..schemas.pairing import PairingCreate, PairingResponse
from ..db.pairing_dao import PairingDAO


router = APIRouter()
dao = PairingDAO()

@router.post("/", response_model=PairingResponse)
def create_pairing(pairing: PairingCreate):
    pairing_id = dao.insert_pairing(pairing)
    if not pairing_id:
        raise HTTPException(status_code=400, detail="Failed to create pairing")
    return dao.get_pairing_by_id(pairing_id)

@router.get("/{pairing_id}", response_model=PairingResponse)
def get_pairing(pairing_id: int):
    pairing = dao.get_pairing_by_id(pairing_id)
    if not pairing:
        raise HTTPException(status_code=404, detail="Pairing not found")
    return pairing

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

@router.delete("/{pairing_id}")
def delete_pairing(pairing_id: int):
    success = dao.delete_pairing(pairing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pairing not found or delete failed")
    return {"message": "Pairing deleted successfully"}

@router.delete("/drop")
def drop_pairing_table():
    dao.drop_table()
    return {"message": "Pairing table dropped successfully"}
