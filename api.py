"""Web backend: a small JSON API and the single-page UI, on top of ``ExpenseStore``.

Run with: ``uv run uvicorn api:app --reload``
"""

from __future__ import annotations

import os
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from expenses import ExpenseStore

STATIC_DIR = Path(__file__).parent / "static"
DEFAULT_FILE = Path(os.environ.get("EXPENSES_DATA_FILE", "expenses.json"))


class ExpenseIn(BaseModel):
    """Request body for recording an expense. ``amount`` is in dollars, e.g. ``12.50``."""

    model_config = ConfigDict(str_strip_whitespace=True)

    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    category: str = Field(min_length=1, max_length=50)
    note: str = Field(default="", max_length=200)


class ExpenseOut(BaseModel):
    """An expense as returned by the API. Amounts are integer cents."""

    expense_id: int
    amount_cents: int
    category: str
    note: str
    spent_on: str


class CategoryTotal(BaseModel):
    """Total spent in one category, in cents."""

    category: str
    total_cents: int


def create_app(path: Path = DEFAULT_FILE) -> FastAPI:
    """Build the app. ``path`` is the JSON file that stores the expenses."""
    app = FastAPI(title="Expense Tracker")
    store = ExpenseStore(path)

    @app.get("/api/expenses")
    def list_expenses() -> list[ExpenseOut]:
        return [ExpenseOut(**asdict(expense)) for expense in store.list_expenses()]

    @app.post("/api/expenses", status_code=201)
    def add_expense(body: ExpenseIn) -> ExpenseOut:
        expense = store.add(int(body.amount * 100), body.category, body.note)
        return ExpenseOut(**asdict(expense))

    @app.get("/api/summary")
    def summary() -> list[CategoryTotal]:
        totals = store.total_by_category()
        return [CategoryTotal(category=name, total_cents=totals[name]) for name in sorted(totals)]

    @app.get("/", include_in_schema=False)
    def home() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    return app


app = create_app()
