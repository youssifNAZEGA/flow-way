from sqlalchemy import Column, Float, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"), unique=True, nullable=True)
    balance = Column(Float, default=0)
    credit_used = Column(Integer, default=0)

    last_recharge = Column(DateTime)
    status = Column(String, default="actif")

    owner = relationship("User")
    company = relationship("Company")