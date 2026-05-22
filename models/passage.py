from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.base import Base
from sqlalchemy.orm import relationship



class Passage(Base):
    __tablename__ = "passages"

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer, ForeignKey("vehicules.id"))
    site_id = Column(Integer, ForeignKey("toll_sites.id"))
    lane_id = Column(Integer, ForeignKey("toll_lanes.id"))

    datetime = Column(DateTime, server_default=func.now())

    amount = Column(Integer)
    status = Column(String)
    image_plate = Column(String)



    vehicle = relationship("Vehicule")
    site = relationship("TollSite")
    lane = relationship("TollLane")