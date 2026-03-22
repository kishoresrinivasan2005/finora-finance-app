from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base  # ✅ IMPORT THE SAME BASE USED BY MODELS

DATABASE_URL = "postgresql://postgres:finora_db_123@localhost:5432/finora"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

