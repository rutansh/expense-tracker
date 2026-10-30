from pathlib import Path

import pytest

from cli import main
from expenses import ExpenseStore, parse_amount


@pytest.fixture
def store(tmp_path: Path) -> ExpenseStore:
    return ExpenseStore(tmp_path / "expenses.json")


def test_parse_amount_converts_to_cents() -> None:
    assert parse_amount("12.50") == 1250
    assert parse_amount("3") == 300


@pytest.mark.parametrize("bad", ["abc", "0", "-5", "1.999"])
def test_parse_amount_rejects_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        parse_amount(bad)


def test_add_assigns_incrementing_ids(store: ExpenseStore) -> None:
    assert store.add(500, "food").expense_id == 1
    assert store.add(900, "travel").expense_id == 2


def test_add_normalizes_category(store: ExpenseStore) -> None:
    assert store.add(500, "  Food ").category == "food"


def test_add_rejects_empty_category(store: ExpenseStore) -> None:
    with pytest.raises(ValueError):
        store.add(500, "  ")


def test_total_by_category(store: ExpenseStore) -> None:
    store.add(500, "food")
    store.add(250, "food")
    store.add(900, "travel")
    assert store.total_by_category() == {"food": 750, "travel": 900}


def test_cli_add_and_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "expenses.json"
    assert main(["add", "12.50", "food"], path=path) == 0
    assert main(["summary"], path=path) == 0
    assert "food: $12.50" in capsys.readouterr().out


def test_cli_add_invalid_amount_fails(tmp_path: Path) -> None:
    assert main(["add", "oops", "food"], path=tmp_path / "expenses.json") == 1
