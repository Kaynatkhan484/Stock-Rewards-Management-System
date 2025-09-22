# models/ledger.py
from sqlalchemy import Column, String, TIMESTAMP, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from . import Base
import uuid

class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    reward_id = Column(UUID(as_uuid=True), nullable=False)  # links to reward_events
    user_id = Column(UUID(as_uuid=True), nullable=False)
    stock_symbol = Column(String, nullable=False)
    shares = Column(Numeric(18,6), nullable=False)  # fractional shares
    inr_value = Column(Numeric(18,4), nullable=False)
    brokerage_fee = Column(Numeric(18,4), default=0)
    stt_fee = Column(Numeric(18,4), default=0)
    gst_fee = Column(Numeric(18,4), default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Ledger(reward_id={self.reward_id}, user={self.user_id}, stock={self.stock_symbol})>"
