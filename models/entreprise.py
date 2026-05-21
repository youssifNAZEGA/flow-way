from sqlalchemy import Column, Integer, String,  ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    siret = Column(String)
    address = Column(String)
    contact = Column(String)

    vehicules = relationship("Vehicule", back_populates="company")