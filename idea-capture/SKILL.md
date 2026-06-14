---
name: idea-capture
description: Quickly capture ideas, notes, and thoughts. Content/post ideas for the "Offene KI-Werkstatt" LinkedIn series route into the LinkedIn idea-backlog; everything else goes to the Obsidian vault. Auto-categorizes, suggests tags/format, and links related notes. Use when the user has a quick thought, post idea, or content angle to save.
license: MIT
allowed-tools:
  - Write
  - Read
  - Edit
  - Glob
---

# Idea-Capture Skill

Schnelle Erfassung von Ideen und Notizen in den Obsidian Vault mit automatischer Kategorisierung und Verlinkung.

## Tool Integration

**Dieser Skill nutzt folgende Tools:**

| Tool | Zweck |
|------|-------|
| `Write` | Notiz-Datei erstellen |
| `Read` | Bestehende Notizen lesen für Verlinkung |
| `Glob` | Ähnliche Notizen finden |

**Ziel-Verzeichnis:**
```
C:\Users\mail\entwicklung\_DEV_DOCS\_DEV_DOCS\
├── Inbox/          # Neue, unsortierte Ideen
├── Ideas/          # Ausgearbeitete Ideen
├── Projects/       # Projektbezogene Notizen
├── Sessions/       # Debugging/Work Sessions
└── Quick/          # Schnellnotizen
```

---

## Wann diesen Skill nutzen

**Allgemeine Ideen → Obsidian-Vault:**
- "Notiere: [Idee]"
- "Merke dir: [Gedanke]"
- "Schnelle Notiz: [Text]"
- "Ich hab eine Idee: [Beschreibung]"
- "Speichere das für später"
- "Das will ich nicht vergessen: [X]"

**Content-/Post-Ideen → LinkedIn-Backlog:**
- "Content-Idee: [X]" / "Post-Idee: [X]"
- "Werkstatt-Idee: [X]" / "Folge-Idee: [X]"
- "Darüber könnte ich (mal) posten: [X]"
- "Für die [Offene KI-]Werkstatt: [X]" / "Für LinkedIn: [X]"
- "Nächste Folge könnte sein: [X]"

---

## Phase 0: Routing — Content-Idee oder Vault?

**ZUERST entscheiden, WOHIN die Idee gehört.** Das bestimmt den gesamten weiteren Ablauf.

```
Content-/Post-Idee?  →  LinkedIn-Backlog  (siehe Abschnitt „Content-Ideen → LinkedIn-Backlog")
sonst                →  Obsidian-Vault    (Phase 1–4 unten)
```

**Content-Idee erkennen** (eines reicht):
- Expliziter Trigger (Content-/Post-/Werkstatt-/Folge-Idee, „für LinkedIn", „darüber posten").
- Inhalt ist etwas, das Dirk **gebaut** hat und öffentlich zeigbar wäre (Tool, Modul, Automatisierung, Artefakt).
- Inhalt ist eine **These/Beobachtung** aus Innensicht, die als Build-in-Public-Post taugt.
- Bezug zu „KI als Mitarbeiter", „hyper-individuelle Commons", Bildung/Selbstständigkeit als Erzählung.

Im Zweifel kurz nachfragen: „Eher ein Werkstatt-Post oder eine Vault-Notiz?"

---

## Content-Ideen → LinkedIn-Backlog

Für die Serie **„Offene KI-Werkstatt"** (Build-in-Public, fester Sonntagspost). Content-Ideen werden NICHT in den Vault geschrieben, sondern in den Backlog — dort sind sie beim Sonntags-Review sofort sichtbar.

**Ziel-Datei:**
```
C:\Users\mail\entwicklung\docker\business\linkedin\IDEEN-backlog.md
```

**Ablauf:**
1. `Read` die Backlog-Datei.
2. Format vorschlagen (Regel: **Das Format folgt der Pointe**):

   | Pointe der Idee | Format |
   |-----------------|--------|
   | Bewegung, Animation, etwas „in Aktion" | **Video** |
   | UI/Welt/Artefakt zum Durchblättern, mehrere Schritte | **Carousel** |
   | Reine These, Beobachtung, Reaktion auf Debatte | **Text** |

