from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.deps import get_db
from core.dependencies import get_current_user
from schemas.notification import NotificationResponse
from services.notification_service import get_notifications, mark_as_read

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
def read_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_notifications(db, current_user.id)

@router.put("/{id}/read", response_model=NotificationResponse)
def read_notification(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notification = mark_as_read(db, id, current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
