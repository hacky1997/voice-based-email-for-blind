#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  release.sh — Push voice-email v2.0.0 and create a GitHub Release
#
#  Requirements:
#    - git
#    - GitHub CLI (gh): https://cli.github.com  → brew install gh  OR
#                                                  winget install GitHub.cli
#
#  Usage:
#    chmod +x release.sh
#    ./release.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e  # exit on any error

REPO="hacky1997/voice-based-email-for-blind"
TAG="v2.0.0"
TITLE="v2.0.0 — Complete Rewrite: PWA + OAuth2 + Multi-provider IMAP"

# ── 1. Sanity checks ──────────────────────────────────────────────────────────
echo "🔍 Checking dependencies..."

if ! command -v git &>/dev/null; then
  echo "❌ git not found. Install git first."; exit 1
fi

if ! command -v gh &>/dev/null; then
  echo "❌ GitHub CLI (gh) not found."
  echo "   Install: https://cli.github.com"
  echo ""
  echo "   macOS:   brew install gh"
  echo "   Windows: winget install GitHub.cli"
  echo "   Linux:   https://github.com/cli/cli/releases"
  exit 1
fi

# Check gh auth
if ! gh auth status &>/dev/null; then
  echo "🔑 Not logged in to GitHub CLI. Running: gh auth login"
  gh auth login
fi

echo "✅ All checks passed."
echo ""

# ── 2. Stage & commit ─────────────────────────────────────────────────────────
echo "📦 Staging all files..."
git add -A

# Only commit if there are staged changes
if git diff --cached --quiet; then
  echo "   (nothing new to commit — files already staged)"
else
  git commit -m "feat: v2.0.0 complete rewrite

- Replace broken SMTP auth with Gmail OAuth2 + App Passwords
- Add PWA (installable on any phone via browser)
- Modular Flask backend with proper REST API
- Full IMAP support: Gmail, Yahoo, generic providers
- New features: reply, delete, mark as read, contact book
- Voice commands via Web Speech API (no server-side audio)
- Docker + Caddy for automatic HTTPS (required for mobile voice)
- 45 tests across API, contacts, and email utilities
- CircleCI pipeline: lint → test → Docker smoke test
- Makefile for developer convenience
- DEPLOY.md covering Railway, Fly.io, local, LAN, Docker"
fi

# ── 3. Tag ────────────────────────────────────────────────────────────────────
echo ""
echo "🏷  Creating tag $TAG..."

# Delete tag locally and remotely if it already exists (safe re-run)
git tag -d "$TAG" 2>/dev/null || true
git push origin ":refs/tags/$TAG" 2>/dev/null || true

git tag -a "$TAG" -m "Release $TAG"

# ── 4. Push ───────────────────────────────────────────────────────────────────
echo ""
echo "🚀 Pushing to GitHub..."
git push origin main
git push origin "$TAG"

# ── 5. Create GitHub Release ──────────────────────────────────────────────────
echo ""
echo "📝 Creating GitHub Release $TAG..."

gh release create "$TAG" \
  --repo "$REPO" \
  --title "$TITLE" \
  --notes "## What's New in v2.0.0

This is a **complete rewrite** of the original 2019 voice email project.

### 🔐 Authentication
- **Gmail** — Proper OAuth2 via Google API (no password ever stored)
- **Yahoo Mail** — App Password support over IMAP/SMTP
- **Any IMAP provider** — Generic IMAP/SMTP with configurable host/port

### 📱 Progressive Web App (Mobile)
- Installable on **any phone** via browser (no app store)
- Works on Android (Chrome) and iOS (Safari)
- Voice input via **Web Speech API** — no server-side audio files
- Offline shell caching via Service Worker
- Dark, accessible UI optimised for touch

### ✉️ Email Features
- Send email by voice or keyboard
- Read inbox with sender, subject, and body
- **Read email aloud** using text-to-speech
- **Reply** to emails by voice
- **Delete** emails (moves to trash)
- **Mark as read**
- **Contact book** with voice-search autocomplete

### 🏗 Architecture
- Modular Flask REST API backend
- Separate \`auth/\`, \`email_client/\` packages
- Environment-based config via \`.env\` (no hardcoded credentials)
- Docker + Caddy for automatic HTTPS
- Deployable to Railway or Fly.io in ~5 minutes

### 🧪 Tests
- 45 tests across API routes, contact CRUD, and email utilities
- Fully mocked — no real email account needed to run tests
- \`make test\` or \`make test-cov\` for coverage report

### ⚙️ CI/CD
- CircleCI pipeline: **lint → test → Docker smoke test**
- Docker image built and validated on every \`main\` push

---

### Quick Start
\`\`\`bash
git clone https://github.com/hacky1997/voice-based-email-for-blind.git
cd voice-based-email-for-blind
make install   # creates venv, installs deps, copies .env.example
# edit .env with your credentials
make run       # http://localhost:5000
\`\`\`

See [DEPLOY.md](DEPLOY.md) for mobile HTTPS setup, Docker, Railway, and Fly.io.

---

### Breaking Changes from v1
- Google removed \"Less Secure Apps\" support in 2024 — the old SMTP auth no longer works. Use OAuth2 (Gmail) or an App Password (Yahoo/others).
- \`pyglet\` and temp MP3 files replaced by the browser's built-in speech engine.
- Credentials must be in \`.env\` — never in source code." \
  --latest

echo ""
echo "✅ Done! Release published:"
echo "   https://github.com/$REPO/releases/tag/$TAG"
