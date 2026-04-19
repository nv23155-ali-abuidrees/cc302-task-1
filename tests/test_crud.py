import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from appp import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client

def test_create_task(client):
    # CREATE
    resp = client.post("/add", data={"content": "Buy milk"}, follow_redirects=True)
    assert resp.status_code == 200

    # READ/VERIFY
    assert "Buy milk" in resp.get_data(as_text=True)


def test_search_task(client):
    client.post("/add", data={"content": "Buy milk"}, follow_redirects=True)
    client.post("/add", data={"content": "Call Alice"}, follow_redirects=True)

    resp = client.get("/?q=milk")
    assert resp.status_code == 200
    assert "Buy milk" in resp.get_data(as_text=True)
    assert "Call Alice" not in resp.get_data(as_text=True)


def test_filter_completed_tasks(client):
    client.post("/add", data={"content": "Buy milk"}, follow_redirects=True)
    client.post("/add", data={"content": "Call Alice"}, follow_redirects=True)
    client.get("/complete/1", follow_redirects=True)

    resp = client.get("/?status=completed")
    assert resp.status_code == 200
    assert "Buy milk" in resp.get_data(as_text=True)
    assert "Call Alice" not in resp.get_data(as_text=True)


def test_update_task(client):
    # CREATE first
    client.post("/add", data={"content": "Old title"}, follow_redirects=True)

    # UPDATE
    resp = client.post("/edit/1", data={"content": "New title"}, follow_redirects=True)
    assert resp.status_code == 200

    # READ/VERIFY
    assert "New title" in resp.get_data(as_text=True)
    assert "Old title" not in resp.get_data(as_text=True)

def test_delete_task(client):
    # CREATE first
    client.post("/add", data={"content": "To be deleted"}, follow_redirects=True)

    # DELETE
    resp = client.get("/delete/1", follow_redirects=True)
    assert resp.status_code == 200

    # READ/VERIFY
    assert "To be deleted" not in resp.get_data(as_text=True)