from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import create_app


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(tmp_path / "expenses.json"))


def test_list_and_summary_start_empty(client: TestClient) -> None:
    assert client.get("/api/expenses").json() == []
    assert client.get("/api/summary").json() == []


def test_add_converts_amount_to_cents_and_normalizes_category(client: TestClient) -> None:
    response = client.post(
        "/api/expenses", json={"amount": "12.50", "category": "  Food ", "note": " lunch "}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["expense_id"] == 1
    assert (body["amount_cents"], body["category"], body["note"]) == (1250, "food", "lunch")
    assert client.get("/api/expenses").json() == [body]


def test_add_accepts_a_json_number_and_defaults_the_note(client: TestClient) -> None:
    response = client.post("/api/expenses", json={"amount": 3, "category": "travel"})
    assert response.status_code == 201
    assert response.json()["amount_cents"] == 300
    assert response.json()["note"] == ""


@pytest.mark.parametrize("amount", ["0", "-5", "1.999", "abc", ""])
def test_add_rejects_invalid_amounts(client: TestClient, amount: str) -> None:
    response = client.post("/api/expenses", json={"amount": amount, "category": "food"})
    assert response.status_code == 422


@pytest.mark.parametrize("payload", [{"amount": "5"}, {"amount": "5", "category": "  "}])
def test_add_rejects_missing_or_blank_category(client: TestClient, payload: dict) -> None:
    assert client.post("/api/expenses", json=payload).status_code == 422


def test_summary_totals_per_category_sorted(client: TestClient) -> None:
    for amount, category in [("5.00", "food"), ("2.50", "food"), ("9.00", "travel")]:
        client.post("/api/expenses", json={"amount": amount, "category": category})
    assert client.get("/api/summary").json() == [
        {"category": "food", "total_cents": 750},
        {"category": "travel", "total_cents": 900},
    ]


def test_home_page_is_served(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Expense" in response.text
