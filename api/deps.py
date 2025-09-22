# api/deps.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Correct DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Chaman%401320@localhost:5432/stocky_db"
)


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

