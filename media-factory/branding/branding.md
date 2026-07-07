# Media Factory Branding System

## Core Principle

All generated media follows a consistent branding per project. The "Dirk Schulenburg" brand family
is recognizable across projects through shared typography and quality standards, but each project
has its own color palette, accent, and visual style.

## How to Apply

### 1. Read the variant

```bash
cat claude-skills/media-factory/branding/variants.json | python3 -c "
import sys, json
variants = json.load(sys.stdin)
project = 'PROJECT_KEY'
v = variants[project]
print(f'Primary: {v[\"primary\"]}')
print(f'Accent: {v[\"accent\"]}')
print(f'Font: {v[\"font\"]}')
print(f'Style: {v[\"style\"]}')
"
```

### 2. Apply to SVGs

Replace these tokens in SVG templates:
- `{primary}` → variant primary color
- `{secondary}` → variant secondary color
- `{accent}` → variant accent color
- `{background}` → variant background (gradient or solid)
- `{text}` → variant text color
- `{textMuted}` → variant muted text color
- `{font}` → variant font family

### 3. Apply to Mermaid

Mermaid supports theming via init directives:
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '{accent}',
  'primaryTextColor': '{text}',
  'primaryBorderColor': '{primary}',
  'lineColor': '{textMuted}',
  'fontFamily': '{font}'
}}}%%
flowchart TD
    A[Start] --> B[End]
```

### 4. Apply to Illustrations (Undraw SVGs)

Undraw SVGs use a single accent color (usually `#6c63ff`). Replace it:
```bash
sed -i 's/#6c63ff/{accent}/g' illustration.svg
```

### 5. Quality Standards

All generated media must meet:
- **Retina-ready**: SVGs are resolution-independent (✓ by nature)
- **Optimized size**: SVGs < 50KB, WebP < 200KB, MP3 < 5MB per minute
- **Accessible**: Alt text for all images, captions for audio
- **Consistent font**: Always use the project font, never system defaults in SVGs
