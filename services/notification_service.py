from sqlalchemy.orm import Session
from models.notification import Notification
from models.utilisateurs import User
from schemas.notification import NotificationRead, NotificationCreate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def get_user_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[NotificationRead]:
    """Récupérer les notifications d'un utilisateur (BF-041)"""
    notifications = (
        db.query(Notification)
        .filter(Notification.utilisateur_id == user_id)
        .order_by(Notification.date_envoi.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [NotificationRead.model_validate(n) for n in notifications]

def mark_as_read(db: Session, notif_id: int, user_id: int) -> NotificationRead:
    """Marquer une notification comme lue"""
    notif = db.query(Notification).filter(
        Notification.id == notif_id,
        Notification.utilisateur_id == user_id
    ).first()
    if not notif:
        raise ValueError("Notification introuvable")
    
    notif.lu = True
    db.commit()
    db.refresh(notif)
    return NotificationRead.model_validate(notif)

def create_notification(db: Session, user_id: int, notif_type: str, title: str, message: str) -> NotificationRead:
    """Créer une notification (BF-041 à BF-047)"""
    new_notif = Notification(
        utilisateur_id=user_id,
        type=notif_type,
        titre=title,
        message=message,
        lu=False
    )
    db.add(new_notif)
    db.commit()
    db.refresh(new_notif)
    return NotificationRead.model_validate(new_notif)

# Notifications spécifiques selon le cahier des charges
def notify_passage_success(db: Session, user_id: int, plaque: str, montant: float, site: str):
    """BF-041: Notification passage réussi"""
    return create_notification(
        db, user_id, "PASSAGE_REUSSI", 
        "✅ Passage validé", 
        f"Véhicule {plaque} passé à {site}. Débit: {montant:.2f}€"
    )

def notify_low_balance(db: Session, user_id: int, solde: float, seuil: float = 5.0):
    """BF-042: Alerte solde faible"""
    if solde <= seuil:
        return create_notification(
            db, user_id, "SOLDE_FAIBLE",
            "⚠️ Solde faible",
            f"Votre solde est de {solde:.2f}€. Pensez à recharger."
        )

def notify_negative_balance(db: Session, user_id: int, solde: float, credits_used: int):
    """BF-043: Notification solde négatif"""
    return create_notification(
        db, user_id, "SOLDE_NEGATIF",
        "🚨 Solde négatif",
        f"Solde: {solde:.2f}€. Crédit de confiance {credits_used}/2 utilisé. Veuillez recharger."
    )

def notify_credit_used(db: Session, user_id: int, credits_remaining: int):
    """BF-046: Notification crédit de confiance utilisé"""
    return create_notification(
        db, user_id, "CREDIT_UTILISE",
        "💳 Crédit de confiance activé",
        f"Passage autorisé malgré solde insuffisant. Il vous reste {credits_remaining} crédit(s)."
    )

def notify_account_blocked(db: Session, user_id: int):
    """BF-047: Notification blocage compte"""
    return create_notification(
        db, user_id, "COMPTE_BLOQUE",
        " Compte bloqué",
        "Crédits de confiance épuisés. Veuillez recharger pour continuer à utiliser le péage."
    )