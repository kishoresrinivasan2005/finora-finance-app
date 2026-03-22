from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import date, datetime, time
from app.schemas.transaction import TopCategoryResponse
from app.schemas.transaction import DailyExpenseTrendResponse
from app.schemas.transaction import CurrentMonthDashboardResponse



from app.core.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category

from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    CategorySummaryResponse,
    IncomeExpenseSummaryResponse,
    MonthlyExpenseTrendResponse,
    CategoryMonthlyBreakdownResponse,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

ALLOWED_TRANSACTION_TYPES = {"income", "expense"}

# --------------------------------------------------
# CREATE TRANSACTION (POST JSON)
# --------------------------------------------------
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
):
    cleaned_type = transaction.transaction_type.strip().lower()

    if cleaned_type not in ALLOWED_TRANSACTION_TYPES:
        raise HTTPException(
            status_code=400,
            detail="transaction_type must be 'income' or 'expense'",
        )

    db_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        transaction_type=cleaned_type,
        category_id=transaction.category_id,
        payment_mode=transaction.payment_mode.strip().lower()
        if transaction.payment_mode
        else None,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# --------------------------------------------------
# GET TRANSACTIONS (FILTER + PAGINATION)
# --------------------------------------------------
@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    user_id: Optional[int] = None,
    category_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    if transaction_type:
        cleaned_type = transaction_type.strip().lower()
        query = query.filter(Transaction.transaction_type == cleaned_type)

    if start_date:
        query = query.filter(
            Transaction.created_at >= datetime.combine(start_date, time.min)
        )

    if end_date:
        query = query.filter(
            Transaction.created_at <= datetime.combine(end_date, time.max)
        )

    return (
        query.order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# --------------------------------------------------
# CATEGORY SUMMARY
# --------------------------------------------------
@router.get(
    "/summary/by-category",
    response_model=List[CategorySummaryResponse],
)
def transactions_summary_by_category(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            Transaction.category_id,
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(Category, Transaction.category_id == Category.id)
        .group_by(Transaction.category_id, Category.name)
    )

    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    return query.all()


# --------------------------------------------------
# INCOME vs EXPENSE SUMMARY
# --------------------------------------------------
@router.get(
    "/summary/income-vs-expense",
    response_model=IncomeExpenseSummaryResponse,
)
def income_vs_expense_summary(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    income_query = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == "income"
    )

    expense_query = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == "expense"
    )

    if user_id:
        income_query = income_query.filter(Transaction.user_id == user_id)
        expense_query = expense_query.filter(Transaction.user_id == user_id)

    income = income_query.scalar() or 0.0
    expense = expense_query.scalar() or 0.0

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
    }


# --------------------------------------------------
# MONTHLY EXPENSE TREND  ✅ FIXED
# --------------------------------------------------
@router.get(
    "/summary/monthly-expense-trend",
    response_model=List[MonthlyExpenseTrendResponse],
)
def monthly_expense_trend(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            func.to_char(
                func.coalesce(Transaction.created_at, func.now()),
                "YYYY-MM",
            ).label("month"),
            func.sum(Transaction.amount).label("total_expense"),
        )
        .filter(Transaction.transaction_type == "expense")
    )

    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    results = (
        query
        .group_by("month")
        .order_by("month")
        .all()
    )

    # 🔑 Explicit serialization to avoid 500 errors
    return [
        {
            "month": row.month,
            "total_expense": float(row.total_expense or 0),
        }
        for row in results
    ]

@router.get(
    "/summary/top-categories",
    response_model=List[TopCategoryResponse],
)
def top_categories_current_month(
    user_id: Optional[int] = None,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    today = datetime.utcnow()

    start_of_month = datetime(today.year, today.month, 1)
    end_of_month = datetime(today.year, today.month, 28, 23, 59, 59)

    query = (
        db.query(
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(Category, Transaction.category_id == Category.id)
        .filter(Transaction.transaction_type == "expense")
        .filter(Transaction.created_at >= start_of_month)
        .filter(Transaction.created_at <= end_of_month)
    )

    # ✅ FILTER FIRST
    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    # ✅ THEN GROUP / ORDER / LIMIT
    results = (
        query
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "category_name": row.category_name,
            "total_amount": float(row.total_amount or 0),
        }
        for row in results
    ]

@router.get(
    "/summary/daily-expense-trend",
    response_model=List[DailyExpenseTrendResponse],
)
def daily_expense_trend(
    user_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            func.to_char(
                func.coalesce(Transaction.created_at, func.now()),
                "YYYY-MM-DD",
            ).label("date"),
            func.sum(Transaction.amount).label("total_expense"),
        )
        .filter(Transaction.transaction_type == "expense")
    )

    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    if start_date:
        query = query.filter(
            Transaction.created_at >= datetime.combine(start_date, time.min)
        )

    if end_date:
        query = query.filter(
            Transaction.created_at <= datetime.combine(end_date, time.max)
        )

    results = (
        query
        .group_by("date")
        .order_by("date")
        .all()
    )

    # 🔑 Explicit serialization (important)
    return [
        {
            "date": row.date,
            "total_expense": float(row.total_expense or 0),
        }
        for row in results
    ]



# --------------------------------------------------
# CATEGORY-WISE MONTHLY BREAKDOWN
# --------------------------------------------------
@router.get(
    "/summary/category-monthly",
    response_model=List[CategoryMonthlyBreakdownResponse],
)
def category_monthly_breakdown(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            func.to_char(
                func.coalesce(Transaction.created_at, func.now()),
                "YYYY-MM",
            ).label("month"),
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(Category, Transaction.category_id == Category.id)
        .filter(Transaction.transaction_type == "expense")
        .group_by("month", Category.name)
        .order_by("month", Category.name)
    )

    if user_id:
        query = query.filter(Transaction.user_id == user_id)

    return query.all()

@router.get(
    "/summary/current-month",
    response_model=CurrentMonthDashboardResponse,
)
def current_month_dashboard(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    today = datetime.utcnow()
    start_of_month = datetime(today.year, today.month, 1)
    end_of_month = datetime(today.year, today.month, 28, 23, 59, 59)

    income_query = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.transaction_type == "income")
        .filter(Transaction.created_at >= start_of_month)
        .filter(Transaction.created_at <= end_of_month)
    )

    expense_query = (
        db.query(func.sum(Transaction.amount))
        .filter(Transaction.transaction_type == "expense")
        .filter(Transaction.created_at >= start_of_month)
        .filter(Transaction.created_at <= end_of_month)
    )

    if user_id:
        income_query = income_query.filter(Transaction.user_id == user_id)
        expense_query = expense_query.filter(Transaction.user_id == user_id)

    income = income_query.scalar() or 0.0
    expense = expense_query.scalar() or 0.0

    category_query = (
        db.query(
            Category.name.label("category_name"),
            func.sum(Transaction.amount).label("total_amount"),
        )
        .join(Category, Transaction.category_id == Category.id)
        .filter(Transaction.transaction_type == "expense")
        .filter(Transaction.created_at >= start_of_month)
        .filter(Transaction.created_at <= end_of_month)
    )

    if user_id:
        category_query = category_query.filter(Transaction.user_id == user_id)

    category_results = (
        category_query
        .group_by(Category.name)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(5)
        .all()
    )

    top_categories = [
        {
            "category_name": row.category_name,
            "total_amount": float(row.total_amount or 0),
        }
        for row in category_results
    ]

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "top_categories": top_categories,
    }


