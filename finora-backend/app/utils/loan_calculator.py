from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate EMI using standard reducing balance formula
    """
    monthly_rate = annual_rate / 12 / 100

    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months \
          / ((1 + monthly_rate) ** tenure_months - 1)

    return round(emi, 2)


def generate_emi_schedule(
    principal: float,
    annual_rate: float,
    tenure_months: int,
    start_date: date,
):
    """
    Generates full amortization schedule
    Returns list of dicts
    """

    monthly_rate = annual_rate / 12 / 100
    emi = calculate_emi(principal, annual_rate, tenure_months)

    balance = principal
    schedule = []

    for i in range(1, tenure_months + 1):
        interest_component = balance * monthly_rate
        principal_component = emi - interest_component

        balance -= principal_component

        schedule.append({
            "installment_number": i,
            "due_date": start_date + relativedelta(months=i - 1),
            "amount": round(emi, 2),
            "principal_component": round(principal_component, 2),
            "interest_component": round(interest_component, 2),
        })

    return schedule
