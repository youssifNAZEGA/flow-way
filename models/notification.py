from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    type = Column(String)
    title = Column(String)
    message = Column(String)

    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime, server_default=func.now())