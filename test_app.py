"""Tests for Task Tracker API."""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        import app as app_module
        app_module.tasks = []
        app_module.next_id = 1
        yield client


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Write tests"
    assert data["status"] == "pending"


def test_create_task_missing_title(client):
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 400


def test_get_single_task(client):
    client.post("/tasks", json={"title": "Test task"})
    response = client.get("/tasks/1")
    assert response.status_code == 200


def test_delete_task(client):
    client.post("/tasks", json={"title": "To delete"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
