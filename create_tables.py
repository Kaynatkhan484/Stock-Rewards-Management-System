# create_tables.py
from models import Base  # Base from models/__init__.py
from models.users import User
from models.stocks import Stock
from models.reward_events import RewardEvent
from api.deps import engine  # engine from updated deps.py

print("Creating database tables...")

# Create all tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
