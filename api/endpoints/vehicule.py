from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from schemas.vehicule import VehicleCreate, VehicleResponse
from services.vehicule_services import create_vehicle, get_user_vehicles, delete_vehicle
from core.dependencies import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicule"])


@router.post("/", response_model=VehicleResponse)
def add_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_vehicle(db, data, current_user)


@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_user_vehicles(db, current_user)


@router.delete("/{vehicle_id}")
def remove_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = delete_vehicle(db, vehicle_id, current_user.id)

    if not result:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return {"message": "Vehicle deleted"}