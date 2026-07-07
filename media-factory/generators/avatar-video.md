# Avatar Video Generator (HeyGen)

> **Phase 3** — Requires HeyGen API Key (`HEYGEN_API_KEY` env var)

## Pricing

~$1/minute of generated video.

## API Reference (Async Workflow)

1. Submit: `POST https://api.heygen.com/v2/video/generate`
2. Poll: `GET https://api.heygen.com/v1/video_status.get?video_id=ID` (every 30s, timeout 10min)
3. Download: URL from completed response

## Status

Not yet implemented. Use Kokoro TTS audio + static image as alternative.
