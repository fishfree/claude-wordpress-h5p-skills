# Pexels Image Search

Search and download stock photos from Pexels, optimized for web deployment.

## When to Use

- Need a real photograph (not illustration or diagram)
- Atmospheric, mood-setting imagery
- Blog featured images
- Background images

## Input

- **query**: Search keywords (English preferred for larger Pexels database)
- **size**: large (default) | medium | small
- **orientation**: landscape (default) | portrait | square
- **count**: Number of results to choose from (default: 5)

## Process

### 1. Search Pexels

```bash
curl -s -H "Authorization: PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=QUERY&per_page=5&orientation=landscape" \
  | python3 -c "import sys,json; photos=json.load(sys.stdin)['photos']; [print(f'{p[\"id\"]}: {p[\"alt\"]} — {p[\"src\"][\"large\"]}') for p in photos]"
```

The PEXELS_API_KEY is available in the environment or in `tools/wp-post-v2.py`.

### 2. Query Optimization Tips

- **Specific beats generic**: "cannabis plant trichomes macro" > "plant"
- **Add context**: "classroom students learning technology" > "education"
- **Use adjectives**: "bright modern workspace laptop" > "office"
- **English always**: Pexels has 10x more English-tagged photos

### 3. Download + Optimize

```bash
# Download the selected photo
curl -s -L "PHOTO_URL" -o /tmp/pexels-raw.jpg

# Optimize: resize to 1200x630, convert to WebP, 85% quality
# Requires: sharp-cli or imagemagick
convert /tmp/pexels-raw.jpg -resize 1200x630^ -gravity center -extent 1200x630 -quality 85 /tmp/pexels-optimized.webp
```

If imagemagick is not available, use the raw JPEG — it's still usable.

### 4. Save

Save to `_assets/media-factory/{project}/images/{filename}.webp`
Write metadata sidecar with Pexels attribution (required by license):

```json
{
  "file": "cannabis-greenhouse.webp",
  "generator": "image-search",
  "source": "pexels",
  "pexels_id": 12345,
  "photographer": "Name",
  "photographer_url": "https://pexels.com/@name",
  "original_url": "https://...",
  "project": "cannabis-kultur",
  "cost": 0,
  "date": "2026-03-12"
}
```

## Fallback

1. Zero results → broaden the query (remove adjectives, try synonyms)
2. Still zero → try alternative query in German
3. API error → inform user, suggest manual search at pexels.com
