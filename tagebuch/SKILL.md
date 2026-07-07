---
name: tagebuch
description: >
  Persoenliches Tagebuch im Obsidian Vault. Erstellt taegliche Eintraege
  mit YAML-Frontmatter, Tags, Stimmung und Kategorien.
  Nutze wenn: "Tagebuch", "Tageseintrag", "Notiz fuer heute",
  "Wie war mein Tag", "Ich moechte festhalten", "Beobachtung",
  "Reflexion", persoenliche Gedanken aufschreiben.
license: MIT
agent: Personal
allowed-tools:
  - Write
  - Read
  - Glob
  - Grep
---

# Tagebuch-Skill

Persoenliches Tagebuch mit strukturierten Eintraegen im Obsidian Vault. Taeglich Gedanken, Beobachtungen und Reflexionen festhalten — mit YAML-Frontmatter, Tags, Stimmung und automatischer Verlinkung.

## Tool Integration

| Tool | Zweck |
|------|-------|
| `Write` | Eintrag erstellen oder an bestehenden Tag anhaengen |
| `Read` | Bestehenden Tageseintrag lesen (fuer Append) |
| `Glob` | Bestehende Eintraege finden |
| `Grep` | Verwandte Eintraege per Tag/Keyword suchen |

**Ziel-Verzeichnis:**
```
C:\Users\mail\Personal_Vault\Personal_Documentation\tagebuch\
├── 2026/
│   ├── 2026-02-09.md
│   ├── 2026-02-10.md
│   └── ...
└── _index.md
```

---

## Wann diesen Skill nutzen

- "Tagebuch" / "Tageseintrag"
- "Notiz fuer heute"
- "Wie war mein Tag"
- "Ich moechte festhalten: ..."
- "Beobachtung: ..."
- "Reflexion: ..."
- Persoenliche Gedanken aufschreiben
- "Was habe ich diese Woche gemacht?" (Rueckblick)

---

## Workflow

### Phase 1: Erfassen

Der Nutzer erzaehlt oder diktiert frei. Der Skill hoert zu und sammelt den Input.

**Wichtig:**
- Nicht unterbrechen — erst alles aufnehmen
- Bei kurzem Input nachfragen: "Moechtest du noch etwas ergaenzen?"
- Bei laengerem Input direkt zu Phase 2 uebergehen

**Trigger-Erkennung:**

| Trigger | Aktion |
|---------|--------|
| "Tagebuch", "Eintrag" | Neuen Eintrag starten |
| "Wie war mein Tag" | Eintrag mit Tagesrueckblick |
| "Beobachtung" | Kategorie `beobachtung` vorschlagen |
| "Reflexion" | Kategorie `reflexion` vorschlagen |
| "Rueckblick", "Zusammenfassung" | Rueckblick-Funktion (Phase R) |

### Phase 2: Strukturieren

1. **Titel ableiten**: Kurzen, beschreibenden Titel aus dem Inhalt generieren
2. **Kategorie erkennen**: Basierend auf Inhalt eine Kategorie vorschlagen

   | Kategorie | Wann |
   |-----------|------|
   | `persoenlich` | Private Gedanken, Alltag, Familie |
   | `beobachtung` | Etwas Gesehenes/Erlebtes beschreiben |
   | `reflexion` | Nachdenken ueber Erfahrungen, Erkenntnisse |
   | `projekt` | Fortschritte bei Projekten, Arbeit, Schule |

3. **Tags vorschlagen**: Schluesselwoerter aus dem Text erkennen

   | Keyword im Text | Vorgeschlagener Tag |
   |-----------------|---------------------|
   | Schule, Unterricht, Moodle | #schule |
   | Projekt, Code, Server | #arbeit |
   | Familie, Zuhause | #familie |
   | Sport, Gesundheit, Laufen | #gesundheit |
   | Kochen, Essen, Rezept | #kochen |
   | Lesen, Buch, Film, Serie | #medien |
   | Reise, Ausflug, Urlaub | #reise |
   | Freunde, Treffen | #soziales |
   | Natur, Garten, Wetter | #natur |
   | Idee, Plan, Vorhaben | #idee |

4. **Stimmung erfragen** (NICHT raten!):

   ```
   Wie wuerdest du deine Stimmung beschreiben?
   - gut
   - gemischt
   - schwer
   (oder eigene Beschreibung)
   ```

5. **Zusammenfassung zeigen** und bestaetigen lassen:

   ```
   Titel: Elternabend und neue Ideen
   Kategorie: persoenlich
   Stimmung: gut
   Tags: #schule #soziales

   Passt das so, oder moechtest du etwas aendern?
   ```

### Phase 3: Speichern & Verlinken

1. **Pruefen ob Datei fuer heute existiert:**

   ```
   Glob: C:\Users\mail\Personal_Vault\Personal_Documentation\tagebuch\{{YYYY}}\{{YYYY-MM-DD}}.md
   ```

