from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Litige(Base):
    __tablename__ = "litige"

    id = Column(Integer, primary_key=True)

    passage_id = Column(Integer)
    user_id = Column(Integer)

    reason = Column(String)
    status = Column(String)

    resolution = Column(String)

    created_at = Column(DateTime, server_default=func.now())