from pydantic import BaseModel

class VehicleCreate(BaseModel):
    plate: str
    brand: str
    model: str


class VehicleResponse(BaseModel):
    id: int
    plate: str
    brand: str
    model: str

    class Config:
        from_attributes = True