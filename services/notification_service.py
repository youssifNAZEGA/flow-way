from sqlalchemy.orm import Session
from models.notification import Notification

def get_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.sent_at.desc()).all()

def mark_as_read(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification

def create_notification(db: Session, user_id: int, type: str, title: str, message: str):
    notification = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
