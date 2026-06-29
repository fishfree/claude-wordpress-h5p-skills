---
name: exercise-quality-optimizer
description: Schlägt konkrete Optimierungen für schwache Übungsaufgaben in Lern-Apps vor (ESA-Mathe, Buchführungstrainer u.a.). Nutzt die Score-Analyse aus exercise-quality-analyzer und produziert Code-Snippets, neue Visualisierungs-Komponenten oder Aufgabentyp-Wechsel. Nutze nach exercise-quality-analyzer oder wenn konkrete Übungs-Verbesserungen benötigt werden.
license: MIT
---

# Exercise Quality Optimizer

Setzt Mikro-Aufgaben-Verbesserungen um — pro schwachem Kriterium gibt es ein
festes Repertoire an Maßnahmen mit Code-Snippets.

## Wann nutzen

- Nach `exercise-quality-analyzer` mit identifizierten Schwächen
- Wenn eine konkrete Aufgabe „zu statisch" wirkt
- Bei Sprachlerner-Zielgruppe: zusätzliche visuelle Anker einbauen
- In Sub-Agent-Pipelines für Bulk-Optimierung

## Voraussetzungen

- Score-Tabelle einer Übungsdatei (von Analyzer) ODER konkrete schwache Aufgabe
- Lese-Zugriff auf `esa-mathe/src/components/visualizations/` und
  `esa-mathe/src/components/exercises/`

## Optimierungs-Bausteine

### Defizit: Story-Anker ≤ 1

**Maßnahme:** `characterComment` ergänzen, Kontext aus Charakter-Welt einbauen.

```javascript
// Vorher:
{ questionText: 'Berechne 12 − 5.' }

// Nachher:
{
  questionText: 'Noor zählt **Bretter**: erst 12, dann nimmt sie 5 mit. Wie viele bleiben?',
  characterId: 'noor',
  context: 'workshop',
  characterComment: 'Beim **Zuschnitt** zähle ich vorher, hinterher und ziehe ab — so weiß ich, was im Lager bleibt.',
}
```

Charakter-Pool (esa-mathe):

| ID | Welt | Typische Kontexte |
|---|---|---|
| yara | Café | Kassenzettel, Bestellung, Trinkgeld, Schicht |
| malik | Job | Lohn, Brutto/Netto, Rabatt, Einkauf |
| noor | Werkstatt | Bretter, Schrauben, Maße, Material |

### Defizit: Visuelle Repräsentation ≤ 1

**Maßnahme A** — Bestehende Visualisierung nutzen:

| Konzept | `visualization.type` | Datei |
|---|---|---|
| Brüche, Anteile | `fraction` | `FractionVisualizer.jsx` |
| Zahlenstrahl, Größenvergleich | `number-line` | `NumberLine.jsx` |
| Säulen-/Balkendiagramm | `bar-chart` | `BarChartBuilder.jsx` |
| Flächen, Rechtecke (Bretter!) | `area` | `AreaCalculator.jsx` |
| Volumen, Quader, 3D | `volume` | `VolumeExplorer.jsx` |
| Lohn-Rechnung | `wage` | `WageCalculator.jsx` |
| Koordinatensystem | `coordinate` | `CoordinateGrid.jsx` |
| Lineare Funktionen | `function-plotter` | `FunctionPlotter.jsx` |
| Maßeinheiten umrechnen | `unit-converter` | `UnitConverter.jsx` |
| **Gleichung als Waage** | `balance-scale` | `BalanceScale.jsx` |

**Maßnahme B** — Neue Visualisierungs-Komponente bauen, wenn kein Match:

Vorlage: SVG + React + optional Framer Motion. Pattern:

```jsx
// src/components/visualizations/<Name>.jsx
export default function MyVis({ value = 0, target = 0, solved = false }) {
  return (
    <svg viewBox="0 0 280 200" width="100%" style={{ maxWidth: 280 }}
         role="img" aria-label="Beschreibung">
      {/* SVG-Inhalt, optional mit CSS-Transition für Animation */}
    </svg>
  );
}
```

Dann in `VisualizationRenderer.jsx` registrieren:

```jsx
import MyVis from './MyVis';
const COMPONENTS = { ..., 'mein-typ': MyVis };
```

**Empfehlungen für Sprachlerner-Zielgruppe:**
- Möglichst piktografisch (nicht Text-lastig)
- Bezeichnungen mehrsprachig oder durch Symbole
- Zahlen prominent, Worte sparsam
- Bretter/Schrauben/Pizza dürfen 3D-isometrisch oder als Rechteck dargestellt werden

### Defizit: Kognitiver Tiefgrad ≤ 1

**Maßnahme:** Aufgabentyp-Wechsel — ergänze zu reinen „Berechne"-Varianten
folgende Formate:

