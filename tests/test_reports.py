import pytest
from expense_tracker.models import Expense
from expense_tracker.reports import format_budget_summary, format_expense_row, print_expenses


@pytest.fixture
def expense():
    return Expense(date="2024-09-18", category="Food", amount=15.5, description="Lunch")


def test_format_expense_row_contains_date(expense):
    row = format_expense_row(1, expense)
    assert "2024-09-18" in row


def test_format_expense_row_contains_category(expense):
    row = format_expense_row(1, expense)
    assert "Food" in row


def test_format_expense_row_contains_2dp_amount(expense):
    row = format_expense_row(1, expense)
    assert "15.50" in row


def test_print_expenses_empty(capsys):
    print_expenses([])
    captured = capsys.readouterr()
    assert "No expenses recorded yet." in captured.out


def test_print_expenses_shows_all_rows(capsys, expense):
    expenses = [
        expense,
        Expense(date="2024-09-19", category="Travel", amount=30.0, description="Taxi"),
    ]
    print_expenses(expenses)
    captured = capsys.readouterr()
    assert "2024-09-18" in captured.out
    assert "2024-09-19" in captured.out
    assert "Taxi" in captured.out


def test_print_expenses_shows_count_footer(capsys, expense):
    print_expenses([expense])
    captured = capsys.readouterr()
    assert "1 expense(s) displayed." in captured.out


def test_format_budget_summary_under_budget():
    result = format_budget_summary(budget=100.0, total_spent=60.0, remaining=40.0, is_over=False)
    assert "left for the month" in result
    assert "40.00" in result


def test_format_budget_summary_over_budget():
    result = format_budget_summary(budget=100.0, total_spent=120.0, remaining=-20.0, is_over=True)
    assert "exceeded your budget" in result
    assert "20.00" in result