2. **Datei erstellen oder anhaengen:**

   - **Neue Datei**: Vollstaendiges Template mit Frontmatter schreiben
   - **Bestehende Datei**: Neuen Abschnitt mit Uhrzeit anhaengen (siehe Append-Template)

3. **Verwandte Eintraege suchen:**

   ```
   Grep: Tags aus dem aktuellen Eintrag in bestehenden Eintraegen suchen
   Pfad: C:\Users\mail\Personal_Vault\Personal_Documentation\tagebuch\
   ```

4. **Related-Links einfuegen**: Gefundene verwandte Eintraege als `related` im Frontmatter verlinken

5. **Bestaetigung ausgeben:**

   ```
   Tagebucheintrag gespeichert!

   Datei: tagebuch/2026/2026-02-09.md
   Titel: Elternabend und neue Ideen
   Kategorie: persoenlich | Stimmung: gut
   Tags: #schule #soziales

   Verwandte Eintraege:
   - [[2026-02-03]] (Tag: #schule)
   - [[2026-01-28]] (Tag: #soziales)
   ```

---

## Eintrag-Template (Neue Datei)

```markdown
---
title: "Kurzer Titel des Eintrags"
date: {{YYYY-MM-DD}}
kategorie: persoenlich
mood: gut
tags:
  - tag1
  - tag2
related:
  - "[[{{verwandtes-datum}}]]"
---

# {{YYYY-MM-DD}} — Kurzer Titel

## Eintrag

Freitext hier...

---
*Erstellt: {{YYYY-MM-DD}} {{HH:mm}}*
```

## Append-Template (Weiterer Eintrag am gleichen Tag)

Wenn bereits eine Datei fuer den Tag existiert:

1. Bestehende Datei mit `Read` lesen
2. Frontmatter-Tags und related aktualisieren (neue Tags ergaenzen)
3. Neuen Abschnitt anhaengen:

```markdown

## {{HH:mm}} — Kurzer Titel

Freitext hier...

---
*Ergaenzt: {{YYYY-MM-DD}} {{HH:mm}}*
```

**Wichtig beim Append:**
- Frontmatter `tags` um neue Tags erweitern (keine Duplikate)
- Frontmatter `related` um neue Links erweitern
- Bestehenden Inhalt NICHT veraendern
- Neuen Abschnitt am Ende der Datei einfuegen (vor dem letzten `---` Timestamp)

---

## Rueckblick-Funktion (Phase R)

Bei Triggern wie "Rueckblick", "Was habe ich diese Woche gemacht?", "Zusammenfassung":

1. **Zeitraum bestimmen**: Standard = letzte 7 Tage, oder vom Nutzer angegeben
2. **Eintraege sammeln**:

   ```
   Glob: C:\Users\mail\Personal_Vault\Personal_Documentation\tagebuch\{{YYYY}}\{{YYYY-MM-*}}.md
   ```

3. **Eintraege lesen** und zusammenfassen:
   - Kategorien-Verteilung (z.B. "3x persoenlich, 2x projekt, 1x reflexion")
   - Stimmungsverlauf
   - Haeufigste Tags
   - Kurze Zusammenfassung pro Tag (1-2 Saetze)

4. **Output-Format:**

   ```
   Rueckblick: 03.02. - 09.02.2026

   Eintraege: 5
   Stimmung: gut (3x), gemischt (2x)
   Top-Tags: #schule (3), #arbeit (2), #familie (1)

   Mo 03.02. — Wochenstart mit Konferenz
   Di 04.02. — Neue Lernsituation geplant
   Mi 05.02. — Reflexion ueber Unterrichtsmethoden
   Do 06.02. — Elternabend und Gespraeche
   So 09.02. — Ruhiger Tag, Planung fuer naechste Woche

   Auffaellig: Schule war diese Woche das Hauptthema.
   ```

---

## Dateipfade

```
VAULT_BASE = C:\Users\mail\Personal_Vault\Personal_Documentation\tagebuch
ENTRY_DIR  = {VAULT_BASE}\{YYYY}\
ENTRY_FILE = {ENTRY_DIR}\{YYYY-MM-DD}.md
INDEX_FILE = {VAULT_BASE}\_index.md
```

**Dateiname-Konvention:** Immer `YYYY-MM-DD.md` — ein File pro Tag, mehrere Eintraege werden angehaengt.

---

## Frontmatter-Schema

```yaml
# Pflichtfelder
title: string           # Kurzer beschreibender Titel
date: YYYY-MM-DD        # Datum des Eintrags
kategorie: string       # persoenlich | beobachtung | reflexion | projekt
mood: string            # gut | gemischt | schwer (vom Nutzer angegeben)

# Optionale Felder
tags: [string]          # Freitext-Tags, lowercase
related: [string]       # Obsidian-Links zu verwandten Eintraegen
```

---

## Tag-Vorschlaege (Automatisch)

