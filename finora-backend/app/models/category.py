from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150))

    created_at = Column(DateTime, default=datetime.utcnow)
