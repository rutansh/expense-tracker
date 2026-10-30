"""Tiny expense store backed by a JSON file. Amounts are stored as integer cents."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


@dataclass
class Expense:
    """A single expense."""

    expense_id: int
    amount_cents: int
    category: str
    note: str
    spent_on: str  # ISO date, YYYY-MM-DD


def parse_amount(text: str) -> int:
    """Convert a decimal string such as "12.50" into integer cents.

    Raises:
        ValueError: If the text is not a positive amount with at most two decimals.
    """
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"invalid amount: {text!r}") from exc
    if value <= 0 or value != value.quantize(Decimal("0.01")):
        raise ValueError("amount must be positive with at most two decimals")
    return int(value * 100)


class ExpenseStore:
    """Persist expenses in a JSON file."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def add(self, amount_cents: int, category: str, note: str = "") -> Expense:
        """Add an expense dated today and return it."""
        if amount_cents <= 0:
            raise ValueError("amount must be positive")
        if not category.strip():
            raise ValueError("category must not be empty")
        expenses = self.list_expenses()
        expense = Expense(
            expense_id=max((e.expense_id for e in expenses), default=0) + 1,
            amount_cents=amount_cents,
            category=category.strip().lower(),
            note=note.strip(),
            spent_on=date.today().isoformat(),
        )
        self._save([*expenses, expense])
        return expense

    def list_expenses(self) -> list[Expense]:
        """Return all expenses in creation order."""
        if not self._path.exists():
            return []
        return [Expense(**item) for item in json.loads(self._path.read_text())]

    def total_by_category(self) -> dict[str, int]:
        """Return total cents spent per category."""
        totals: dict[str, int] = {}
        for expense in self.list_expenses():
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount_cents
        return totals

    def _save(self, expenses: list[Expense]) -> None:
        self._path.write_text(json.dumps([asdict(e) for e in expenses], indent=2))
