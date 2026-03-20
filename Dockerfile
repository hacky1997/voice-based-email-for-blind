# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-prod.txt

# Copy source
COPY . .

# ── Runtime ───────────────────────────────────────────────────────────────────
FROM base AS runtime

# Non-root user for security
RUN useradd -m -u 1000 voicemail
USER voicemail

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Use gunicorn in production (installed via requirements-prod.txt)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 60 --access-logfile -"]
