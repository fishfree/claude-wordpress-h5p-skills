---
name: weekly-digest
description: Generate a weekly activity summary from logs, emails, and completed tasks. Provides insights into productivity and accomplishments. Use when the user wants a weekly review or summary.
license: MIT
allowed-tools:
  - mcp__imap__imap_list_emails
  - mcp__imap__imap_read_email
  - WebFetch
---

# Weekly-Digest Skill

Generiert einen Wochenrückblick mit Aktivitäten, Email-Statistiken und erledigten Aufgaben.

## MCP/Tool Integration

**Dieser Skill nutzt folgende Tools:**

| Tool | Zweck |
|------|-------|
| `imap_list_emails` | Email-Statistiken der Woche |
| `WebFetch` | Activity-Log vom n8n Webhook abrufen |

**Datenquellen:**

| Quelle | Methode | Daten |
|--------|---------|-------|
| Emails | IMAP MCP (`imap_list_emails`) | Empfangen, Gesendet, Archiviert |
| Git Log | `git log --since=7.days` | Commits, geaenderte Dateien |
| Blog | WordPress MCP (`wp_list_posts`) | Neue Artikel |
| Moodle | Moodle MCP (`moodle_list_courses`) | Kursaenderungen |

---

## Wann diesen Skill nutzen

- "Erstelle einen Wochenrückblick"
- "Was habe ich diese Woche gemacht?"
- "Zeig mir meine Aktivitäten der letzten 7 Tage"
- "Weekly Review"
- "Produktivitätsübersicht"

---

## Workflow

### Phase 1: Daten sammeln

**1. Git-Aktivitaet abrufen:**
```bash
# Commits der letzten 7 Tage
git log --since="7 days ago" --oneline --format="%h %s (%an, %ar)"

# Geaenderte Dateien
git diff --stat HEAD~7..HEAD
```

**2. Email-Statistiken:**
```javascript
// Emails der letzten 7 Tage
imap_list_emails({
  account: "onecom",
  folder: "INBOX",
  limit: 100,
  criteria: "SINCE 7-DAYS-AGO"  // Pseudo-Syntax
})

// Gesendete Emails
imap_list_emails({
  account: "onecom",
  folder: "Sent",
  limit: 50
})
```

### Phase 2: Analyse

**Metriken berechnen:**

```javascript
const metrics = {
  // Aktivitäten
  total_activities: activities.length,
  by_agent: groupBy(activities, 'agent'),
  by_action: groupBy(activities, 'action'),
  success_rate: calcSuccessRate(activities),

  // Emails
  emails_received: inbox.length,
  emails_sent: sent.length,
  emails_archived: archived.length,
  top_senders: getTopSenders(inbox, 5),

  // Skills
  skills_used: countSkills(activities),
  most_used_skill: getMostUsed(skills),

  // Kontexte
  context_switches: countContextSwitches(activities),
  primary_context: getPrimaryContext(activities)
};
```

### Phase 3: Report generieren

**Ausgabeformat:**

