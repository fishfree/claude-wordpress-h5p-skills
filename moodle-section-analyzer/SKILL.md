---
name: moodle-section-analyzer
description: Analysiert Moodle-Kursabschnitte auf 4K-Defizite, Storytelling, Gamification und Interaktivität. Empfiehlt HTML5/CSS/JS/React-Komponenten als Standard, H5P nur auf Anweisung. Nutze wenn Lehrer einen Kurs modernisieren, mehr Engagement erreichen oder didaktisch aufwerten wollen.
license: MIT
version: "2.0"
date: 2026-03-12
---

# Moodle Section Analyzer v2.0

Analysiert Moodle-Abschnitte und identifiziert Optimierungspotenzial nach modernen didaktischen Prinzipien: 4K, Storytelling, Gamification, Interaktivität.

**Paradigma:** HTML5/CSS/JS/React-Komponenten sind Standard. H5P nur auf explizite Anweisung oder wenn technisch überlegen (z.B. Interactive Video, xAPI-Tracking).

## Wann nutzen

- Bestehenden Moodle-Kurs modernisieren
- 4K-Defizite systematisch identifizieren
- Storytelling und Gamification bewerten
- Vor Einsatz des `moodle-section-optimizer` Skills
- Qualitätscheck für E-Learning-Inhalte

## Voraussetzungen

- **MCP Server**: moodle-mcp mit `moodle_get_course_contents`, `moodle_get_page`, `moodle_get_label`
- **Kurs-ID**: Muss bekannt sein

---

## Analyse-Framework (6 Dimensionen)

### 1. 4K-Kompetenzmodell

| K | Beschreibung | Starke Indikatoren | Schwache Indikatoren |
|---|--------------|-------------------|---------------------|
| **Kreativität** | Eigene Lösungen entwickeln | Offene Aufgaben, Drag&Drop-Builder, Sandbox-Tools | Nur Multiple Choice |
| **Kritisches Denken** | Analysieren, Bewerten | Entscheidungssimulationen, Vergleichstools, Szenario-Analyse | Nur Lückentexte |
| **Kommunikation** | Ideen austauschen | Peer-Review, Rollenspiel-Szenarien, Präsentationen | Nur Forendiskussion |
| **Kollaboration** | Zusammenarbeiten | Gemeinsame Projekte, Wiki, Team-Challenges | Nur Einzelarbeit |

### 2. Storytelling-Dimension

| Level | Beschreibung | Indikatoren |
|-------|-------------|-------------|
| 0 — Keins | Lose Inhalte ohne Rahmen | Nur Themen-Überschriften, kein roter Faden |
| 1 — Kontext | Situationsbeschreibung vorhanden | "Stellen Sie sich vor..." als Einleitung |
| 2 — Szenario | Durchgängige Rahmenhandlung | Wiederkehrendes Unternehmen/Person, Problemstellung |
| 3 — Narrativ | Vollständiger Story-Arc | Charakter + Konflikt + Progression + Auflösung, SuS als Akteure |

**Storytelling-Signale im Kurs:**
- Wiederkehrende Firmennamen/Personen → Szenario vorhanden
- "Sie sind..." / "Ihr Auftrag..." → SuS als Akteure
- Aufgaben bauen aufeinander auf → Progression
- Abschluss referenziert Anfang → Arc vorhanden

### 3. Gamification-Dimension

| Level | Beschreibung | Indikatoren |
|-------|-------------|-------------|
| 0 — Keins | Keine Spielelemente | Rein akademischer Aufbau |
| 1 — Feedback | Sofortige Rückmeldung | Quizze mit Ergebnis, Richtig/Falsch |
| 2 — Progression | Fortschrittsanzeige | Level, Phasen, Checklisten, Meilensteine |
| 3 — Vollständig | Punkte, Badges, Challenge | XP-System, Achievements, Leaderboard, Streaks |

**Gamification-Signale:**
- Punkte/Scores in Quizzen → Level 1
- Phase-Labels mit Fortschritt → Level 2
- XP, Badges, Level-System → Level 3
- Wettbewerb-Elemente → Level 3

### 4. Engagement-Indikatoren

