from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class TollSite(Base):
    __tablename__ = "toll_sites"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    address = Column(String)

    latitude = Column(String)
    longitude = Column(String)

    is_active = Column(Boolean, default=True)
    lanes_count = Column(Integer)