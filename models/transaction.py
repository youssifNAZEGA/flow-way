from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer)
    amount = Column(Integer)
    type = Column(String)

    balance_after = Column(Integer)
    reference = Column(String)

    created_at = Column(DateTime, server_default=func.now())