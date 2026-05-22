from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.deps import get_db

from schemas.tariff_config import (
    TariffConfigCreate,
    TariffConfigUpdate
)

from services.tariff_config_service import (
    create_tariff_config,
    get_all_tariffs,
    update_tariff
)

router = APIRouter(
    prefix="/tariffs",
    tags=["Tariffs"]
)


@router.post("/")
def create_tariff(
        data: TariffConfigCreate,
        db: Session = Depends(get_db)
):

    return create_tariff_config(db, data)


@router.get("/")
def get_tariffs(
        db: Session = Depends(get_db)
):

    return get_all_tariffs(db)


@router.put("/{tariff_id}")
def update_tariff_route(
        tariff_id: int,
        data: TariffConfigUpdate,
        db: Session = Depends(get_db)
):

    tariff = update_tariff(
        db,
        tariff_id,
        data
    )

    if not tariff:
        raise HTTPException(
            status_code=404,
            detail="Tarif introuvable"
        )

    return tariff