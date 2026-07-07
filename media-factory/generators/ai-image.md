# AI Image Generator (Nano Banana)

> **Phase 2** — Active. Requires `GOOGLE_API_KEY` in `.env`

## Models (verified 2026-03-13)

| Name | Model ID | Cost | Quality |
|------|----------|------|---------|
| **Nano Banana** | `gemini-2.5-flash-image` | ~$0.04/image | Fast, good |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | ~$0.13-0.24/image | Best quality |
| **Nano Banana 3.1** | `gemini-3.1-flash-image-preview` | ~$0.04/image | Newest flash |
| **Imagen 4** | `imagen-4.0-generate-001` | ~$0.04/image | Google Imagen |
| **Imagen 4 Ultra** | `imagen-4.0-ultra-generate-001` | ~$0.08/image | Highest quality |

Default: `gemini-2.5-flash-image` (best price/quality ratio)

## API Reference

Docs: https://ai.google.dev/gemini-api/docs/image-generation

## Process

### 1. Load API Key

```bash
GOOGLE_API_KEY=$(grep '^GOOGLE_API_KEY=' .env | cut -d= -f2)
```

### 2. Show cost estimate and get confirmation

Read cost-tracker.md for the confirmation template.

### 3. Generate Image

```bash
MODEL="gemini-2.5-flash-image"  # or gemini-3-pro-image-preview for higher quality

curl -s "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "Generate an image: PROMPT"}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
  }' | python3 -c "
import sys, json, base64
resp = json.load(sys.stdin)
if 'error' in resp:
    print(f'ERROR: {resp[\"error\"][\"message\"]}')
    sys.exit(1)
for part in resp['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        img = base64.b64decode(part['inlineData']['data'])
        with open('OUTPUT_PATH', 'wb') as f:
            f.write(img)
        print(f'OK: {len(img)} bytes saved')
    elif 'text' in part:
        print(f'Text: {part[\"text\"][:200]}')
"
```

Response: base64-encoded image in `parts[].inlineData.data`

### 4. Save

Save to `_assets/media-factory/{project}/images/{filename}.png`
Write metadata sidecar (see deployer.md).

### 5. Log cost

Append to `_assets/media-factory/cost-log.jsonl` (see cost-tracker.md).

## Prompt Tips

- **Style prefixes**: "Botanical illustration:", "Flat design icon:", "Photorealistic:", "Watercolor:"
- **Negative context**: Add "no text, no watermarks, no logos" for cleaner results
- **Aspect ratio**: Specify in prompt: "wide 16:9 landscape" or "square 1:1"
- **Quality boost**: "Professional, high detail, sharp focus, studio lighting"

## Fallback

1. API error → retry once with simpler prompt
2. Still fails → fall back to Pexels search
3. If abstract concept → fall back to Claude SVG generator
