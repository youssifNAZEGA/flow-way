from pydantic import BaseModel

class CompteResponse(BaseModel):
    id: int
    balance: float
    status: str

    class Config:
        from_attributes = True


class RechargeSchema(BaseModel):
    montant: float