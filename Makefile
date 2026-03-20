.PHONY: help install run run-lan run-debug test test-cov lint docker docker-https clean

# ── Config ────────────────────────────────────────────────────────────────────
PYTHON   := python3
VENV     := venv
PIP      := $(VENV)/bin/pip
PYTEST   := $(VENV)/bin/pytest
FLASK    := $(VENV)/bin/python app.py

# Detect OS for open command
UNAME := $(shell uname -s)
ifeq ($(UNAME),Darwin)
  OPEN := open
else ifeq ($(UNAME),Linux)
  OPEN := xdg-open
else
  OPEN := start
endif

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Voice Email — Developer Commands"
	@echo "  ─────────────────────────────────────────────"
	@echo "  make install      Create venv & install deps"
	@echo "  make run          Start server (localhost only)"
	@echo "  make run-lan      Start server on LAN (for mobile)"
	@echo "  make run-debug    Start with Flask debugger"
	@echo "  make test         Run all tests"
	@echo "  make test-cov     Run tests + coverage report"
	@echo "  make lint         Run flake8 linter"
	@echo "  make docker       Build & run with Docker"
	@echo "  make docker-https Docker + Caddy HTTPS (mobile ready)"
	@echo "  make clean        Remove venv, cache, temp files"
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt -r requirements-prod.txt
	$(PIP) install pytest pytest-cov flake8
	@[ -f .env ] || cp .env.example .env
	@echo ""
	@echo "  ✅  Setup complete. Edit .env with your credentials, then: make run"
	@echo ""

# ── Dev servers ───────────────────────────────────────────────────────────────
run:
	$(FLASK) --host 127.0.0.1 --port 5000

run-lan:
	@echo "  📱  Opening on LAN — find your IP and visit it on your phone"
	@ip route get 1.1.1.1 2>/dev/null | awk '{print "  → http://"$$7":5000"}' || \
	  ipconfig 2>/dev/null | grep "IPv4" | head -1 | awk '{print "  → http://"$$NF":5000"}'
	$(FLASK) --host 0.0.0.0 --port 5000

run-debug:
	$(FLASK) --host 127.0.0.1 --port 5000 --debug

# ── Tests ─────────────────────────────────────────────────────────────────────
test:
	$(PYTEST)

test-cov:
	$(PYTEST) --cov=. --cov-report=term-missing --cov-report=html
	@echo "  Coverage report: htmlcov/index.html"

# ── Lint ──────────────────────────────────────────────────────────────────────
lint:
	$(VENV)/bin/flake8 . --exclude=$(VENV),htmlcov --max-line-length=100 \
	  --ignore=E501,W503

# ── Docker ────────────────────────────────────────────────────────────────────
docker:
	@[ -f .env ] || (echo "  ⚠  Copy .env.example to .env first"; exit 1)
	docker compose up --build

docker-https:
	@[ -f .env ] || (echo "  ⚠  Copy .env.example to .env first"; exit 1)
	docker compose --profile https up --build

docker-stop:
	docker compose down

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	@echo "  🧹  Cleaned"
