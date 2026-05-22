<<<<<<< HEAD
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
=======
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationRead(BaseModel):
    id: int
    utilisateur_id: int
    type: str
    titre: str
    message: str
    lu: bool
    date_envoi: Optional[datetime]

    model_config = {"from_attributes": True}

class NotificationCreate(BaseModel):
    utilisateur_id: int
    type: str
    titre: str
    message: str
>>>>>>> 6ef03b7f56918ea2250fb88f09a6b3295817bef0
