from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.deps import get_db

from schemas.tariff_config import (
    VehicleTypeCreate
)

from services.vehicule_type_service import (
    create_vehicle_type,
    get_vehicle_types
)

router = APIRouter(
    prefix="/vehicle-types",
    tags=["Vehicle Types"]
)


@router.post("/")
def create_type(
        data: VehicleTypeCreate,
        db: Session = Depends(get_db)
):

    return create_vehicle_type(db, data)


@router.get("/")
def get_types(
        db: Session = Depends(get_db)
):

    return get_vehicle_types(db)