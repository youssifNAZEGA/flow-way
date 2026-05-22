from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    licensePlate: str
    vehicleType: str
    brand: Optional[str] = "Inconnu"
    model: Optional[str] = "Inconnu"


class VehicleResponse(BaseModel):
    id: int
    plate: str
    brand: Optional[str]
    model: Optional[str]
    vehicle_type_id: Optional[int]

    class Config:
        from_attributes = True
