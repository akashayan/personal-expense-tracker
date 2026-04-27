from __future__ import annotations

from .models import CSV_FIELDS, Expense


def format_expense_row(index: int, expense: Expense) -> str:
    """Return a formatted single-line string for one expense."""
    return (
        f"  {index:<4} {expense.date:<12} {expense.category:<15} "
        f"{expense.amount:>10.2f}  {expense.description}"
    )


def print_expenses(expenses: list[Expense]) -> None:
    """Print all expenses as a formatted table to stdout."""
    print("\n--- All Expenses ---")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    print(f"  {'#':<4} {'Date':<12} {'Category':<15} {'Amount':>10}  {'Description'}")
    print("  " + "-" * 65)

    for i, expense in enumerate(expenses, start=1):
        print(format_expense_row(i, expense))

    print("  " + "-" * 65)
    print(f"  {len(expenses)} expense(s) displayed.")


def format_budget_summary(budget: float, total_spent: float, remaining: float, is_over: bool) -> str:
    """Return a multi-line budget summary string."""
    lines = [
        f"  Monthly budget : {budget:.2f}",
        f"  Total spent    : {total_spent:.2f}",
    ]
    if is_over:
        lines.append(f"  You have exceeded your budget by {abs(remaining):.2f}!")
    else:
        lines.append(f"  You have {remaining:.2f} left for the month.")
    return "\n".join(lines)
