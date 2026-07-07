# SVG Generator

Generate branded SVG infographics, diagrams, and visual content using Claude's native SVG generation.

## When to Use

- Infographics (process overviews, comparisons, data summaries)
- Scientific diagrams (biological processes, chemical pathways)
- Branded visual content (section headers, feature cards)
- Any visual that benefits from vector quality and small file size

## Input

- **topic**: What the SVG should depict
- **type**: infographic | diagram | process | comparison | header | wheel
- **project**: Key from branding/variants.json (determines colors, fonts, style)
- **dimensions**: Default 800x500, override as needed

## Process

### 1. Load branding

Read `claude-skills/media-factory/branding/variants.json` and extract the project variant.

### 2. Generate SVG

Follow these design rules strictly:

**Layout:**
- viewBox: `0 0 {width} {height}`
- Background: Use project gradient or solid color
- Padding: 40px minimum on all sides
- Grid: Align elements to invisible grid (40px increments)

**Typography:**
- Font: Use project font from variants.json
- Title: 24px bold, project text color
- Subtitle: 16px, project textMuted color
- Labels: 13px, project text color
- Numbers/stats: 32px bold, project accent color

**Colors:**
- Primary elements: project primary
- Backgrounds: project background gradient
- Accents/highlights: project accent
- Text: project text / textMuted
- Use opacity variants: `{accent}15` for light fills, `{accent}40` for medium

**Effects (use sparingly):**
- Subtle glow: `<filter id="glow"><feGaussianBlur stdDeviation="3" /></filter>`
- Rounded rects: rx="8"
- Gradient fills for backgrounds

**Structure for common types:**

Infographic (comparison):
```svg
<svg viewBox="0 0 800 500">
  <!-- Background gradient -->
  <defs><linearGradient id="bg">...</linearGradient></defs>
  <rect width="800" height="500" fill="url(#bg)" rx="12"/>
  <!-- Title -->
  <text x="400" y="50" text-anchor="middle" font-size="24" font-weight="bold">Title</text>
  <!-- Content cards (3-column grid) -->
  <g transform="translate(40, 100)">
    <!-- Card 1 --> <rect width="220" height="300" rx="8" fill="{primary}"/>
    <!-- Card 2 --> <rect x="260" width="220" height="300" rx="8" fill="{primary}"/>
    <!-- Card 3 --> <rect x="520" width="220" height="300" rx="8" fill="{primary}"/>
  </g>
</svg>
```

Process diagram (horizontal flow):
```svg
<svg viewBox="0 0 800 300">
  <!-- Steps connected by arrows -->
  <g transform="translate(40, 100)">
    <!-- Step circles with numbers -->
    <!-- Arrow connectors -->
    <!-- Labels below -->
  </g>
</svg>
```

### 3. Validate

Check the generated SVG:
- Valid XML (no unclosed tags)
- No `<script>` tags
- All text uses the project font
- Colors match the branding variant

### 4. Save

Save to `_assets/media-factory/{project}/svg/{filename}.svg`
Write metadata sidecar (see deployer.md).

## Existing Examples

Reference these for style quality:
- `docker/tmp/biosynthese.svg` — Cannabinoid biosynthesis pathway (dark navy, glow effects)
- `docker/tmp/terpene-wheel.svg` — Terpene flavor wheel (circular layout, 800x800)
- `docker/tmp/ecs-rezeptoren.svg` — Receptor mapping (semantic colors per substance)

## Fallback

If SVG generation fails (invalid XML, too complex):
1. Retry with simpler layout (fewer elements, basic shapes)
2. If still fails → switch to Mermaid generator for a diagram representation
