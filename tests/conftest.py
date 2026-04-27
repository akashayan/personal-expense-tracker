import pytest
from expense_tracker.models import Expense


@pytest.fixture
def sample_expense():
    return Expense(date="2024-09-18", category="Food", amount=15.5, description="Lunch")


@pytest.fixture
def sample_expense_dict():
    return {"date": "2024-09-18", "category": "Food", "amount": "15.5", "description": "Lunch"}
