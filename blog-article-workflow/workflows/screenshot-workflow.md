# Screenshot-Workflow für Blog-Artikel

Standardisierter Prozess für Screenshots in Tutorials und Blog-Artikeln.

## Tools

| Tool | Plattform | Zweck |
|------|-----------|-------|
| **Win+Shift+S** | Windows | Schneller Screenshot (Snipping Tool) |
| **ShareX** | Windows | Annotationen, Auto-Upload, Workflows |
| **Greenshot** | Windows | Leichtgewichtig, Annotation |
| **Cmd+Shift+4** | Mac | Bereichsauswahl |

**Empfehlung:** Win+Shift+S für schnelle Captures, ShareX für annotierte Tutorial-Screenshots.

## Naming Convention

```
[artikel-slug]-screenshot-[nummer]-[kontext].png
```

**Beispiele:**
```
claude-tutorial-screenshot-01-editor.png
claude-tutorial-screenshot-02-settings.png
claude-tutorial-screenshot-03-result.png
h5p-guide-screenshot-01-content-type.png
h5p-guide-screenshot-02-preview.png
```

## Capture-Standards

### Bildgröße
- **Breite:** 1200-1400px (skaliert in WordPress auf max. 1024px)
- **Höhe:** Variabel, aber max. 900px (sonst croppen)
- **DPI:** 96 (Standard-Bildschirm, nicht Retina)

### Was capturen
```
✅ Nur den relevanten UI-Bereich
✅ Genug Kontext für Orientierung
✅ Menüs/Dropdowns im geöffneten Zustand
✅ Cursor auf dem relevanten Element (bei Hover-States)

❌ Nicht die gesamte Browser-Chrome
❌ Keine Taskbar/Desktop-Elemente
❌ Keine persönlichen Daten (Email, Name in URL-Bar)
❌ Keine API-Keys oder Passwörter
```

### Annotation-Standards

**Elemente:**
- **Rote Pfeile** (2px) → Zeigen auf wichtige UI-Elemente
- **Rote Boxen** (2px, keine Füllung) → Hervorhebung von Bereichen
- **Nummerierte Kreise** (rot, weiß gefüllt) → Schritt-Reihenfolge
- **Text-Callouts** (schwarz auf halbtransparent weiß) → Erklärungen

**Farben:**
```
Hervorhebung:  #FF0000 (Rot) - Pfeile, Boxen
Nummerierung:  #FF0000 Kreis mit #FFFFFF Text
Callout-Text:  #333333 auf rgba(255,255,255,0.9)
Blur/Redact:   Gaussian Blur für sensible Daten
```

## Upload-Workflow

### Quick (Einzelbild)

```bash
# Screenshot optimieren und hochladen
python tools/wp-post-v2.py upload-image \
  --file "claude-tutorial-screenshot-01-editor.png" \
  --title "Claude Tutorial - Editor Interface" \
  --alt "Screenshot of Claude Code editor with open file" \
  --optimize
```

### Batch (mehrere Screenshots)

```bash
# Alle Screenshots eines Artikels hochladen
python tools/wp-post-v2.py batch-upload \
  --folder "C:/screenshots/claude-tutorial/" \
  --optimize \
  --prefix "Claude Tutorial - "
```

### Asset Library Integration

Screenshots nach `_assets/blog/[slug]/` kopieren:

```bash
# Ordner erstellen
mkdir _assets/blog/claude-tutorial

# Screenshots hinein kopieren (oder direkt dort speichern)
cp screenshot-*.png _assets/blog/claude-tutorial/
```

## WordPress Embedding

### Standard (mit Kontext)

```html
<!-- wp:paragraph -->
<p><strong>Schritt 2:</strong> Klicke auf "Interactive Video" im Dropdown:</p>
<!-- /wp:paragraph -->

<!-- wp:image {"id":125,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="[URL]"
       alt="Screenshot of H5P editor with Interactive Video selected"
       class="wp-image-125"/>
  <figcaption class="wp-element-caption">Wähle Interactive Video als Content-Typ</figcaption>
</figure>
<!-- /wp:image -->
```

### Kompakt (ohne Caption)

```html
<!-- wp:image {"id":126,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="[URL]"
       alt="Settings panel with highlighted save button"
       class="wp-image-126"/>
</figure>
<!-- /wp:image -->
```

## Alt-Text Formeln für Screenshots

```
"Screenshot of [tool/interface] showing [was sichtbar ist]"
"Screenshot of [tool] with [element] highlighted"
"[Tool] interface after [action] - [result visible]"
```

**Beispiele:**
```
"Screenshot of Claude Code editor with Python file open"
"Screenshot of WordPress media library with upload dialog"
"Moodle course page after adding H5P activity - quiz visible in section 3"
```

## Checkliste pro Screenshot

- [ ] Relevanter Bereich gecaptured (nicht zu viel, nicht zu wenig)
- [ ] Sensible Daten geblurrt/entfernt
- [ ] Annotationen hinzugefügt (falls Tutorial-Schritt)
- [ ] Dateiname folgt Convention: `[slug]-screenshot-[nr]-[kontext].png`
- [ ] Alt-Text geschrieben
- [ ] Optimiert und hochgeladen (`--optimize`)
