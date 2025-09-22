# models/reward_events.py
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Numeric, String
from sqlalchemy.sql import func
from . import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class RewardEvent(Base):
    __tablename__ = "reward_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stock_symbol = Column(String, ForeignKey("stocks.symbol"), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    inr_value = Column(Numeric(18, 4), nullable=False)
    brokerage_fee = Column(Numeric(18, 4), nullable=False, default=0)
    stt_fee = Column(Numeric(18, 4), nullable=False, default=0)
    gst_fee = Column(Numeric(18, 4), nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
