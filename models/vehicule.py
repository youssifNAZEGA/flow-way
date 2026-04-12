from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    plate = Column(String, unique=True, index=True)

    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)

    type_id = Column(Integer)
    brand = Column(String)
    model = Column(String)
    color = Column(String)
    photo = Column(String)

    is_active = Column(Boolean, default=True)