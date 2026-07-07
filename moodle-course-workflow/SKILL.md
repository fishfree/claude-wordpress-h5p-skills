---
name: moodle-course-workflow
description: Kompletter Workflow fuer Moodle-Kurserstellung mit nativer H5P-Integration, Quizzen und interaktiven Inhalten. Nutze wenn Kurse erstellt, H5P-Module eingebunden oder Kursstrukturen automatisiert werden sollen.
license: MIT
---

# Moodle-Kurs Erstellungs-Workflow

Kompletter Workflow fuer Moodle-Kurse mit Abschnitten, Aktivitaeten, Quizzen und H5P-Inhalten.

## Wann diesen Skill nutzen

- Neue Moodle-Kurse programmatisch erstellen
- Interaktive H5P-Inhalte in Moodle einbinden
- Quizze mit verschiedenen Fragetypen erstellen
- Strukturierte Lernmodule mit mehreren Abschnitten aufbauen

## Voraussetzungen

### MCP-Server
- **moodle-mcp** (mcp-moodle.dirk-schulenburg.net) — 73 Tools fuer Kursverwaltung

### Moodle-Plugins (auf Server installiert)
- `local_sync_service` — Label, Page, URL, Resource, Quiz erstellen
- `local_h5p_api` — H5P Upload, Embed, Activity
- `local_wsmanagesections` — Abschnittsverwaltung via API

## Quick Start

### Minimaler Kurs (3 Schritte)

```
1. moodle_create_course → Kurs anlegen
2. moodle_update_section → Abschnitte benennen
3. moodle_create_label / moodle_create_page → Inhalte hinzufuegen
```

### Kurs mit H5P + Quiz (5 Schritte)

```
1. moodle_create_course → Kurs anlegen
2. moodle_update_section → Abschnitte benennen
3. moodle_create_label → Strukturelemente (HTML/JS)
4. moodle_upload_h5p + moodle_create_h5p_activity → Interaktive Inhalte
5. moodle_create_quiz + moodle_add_quiz_question_* → Pruefungen
```

## Verfuegbare MCP-Tools

### Kurs-Verwaltung

| Tool | Beschreibung |
|------|-------------|
| `moodle_create_course` | Kurs erstellen (fullname, shortname, categoryid) |
| `moodle_update_course` | Kurs aktualisieren |
| `moodle_delete_course` | Kurs loeschen |
| `moodle_list_courses` | Alle Kurse auflisten |
| `moodle_list_categories` | Kategorien auflisten |
| `moodle_create_category` | Neue Kategorie erstellen |

### Abschnitte

| Tool | Beschreibung |
|------|-------------|
| `moodle_create_section` | Neuen Abschnitt erstellen |
| `moodle_update_section` | Abschnitt umbenennen/bearbeiten |
| `moodle_get_course_contents` | Kursstruktur anzeigen |

### Inhalte erstellen

| Tool | Beschreibung |
|------|-------------|
| `moodle_create_label` | HTML/JS-Label (inline im Kurs) |
| `moodle_create_page` | Seite mit HTML-Inhalt |
| `moodle_create_url` | URL-Ressource |
| `moodle_create_resource` | Datei-Ressource |
| `moodle_create_folder` | Ordner-Ressource |
| `moodle_update_label` | Label aktualisieren |
| `moodle_update_page` | Seite aktualisieren |
| `moodle_update_url` | URL aktualisieren |

### Inhalte verwalten

| Tool | Beschreibung |
|------|-------------|
| `moodle_get_module` | Modul-Details abrufen |
| `moodle_delete_module` | Modul loeschen |
| `moodle_duplicate_module` | Modul duplizieren |
| `moodle_move_module` | Modul in anderen Abschnitt verschieben |
| `moodle_reorder_modules` | Module innerhalb eines Abschnitts sortieren |

### H5P (nativer Moodle-H5P)

| Tool | Beschreibung |
|------|-------------|
| `moodle_upload_h5p` | H5P-Datei nach Moodle hochladen |
| `moodle_create_h5p_activity` | H5P-Aktivitaet im Kurs erstellen |
| `moodle_list_h5p` | H5P-Inhalte auflisten |
| `moodle_get_h5p_embed` | Embed-Code fuer H5P abrufen |
| `moodle_get_h5p_results` | H5P-Ergebnisse abrufen |
| `moodle_get_h5p_user_attempts` | Nutzer-Versuche anzeigen |

### Quizze

| Tool | Beschreibung |
|------|-------------|
| `moodle_create_quiz` | Quiz erstellen |
| `moodle_update_quiz` | Quiz aktualisieren |
| `moodle_list_quizzes` | Quizze im Kurs auflisten |
| `moodle_add_quiz_question_multichoice` | Multiple-Choice-Frage |
| `moodle_add_quiz_question_truefalse` | Wahr/Falsch-Frage |
| `moodle_add_quiz_question_shortanswer` | Kurzantwort-Frage |
| `moodle_add_quiz_question_numerical` | Numerische Frage |
| `moodle_add_quiz_question_matching` | Zuordnungs-Frage |
| `moodle_add_quiz_question_essay` | Essay-Frage |
| `moodle_add_quiz_question_description` | Beschreibungs-Element |
| `moodle_bulk_add_questions` | Mehrere Fragen auf einmal |
| `moodle_import_gift` | GIFT-Format importieren |
| `moodle_quiz_add_random_questions` | Zufallsfragen aus Fragenpool |

