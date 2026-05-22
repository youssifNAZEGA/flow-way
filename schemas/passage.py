from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PassageResponse(BaseModel):
    id: int
    vehicleId: int = Field(alias="vehicle_id")
    siteId: Optional[int] = Field(alias="site_id")
    laneId: Optional[int] = Field(alias="lane_id")
    timestamp: datetime = Field(alias="datetime")
    amount: float
    status: str
    imagePlate: Optional[str] = Field(alias="image_plate")

    class Config:
        from_attributes = True
        populate_by_name = True
