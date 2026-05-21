from models.vehicule import Vehicule
from models.compte import Account
from models.passage import Passage

def process_passage(db, plaque):

    vehicule = db.query(Vehicule).filter(Vehicule.plate == plaque).first()

    if not vehicule:
        return {"error": "Véhicule non trouvé"}

    compte = db.query(Account).filter(
        Account.user_id == vehicule.user_id
    ).first()

    if not compte:
        return {"error": "Compte non trouvé"}

    montant = 500  

    if compte.balance < montant:
        passage = Passage(
            vehicle_id=vehicule.id,
            amount=montant,
            status="echec"
        )
        db.add(passage)
        db.commit()
        return {"error": "Solde insuffisant"}

    compte.balance -= montant

    passage = Passage(
        vehicle_id=vehicule.id,
        amount=montant,
        status="reussi"
    )

    db.add(passage)
    db.commit()
    db.refresh(passage)

    return passage