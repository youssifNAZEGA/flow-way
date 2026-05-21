from pydantic import BaseModel

class PassageCreate(BaseModel):
    plaque: str


class PassageResponse(BaseModel):
    id: int
    amount: float
    statut: str

    class Config:
        from_attributes = True