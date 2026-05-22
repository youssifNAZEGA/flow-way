from pydantic import BaseModel
from datetime import datetime


class PassageCreate(BaseModel):
    vehicle_id: int
    site_id: int
    lane_id: int
    amount: int
    status: str
    image_plate: str | None = None


class PassageResponse(BaseModel):
    id: int

    plaque: str

    site: str

    voie: str

    amount: int

    status: str

    image_plate: str | None

    datetime: datetime

    class Config:
        from_attributes = True