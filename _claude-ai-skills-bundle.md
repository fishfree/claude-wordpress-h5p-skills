# Claude AI Skills Bundle

This file contains all specialized Claude Code skills for the Dirk Schulenburg infrastructure. These skills provide domain-specific workflows and automation capabilities across Education, Personal, and DevOps contexts.

**Generated:** 2026-01-26
**Skills Count:** 13
**Agents:** Education (7), Personal (2), DevOps (4)

---

## Table of Contents

1. [h5p-quiz-to-moodle](#h5p-quiz-to-moodle) - Generate H5P quizzes and upload to Moodle
2. [h5p-generator](#h5p-generator) - Create H5P files programmatically
3. [h5p-wordpress-workflow](#h5p-wordpress-workflow) - H5P + WordPress integration
4. [moodle-course-workflow](#moodle-course-workflow) - Create Moodle courses with H5P
5. [moodle-section-analyzer](#moodle-section-analyzer) - Analyze courses for 4K deficits
6. [moodle-section-optimizer](#moodle-section-optimizer) - Optimize Moodle sections
7. [lernfeld-zu-moodle-kurs](#lernfeld-zu-moodle-kurs) - Transform teaching materials to Moodle
8. [bswi-infobrief](#bswi-infobrief) - Format school newsletters
9. [blog-article-workflow](#blog-article-workflow) - Create and publish blog articles
10. [recherche-workflow](#recherche-workflow) - Research contrarian positions
11. [docker-management](#docker-management) - Manage Docker containers
12. [mcp-server-deploy](#mcp-server-deploy) - Deploy MCP servers
13. [n8n-workflow](#n8n-workflow) - Create and debug n8n workflows

---

# h5p-quiz-to-moodle

---
name: h5p-quiz-to-moodle
description: Generate H5P quizzes from natural language prompts and upload directly to Moodle. Say "Make a quiz about X" and get it in Moodle instantly.
license: MIT
agent: Education
---

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
```python
from h5p_system import H5PSystem

system = H5PSystem()
result = system.generate_from_questions(
    questions_text,
    title=title,
    domain=domain
)
```

### Step 4: Upload to Moodle
```python
# Via Moodle MCP
POST https://mcp-moodle.dirk-schulenburg.net/mcp
Headers:
  Content-Type: application/json
  Accept: application/json, text/event-stream
  x-api-key: {MCP_API_KEY}

Body:
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "moodle_upload_h5p",
    "arguments": {
      "base64data": "{h5p_base64}",
      "filename": "{filename}.h5p",
      "title": "{title}",
      "courseid": {course_id}
    }
  }
}
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

*Skill fuer den Education Agent - Dirk als Lehrer an der BS:WI*

---

# h5p-generator

---
name: h5p-generator
description: Generate H5P interactive content files (.h5p) programmatically using Python. Supports 9 content types with error handling, styling themes, and batch creation. Use for quizzes, flashcards, drag-and-drop, and more.
license: MIT
agent: Education
---

## H5P Generator v2.3

Generate .h5p files directly from Python with robust error handling and customizable styling.

## Supported Content Types (12)

| Type | Function | Use Case |
|------|----------|----------|
| **True/False** | `create_true_false()` | Wahr/Falsch Quizze |
| **Multiple Choice** | `create_multi_choice()` | MC-Fragen mit 2+ Optionen |
| **Fill in Blanks** | `create_fill_blanks()` | Lückentexte mit `*Lücke*` |
| **Drag and Drop** | `create_drag_drop()` | Zuordnungsaufgaben (Kategorien) |
| **Drag the Words** | `create_drag_text()` | Wörter in Lücken ziehen |
| **Single Choice** | `create_single_choice()` | Schnelle Single-Choice |
| **Flashcards** | `create_flashcards()` | Lernkarten (Dialog Cards) |
| **Mark Words** | `create_mark_words()` | Wörter im Text markieren |
| **Summary** | `create_summary()` | Zusammenfassungen |
| **Accordion** | `create_accordion()` | Aufklappbare Abschnitte |
| **Timeline** | `create_timeline()` | Zeitleisten mit Events |
| **Memory Game** | `create_memory_game()` | Memory (benötigt Bilder) |

## Entscheidungsmatrix (Wann welcher Typ?)

Siehe `references/templates/decision-matrix.md` für die vollständige Logik.

| Lernziel | Operator | H5P-Typ |
|----------|----------|---------|
| Begriffe lernen | nennen | Flashcards |
| Fakten prüfen | beschreiben | True-False |
| Kategorien | zuordnen | Drag-and-Drop |
| Lücken füllen | ergänzen | Fill-in-Blanks oder Drag-Text |
| Chronologie | ordnen | Timeline |
| Zusammenhänge | erklären | Accordion |
| Optionen | bewerten | Branching (manuell) |

**Didaktische Regel:** Gamification-Typen (Flashcards, Drag&Drop, Memory) nur unterstützend einsetzen, nicht als Hauptlernform auf IHK/Abitur-Niveau.

## Quick Start

```python
from h5p_generator import (
    create_true_false, create_multi_choice, create_fill_blanks,
    create_drag_drop, create_single_choice, create_flashcards,
    create_mark_words, create_summary, create_accordion,
    THEMES, H5PStyle
)

# Mit Education-Theme
style = THEMES['education']

# True/False Quiz
result = create_true_false(
    "Python Basics",
    [
        {"text": "Python ist eine Programmiersprache.", "correct": True},
        {"text": "Python wurde 2020 erfunden.", "correct": False}
    ],
    "python-quiz",
    style=style
)

if result.success:
    print(f"Erstellt: {result.path}")
else:
    print(f"Fehler: {result.error}")
```

## Error Handling

Alle Funktionen geben ein `H5PResult` zurück:

```python
@dataclass
class H5PResult:
    success: bool           # True = OK, False = Fehler
    path: Path | None       # Pfad zur .h5p Datei
    error: str | None       # Fehlermeldung
    content_type: str       # z.B. "TrueFalse"
    title: str              # Titel des Inhalts
```

## Styling & Themes

Vordefinierte Themes:

| Theme | Beschreibung |
|-------|--------------|
| `default` | Blaue Akzente, neutral |
| `dark` | Dunkler Hintergrund |
| `education` | Grüne Akzente, Schüler-freundlich |
| `professional` | Business-Look |

## Content Types im Detail

### 1. True/False

```python
questions = [
    {
        "text": "Die Erde ist rund.",
        "correct": True,
        "feedback_correct": "Richtig!",
        "feedback_wrong": "Leider falsch."
    }
]
create_true_false("Geo Quiz", questions, "geo-quiz")
```

### 2. Multiple Choice

```python
questions = [
    {
        "question": "Was ist die Hauptstadt von Deutschland?",
        "answers": [
            {"text": "Berlin", "correct": True},
            {"text": "Hamburg", "correct": False},
            {"text": "München", "correct": False},
            {"text": "Köln", "correct": False}
        ]
    }
]
create_multi_choice("Städte Quiz", questions, "staedte")
```

### 3. Fill in Blanks (Lückentext)

```python
text = "<p>Die Hauptstadt ist *Berlin*. Die Währung ist der *Euro/EUR*.</p>"
create_fill_blanks("Deutschland", text, "de-luecken")
```

### 4. Drag and Drop

```python
dropzones = ["Obst", "Gemüse", "Fleisch"]
draggables = [
    {"text": "Apfel", "dropzone": 0},
    {"text": "Karotte", "dropzone": 1},
    {"text": "Steak", "dropzone": 2},
    {"text": "Banane", "dropzone": 0}
]
create_drag_drop("Lebensmittel", "Ordne zu!", dropzones, draggables, "food")
```

### 5. Single Choice Set

```python
questions = [
    {
        "question": "Was ist 2 + 2?",
        "answers": ["4", "3", "5", "6"]  # Erste = korrekt
    }
]
create_single_choice("Mathe", questions, "mathe-quick")
```

### 6. Flashcards (Lernkarten)

```python
cards = [
    {"front": "Haus", "back": "house", "tip": "Beginnt mit H"},
    {"front": "Auto", "back": "car"},
    {"front": "Baum", "back": "tree"}
]
create_flashcards("Englisch Vokabeln", cards, "vokabeln")
```

### 7. Mark the Words

```python
text = "Berlin ist die *Hauptstadt* von *Deutschland*. Paris liegt in Frankreich."
create_mark_words(
    "Geografie",
    text,
    "geo-mark",
    task="Markiere alle Begriffe, die zu Deutschland gehören."
)
```

### 8. Summary

```python
items = [
    {
        "statements": [
            "Python ist interpretiert",  # Korrekt
            "Python ist kompiliert",
            "Python ist assembler"
        ]
    }
]
create_summary("Python Facts", items, "python-summary")
```

### 9. Accordion

```python
panels = [
    {"title": "Einführung", "content": "Dies ist die Einführung..."},
    {"title": "Hauptteil", "content": "Der Hauptteil behandelt..."},
    {"title": "Fazit", "content": "Zusammenfassend lässt sich sagen..."}
]
create_accordion("Lerneinheit", panels, "lerneinheit")
```

### 10. Drag the Words

```python
text = "In *Scrum* arbeitet das Team in *Sprints*. Der *Product Owner* priorisiert."
create_drag_text(
    "Agile Begriffe",
    text,
    "agile-dragtext",
    task="Ziehe die Begriffe an die richtige Stelle."
)
```

### 11. Timeline

```python
events = [
    {"headline": "ARPANET", "start_date": "1969", "text": "Erstes Netzwerk"},
    {"headline": "World Wide Web", "start_date": "1991", "text": "Tim Berners-Lee"},
    {"headline": "Google", "start_date": "1998-09", "text": "Suchmaschine gestartet"},
]
create_timeline("Internet-Geschichte", events, "internet-timeline")
```

### 12. Memory Game

```python
cards = [
    {"description": "Scrum Master", "image": "https://example.com/sm.jpg"},
    {"description": "Product Owner", "image": "https://example.com/po.jpg"},
]
create_memory_game("Scrum-Rollen Memory", cards, "scrum-memory")
```

## Batch-Erstellung

```python
from h5p_generator import batch_create, THEMES

content = [
    {
        "type": "true_false",
        "title": "Quiz 1",
        "questions": [{"text": "Test", "correct": True}]
    },
    {
        "type": "flashcards",
        "title": "Vokabeln",
        "cards": [{"front": "Hallo", "back": "Hello"}]
    }
]

results = batch_create(content, style=THEMES['education'])
```

## Text-zu-Quiz (v2.3)

```python
from h5p_system import H5PSystem

system = H5PSystem()

# Multiple Choice mit Antworten
result = system.generate_from_questions('''
    Was ist ein Debitor?
    - Ein Schuldner
    - Ein Glaeubiger [correct]
    - Ein Lieferant
''', title="Rechnungswesen Quiz")
```

## Limitations

- **Image Hotspots**: Nicht unterstützt (Web-Editor nutzen)
- **Branching Scenario**: Zu komplex (manuell erstellen)
- **Interactive Video**: Benötigt Video-Dateien
- **Course Presentation**: Zu komplex (manuell erstellen)
- **Interactive Book**: Manuell in H5P-Editor erstellen

---

*Version 2.3 - Text-zu-Quiz mit Distractor-Generator*

---

# h5p-wordpress-workflow

---
name: h5p-wordpress-workflow
description: Complete workflow for creating and publishing H5P interactive content to WordPress. Use when users want to create interactive educational content (quizzes, videos, presentations), integrate H5P with WordPress, or automate H5P content publishing workflows with MCP servers.
license: MIT
agent: Education
---

Complete workflow for creating interactive educational content with H5P and publishing to WordPress, with optional MCP automation.

## When to Use This Skill

Use this skill when:
- Creating interactive educational content (quizzes, interactive videos, timelines, etc.)
- Publishing H5P content to WordPress
- Automating H5P workflows with MCP servers
- Setting up H5P for educational institutions
- Migrating H5P content between platforms

## Quick Start

### Basic Workflow (Manual)
1. Create H5P content on H5P.com or locally
2. Export as .h5p file
3. Upload to WordPress via Media Library
4. Embed using shortcode: `[h5p id="123"]`

### Advanced Workflow (MCP Automation)
1. Create H5P content
2. Store .h5p file in accessible location (URL)
3. Use MCP to upload and publish automatically

## H5P Content Types Overview

### Most Popular for Education

**Interactive Video** - Videos with embedded questions, popups, and navigation
- Use case: Flipped classroom, video lessons with comprehension checks
- Engagement: 5/5

**Quiz (Question Set)** - Multiple question types in sequence
- Use case: Assessments, self-checks, homework
- Engagement: 4/5

**Course Presentation** - Slide-based presentations with interactive elements
- Use case: Lessons, tutorials, presentations
- Engagement: 4/5

**Interactive Book** - Multi-page content with various H5P elements
- Use case: Digital textbooks, comprehensive learning modules
- Engagement: 5/5

## WordPress Integration

### Requirements
- WordPress 5.0+
- H5P plugin installed and activated
- Sufficient upload size limit (typically 64MB+)

### MCP Automation Process

```javascript
// 1. Use MCP tool: wp_upload_h5p_from_url
//    Input: fileUrl, title (optional)
//    Output: Media ID

// 2. Use MCP tool: wp_create_post or wp_update_post
//    Include H5P shortcode with returned Media ID
```

## MCP Integration Details

### Tool: wp_upload_h5p_from_url
```javascript
Input:
{
  fileUrl: "https://example.com/content.h5p",
  title: "Interactive Quiz - Chapter 1"
}

Output:
{
  id: 123,
  source_url: "https://yoursite.com/wp-content/uploads/h5p/content.h5p",
  mime_type: "application/zip"
}
```

### Tool: wp_create_post (with H5P)
```javascript
Input:
{
  title: "Lesson: Introduction to Photosynthesis",
  content: "<p>Watch this interactive video...</p>",
  h5pId: "123",  // Appends [h5p id="123"] automatically
  status: "draft"
}
```

## Best Practices

### Content Creation
- Start simple, add complexity gradually
- Test on target device types (mobile, tablet, desktop)
- Include clear instructions within H5P content
- Provide feedback for all answer types
- Use multimedia strategically (not for decoration)

### WordPress Integration
- Use descriptive titles when uploading H5P files
- Add H5P content early in post (don't bury it)
- Provide context before and after H5P element
- Test all interactions after publishing
- Check mobile responsiveness

---

*This skill is based on real-world usage by educators using H5P daily in classroom settings.*

---

# moodle-course-workflow

---
name: moodle-course-workflow
description: Complete workflow for creating Moodle courses with H5P content integration from WordPress. Use when creating educational courses, adding interactive H5P modules to Moodle, or automating course deployment.
license: MIT
agent: Education
---

Complete workflow for creating Moodle courses with sections, activities, and H5P content integration from WordPress.

## When to Use This Skill

Use this skill when:
- Creating new Moodle courses programmatically
- Adding H5P interactive content from WordPress to Moodle
- Building structured learning modules with multiple sections
- Automating course deployment workflows
- Setting up courses based on course templates/concepts

## Prerequisites

### Required MCP Servers
1. **moodle-mcp** - Moodle course management
   - Tools: `moodle_create_course`, `moodle_create_section`, `moodle_create_url`, `moodle_create_page`, `moodle_create_label`

2. **wp-mcp** - WordPress/H5P management (for H5P integration)
   - Tools: `wp_import_h5p`, `wp_list_h5p_contents`, `wp_create_post`

## Quick Start

### Basic Course Creation

```
1. Create course: moodle_create_course
   - fullname, shortname, categoryid, numsections

2. Add sections: moodle_create_section (repeat for each module)
   - courseId, position, name, summary

3. Add content: moodle_create_url / moodle_create_page / moodle_create_label
   - courseId, sectionNum, name/content
```

## H5P Integration Methods

### Method 1: URL Resource (Simple)

```javascript
moodle_create_url({
  courseId: 123,
  sectionNum: 1,
  name: "Interactive Quiz",
  url: "https://your-wordpress.com/?p=POST_ID_WITH_H5P"
})
```

### Method 2: Page with iFrame (Embedded)

```javascript
moodle_create_page({
  courseId: 123,
  sectionNum: 1,
  pageName: "Interactive Quiz",
  content: `
    <p>Complete the following interactive quiz:</p>
    <iframe
      src="https://your-wordpress.com/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID"
      width="100%"
      height="600"
      frameborder="0"
      allowfullscreen>
    </iframe>
  `
})
```

### Method 3: Label with Embed (Inline)

```javascript
moodle_create_label({
  courseId: 123,
  sectionNum: 1,
  labelText: `
    <h4>Practice Exercise</h4>
    <iframe
      src="https://your-wordpress.com/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID"
      width="100%"
      height="500"
      frameborder="0">
    </iframe>
  `
})
```

## H5P Embed URL Format

```
https://YOUR-WORDPRESS-URL/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID
```

## Moodle Tools (via moodle-mcp)

| Tool | Description |
|------|-------------|
| `moodle_create_course` | Create new course |
| `moodle_create_section` | Add section to course |
| `moodle_update_section` | Rename/modify section |
| `moodle_create_url` | Add URL resource |
| `moodle_create_page` | Add page with content |
| `moodle_create_label` | Add inline text/HTML |
| `moodle_get_course_contents` | View course structure |

---

*This skill combines moodle-mcp and wp-mcp for seamless course creation with interactive content.*

---

# moodle-section-analyzer

---
name: moodle-section-analyzer
description: Analysiert Moodle-Kursabschnitte auf 4K-Defizite (Kreativität, Kritisches Denken, Kommunikation, Kollaboration), fehlende Interaktivität und Multimedia-Lücken. Gibt konkrete Optimierungsvorschläge mit H5P-Empfehlungen. Nutze wenn Lehrer einen Kurs modernisieren, mehr Engagement erreichen oder didaktisch aufwerten wollen.
license: MIT
agent: Education
---

Analysiert Moodle-Abschnitte und identifiziert Optimierungspotenzial nach modernen didaktischen Prinzipien (4K, Gamification, Multimedia).

## Wann nutzen

- Bestehenden Moodle-Kurs modernisieren
- 4K-Defizite systematisch identifizieren
- Vor Einsatz des `moodle-section-optimizer` Skills
- Qualitätscheck für E-Learning-Inhalte

## Voraussetzungen

- **MCP Server**: moodle-mcp mit `moodle_get_course_contents`, `moodle_get_page`, `moodle_get_label`
- **Kurs-ID**: Muss bekannt sein

## Analyse-Framework

### 4K-Kompetenzmodell

| K | Beschreibung | Moodle-Indikatoren |
|---|--------------|-------------------|
| **Kreativität** | Eigene Lösungen entwickeln | Aufgaben, Wikis, H5P Drag&Drop |
| **Kritisches Denken** | Analysieren, Bewerten | Quizze, Selbsttests, Reflexionsaufgaben |
| **Kommunikation** | Ideen austauschen | Foren, Peer-Feedback, Präsentationen |
| **Kollaboration** | Zusammenarbeiten | Wikis, Gruppenforen, gemeinsame Dokumente |

### Engagement-Indikatoren

| Element | Typ | Engagement-Score |
|---------|-----|------------------|
| Label (nur Text) | Passiv | 1/5 |
| URL (externer Link) | Passiv | 1/5 |
| Page (Inhaltsseite) | Passiv | 2/5 |
| Forum | Aktiv | 3/5 |
| Assignment | Aktiv | 3/5 |
| Quiz | Interaktiv | 4/5 |
| H5P | Interaktiv | 5/5 |
| Wiki | Kollaborativ | 4/5 |

### Engagement-Score Berechnung

```
Engagement-Score = (Aktiv x 2 + Interaktiv x 3) / (Passiv + Aktiv x 2 + Interaktiv x 3) x 100
```

- < 30%: Kritisch (zu passiv)
- 30-50%: Verbesserungswürdig
- 50-70%: Gut
- > 70%: Exzellent

## Native Moodle H5P (empfohlen)

Seit dem `local_h5p_api` Plugin können H5P-Inhalte direkt in der Moodle Content Bank gespeichert werden:

| Aspekt | WordPress H5P | Moodle H5P (nativ) |
|--------|---------------|-------------------|
| Backup | Nicht im Kurs-Export | Im Kurs-Backup |
| Embed | iframe zu WordPress | Moodle-native |
| Abhängigkeit | WordPress muss laufen | Standalone |

## Kritische Warnung: Berechtigungen

Nach CLI-Befehlen im Moodle-Container können Berechtigungsprobleme auftreten:

**Symptom:** "Invalid permissions detected when trying to create a directory"

**Lösung:**
```bash
docker exec moodle chown -R daemon:daemon /bitnami/moodledata/
```

**Prävention:** CLI-Befehle als daemon ausführen:
```bash
docker exec -u daemon moodle php /bitnami/moodle/admin/cli/purge_caches.php
```

---

*Skill Version: 1.1 - Abhängigkeiten: moodle-mcp (v2.4.0+)*

---

# moodle-section-optimizer

---
name: moodle-section-optimizer
description: Optimiert Moodle-Kursabschnitte basierend auf 4K-Analyse. Erstellt Labels mit Bildern, generiert H5P-Inhalte, fügt Struktur-Elemente hinzu. Nutze nach moodle-section-analyzer oder wenn konkrete Verbesserungen umgesetzt werden sollen.
license: MIT
agent: Education
---

Setzt konkrete Optimierungen für Moodle-Abschnitte um: Labels, H5P, Struktur, Multimedia.

## Wann nutzen

- Nach Analyse mit `moodle-section-analyzer`
- Konkrete 4K-Lücken schließen
- Abschnitt visuell aufwerten
- Interaktive Elemente hinzufügen

## Voraussetzungen

- **MCP Server**: moodle-mcp (v2.4.0+) mit H5P-Tools
- **Skills**: h5p-generator (für H5P-Erstellung)
- **Analyse**: Idealerweise vorher `moodle-section-analyzer` ausführen

## Optimierungs-Bausteine

### 1. Phasen-Labels (Struktur)

```html
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
  <h3 style="margin: 0;">Phase 1: Orientierung</h3>
  <p style="margin: 5px 0 0 0; opacity: 0.9;">ca. 15 Minuten</p>
</div>
```

**Farb-Schema nach Phase:**

| Phase | Farbe | Hex |
|-------|-------|-----|
| Orientierung | Blau-Lila | #667eea -> #764ba2 |
| Motivation | Orange-Rot | #f093fb -> #f5576c |
| Erarbeitung | Grün | #4facfe -> #00f2fe |
| Analyse | Gelb-Orange | #fa709a -> #fee140 |
| Anwendung | Türkis | #30cfd0 -> #330867 |
| Reflexion | Grün-Blau | #38f9d7 -> #43e97b |
| Abschluss | Gold | #f7971e -> #ffd200 |

### 2. Lernziel-Labels

```html
<div style="background: #e8f5e9; padding: 15px; border-radius: 8px;
            border-left: 4px solid #4caf50;">
  <h4 style="margin: 0 0 10px 0;">Lernziele</h4>
  <ul style="margin: 0; padding-left: 20px;">
    <li>Den Checkout-Prozess beschreiben können</li>
    <li>Abbruchgründe analysieren und bewerten</li>
  </ul>
</div>
```

### 3. H5P-Elemente (via h5p-generator)

| 4K-Defizit | H5P-Typ | Beispiel |
|------------|---------|----------|
| Kreativität niedrig | Drag & Drop | Checkout-Schritte zuordnen |
| Krit. Denken niedrig | Quiz / True-False | Wissen überprüfen |
| Krit. Denken niedrig | Fill in Blanks | Definitionen vervollständigen |

## Optimierungs-Rezepte

### Rezept 1: "Quick Win" - Visuelle Aufwertung (15 Min)

```yaml
schritte:
  1. Phase-Label am Anfang (Gradient + Emoji)
  2. Lernziel-Label nach Einführung
  3. Abschluss-Label am Ende

aufwand: 1/3
4k_impact: Gering (Orientierung verbessert)
```

### Rezept 2: "Interaktivität" - H5P hinzufügen (30 Min)

```yaml
schritte:
  1. Quiz mit 5 Fragen erstellen (h5p-generator)
  2. Fill-in-Blanks für Definitionen
  3. In Moodle als Page einbetten

aufwand: 2/3
4k_impact: Kritisches Denken erhöht
```

### Rezept 3: "Vollständig" - Alle 4K abdecken (60 Min)

```yaml
schritte:
  1. Struktur-Labels (Phasen)
  2. Einführungs-Label mit Bild
  3. H5P Quiz (Kritisches Denken)
  4. H5P Drag&Drop (Kreativität)
  5. Forum-Aufgabe umformulieren (Kollaboration)
  6. Peer-Review-Anweisung (Kommunikation)
  7. Abschluss-Label mit Badge-Hinweis

aufwand: 3/3
4k_impact: Alle 4K verbessert
```

## Reihenfolge der Module

Nach Optimierung sollte ein Abschnitt folgende Struktur haben:

```
Abschnitt X: [Thema]
|- Phase-Label (Einführung)
|- Lernziele
|- Einführungs-Label mit Bild
|- LOOP/Theorie-Link
|- H5P Selbsttest (Verständnissicherung)
|- Arbeitsauftrag / Assignment
|- Forum zur Aufgabe
|- H5P Quiz (Abschlusstest)
|- Abschluss-Label
```

## Limitations

| Limitation | Workaround |
|------------|------------|
| **Module immer am Ende** | Manuell in Moodle sortieren |
| **Keine Modul-Sortierung** | Drag&Drop im Browser |
| **Kein Forum/Quiz erstellen** | Manuell anlegen |

---

*Skill Version: 1.1 - Abhängigkeiten: moodle-mcp (v2.4.0+), h5p-generator*

---

# lernfeld-zu-moodle-kurs

---
name: lernfeld-zu-moodle-kurs
description: Erstellt Moodle-Kurse aus Lernfeld-Materialien (Matchpläne, Präsentationen, Arbeitsblätter). Use when Lehrer möchte Unterrichtsmaterial in Moodle-Kursstruktur umwandeln, Lernfelder/Lernsituationen digitalisieren, oder bestehende Kurse als Template nutzen.
license: MIT
agent: Education
tools:
  - moodle:moodle_create_course
  - moodle:moodle_create_section
  - moodle:moodle_update_section
  - moodle:moodle_create_page
  - moodle:moodle_create_label
  - moodle:moodle_create_url
  - moodle:moodle_create_folder
---

Workflow zur Transformation von Lernfeld-Materialien (Matchpläne, PPT, Arbeitsblätter) in strukturierte Moodle-Kurse.

## Wann diesen Skill nutzen

- Lernfeld-Unterlagen in Moodle-Kurs umwandeln
- Matchpläne als Basis für Kursstruktur verwenden
- Konsistente Kursstrukturen über Lernfelder hinweg erstellen
- Bestehende Präsenzmaterialien digitalisieren

## Voraussetzungen

### MCP Server
- **moodle-mcp** mit Tools: create_course, create_section, create_page, create_label, create_url, create_folder

### Input-Materialien
- **Matchpläne** (.docx) - Unterrichtsplanung mit Folienreferenzen
- **Präsentationen** (.pptx) - LuL und SuS Versionen
- **Arbeitsblätter** (.docx) - Übungen, Lösungen
- **Optional:** LOOP-Links, externe Ressourcen

## Kurs-Struktur-Template

```yaml
kurs:
  fullname: "LF[X] - [Lernfeld-Titel]"
  shortname: "LF[X]-[Bildungsgang]"
  format: topics

abschnitte:
  # Abschnitt 0: Meta/Einleitung
  - position: 0
    name: "[Lernfeld-Titel]"
    inhalte:
      - type: label
        text: "Willkommen im Lernraum..."
      - type: forum
        name: "Ankündigungen"
      - type: page
        name: "Informationen zur Arbeit mit diesem Modul"

  # Abschnitt 1: Lehrer-Material (versteckt)
  - position: 1
    name: "Hinweise für Lehrkräfte (für SuS nicht sichtbar)"
    visible: false
    inhalte:
      - type: folder
        name: "Hinweise zur Arbeit mit diesem Lernfeld"

  # Abschnitte 2+: Lernsituationen/Kapitel
  - position: 2
    name: "[Nr] [Kapitel-Titel]"
    inhalte:
      - type: forum
        name: "Forum [Nr]: [Kapitel-Titel]"
      - type: url
        name: "[Kapitel-Titel] (LOOP-Kapitel)"
```

## Workflow

### Phase 1: Material-Analyse (10 Min)

```
Lernfeld-Material/
|- Lernsituation_01/
|  |- Matchplan.docx          <- Hauptquelle für Struktur
|  |- Präsentation_LuL.pptx   <- Folienreferenzen
|  |- Präsentation_SuS.pptx   <- Für Schüler
|  |- Arbeitsblätter/
|- Lernsituation_02/
|- Allgemein/
   |- Lehrerinfo.docx
```

### Phase 2: Struktur-Mapping (15 Min)

**Matchplan-Zeile -> Moodle-Aktivität:**

| Matchplan-Element | Moodle-Aktivität |
|-------------------|------------------|
| "Schüler diskutieren..." | Forum |
| "Schüler recherchieren..." | URL (externe Quelle) |
| "Arbeitsauftrag siehe Folie" | Page mit Aufgabenstellung |
| "Schüler bearbeiten AB" | Assignment |
| "Gruppenarbeit..." | Forum oder Wiki |

### Phase 3: Kurs erstellen (MCP)

```javascript
// 1. Kurs anlegen
moodle:moodle_create_course({
  fullname: "LF3 - Verträge im Online-Vertrieb",
  shortname: "LF3-ECOM",
  categoryid: "1",
  format: "topics",
  numsections: "9"
})

// 2. Abschnitte benennen
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "0",
  name: "Lernfeld 3 - Verträge im Online-Vertrieb"
})

// 3. Aktivitäten hinzufügen
moodle:moodle_create_label({
  courseId: "6",
  sectionNum: "0",
  labelText: "<h3>Herzlich Willkommen!</h3>"
})
```

## Best Practices

### Struktur
- **Konsistente Nummerierung:** "1 Titel", "2 Titel" (nicht "LS01")
- **Abschnitt 0** immer für Meta-Infos (Willkommen, Foren)
- **Abschnitt 1** versteckt für Lehrer-Material
- **Foren vor Aufgaben:** Erst diskutieren, dann abgeben

### Benennung
- Hauptforum: "Forum X: [Kapitel-Titel]"
- Aufgabenforum: "Forum zur Aufgabe X: [Kontext]"
- LOOP-Links: "[Titel] (LOOP-Kapitel)"
- Assignments: "Aufgabe X: [Aufgaben-Titel]"

## Limitationen

### Was dieser Skill NICHT kann:
- **Foren automatisch erstellen** (Moodle-API unterstützt das nicht)
- **Assignments erstellen** (benötigt mod_assign Capability)
- **Dateien hochladen** (benötigt separaten Upload-Workflow)
- **Quiz/H5P erstellen** (siehe h5p-generator Skill)

### Workarounds:
- Foren: Manuell in Moodle erstellen oder Kurs-Template nutzen
- Dateien: Über Moodle-UI oder WebDAV hochladen
- Assignments: Manuell anlegen, Struktur als Vorlage nutzen

---

*Skill basiert auf dem E-Commerce Lernfeld 3 Kurs (Kurs-ID 6) der BS:WI Hamburg.*

---

# bswi-infobrief

---
name: bswi-infobrief
description: Formatiert Markdown-Infobriefe im Corporate Design der BS:WI Hamburg. Nutze diesen Skill, um Infobriefe professionell zu gestalten, HTML/PDF zu exportieren und das CI der Schule (Farben, Logo, Layout) anzuwenden.
license: MIT
agent: Education
allowed-tools: Read, Glob, Bash(python:*), Write, Edit
---

## Überblick

Dieser Skill formatiert deine Markdown-Infobriefe im Corporate Design der Beruflichen Schule für Wirtschaft und Internationales Hamburg (BS:WI). Er wandelt einfache Markdown-Dateien in professionell gestaltete HTML- oder PDF-Dokumente mit dem offiziellen CI um.

**Features:**
- Automatische Anwendung der BS:WI Farben (Dunkelblau, Hellblau, Neongelb)
- Professionelles Header-Design mit Schullogo
- Strukturierte Darstellung von "Need-to-know" und "Nice-to-know" Abschnitten
- HTML-Export für E-Mail-Versand oder Web-Veröffentlichung
- Optional: PDF-Export für Druck oder Archivierung
- Metadaten-Extraktion (Datum, Autor, Teams-Link)

## Verwendung

### HTML-Datei erstellen
```bash
python scripts/format_infobrief.py "pfad/zur/datei.md" --output html
```

### PDF erstellen
```bash
python scripts/format_infobrief.py "pfad/zur/datei.md" --output pdf
```

### Alle Infobriefe im Ordner konvertieren
```bash
python scripts/format_infobrief.py "ordner/" --batch --output html
```

### Vorschau im Browser
```bash
python scripts/format_infobrief.py "datei.md" --preview
```

## Corporate Design Details

**Farben:**
- **Primär Dunkelblau:** #003366 (Header, Footer, Überschriften)
- **Akzent Hellblau:** #00A3E0 (Links, Highlights)
- **Signal Neongelb:** #B5E505 (Wichtige Markierungen, BS05-Branding)
- **Hintergrund Weiß:** #FFFFFF
- **Text Dunkelgrau:** #333333

**Typografie:**
- Überschriften: Sans-Serif (Arial, Helvetica)
- Fließtext: Sans-Serif (Arial, Helvetica)
- Zeilenhöhe: 1.6 für optimale Lesbarkeit

**Layout:**
- Maximale Breite: 800px
- Seitenränder: 40px
- Abschnitte klar getrennt mit visuellen Markern

## Struktur-Erkennung

Der Skill erkennt automatisch:
- **Metadaten:** Datum, Autor, Teams-Link (aus Blockquote am Anfang)
- **Kategorien:** Need-to-know, Nice-to-know (mit visuellen Markern)
- **Listen:** Automatische Formatierung mit Bullet-Points
- **Links:** Teams-Links werden hervorgehoben

---

# blog-article-workflow

---
name: blog-article-workflow
description: Complete workflow for creating and publishing blog articles with Claude AI and WordPress MCP integration. Use when creating educational blog posts, tutorial articles, or documentation that needs to be published to WordPress.
license: MIT
agent: Personal
mcp_servers:
  - wordpress
---

Step-by-step workflow for creating high-quality blog articles from concept to publication, with WordPress automation via MCP.

## MCP Integration (WICHTIG)

**Dieser Skill nutzt den WordPress MCP Server direkt. Verwende immer diese Tools:**

| Tool | Zweck |
|------|-------|
| `wp_upload_media_from_url` | Bild hochladen, gibt Media-ID zurück |
| `wp_create_post` | Neuen Beitrag erstellen (mit `featuredMediaId`) |
| `wp_update_post` | Bestehenden Beitrag aktualisieren |
| `wp_list_posts` | Beiträge auflisten |
| `wp_list_media` | Medien in Bibliothek auflisten |

**Standard-Workflow:**
```
1. wp_upload_media_from_url -> Media-ID erhalten
2. wp_create_post mit featuredMediaId -> Draft erstellen
3. User reviewed in WordPress -> Publish
```

## When to Use This Skill

Use this skill when:
- Creating educational blog posts or tutorials
- Writing technical documentation for publication
- Producing content series for a blog
- Automating WordPress publishing workflows
- Converting ideas/audio/notes into structured articles

## Workflow Overview

### Phase 1: Concept & Structure (5-10 min)
1. Define topic and audience
2. Identify key message/takeaway
3. Create article structure
4. Gather examples/resources

### Phase 2: Content Creation (20-40 min)
1. Write hook/introduction
2. Develop main sections
3. Add practical examples
4. Include visuals/illustrations
5. Write conclusion/call-to-action

### Phase 3: Formatting (5-10 min)
1. Convert to WordPress-compatible HTML
2. Add proper heading hierarchy
3. Format lists, quotes, code blocks
4. Optimize for readability

### Phase 4: Publishing (2-5 min)
1. Upload to WordPress (manual or via MCP)
2. Add featured image
3. Set categories/tags
4. Preview and publish

**Total Time:** 30-60 minutes per article

## Writing Principles

**1. Start with the hook**
- Personal anecdote
- Surprising statistic
- Provocative question
- Common pain point

**Bad:** "In this article, I will explain H5P..."
**Good:** "Last week I created an interactive module in 10 minutes that kept students engaged 3x longer than a PDF worksheet."

**2. Show, don't just tell**
- Use concrete examples
- Include real numbers/data
- Reference actual projects
- Share screenshots/visuals

**3. Write conversationally**
- Use "you" and "I"
- Short paragraphs (2-4 sentences)
- Varied sentence length
- Active voice

## WordPress Formatting

**Headings:**
```html
## Section -> <h2 class="wp-block-heading">
### Subsection -> <h3 class="wp-block-heading">
```

**Paragraphs:**
```html
<!-- wp:paragraph -->
<p>Text here</p>
<!-- /wp:paragraph -->
```

**Lists:**
```html
<!-- wp:list -->
<ul class="wp-block-list">
<li>Item 1</li>
<li>Item 2</li>
</ul>
<!-- /wp:list -->
```

## Publishing via MCP

```javascript
// Step 1: Upload image and get Media-ID
const media = await wp_upload_media_from_url({
  fileUrl: "https://example.com/image.png",
  title: "Article Featured Image",
  altText: "Description for SEO"
});

// Step 2: Create post with Featured Image
wp_create_post({
  title: "Article Title",
  content: articleContent,
  status: "draft",
  featuredMediaId: media.id
});
```

---

*This skill is based on producing 50+ blog articles using this exact workflow.*

---

# recherche-workflow

---
name: recherche-workflow
description: Research workflow for finding well-substantiated contrarian positions. Specialized in anarchist theory, stigmergy, grassroots movements, guerilla gardening, and alternative media. Use when researching topics that benefit from non-mainstream perspectives with academic rigor.
license: MIT
agent: Personal
tools:
  - WebSearch
  - WebFetch
---

Systematischer Workflow zur Recherche von gut untermauerten, nicht-mainstream Perspektiven zu gesellschaftlichen, politischen und kulturellen Themen.

## MCP/Tool Integration (WICHTIG)

**Dieser Skill nutzt folgende Tools direkt:**

| Tool | Zweck |
|------|-------|
| `WebSearch` | Web-Suche nach Quellen, akademischen Papers, Bewegungsliteratur |
| `WebFetch` | Inhalte von URLs abrufen und analysieren |

**Suchstrategien:**
```
WebSearch: "[Thema] site:theanarchistlibrary.org"
WebSearch: "[Thema] anarchist OR commons OR grassroots filetype:pdf"
WebSearch: "[Thema] site:academia.edu"
WebFetch: URL + Prompt zur Inhaltsextraktion
```

## Wann diesen Skill nutzen

- Recherche zu Themen, bei denen Mainstream-Medien blinde Flecken haben
- Suche nach akademisch fundierten alternativen Perspektiven
- Hintergrundrecherche zu Grassroots-Bewegungen, Selbstorganisation, Commons
- Kritische Analyse von Narrativen mit Gegenpositionen
- Quellensammlung für Blog-Artikel oder Dokumentation

## Kernprinzipien

### 1. Substanz vor Sensation
- Bevorzuge peer-reviewed Quellen und akademische Arbeiten
- Priorisiere Primärquellen (Originaltexte, Interviews, Dokumente)
- Prüfe Argumentationsketten, nicht nur Schlussfolgerungen
- Vermeide reine Meinungsblogs ohne Belege

### 2. Quellenvielfalt
- Kombiniere akademische + aktivistische + journalistische Quellen
- Suche bewusst nach Gegenpositionen zur eigenen These
- Nutze internationale Quellen (nicht nur DACH/anglophon)
- Berücksichtige historische Kontexte

### 3. Transparente Einordnung
- Kennzeichne ideologische Standpunkte der Quellen
- Unterscheide Fakten, Interpretationen und Meinungen
- Dokumentiere Limitationen und offene Fragen

## Workflow

### Phase 1: Framing (5 min)

**Fragen klären:**
```
1. Was ist die Mainstream-Position zu diesem Thema?
2. Welche Aspekte werden dabei ausgeblendet oder vereinfacht?
3. Wer profitiert von der dominanten Erzählung?
4. Welche Gegennarrative existieren?
```

### Phase 2: Quellenrecherche (15-30 min)

**Suchstrategie nach Quellentyp:**

#### Akademisch (höchste Priorität für Substanz)
```
- Google Scholar: [Thema] + "anarchist" OR "commons" OR "grassroots"
- Academia.edu: Stigmergy, alternative economics, social movements
- JSTOR/ResearchGate: Peer-reviewed zu spezifischen Theorien
```

#### Bewegungsliteratur (Primärquellen)
```
- The Anarchist Library: theanarchistlibrary.org/search?query=[thema]
- CrimethInc.: crimethinc.com (Analysen, Toolkits)
- libcom.org: Arbeiterbewegung, Syndikalismus
- Fifth Estate Magazine: Langform-Essays seit 1965
```

### Phase 3: Quellenauswertung (20-40 min)

**Für jede relevante Quelle dokumentieren:**

```markdown
## [Titel der Quelle]

**Bibliografie:** [Autor, Jahr, Publikation, URL]
**Kernthese:** [1-2 Sätze]
**Hauptargumente:** [Argument + Beleg]
**Methodik/Evidenz:** [Wie wird argumentiert?]
**Ideologischer Standpunkt:** [Transparent einordnen]
**Stärken:** [Was ist überzeugend?]
**Schwächen/Limitationen:** [Wo greift die Argumentation zu kurz?]
```

## Bewertungskriterien für Quellen

### Hohe Qualität (bevorzugen)
- Peer-reviewed akademische Arbeiten
- Primärquellen (Originaltexte, Manifeste, Interviews)
- Langform-Analysen mit Quellenangaben
- Dokumentierte Fallstudien mit Methodik

### Niedrige Qualität (vermeiden)
- Social-Media-Posts ohne Kontext
- Anonyme Pamphlete ohne Argumentation
- Reine Meinungsstücke ohne Belege
- Verschwörungstheoretische Quellen
- Clickbait und Sensationalismus

---

*Dieser Skill basiert auf den kuratierten Quellen in [[Newsquellen]] und [[feeds]].*

---

# docker-management

---
name: docker-management
description: Manage Docker containers on the Hetzner server. Check status, view logs, restart services, and troubleshoot container issues via SSH.
license: MIT
agent: DevOps
---

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
# SSH Command
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# Or with alias (if configured)
ssh hetzner
```

### Server Details

| Property | Value |
|----------|-------|
| **Host** | 95.217.163.192 |
| **User** | dirk |
| **OS** | Ubuntu LTS 24 |
| **Docker** | Docker Compose v2 |

## Container Overview

| Container | Service | Port | Domain |
|-----------|---------|------|--------|
| traefik | Reverse Proxy | 80, 443 | - |
| n8n | Workflow Automation | 5678 | n8n.dirk-schulenburg.net |
| wordpress | Blog/CMS | - | www.dirk-schulenburg.net |
| moodle | LMS | - | moodle.dirk-schulenburg.net |
| moodle-db | MariaDB | 3306 | - |
| n8n-postgres | PostgreSQL | 5432 | - |
| wp-mcp | WordPress MCP | 8000 | mcp-wp.dirk-schulenburg.net |
| moodle-mcp | Moodle MCP | 8001 | mcp-moodle.dirk-schulenburg.net |
| imap-mcp | IMAP MCP | 8002 | mcp-imap.dirk-schulenburg.net |

## Quick Commands

### Check All Containers

```bash
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Check Specific Container

```bash
# Container status
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker ps -f name=n8n'

# Container logs (last 50 lines)
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker logs n8n --tail 50'
```

### Health Checks

```bash
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  echo "=== MCP Health Checks ==="
  curl -s https://mcp-wp.dirk-schulenburg.net/health && echo " - wp-mcp"
  curl -s https://mcp-moodle.dirk-schulenburg.net/health && echo " - moodle-mcp"
  curl -s https://mcp-imap.dirk-schulenburg.net/health && echo " - imap-mcp"
'
```

## Container Management

### Restart Container

```bash
# Restart single container
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker restart n8n'

# Restart via docker-compose
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/n8n
  docker compose restart
'
```

### Rebuild Container

```bash
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/mcp-servers/wp-mcp
  docker compose down
  docker compose up -d --build
'
```

## Troubleshooting

### Container Won't Start

```bash
# 1. Check logs
docker logs {container} --tail 100

# 2. Check compose config
cd /home/dirk/docker/{service}
docker compose config

# 3. Check ports
netstat -tlnp | grep {port}

# 4. Check disk space
df -h

# 5. Check memory
free -h
```

### Network Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect proxy

# Check container network
docker inspect {container} | grep -A 20 Networks
```

## Resource Management

### Check Resource Usage

```bash
# Live stats
docker stats

# One-time snapshot
docker stats --no-stream
```

### Cleanup Commands

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Full cleanup (unused containers, networks, images)
docker system prune -f
```

## Backup & Restore

### Database Backup

```bash
# PostgreSQL (n8n)
docker exec n8n-postgres pg_dump -U n8n n8n > backup_n8n_$(date +%Y%m%d).sql

# MariaDB (Moodle)
docker exec moodle-db mysqldump -u root -p$MYSQL_ROOT_PASSWORD moodle > backup_moodle_$(date +%Y%m%d).sql
```

---

*DevOps Skill - Docker Management*

---

# mcp-server-deploy

---
name: mcp-server-deploy
description: Deploy MCP servers from local development to production via Git and Docker. Handles code push, SSH deployment, container rebuild, and health verification.
license: MIT
agent: DevOps
---

Complete workflow for deploying MCP servers from local development to the Hetzner production server via Git and Docker.

## When to Use This Skill

Use this skill when:
- Deploying new or updated MCP server code to production
- Setting up a new MCP server from scratch
- Rolling back to a previous version
- Checking deployment status and health

## Prerequisites

### Local Environment
- Git repository: `C:\Users\mail\entwicklung\docker\mcp-servers\{server-name}`
- SSH key: `C:\Users\mail\.ssh\hetzner_ssh_key`

### Server Environment
- **Host:** 95.217.163.192 (Hetzner)
- **User:** dirk
- **Path:** `/home/dirk/docker/mcp-servers/{server-name}`
- **Traefik:** Reverse proxy with auto-SSL

### MCP Servers

| Server | Local Port | Domain | Repo Path |
|--------|------------|--------|-----------|
| wp-mcp | 8000 | mcp-wp.dirk-schulenburg.net | mcp-servers/wp-mcp |
| moodle-mcp | 8001 | mcp-moodle.dirk-schulenburg.net | mcp-servers/moodle-mcp |
| imap-mcp | 8002 | mcp-imap.dirk-schulenburg.net | mcp-servers/imap-mcp |

## Quick Deploy

### One-Liner Deployment

```bash
# WordPress MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/wp-mcp && git pull && docker compose down && docker compose up -d --build'

# Moodle MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/moodle-mcp && git pull && docker compose down && docker compose up -d --build'

# IMAP MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/imap-mcp && git pull && docker compose down && docker compose up -d --build'
```

## Full Deployment Workflow

### Phase 1: Local Development

```bash
# 1. Navigate to project
cd C:\Users\mail\entwicklung\docker\mcp-servers\{server-name}

# 2. Make changes to code

# 3. Local testing
docker compose up --build

# 4. Test endpoint
curl http://localhost:8000/health
```

### Phase 2: Git Commit & Push

```bash
# 1. Stage changes
git add .

# 2. Commit with descriptive message
git commit -m "feat: add new tool moodle_create_quiz"

# 3. Push to remote
git push origin master
```

### Phase 3: Server Deployment

```bash
# 1. SSH to server
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# 2. Navigate to MCP server directory
cd /home/dirk/docker/mcp-servers/{server-name}

# 3. Pull latest code
git pull origin master

# 4. Rebuild and restart container
docker compose down
docker compose up -d --build
```

### Phase 4: Verification

```bash
# 1. Check container status
docker ps | grep mcp

# 2. Health check
curl https://mcp-{name}.dirk-schulenburg.net/health

# 3. View logs (if issues)
docker logs mcp-{name}-1 --tail 100
```

## Rollback Procedure

```bash
# 1. SSH to server
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# 2. Navigate and rollback
cd /home/dirk/docker/mcp-servers/{server-name}
git log --oneline -5  # Find commit to rollback to
git checkout {commit-hash}

# 3. Rebuild
docker compose down && docker compose up -d --build
```

## Commit Message Convention

```
feat: add new feature
fix: bug fix
docs: documentation only
refactor: code refactoring
test: adding tests
chore: maintenance
```

Examples:
- `feat: add moodle_create_quiz tool`
- `fix: handle empty response in wp_list_posts`
- `refactor: extract validation logic`

---

*DevOps Skill - MCP Server Deployment*

---

# n8n-workflow

---
name: n8n-workflow
description: Create, debug, and manage n8n workflows. Use for building automations, analyzing workflow executions, fixing errors, and optimizing performance.
license: MIT
agent: DevOps
---

Complete workflow for creating, debugging, and managing n8n automations.

## When to Use This Skill

Use this skill when:
- Creating new n8n workflows
- Debugging failed workflow executions
- Analyzing workflow performance
- Migrating or copying workflows
- Building integrations between services

## Prerequisites

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `n8n_list_workflows` | List all workflows with status |
| `n8n_get_workflow` | Get workflow details by ID |
| `n8n_get_workflow_structure` | Get nodes and connections only |
| `n8n_create_workflow` | Create new workflow |
| `n8n_update_full_workflow` | Full workflow update |
| `n8n_update_partial_workflow` | Incremental updates (add/remove nodes) |
| `n8n_delete_workflow` | Delete workflow |
| `n8n_list_executions` | List execution history |
| `n8n_get_execution` | Get execution details |
| `n8n_validate_workflow` | Validate workflow structure |
| `n8n_autofix_workflow` | Auto-fix common issues |
| `n8n_trigger_webhook_workflow` | Trigger webhook workflow |

### Access

- **URL:** https://n8n.dirk-schulenburg.net
- **API:** Via n8n MCP Gateway

## Quick Start

### List All Workflows

```javascript
n8n_list_workflows({
  limit: 100,
  active: true
})
```

### Get Workflow Details

```javascript
// Full workflow with parameters
n8n_get_workflow({ id: "123" })

// Structure only (nodes + connections)
n8n_get_workflow_structure({ id: "123" })
```

### Check Executions

```javascript
// Recent executions for a workflow
n8n_list_executions({
  workflowId: "123",
  limit: 10
})

// Get execution details
n8n_get_execution({
  id: "456",
  mode: "summary"
})
```

## Creating Workflows

### Basic Workflow Structure

```javascript
n8n_create_workflow({
  name: "My Automation",
  nodes: [
    {
      id: "trigger-1",
      name: "Webhook Trigger",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [250, 300],
      parameters: {
        path: "my-webhook",
        httpMethod: "POST"
      }
    },
    {
      id: "http-1",
      name: "HTTP Request",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [450, 300],
      parameters: {
        url: "https://api.example.com/data",
        method: "GET"
      }
    }
  ],
  connections: {
    "trigger-1": {
      main: [[{ node: "http-1", type: "main", index: 0 }]]
    }
  }
})
```

### Common Node Types

| Node Type | Use Case |
|-----------|----------|
| `n8n-nodes-base.webhook` | HTTP trigger |
| `n8n-nodes-base.scheduleTrigger` | Cron/interval trigger |
| `n8n-nodes-base.httpRequest` | API calls |
| `n8n-nodes-base.set` | Set/transform data |
| `n8n-nodes-base.if` | Conditional logic |
| `n8n-nodes-base.switch` | Multiple conditions |
| `n8n-nodes-base.code` | Custom JavaScript |
| `n8n-nodes-base.emailSend` | Send emails |
| `n8n-nodes-base.slack` | Slack integration |

## Debugging Workflows

### Step 1: Check Execution History

```javascript
n8n_list_executions({
  workflowId: "123",
  status: "error",
  limit: 5
})
```

### Step 2: Analyze Failed Execution

```javascript
n8n_get_execution({
  id: "456",
  mode: "full",
  includeInputData: true
})
```

### Step 3: Identify Error

Look for:
- **Node that failed:** Check `error` field
- **Input data:** What data reached the failing node
- **Error message:** API errors, validation errors, etc.

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED` | API unreachable | Check URL, network |
| `401 Unauthorized` | Bad credentials | Update API key |
| `undefined` in expression | Missing data | Add null check |
| `Workflow could not be activated` | Missing credentials | Configure credentials |

## Validation & Auto-Fix

### Validate Workflow

```javascript
n8n_validate_workflow({
  id: "123",
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"
  }
})
```

### Auto-Fix Issues

```javascript
// Preview fixes
n8n_autofix_workflow({
  id: "123",
  applyFixes: false
})

// Apply fixes
n8n_autofix_workflow({
  id: "123",
  applyFixes: true,
  confidenceThreshold: "high"
})
```

## Best Practices

### Naming Conventions
- Workflows: `[Category] Description` (e.g., `[Email] Daily Newsletter`)
- Nodes: Descriptive action (e.g., `Fetch User Data`, `Send Slack Alert`)

### Error Handling
- Use `continueOnFail` for non-critical nodes
- Add error workflows for critical processes
- Log errors to external service

### Performance
- Limit data early with filters
- Use pagination for large datasets
- Batch operations when possible

### Security
- Use credentials instead of hardcoded secrets
- Validate webhook input
- Limit webhook exposure (authentication)

---

*DevOps Skill - n8n Workflow Management*

---

## End of Skills Bundle

This bundle contains 13 specialized skills organized by agent domain:

**Education Agent (7 skills):**
- h5p-quiz-to-moodle, h5p-generator, h5p-wordpress-workflow
- moodle-course-workflow, moodle-section-analyzer, moodle-section-optimizer
- lernfeld-zu-moodle-kurs, bswi-infobrief

**Personal Agent (2 skills):**
- blog-article-workflow, recherche-workflow

**DevOps Agent (4 skills):**
- docker-management, mcp-server-deploy, n8n-workflow

For skill invocation, use the Skill tool with the skill name (e.g., `skill: "h5p-generator"`).
