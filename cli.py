"""Command line interface: python cli.py add|list|done."""

from __future__ import annotations

import argparse
from pathlib import Path

from todo import TodoStore

DEFAULT_FILE = Path("todos.json")


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="show all tasks")
    add = sub.add_parser("add", help="add a task")
    add.add_argument("title")
    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("task_id", type=int)
    return parser


def main(argv: list[str] | None = None, path: Path = DEFAULT_FILE) -> int:
    """Run the CLI and return a process exit code."""
    args = build_parser().parse_args(argv)
    store = TodoStore(path)
    if args.command == "add":
        task = store.add(args.title)
        print(f"added #{task.task_id}: {task.title}")
    elif args.command == "done":
        try:
            task = store.complete(args.task_id)
        except KeyError as exc:
            print(exc.args[0])
            return 1
        print(f"completed #{task.task_id}: {task.title}")
    else:
        for task in store.list_tasks():
            mark = "x" if task.is_done else " "
            print(f"[{mark}] #{task.task_id} {task.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
