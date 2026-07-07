# Kokoro TTS Audio Generator

Generate spoken audio using Kokoro TTS via the Voice-MCP server.

## When to Use

- Narration: Read learning content aloud
- Podcast: Two-speaker dialogue
- Dictation: Slow speech with pauses for writing exercises
- Audio quiz: Spoken questions with answer pauses
- Multi-language: Same content in up to 7 languages

## Input

- **text**: The text to speak
- **language**: de | en | es | fr | it | nl | pt
- **voice**: Voice ID (see available voices below)
- **mode**: narration | podcast | dictation | quiz
- **speed**: 0.8 (slow/dictation) | 1.0 (normal) | 1.2 (fast)

## Available Voices

Check Voice-MCP for current voice list. Common voices:
- `af_heart` — Female, warm (default)
- `am_adam` — Male, neutral
- `bf_emma` — Female, British
- `bm_george` — Male, British

## Process

### Mode: Narration (single voice)

Use the Voice-MCP TTS endpoint to generate audio for the full text.
The Voice-MCP is accessible via MCP tools or direct API call on the server.

```bash
# Via SSH on Hetzner (docker exec — service not exposed on host network)
ssh -i $SSH_KEY $HETZNER \
  "docker exec kokoro-tts curl -s -X POST http://localhost:8880/v1/audio/speech \
    -H 'Content-Type: application/json' \
    -d '{\"model\": \"kokoro\", \"input\": \"TEXT\", \"voice\": \"VOICE\", \"speed\": SPEED, \"response_format\": \"mp3\"}' \
    --output /tmp/narration.mp3 && \
  docker cp kokoro-tts:/tmp/narration.mp3 /tmp/narration.mp3"

# Download to local
scp -i $SSH_KEY $HETZNER:/tmp/narration.mp3 _assets/media-factory/PROJECT/audio/
```

**API Notes (OpenAI-compatible):**
- `model`: always `"kokoro"`
- `input`: the text to speak (not `text`)
- `response_format`: `"mp3"` | `"wav"` | `"opus"`
- Container name: `kokoro-tts`, internal port: `8880`

### Mode: Podcast (two voices alternating)

1. Generate a dialogue script with two speakers (A and B)
2. Render each segment separately with different voices
3. Merge with ffmpeg:

```bash
# On the server (via docker exec):
# 1. Generate segments
docker exec kokoro-tts curl -s -X POST http://localhost:8880/v1/audio/speech -H 'Content-Type: application/json' -d '{"model":"kokoro","input":"Speaker A text","voice":"af_heart","response_format":"wav"}' -o /tmp/seg_01.wav
docker exec kokoro-tts curl -s -X POST http://localhost:8880/v1/audio/speech -H 'Content-Type: application/json' -d '{"model":"kokoro","input":"Speaker B text","voice":"am_adam","response_format":"wav"}' -o /tmp/seg_02.wav
# ... repeat for all segments

# 2. Create concat file
echo "file '/tmp/seg_01.wav'" > /tmp/concat.txt
echo "file '/tmp/seg_02.wav'" >> /tmp/concat.txt

# 3. Merge with ffmpeg
ffmpeg -f concat -safe 0 -i /tmp/concat.txt -codec:a libmp3lame -q:a 2 /tmp/podcast.mp3
```

### Mode: Dictation (slow with pauses)

1. Split text into sentences
2. Render each sentence at speed 0.8
3. Insert 3-second silence between sentences:

```bash
# Generate silence
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 3 /tmp/silence.wav

# Interleave: sentence, silence, sentence, silence, ...
# Build concat file with silence segments between speech
```

### Mode: Quiz (question + pause + options)

1. Render the question
2. Insert 5-second pause (thinking time)
3. Render answer options (A, B, C, D)
4. Merge all segments

## Prerequisite Check

Before generating audio, verify Voice-MCP is running:

```bash
ssh -i $SSH_KEY $HETZNER "docker ps --filter name=kokoro-tts --format '{{.Status}}'"
```

If not running:
```bash
ssh -i $SSH_KEY $HETZNER "cd /home/dirk/docker && docker compose -f docker-compose-voice.yml up -d"
```

Also verify ffmpeg is available (needed for podcast/dictation/quiz modes):
```bash
ssh -i $SSH_KEY $HETZNER "which ffmpeg || echo 'MISSING: install with apt install ffmpeg'"
```

## Save

Save to `_assets/media-factory/{project}/audio/{filename}.mp3`
Write metadata sidecar.

## Fallback

1. Voice-MCP not running → attempt auto-start via SSH
2. Auto-start fails → inform user: "Voice-MCP Container gestoppt. Bitte manuell starten."
3. ffmpeg missing → inform user, generate individual segments without merging
