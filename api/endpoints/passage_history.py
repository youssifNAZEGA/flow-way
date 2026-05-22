from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.deps import get_db

from services.passage_history_service import (
    create_passage_history,
    get_all_histories,
    get_history_by_id
)

from schemas.passage_history import PassageCreate


router = APIRouter(
    prefix="/historiques",
    tags=["Historiques"]
)


@router.post("/")
def create_history(
    data: PassageCreate,
    db: Session = Depends(get_db)
):

    return create_passage_history(
        db=db,
        vehicle_id=data.vehicle_id,
        site_id=data.site_id,
        lane_id=data.lane_id,
        amount=data.amount,
        status=data.status,
        image_plate=data.image_plate
    )


@router.get("/")
def get_histories(db: Session = Depends(get_db)):

    return get_all_histories(db)


@router.get("/{passage_id}")
def get_history(
    passage_id: int,
    db: Session = Depends(get_db)
):

    history = get_history_by_id(db, passage_id)

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Historique introuvable"
        )

    return history