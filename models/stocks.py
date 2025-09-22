from sqlalchemy import Column, String, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from . import Base


class Stock(Base):
    __tablename__ = "stocks"

    symbol = Column(String, primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(18, 4), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
