from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Link to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Money details
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(10), nullable=False)  # income / expense
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)     
    payment_mode = Column(String(20))                      # upi / bank

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", backref="transactions")
    category = relationship("Category", backref="transactions") 
