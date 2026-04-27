from __future__ import annotations

from datetime import datetime

from .models import DATE_FORMAT


def validate_date(value: str) -> str:
    """Return the stripped date string or raise ValueError."""
    value = value.strip()
    if not value:
        raise ValueError("Date must not be empty.")
    try:
        parsed = datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Invalid date format '{value}'. Use YYYY-MM-DD (e.g. 2024-09-18).")
    if parsed.date() > datetime.today().date():
        raise ValueError(f"Date '{value}' is in the future. Please enter today's date or earlier.")
    return value


def validate_positive_float(value: str) -> float:
    """Return a positive float rounded to 2dp or raise ValueError."""
    value = value.strip()
    if not value:
        raise ValueError("Value must not be empty.")
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"Invalid number '{value}'. Please enter a numeric value (e.g. 15.50).")
    if number <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(number, 2)


def validate_non_empty_str(value: str) -> str:
    """Return the stripped string or raise ValueError."""
    stripped = value.strip()
    if not stripped:
        raise ValueError("Value must not be empty.")
    return stripped
