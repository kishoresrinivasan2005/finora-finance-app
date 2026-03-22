from app.db.base import Base
from app.db.session import engine

# Import ALL models so SQLAlchemy registers them
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.loan import Loan
from app.models.emi import EMI


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Tables created successfully")

