import pytest
from expense_tracker.models import Expense


def test_amount_rounded_to_2dp():
    e = Expense(date="2024-01-01", category="Food", amount=9.999, description="Test")
    assert e.amount == 10.0


def test_amount_already_2dp():
    e = Expense(date="2024-01-01", category="Food", amount=9.99, description="Test")
    assert e.amount == 9.99


def test_to_dict_has_all_keys(sample_expense):
    d = sample_expense.to_dict()
    assert set(d.keys()) == {"date", "category", "amount", "description"}


def test_to_dict_amount_is_float(sample_expense):
    d = sample_expense.to_dict()
    assert isinstance(d["amount"], float)


def test_from_dict_round_trip(sample_expense_dict):
    expense = Expense.from_dict(sample_expense_dict)
    assert expense.date == "2024-09-18"
    assert expense.category == "Food"
    assert expense.amount == 15.5
    assert expense.description == "Lunch"


def test_from_dict_bad_amount_raises():
    with pytest.raises(ValueError, match="Invalid amount"):
        Expense.from_dict({"date": "2024-01-01", "category": "Food", "amount": "abc", "description": "x"})


def test_from_dict_blank_date_raises():
    with pytest.raises(ValueError, match="date"):
        Expense.from_dict({"date": "  ", "category": "Food", "amount": "5.0", "description": "x"})


def test_from_dict_blank_description_raises():
    with pytest.raises(ValueError, match="description"):
        Expense.from_dict({"date": "2024-01-01", "category": "Food", "amount": "5.0", "description": ""})


def test_month_key(sample_expense):
    assert sample_expense.month_key() == "2024-09"