| Element | Typ | Score | Beispiele |
|---------|-----|-------|-----------|
| Label (nur Text) | Passiv | ⭐ | Textblock ohne Interaktion |
| URL (externer Link) | Passiv | ⭐ | Link zu Theorie |
| Page (Inhaltsseite) | Passiv | ⭐⭐ | Strukturierter Inhalt |
| Page mit JS-Komponente | Interaktiv | ⭐⭐⭐⭐⭐ | Quiz, Flashcards, Simulationen |
| Label mit JS-Komponente | Interaktiv | ⭐⭐⭐⭐⭐ | Inline-Quiz, Akkordeon, Timer |
| Forum | Aktiv | ⭐⭐⭐ | Diskussion |
| Assignment | Aktiv | ⭐⭐⭐ | Abgabe |
| Quiz (Moodle-nativ) | Interaktiv | ⭐⭐⭐⭐ | Bewertetes Quiz |
| H5P | Interaktiv | ⭐⭐⭐⭐ | Interaktive Übung |
| React-App (iframe) | Interaktiv | ⭐⭐⭐⭐⭐ | Vollständige Lern-App |
| Wiki | Kollaborativ | ⭐⭐⭐⭐ | Gemeinsames Produkt |

### 5. Multimedia-Check

| Element | Vorhanden? | Empfehlung |
|---------|------------|------------|
| Bilder/Illustrationen | ❓ | Min. 1 pro Phase |
| Videos | ❓ | Für komplexe Konzepte |
| Infografiken (SVG) | ❓ | Für Prozesse/Übersichten |
| Animationen/Transitions | ❓ | Für Aufmerksamkeit |
| Icons/Emojis | ❓ | Visuelle Orientierung |

### 6. Technologie-Mix

| Technologie | Vorhanden? | Möglichkeiten |
|-------------|------------|---------------|
| Inline HTML/CSS | ❓ | Labels, Pages mit Design |
| Inline JavaScript | ❓ | Quizze, Flashcards, Timer, Akkordeon |
| React-App (iframe) | ❓ | Komplexe Simulationen, Trainer |
| SVG-Grafiken | ❓ | Interaktive Infografiken |
| CSS Animations | ❓ | Micro-Interactions, Transitions |
| H5P | ❓ | Nur wenn spezifisch nötig |

---

## Scoring-Regeln

### 4K-Score Berechnung (0-3 pro K)

**Kreativität:**
- 0: Nur passive Inhalte (Labels, URLs)
- 1: Assignments vorhanden, aber nur Textabgabe
- 2: Offene Aufgaben, JS-Sandbox, Drag&Drop
- 3: Projektaufgaben, Builder-Tools, freie Gestaltung

**Kritisches Denken:**
- 0: Keine Selbsttests oder Reflexion
- 1: Einfache Quizze (richtig/falsch)
- 2: Szenario-basierte Fragen, Entscheidungsbäume, Vergleichstools
- 3: Mehrstufige Analyse, Peer-Review, Bewertungsaufgaben

**Kommunikation:**
- 0: Keine Interaktion zwischen SuS
- 1: Ein allgemeines Forum
- 2: Aufgabenbezogene Foren, Peer-Feedback
- 3: Rollenspiele, Präsentationen, strukturierte Debatten

**Kollaboration:**
- 0: Nur Einzelarbeit
- 1: Forum-Diskussionen
- 2: Wiki oder gemeinsames Dokument
- 3: Explizite Team-Challenges, gemeinsame Produkte

### Storytelling-Score (0-3)
Siehe Storytelling-Dimension oben.

### Gamification-Score (0-3)
Siehe Gamification-Dimension oben.

### Engagement-Score

```
Engagement = (Aktiv×2 + Interaktiv×3) / (Passiv + Aktiv×2 + Interaktiv×3) × 100
```

- < 30%: 🔴 Kritisch (zu passiv)
- 30-50%: 🟡 Verbesserungswürdig
- 50-70%: 🟢 Gut
- \> 70%: 🌟 Exzellent

---

## Workflow

### Schritt 1: Kursinhalt abrufen

```
moodle_get_course_contents(courseId)
→ Alle Abschnitte mit Modulen
```

### Schritt 2: Abschnitt analysieren

Für jeden Abschnitt erfassen:

```yaml
abschnitt:
  id: [SECTION_ID]
  name: "[NAME]"
  module_count: [ANZAHL]

module_typen:
  labels: [N]
  pages: [N]
  urls: [N]
  forums: [N]
  assignments: [N]
  quizzes: [N]
  h5p: [N]
  wikis: [N]
  folders: [N]

scores:
  kreativität: [0-3]
  kritisches_denken: [0-3]
  kommunikation: [0-3]
  kollaboration: [0-3]
  storytelling: [0-3]
  gamification: [0-3]

engagement:
  passive_module: [N]
  aktive_module: [N]
  interaktive_module: [N]
  ratio: "[X]% passiv"

technologie:
  hat_inline_js: [true/false]
  hat_react_iframe: [true/false]
  hat_css_animations: [true/false]
  hat_svg: [true/false]
  hat_h5p: [true/false]

multimedia:
  bilder: [true/false]
  videos: [true/false]
  infografiken: [true/false]
```

