# stocky/api/main.py
from fastapi import FastAPI
from stocky.api.routes import rewards, users  # <-- updated

app = FastAPI(title="Stocky API")

app.include_router(rewards.router, prefix="/rewards", tags=["Rewards"])
app.include_router(users.router, prefix="/users", tags=["Users"])

