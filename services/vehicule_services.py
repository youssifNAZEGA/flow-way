from sqlalchemy.orm import Session
from models.vehicule import Vehicule


def create_vehicle(db, data, current_user):

    vehicle = Vehicule(
        plate=data.plate,
        brand=data.brand,
        model=data.model
    )

    existing = db.query(Vehicule).filter(Vehicule.plate == data.plate).first()

    if existing:
        raise Exception("Plaque déjà enregistrée")

    if current_user.role == "entreprise":
        vehicle.company_id = current_user.entreprise_id
    else:
        vehicle.user_id = current_user.id

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


def get_user_vehicles(db, current_user):

    if current_user.role == "entreprise":
        return db.query(Vehicule).filter(
            Vehicule.entreprise_id == current_user.entreprise_id
        ).all()

    return db.query(Vehicule).filter(
        Vehicule.user_id == current_user.id
    ).all()

def delete_vehicle(db: Session, vehicle_id, user_id):
    vehicle = db.query(Vehicule).filter(
        Vehicule.id == vehicle_id,
        Vehicule.user_id == user_id
    ).first()

    if not vehicle:
        return None

    db.delete(vehicle)
    db.commit()
    return True