| Keyword im Content | Vorgeschlagener Tag |
|---------------------|---------------------|
| Schule, Unterricht, Moodle, Klasse | #schule |
| Projekt, Code, Server, Deploy | #arbeit |
| Familie, Kinder, Zuhause | #familie |
| Sport, Laufen, Gym, Gesundheit | #gesundheit |
| Kochen, Essen, Rezept, Restaurant | #kochen |
| Buch, Film, Serie, Lesen, Podcast | #medien |
| Reise, Ausflug, Urlaub, Wandern | #reise |
| Freunde, Treffen, Feier, Abend | #soziales |
| Natur, Garten, Wetter, Spaziergang | #natur |
| Idee, Plan, Vorhaben, Ziel | #idee |
| Cannabis, CSC, Growing, Verein | #csc |
| Docker, MCP, n8n, Infrastruktur | #devops |
| Stress, Muede, Erschoepft | #belastung |
| Dankbar, Gluecklich, Zufrieden | #dankbarkeit |

---

## Beispiel-Session

**User:** "Tagebuch — Heute war ein guter Tag. Hatte morgens ein langes Gespraech mit einem Kollegen ueber neue Unterrichtsideen fuer die IT-Klasse. Nachmittags dann endlich den MCP-Server fertig deployed. Abends noch gekocht, Pasta mit Pesto."

**Claude:**

1. **Erfassen**: Input aufnehmen (komplett, nicht unterbrechen)

2. **Strukturieren**:
   ```
   Titel: Guter Tag mit Kollegenaustausch und Deployment
   Kategorie: persoenlich (Tagesrueckblick, mehrere Themen)
   Tags: #schule #arbeit #devops #kochen
   ```

3. **Stimmung erfragen**:
   ```
   Wie wuerdest du deine Stimmung beschreiben?
   - gut
   - gemischt
   - schwer
   ```
   User: "gut"

4. **Bestaetigen**:
   ```
   Titel: Guter Tag mit Kollegenaustausch und Deployment
   Kategorie: persoenlich | Stimmung: gut
   Tags: #schule #arbeit #devops #kochen

   Passt das so?
   ```
   User: "ja"

5. **Speichern**: Pruefen ob `2026-02-09.md` existiert → Nein → Neue Datei:

   ```markdown
   ---
   title: "Guter Tag mit Kollegenaustausch und Deployment"
   date: 2026-02-09
   kategorie: persoenlich
   mood: gut
   tags:
     - schule
     - arbeit
     - devops
     - kochen
   related:
     - "[[2026-02-07]]"
   ---

   # 2026-02-09 — Guter Tag mit Kollegenaustausch und Deployment

   ## Eintrag

   Heute war ein guter Tag. Hatte morgens ein langes Gespraech mit einem Kollegen ueber neue Unterrichtsideen fuer die IT-Klasse. Nachmittags dann endlich den MCP-Server fertig deployed. Abends noch gekocht, Pasta mit Pesto.

   ---
   *Erstellt: 2026-02-09 19:30*
   ```

6. **Bestaetigung**:
   ```
   Tagebucheintrag gespeichert!

   Datei: tagebuch/2026/2026-02-09.md
   Titel: Guter Tag mit Kollegenaustausch und Deployment
   Kategorie: persoenlich | Stimmung: gut
   Tags: #schule #arbeit #devops #kochen

   Verwandte Eintraege:
   - [[2026-02-07]] (Tag: #devops)
   ```

---

## Append-Beispiel

**User:** "Noch ein Eintrag fuer heute: Gerade einen schoenen Spaziergang gemacht, Vollmond."

**Claude:**

1. Pruefen: `2026-02-09.md` existiert bereits → Append-Modus
2. Bestehende Datei lesen
3. Stimmung: "Passt die Stimmung 'gut' noch, oder moechtest du sie aendern?"
4. Neue Tags: #natur
5. Frontmatter-Tags aktualisieren (natur ergaenzen)
6. Neuen Abschnitt anhaengen:

```markdown

## 21:15 — Spaziergang bei Vollmond

Gerade einen schoenen Spaziergang gemacht, Vollmond.

---
*Ergaenzt: 2026-02-09 21:15*
```

---

## Best Practices

### Do

- Stimmung immer erfragen, nie annehmen
- Tags vorschlagen, aber Nutzer entscheiden lassen
- Bei Append bestehenden Inhalt nie veraendern
- Kurze, praegnante Titel waehlen
- Verwandte Eintraege automatisch verlinken

### Don't

- Stimmung raten oder interpretieren
- Inhalt umformulieren (Original-Wortlaut beibehalten)
- Bewertungen oder Ratschlaege geben (es ist ein Tagebuch, kein Coach)
- Zu viele Tags vorschlagen (max 5-6)
- Eintraege anderer Tage veraendern

---

## Verwandte Skills

- **idea-capture**: Schnelle Ideen festhalten (kuerzer, weniger strukturiert)
- **weekly-digest**: Woechentliche Zusammenfassung (kann Tagebuch-Eintraege einbeziehen)
- **recherche-workflow**: Themen aus dem Tagebuch vertiefen

---

*Zuletzt aktualisiert: 09.02.2026*
*Version: 1.0*
