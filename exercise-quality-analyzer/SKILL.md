---
name: exercise-quality-analyzer
description: Analysiert einzelne Übungsaufgaben in ESA-Mathe und verwandten Lern-Apps nach dem 5-Kriterien-Mikro-Aufgaben-Modell (Story-Anker, Visuelle Repräsentation, Kognitiver Tiefgrad, Aktivitätsform, Fehler-Pädagogik). Liefert Score-Tabelle pro Modul und identifiziert die schwächsten Aufgaben. Nutze für Qualitätssicherung von Übungs-Daten in Trainer-Apps (esa-mathe, buchfuehrung-trainer, word-trainer).
license: MIT
---

# Exercise Quality Analyzer

Bewertet Mikro-Aufgaben (single exercise objects) in Lern-Apps nach
einheitlichem 5-Kriterien-Modell. Inspiriert vom 4K-Modell aus
`moodle-section-analyzer`, aber auf die Mikro-Ebene zugeschnitten.

## Wann nutzen

- Qualitätsinventur eines Übungs-Moduls (z.B. `esa-mathe/src/data/exercises/prozent.js`)
- Vor Einsatz des `exercise-quality-optimizer` Skills
- Identifikation schwacher Aufgaben für Refactoring-Sprints

## Voraussetzungen

- Lese-Zugriff auf die Exercise-Datei (`*.js` mit `export const exercises = [...]`)
- Kenntnis des Domain-Modells: siehe `esa-mathe/docs/exercise-quality.md`

## Die fünf Kriterien (0–3 Punkte)

| # | Kriterium | Felder im Exercise-Objekt |
|---|-----------|----------------------------|
| 1 | **Story-Anker** | `data.questionText`, `characterComment`, `characterId`, `context` |
| 2 | **Visuelle Repräsentation** | `visualization` |
| 3 | **Kognitiver Tiefgrad** | `data.questionText` (Verben: berechne / finde Fehler / schätze / erkläre) |
| 4 | **Aktivitätsform** | `type` (numeric-input, drag-match, slider-answer, …) — schwierigkeitsabhängig |
| 5 | **Fehler-Pädagogik** | `data.commonMistakes`, `hints` |

Vollständige Scoring-Regeln: `esa-mathe/docs/exercise-quality.md`.

## Workflow

### Schritt 1: Datei laden und parsen

```javascript
import { exercises } from './brueche.js';
// exercises ist Array von Exercise-Objekten
```

### Schritt 2: Pro Übung scoren

Für jedes Exercise-Objekt:

```yaml
exercise:
  id: 'bruch-bas-001'
  diffLevel: 'basis'
  type: 'numeric-input'

scores:
  story:    0-3   # Story-Anker
  visual:   0-3   # Visuelle Repräsentation (visualization-Property)
  bloom:    0-3   # Kognitiver Tiefgrad (Bloom-Stufe aus questionText)
  aktion:   0-3   # Aktivitätsform (type, abhängig von diffLevel)
  fehler:   0-3   # Fehler-Pädagogik (commonMistakes + hints)
  sum:      0-15

stage:    "vorzeige" | "solide" | "verbesserungswuerdig" | "defizit"
weakest:  ["bloom", "aktion"]   # Kriterien mit Score ≤ 1
```

### Schritt 3: Score-Tabelle ausgeben (Markdown)

```markdown
## Modul: brueche.js (47 Aufgaben)

### Verteilung
- ★★★ Vorzeige (13–15):    N
- ★★ Solide (9–12):         N
- ★ Verbesserungswürdig (5–8): N
- 🔴 Defizit (0–4):          N

### Schwächste 10 Aufgaben

| # | ID | Diff | Story | Vis | Bloom | Aktion | Fehler | Σ | Schwächstes Kriterium |
|---|----|------|-------|-----|-------|--------|--------|---|------------------------|
| 1 | bruch-bas-014 | basis | 1 | 0 | 1 | 0 | 2 | 4 | visual+aktion |
| ... |

### Modul-Durchschnitt: X.X / 15
```

## Scoring-Heuristiken

