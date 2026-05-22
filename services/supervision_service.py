from sqlalchemy.orm import Session
from models.passage import Passage
# from models.sitePeage import SitePeage
from models.vehicule import Vehicule
from models.utilisateurs import User
from schemas.supervision import PassageBrief, SupervisionStats
from datetime import datetime, timedelta
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def get_realtime_passages(db: Session, site_id: Optional[int] = None, limit: int = 50) -> List[PassageBrief]:
    """BF-054: Supervision des passages en temps réel"""
    query = (
        db.query(Passage)
        .join(Vehicule, Passage.vehicule_id == Vehicule.id, isouter=True)
        .order_by(Passage.date_heure.desc())
    )
    if site_id:
        query = query.filter(Passage.site_peage_id == site_id)
        
    passages = query.limit(limit).all()
    result = []
    for p in passages:
        result.append(PassageBrief(
            id=p.id,
            plaque=p.vehicule.plaque if p.vehicule else "Inconnu",
            site_nom=p.site_peage.nom if p.site_peage else "Inconnu",
            date_heure=p.date_heure,
            montant=p.montant,
            statut=p.statut,
            image_plaque_url=p.image_plaque,
            valide_par=p.valide_par
        ))
    return result

def get_dashboard_stats(db: Session, site_id: Optional[int] = None) -> SupervisionStats:
    """Statistiques du tableau de bord"""
    query = db.query(Passage)
    if site_id:
        query = query.filter(Passage.site_peage_id == site_id)

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_passages = query.filter(Passage.date_heure >= today_start).all()

    total = len(today_passages)
    success = sum(1 for p in today_passages if p.statut == "reussi")
    manual = sum(1 for p in today_passages if p.statut == "manuel")
    lpr_rate = (success / total * 100) if total > 0 else 0.0

    return SupervisionStats(
        total_passages_today=total,
        success_count=success,
        manual_validation_count=manual,
        lpr_success_rate=round(lpr_rate, 2)
    )

def manually_validate_passage(db: Session, passage_id: int, manager_id: int) -> PassageBrief:
    """BF-036: Validation manuelle d'un passage (échec LPR)"""
    passage = db.query(Passage).filter(Passage.id == passage_id).first()
    if not passage:
        raise ValueError("Passage introuvable")
    if passage.statut not in ["echec_lpr", "en_attente"]:
        raise ValueError(f"Ce passage ne peut pas être validé manuellement (statut: {passage.statut})")

    passage.statut = "manuel"
    passage.valide_par = manager_id
    passage.date_validation = datetime.utcnow()
    db.commit()
    db.refresh(passage)

    return PassageBrief(
        id=passage.id,
        plaque=passage.vehicule.plaque if passage.vehicule else "Inconnu",
        site_nom=passage.site_peage.nom if passage.site_peage else "Inconnu",
        date_heure=passage.date_heure,
        montant=passage.montant,
        statut=passage.statut,
        image_plaque_url=passage.image_plaque,
        valide_par=passage.valide_par
    )

def get_passages_by_date_range(db: Session, start_date: datetime, end_date: datetime, site_id: Optional[int] = None) -> List[PassageBrief]:
    """BF-061: Rapport des passages par période"""
    query = (
        db.query(Passage)
        .filter(Passage.date_heure.between(start_date, end_date))
        .join(Vehicule, isouter=True)
        .order_by(Passage.date_heure.desc())
    )
    if site_id:
        query = query.filter(Passage.site_peage_id == site_id)
    
    passages = query.all()
    return [PassageBrief.model_validate(p) for p in passages]