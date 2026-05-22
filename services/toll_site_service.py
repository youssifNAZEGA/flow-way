from sqlalchemy.orm import Session

from models.sitePeage import TollSite


def create_toll_site(db: Session, data):

    toll_site = TollSite(
        name=data.name,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        lanes_count=data.lanes_count
    )

    db.add(toll_site)
    db.commit()
    db.refresh(toll_site)

    return toll_site


def get_all_toll_sites(db: Session):

    return db.query(TollSite)\
        .order_by(TollSite.id.desc())\
        .all()


def get_active_toll_sites(db: Session):

    return db.query(TollSite)\
        .filter(TollSite.is_active == True)\
        .all()


def get_toll_site_by_id(db: Session, site_id: int):

    return db.query(TollSite)\
        .filter(TollSite.id == site_id)\
        .first()


def update_toll_site(
        db: Session,
        site_id: int,
        data
):

    toll_site = get_toll_site_by_id(db, site_id)

    if not toll_site:
        return None

    if data.name is not None:
        toll_site.name = data.name

    if data.address is not None:
        toll_site.address = data.address

    if data.latitude is not None:
        toll_site.latitude = data.latitude

    if data.longitude is not None:
        toll_site.longitude = data.longitude

    if data.lanes_count is not None:
        toll_site.lanes_count = data.lanes_count

    if data.is_active is not None:
        toll_site.is_active = data.is_active

    db.commit()
    db.refresh(toll_site)

    return toll_site


def delete_toll_site(
        db: Session,
        site_id: int
):

    toll_site = get_toll_site_by_id(db, site_id)

    if not toll_site:
        return False

    db.delete(toll_site)
    db.commit()

    return True