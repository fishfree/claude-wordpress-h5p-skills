# Canva Design Generator

> **Phase 3** — Requires Canva Developer Account + OAuth2 Integration

## Overview

Create professional designs (social media posts, certificates, flyers, presentations) via the
Canva Connect API. Canva Education accounts are free for teachers and include full API access.

## Setup (one-time)

### 1. Canva Education Account
- Sign up at https://www.canva.com/education/ with school email
- Verify teacher status → unlocks Canva Pro features for free

### 2. Register Developer Integration
- Go to https://www.canva.dev/
- Create a new integration (private, for your team)
- Note the **Client ID** and **Client Secret**
- Set scopes: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`
- Set redirect URL: `http://localhost:3000/callback` (for local OAuth flow)

### 3. Store credentials
Add to `.env`:
```
CANVA_CLIENT_ID=your-client-id
CANVA_CLIENT_SECRET=your-client-secret
```

## Authentication (OAuth 2.0 + PKCE)

Canva uses OAuth 2.0 Authorization Code flow with PKCE. First-time setup requires a browser
redirect to get an access token.

### Initial Token Generation

```bash
# 1. Generate PKCE challenge
CODE_VERIFIER=$(python3 -c "import secrets,base64; v=secrets.token_urlsafe(64); print(v)")
CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -sha256 -binary | base64 -w0 | tr '+/' '-_' | tr -d '=')

# 2. Open browser for authorization (manual step)
echo "Open this URL in browser:"
echo "https://www.canva.com/api/oauth/authorize?code_challenge=${CODE_CHALLENGE}&code_challenge_method=S256&scope=design:content:write%20asset:write&response_type=code&client_id=${CANVA_CLIENT_ID}&redirect_uri=http://localhost:3000/callback"

# 3. After authorization, extract code from redirect URL and exchange:
AUTH_CODE="paste-code-here"
curl -s -X POST "https://api.canva.com/rest/v1/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=${AUTH_CODE}&redirect_uri=http://localhost:3000/callback&code_verifier=${CODE_VERIFIER}&client_id=${CANVA_CLIENT_ID}&client_secret=${CANVA_CLIENT_SECRET}"
```

Save the returned `access_token` and `refresh_token` to `_assets/media-factory/.canva-token.json`
(gitignored).

### Token Refresh

```bash
curl -s -X POST "https://api.canva.com/rest/v1/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=${REFRESH_TOKEN}&client_id=${CANVA_CLIENT_ID}&client_secret=${CANVA_CLIENT_SECRET}"
```

## Create Design

```bash
ACCESS_TOKEN=$(python3 -c "import json; print(json.load(open('_assets/media-factory/.canva-token.json'))['access_token'])")

curl -s -X POST "https://api.canva.com/rest/v1/designs" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "design_type": {"type": "preset", "name": "Instagram Post"},
    "title": "DESIGN_TITLE"
  }'
```

Design types: `Instagram Post`, `Presentation`, `A4 Document`, `Certificate`, `Facebook Post`, `Twitter Post`, `Poster`

## Fallback

If Canva is not configured or token expired:
- For social media graphics → fall back to Nano Banana AI image
- For certificates → fall back to Claude SVG generator
- For presentations → suggest HedgeDoc presentation skill instead

## Status

Not yet configured. Requires:
1. [ ] Canva Education account registration
2. [ ] Developer integration at canva.dev
3. [ ] OAuth token generation (one-time browser flow)
