# AI Video Generator (Veo)

> **Phase 3** — Active. Uses same `GOOGLE_API_KEY` from `.env`

## Models (verified 2026-03-13)

| Name | Model ID | Cost | Quality |
|------|----------|------|---------|
| **Veo 2** | `veo-2.0-generate-001` | ~$0.10/s | Good |
| **Veo 3 Fast** | `veo-3.0-fast-generate-001` | ~$0.15/s | Fast, good |
| **Veo 3** | `veo-3.0-generate-001` | ~$0.40/s | High quality |
| **Veo 3.1 Fast** | `veo-3.1-fast-generate-preview` | ~$0.15/s | Newest, fast |
| **Veo 3.1** | `veo-3.1-generate-preview` | ~$0.40-0.75/s | Best quality, native audio |

Default: `veo-3.1-fast-generate-preview` (best price/quality for short clips)

**Duration:** 4, 6, or 8 seconds. 8s at $0.15/s = ~$1.20 per video.

## API Reference

Docs: https://ai.google.dev/gemini-api/docs/video

**IMPORTANT:** Veo uses an **async workflow** (submit → poll → download). Videos take 30-120 seconds to generate.

## Process

### 1. Load API Key

```bash
GOOGLE_API_KEY=$(grep '^GOOGLE_API_KEY=' .env | cut -d= -f2)
BASE_URL="https://generativelanguage.googleapis.com/v1beta"
```

### 2. Show cost estimate and get confirmation

Read cost-tracker.md for the confirmation template. Estimate: duration * per-second rate.

### 3. Submit Video Generation

```bash
MODEL="veo-3.1-fast-generate-preview"

OPERATION=$(curl -s "${BASE_URL}/models/${MODEL}:predictLongRunning" \
  -H "x-goog-api-key: $GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "instances": [{
      "prompt": "PROMPT_HERE"
    }]
  }' | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','ERROR'))")

echo "Operation: $OPERATION"
```

### 4. Poll Until Done

```bash
while true; do
  RESP=$(curl -s -H "x-goog-api-key: $GOOGLE_API_KEY" "${BASE_URL}/${OPERATION}")
  DONE=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('done',False))")
  if [ "$DONE" = "True" ]; then
    echo "Video ready!"
    break
  fi
  echo "Generating... (polling every 10s)"
  sleep 10
done
```

### 5. Download Video

```bash
VIDEO_URI=$(echo "$RESP" | python3 -c "
import sys,json
r=json.load(sys.stdin)
samples=r.get('response',{}).get('generateVideoResponse',{}).get('generatedSamples',[])
if samples: print(samples[0]['video']['uri'])
else: print('ERROR: no video in response')
")

curl -L -o OUTPUT_PATH.mp4 -H "x-goog-api-key: $GOOGLE_API_KEY" "$VIDEO_URI"
```

### 6. Save

Save to `_assets/media-factory/{project}/video/{filename}.mp4`
Write metadata sidecar. Log cost to cost-log.jsonl.

## Prompt Tips

- **Be cinematic:** "Slow dolly shot of...", "Close-up tracking...", "Aerial view of..."
- **Specify mood:** "warm golden hour lighting", "dramatic shadows", "soft focus"
- **Keep it simple:** 1-2 subjects, one action, clear description
- **Duration hint:** Short prompts = 4s clips, detailed prompts = 8s

## Fallback

1. API error / timeout → retry once with simpler prompt
2. Generation fails → fall back to Kokoro TTS audio + static image
3. Budget exceeded → warn user, suggest Nano Banana still image instead
