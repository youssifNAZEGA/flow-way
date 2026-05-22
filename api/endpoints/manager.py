from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from core.dependencies import get_current_user
from models.passage import Passage
from models.litige import Litige
from models.compte import Account
from models.transaction import Transaction

router = APIRouter(prefix="/manager", tags=["Manager"])

@router.get("/validations")
def get_validations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")
    
    # Passages nécessitant une validation (status pending ou manual_validation)
    passages = db.query(Passage).filter(Passage.status == "manual_validation").all()
    return {
        "data": passages,
        "total": len(passages)
    }

@router.post("/validations/{id}")
def validate_passage(
    id: int,
    data: dict, # {"action": "approve/reject", "justification": "..."}
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")

    passage = db.query(Passage).filter(Passage.id == id).first()
    if not passage:
        raise HTTPException(status_code=404, detail="Passage not found")
    
    action = data.get("action")
    passage.status = "reussi" if action == "approve" else "echec"
    passage.image_plate = data.get("justification") # On détourne ce champ pour la justification pour l'instant
    
    db.commit()
    db.refresh(passage)
    return passage

@router.get("/disputes")
def get_disputes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")
        
    litiges = db.query(Litige).all()
    return {
        "data": litiges,
        "total": len(litiges)
    }

@router.post("/disputes/{id}/resolve")
def resolve_dispute(
    id: int,
    data: dict, # {"resolution": "...", "refund": true/false}
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")

    litige = db.query(Litige).filter(Litige.id == id).first()
    if not litige:
        raise HTTPException(status_code=404, detail="Litige not found")
    
    litige.status = "resolu"
    litige.resolution = data.get("resolution")
    
    if data.get("refund"):
        # Logique de remboursement
        passage = db.query(Passage).filter(Passage.id == litige.passage_id).first()
        if passage:
            # Trouver le compte
            from models.vehicule import Vehicule
            vehicule = db.query(Vehicule).filter(Vehicule.id == passage.vehicle_id).first()
            if vehicule:
                compte = db.query(Account).filter(Account.user_id == vehicule.user_id).first()
                if compte:
                    compte.balance += passage.amount
                    # Créer transaction
                    trans = Transaction(
                        account_id=compte.id,
                        amount=passage.amount,
                        type="refund",
                        balance_after=compte.balance,
                        reference=f"REFUND_{litige.id}"
                    )
                    db.add(trans)

    db.commit()
    return litige

@router.get("/realtime")
def get_realtime(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Manager access required")
    
    return db.query(Passage).order_by(Passage.datetime.desc()).limit(20).all()
