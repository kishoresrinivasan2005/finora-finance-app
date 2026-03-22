from fastapi import FastAPI

from app.core.database import engine, Base
from app.models import user, transaction, category, loan, emi  # ensure models are registered

from app.routes.transactions import router as transaction_router
from app.routes.categories import router as category_router
from app.routes.loans import router as loan_router
from app.routes.emis import router as emi_router
from fastapi.middleware.cors import CORSMiddleware



# 1️⃣ Create FastAPI app
app = FastAPI(title="Finora Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2️⃣ Startup event (create tables)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# 3️⃣ Register routers
app.include_router(transaction_router)
app.include_router(category_router)
app.include_router(loan_router)
app.include_router(emi_router)


# 4️⃣ Root endpoint
@app.get("/")
def root():
    return {"message": "Finora backend is connected to PostgreSQL"}