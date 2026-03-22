# Finora 💰

Finora is a full-stack personal finance management application that enables users to track income, expenses, and loans while providing insightful analytics through an interactive dashboard.

---

## 🚀 Features

- 💸 Income & Expense Tracking
- 📊 Real-time Financial Dashboard
- 🏷 Category-based Transactions
- 🏦 Loan & EMI Management System
- 📈 Monthly Expense Trend Visualization
- ⚡ Fast and Responsive UI

---

## 🛠 Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

### Frontend
- React (Vite)
- Axios
- Recharts

---

## 📂 Project Structure
finora/
├── finora-backend/
└── finora-frontend/


---

## ⚙️ Setup Instructions

### 🔧 Backend Setup/frontend setup

```bash
cd finora-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
Backend will run at:

http://127.0.0.1:8000

cd finora-frontend

# Install dependencies
npm install

# Run development server
npm run dev

Frontend will run at:

http://localhost:5173





