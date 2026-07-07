---
name: hedgedoc-presentation
description: Erstellt professionelle Slide-Präsentationen auf HedgeDoc (reveal.js) im persönlichen Branding-Design. Hintergrundbild von Pexels, BS:WI-Logo als Wasserzeichen, dunkler Overlay mit transparenten Rändern. Nutze diesen Skill wenn der User eine Präsentation, Slides, einen Vortrag oder ein Blitzlicht erstellen möchte.
---

# HedgeDoc Presentation Skill

Erstellt öffentliche Präsentationen im persönlichen Branding-Design auf HedgeDoc (codimd.dirk-schulenburg.net) als reveal.js Slides.

## Wann diesen Skill nutzen

- "Präsentation erstellen"
- "Slides machen"
- "Vortrag vorbereiten"
- "Blitzlicht erstellen"
- "HedgeDoc Slides"
- Alles rund um öffentliche Präsentationen

## Design-Spezifikation

### Layer-Architektur (von hinten nach vorne)

```
Layer 1: Pexels-Hintergrundbild (fullscreen, cover)
Layer 2: BS:WI Logo weiss (oben rechts, 10%, Wasserzeichen)
Layer 3: Dunkler Overlay (70% schwarz, nur mittlere 90%)
Layer 4: Slide-Inhalt (Text, Listen, Quotes)
```

### Hintergrundbild

- **Quelle:** Pexels API (kostenlos, hotlinkbar)
- **Standard-Bild:** Sebastian Luna Foto (ID: 36068855) — dunkelgrüne Blätter
- **Alternative:** User kann anderes Pexels-Bild wählen
- **Format:** `?auto=compress&cs=tinysrgb&fit=crop&h=1080&w=1920` (Landscape, HD)
- **Pexels API Key:** In `tools/.env` als `PEXELS_API_KEY`

### BS:WI Logo

- **Datei:** `https://lernmodule.dirk-schulenburg.net/assets/bswi-logo-weiss.png`
- **Position:** Oben rechts (`right 3% top 3%`)
- **Größe:** 10% der Viewport-Breite
- **Wirkung:** Subtiles Wasserzeichen, scheint durch den transparenten Rand des Overlays

### Overlay

- **Farbe:** Schwarz, 72% Deckkraft (`rgba(0,0,0,0.72)`)
- **WICHTIG:** Nicht fullscreen! Oben und unten je 5% transparent
- **Technik:** CSS `linear-gradient` auf jeder Section
- **Effekt:** Hintergrundbild + Logo scheinen an den Rändern durch

### Farbschema

```css
/* Überschriften */
h1, h2:  #4ade80  (helles Grün, mit Glow-Shadow)
h3:      #86efac  (noch helleres Grün)

/* Text-Akzente */
strong:  #4ade80  (Grün)
code:    #86efac  auf rgba(74,222,128,0.1)
links:   #67e8f9  (Cyan)

/* Blockquotes */
background: rgba(74,222,128,0.08)
border-left: 4px solid #4ade80
```

## Template

### YAML-Header

```yaml
---
title: {{TITEL}}
description: {{UNTERTITEL}}
slideOptions:
  theme: black
  transition: slide
---
```

### CSS-Block (nach dem Header, vor dem Content)

```html
<style>
/* Layer 1: Pexels background + BS:WI watermark */
.reveal {
  background:
    url('https://lernmodule.dirk-schulenburg.net/assets/bswi-logo-weiss.png') right 3% top 3% / 10% auto no-repeat,
    url('{{PEXELS_IMAGE_URL}}') center / cover no-repeat !important;
}

/* Layer 2: Dark overlay — top/bottom 5% transparent */
.reveal .slides section {
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0,0,0,0.72) 5%,
    rgba(0,0,0,0.72) 95%,
    transparent 100%
  ) !important;
  padding-top: 40px !important;
  padding-bottom: 40px !important;
}

/* Typography */
.reveal h1, .reveal h2 {
  color: #4ade80 !important;
  text-shadow: 0 0 20px rgba(74,222,128,0.3);
}
.reveal h3 {
  color: #86efac !important;
}
.reveal blockquote {
  background: rgba(74,222,128,0.08);
  border-left: 4px solid #4ade80;
  padding: 10px 20px;
  font-style: italic;
}
.reveal strong {
  color: #4ade80;
}
.reveal code {
  color: #86efac;
  background: rgba(74,222,128,0.1);
}
.reveal a {
  color: #67e8f9 !important;
}
</style>
```

