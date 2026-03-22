from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class EMI(Base):
    __tablename__ = "emis"

    id = Column(Integer, primary_key=True, index=True)

    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    installment_number = Column(Integer, nullable=False)

    due_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

    principal_component = Column(Float, nullable=False)
    interest_component = Column(Float, nullable=False)

    status = Column(String, default="pending")  
    # pending / paid / missed

    paid_on = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
