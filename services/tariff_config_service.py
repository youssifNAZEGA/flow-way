from sqlalchemy.orm import Session

from models.tariff_config import TariffConfig
from models.typeVehicule import VehiculeType
from models.sitePeage import TollSite


def create_tariff_config(
        db: Session,
        data
):

    tariff = TariffConfig(
        vehicule_type_id=data.vehicule_type_id,
        toll_site_id=data.toll_site_id,
        amount=data.amount
    )

    db.add(tariff)
    db.commit()
    db.refresh(tariff)

    return tariff


def get_all_tariffs(db: Session):

    return db.query(TariffConfig).all()


def get_tariff_for_vehicle(
        db: Session,
        vehicule_type_id: int,
        toll_site_id: int
):

    return db.query(TariffConfig)\
        .filter(
            TariffConfig.vehicule_type_id == vehicule_type_id,
            TariffConfig.toll_site_id == toll_site_id,
            TariffConfig.is_active == True
        )\
        .first()


def update_tariff(
        db: Session,
        tariff_id: int,
        data
):

    tariff = db.query(TariffConfig)\
        .filter(TariffConfig.id == tariff_id)\
        .first()

    if not tariff:
        return None

    if data.amount is not None:
        tariff.amount = data.amount

    if data.is_active is not None:
        tariff.is_active = data.is_active

    db.commit()
    db.refresh(tariff)

    return tariff