### Schritt 3: Diagnose erstellen

```markdown
## Diagnose: [Abschnittsname]

### Stärken
- [Was bereits gut ist]

### Gesamtbild (Radar)

| Dimension | Score | Status |
|-----------|-------|--------|
| Kreativität | X/3 | 🔴🟡🟢 |
| Kritisches Denken | X/3 | 🔴🟡🟢 |
| Kommunikation | X/3 | 🔴🟡🟢 |
| Kollaboration | X/3 | 🔴🟡🟢 |
| Storytelling | X/3 | 🔴🟡🟢 |
| Gamification | X/3 | 🔴🟡🟢 |
| Engagement | X% | 🔴🟡🟢🌟 |

### Storytelling-Analyse
- Aktuell: [Level 0-3 mit Beschreibung]
- Potenzial: [Was möglich wäre]
- Empfehlung: [Konkreter Vorschlag für Rahmenhandlung]

### Gamification-Analyse
- Aktuell: [Level 0-3]
- Quick Wins: [Was sofort geht]
- Empfehlung: [XP-System, Badges, Progress-Bar etc.]

### Konkrete Optimierungsvorschläge

1. **[Vorschlag 1]**
   - Umsetzung: HTML/CSS/JS | React | H5P (nur wenn begründet)
   - 4K-Bezug: [Welches K wird gestärkt]
   - Storytelling-Bezug: [Wie es in die Erzählung passt]
   - Aufwand: ⭐/⭐⭐/⭐⭐⭐

2. **[Vorschlag 2]**
   ...
```

---

## Empfehlungs-Priorität

### Standard: HTML5/CSS/JS (in Moodle Labels/Pages)

Für die meisten interaktiven Elemente reicht Inline-JavaScript in Moodle:
- Quizze, Flashcards, Akkordeon, Timer, Drag&Drop
- Fortschrittsbalken, XP-Anzeige, Badge-System
- Entscheidungsbäume, Szenario-Simulationen
- Interaktive Infografiken (SVG + JS)

**Vorteile:** Kein externer Server nötig, sofort sichtbar, volle Kontrolle über Design, Gamification integrierbar.

### Bei Bedarf: React-App (als iframe)

Für komplexe Anwendungen wie der Excel-Trainer oder Word-Trainer:
- Multi-Level-Trainer mit Gamification
- Komplexe Simulationen mit State Management
- Apps mit mehreren Screens/Routen

**Deployment:** `lernmodule.dirk-schulenburg.net/[app-name]/` (nginx)

### Nur auf Anweisung: H5P

H5P wird **nur** empfohlen wenn:
1. Der User es **explizit anfordert**
2. **Interactive Video** benötigt wird (zu aufwändig selbst zu bauen)
3. **Branching Scenario** mit komplexer Verzweigung benötigt wird
4. **xAPI-Tracking** für Moodle-Gradebook zwingend erforderlich ist
5. **Kurs-Export** mit eingebetteten Aktivitäten nötig ist (H5P reist im Backup mit)

Wenn H5P empfohlen wird, immer den **Grund** angeben.

---

## Storytelling-Patterns für Empfehlungen

### Pattern A: "Der Auftrag"
SuS bekommen einen realistischen Arbeitsauftrag in einem fiktiven Unternehmen. Jede Phase des Abschnitts ist ein Schritt zur Lösung.

### Pattern B: "Die Ermittlung"
SuS untersuchen einen Fall (Fehler, Problem, Reklamation). Sie sammeln Hinweise, analysieren Daten und präsentieren eine Lösung.

### Pattern C: "Die Challenge"
SuS treten (gegen sich selbst oder gegeneinander) an. Level steigen in Schwierigkeit, Punkte werden gesammelt, am Ende steht ein Ergebnis.

### Pattern D: "Die Reise"
SuS durchlaufen Stationen einer Lernreise mit klarem Start und Ziel. Jede Station bringt neues Wissen und einen "Stempel" (Badge/Checkpoint).

