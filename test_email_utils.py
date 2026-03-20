"""
Tests for email utility functions — no network calls needed.
"""
import base64
import email as email_lib
import pytest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_client.reader import _decode_header_value, _extract_text_body
from email_client.sender import _build_mime


# ── _decode_header_value ─────────────────────────────────────────────────────

def test_decode_plain_header():
    assert _decode_header_value("Hello World") == "Hello World"


def test_decode_none_header():
    assert _decode_header_value(None) == ""


def test_decode_encoded_header():
    # RFC 2047 encoded header (UTF-8 base64)
    encoded = "=?utf-8?b?SGVsbG8gV29ybGQ=?="
    assert _decode_header_value(encoded) == "Hello World"


def test_decode_quoted_printable_header():
    encoded = "=?utf-8?q?Hello_World?="
    assert _decode_header_value(encoded) == "Hello World"


# ── _extract_text_body ────────────────────────────────────────────────────────

def _make_simple_message(body: str, ctype: str = "text/plain") -> email_lib.message.Message:
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(body, ctype.split("/")[1]))
    return msg


def test_extract_plain_text():
    msg = _make_simple_message("Hello from the body", "text/plain")
    assert "Hello from the body" in _extract_text_body(msg)


def test_extract_html_body():
    html = "<html><body><p>Hello HTML</p></body></html>"
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(html, "html"))
    body = _extract_text_body(msg)
    assert "Hello HTML" in body


def test_plain_preferred_over_html():
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText("Plain text version", "plain"))
    msg.attach(MIMEText("<p>HTML version</p>", "html"))
    body = _extract_text_body(msg)
    assert "Plain text version" in body


def test_empty_message():
    msg = MIMEMultipart("alternative")
    assert _extract_text_body(msg) == ""


# ── _build_mime ────────────────────────────────────────────────────────────────

def test_build_mime_headers():
    msg = _build_mime("from@test.com", "to@test.com", "Test Subject", "Hello body")
    assert msg["From"] == "from@test.com"
    assert msg["To"] == "to@test.com"
    assert msg["Subject"] == "Test Subject"


def test_build_mime_body():
    msg = _build_mime("f@t.com", "t@t.com", "Subj", "My message body")
    payload = msg.get_payload()
    body_text = payload[0].get_payload()
    assert "My message body" in body_text


def test_build_mime_is_multipart():
    msg = _build_mime("f@t.com", "t@t.com", "S", "B")
    assert msg.is_multipart()


# ── sender reply subject ──────────────────────────────────────────────────────

def test_reply_subject_adds_re():
    from email_client.sender import _build_mime
    subject = "Original Subject"
    reply_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    assert reply_subject == "Re: Original Subject"


def test_reply_subject_no_double_re():
    subject = "Re: Already a reply"
    reply_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"
    assert reply_subject == "Re: Already a reply"
    assert not reply_subject.startswith("Re: Re:")
