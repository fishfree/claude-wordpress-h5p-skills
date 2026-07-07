---
name: session-end
description: >
  Session abschliessen und Tasks auf das Taskboard vorschlagen.
  Nutze am Ende jeder Session oder wenn der User "Session Ende",
  "wir sind fertig", "Schluss fuer heute", "wrap up" sagt.
license: MIT
agent: DevOps
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Session-End Skill

Schliesse die aktuelle Claude-Code-Session ab, indem du offene Tasks, Follow-ups und Ideen auf das Taskboard vorschlaegst.

## Ablauf

### 1. Session reviewen

Gehe die aktuelle Session durch und identifiziere:

- **Offene Punkte**: Was wurde besprochen aber nicht umgesetzt?
- **Follow-ups**: Was muss als naechstes passieren?
- **Ideen**: Was wurde erwaehnt aber zurueckgestellt?
- **Versprechen**: Was hat der User gesagt, das er noch tun will?
- **Bugs/Issues**: Wurden Probleme entdeckt, die noch offen sind?

### 2. Tasks formulieren

Fuer jeden identifizierten Punkt:
- **title**: Kurz, actionable, im Imperativ ("Stripe Webhooks testen", nicht "Stripe Webhooks sollten getestet werden")
- **tags**: Relevante Tags (Projektname, Kategorie, Dringlichkeit)
- **context**: Session-Datum + kurze Erklaerung warum der Task existiert

### 3. An Taskboard senden

Nutze die MCP-Taskboard-Tools (bereits authentifiziert):

```
mcp__taskboard__task_create  — Einzelnen Task anlegen
mcp__taskboard__task_list    — Bestehende Tasks pruefen (Duplikate vermeiden)
mcp__taskboard__task_search  — Nach aehnlichen Tasks suchen
```

Fuer jeden Task `mcp__taskboard__task_create` mit title, tags, context aufrufen.
Status `suggested` wird automatisch gesetzt.

### 4. Zusammenfassung

Zeige dem User:
- Anzahl vorgeschlagener Tasks
- Liste der Task-Titel
- Link zum Dashboard: `https://tasks.dirk-schulenburg.net`

## Regeln

- **Keine Duplikate**: Vor dem Senden pruefen ob aehnliche Tasks schon existieren (`GET /tasks`)
- **Qualitaet > Quantitaet**: Lieber 3 gute Tasks als 10 vage
- **Kontext ist Pflicht**: Jeder Task braucht ein `context`-Feld mit Session-Bezug
- **Nicht nerven**: Wenn die Session trivial war (nur eine Frage beantwortet), keine Tasks vorschlagen
- **Proaktiv**: Auch ohne expliziten Aufruf am Session-Ende Tasks vorschlagen, wenn sich welche ergeben haben

## Taskboard API

Primaer die MCP-Tools nutzen (`mcp__taskboard__task_*`). Die REST-API ist als Fallback verfuegbar:

| Endpoint | Zweck |
|----------|-------|
| `GET /tasks` | Bestehende Tasks pruefen (Duplikate vermeiden) |
| `POST /tasks/suggest` | Batch-Vorschlaege senden |
| `POST /tasks` | Einzelnen Task direkt anlegen (fuer dringendes) |

**Auth:** Basic Auth — Credentials in `$TASKBOARD_AUTH` env var (Format: `user:pass`)
**URL:** `https://tasks.dirk-schulenburg.net`
