from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from db.base import Base


class TariffConfig(Base):
    __tablename__ = "tariff_configs"

    id = Column(Integer, primary_key=True, index=True)

    vehicule_type_id = Column(
        Integer,
        ForeignKey("vehicule_types.id")
    )

    toll_site_id = Column(
        Integer,
        ForeignKey("toll_sites.id")
    )

    amount = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)

    vehicle_type = relationship("TypeVehicule")

    toll_site = relationship("TollSite")