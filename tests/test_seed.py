from pathlib import Path

from expenses import ExpenseStore
from seed import SAMPLE_EXPENSES, seed


def test_seed_fills_an_empty_list_with_ordered_ids(tmp_path: Path) -> None:
    path = tmp_path / "expenses.json"
    assert seed(path) == len(SAMPLE_EXPENSES)
    expenses = ExpenseStore(path).list_expenses()
    assert [e.expense_id for e in expenses] == list(range(1, len(SAMPLE_EXPENSES) + 1))
    assert len({e.spent_on for e in expenses}) > 1  # dates are spread out, not all today


def test_seed_never_overwrites_existing_expenses(tmp_path: Path) -> None:
    path = tmp_path / "expenses.json"
    ExpenseStore(path).add(500, "food", "mine")
    assert seed(path) == 0
    assert [e.note for e in ExpenseStore(path).list_expenses()] == ["mine"]
