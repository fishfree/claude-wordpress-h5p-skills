# Illustration Library

Search and retrieve SVG illustrations from the curated local library.
All illustrations are pre-downloaded Undraw.co SVGs (MIT license).

## When to Use

- Concept explanations needing a friendly visual
- Decorative illustrations for section headers
- Abstract concepts (teamwork, learning, technology, nature)
- When Pexels photos are too literal and SVG diagrams too technical

## Input

- **keyword**: Concept to illustrate (e.g., "learning", "teamwork", "plant")
- **project**: Target project (for accent color replacement)

## Process

### 1. Search the library index

Read `_assets/media-factory/illustrations/index.json` to find matching illustrations.
The index maps keywords to filenames.

### 2. Match keywords

Find the best match by comparing the input keyword against the index tags.
If multiple match, present the top 3 options to the user with descriptions.

### 3. Apply branding colors

Read the project branding from `branding/variants.json`, then replace
the default Undraw accent color with the project accent:

```bash
cp _assets/media-factory/illustrations/SOURCE.svg _assets/media-factory/PROJECT/svg/OUTPUT.svg
sed -i 's/#6c63ff/PROJECT_ACCENT/g' _assets/media-factory/PROJECT/svg/OUTPUT.svg
```

### 4. Save

The recolored SVG is ready for deployment.

## Fallback

If no illustration matches the keyword:
1. Suggest alternative keywords
2. If still no match → fall back to Claude SVG generator
3. Or suggest Nano Banana for a custom AI-generated illustration

## Library Management

To add new illustrations:
1. Visit undraw.co, find the illustration
2. Download SVG (set any accent color — will be replaced)
3. Save to `_assets/media-factory/illustrations/`
4. Add entry to `index.json`
