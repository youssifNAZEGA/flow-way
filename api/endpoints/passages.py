from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from services.passage_service import process_passage
from services.passage_history_service import get_all_histories, get_history_by_id
from utils.ocr import detect_plaque
from core.dependencies import get_current_user
from schemas.passage import PassageResponse
from typing import List

router = APIRouter(prefix="/passages", tags=["Passages"])

@router.post("/image")
async def process_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    image_path = "temp.jpg"
    with open(image_path, "wb") as f:
        f.write(contents)

    # OCR
    plaque = detect_plaque(image_path)

    if not plaque:
        return {
            "success": False,
            "message": "Plaque non trouvée"
        }

    result = process_passage(db=db, plaque=plaque)
    return {
        "success": True,
        "plaque": plaque,
        "result": result
    }

@router.get("/", response_model=dict)
def get_passages(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role == "admin":
        passages = get_all_histories(db)
    else:
        from models.vehicule import Vehicule
        from models.passage import Passage
        user_vehicles = db.query(Vehicule).filter(Vehicule.user_id == current_user.id).all()
        vehicle_ids = [v.id for v in user_vehicles]
        passages = db.query(Passage).filter(Passage.vehicle_id.in_(vehicle_ids)).all()
    
    return {
        "data": passages,
        "total": len(passages)
    }

@router.get("/{id}", response_model=PassageResponse)
def get_passage(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    history = get_history_by_id(db, id)
    if not history:
        raise HTTPException(status_code=404, detail="Passage introuvable")
    return history
