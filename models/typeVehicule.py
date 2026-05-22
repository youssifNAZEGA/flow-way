from sqlalchemy import Column, Integer, String
from db.base import Base


class VehiculeType(Base):
    __tablename__ = "vehicule_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)