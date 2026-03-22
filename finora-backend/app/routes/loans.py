from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.loan import Loan
from app.models.emi import EMI

from app.schemas.loan import LoanCreate, LoanResponse
from app.schemas.emi import EMIResponse

from app.utils.loan_calculator import calculate_emi, generate_emi_schedule


router = APIRouter(prefix="/loans", tags=["Loans"])


# -----------------------------
# Create Loan
# -----------------------------
@router.post("/", response_model=LoanResponse)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):

    # Calculate EMI
    emi_amount = calculate_emi(
        loan.principal_amount,
        loan.interest_rate,
        loan.tenure_months
    )

    total_payable = emi_amount * loan.tenure_months
    total_interest = total_payable - loan.principal_amount

    # Create loan object
    new_loan = Loan(
        user_id=loan.user_id,
        lender_name=loan.lender_name,
        principal_amount=loan.principal_amount,
        interest_rate=loan.interest_rate,
        tenure_months=loan.tenure_months,
        start_date=loan.start_date,
        emi_amount=emi_amount,
        total_interest=total_interest,
        total_payable=total_payable
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    # Generate EMI schedule
    schedule = generate_emi_schedule(
        loan.principal_amount,
        loan.interest_rate,
        loan.tenure_months,
        loan.start_date
    )

    # Insert EMI rows
    for emi in schedule:
        new_emi = EMI(
            loan_id=new_loan.id,
            user_id=loan.user_id,
            installment_number=emi["installment_number"],
            due_date=emi["due_date"],
            amount=emi["amount"],
            principal_component=emi["principal_component"],
            interest_component=emi["interest_component"]
        )

        db.add(new_emi)

    db.commit()

    return new_loan


# -----------------------------
# Get All Loans
# -----------------------------
@router.get("/", response_model=List[LoanResponse])
def get_loans(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Loan)
    if user_id:
        query = query.filter(Loan.user_id == user_id)
    return query.order_by(Loan.start_date.desc()).all()


# -----------------------------
# Get EMI Schedule
# -----------------------------
@router.get("/{loan_id}/emis", response_model=List[EMIResponse])
def get_loan_emis(loan_id: int, db: Session = Depends(get_db)):

    emis = (
        db.query(EMI)
        .filter(EMI.loan_id == loan_id)
        .order_by(EMI.installment_number)
        .all()
    )

    return emis