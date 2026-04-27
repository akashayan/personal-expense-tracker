from __future__ import annotations

from .validators import validate_date, validate_non_empty_str, validate_positive_float


def prompt_date(label: str) -> str:
    """Prompt until a valid YYYY-MM-DD date is entered."""
    while True:
        raw = input(f"  {label} (YYYY-MM-DD): ")
        try:
            return validate_date(raw)
        except ValueError as exc:
            print(f"  {exc}")


def prompt_positive_float(label: str) -> float:
    """Prompt until a positive numeric value is entered."""
    while True:
        raw = input(f"  {label}: ")
        try:
            return validate_positive_float(raw)
        except ValueError as exc:
            print(f"  {exc}")


def prompt_non_empty_str(label: str) -> str:
    """Prompt until a non-empty string is entered."""
    while True:
        raw = input(f"  {label}: ")
        try:
            return validate_non_empty_str(raw)
        except ValueError as exc:
            print(f"  {exc}")
