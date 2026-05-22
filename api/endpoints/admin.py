from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.deps import get_db
from core.dependencies import get_admin_user
from models.utilisateurs import User
from models.compte import Account
from models.vehicule import Vehicule
from models.litige import Litige
from datetime import datetime, timedelta
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    users = db.query(User).all()
    return {
        "data": users,
        "total": len(users)
    }

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    data: dict, # {"role": "..."}
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = data.get("role")
    db.commit()
    db.refresh(user)
    return user

@router.get("/exports/{type}")
def export_data(
    type: str,
    format: str = "csv",
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    # Simuler un export
    return {"message": f"Export {type} au format {format} généré avec succès"}

@router.get("/statistics")
def get_stats(
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    total_passages = db.query(Passage).count()
    total_revenue = db.query(func.sum(Passage.amount)).filter(Passage.status != "echec").scalar() or 0
    total_vehicles = db.query(Vehicule).count()
    total_users = db.query(Account).count()
    
    # Passages today
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_passages = db.query(Passage).filter(Passage.datetime >= today).count()
    today_revenue = db.query(func.sum(Passage.amount)).filter(Passage.datetime >= today, Passage.status != "echec").scalar() or 0
    
    # Manual validation rate (simulated)
    manual_count = db.query(Passage).filter(Passage.status == "manual_validation").count()
    manual_rate = (manual_count / total_passages * 100) if total_passages > 0 else 0
    
    return {
        "totalPassages": total_passages,
        "totalRevenue": total_revenue,
        "manualValidationRate": manual_rate,
        "activeIncidents": db.query(Litige).filter(Litige.status == "ouvert").count(),
        "todayPassages": today_passages,
        "todayRevenue": today_revenue
    }

@router.get("/passages/realtime")
def get_realtime_passages(
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    # Return last 50 passages
    return db.query(Passage).order_by(Passage.datetime.desc()).limit(50).all()

@router.get("/litiges")
def get_litiges(
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    return db.query(Litige).all()

@router.put("/litiges/{id}")
def update_litige(
    id: int,
    status: str,
    resolution: str = None,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_user)
):
    litige = db.query(Litige).filter(Litige.id == id).first()
    if not litige:
        raise HTTPException(status_code=404, detail="Litige not found")
    
    litige.status = status
    if resolution:
        litige.resolution = resolution
    
    db.commit()
    db.refresh(litige)
    return litige