### Nutzer-Verwaltung

| Tool | Beschreibung |
|------|-------------|
| `moodle_enrol_user` | Nutzer einschreiben |
| `moodle_list_enrolled_users` | Eingeschriebene Nutzer auflisten |
| `moodle_get_grades` | Noten abrufen |

### BigBlueButton (Videokonferenz)

| Tool | Beschreibung |
|------|-------------|
| `moodle_bbb_get_join_url` | BBB-Beitritts-URL |
| `moodle_bbb_meeting_info` | Meeting-Info |
| `moodle_bbb_get_recordings` | Aufnahmen auflisten |

## H5P-Workflow (nativ in Moodle)

### H5P-Datei erstellen und einbinden

```
1. H5P-Datei generieren (h5p-generator Skill)
   → Erzeugt .h5p Datei lokal

2. moodle_upload_h5p
   → Laedt .h5p Datei nach Moodle hoch
   → Gibt content_id zurueck

3. moodle_create_h5p_activity
   → Erstellt H5P-Aktivitaet im Kurs
   → Verknuepft mit content_id
```

### H5P als Embed in Label/Page

```
1. moodle_upload_h5p → content_id erhalten
2. moodle_get_h5p_embed → Embed-Code abrufen
3. moodle_create_label oder moodle_create_page
   → Embed-Code als HTML einbetten
```

## Quiz-Workflow

### KRITISCH: quiz_sections

Nach Quiz-Erstellung MUSS eine `quiz_sections` Zeile existieren, sonst "No questions found" Fehler. Die MCP-Tools machen das automatisch, aber bei manueller Erstellung:

```php
$section = new \stdClass();
$section->quizid = $instance->id;
$section->firstslot = 1;
$section->heading = '';
$section->shufflequestions = 0;
$DB->insert_record('quiz_sections', $section);
```

### GIFT-Format Import

Schnellste Methode fuer viele Fragen:

```
// Multiple Choice
::Frage 1::Was ist Cannabis?{
  =Eine Pflanze
  ~Ein Mineral
  ~Ein Tier
}

// Wahr/Falsch
::Frage 2::Cannabis gehoert zur Familie Cannabaceae.{TRUE}

// Kurzantwort
::Frage 3::Wie heisst der psychoaktive Wirkstoff?{=THC =Tetrahydrocannabinol}
```

## Umlaute als HTML-Entities

**PFLICHT in allen Moodle-MCP Inhalten:**

| Zeichen | Entity |
|---------|--------|
| &auml; &ouml; &uuml; | `&auml;` `&ouml;` `&uuml;` |
| &Auml; &Ouml; &Uuml; | `&Auml;` `&Ouml;` `&Uuml;` |
| &szlig; | `&szlig;` |

## Workflow-Muster

### Muster 1: Schnelles Modul

**Anwendung:** Einzelne Aktivitaet in bestehendem Kurs

```
1. moodle_get_course_contents → Struktur pruefen
2. moodle_create_label / moodle_create_page → Inhalt hinzufuegen
```

### Muster 2: Kompletter Kursbau

**Anwendung:** Neuer Kurs von Grund auf

```
1. moodle_create_course → Kurs anlegen
2. Loop: moodle_update_section → Abschnitte benennen
3. Loop: moodle_create_label/page/url → Inhalte hinzufuegen
4. moodle_create_quiz + Fragen → Pruefungen
5. moodle_upload_h5p + moodle_create_h5p_activity → Interaktiv
6. moodle_enrol_user → Teilnehmer einschreiben
```

### Muster 3: Interaktive Labels (JS-Komponenten)

**Anwendung:** Inline-Interaktivitaet ohne H5P

Labels koennen HTML + JavaScript enthalten. Gut fuer:
- Mini-Quizze (Self-Check)
- Akkordeon-Elemente
- Flashcards
- Drag-and-Drop

Siehe `moodle-section-optimizer` Skill fuer JS-Templates.

## Best Practices

### Kursstruktur
- Abschnittsnamen kurz und konsistent: "Modul X: Thema"
- Section Summaries fuer Navigation nutzen
- Max 5-7 Aktivitaeten pro Abschnitt

### H5P
- Nativer Moodle-H5P bevorzugen (nicht WordPress-Embed)
- Library-Versionen pruefen (muessen zu Moodle passen)
- Max 2-3 H5P pro Seite (Performance)

### Quizze
- `moodle_bulk_add_questions` fuer effizienten Massenimport
- `moodle_import_gift` fuer textbasierte Fragenerstellung
- Quiz-Cache leeren nach Aenderungen: `moodle_purge_caches` oder via CLI

---

*Education Skill - Moodle Course Workflow v2.0 (2026-03-12)*
