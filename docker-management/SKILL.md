---
name: docker-management
description: Manage Docker containers on the Hetzner server. Check status, view logs, restart services, and troubleshoot container issues via SSH.
license: MIT
---

# Docker Management

Complete workflow for managing Docker containers on the production Hetzner server.

## When to Use This Skill

Use this skill when:
- Checking container health and status
- Viewing and analyzing container logs
- Restarting or rebuilding containers
- Troubleshooting container issues
- Managing Docker resources (cleanup, volumes)

## Prerequisites

### SSH Access

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192
```

### Server Details

| Property | Value |
|----------|-------|
| **Host** | 95.217.163.192 |
| **User** | dirk |
| **OS** | Ubuntu LTS 24 |
| **Docker** | Docker Compose v2 |
| **Base Dir** | /home/dirk/docker/ |

## Container Overview

### Application Services

| Container | Service | Domain | Compose File |
|-----------|---------|--------|-------------|
| traefik | Reverse Proxy + Let's Encrypt | traefik.dirk-schulenburg.net | docker-compose-traefik.yml |
| n8n | Workflow Automation | n8n.dirk-schulenburg.net | docker-compose-n8n.yml |
| moodle | LMS (moodlehq 5.0) | moodle.dirk-schulenburg.net | moodle/docker-compose-official.yml |
| hedgedoc | Markdown-Editor (reveal.js) | codimd.dirk-schulenburg.net | docker-compose-hedgedoc.yml |
| edugrow-wordpress | EduGrow CMS (Headless) | wp-admin.cannabis-kultur.online | edugrow/infrastructure/docker-compose-edugrow-wordpress.yml |
| cannabis-kultur-frontend | EduGrow Next.js | cannabis-kultur.online | edugrow/infrastructure/docker-compose-edugrow-frontend.yml |
| cccs-tool | Cannabis Chemovar Classification | cccs.cannabis-kultur.online | docker-compose-cccs-tool.yml |
| lernmodule | Lernmaterial-Portal (nginx) | lernmodule.dirk-schulenburg.net | docker-compose-lernmodule.yml |
| h5p-preview | H5P Rendering | h5p-preview.dirk-schulenburg.net | docker-compose-h5p-preview.yml |
| dashboard | Status Dashboard (React) | dashboard.dirk-schulenburg.net | docker-compose-dashboard.yml |
| react-factory | React-Komponenten-Server | react-factory.dirk-schulenburg.net | mcp-servers/react-factory/docker-compose.yml |

### MCP Servers

| Container | Service | Domain | Tools |
|-----------|---------|--------|-------|
| moodle-mcp | Moodle API | mcp-moodle.dirk-schulenburg.net | 73 Tools |
| wp-mcp | WordPress MCP | mcp-wp.dirk-schulenburg.net | 4 Tools |
| edugrow-mcp | EduGrow WordPress API | mcp-edugrow.dirk-schulenburg.net | Media, Posts, H5P |
| imap-mcp | Email Management | mcp-imap.dirk-schulenburg.net | IMAP + SMTP |
| sharepoint-mcp | MS Graph API | mcp-sharepoint.dirk-schulenburg.net | 10 Tools |
| teams-mcp | MS Teams API | mcp-teams.dirk-schulenburg.net | 10 Tools + Calendar |
| ms365-admin-mcp | M365/Entra ID Admin | mcp-ms365.dirk-schulenburg.net | 21 Tools |
| voice-mcp | Whisper + Kokoro TTS | voice-mcp.dirk-schulenburg.net | STT + TTS (oft gestoppt) |

### Databases

| Container | Engine | For |
|-----------|--------|-----|
| n8n-postgres | PostgreSQL | n8n |
| moodle-db | MariaDB | Moodle |
| edugrow-db | MariaDB | EduGrow WordPress |
| hedgedoc-db | PostgreSQL | HedgeDoc |

### Directory Structure (Server)

```
/home/dirk/docker/
├── docker-compose-traefik.yml
├── docker-compose-n8n.yml
├── docker-compose-hedgedoc.yml
├── docker-compose-h5p-preview.yml
├── docker-compose-dashboard.yml
├── docker-compose-cccs-tool.yml
├── docker-compose-lernmodule.yml
├── docker-compose-imap-mcp.yml
├── docker-compose-moodle-mcp.yml
├── docker-compose-wp-mcp.yml
├── docker-compose-voice.yml
├── moodle/
│   └── docker-compose-official.yml
├── edugrow/
│   └── infrastructure/
│       ├── docker-compose-edugrow-wordpress.yml
│       ├── docker-compose-edugrow-frontend.yml
│       └── docker-compose-edugrow-mcp.yml
├── mcp-servers/
│   ├── wp-mcp/               (Submodule)
│   ├── moodle-mcp/           (Submodule)
│   ├── sharepoint-mcp/
│   ├── teams-mcp/
│   ├── ms365-admin-mcp/
│   └── react-factory/
├── lernmodule/
│   └── html/                 (nginx mount)
├── website/                  (NOT a git repo — deploy via SCP!)
└── deploy.sh
```

## Quick Commands

### Check All Containers

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Check Specific Container

```bash
# Container status
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker ps -f name=n8n'

# Container logs (last 50 lines)
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker logs n8n --tail 50'

