from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Vehicule(Base):
    __tablename__ = "vehicules"

    id = Column(Integer, primary_key=True)
    plate = Column(String, unique=True, index=True)

    user_id = Column(Integer,ForeignKey("users.id"), nullable=True)
    company_id = Column(Integer,ForeignKey("companies.id"), nullable=True)

    type_id = Column(Integer)
    brand = Column(String)
    model = Column(String)
    color = Column(String)
    photo = Column(String)

    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="vehicules")
    company = relationship("Company", back_populates="vehicules")