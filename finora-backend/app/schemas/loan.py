from pydantic import BaseModel
from datetime import date
from typing import Optional


class LoanCreate(BaseModel):
    user_id: int
    lender_name: str
    principal_amount: float
    interest_rate: float
    tenure_months: int
    start_date: date


class LoanResponse(BaseModel):
    id: int
    user_id: int
    lender_name: str
    principal_amount: float
    interest_rate: float
    tenure_months: int
    start_date: date

    emi_amount: float
    total_interest: float
    total_payable: float

    status: str

    class Config:
        from_attributes = True