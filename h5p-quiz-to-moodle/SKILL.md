---
name: h5p-quiz-to-moodle
description: Generate H5P quizzes from natural language prompts and upload directly to Moodle. Say "Make a quiz about X" and get it in Moodle instantly.
license: MIT
---

# H5P Quiz to Moodle

Generate interactive H5P quizzes from simple prompts and upload them directly to Moodle LMS.

## When to Use This Skill

Use this skill when the user says things like:
- "Erstelle ein Quiz zu [Thema]"
- "Mach 10 Fragen zur Bilanz"
- "Generiere ein H5P-Quiz ueber Scrum und lade es zu Moodle hoch"
- "Quiz mit schwierigen Fragen zu [Thema] fuer Kurs [ID]"

## Quick Start

**User:** "Mach ein Quiz mit 10 schwierigen Fragen zur Bilanz"

**Claude:**
1. Generiert 10 fachlich korrekte Multiple-Choice-Fragen
2. Erstellt H5P-Datei mit dem h5p-generator
3. Laedt zu Moodle hoch (Kurs 2 = Default)
4. Gibt Content-ID und Embed-Link zurueck

## Workflow

```
[User Prompt] --> [Fragen generieren] --> [H5P erstellen] --> [Moodle Upload] --> [Fertig]
     |                   |                      |                   |
  "Quiz zu X"      Claude Wissen          h5p-generator        moodle-mcp
```

## Parameters

| Parameter | Default | Beschreibung |
|-----------|---------|--------------|
| topic | (required) | Thema des Quiz |
| count | 10 | Anzahl der Fragen |
| difficulty | medium | easy, medium, hard |
| type | multi_choice | multi_choice, true_false, mixed |
| course_id | 2 | Moodle Kurs-ID |
| domain | auto | accounting, scrum, it, business (fuer bessere Distraktoren) |

## Supported Domains

| Domain | Konzepte |
|--------|----------|
| `accounting` | Debitor, Kreditor, Aktiva, Passiva, Soll, Haben, Bilanz, GuV, Buchungen |
| `scrum` | Product Owner, Scrum Master, Sprint, Backlog, Daily, Review, Retrospektive |
| `it` | Server, Client, CPU, RAM, Netzwerk, Datenbank, Protokolle, Programmierung |
| `business` | Angebot, Nachfrage, Preis, Gewinn, Verlust, Kosten, Marketing |

## Example Prompts

### Basic
```
Erstelle ein Quiz zur Bilanz
```

### With Count
```
Mach 15 Fragen zum Thema Scrum-Rollen
```

### With Difficulty
```
Generiere 10 schwierige Pruefungsfragen zur doppelten Buchfuehrung
```

### With Course ID
```
Quiz zu SQL-Grundlagen fuer Kurs 5
```

### Full Specification
```
Erstelle ein Multiple-Choice-Quiz mit 12 mittelschweren Fragen
zum Thema Netzwerkprotokolle und lade es in Kurs 3 hoch
```

## Output

Nach erfolgreicher Ausfuehrung:

```
H5P Quiz erstellt und zu Moodle hochgeladen!

| Eigenschaft | Wert |
|-------------|------|
| Content ID | 27 |
| Titel | Bilanz - Pruefungsfragen |
| Fragen | 10 |
| Typ | Multiple Choice |
| Kurs ID | 2 |

Embed URL: https://moodle.../h5p/embed.php?url=...

Das Quiz kann jetzt in Moodle-Aktivitaeten eingebunden werden.
```

## Technical Implementation

### Step 1: Parse User Request
- Extrahiere Thema, Anzahl, Schwierigkeit
- Bestimme Domain automatisch oder aus Kontext

### Step 2: Generate Questions
- Nutze Claude's Fachwissen fuer das Thema
- Generiere Fragen im h5p-generator Format:
  ```
  Was ist X?
  - Falsche Antwort A
  - Richtige Antwort [correct]
  - Falsche Antwort B
  - Falsche Antwort C
  ```

### Step 3: Create H5P
```
# h5p-generator Skill aufrufen
# Generiert .h5p Datei aus den Fragen
# Output: pfad/zur/datei.h5p
```

### Step 4: Upload to Moodle
```
# Via Moodle MCP Tool (automatisch verfuegbar)
moodle_upload_h5p:
  base64data: [BASE64_ENCODED_H5P]
  filename: "quiz-titel.h5p"
  title: "Quiz-Titel"
  courseid: [KURS_ID]

# Optional: Als Aktivitaet im Kurs einbinden
moodle_create_h5p_activity:
  courseid: [KURS_ID]
  sectionnum: [ABSCHNITT]
  contentid: [CONTENT_ID aus Upload]
  name: "Quiz-Titel"
```

## Requirements

- h5p-generator (lokal)
- moodle-mcp Server (remote)
- Moodle mit local_h5p_api Plugin

## Error Handling

| Fehler | Loesung |
|--------|---------|
| "Plugin nicht installiert" | local_h5p_api in Moodle aktivieren |
| "Unauthorized" | MCP_API_KEY pruefen |
| "Kurs nicht gefunden" | course_id pruefen |
| "H5P-Generierung fehlgeschlagen" | Fragen-Format pruefen |

## Integration with Other Skills

Kann kombiniert werden mit:
- `moodle-course-workflow`: Quiz in neuen Kurs einbetten
- `moodle-section-optimizer`: Quiz als Abschluss einer Sektion
- `lernfeld-zu-moodle-kurs`: Automatische Quiz-Generierung pro Lernsituation

---

*Education Skill — H5P Quiz to Moodle v1.1 (2026-03-12)*
