from models.compte import Account

def get_or_create_compte(db, current_user):

    if current_user.role == "entreprise":
        compte = db.query(Account).filter(
            Account.company_id == current_user.company_id
        ).first()

        if not compte:
            compte = Account(
                company_id=current_user.company_id,
                balance=0.0
            )
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

def get_solde(db, current_user):
    return get_or_create_compte(db, current_user)


def recharge_account(db, current_user, montant):

    account = get_or_create_compte(db, current_user)

    if montant <= 0:
        raise Exception("Montant invalide")
    account.balance += montant

    db.commit()
    db.refresh(account)

    return account