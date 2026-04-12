from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class TollLane(Base):
    __tablename__ = "toll_lanes"

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer)
    lane_number = Column(Integer)

    camera_id = Column(String)
    barrier_id = Column(String)

    status = Column(String)