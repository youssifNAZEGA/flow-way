from sqlalchemy.orm import Session

from models.typeVehicule import VehiculeType


def create_vehicle_type(
        db: Session,
        data
):

    vehicle_type = VehiculeType(
        name=data.name,
        description=data.description
    )

    db.add(vehicle_type)
    db.commit()
    db.refresh(vehicle_type)

    return vehicle_type


def get_vehicle_types(db: Session):

    return db.query(VehiculeType).all()