# Follow logs in real-time
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker logs n8n -f --tail 20'
```

### Health Checks

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  echo "=== MCP Health Checks ==="
  for svc in mcp-moodle mcp-wp mcp-edugrow mcp-imap mcp-sharepoint mcp-teams mcp-ms365; do
    status=$(curl -sf https://${svc}.dirk-schulenburg.net/health 2>/dev/null && echo "OK" || echo "FAIL")
    echo "  $svc: $status"
  done

  echo ""
  echo "=== Application Health ==="
  curl -sf https://n8n.dirk-schulenburg.net/healthz > /dev/null && echo "  n8n: OK" || echo "  n8n: FAIL"
  curl -sf https://moodle.dirk-schulenburg.net > /dev/null && echo "  moodle: OK" || echo "  moodle: FAIL"
  curl -sf https://cannabis-kultur.online > /dev/null && echo "  edugrow: OK" || echo "  edugrow: FAIL"
  curl -sf https://codimd.dirk-schulenburg.net > /dev/null && echo "  hedgedoc: OK" || echo "  hedgedoc: FAIL"
  curl -sf https://lernmodule.dirk-schulenburg.net > /dev/null && echo "  lernmodule: OK" || echo "  lernmodule: FAIL"
'
```

## Container Management

### Restart Container

```bash
# Restart single container
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker restart n8n'

# Restart via docker-compose
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  docker compose -f docker-compose-n8n.yml restart
'
```

### Rebuild Container

```bash
# Rebuild with new code
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  docker compose -f docker-compose-wp-mcp.yml up -d --build
'

# Rebuild without cache
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  docker compose -f docker-compose-wp-mcp.yml build --no-cache
  docker compose -f docker-compose-wp-mcp.yml up -d
'
```

## Log Analysis

### View Logs

```bash
# Last 100 lines
docker logs {container} --tail 100

# Last hour
docker logs {container} --since 1h

# Grep for errors
docker logs {container} 2>&1 | grep -i error
```

### Common Container Names

| Service | Container Name |
|---------|---------------|
| Traefik | `traefik` |
| n8n | `n8n` |
| Moodle | `moodle` |
| HedgeDoc | `hedgedoc` |
| EduGrow Frontend | `cannabis-kultur-frontend` |
| EduGrow WordPress | `edugrow-wordpress` |
| MCP Servers | `moodle-mcp`, `wp-mcp`, `imap-mcp`, `sharepoint-mcp`, `teams-mcp`, `ms365-admin-mcp` |

### Log Patterns to Watch

```bash
# Error patterns
docker logs n8n 2>&1 | grep -E "(ERROR|FATAL|Exception)"

# Connection issues (Traefik)
docker logs traefik 2>&1 | grep -E "(502|503|504)"

# Authentication failures
docker logs moodle-mcp 2>&1 | grep -i "auth"
```

## Troubleshooting

### Container Won't Start

```bash
# 1. Check logs
docker logs {container} --tail 100

# 2. Check compose config
cd /home/dirk/docker
docker compose -f {compose-file} config

# 3. Check ports
netstat -tlnp | grep {port}

# 4. Check disk space
df -h

# 5. Check memory
free -h
```

### Network Issues

```bash
# All services use the 'proxy' network
docker network inspect proxy

# Check container network
docker inspect {container} | grep -A 20 Networks
```

### Moodle-Specific

```bash
# CLI-Pfad: /var/www/html (moodlehq Image, NICHT /bitnami/)
# User: www-data (NICHT daemon)
docker exec moodle php /var/www/html/admin/cli/purge_caches.php
docker exec moodle php /var/www/html/admin/cli/maintenance.php --enable
docker exec moodle php /var/www/html/admin/cli/upgrade.php --non-interactive
```

## Resource Management

### Check Resource Usage

```bash
docker stats --no-stream
```

### Cleanup Commands

```bash
# Safe cleanup (stopped containers + unused images)
docker system prune -f && docker image prune -f

# Check disk usage
docker system df
```

## Backup & Restore

### Database Backup

```bash
# PostgreSQL (n8n)
docker exec n8n-postgres pg_dump -U n8n n8n > backup_n8n_$(date +%Y%m%d).sql

# MariaDB (Moodle)
docker exec moodle-db mysqldump -u root -p$MYSQL_ROOT_PASSWORD moodle > backup_moodle_$(date +%Y%m%d).sql

# MariaDB (EduGrow WordPress)
docker exec edugrow-db mysqldump -u root -p$EDUGROW_DB_ROOT_PASSWORD edugrow > backup_edugrow_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# PostgreSQL
cat backup_n8n.sql | docker exec -i n8n-postgres psql -U n8n n8n

# MariaDB
cat backup_moodle.sql | docker exec -i moodle-db mysql -u root -p$MYSQL_ROOT_PASSWORD moodle
```

## Service-Specific Commands

### n8n

```bash
docker exec -it n8n n8n
docker exec n8n n8n export:workflow --all --output=/data/workflows.json
```

### Database Shells

```bash
docker exec -it n8n-postgres psql -U n8n n8n
docker exec -it moodle-db mysql -u root -p
docker exec -it edugrow-db mysql -u root -p
```

## Quick Reference One-Liners

```bash
# All container status
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker ps -a --format "table {{.Names}}\t{{.Status}}"'

# Restart all MCP servers
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker
  for f in docker-compose-moodle-mcp.yml docker-compose-wp-mcp.yml docker-compose-imap-mcp.yml; do
    docker compose -f $f restart
  done
  cd mcp-servers/sharepoint-mcp && docker compose restart && cd ../..
  cd mcp-servers/teams-mcp && docker compose restart && cd ../..
  cd mcp-servers/ms365-admin-mcp && docker compose restart
'

# View all errors across containers (last hour)
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker ps -q | xargs -I {} sh -c "echo === {} === && docker logs {} --since 1h 2>&1 | grep -i error | tail -5"'

# Disk cleanup
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker system prune -f && docker image prune -f'

# Deploy script
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 '/home/dirk/docker/deploy.sh {server-name}'
```

---

*DevOps Skill - Docker Management v2.0 (2026-03-12)*
