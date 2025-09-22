# stocky/api/routes/rewards.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from stocky.models.ledger import Ledger
from stocky.models.reward_events import RewardEvent
from stocky.api.db import get_db  # <-- added







router = APIRouter()


# -------------------------
# POST /reward → Create reward + ledger entry
# -------------------------
@router.post("/reward")
def create_reward(
    user_id: str,
    stock_symbol: str,
    quantity: float,
    inr_value: float,
    brokerage_fee: float = 0,
    stt_fee: float = 0,
    gst_fee: float = 0,
    db: Session = Depends(get_db)
):
    try:
        today = date.today()
        # Duplicate check for same user + stock + today
        existing = db.query(RewardEvent).filter(
            RewardEvent.user_id == user_id,
            RewardEvent.stock_symbol == stock_symbol,
            func.date(RewardEvent.created_at) == today
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Reward already exists for today")

        # Create reward
        new_reward = RewardEvent(
            user_id=user_id,
            stock_symbol=stock_symbol,
            quantity=quantity,
            inr_value=inr_value,
            brokerage_fee=brokerage_fee,
            stt_fee=stt_fee,
            gst_fee=gst_fee
        )
        db.add(new_reward)
        db.commit()
        db.refresh(new_reward)

        # Create ledger entry
        ledger_entry = Ledger(
            reward_id=new_reward.id,
            user_id=user_id,
            stock_symbol=stock_symbol,
            shares=quantity,
            inr_value=inr_value,
            brokerage_fee=brokerage_fee,
            stt_fee=stt_fee,
            gst_fee=gst_fee
        )
        db.add(ledger_entry)
        db.commit()

        return {"reward_id": new_reward.id, "status": "success"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# -------------------------
# PUT /reward/{id} → Update reward + ledger
# -------------------------
@router.put("/reward/{reward_id}")
def update_reward(
    reward_id: str,
    user_id: str,
    stock_symbol: str,
    quantity: float,
    inr_value: float,
    brokerage_fee: float = 0,
    stt_fee: float = 0,
    gst_fee: float = 0,
    db: Session = Depends(get_db)
):
    try:
        reward = db.query(RewardEvent).filter(RewardEvent.id == reward_id).first()
        if not reward:
            raise HTTPException(status_code=404, detail="Reward not found")

        # Update reward
        reward.user_id = user_id
        reward.stock_symbol = stock_symbol
        reward.quantity = quantity
        reward.inr_value = inr_value
        reward.brokerage_fee = brokerage_fee
        reward.stt_fee = stt_fee
        reward.gst_fee = gst_fee
        db.commit()
        db.refresh(reward)

        # Update ledger
        ledger = db.query(Ledger).filter(Ledger.reward_id == reward_id).first()
        if ledger:
            ledger.user_id = user_id
            ledger.stock_symbol = stock_symbol
            ledger.shares = quantity
            ledger.inr_value = inr_value
            ledger.brokerage_fee = brokerage_fee
            ledger.stt_fee = stt_fee
            ledger.gst_fee = gst_fee
            db.commit()

        return {"reward_id": reward.id, "status": "updated"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# -------------------------
# DELETE /reward/{reward_id} → Refund/cancel reward + ledger
# -------------------------
@router.delete("/reward/{reward_id}")
def delete_reward(reward_id: str, db: Session = Depends(get_db)):
    try:
        reward = db.query(RewardEvent).filter(RewardEvent.id == reward_id).first()
        if not reward:
            raise HTTPException(status_code=404, detail="Reward not found")

        # Delete ledger entry
        db.query(Ledger).filter(Ledger.reward_id == reward_id).delete()

        # Delete reward
        db.delete(reward)
        db.commit()

        return {"status": "deleted"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# -------------------------
# GET /rewards → List all rewards
# -------------------------
@router.get("/rewards")
def list_rewards(db: Session = Depends(get_db)):
    try:
        rewards = db.query(RewardEvent).all()
        return rewards
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# -------------------------
# GET /reward/{id} → Fetch single reward
# -------------------------
@router.get("/reward/{reward_id}")
def get_reward(reward_id: str, db: Session = Depends(get_db)):
    try:
        reward = db.query(RewardEvent).filter(RewardEvent.id == reward_id).first()
        if not reward:
            raise HTTPException(status_code=404, detail="Reward not found")
        return reward
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# -------------------------
# GET /today-stocks/{user_id} → Rewards for today
# -------------------------
@router.get("/today-stocks/{user_id}")
def get_today_stocks(user_id: str, db: Session = Depends(get_db)):
    today = date.today()
    rewards = db.query(RewardEvent).filter(
        RewardEvent.user_id == user_id,
        func.date(RewardEvent.created_at) == today
    ).all()
    return rewards


# -------------------------
# GET /historical-inr/{user_id} → Daily INR value
# -------------------------
@router.get("/historical-inr/{user_id}")
def get_historical_inr(user_id: str, db: Session = Depends(get_db)):
    result = db.query(
        func.date(Ledger.created_at).label("date"),
        func.sum(Ledger.inr_value).label("total_inr")
    ).filter(
        Ledger.user_id == user_id
    ).group_by(
        func.date(Ledger.created_at)
    ).order_by(func.date(Ledger.created_at)).all()

    return [{"date": str(r.date), "total_inr": float(r.total_inr)} for r in result]


# -------------------------
# GET /stats/{user_id} → Shares today + current INR portfolio
# -------------------------
@router.get("/stats/{user_id}")
def get_stats(user_id: str, db: Session = Depends(get_db)):
    today = date.today()

    shares_today = db.query(
        Ledger.stock_symbol,
        func.sum(Ledger.shares).label("total_shares")
    ).filter(
        Ledger.user_id == user_id,
        func.date(Ledger.created_at) == today
    ).group_by(Ledger.stock_symbol).all()

    total_inr = db.query(func.sum(Ledger.inr_value)).filter(Ledger.user_id == user_id).scalar() or 0

    return {
        "shares_today": {r.stock_symbol: float(r.total_shares) for r in shares_today},
        "current_inr_value": float(total_inr)
    }


# -------------------------
# GET /portfolio/{user_id} → Holdings per stock
# -------------------------
@router.get("/portfolio/{user_id}")
def get_portfolio(user_id: str, db: Session = Depends(get_db)):
    portfolio = db.query(
        Ledger.stock_symbol,
        func.sum(Ledger.shares).label("total_shares"),
        func.sum(Ledger.inr_value).label("total_inr")
    ).filter(
        Ledger.user_id == user_id
    ).group_by(Ledger.stock_symbol).all()

    return [
        {
            "stock_symbol": r.stock_symbol,
            "shares": float(r.total_shares),
            "inr_value": float(r.total_inr)
        }
        for r in portfolio
    ]
