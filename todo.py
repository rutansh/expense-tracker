"""Tiny todo store backed by a JSON file."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Task:
    """A single todo item."""

    task_id: int
    title: str
    is_done: bool = False


class TodoStore:
    """Persist tasks in a JSON file."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def add(self, title: str) -> Task:
        """Add a new task and return it."""
        if not title.strip():
            raise ValueError("title must not be empty")
        tasks = self.list_tasks()
        task = Task(task_id=max((t.task_id for t in tasks), default=0) + 1, title=title.strip())
        self._save([*tasks, task])
        return task

    def list_tasks(self) -> list[Task]:
        """Return all tasks in creation order."""
        if not self._path.exists():
            return []
        return [Task(**item) for item in json.loads(self._path.read_text())]

    def complete(self, task_id: int) -> Task:
        """Mark a task as done. Raises KeyError if it does not exist."""
        tasks = self.list_tasks()
        for task in tasks:
            if task.task_id == task_id:
                task.is_done = True
                self._save(tasks)
                return task
        raise KeyError(f"no task with id {task_id}")

    def _save(self, tasks: list[Task]) -> None:
        self._path.write_text(json.dumps([asdict(t) for t in tasks], indent=2))