Diese Regeln sind operationalisierbar und können von Sub-Agents konsistent
angewendet werden.

### Story-Anker

```python
score = 0
if has_character_id:                                score += 1   # Person
if context_in ['job','workshop','cafe','grocery']:  score += 1   # Alltag
if character_comment_length > 100 chars:            score += 1   # emotionaler Anker
score = min(score, 3)
```

### Visuelle Repräsentation

```python
if not visualization: return 0
type = visualization.type
if type in ['decoration', 'bullet']: return 1
if type in ['fraction', 'number-line', 'bar-chart', 'area', 'wage',
            'coordinate', 'volume', 'unit-converter']: return 2
if type in ['balance-scale', 'function-plotter']: return 3   # live-reaktiv
return 2  # default für unbekannte aber gesetzte Visualisierungen
```

### Kognitiver Tiefgrad (Bloom)

Aus `data.questionText` (Sprache erkennen, Schlüsselwörter):

```python
# Stufe 0 — Erinnern: nur Zahlen-Fakten
if matches(/^berechne|^wie viel ist \d/i): return 0

# Stufe 1 — Verstehen / Anwenden (Default für die meisten Aufgaben)
default = 1

# Stufe 2 — Analysieren
if matches(/finde den fehler|was stimmt nicht|stimmt das/i): return 2

# Stufe 3 — Bewerten / Schätzen / Erklären
if matches(/schätze|erkläre|begründe|war .* gut|warum/i): return 3

return default
```

### Aktivitätsform (schwierigkeitsabhängig)

**Basis-Stufe:**

| `type` | Score |
|--------|-------|
| numeric-input, fraction-input | 0 |
| multiple-choice, comparison, answer-sentence | 1 |
| slider-answer, order-sort, number-line-click, unit-convert | 2 |
| drag-match, graph-plot, fill-table, diagram-read | 3 |

**Standard / Prüfungs-Stufe:**

| `type` | Score |
|--------|-------|
| multiple-choice (ohne Begründung) | 0 |
| answer-sentence | 1 |
| numeric-input, fraction-input, step-solver | 2 |
| drag-match, graph-plot | 3 |

### Fehler-Pädagogik

```python
hints = exercise.hints or []
mistakes = exercise.data.commonMistakes or []

if not hints and not mistakes: return 0
if len(hints) >= 1 and not mistakes: return 1
if len(hints) >= 3 and 1 <= len(mistakes) <= 2: return 2
if len(hints) >= 4 and len(mistakes) >= 3:
  if all(m.hint and len(m.hint) > 30 for m in mistakes): return 3
  return 2
return 1
```

## Aggregation

```python
sum_score = story + visual + bloom + aktion + fehler

if sum_score >= 13: stage = "vorzeige"
elif sum_score >= 9: stage = "solide"
elif sum_score >= 5: stage = "verbesserungswuerdig"
else:                stage = "defizit"
```

## Output-Format

Default: ein Markdown-Report pro Modul mit Score-Tabelle und schwächsten 10
Aufgaben. Bei mehreren Modulen: ein Cross-Modul-Bericht mit Gesamtdurchschnitt
und Top-30 schwächster Aufgaben über alle Module.

## Integration

| Skill | Zusammenspiel |
|-------|---------------|
| `exercise-quality-optimizer` | Erhält schwache Aufgaben als Input |
| `media-factory` | Liefert empfohlene Multimedia-Inhalte (SVG, Bilder, Audio) |
| `lesson-creator` | Übergeordneter Workflow für komplette Module |

## Limitations

- Bewertet nur Struktur und Datenfelder, nicht inhaltliche Korrektheit
- Bloom-Stufen-Erkennung über Schlüsselwörter ist heuristisch — kann bei
  metaphorischen Formulierungen falsch klassifizieren
- Mehrsprachige Aufgaben werden derzeit nur in der Hauptsprache (Deutsch)
  bewertet

## Referenzen

- `esa-mathe/docs/exercise-quality.md` — vollständige Scoring-Regeln
- `claude-skills/moodle-section-analyzer/SKILL.md` — verwandtes Modell für Sections