| Format | Beispiel | Aufgabentyp |
|---|---|---|
| Was-stimmt-nicht | „30 % Rabatt von 80 € — neuer Preis 60 €. Stimmt das?" | `multiple-choice` mit Begründung oder `answer-sentence` |
| Schätze-zuerst | „Schätze: ist der Tank halb voll? Dann rechne nach." | `comparison` (Schätzung vs. Lösung) |
| Erkläre-warum | „Erkläre, warum 10 % einfacher zu berechnen ist als 17 %." | `answer-sentence` mit Schlüsselwort-Match |
| Finde-den-Fehler | „Hier ist eine Rechnung. Wo ist der Fehler?" | `multiple-choice` (Position des Fehlers) |

### Defizit: Aktivitätsform ≤ 1 (Basis-Stufe)

**Maßnahme:** `type` wechseln zu interaktivem Renderer.

| Aktueller `type` | Wechsel-Vorschlag | Wann sinnvoll |
|---|---|---|
| numeric-input | drag-match | bei Mengen-Aufgaben (zähle, ordne zu) |
| numeric-input | slider-answer | bei kontinuierlichen Werten (Prozent, Geschwindigkeit) |
| numeric-input | number-line-click | bei Zahlenstrahl-tauglichen Aufgaben |
| multiple-choice | drag-match | wenn mehrere Items zugeordnet werden |

### Defizit: Fehler-Pädagogik ≤ 1

**Maßnahme:** `commonMistakes` ausbauen.

```javascript
commonMistakes: [
  // Mindestens 3 Einträge, jeder mit:
  {
    value: 17,                        // typischer falscher Wert
    tolerance: 0.001,                 // Toleranz für Treffer
    hint: 'Du hast **addiert statt subtrahiert**. Um x allein zu bekommen, muss die +5 weg — also **12 − 5**, nicht 12 + 5.',
    // → diagnostisch: WARUM dieser Fehler entsteht, WIE er korrigiert wird
  },
]
```

`hints` auf 4 Stufen ausbauen:

```javascript
hints: [
  { level: 1, type: 'tip',         content: 'kurzer Hinweis' },
  { level: 2, type: 'formula',     content: 'die passende Formel' },
  { level: 3, type: 'walkthrough', content: 'Lösungsweg in 1–2 Zeilen' },
  { level: 4, type: 'example',     content: 'Beispiel mit anderen Zahlen' },
]
```

## Workflow für Sub-Agents

### Eingabe pro Sub-Agent

```yaml
input:
  exercise_file: "esa-mathe/src/data/exercises/brueche.js"
  weak_exercises: ["bruch-bas-007", "bruch-bas-014", ...]    # aus Analyzer
  max_changes: 5                                              # pro Lauf
```

### Ausgabe pro Sub-Agent

```markdown
## Optimierungsvorschläge: brueche.js

### bruch-bas-007 (Σ 4 → erwartet 9)

**Schwachstellen:** visual=0, aktion=0, bloom=1

**Vorschlag 1 — Visualisierung:**
```diff
+ visualization: { type: 'fraction', parts: 4, highlighted: 1, shape: 'circle' },
```

**Vorschlag 2 — Aufgabentyp:**
```diff
- type: 'numeric-input',
+ type: 'fraction-input',
```

**Vorschlag 3 — Bloom-Anhebung:**
```diff
- questionText: 'Wie viel ist 1/4?',
+ questionText: 'Schätze zuerst: ist 1/4 mehr oder weniger als 1/3? Dann rechne 1/4 von 12 €.',
```

Erwarteter Score-Gewinn: +5 Punkte.

### bruch-bas-014 ...
```

## Approval-Pfad

1. Sub-Agent generiert Vorschläge (kein Code-Edit ohne Approval)
2. Master-Agent (oder Lehrer) reviewed Vorschläge
3. Approved Vorschläge werden als Edit/Patch angewandt
4. `exercise-quality-analyzer` läuft erneut → Score-Gewinn dokumentieren

## Limitations

- Generiert Code-Vorschläge, **prüft nicht** mathematische Korrektheit der
  Aufgabe (Lehrer muss Inhalt validieren)
- Neue Visualisierungs-Komponenten kann der Skill nur skizzieren; das
  React-Rendering muss manuell ergänzt werden
- Mehrsprachige Inhalte (i18n-Files) werden vom Optimizer nicht synchron
  aktualisiert — separater Pass nötig

## Referenzen

- `claude-skills/exercise-quality-analyzer/SKILL.md` — vorgelagerter Skill
- `esa-mathe/docs/exercise-quality.md` — Scoring-Modell
- `esa-mathe/src/components/visualizations/` — vorhandene Visualisierungen
- `esa-mathe/src/components/exercises/` — vorhandene Aufgabentypen
