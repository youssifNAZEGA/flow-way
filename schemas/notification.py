from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    type: str
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    isRead: bool = Field(alias="is_read")
    createdAt: datetime = Field(alias="sent_at")

    class Config:
        from_attributes = True
        populate_by_name = True
