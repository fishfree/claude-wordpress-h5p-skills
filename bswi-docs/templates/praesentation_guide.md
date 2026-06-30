# BS:WI Präsentation – Template Guide

## Überblick

Die **BSWI_Master.pptx** ist die offizielle Präsentationsvorlage der BS:WI. Sie enthält fertige Folienlayouts im Corporate Design.

---

## Vorhandene Folien in BSWI_Master.pptx

| Folie | Layout | Verwendung |
|-------|--------|------------|
| 1 | Titelfolie | Claim "Kompetent Zukunft Gestalten" mit Icon |
| 2 | Titel + Bild (rechts) | Standard-Inhaltsfolie |
| 3 | Titel + Bild (rechts) | Variante mit anderem Bild |
| 4 | Zwei Bilder + Text | Für Vergleiche, Gegenüberstellungen |
| 5 | Titel + Bild (groß) | Abschluss/Feature-Folie |

---

## Design-Spezifikationen

### Farben (aus Theme)

| Verwendung | Farbe | HEX |
|------------|-------|-----|
| Hintergrund hell | Blau 7 | `#EAF6FE` |
| Text dunkel | Blau 1 | `#1C3D71` |
| Akzent | Blau 5 | `#41C0F0` |
| Links | Blau 5 | `#41C0F0` |
| Highlight | Neongelb | `#E8FF00` |

### Schriften (aus Theme)

| Element | Schrift |
|---------|---------|
| Headlines | Bree Serif |
| Body | Roboto |
| Fallback | Montserrat Light |

---

## Workflow: Neue Präsentation erstellen

### Option 1: BSWI_Master.pptx als Vorlage öffnen

1. BSWI_Master.pptx öffnen
2. "Speichern unter" → neuer Dateiname
3. Unbenötigte Folien löschen
4. Folien duplizieren und anpassen
5. Inhalte einfügen

### Option 2: Mit Claude/Code bearbeiten

```bash
# 1. Template analysieren
python scripts/thumbnail.py BSWI_Master.pptx
python -m markitdown BSWI_Master.pptx

# 2. Entpacken
python scripts/office/unpack.py BSWI_Master.pptx unpacked/

# 3. Folien bearbeiten (XML in ppt/slides/)
# 4. Aufräumen
python scripts/clean.py unpacked/

# 5. Neu packen
python scripts/office/pack.py unpacked/ output.pptx --original BSWI_Master.pptx
```

---

## Folien-Typen für BS:WI

### Titelfolie
- Großes Logo/Icon
- Claim "Kompetent Zukunft Gestalten"
- Titel der Präsentation
- Optional: Datum, Autor

### Agenda-Folie
- Nummerierte Punkte
- Icons pro Abschnitt (optional)

### Inhaltsfolie
- Überschrift links oben
- Text oder Bullets links
- Bild/Grafik rechts

### Zwei-Spalten-Folie
- Für Vergleiche
- Pro/Contra
- Vorher/Nachher

### Zitat-Folie
- Großes Zitat zentriert
- Quelle darunter

### Abschlussfolie
- Logo
- Kontaktdaten
- "Kompetent Zukunft Gestalten"

---

## Bildsprache

> **Echt, freundlich, weltoffen, international**

- Echte Fotos von der Schule
- Authentische Situationen
- Diverse Menschen
- Helle, freundliche Atmosphäre

---

## Do's und Don'ts

### ✅ Do's
- Logo auf jeder Folie (klein, Ecke)
- Einheitliche Schriftgrößen
- Genug Weißraum
- Max. 6 Bullet Points pro Folie
- Bilder verwenden

### ❌ Don'ts
- Keine überfüllten Folien
- Keine anderen Farben als CI
- Logo nicht drehen oder verzerren
- Keine Comic Sans oder ähnlich
- Keine animierten GIFs

---

## Kontakt

**Dirk Schulenburg**  
BS:WI – Berufliche Schule für Wirtschaft und Internationales Hamburg  
vorname.nachname@schule.de

---

## Dateien

| Datei | Beschreibung |
|-------|-------------|
| `BSWI_Master.pptx` | Offizielle PowerPoint-Vorlage |
| `Logo_BSWI_*.svg/png` | Logo-Varianten |
| `BSWI_Corporate_Design_Manual.pdf` | Vollständiges CI-Handbuch |
