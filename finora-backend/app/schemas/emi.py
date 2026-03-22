from pydantic import BaseModel
from datetime import date


class EMIResponse(BaseModel):
    id: int
    loan_id: int
    installment_number: int
    due_date: date
    amount: float
    principal_component: float
    interest_component: float
    status: str
    paid_on: date | None


    class Config:
        from_attributes = True

class EMIPaymentResponse(BaseModel):
    message: str
    emi_id: int
    paid_on: date
