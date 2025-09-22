from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from datetime import datetime

class RewardCreate(BaseModel):
    user_id: UUID
    stock_symbol: str
    quantity: Decimal
    inr_value: Decimal
    brokerage_fee: Decimal = 0
    stt_fee: Decimal = 0
    gst_fee: Decimal = 0

class RewardResponse(RewardCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
