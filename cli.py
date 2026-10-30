"""Command line interface: python cli.py add|list|summary."""

from __future__ import annotations

import argparse
from pathlib import Path

from expenses import ExpenseStore, parse_amount

DEFAULT_FILE = Path("expenses.json")


def format_money(cents: int) -> str:
    """Format integer cents as a dollar string."""
    return f"${cents / 100:,.2f}"


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(prog="expenses")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount", help="for example 12.50")
    add.add_argument("category")
    add.add_argument("--note", default="")
    sub.add_parser("list", help="show all expenses")
    sub.add_parser("summary", help="show totals per category")
    return parser


def main(argv: list[str] | None = None, path: Path = DEFAULT_FILE) -> int:
    """Run the CLI and return a process exit code."""
    args = build_parser().parse_args(argv)
    store = ExpenseStore(path)
    if args.command == "add":
        try:
            expense = store.add(parse_amount(args.amount), args.category, args.note)
        except ValueError as exc:
            print(exc)
            return 1
        print(
            f"added #{expense.expense_id}: {format_money(expense.amount_cents)} {expense.category}"
        )
    elif args.command == "summary":
        for category, total in sorted(store.total_by_category().items()):
            print(f"{category}: {format_money(total)}")
    else:
        for e in store.list_expenses():
            print(
                f"#{e.expense_id} {e.spent_on} {format_money(e.amount_cents)} {e.category} {e.note}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
