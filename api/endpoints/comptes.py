from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.deps import get_db
from core.dependencies import get_current_user
from schemas.compte import CompteResponse, RechargeSchema
from services.compte_services import get_solde, recharge_account

router = APIRouter(prefix="/compte", tags=["Compte"])


@router.get("/", response_model=CompteResponse)
def read_solde(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_solde(db, current_user)


@router.post("/recharge", response_model=CompteResponse)
def recharge(
    data: RechargeSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return recharge_account(db, current_user, data.montant)