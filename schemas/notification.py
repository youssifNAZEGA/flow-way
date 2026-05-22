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