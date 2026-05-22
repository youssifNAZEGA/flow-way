from sqlalchemy.orm import Session
from models.vehicule import Vehicule
from models.typeVehicule import VehiculeType


def create_vehicle(db: Session, data, current_user):
    # Map vehicleType name/id to vehicle_type_id
    vt = db.query(VehiculeType).filter(VehiculeType.name == data.vehicleType).first()
    if not vt:
        # Fallback to first if not found or create?
        vt = db.query(VehiculeType).first()
        if not vt:
            # Create a default one if none exists
            vt = VehiculeType(name=data.vehicleType, description="Auto-created")
            db.add(vt)
            db.commit()
            db.refresh(vt)

    vehicle = Vehicule(
        plate=data.licensePlate,
        brand=data.brand,
        model=data.model,
        vehicle_type_id=vt.id
    )

    existing = db.query(Vehicule).filter(Vehicule.plate == data.licensePlate).first()
    if existing:
        raise Exception("Plaque déjà enregistrée")

    if current_user.role == "entreprise":
        vehicle.company_id = current_user.company_id
    else:
        vehicle.user_id = current_user.id

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def get_user_vehicles(db: Session, current_user):
    if current_user.role == "entreprise":
        return db.query(Vehicule).filter(
            Vehicule.company_id == current_user.company_id
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
