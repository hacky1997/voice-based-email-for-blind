"""
Tests for ContactBook — no external services needed.
"""
import os
import tempfile
import pytest
from email_client.contacts import ContactBook


@pytest.fixture
def book(tmp_path):
    return ContactBook(str(tmp_path / "contacts.json"))


def test_empty_on_init(book):
    assert book.list_all() == []


def test_add_contact(book):
    c = book.add("Alice Smith", "alice@example.com")
    assert c["name"] == "Alice Smith"
    assert c["email"] == "alice@example.com"
    assert "id" in c


def test_list_contacts(book):
    book.add("Alice", "alice@example.com")
    book.add("Bob", "bob@example.com")
    contacts = book.list_all()
    assert len(contacts) == 2


def test_search_by_name(book):
    book.add("Alice Smith", "alice@example.com")
    book.add("Bob Jones", "bob@example.com")
    results = book.search("alice")
    assert len(results) == 1
    assert results[0]["name"] == "Alice Smith"


def test_search_by_email(book):
    book.add("Alice", "alice@company.com")
    book.add("Bob", "bob@other.com")
    results = book.search("company")
    assert len(results) == 1


def test_search_case_insensitive(book):
    book.add("Alice", "alice@example.com")
    assert len(book.search("ALICE")) == 1


def test_delete_contact(book):
    c = book.add("Alice", "alice@example.com")
    assert book.delete(c["id"]) is True
    assert book.list_all() == []


def test_delete_nonexistent(book):
    assert book.delete("does-not-exist") is False


def test_update_contact(book):
    c = book.add("Alice", "alice@example.com")
    updated = book.update(c["id"], name="Alice Updated", email="new@example.com")
    assert updated["name"] == "Alice Updated"
    assert updated["email"] == "new@example.com"


def test_update_preserves_id(book):
    c = book.add("Alice", "alice@example.com")
    updated = book.update(c["id"], name="Alice Updated")
    assert updated["id"] == c["id"]


def test_get_by_id(book):
    c = book.add("Alice", "alice@example.com")
    fetched = book.get(c["id"])
    assert fetched["email"] == "alice@example.com"


def test_get_nonexistent(book):
    assert book.get("bad-id") is None


def test_persistence(tmp_path):
    """Data survives re-instantiation (file-based persistence)."""
    path = str(tmp_path / "contacts.json")
    book1 = ContactBook(path)
    book1.add("Alice", "alice@example.com")

    book2 = ContactBook(path)
    assert len(book2.list_all()) == 1
    assert book2.list_all()[0]["name"] == "Alice"
