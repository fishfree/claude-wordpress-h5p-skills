# DevOps Skills Bundle

Sammlung der DevOps-Skills für Claude.ai Projekte.

---

# 1. Docker Management

Complete workflow for managing Docker containers on the production Hetzner server.

## When to Use

- Checking container health and status
- Viewing and analyzing container logs
- Restarting or rebuilding containers
- Troubleshooting container issues
- Managing Docker resources (cleanup, volumes)

## Server Details

| Property | Value |
|----------|-------|
| **Host** | 95.217.163.192 |
| **User** | dirk |
| **OS** | Ubuntu LTS 24 |
| **SSH** | `ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192` |

## Running Services

| Container | Domain |
|-----------|--------|
| traefik | (Reverse Proxy) |
| n8n | n8n.dirk-schulenburg.net |
| wordpress | www.dirk-schulenburg.net |
| moodle | moodle.dirk-schulenburg.net |
| wp-mcp | mcp-wp.dirk-schulenburg.net |
| moodle-mcp | mcp-moodle.dirk-schulenburg.net |
| imap-mcp | mcp-imap.dirk-schulenburg.net |
| h5p-viewer | h5p-preview.dirk-schulenburg.net |

## Quick Commands

```bash
# Check all containers
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker ps --format "table {{.Names}}\t{{.Status}}"'

# Container logs
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker logs {container} --tail 50'

# Restart container
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 'docker restart {container}'

# Health checks
curl -s https://mcp-wp.dirk-schulenburg.net/health
curl -s https://mcp-moodle.dirk-schulenburg.net/health
curl -s https://mcp-imap.dirk-schulenburg.net/health
```

## Troubleshooting

```bash
# Container won't start
docker logs {container} --tail 100
docker compose config
df -h  # Check disk space

# Network issues
docker network ls
docker network inspect proxy

# Cleanup
docker system prune -f
docker image prune -f
```

---

# 2. MCP Server Deployment

Complete workflow for deploying MCP servers from local development to Hetzner via Git and Docker.

## When to Use

- Deploying new or updated MCP server code
- Setting up a new MCP server from scratch
- Rolling back to a previous version
- Checking deployment status

## MCP Servers

| Server | Domain | Local Path |
|--------|--------|------------|
| wp-mcp | mcp-wp.dirk-schulenburg.net | mcp-servers/wp-mcp |
| moodle-mcp | mcp-moodle.dirk-schulenburg.net | mcp-servers/moodle-mcp |
| imap-mcp | mcp-imap.dirk-schulenburg.net | mcp-servers/imap-mcp |

## Quick Deploy

```bash
# One-liner deployment (example: wp-mcp)
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/wp-mcp && git pull && docker compose down && docker compose up -d --build'
```

## Full Workflow

### 1. Local Development
```bash
cd C:\Users\mail\entwicklung\docker\mcp-servers\{server-name}
# Make changes
docker compose up --build  # Test locally
curl http://localhost:8000/health
```

### 2. Git Push
```bash
git add .
git commit -m "feat: description"
git push origin master
```

### 3. Server Deployment
```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192
cd /home/dirk/docker/mcp-servers/{server-name}
git pull origin master
docker compose down
docker compose up -d --build
```

### 4. Verification
```bash
docker ps | grep mcp
curl https://mcp-{name}.dirk-schulenburg.net/health
docker logs mcp-{name}-1 --tail 100
```

## Rollback

```bash
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192
cd /home/dirk/docker/mcp-servers/{server-name}
git log --oneline -5
git checkout {commit-hash}
docker compose down && docker compose up -d --build
```

---

# 3. n8n Workflow Management

Complete workflow for creating, debugging, and managing n8n automations.

## When to Use

- Creating new n8n workflows
- Debugging failed executions
- Analyzing workflow performance
- Building integrations

## Access

- **URL:** https://n8n.dirk-schulenburg.net
- **API:** Via n8n MCP Gateway

## MCP Tools

| Tool | Description |
|------|-------------|
| `n8n_list_workflows` | List all workflows |
| `n8n_get_workflow` | Get workflow by ID |
| `n8n_create_workflow` | Create new workflow |
| `n8n_update_partial_workflow` | Incremental updates |
| `n8n_list_executions` | Execution history |
| `n8n_get_execution` | Execution details |
| `n8n_validate_workflow` | Validate structure |
| `n8n_autofix_workflow` | Auto-fix issues |

## Quick Start

```javascript
// List workflows
n8n_list_workflows({ limit: 100 })

// Get workflow
n8n_get_workflow({ id: "123" })

// Check executions
n8n_list_executions({ workflowId: "123", status: "error", limit: 5 })

// Get execution details
n8n_get_execution({ id: "456", mode: "summary" })
```

## Creating Workflows

```javascript
n8n_create_workflow({
  name: "My Automation",
  nodes: [
    {
      id: "trigger-1",
      name: "Webhook",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [250, 300],
      parameters: { path: "my-hook", httpMethod: "POST" }
    },
    {
      id: "http-1",
      name: "API Call",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [450, 300],
      parameters: { url: "https://api.example.com", method: "GET" }
    }
  ],
  connections: {
    "trigger-1": { main: [[{ node: "http-1", type: "main", index: 0 }]] }
  }
})
```

## Debugging

```javascript
// 1. Find failed executions
n8n_list_executions({ workflowId: "123", status: "error" })

// 2. Analyze execution
n8n_get_execution({ id: "456", mode: "full", includeInputData: true })

// 3. Fix node
n8n_update_partial_workflow({
  id: "123",
  operations: [{
    type: "updateNode",
    nodeId: "http-1",
    parameters: { url: "https://correct-url.com" }
  }]
})
```

## Common Node Types

| Node | Use Case |
|------|----------|
| `webhook` | HTTP trigger |
| `scheduleTrigger` | Cron/interval |
| `httpRequest` | API calls |
| `set` | Transform data |
| `if` | Conditional logic |
| `code` | Custom JavaScript |

---

*DevOps Skills Bundle - Docker, MCP Deploy, n8n*
