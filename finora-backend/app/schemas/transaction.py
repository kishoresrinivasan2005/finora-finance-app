from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- TRANSACTION INPUT ----------
class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    transaction_type: str
    category_id: int
    payment_mode: Optional[str] = None


# ---------- TRANSACTION OUTPUT ----------
class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    category_id: int
    payment_mode: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- CATEGORY SUMMARY ----------
class CategorySummaryResponse(BaseModel):
    category_id: int
    category_name: str
    total_amount: float


# ---------- INCOME vs EXPENSE SUMMARY ----------
class IncomeExpenseSummaryResponse(BaseModel):
    income: float
    expense: float
    balance: float

class MonthlyExpenseTrendResponse(BaseModel):
    month: str   # YYYY-MM
    expense: float

class CategoryMonthlyBreakdownResponse(BaseModel):
    month: str          # YYYY-MM
    category_name: str
    total_amount: float

class MonthlyExpenseTrendResponse(BaseModel):
    month: str
    total_expense: float

    class Config:
        from_attributes = True

class TopCategoryResponse(BaseModel):
    category_name: str
    total_amount: float

    class Config:
        from_attributes = True

class DailyExpenseTrendResponse(BaseModel):
    date: str
    total_expense: float

    class Config:
        from_attributes = True

class DashboardCategoryResponse(BaseModel):
    category_name: str
    total_amount: float


class CurrentMonthDashboardResponse(BaseModel):
    income: float
    expense: float
    balance: float
    top_categories: list[DashboardCategoryResponse]

    class Config:
        from_attributes = True








