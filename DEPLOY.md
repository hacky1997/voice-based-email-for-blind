# Deployment Guide

## Quick Reference

| Target | HTTPS | Voice on Mobile | Effort |
|---|---|---|---|
| Localhost (dev) | No | ✅ (localhost is exempt) | `make run` |
| LAN (phone on same Wi-Fi) | No | ⚠️ (use Chrome, accept warning) | `make run-lan` |
| Docker + Caddy (LAN/server) | ✅ Auto | ✅ | `make docker-https` |
| Railway (free cloud) | ✅ Auto | ✅ | 5 min |
| Fly.io (free cloud) | ✅ Auto | ✅ | 10 min |

> **Why HTTPS matters for mobile:** The Web Speech API (voice input) requires a secure context on mobile browsers. Localhost is always allowed; everything else needs HTTPS.

---

## 1. Local Development

```bash
make install    # first time only
make run        # http://localhost:5000
```

---

## 2. LAN Access (Test on Your Phone)

Both devices must be on the same Wi-Fi network.

```bash
make run-lan
```

The Makefile will print your local IP. Open `http://<ip>:5000` on your phone.

**Voice input on Chrome Android:** Works on `http://` for local IP in Chrome — Chrome exempts local network addresses. On Safari iOS, you'll need HTTPS (see option 3 or 4).

---

## 3. Docker + Caddy (Self-hosted HTTPS)

Best for a home server or a VPS where you want HTTPS on your phone permanently.

### With a real domain:
1. Point your domain's DNS A record to your server IP
2. Edit `Caddyfile`: replace `:80` with `yourdomain.com`
3. Run:
```bash
make docker-https
```
Caddy automatically fetches a Let's Encrypt certificate.

### With just a LAN IP (self-signed):
Edit `Caddyfile`:
```
192.168.1.10 {      # your LAN IP
    tls internal    # self-signed cert
    reverse_proxy app:8000
}
```
Then `make docker-https`. On your phone, visit `https://192.168.1.10` and accept the cert warning once.

---

## 4. Railway (Free Cloud — Easiest)

Railway gives you a free HTTPS URL in under 5 minutes.

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy:
```bash
railway init
railway up
```
4. Set environment variables in the Railway dashboard (same as your `.env`)
5. Update `GOOGLE_REDIRECT_URI` in your Google Cloud Console to the Railway URL

Your app will be live at `https://<project>.up.railway.app`.

---

## 5. Fly.io (Free Cloud — More Control)

```bash
# Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
fly auth login
fly launch          # detects Dockerfile automatically
fly secrets set SECRET_KEY=your-secret-key
fly secrets set GOOGLE_CLIENT_ID=your-client-id
fly secrets set GOOGLE_CLIENT_SECRET=your-client-secret
fly deploy
```

Your app will be live at `https://<app-name>.fly.dev`.

---

## Environment Variables (All Platforms)

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Random secret for Flask sessions. Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `GOOGLE_CLIENT_ID` | Gmail only | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Gmail only | From Google Cloud Console |
| `GOOGLE_REDIRECT_URI` | Gmail only | Must match your deployment URL exactly |
| `CONTACTS_FILE` | No | Path for contacts JSON (default: `contacts.json`) |

---

## Generating a SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Never use the default or a short key in production.
