from models.compte import Account
from models.transaction import Transaction
from sqlalchemy.orm import Session
import datetime

def get_or_create_compte(db: Session, current_user):

    if current_user.role == "entreprise":
        compte = db.query(Account).filter(
            Account.company_id == current_user.company_id
        ).first()

        if not compte:
            compte = Account(
                company_id=current_user.company_id,
                balance=0.0
            )
            db.add(compte)
            db.commit()
            db.refresh(compte)
    else:
        compte = db.query(Account).filter(
            Account.user_id == current_user.id
        ).first()

        if not compte:
            compte = Account(
                user_id=current_user.id,
                balance=0.0
            )
            db.add(compte)
            db.commit()
            db.refresh(compte)

    return compte

def get_solde_response(db: Session, current_user):
    account = get_or_create_compte(db, current_user)
    # Mapping for frontend camelCase
    return {
        "id": account.id,
        "balance": account.balance,
        "status": account.status,
        "trustCreditsRemaining": account.trust_credits_remaining,
        "minBalanceAlert": account.min_balance_alert
    }


def recharge_account(db: Session, current_user, amount: float, method: str = "card"):

    account = get_or_create_compte(db, current_user)

    if amount <= 0:
        raise Exception("Montant invalide")
    
    account.balance += amount
    account.last_recharge = datetime.datetime.now()
    
    if account.balance >= 0:
        account.credit_used = 0
        account.trust_credits_remaining = 2
        account.status = "actif"

    db.commit()

    # Create transaction
    transaction = Transaction(
        account_id=account.id,
        amount=amount,
        type="recharge",
        balance_after=account.balance,
        reference="RECHARGE",
        # Adding method to transaction would require model update, 
        # but the model doesn't have it yet. Let's stick to base for now.
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)

    return get_solde_response(db, current_user)

def get_transactions(db: Session, current_user):
    account = get_or_create_compte(db, current_user)
    return db.query(Transaction).filter(Transaction.account_id == account.id).order_by(Transaction.created_at.desc()).all()

def update_min_balance(db: Session, current_user, amount: float):
    account = get_or_create_compte(db, current_user)
    account.min_balance_alert = amount
    db.commit()
    db.refresh(account)
    return get_solde_response(db, current_user)
