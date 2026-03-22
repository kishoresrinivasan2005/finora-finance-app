from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = Category(name=category.name.strip())

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse
from typing import List


@router.get("/{category_id}/transactions", response_model=List[TransactionResponse])
def get_transactions_by_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.category_id == category_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    return transactions
