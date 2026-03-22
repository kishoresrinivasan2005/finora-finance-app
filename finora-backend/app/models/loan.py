from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    lender_name = Column(String, nullable=False)

    principal_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Annual %

    tenure_months = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)

    emi_amount = Column(Float, nullable=False)
    total_interest = Column(Float, nullable=False)
    total_payable = Column(Float, nullable=False)

    status = Column(String, default="active")  # active / closed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
