from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.deps import get_db
from db.security import get_current_user
from services.notification_service import get_user_notifications, mark_as_read
from schemas.notification import NotificationRead
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationRead])
def fetch_notifications(
    skip: int = Query(0, ge=0, description="Nombre de notifications à ignorer"),
    limit: int = Query(50, ge=1, le=200, description="Nombre max de notifications"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """BF-041: Récupérer les notifications de l'utilisateur connecté"""
    return get_user_notifications(db, current_user.id, skip, limit)

@router.put("/{notif_id}/read", response_model=NotificationRead)
def mark_notification_read(
    notif_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Marquer une notification comme lue"""
    try:
        return mark_as_read(db, notif_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))