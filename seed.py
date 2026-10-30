"""Fill an empty expense list with sample data for demos: ``uv run python seed.py``."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path

from api import DEFAULT_FILE
from expenses import Expense, ExpenseStore

# (days ago, amount in cents, category, note)
SAMPLE_EXPENSES = [
    (13, 4250, "groceries", "Weekly shop"),
    (11, 1890, "transport", "Train pass top-up"),
    (9, 6400, "dining", "Team dinner"),
    (7, 1299, "subscriptions", "Streaming"),
    (5, 3875, "groceries", "Farmers market"),
    (3, 2200, "transport", "Taxi to airport"),
    (2, 1450, "dining", "Lunch with Sam"),
    (0, 899, "groceries", "Coffee beans"),
]


def seed(path: Path = DEFAULT_FILE) -> int:
    """Write the sample expenses. Does nothing if there are already expenses.

    Returns:
        The number of expenses added.
    """
    if ExpenseStore(path).list_expenses():
        return 0
    today = date.today()
    expenses = [
        Expense(
            expense_id=number,
            amount_cents=cents,
            category=category,
            note=note,
            spent_on=(today - timedelta(days=days_ago)).isoformat(),
        )
        for number, (days_ago, cents, category, note) in enumerate(SAMPLE_EXPENSES, start=1)
    ]
    path.write_text(json.dumps([asdict(e) for e in expenses], indent=2))
    return len(expenses)


if __name__ == "__main__":
    added = seed()
    print(f"added {added} sample expenses" if added else "list is not empty; nothing added")
