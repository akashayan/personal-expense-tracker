import csv
from datetime import date, timedelta
from pathlib import Path

import pytest
from expense_tracker.models import CSV_FIELDS, Expense
from expense_tracker.storage import load_expenses, save_expenses


def test_missing_file_returns_empty(tmp_path):
    result = load_expenses(tmp_path / "nonexistent.csv")
    assert result == []


def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "expenses.csv"
    expenses = [
        Expense(date="2024-01-01", category="Food", amount=10.0, description="Lunch"),
        Expense(date="2024-01-02", category="Travel", amount=25.5, description="Bus"),
    ]
    save_expenses(expenses, path)
    loaded = load_expenses(path)

    assert len(loaded) == 2
    assert loaded[0].date == "2024-01-01"
    assert loaded[0].amount == 10.0
    assert loaded[1].category == "Travel"


def test_skips_row_with_invalid_amount(tmp_path, capsys):
    path = tmp_path / "expenses.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerow({"date": "2024-01-01", "category": "Food", "amount": "bad", "description": "x"})
        writer.writerow({"date": "2024-01-02", "category": "Food", "amount": "5.00", "description": "y"})

    loaded = load_expenses(path)
    captured = capsys.readouterr()

    assert len(loaded) == 1
    assert loaded[0].description == "y"
    assert "warning" in captured.out


def test_skips_row_with_blank_field(tmp_path, capsys):
    path = tmp_path / "expenses.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerow({"date": "", "category": "Food", "amount": "5.00", "description": "x"})
        writer.writerow({"date": "2024-01-02", "category": "Food", "amount": "5.00", "description": "y"})

    loaded = load_expenses(path)
    captured = capsys.readouterr()

    assert len(loaded) == 1
    assert "warning" in captured.out


def test_empty_list_produces_header_only(tmp_path):
    path = tmp_path / "expenses.csv"
    save_expenses([], path)

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert "date" in lines[0]


def test_skips_future_dated_row(tmp_path, capsys):
    path = tmp_path / "expenses.csv"
    future = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerow({"date": future, "category": "Food", "amount": "10.00", "description": "future entry"})
        writer.writerow({"date": "2024-01-01", "category": "Food", "amount": "5.00", "description": "past entry"})

    loaded = load_expenses(path)
    captured = capsys.readouterr()

    assert len(loaded) == 1
    assert loaded[0].description == "past entry"
    assert "warning" in captured.out
    assert "future" in captured.out
