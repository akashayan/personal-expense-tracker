from __future__ import annotations

import csv
from pathlib import Path

from datetime import datetime

from .models import CSV_FIELDS, DATE_FORMAT, Expense


def load_expenses(path: Path) -> list[Expense]:
    """Load expenses from a CSV file. Returns [] if the file does not exist."""
    if not path.exists():
        return []

    today = datetime.today().date()
    expenses: list[Expense] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  # row 1 is the header
            try:
                expense = Expense.from_dict(dict(row))
            except ValueError as exc:
                print(f"  [warning] Row {i} in {path.name}: {exc} — skipped.")
                continue
            if datetime.strptime(expense.date, DATE_FORMAT).date() > today:
                print(f"  [warning] Row {i} in {path.name}: date '{expense.date}' is in the future — skipped.")
                continue
            expenses.append(expense)

    return expenses


def save_expenses(expenses: list[Expense], path: Path) -> None:
    """Save expenses to a CSV file, creating it if necessary."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense.to_dict())
    print(f"  Expenses saved to {path.name}.")
