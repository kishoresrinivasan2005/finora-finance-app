from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.models.emi import EMI
from app.models.transaction import Transaction
from app.schemas.emi import EMIPaymentResponse


router = APIRouter(prefix="/emis", tags=["EMIs"])


@router.patch("/{emi_id}/pay", response_model=EMIPaymentResponse)
def pay_emi(emi_id: int, db: Session = Depends(get_db)):

    emi = db.query(EMI).filter(EMI.id == emi_id).first()

    if not emi:
        raise HTTPException(status_code=404, detail="EMI not found")

    if emi.status == "paid":
        raise HTTPException(status_code=400, detail="EMI already paid")

    emi.status = "paid"
    emi.paid_on = date.today()

    from app.models.category import Category
    category = db.query(Category).filter(Category.name == "Loan EMI").first()
    if not category:
        category = Category(name="Loan EMI")
        db.add(category)
        db.commit()
        db.refresh(category)

    # 🔹 Create expense transaction
    transaction = Transaction(
        user_id=emi.user_id,
        amount=emi.amount,
        transaction_type="expense",
        category_id=category.id,
        payment_mode="loan",
        created_at=emi.paid_on
    )

    db.add(transaction)

    db.commit()
    db.refresh(emi)

    return {
        "message": "EMI paid and expense recorded",
        "emi_id": emi.id,
        "paid_on": emi.paid_on
    }