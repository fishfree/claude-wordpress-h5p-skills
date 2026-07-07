# Illustration Guide - Best Practices für Blog-Visuals

Entscheidungshilfe: Welches Bild wann, woher, und wie einsetzen.

## Entscheidungsbaum: Welche Bildquelle?

```
Brauche ich ein Bild?
│
├─ Featured Image (Hero) ───────── Pexels via --auto-image (30 Sek)
│                                   → Echtes Foto, professionell, automatisch optimiert
│
├─ Konzept-Illustration ────────── undraw.co (2-3 Min)
│   (abstrakt, Workflow,            → Flat Design, kostenlos, konsistenter Stil
│    Teamwork, Idee)                → find-illustration "keywords"
│
├─ Tutorial-Schritt ────────────── Screenshot (1-2 Min)
│   (UI, Editor, Settings)          → Win+Shift+S → annotieren → upload-image --optimize
│
├─ Daten/Vergleich ─────────────── Diagramm/Chart (5-10 Min)
│   (Zahlen, Prozesse)              → Mermaid, draw.io, oder HTML-Tabelle
│
└─ Aufzählung/Feature-Liste ────── Emoji (0 Sek)
                                    → ✅ 🚀 📊 💡 direkt im Text
```

## Pexels vs. undraw.co - Wann was?

| Kriterium | Pexels (Fotos) | undraw.co (Illustrationen) |
|-----------|----------------|---------------------------|
| **Beste für** | Featured Images, Header, Mood | Konzepte, Workflows, abstrakte Ideen |
| **Wirkung** | Professionell, emotional, real | Modern, clean, tech-affin |
| **Geschwindigkeit** | 30 Sek (automatisiert) | 2-3 Min (manuell suchen) |
| **Konsistenz** | Variiert (verschiedene Fotografen) | Einheitlicher Stil |
| **Anpassbar** | Nein (Foto ist Foto) | Ja (Farbe änderbar auf undraw.co) |
| **Lizenz** | Pexels License (frei, Attribution optional) | MIT-ähnlich (frei, keine Attribution) |

### Pexels nutzen wenn...
- Featured Image / Hero benötigt
- Emotionale Wirkung wichtig (Menschen, Atmosphäre)
- Schnelligkeit zählt (Auto-Image)
- Reale Szenarien gezeigt werden (Arbeitsplatz, Klassenzimmer)

### undraw.co nutzen wenn...
- Abstrakte Konzepte visualisiert werden (Teamwork, Datenfluss, Lernen)
- Konsistenter Stil über mehrere Inline-Bilder gebraucht wird
- Tech-Themen illustriert werden (Coding, Server, APIs)
- Farblich zum Branding passen soll

### Emoji nutzen wenn...
- Feature-Listen aufgelockert werden sollen
- Kurze visuelle Marker in Überschriften
- Kein Platz/Bedarf für echte Bilder
- Quick-Reference / Checklisten

## Gute vs. schlechte Bildauswahl

### Featured Images

**Gut:**
```
✅ "modern classroom students digital tablets learning"
   → Zeigt echte Szene, relevant zum Thema, professionell

✅ "coffee laptop morning workspace productivity"
   → Atmosphärisch, universal ansprechend, passt zu Produktivitäts-Artikeln

✅ "teacher whiteboard explaining concept"
   → Direkt relevant für Bildungs-Content
```

**Schlecht:**
```
❌ "work" → Zu generisch, liefert zufällige Ergebnisse
❌ "technology blue abstract" → Stock-Photo-Klischee, sagt nichts aus
❌ "happy people office" → Generic corporate, wirkt unauthentisch
```

### Inline-Illustrationen

**Gut:**
```
✅ Illustration nach 300-400 Wörtern Text (visueller Break)
✅ Illustration zeigt das Konzept, das gerade erklärt wird
✅ undraw "collaboration" bei einem Abschnitt über Teamarbeit
```

**Schlecht:**
```
❌ Illustration hat keinen Bezug zum Abschnitt (nur Deko)
❌ 5 Illustrationen in 500 Wörtern (überladen)
❌ Illustration wiederholt was der Text schon sagt (redundant)
```

### Screenshots

**Gut:**
```
✅ Nur den relevanten UI-Bereich gecaptured
✅ Roter Pfeil zeigt auf den Button, der geklickt werden soll
✅ Nummerierte Kreise für mehrstufige Aktionen im gleichen Screenshot
```

**Schlecht:**
```
❌ Ganzer Desktop mit Taskbar sichtbar
❌ Keine Annotation - Leser muss selbst suchen
❌ Screenshot ist 3000px breit und unscharf weil runterskaliert
```

## Visueller Rhythmus

**Empfohlene Abstände zwischen Visuals:**

```
Intro (200-300 Wörter)
    ↓ Featured Image (automatisch oben)
Text (300-400 Wörter)
    ↓ Illustration oder Screenshot
Text (300-400 Wörter)
    ↓ Illustration oder Screenshot
Text (300-400 Wörter)
    ↓ Optional: Drittes Visual
Conclusion (200 Wörter)
```

**Faustregeln:**
- 800-1200 Wörter: 1-2 Visuals + Emoji
- 1200-2000 Wörter: 2-3 Visuals + Emoji
- 2000+ Wörter: 3-5 Visuals + Emoji
- Nie mehr als 500 Wörter ohne visuellen Break

## Checkliste: Visuelle Konsistenz

### Innerhalb eines Artikels
- [ ] Alle Screenshots haben gleichen Annotationsstil (Farbe, Pfeildicke)
- [ ] Illustrationen haben ähnlichen Stil (nicht Flat + 3D gemischt)
- [ ] Emoji werden konsistent eingesetzt (gleiche Emoji für gleiche Bedeutung)
- [ ] Alt-Texte folgen dem gleichen Schema

### Über Artikel hinweg (Serien)
- [ ] Featured Images haben ähnliche Stimmung/Farbpalette
- [ ] Gleicher Illustrationsstil (alle undraw ODER alle Pexels)
- [ ] Nummerierung der Screenshots ist konsistent

## Optimierungsrichtlinien

| Typ | Format | Zielgröße | Tool |
|-----|--------|-----------|------|
| Featured Image | WebP | < 80 KB | `--auto-image` (automatisch) |
| Inline Foto | WebP/JPEG | < 150 KB | `upload-image --optimize` |
| Illustration (PNG) | PNG | < 200 KB | `upload-image --optimize` |
| Illustration (SVG) | SVG | < 50 KB | Direkt hochladen |
| Screenshot | PNG | < 300 KB | `upload-image --optimize` |

## Quick-Reference: Befehle

```bash
# Featured Image (Pexels, automatisch)
python tools/wp-post-v2.py create --auto-image "keywords" ...

# Illustration suchen (undraw Katalog)
python tools/wp-post-v2.py find-illustration "education coding"

# Screenshot hochladen (optimiert)
python tools/wp-post-v2.py upload-image --file screenshot.png --optimize

# Batch-Upload (Ordner mit Screenshots)
python tools/wp-post-v2.py batch-upload --folder ./screenshots/ --optimize

# Bild auf Pexels suchen (manuell)
python tools/wp-post-v2.py find-image "classroom education" --limit 5
```

---

*Version 1.0 - 15.02.2026*
