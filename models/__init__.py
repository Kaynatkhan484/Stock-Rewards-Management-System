# models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/stocky_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# expose models for easier imports
# models/__init__.py
# stocky/models/__init__.py
from .ledger import Ledger
from .reward_events import RewardEvent





# # models/__init__.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# import os

# # PostgreSQL connection URL
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/stocky_db")

# # Create SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Create a configured "Session" class
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for all models
# Base = declarative_base()