3. `Edit`: den neuen Eintrag direkt **unter** der Zeile `<!-- neue Einträge hier darunter anhängen -->` (Abschnitt „📥 Inbox") einfügen. Eintragsformat:
   ```
   - **<Kurztitel>** — <Idee in 1 Satz>. Winkel: <warum interessant / Anschluss an These>. Format: <Video|Carousel|Text>. _(erfasst <YYYY-MM-DD>)_
   ```
4. Bestätigen:
   ```
   ✅ In den Werkstatt-Backlog gelegt (Inbox)

   **Eintrag:** <der Bullet>
   **Format-Vorschlag:** <X> — <ein Halbsatz Begründung>

   Liegt bereit fürs Sonntags-Review. Sag „lass uns den Sonntagspost machen", dann ziehen wir einen raus.
   ```

**Wichtig:**
- Bei Content-Ideen **nur** den Backlog beschreiben, NICHT zusätzlich den Vault (keine Doppelablage).
- `created`/Datum NICHT raten — aktuelles Datum aus dem Session-Kontext nehmen.
- Stimme der Serie (für den Winkel mitdenken): peer-respektvoll, systemkritisch aus Innensicht, ehrlich auch über das, „woran es klemmt".
- Hintergrund/Kadenz: das Memory `project-offene-ki-werkstatt-linkedin` und der Kopf der Backlog-Datei.

---

## Workflow

### Phase 1: Input erfassen

**Eingabetypen:**

| Typ | Trigger | Beispiel |
|-----|---------|----------|
| Quick | "Notiere:", "Merke:" | Kurzer Gedanke |
| Idea | "Idee:", "Ich hab eine Idee" | Ausführlichere Idee |
| Todo | "Todo:", "Ich muss noch" | Aufgabe |
| Link | "Interessanter Link:" | URL mit Kontext |
| Quote | "Zitat:", "Merken:" | Text zum Merken |

### Phase 2: Kategorisierung

**Automatische Erkennung:**

```javascript
const CATEGORIES = {
  // Nach Keywords
  'code': ['bug', 'feature', 'refactor', 'api', 'function'],
  'content': ['artikel', 'blog', 'video', 'tutorial'],
  'tool': ['tool', 'app', 'software', 'service'],
  'learning': ['lernen', 'kurs', 'buch', 'studieren'],
  'project': ['projekt', 'idee', 'konzept', 'plan'],

  // Nach Kontext
  'education': ['moodle', 'h5p', 'schule', 'unterricht'],
  'devops': ['server', 'docker', 'deploy', 'mcp'],
  'personal': ['blog', 'privat', 'familie']
};
```

### Phase 3: Notiz erstellen

**Standard-Template:**

```markdown
---
created: {{date}}
type: {{type}}
status: inbox
tags: [{{tags}}]
related: []
---

# {{title}}

{{content}}

---

## Kontext
- Erfasst: {{datetime}}
- Quelle: Claude Code Conversation

## Nächste Schritte
- [ ] Ausarbeiten
- [ ] Einordnen
- [ ] Verlinken
```

**Dateiname-Format:**
```
{{YYYY-MM-DD}}-{{slug}}.md

Beispiel: 2026-02-03-mcp-server-idee.md
```

### Phase 4: Verlinkung

**Ähnliche Notizen finden:**

```javascript
// Nach Tags suchen
Glob({ pattern: "_DEV_DOCS/**/*.md" })
// → Dateien mit ähnlichen Tags identifizieren

// Backlinks vorschlagen
const related = findRelated(content, existingNotes);
```

**Output:**

```markdown
✅ Notiz gespeichert!

**Datei:** `_DEV_DOCS/Inbox/2026-02-03-mcp-server-idee.md`

**Vorgeschlagene Verlinkungen:**
- [[MCP-Server-Architektur]] (Tag: mcp)
- [[DevOps-Roadmap]] (Tag: server)

Soll ich die Links hinzufügen?
```

---

## Notiz-Templates

### Quick Note

```markdown
---
created: 2026-02-03
type: quick
status: inbox
tags: []
---

# Quick Note

{{content}}
```

### Idea

```markdown
---
created: 2026-02-03
type: idea
status: inbox
tags: [idea]
priority: medium
---

# {{title}}

## Idee
{{content}}

## Warum interessant?
[Automatisch oder manuell ergänzen]

## Mögliche Umsetzung
- [ ] Schritt 1
- [ ] Schritt 2

## Ressourcen
-
```

### Todo

```markdown
---
created: 2026-02-03
type: todo
status: open
tags: [todo]
due:
priority: medium
---

# TODO: {{title}}

## Aufgabe
{{content}}

## Kontext
[Warum ist das wichtig?]

## Schritte
- [ ]
```

### Link/Resource

```markdown
---
created: 2026-02-03
type: resource
status: inbox
tags: [link, resource]
url: {{url}}
---

# {{title}}

## Link
{{url}}

## Warum interessant?
{{context}}

## Notizen
[Ergänzen nach dem Lesen]

## Zitate
>
```

### Quote

```markdown
---
created: 2026-02-03
type: quote
status: inbox
tags: [quote]
source:
---

# Quote: {{short_title}}

> {{quote}}

— {{source}}

## Kontext
{{why_relevant}}

## Verwandte Gedanken
-
```

---

## Tag-Vorschläge

### Automatische Tags

| Keyword in Content | Vorgeschlagener Tag |
|-------------------|---------------------|
| MCP, Server | #devops, #mcp |
| Moodle, H5P | #education, #lms |
| Blog, Artikel | #content, #writing |
| Idee, Konzept | #idea, #brainstorm |
| Bug, Fix | #code, #debugging |
| Tool, App | #tools, #software |
| Buch, Lernen | #learning, #reading |

### Kontext-Tags

| Aktueller Kontext | Tags |
|-------------------|------|
| education | #education, #teaching |
| devops | #devops, #infrastructure |
| personal | #personal, #life |

---

## Obsidian-Integration

### Dateipfade

```javascript
const PATHS = {
  inbox: '_DEV_DOCS/_DEV_DOCS/Inbox/',
  ideas: '_DEV_DOCS/_DEV_DOCS/Ideas/',
  todos: '_DEV_DOCS/_DEV_DOCS/Tasks/',
  resources: '_DEV_DOCS/_DEV_DOCS/Resources/',
  quick: '_DEV_DOCS/_DEV_DOCS/Quick/'
};
```

### Frontmatter-Schema

```yaml
# Pflichtfelder
created: YYYY-MM-DD
type: quick|idea|todo|resource|quote
status: inbox|active|done|archived

# Optional
tags: [tag1, tag2]
priority: low|medium|high
due: YYYY-MM-DD
related: [[Note1]], [[Note2]]
source: URL oder Referenz
```

### Verlinkung

```markdown
# Interne Links
[[Andere Notiz]]
[[Ordner/Notiz]]

# Tags
#tag-name

# Backlinks werden automatisch von Obsidian erkannt
```

---

## Beispiel-Session

**User:** "Notiere: Idee für einen n8n Workflow der automatisch Meeting-Protokolle erstellt"

**Claude:**

1. Input analysieren:
   - Typ: idea
   - Thema: n8n, Workflow, Meeting-Protokolle
   - Kontext: devops

2. Notiz erstellen:

```markdown
---
created: 2026-02-03
type: idea
status: inbox
tags: [idea, n8n, automation, meetings]
priority: medium
---

# Meeting-Protokoll Workflow

## Idee
n8n Workflow der automatisch Meeting-Protokolle erstellt

## Warum interessant?
- Zeitersparnis bei Dokumentation
- Konsistente Protokoll-Formate
- Integration mit Kalender möglich

## Mögliche Umsetzung
- [ ] Voice-MCP für Transkription nutzen
- [ ] Claude für Zusammenfassung
- [ ] Output als Markdown oder Email

## Ressourcen
- [[Voice-MCP]] für Audio-Verarbeitung
- [[n8n-Workflows]] für Beispiele
```

3. Speichern:
```javascript
Write({
  file_path: "_DEV_DOCS/_DEV_DOCS/Inbox/2026-02-03-meeting-protokoll-workflow.md",
  content: noteContent
})
```

4. Bestätigung:
```
✅ Idee gespeichert!

**Datei:** `Inbox/2026-02-03-meeting-protokoll-workflow.md`

**Tags:** #idea #n8n #automation #meetings

**Verwandte Notizen gefunden:**
- [[Voice-MCP]]
- [[n8n-Workflows]]

Soll ich die Idee weiter ausarbeiten?
```

---

## Best Practices

### Do

- Ideen sofort erfassen, später sortieren
- Tags sparsam aber konsistent verwenden
- Kurze, beschreibende Titel wählen
- Kontext mitliefern (warum interessant?)

### Don't

- Zu viel Zeit mit Formatierung verbringen
- Ideen "für später" merken wollen
- Komplexe Hierarchien erstellen
- Alles taggen

---

## Inbox-Workflow

### Tägliche Review (2 min)

```
1. Inbox öffnen
2. Neue Notizen durchgehen
3. Entweder:
   - Ausarbeiten → Ideas/Projects
   - Als Todo markieren → Tasks
   - Archivieren
   - Löschen
```

### Wöchentliche Review

```
1. Alle Inbox-Items durchgehen
2. Ideas priorisieren
3. Todos aktualisieren
4. Verwaiste Notizen verlinken
```

---

## Verwandte Skills

- **recherche-workflow**: Ideen vertiefen und recherchieren
- **blog-article-workflow**: Ideen zu Artikeln ausarbeiten

---

*Zuletzt aktualisiert: 14.06.2026*
*Version: 2.0 - Content-Routing: Post-Ideen → LinkedIn-Backlog (Offene KI-Werkstatt), sonst Obsidian-Vault*
