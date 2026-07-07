---
name: mcp-key-manager
description: >
  Erstellt API-Keys fuer MCP-Server und versendet die Zugangsdaten per Email an Kollegen.
  Use when: "Key erstellen", "Neuen Zugang anlegen", "Kollegen freischalten", "MCP Key erzeugen"
agent: DevOps
allowed-tools:
  - Bash
  - AskUserQuestion
  - mcp__imap__smtp_send_email
---

# MCP Key Manager

Erstellt API-Keys fuer Moodle-MCP (und kuenftig weitere MCP-Server) ueber die Admin-API und versendet die Zugangsdaten per Email an den Kollegen.

## Voraussetzungen

- Admin-API-Key in `config/api-keys.json` auf dem Server
- IMAP-MCP Server laeuft (fuer Email-Versand)
- Admin-Key fuer den Moodle-MCP Server

## Bekannte Kollegen

| Name | Email |
|------|-------|
| Goesicke | goesicke@bswi.de |

Bei unbekannten Kollegen wird die Email-Adresse abgefragt.

---

## Workflow

### Phase 1: Username abfragen

Frage den User nach dem Namen des Kollegen:

> "Fuer welchen Kollegen soll ein API-Key erstellt werden?"

Optionen aus der Kollegenliste anbieten + "Anderer" Option.

### Phase 2: Email-Adresse ermitteln

- Bekannter Kollege: Email aus Tabelle oben nehmen
- Unbekannter Kollege: Email-Adresse abfragen

### Phase 3: Key erzeugen

Admin-Key aus dem Server lesen und Key erzeugen:

```bash
# Admin-Key vom Server holen
ssh -i ~/.ssh/hetzner_ssh_key dirk@95.217.163.192 \
  "jq -r '.keys[] | select(.role==\"admin\") | .key' /home/dirk/docker/mcp-servers/moodle-mcp/config/api-keys.json"

# Key erzeugen
curl -s -X POST https://mcp-moodle.dirk-schulenburg.net/admin/keys \
  -H "x-api-key: ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user":"USERNAME"}' | python -m json.tool
```

Die API gibt zurueck:
```json
{
  "ok": true,
  "key": "64-char-hex",
  "user": "Name",
  "claudeCodeConfig": {
    "mcpServers": {
      "moodle": {
        "type": "url",
        "url": "https://mcp-moodle.dirk-schulenburg.net/mcp",
        "headers": { "x-api-key": "..." }
      }
    }
  }
}
```

### Phase 4: Email versenden

Sende eine Email ueber `smtp_send_email` (IMAP-MCP) mit den Zugangsdaten:

```
Von: mail@dirk-schulenburg.net
An: {kollege}@{domain}
Betreff: Dein Moodle-MCP Zugang

Hallo {Name},

hier sind deine Zugangsdaten fuer den Moodle-MCP Server.
Damit kannst du ueber Claude Code direkt auf Moodle zugreifen.

## Einrichtung

Fuege folgenden Block in deine Claude Code Konfiguration ein
(Datei: ~/.claude/settings.json unter "mcpServers"):

{claudeCodeConfig als formatierter JSON-Block}

## Was du damit machen kannst

- Moodle-Kurse erstellen und verwalten
- Quiz und Aufgaben anlegen
- Nutzer einschreiben
- H5P-Inhalte hochladen
- und vieles mehr (71 Tools)

Dokumentation: https://mcp-moodle.dirk-schulenburg.net/health

Bei Fragen melde dich einfach!

Viele Gruesse
Dirk
```

### Phase 5: Bestaetigung

Zeige dem User:
```
Key erstellt fuer: {Name}
Email gesendet an: {Email}
Key-Prefix: {erste 8 Zeichen}...
```

---

## Fehlerbehandlung

### "Key management requires file-based auth"
Der Server laeuft noch im Env-Modus. Zuerst `config/api-keys.json` auf dem Server anlegen.

### "Admin access required" (403)
Der verwendete Key hat keine Admin-Rolle. In `api-keys.json` pruefen.

### Email-Versand fehlgeschlagen
IMAP-MCP Server pruefen: https://mcp-imap.dirk-schulenburg.net/health

---

*Version: 1.1 — 2026-03-12 — Fixed email tool reference (smtp_send_email statt sendMessage)*
