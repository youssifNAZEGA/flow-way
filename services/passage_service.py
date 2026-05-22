from sqlalchemy.orm import Session
from models.vehicule import Vehicule
from models.compte import Account
from models.passage import Passage
from models.tariff_config import TariffConfig
from models.transaction import Transaction
from models.notification import Notification
from models.sitePeage import TollSite
from models.entreprise import Company
from models.utilisateurs import User
import datetime

def process_passage(db: Session, plaque: str, site_id: int = None, lane_id: int = None):
    # 1. Trouver le véhicule
    vehicule = db.query(Vehicule).filter(Vehicule.plate == plaque).first()
    if not vehicule:
        return {"error": "Véhicule non trouvé"}

    # 2. Déterminer le site de péage
    if site_id is None:
        site = db.query(TollSite).first()
        if not site:
            return {"error": "Aucun site de péage configuré"}
        site_id = site.id

    # 3. Trouver le tarif
    tariff = db.query(TariffConfig).filter(
        TariffConfig.vehicule_type_id == vehicule.vehicle_type_id,
        TariffConfig.toll_site_id == site_id,
        TariffConfig.is_active == True
    ).first()

    if not tariff:
        # Tarif par défaut si non trouvé
        amount = 500
    else:
        amount = tariff.amount

    # 4. Trouver le compte (individu ou entreprise)
    if vehicule.company_id:
        compte = db.query(Account).filter(Account.company_id == vehicule.company_id).first()
        owner_id = db.query(User).filter(User.id == db.query(Company).filter(Company.id == vehicule.company_id).first().user_id).first().id if vehicule.company_id else None
    else:
        compte = db.query(Account).filter(Account.user_id == vehicule.user_id).first()
        owner_id = vehicule.user_id

    if not compte:
        return {"error": "Compte non trouvé pour ce véhicule"}

    # 5. Vérifier le solde + crédit de confiance
    # Max 2 passages autorisés à solde nul (credit_used < 2)
    can_pass = False
    status = "reussi"
    
    if compte.balance >= amount:
        compte.balance -= amount
        can_pass = True
    elif compte.trust_credits_remaining > 0:
        compte.balance -= amount # Le solde devient négatif
        compte.credit_used += 1
        compte.trust_credits_remaining -= 1
        can_pass = True
        status = "trust_credit_used"
    else:
        status = "blocked"
        can_pass = False

    # 6. Enregistrer le passage
    passage = Passage(
        vehicle_id=vehicule.id,
        site_id=site_id,
        lane_id=lane_id,
        amount=amount,
        status=status
    )
    db.add(passage)
    db.commit()
    db.refresh(passage)

    if can_pass:
        # 7. Créer la transaction
        transaction = Transaction(
            account_id=compte.id,
            amount=amount,
            type="debit",
            balance_after=compte.balance,
            reference=f"PASSAGE_{passage.id}"
        )
        db.add(transaction)

        # 8. Créer la notification
        msg = f"Passage au péage réussi. Montant: {amount} FCFA."
        if status == "trust_credit_used":
            msg += f" Crédit de confiance utilisé. Reste: {compte.trust_credits_remaining}/2. Veuillez recharger votre compte."
        
        notification = Notification(
            user_id=owner_id,
            type=status if status != "reussi" else "passage_success",
            title="Passage Péage",
            message=msg
        )
        db.add(notification)
        
        db.commit()

        return {
            "success": True,
            "passage_id": passage.id,
            "status": status,
            "amount": amount,
            "balance": compte.balance,
            "message": "Barrière ouverte"
        }
    else:
        return {
            "success": False,
            "status": "echec",
            "message": "Solde insuffisant et crédits de confiance épuisés"
        }
