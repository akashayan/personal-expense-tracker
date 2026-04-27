from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
CSV_FIELDS = ["date", "category", "amount", "description"]


@dataclass
class Expense:
    date: str
    category: str
    amount: float
    description: str

    def __post_init__(self) -> None:
        self.amount = round(float(self.amount), 2)

    def to_dict(self) -> dict[str, str | float]:
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Expense":
        for key in ("date", "category", "description"):
            if not str(data.get(key, "")).strip():
                raise ValueError(f"Field '{key}' must not be blank.")
        try:
            amount = float(data["amount"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid amount: {data.get('amount')!r}") from exc
        return cls(
            date=str(data["date"]).strip(),
            category=str(data["category"]).strip(),
            amount=amount,
            description=str(data["description"]).strip(),
        )

    def month_key(self) -> str:
        return datetime.strptime(self.date, DATE_FORMAT).strftime("%Y-%m")
