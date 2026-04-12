from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)

    balance = Column(Integer, default=0)
    credit_used = Column(Integer, default=0)

    last_recharge = Column(DateTime)
    status = Column(String)