```markdown
# Wochenrückblick: [Datum] - [Datum]

## Zusammenfassung

Diese Woche war der Fokus auf **[Primärer Kontext]** mit **[X] Aktivitäten**.

| Metrik | Wert |
|--------|------|
| Aktivitäten gesamt | 42 |
| Erfolgsrate | 95% |
| Emails empfangen | 87 |
| Emails gesendet | 12 |
| Skills verwendet | 8 |

---

## Aktivitäten nach Kontext

### 🎓 Education (18 Aktivitäten)
- 5x Moodle-Kurse bearbeitet
- 8x H5P-Content erstellt
- 3x Quizze generiert
- 2x Kursabschnitte optimiert

### 🔧 DevOps (15 Aktivitäten)
- 4x MCP-Server deployed
- 6x Docker-Container verwaltet
- 3x n8n-Workflows debugged
- 2x Backups erstellt

### 📝 Personal (9 Aktivitäten)
- 2x Blog-Artikel veröffentlicht
- 5x Email-Sessions verarbeitet
- 2x Recherchen durchgeführt

---

## Email-Übersicht

### Empfangen: 87 Emails

| Kategorie | Anzahl | Aktion |
|-----------|--------|--------|
| Persönlich | 12 | Beantwortet: 8 |
| Newsletter | 34 | Archiviert: 30 |
| Admin | 15 | Archiviert: 15 |
| Rechnungen | 8 | Geprüft: 8 |
| Spam | 18 | Gelöscht: 18 |

### Top Absender
1. newsletter@service.de (12)
2. support@tool.com (8)
3. kollegin@schule.de (6)

### Gesendet: 12 Emails
- Formell: 4
- Informell: 6
- Follow-ups: 2

---

## Skills-Nutzung

| Skill | Aufrufe | Erfolgsrate |
|-------|---------|-------------|
| h5p-generator | 8 | 100% |
| moodle-section-optimizer | 5 | 100% |
| blog-article-workflow | 2 | 100% |
| email-to-action | 5 | 100% |
| recherche-workflow | 2 | 100% |

**Meistgenutzt:** h5p-generator (8x)

---

## Highlights der Woche

### Erreicht
- ✅ 3 neue Moodle-Kurse erstellt
- ✅ Voice-MCP Server deployed
- ✅ 2 Blog-Artikel veröffentlicht
- ✅ Email-Inbox von 150 auf 20 reduziert

### Begonnen
- 🔄 SharePoint-Integration für Kollegen
- 🔄 Neuer n8n Workflow für Protokolle

### Geplant (nächste Woche)
- 📋 Lernfeld 3 digitalisieren
- 📋 Weekly-Digest automatisieren

---

## Trends

### Produktivität
```
Mo: ████████ 8
Di: ██████████ 10
Mi: ██████ 6
Do: ████████████ 12
Fr: ██████ 6
```
**Peak-Tag:** Donnerstag

### Kontext-Verteilung
```
Education: ████████████████ 43%
DevOps:    ████████████ 36%
Personal:  ████████ 21%
```

---

## Empfehlungen

1. **Email-Management**: Newsletter-Abos überprüfen (34 diese Woche)
2. **Fokus**: Donnerstag ist produktivster Tag - wichtige Tasks dort planen
3. **Skill-Gap**: `email-send` noch nicht genutzt - ausprobieren?

---

*Generiert am [Datum] um [Uhrzeit]*
```

---

## Datenquellen-Details

### Git Log Format

```bash
# Zusammenfassung nach Bereich
git log --since="7 days ago" --format="%s" | sort | uniq -c | sort -rn
```

### Email-Zählung

```javascript
// Zeitraum: Letzte 7 Tage
const weekAgo = new Date();
weekAgo.setDate(weekAgo.getDate() - 7);

// Filter nach Datum
const thisWeek = emails.filter(e =>
  new Date(e.date) >= weekAgo
);
```

---

## Konfiguration

### Report-Umfang

```javascript
const CONFIG = {
  // Zeitraum
  days: 7,  // Standard: 7 Tage

  // Limits
  max_activities: 200,
  max_emails: 500,
  top_senders: 5,

  // Ausgabe
  include_trends: true,
  include_recommendations: true,
  format: 'markdown'  // oder 'html', 'json'
};
```

### Speicherort

```markdown
Report wird gespeichert in:
_DEV_DOCS/Weekly/[YYYY-WW]-weekly-digest.md

Beispiel: _DEV_DOCS/Weekly/2026-W05-weekly-digest.md
```

---

## Automatisierung

### n8n Workflow (geplant)

```
Trigger: Jeden Sonntag 20:00
1. Activity Log abrufen
2. Email Stats sammeln
3. Report generieren
4. In Obsidian speichern
5. Optional: Per Email senden
```

---

## Best Practices

### Do

- Report am Wochenende erstellen (Sonntag Abend ideal)
- Trends über mehrere Wochen vergleichen
- Empfehlungen umsetzen oder bewusst ignorieren
- Highlights feiern!

### Don't

- Zu oft generieren (max. 1x/Woche sinnvoll)
- Sich von niedrigen Zahlen demotivieren lassen
- Micro-Management basierend auf Metriken

---

## Verwandte Skills

- **email-to-action**: Emails der Woche verarbeiten
- **recherche-workflow**: Trends zu Themen recherchieren

---

*Zuletzt aktualisiert: 12.03.2026*
*Version: 1.1 — n8n-Webhook durch git log + MCP-Datenquellen ersetzt*
