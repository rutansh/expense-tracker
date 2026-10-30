from pathlib import Path

import pytest

from cli import main
from todo import TodoStore


@pytest.fixture
def store(tmp_path: Path) -> TodoStore:
    return TodoStore(tmp_path / "todos.json")


def test_add_assigns_incrementing_ids(store: TodoStore) -> None:
    assert store.add("write docs").task_id == 1
    assert store.add("ship it").task_id == 2


def test_add_rejects_empty_title(store: TodoStore) -> None:
    with pytest.raises(ValueError):
        store.add("   ")


def test_complete_marks_task_done(store: TodoStore) -> None:
    task = store.add("write docs")
    store.complete(task.task_id)
    assert store.list_tasks()[0].is_done is True


def test_complete_unknown_id_raises(store: TodoStore) -> None:
    with pytest.raises(KeyError):
        store.complete(99)


def test_cli_add_and_list(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "todos.json"
    assert main(["add", "buy milk"], path=path) == 0
    assert main(["list"], path=path) == 0
    assert "[ ] #1 buy milk" in capsys.readouterr().out


def test_cli_done_unknown_id_fails(tmp_path: Path) -> None:
    assert main(["done", "5"], path=tmp_path / "todos.json") == 1
