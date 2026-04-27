import pytest
from expense_tracker.budget import calculate_budget_summary, calculate_monthly_summary
from expense_tracker.models import Expense


@pytest.fixture
def expenses():
    return [
        Expense(date="2024-09-01", category="Food", amount=40.0, description="Groceries"),
        Expense(date="2024-09-15", category="Travel", amount=30.0, description="Bus"),
        Expense(date="2024-10-01", category="Food", amount=25.0, description="Dinner"),
    ]


def test_under_budget(expenses):
    summary = calculate_budget_summary(expenses, budget=200.0)
    assert not summary.is_over_budget
    assert summary.total_spent == 95.0
    assert summary.remaining == 105.0


def test_over_budget(expenses):
    summary = calculate_budget_summary(expenses, budget=50.0)
    assert summary.is_over_budget
    assert summary.remaining == -45.0


def test_empty_expenses():
    summary = calculate_budget_summary([], budget=100.0)
    assert summary.total_spent == 0.0
    assert not summary.is_over_budget


def test_monthly_summary_filters_correctly(expenses):
    sep = calculate_monthly_summary(expenses, "2024-09")
    assert len(sep) == 2
    assert all(e.month_key() == "2024-09" for e in sep)


def test_monthly_summary_empty_when_no_match(expenses):
    result = calculate_monthly_summary(expenses, "2024-11")
    assert result == []


def test_monthly_summary_exact_month(expenses):
    oct_expenses = calculate_monthly_summary(expenses, "2024-10")
    assert len(oct_expenses) == 1
    assert oct_expenses[0].description == "Dinner"