### Slide-Struktur

Slides werden durch `---` getrennt. Jede Slide maximal 5-7 Zeilen Content.

**Titel-Slide:**
```markdown
# {{TITEL}}

### {{UNTERTITEL}}

*Dirk Schulenburg — {{ANLASS}} {{DATUM}}*
```

**Content-Slides:**
```markdown
---

## {{ÜBERSCHRIFT}}

- Punkt 1
- Punkt 2
- Punkt 3

> **Zitat oder Kernaussage**
```

**Schluss-Slide:**
```markdown
---

# Danke!

### Fragen?

*Dirk Schulenburg — BS:WI Hamburg*
```

## Slide-Regeln

### Do

- Max 5-7 Zeilen Content pro Slide (reveal.js hat begrenzte Höhe!)
- Kurze Stichpunkte, keine ganzen Sätze
- Blockquotes für Kernaussagen
- `**Fett**` für Betonungen (wird grün dargestellt)
- Links als Markdown-Links
- Code-Blöcke für Prompts/Befehle

### Don't

- Keine Tabellen mit mehr als 4 Zeilen (Overflow-Gefahr!)
- Keine Emojis (professioneller Look)
- Keine Bilder im Content (Hintergrundbild reicht)
- Keine verschachtelten Listen
- Kein Content der über die Slide-Höhe hinausgeht

## Workflow

### Phase 1: Vorbereitung

1. **Thema & Anlass** klären (Konferenz, Workshop, Blitzlicht?)
2. **Dauer** bestimmen → Anzahl Slides (ca. 1 Slide pro Minute)
3. **Kernbotschaft** definieren

### Phase 2: Hintergrundbild wählen

Standardbild (dunkelgrüne Blätter) verwenden ODER neues Pexels-Bild suchen:

```bash
curl -s "https://api.pexels.com/v1/search?query=SUCHBEGRIFF&per_page=5&orientation=landscape" \
  -H "Authorization: $(grep PEXELS_API_KEY C:/Users/mail/entwicklung/docker/tools/.env | cut -d= -f2)"
```

Bild-URL-Format für den CSS-Hintergrund:
```
https://images.pexels.com/photos/{{ID}}/pexels-photo-{{ID}}.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1080&w=1920
```

### Phase 3: Slides erstellen

1. Markdown-Datei schreiben: `docs/presentations/{{YYYY-MM-DD}}-{{THEMA}}.md`
2. Template oben verwenden (Header + CSS + Slides)
3. Auf max 5-7 Zeilen pro Slide achten!

### Phase 4: Upload zu HedgeDoc

```bash
curl -s -X POST "https://codimd.dirk-schulenburg.net/new" \
  -H "Content-Type: text/markdown" \
  --data-binary @"DATEI.md" \
  -D - -o /dev/null 2>&1 | grep -i location
```

**Ergebnis:** HedgeDoc gibt die Note-URL zurück.

- **Edit-Modus:** `https://codimd.dirk-schulenburg.net/{{NOTE_ID}}`
- **Slide-Modus:** `https://codimd.dirk-schulenburg.net/p/{{NOTE_ID}}`

### Phase 5: Feintuning

User prüft die Slides im Browser. Typische Anpassungen:
- Slide-Overflow → Content kürzen
- Hintergrundbild ändern → CSS-URL tauschen
- Farbschema anpassen → CSS-Variablen ändern

Bei jeder Änderung: neue Note erstellen (HedgeDoc hat kein Update-API).

## Referenz-Präsentation

`docs/presentations/2026-02-24-bsk-blitzlicht-claude.md` — BSK Blitzlicht "KI im Klassenzimmer"

## Standard-Hintergrundbilder

| Thema | Pexels-ID | Beschreibung |
|-------|-----------|--------------|
| Standard/Natur | 36068855 | Dunkelgrüne Blätter (Sebastian Luna) |

Weitere können per Pexels-Suche gefunden und hier ergänzt werden.