### Pattern E: "Der Experten-Aufstieg"
Vom Anfänger zum Experten in Stufen: Lehrling → Geselle → Meister. Jede Stufe hat eigene Challenges und Tests.

---

## Gamification-Elemente für Empfehlungen

| Element | Komplexität | Umsetzung | Wirkung |
|---------|-------------|-----------|---------|
| Fortschrittsbalken | ⭐ | CSS/HTML in Label | Orientierung |
| Punkte pro Aufgabe | ⭐ | JS in Quiz-Labels | Motivation |
| Phase-Badges | ⭐⭐ | CSS/HTML in Abschluss-Label | Erfolgserlebnis |
| XP-System | ⭐⭐ | JS mit localStorage | Langfristmotivation |
| Timer-Challenge | ⭐⭐ | JS in Page | Spannung |
| Streak-Counter | ⭐⭐ | JS mit localStorage | Gewohnheit |
| Leaderboard | ⭐⭐⭐ | React-App (iframe) | Wettbewerb |
| Level-System | ⭐⭐⭐ | React-App (iframe) | Langfristige Bindung |

---

## Beispiel-Analyse

### Input
```
Kurs-ID: 6, Abschnitt: 2 (Checkout-Prozess analysieren)
```

### Output

```markdown
## Diagnose: Abschnitt 2 — Den Checkout-Prozess analysieren

### Ist-Zustand
- 4 Module: 1 URL, 3 Foren
- Kein interaktiver Content, keine Bilder, kein roter Faden

### Gesamtbild

| Dimension | Score | Status |
|-----------|-------|--------|
| Kreativität | 0/3 | 🔴 |
| Kritisches Denken | 1/3 | 🟡 |
| Kommunikation | 2/3 | 🟢 |
| Kollaboration | 1/3 | 🟡 |
| Storytelling | 0/3 | 🔴 |
| Gamification | 0/3 | 🔴 |
| Engagement | 43% | 🟡 |

### Storytelling-Empfehlung
**Pattern B: "Die Ermittlung"** — SuS untersuchen einen realen
Online-Shop mit hoher Abbruchrate. Jede Phase liefert neue Daten
(Heatmaps, Statistiken, Kundenfeedback). Am Ende präsentieren sie
einen Optimierungsvorschlag.

### Top-4 Optimierungen

1. **Szenario-Einführung: "Fall Shopify-Peters"**
   - Umsetzung: HTML/CSS in Label (Storytelling-Rahmen)
   - Wirkung: Storytelling 0→2, Engagement ↑
   - Aufwand: ⭐

2. **JS-Quiz: Checkout-Basics (8 Fragen)**
   - Umsetzung: JavaScript in Moodle-Page
   - Wirkung: Kritisches Denken ↑, Gamification 0→1 (Punkte)
   - Aufwand: ⭐⭐

3. **Interaktive Checkout-Analyse (Drag&Drop)**
   - Umsetzung: HTML/CSS/JS in Page (Schritte zuordnen)
   - Wirkung: Kreativität ↑, Engagement ↑↑
   - Aufwand: ⭐⭐

4. **Fortschrittsbalken + Abschluss-Badge**
   - Umsetzung: CSS in Labels (Start + Ende)
   - Wirkung: Gamification 0→2
   - Aufwand: ⭐
```

---

## Integration mit anderen Skills

| Skill | Zusammenspiel |
|-------|---------------|
| `moodle-section-optimizer` | Erhält Diagnose als Input, setzt Empfehlungen um |
| `h5p-generator` | Nur wenn H5P explizit gewünscht oder technisch nötig |
| `lernfeld-zu-moodle-kurs` | Kann Analyzer für QA nutzen |
| `lesson-creator` | HTML-Arbeitsblätter als Grundlage |

## Moodle-Berechtigungen

Nach CLI-Befehlen im Container:
```bash
docker exec moodle chown -R www-data:www-data /var/www/html/
```

## Limitations

- Kann Inhaltsqualität nicht bewerten (nur Struktur)
- Matchplan-Abgleich erfordert manuellen Input
- H5P-Inhalte in Moodle nicht direkt analysierbar (nur Existenz prüfbar)
- JS in Moodle-Labels kann von Theme-Updates beeinflusst werden

---

*Skill Version: 2.0*
*Abhängigkeiten: moodle-mcp (v3.3.0, 73 Tools)*
*Letzte Aktualisierung: 2026-03-12*
*Paradigmenwechsel: HTML5/CSS/JS/React first, H5P nur auf Anweisung*
