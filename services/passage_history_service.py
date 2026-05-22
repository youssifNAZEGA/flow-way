from sqlalchemy.orm import Session

from models.passage import Passage
from models.vehicule import Vehicule
from models.sitePeage import TollSite
from models.voiePeage import TollLane


def create_passage_history(
        db: Session,
        vehicle_id: int,
        site_id: int,
        lane_id: int,
        amount: int,
        status: str,
        image_plate: str = None
):

    passage = Passage(
        vehicle_id=vehicle_id,
        site_id=site_id,
        lane_id=lane_id,
        amount=amount,
        status=status,
        image_plate=image_plate
    )

    db.add(passage)
    db.commit()
    db.refresh(passage)

    return passage


def get_all_histories(db: Session):

    passages = db.query(Passage)\
        .order_by(Passage.datetime.desc())\
        .all()

    results = []

    for p in passages:

        vehicle = db.query(Vehicule)\
            .filter(Vehicule.id == p.vehicle_id)\
            .first()

        site = db.query(TollSite)\
            .filter(TollSite.id == p.site_id)\
            .first()

        lane = db.query(TollLane)\
            .filter(TollLane.id == p.lane_id)\
            .first()

        results.append({
            "id": p.id,
            "plaque": vehicle.plate if vehicle else "Inconnue",
            "site": site.name if site else "Inconnu",
            "voie": lane.name if lane else "Inconnue",
            "amount": p.amount,
            "status": p.status,
            "image_plate": p.image_plate,
            "datetime": p.datetime
        })

    return results


def get_history_by_id(db: Session, passage_id: int):

    p = db.query(Passage)\
        .filter(Passage.id == passage_id)\
        .first()

    if not p:
        return None

    vehicle = db.query(Vehicule)\
        .filter(Vehicule.id == p.vehicle_id)\
        .first()

    site = db.query(TollSite)\
        .filter(TollSite.id == p.site_id)\
        .first()

    lane = db.query(TollLane)\
        .filter(TollLane.id == p.lane_id)\
        .first()

    return {
        "id": p.id,
        "plaque": vehicle.plate if vehicle else "Inconnue",
        "site": site.name if site else "Inconnu",
        "voie": lane.name if lane else "Inconnue",
        "amount": p.amount,
        "status": p.status,
        "image_plate": p.image_plate,
        "datetime": p.datetime
    }