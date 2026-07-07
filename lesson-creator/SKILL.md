---
name: lesson-creator
description: Erstellt komplette Unterrichtsmaterialien für Lernsituationen mit HTML-Arbeitsblättern, H5P-Inhalten, Excel-Vorlagen und Moodle-Integration. Nutze diesen Skill wenn du eine neue Lernsituation aufbauen, Arbeitsblätter mit echten Eingabefeldern erstellen, oder H5P-Quizze generieren möchtest.
---

# Lesson Creator

Erstellt vollständige Unterrichtsmaterialien für berufliche Lernsituationen mit modernem HTML-Design, interaktiven H5P-Elementen und Moodle-Integration.

## Wann nutzen

- Neue Lernsituation aus einem Lernfeld erstellen
- Arbeitsblätter mit echten Eingabefeldern (Input/Textarea) generieren
- H5P-Quizze und interaktive Elemente erstellen
- Excel-Vorlagen für Berechnungen
- Übersichtsseiten mit Navigation
- Material in Moodle-Kurs hochladen

## Output-Struktur

```
lesson-creator/output/[LF]_[LS]/
├── index.html                    # Übersichtsseite mit Links
├── [Nr]a_[Einstieg].html        # Problemsituation
├── [Nr]b_Dossier_[Thema].html   # Infomaterial
├── [Nr]c_UEB_[Thema].html       # Übungsaufgaben
├── [Nr]d_[Fallmaterial].html    # Fallstudie/Angebote
├── [Nr]e_[Arbeitsblatt].html    # Arbeitsblatt
├── ...
├── [Nr]k_Checkliste.html        # Selbstcheck
├── h5p/
│   ├── *.h5p                    # H5P-Dateien
│   └── upload_all_h5p.ps1       # Batch-Upload-Script
└── excel/
    ├── *.xlsx                   # Excel-Vorlagen
    └── create_excel_templates.py
```

## HTML-Arbeitsblatt-Pattern

