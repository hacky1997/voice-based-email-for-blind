"""
Flask API integration tests using mocked email backends.
No real email account needed — all connections are mocked.
"""
import json
import pytest
from unittest.mock import MagicMock, patch

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app


@pytest.fixture
def client(tmp_path):
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret"
    # Use a temp contacts file for each test
    import app as app_module
    app_module._contact_book.__init__(str(tmp_path / "contacts.json"))
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def authed_client(client):
    """Client with a pre-seeded IMAP session."""
    import app as app_module
    mock_conn = MagicMock()
    mock_conn.get_imap.return_value = MagicMock()

    with flask_app.test_request_context():
        from flask import session
        pass

    with client.session_transaction() as sess:
        sess["sid"] = "test-session-id"

    app_module._connections["test-session-id"] = {
        "type": "imap",
        "conn": mock_conn,
        "email": "test@example.com",
    }
    yield client
    app_module._connections.pop("test-session-id", None)


# ── Auth status ───────────────────────────────────────────────────────────────

def test_auth_status_unauthenticated(client):
    res = client.get("/api/auth/status")
    data = json.loads(res.data)
    assert data["ok"] is True
    assert data["data"]["authenticated"] is False


def test_auth_status_authenticated(authed_client):
    res = authed_client.get("/api/auth/status")
    data = json.loads(res.data)
    assert data["data"]["authenticated"] is True
    assert data["data"]["email"] == "test@example.com"


# ── IMAP Login ────────────────────────────────────────────────────────────────

def test_imap_login_missing_fields(client):
    res = client.post("/api/auth/imap",
        data=json.dumps({"provider": "yahoo"}),
        content_type="application/json")
    data = json.loads(res.data)
    assert data["ok"] is False
    assert res.status_code == 400


@patch("app.imap_auth.validate_credentials", return_value=(True, ""))
@patch("app.imap_auth.IMAPConnection")
def test_imap_login_success(mock_conn_cls, mock_validate, client):
    mock_conn_cls.return_value = MagicMock()
    res = client.post("/api/auth/imap",
        data=json.dumps({
            "provider": "yahoo",
            "email": "user@yahoo.com",
            "password": "app-password-here"
        }),
        content_type="application/json")
    data = json.loads(res.data)
    assert data["ok"] is True
    assert data["data"]["email"] == "user@yahoo.com"


@patch("app.imap_auth.validate_credentials", return_value=(False, "Authentication failed"))
def test_imap_login_bad_credentials(mock_validate, client):
    res = client.post("/api/auth/imap",
        data=json.dumps({
            "provider": "yahoo",
            "email": "user@yahoo.com",
            "password": "wrong"
        }),
        content_type="application/json")
    assert res.status_code == 401


# ── Contacts CRUD ─────────────────────────────────────────────────────────────

def test_contacts_empty(client):
    res = client.get("/api/contacts")
    data = json.loads(res.data)
    assert data["ok"] is True
    assert data["data"] == []


def test_add_contact(client):
    res = client.post("/api/contacts",
        data=json.dumps({"name": "Alice", "email": "alice@example.com"}),
        content_type="application/json")
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["data"]["name"] == "Alice"


def test_add_contact_missing_fields(client):
    res = client.post("/api/contacts",
        data=json.dumps({"name": "Alice"}),
        content_type="application/json")
    assert res.status_code == 400


def test_search_contacts(client):
    client.post("/api/contacts",
        data=json.dumps({"name": "Alice", "email": "alice@test.com"}),
        content_type="application/json")
    res = client.get("/api/contacts?q=alice")
    data = json.loads(res.data)
    assert len(data["data"]) == 1


def test_delete_contact(client):
    add_res = client.post("/api/contacts",
        data=json.dumps({"name": "Alice", "email": "alice@test.com"}),
        content_type="application/json")
    contact_id = json.loads(add_res.data)["data"]["id"]
    del_res = client.delete(f"/api/contacts/{contact_id}")
    assert json.loads(del_res.data)["ok"] is True
    assert client.get("/api/contacts").json["data"] == []


def test_delete_nonexistent_contact(client):
    res = client.delete("/api/contacts/does-not-exist")
    assert res.status_code == 404


# ── Email endpoints require auth ──────────────────────────────────────────────

def test_emails_require_auth(client):
    res = client.get("/api/emails")
    assert res.status_code == 401


def test_send_email_requires_auth(client):
    res = client.post("/api/emails",
        data=json.dumps({"to": "x@x.com", "body": "hi"}),
        content_type="application/json")
    assert res.status_code == 401


# ── Email list (mocked IMAP) ──────────────────────────────────────────────────

@patch("app.reader.imap_list_inbox")
def test_list_emails(mock_list, authed_client):
    mock_list.return_value = {
        "emails": [
            {"id": "1", "from": "Bob <bob@test.com>", "subject": "Hello",
             "date": "Mon, 1 Jan 2024", "unread": True, "snippet": ""}
        ],
        "next_page_token": None
    }
    res = authed_client.get("/api/emails")
    data = json.loads(res.data)
    assert data["ok"] is True
    assert len(data["data"]["emails"]) == 1
    assert data["data"]["emails"][0]["subject"] == "Hello"


@patch("app.reader.imap_get_email")
def test_get_single_email(mock_get, authed_client):
    mock_get.return_value = {
        "id": "42", "from": "Bob <b@b.com>", "to": "me@me.com",
        "subject": "Hi", "date": "now", "body": "Hello there", "unread": True
    }
    res = authed_client.get("/api/emails/42")
    data = json.loads(res.data)
    assert data["data"]["body"] == "Hello there"


@patch("app.sender.smtp_send")
def test_send_email(mock_send, authed_client):
    res = authed_client.post("/api/emails",
        data=json.dumps({"to": "bob@example.com", "subject": "Hey", "body": "Hello Bob"}),
        content_type="application/json")
    assert json.loads(res.data)["ok"] is True
    mock_send.assert_called_once()


def test_send_email_missing_to(authed_client):
    res = authed_client.post("/api/emails",
        data=json.dumps({"body": "Hello"}),
        content_type="application/json")
    assert res.status_code == 400


@patch("app.reader.imap_delete")
def test_delete_email(mock_del, authed_client):
    res = authed_client.delete("/api/emails/42")
    assert json.loads(res.data)["ok"] is True
    mock_del.assert_called_once()


@patch("app.reader.imap_mark_read")
def test_mark_read(mock_mark, authed_client):
    res = authed_client.patch("/api/emails/42/read")
    assert json.loads(res.data)["ok"] is True
    mock_mark.assert_called_once()


# ── Logout ────────────────────────────────────────────────────────────────────

def test_logout(authed_client):
    res = authed_client.post("/api/auth/logout")
    assert json.loads(res.data)["ok"] is True
    # Should be unauthenticated after logout
    status = authed_client.get("/api/auth/status")
    assert json.loads(status.data)["data"]["authenticated"] is False
