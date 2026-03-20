# 🎙 Voice Email

> A voice-controlled email client for everyone — accessible, modern, and runs on any device.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PWA](https://img.shields.io/badge/PWA-Installable-5A0FC8?logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What's New in v2

| Feature | v1 (2019) | v2 (Now) |
|---|---|---|
| Auth | Plain password in source code ❌ | OAuth2 (Gmail) + App Passwords ✅ |
| Audio | pyglet + temp MP3 files | Web Speech API (no files) ✅ |
| Email API | Gmail SMTP (broken since 2024) | Gmail REST API + generic IMAP ✅ |
| Mobile | None | Full PWA — install on any phone ✅ |
| Features | Send, read | Send, read, reply, delete, mark as read, contact book ✅ |
| Structure | Single flat script | Modular packages + REST API ✅ |

---

## Features

- **Send email** by voice or keyboard
- **Read inbox** aloud with text-to-speech
- **Reply** to emails by voice
- **Delete / Mark as read** any email
- **Contact book** with voice-search autocomplete
- **Works on any phone** — installable PWA (no app store needed)
- **Providers:** Gmail (OAuth2), Yahoo Mail, any IMAP/SMTP server

---

## Architecture

```
Flask Backend (Python)          PWA Frontend (Browser)
      │                                │
      ├── auth/gmail_oauth.py          ├── Web Speech API (STT)
      ├── auth/imap_auth.py            ├── SpeechSynthesis (TTS)
      ├── email_client/reader.py       ├── Service Worker (offline)
      ├── email_client/sender.py       └── Installable manifest
      ├── email_client/contacts.py
      └── app.py (REST API + serve PWA)
```

---

## Setup

### 1. Clone & Install

```bash
git clone https://github.com/hacky1997/voice-based-email-for-blind.git
cd voice-based-email-for-blind
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure `.env`

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Provider-specific setup

<details>
<summary><strong>Gmail (OAuth2)</strong></summary>

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **Gmail API**
3. Create **OAuth 2.0 credentials** (Web Application)
4. Add `http://localhost:5000/api/auth/gmail/callback` as a redirect URI
5. Copy Client ID and Secret into `.env`

</details>

<details>
<summary><strong>Yahoo Mail</strong></summary>

1. Go to [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Generate an **App Password**
3. Use that (not your main password) when signing in

</details>

<details>
<summary><strong>Generic IMAP</strong></summary>

Enter your IMAP/SMTP host and port in the "Advanced" section of the login screen.
Make sure IMAP is enabled in your email provider's settings.

</details>

### 4. Run

```bash
# Desktop only
python app.py

# LAN access (required for mobile PWA)
python app.py --host 0.0.0.0
```

Then open `http://localhost:5000` in your browser.

---

## Mobile / Phone Access

Since this is a **Progressive Web App (PWA)**:

1. Start the server with `--host 0.0.0.0`
2. Find your computer's local IP: `ip addr` (Linux) / `ipconfig` (Windows)
3. Open `http://<your-local-ip>:5000` in Chrome or Safari on your phone
4. Tap **"Add to Home Screen"** to install it like an app

> **Note:** Web Speech API requires HTTPS on mobile (except localhost).
> For production deployment, use a service like [Railway](https://railway.app) or
> [Fly.io](https://fly.io) which provide free HTTPS.

---

## Voice Commands

| Say… | Action |
|---|---|
| "Open inbox" | Load your inbox |
| "Read email" | Open the latest email |
| "Read aloud" | Speak the open email |
| "Next email" | Navigate to next |
| "Reply" | Reply to open email |
| "Delete" | Trash open email |
| "Mark as read" | Mark open email read |
| "Compose email" | Open compose screen |
| "Contacts" | Open contact book |
| "Sign out" | Disconnect |

---

## Project Structure

```
voice-email/
├── app.py                  # Flask app, REST API, serves PWA
├── config.py               # Environment config
├── requirements.txt
├── .env.example
├── auth/
│   ├── gmail_oauth.py      # Gmail OAuth2 flow
│   └── imap_auth.py        # Generic IMAP/SMTP (Yahoo etc.)
├── email_client/
│   ├── reader.py           # List, fetch, delete, mark as read
│   ├── sender.py           # Send, reply
│   └── contacts.py         # JSON contact book
└── static/                 # PWA files (served by Flask)
    ├── index.html          # Full single-page app
    ├── manifest.json       # PWA manifest (installable)
    └── sw.js               # Service worker (offline)
```

---

## Contributing

Issues and PRs are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT © Sayak Naskar
