from pydantic import BaseModel

class CompteResponse(BaseModel):
    id: int
    balance: float
    status: str
    trustCreditsRemaining: int
    minBalanceAlert: float

    class Config:
        from_attributes = True
        # For mapping snake_case to camelCase automatically
        # but since I used exact names in response, it's fine.
        # However, let's be explicit.

class RechargeSchema(BaseModel):
    amount: float
    method: str = "card"
