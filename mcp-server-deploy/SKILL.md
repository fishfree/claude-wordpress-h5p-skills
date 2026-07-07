---
name: mcp-server-deploy
description: Deploy MCP servers from local development to production via Git and Docker. Handles code push, SSH deployment, container rebuild, and health verification.
license: MIT
---

# MCP Server Deployment Workflow

Complete workflow for deploying MCP servers from local development to the Hetzner production server.

## When to Use This Skill

Use this skill when:
- Deploying new or updated MCP server code to production
- Setting up a new MCP server from scratch
- Rolling back to a previous version
- Checking deployment status and health

## Prerequisites

### Local Environment
- Git repository: `C:\Users\mail\entwicklung\docker\`
- SSH key: `~/.ssh/hetzner_ssh_key`

### Server Environment
- **Host:** 95.217.163.192 (Hetzner)
- **User:** dirk
- **Base Path:** `/home/dirk/docker/`
- **Traefik:** Reverse proxy with auto-SSL (HTTP challenge)

## MCP Servers

| Server | Domain | Local Path | Deploy Type |
|--------|--------|------------|-------------|
| moodle-mcp | mcp-moodle.dirk-schulenburg.net | mcp-servers/moodle-mcp | **Submodule** (eigenes Git-Repo) |
| wp-mcp | mcp-wp.dirk-schulenburg.net | mcp-servers/wp-mcp | **Submodule** (eigenes Git-Repo) |
| imap-mcp | mcp-imap.dirk-schulenburg.net | (root compose) | Parent Repo |
| edugrow-mcp | mcp-edugrow.dirk-schulenburg.net | edugrow/infrastructure/ | Parent Repo |
| sharepoint-mcp | mcp-sharepoint.dirk-schulenburg.net | mcp-servers/sharepoint-mcp | Parent Repo |
| teams-mcp | mcp-teams.dirk-schulenburg.net | mcp-servers/teams-mcp | Parent Repo |
| ms365-admin-mcp | mcp-ms365.dirk-schulenburg.net | mcp-servers/ms365-admin-mcp | Parent Repo |
| voice-mcp | voice-mcp.dirk-schulenburg.net | (root compose) | Parent Repo |

## Deploy Patterns

### Pattern 1: Submodule-Server (moodle-mcp, wp-mcp)

**WICHTIG:** Submodules haben eigene Git-Repos. Zwei Commits noetig!

```bash
# 1. Im Submodule committen + pushen
cd C:\Users\mail\entwicklung\docker\mcp-servers\moodle-mcp
git add .
git commit -m "feat: add new tool"
git push origin master

# 2. Im Parent-Repo die Referenz aktualisieren
cd C:\Users\mail\entwicklung\docker
git add mcp-servers/moodle-mcp
git commit -m "chore: update moodle-mcp submodule"
git push

# 3. Auf Server deployen
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/mcp-servers/moodle-mcp
  git pull origin master
  docker compose up -d --build
'
```

### Pattern 2: Parent-Repo-Server (sharepoint, teams, ms365, imap)

```bash
# 1. Lokal committen + pushen
cd C:\Users\mail\entwicklung\docker
git add mcp-servers/sharepoint-mcp/
git commit -m "feat(sharepoint-mcp): add new tool"
git push

# 2. Auf Server deployen
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  git pull
  cd mcp-servers/sharepoint-mcp
  docker compose up -d --build
'
```

### Pattern 3: Root-Compose-Server (imap, voice)

```bash
# Compose-File liegt im Root, nicht im mcp-servers/ Ordner
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  git pull
  docker compose -f docker-compose-imap-mcp.yml up -d --build
'
```

### Pattern 4: SCP-Deploy (Website — KEIN Git-Repo auf Server!)

```bash
# WICHTIG: /home/dirk/docker/website/ ist KEIN Git-Repo
# Deploy-Reihenfolge KRITISCH: Erst SCP, DANN rebuild!

# 1. Dateien hochladen
scp -i ~/.ssh/hetzner_ssh_key -r ./website/* dirk@95.217.163.192:/home/dirk/docker/website/

# 2. Container rebuilden
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/website
  docker compose up -d --build
'
```

## Deploy Script

Das `deploy.sh` Script auf dem Server vereinfacht den Prozess:

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '/home/dirk/docker/deploy.sh {server-name}'
```

## Verification

### Health Check (nach Deploy)

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  echo "=== Container Status ==="
  docker ps -f name={container-name} --format "{{.Names}}: {{.Status}}"

  echo "=== Health Check ==="
  curl -sf https://mcp-{name}.dirk-schulenburg.net/health && echo " OK" || echo " FAIL"

  echo "=== Recent Logs ==="
  docker logs {container-name} --tail 20
'
```

### All MCP Health Checks

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  for svc in mcp-moodle mcp-wp mcp-edugrow mcp-imap mcp-sharepoint mcp-teams mcp-ms365; do
    status=$(curl -sf https://${svc}.dirk-schulenburg.net/health 2>/dev/null && echo "OK" || echo "FAIL")
    echo "  $svc: $status"
  done
'
```

## New MCP Server Setup

### Docker Compose Template

```yaml
services:
  {server-name}:
    build: .
    container_name: {server-name}
    restart: unless-stopped
    env_file: .env
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=proxy"
      - "traefik.http.routers.{server-name}.rule=Host(`mcp-{short}.dirk-schulenburg.net`)"
      - "traefik.http.routers.{server-name}.entrypoints=https"
      - "traefik.http.routers.{server-name}.tls=true"
      - "traefik.http.routers.{server-name}.tls.certresolver=letsencrypt"
      - "traefik.http.services.{server-name}.loadbalancer.server.port=8000"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

networks:
  proxy:
    external: true
```

### Dockerfile Template (Security-Hardened)

```dockerfile
FROM node:20-alpine

# Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["node", "src/server.mjs"]
```

## Rollback

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/mcp-servers/{server-name}
  git log --oneline -5
  git checkout {commit-hash}
  docker compose up -d --build
'
```

## Troubleshooting

### Container Won't Start

```bash
docker logs {container-name} --tail 100
docker compose config
docker compose build --no-cache && docker compose up -d
```

### Health Check Fails

```bash
# Internal test
docker exec {container-name} wget -qO- http://localhost:8000/health

# Check Traefik routing
docker logs traefik --tail 50 | grep {server-name}

# DNS check
nslookup mcp-{name}.dirk-schulenburg.net
```

## Multi-Key Auth

Moodle-MCP und SharePoint-MCP unterstuetzen Multi-Key Auth fuer Kollegen-Zugriff:

```env
MCP_API_KEYS=key1:user1,key2:user2
```

Doku: `_DEV_DOCS/MCP/MCP-Zugriff-fuer-Kollegen.md`

---

*DevOps Skill - MCP Server Deployment v2.0 (2026-03-12)*
