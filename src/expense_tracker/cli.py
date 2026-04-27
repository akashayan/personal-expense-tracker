from __future__ import annotations

import sys
from pathlib import Path

from .budget import calculate_budget_summary
from .models import Expense
from .prompts import prompt_date, prompt_non_empty_str, prompt_positive_float
from .reports import format_budget_summary, print_expenses
from .storage import load_expenses, save_expenses

EXPENSES_FILE = Path("expenses.csv")


def display_menu() -> None:
    print("\n============================")
    print("   Personal Expense Tracker ")
    print("============================")
    print("  1. Add expense")
    print("  2. View expenses")
    print("  3. Track budget")
    print("  4. Save expenses")
    print("  5. Exit")
    print("============================")


def handle_add(expenses: list[Expense]) -> None:
    print("\n--- Add Expense ---")
    date = prompt_date("Date")
    category = prompt_non_empty_str("Category (e.g. Food, Travel, Utilities)")
    amount = prompt_positive_float("Amount")
    description = prompt_non_empty_str("Description")

    expense = Expense(date=date, category=category, amount=amount, description=description)
    expenses.append(expense)
    print(f"  Expense added: {expense.to_dict()}")


def handle_view(expenses: list[Expense]) -> None:
    print_expenses(expenses)


def handle_budget(expenses: list[Expense], budget: float) -> float:
    """Display budget tracking. If no budget set, prompt for one first. Returns (possibly updated) budget."""
    print("\n--- Track Budget ---")
    if budget <= 0:
        budget = prompt_positive_float("Enter your monthly budget")

    summary = calculate_budget_summary(expenses, budget)
    print(format_budget_summary(summary.budget, summary.total_spent, summary.remaining, summary.is_over_budget))
    return budget


def handle_save(expenses: list[Expense], path: Path) -> None:
    save_expenses(expenses, path)


def run(path: Path = EXPENSES_FILE) -> None:
    expenses = load_expenses(path)
    if expenses:
        print(f"Loaded {len(expenses)} expense(s) from {path.name}.")

    budget: float = 0.0

    while True:
        display_menu()
        try:
            choice = input("Select an option (1-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nInterrupted. Saving and exiting...")
            save_expenses(expenses, path)
            sys.exit(0)

        if choice == "1":
            handle_add(expenses)
        elif choice == "2":
            handle_view(expenses)
        elif choice == "3":
            budget = handle_budget(expenses, budget)
        elif choice == "4":
            handle_save(expenses, path)
        elif choice == "5":
            save_expenses(expenses, path)
            print("Goodbye!")
            sys.exit(0)
        else:
            print("  Invalid option. Please enter a number between 1 and 5.")
