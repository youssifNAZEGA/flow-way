from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.deps import get_db
from core.dependencies import get_current_user
from schemas.compte import CompteResponse, RechargeSchema
from schemas.transaction import TransactionResponse, TransactionListResponse
from services.compte_services import get_solde_response, recharge_account, get_transactions, update_min_balance
from typing import List

router = APIRouter(prefix="/account", tags=["Compte"])


@router.get("/balance", response_model=CompteResponse)
def read_solde(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_solde_response(db, current_user)


@router.post("/recharge", response_model=CompteResponse)
def recharge(
    data: RechargeSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return recharge_account(db, current_user, data.amount, data.method)

@router.put("/balance", response_model=CompteResponse)
def update_alert(
    data: dict, # {"minBalanceAlert": ...}
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_min_balance(db, current_user, data.get("minBalanceAlert"))

@router.get("/transactions", response_model=TransactionListResponse)
def read_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    transactions = get_transactions(db, current_user)
    # Map created_at to createdAt for frontend if needed, 
    # but Pydantic Config from_attributes should handle it if names match.
    # In TransactionResponse I have created_at. Let's fix it to createdAt.
    return {
        "data": transactions,
        "total": len(transactions)
    }