### Grundstruktur mit Eingabefeldern

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>[Titel]</title>
    <style>
        @page { size: A4; margin: 1.5cm; }
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 15px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            border-bottom: 2px solid #003366;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        .header h1 { color: #003366; font-size: 13pt; margin: 0; }

        /* Eingabefelder */
        input[type="text"] {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px 6px;
            font-size: 10pt;
            background: #fffef0;
            text-align: center;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #0077b6;
            background: #fff;
        }
        .name-input {
            border: none;
            border-bottom: 1px solid #333;
            background: transparent;
            width: 150px;
        }

        /* Tabellen */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #333;
            padding: 6px 8px;
        }
        th {
            background: #003366;
            color: white;
        }
        .input-cell {
            background: white;
            padding: 3px;
        }
        .input-cell input[type="text"] {
            width: 90%;
        }

        /* Info-Boxen */
        .info-box {
            background: #e8f4f8;
            border-left: 4px solid #0077b6;
            padding: 10px;
            margin: 10px 0;
        }
        .tip-box {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 10px;
            margin: 10px 0;
        }
        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin: 10px 0;
        }

        /* Page Sections für Print */
        .page-section {
            margin-bottom: 20px;
        }

        /* ===== PRINT STYLES ===== */
        @media print {
            body { padding: 0; margin: 0 auto; }

            .page-section.page-break-after {
                page-break-after: always;
            }

            /* Farben erhalten */
            th, .info-box, .tip-box, .warning-box {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            /* Eingabefelder für Print */
            input[type="text"], textarea {
                border: none !important;
                border-bottom: 1px solid #333 !important;
                background: transparent !important;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>[Titel]</h1>
        <div style="text-align: right; font-size: 9pt;">
            [LF] [LS] | Station [N]<br>
            Name: <input type="text" class="name-input" placeholder="">
        </div>
    </div>

    <!-- Inhalt hier -->

</body>
</html>
```

### Eingabefeld-Typen

| Typ | HTML | Verwendung |
|-----|------|------------|
| Kurzer Text | `<input type="text" placeholder="0,00 EUR">` | Zahlen, kurze Antworten |
| Langer Text | `<textarea placeholder="..."></textarea>` | Berechnungen, Begründungen |
| In Tabelle | `<td class="input-cell"><input type="text"></td>` | Vergleichstabellen |
| Name/Datum | `<input type="text" class="name-input">` | Header |

### Page Breaks für PDF

```html
<!-- Erste Seite -->
<div class="page-section page-break-after">
    <h2>Schritt 1</h2>
    ...
</div>

<!-- Zweite Seite -->
<div class="page-section page-break-after">
    <h2>Schritt 2</h2>
    ...
</div>

<!-- Letzte Seite (kein break) -->
<div class="page-section">
    <h2>Ergebnis</h2>
    ...
</div>
```

## Material-Typen

| Nr-Suffix | Typ | Beschreibung | Template |
|-----------|-----|--------------|----------|
| a | Einstieg | Problemsituation, E-Mail, Auftrag | Mail, Memo |
| b, f | Dossier | Infomaterial, Fachtexte | Info-Box, Definitionen |
| c, j | Übung | Aufgaben mit Eingabefeldern | Input-Tabellen |
| d | Fallmaterial | Angebote, Belege, Dokumente | Tabellen |
| e, g | Arbeitsblatt | Strukturierte Aufgaben | Kalkulations-Tabellen |
| h | Vorlage | Templates zum Ausfüllen | Formular |
| i | Bewertung | Kriterienkatalog | Bewertungstabelle |
| k | Checkliste | Selbsteinschätzung | Checkbox-Liste |

## H5P-Integration

### H5P-Dateien generieren

Nutze den `h5p-generator` Skill:

```python
from h5p_generator import create_multi_choice, create_drag_drop, THEMES

# Quiz
result = create_multi_choice(
    "Bezugskalkulation: Wissensfragen",
    questions=[
        {
            "question": "Was ist der Zieleinkaufspreis?",
            "answers": [
                {"text": "Listenpreis minus Rabatt", "correct": True},
                {"text": "Bareinkaufspreis plus Skonto", "correct": False},
            ]
        }
    ],
    "bezugskalkulation_quiz",
    style=THEMES['education']
)
```

### H5P nach Moodle hochladen

```powershell
# Einzelne Datei
$base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes('quiz.h5p'))

# Via MCP
moodle_upload_h5p:
  base64data: $base64
  filename: "quiz.h5p"
  title: "Quiz-Titel"
  courseid: 13

# Dann Aktivität erstellen
moodle_create_h5p_activity:
  courseid: 13
  sectionnum: 7
  contentid: [CONTENT_ID aus Upload]
  name: "Quiz-Titel"
```

### Batch-Upload Script

```powershell
# upload_all_h5p.ps1
$API_KEY = 'YOUR_KEY'
$COURSE_ID = 13
$MCP_URL = 'https://mcp-moodle.dirk-schulenburg.net/mcp/rpc'

$h5pFiles = @(
    @{ file = 'quiz.h5p'; title = 'Quiz-Titel' },
    @{ file = 'flashcards.h5p'; title = 'Lernkarten' }
)

foreach ($h5p in $h5pFiles) {
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($h5p.file))
    # ... API-Aufruf
}
```

## Excel-Vorlagen

### Template-Script

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

def create_template():
    wb = Workbook()
    ws = wb.active
    ws.title = "Vorlage"

    # Header
    header_fill = PatternFill(start_color="003366", fill_type="solid")
    for col, header in enumerate(["A", "B", "C"], 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)

    wb.save("Vorlage.xlsx")
```

## Index-Seite

Die `index.html` enthält:

1. **Header** mit Metadaten (Lernfeld, Zeit, Ausbildungsjahr)
2. **Ausgangssituation** mit Lernzielen
3. **Phasen** als Karten mit Material-Links
4. **H5P-Hinweise** (in Moodle)
5. **Footer** mit Moodle-Link

### Material-Karten

```html
<a href="05c_UEB_Bezugskalkulation.html" class="material-card">
    <span class="type type-uebung">Übung</span>
    <h4>05c: Übungen Bezugskalkulation</h4>
    <p>Praktische Übungsaufgaben mit Eingabefeldern</p>
</a>
```

### Typ-Badges

```css
.type-info { background: #e3f2fd; color: #1565c0; }
.type-uebung { background: #e8f5e9; color: #2e7d32; }
.type-arbeitsblatt { background: #fff3e0; color: #ef6c00; }
.type-fallmaterial { background: #fce4ec; color: #c2185b; }
.type-bewertung { background: #f3e5f5; color: #7b1fa2; }
.type-checkliste { background: #e0f2f1; color: #00796b; }
```

## Moodle-Integration

### Kursabschnitt erstellen

```
1. moodle_create_section (optional, falls neuer Abschnitt)
2. moodle_create_label (Phasen-Überschriften)
3. moodle_create_page (HTML-Inhalte als Page)
4. moodle_upload_h5p + moodle_create_h5p_activity (interaktive Elemente)
```

### ⚠️ KRITISCH: Umlaute als HTML-Entities

Bei allen Moodle MCP Aufrufen:

| Zeichen | Entity |
|---------|--------|
| ä | `&auml;` |
| ö | `&ouml;` |
| ü | `&uuml;` |
| ß | `&szlig;` |
| Ä | `&Auml;` |
| Ö | `&Ouml;` |
| Ü | `&Uuml;` |

## Workflow: Neue Lernsituation

### Schritt 1: Planung

```yaml
lernsituation:
  lernfeld: LF02
  ls_nummer: 05
  titel: "Angebote vergleichen"
  zeitrichtwert: 12 UStd
  modellunternehmen: "Jungkuhn GmbH"

phasen:
  - name: "Einstieg"
    material: [05a_Mail]
  - name: "Erarbeitung"
    material: [05b_Dossier, 05c_UEB]
  ...
```

### Schritt 2: HTML-Materialien erstellen

1. Ordner anlegen: `output/LF02_LS05/`
2. HTML-Dateien mit Eingabefeldern
3. Print-Styles mit Page Breaks
4. Einheitliches Corporate Design

### Schritt 3: H5P generieren

1. Fragen/Inhalte definieren
2. `h5p-generator` Skill nutzen
3. Dateien in `h5p/` Ordner

### Schritt 4: Excel-Vorlagen

1. Python-Script für Vorlagen
2. Formeln und Formatierung
3. In `excel/` Ordner

### Schritt 5: Index-Seite

1. `index.html` mit allen Links
2. Phasen-Struktur
3. H5P-Verweise

### Schritt 6: Moodle-Upload

1. H5P-Dateien hochladen
2. Activities erstellen
3. Pages/Labels anlegen

## Beispiel-Projekte

| Projekt | Pfad | Beschreibung |
|---------|------|--------------|
| LF02 LS05 | `output/LF02_LS05/` | Angebotsvergleich (vollständig) |

## Abhängigkeiten

| Skill/Tool | Verwendung |
|------------|------------|
| `h5p-generator` | H5P-Dateien erstellen |
| `moodle-mcp` | Upload nach Moodle |
| `openpyxl` | Excel-Vorlagen |

## Referenzen

- [[LF02-LS05-Angebotsvergleich]] - Beispiel-Dokumentation
- [[Moodle-H5P-API-Plugin]] - H5P-Upload-API
- [[h5p-generator]] - H5P-Generator Skill

---

*Skill Version: 1.1*
*Erstellt: 2026-02-02, aktualisiert: 2026-03-12*
*Basiert auf: LF02 LS05 Angebotsvergleich*
*Font/Radius an BS:WI Corporate Design angepasst (Arial, 4px)*
