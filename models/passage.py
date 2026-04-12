from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Passage(Base):
    __tablename__ = "passages"

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer)
    site_id = Column(Integer)
    lane_id = Column(Integer)

    datetime = Column(DateTime, server_default=func.now())

    amount = Column(Integer)
    status = Column(String)
    image_plate = Column(String)