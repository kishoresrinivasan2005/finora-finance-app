from sqlalchemy.orm import declarative_base

Base = declarative_base()
from app.models.loan import Loan
from app.models.emi import EMI
