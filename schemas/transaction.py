from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class TransactionResponse(BaseModel):
    id: int
    account_id: int = Field(alias="accountId")
    amount: float
    type: str
    balance_after: float = Field(alias="balanceAfter")
    reference: Optional[str]
    createdAt: datetime = Field(alias="created_at")

    class Config:
        from_attributes = True
        populate_by_name = True

class TransactionListResponse(BaseModel):
    data: List[TransactionResponse]
    total: int
