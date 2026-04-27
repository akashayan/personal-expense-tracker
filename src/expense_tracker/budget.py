from __future__ import annotations

from dataclasses import dataclass

from .models import Expense


@dataclass
class BudgetSummary:
    budget: float
    total_spent: float
    remaining: float
    is_over_budget: bool


def calculate_budget_summary(expenses: list[Expense], budget: float) -> BudgetSummary:
    """Return a BudgetSummary for all expenses against the given budget."""
    total_spent = round(sum(e.amount for e in expenses), 2)
    remaining = round(budget - total_spent, 2)
    return BudgetSummary(
        budget=budget,
        total_spent=total_spent,
        remaining=remaining,
        is_over_budget=total_spent > budget,
    )


def calculate_monthly_summary(expenses: list[Expense], month: str) -> list[Expense]:
    """Return only the expenses whose month_key() matches 'YYYY-MM'."""
    return [e for e in expenses if e.month_key() == month]
