---
name: media-factory
description: >
  Generate and deploy multimedia content (SVG infographics, Mermaid diagrams, Pexels photos,
  Kokoro TTS audio, AI images, AI videos, HeyGen avatars) for learning modules and web platforms.
  Use when: "Infografik erstellen", "Diagramm", "Bild suchen", "Audio", "Narration", "Podcast",
  "Illustration", "Video erstellen", "Multimedia", "Media Factory", content needs visuals or audio.
license: MIT
version: "1.0"
date: 2026-03-12
agent: DevOps
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
  - AskUserQuestion
  - mcp__MCP_DOCKER__sendMessage
---

# Media Factory

Generate and deploy multimedia content for learning modules and web platforms. Works standalone
or integrated into other skills (4K-Optimizer, Blog-Workflow, Lesson-Creator).

## When to Use

- User asks for a visual, diagram, infographic, illustration, photo, or audio
- Another skill detects a multimedia gap (e.g., 4K-Analyzer recommends visuals)
- User says "Media Factory" or any trigger phrase above

## Quick Start

1. **Determine what's needed** — read the router decision matrix (router.md)
2. **Identify the project** — ask which platform if not obvious (read branding/variants.json)
3. **Generate** — invoke the appropriate generator sub-file
4. **Deploy** — use deployer.md to send the asset to the target platform

## Workflow

### Step 1: Understand the Request

Parse what the user needs:
- **Explicit tool request?** → Use that tool directly (e.g., "Nutze Pexels" → image-search.md)
- **Topic + context?** → Consult router.md decision matrix for recommendation
- **From another skill?** → The calling skill provides context and target

### Step 2: Select Project Branding

Read `claude-skills/media-factory/branding/variants.json` to get the color palette, font, and style
for the target project. If the target is unclear, ask the user:
> "Für welches Projekt? (dirk-schulenburg / cannabis-kultur / stecklingsmeister / lernmodule / bswi)"

### Step 3: Generate

Invoke the appropriate generator file:
| Generator | File | Cost |
|-----------|------|------|
| SVG Infographic/Diagram | generators/svg-generator.md | Free |
| Mermaid Flowchart | generators/mermaid-generator.md | Free |
| Pexels Stock Photo | generators/image-search.md | Free |
| Illustration (Undraw Library) | generators/illustration-search.md | Free |
| Kokoro TTS Audio | generators/tts-audio.md | Free |
| AI Image (Nano Banana) | generators/ai-image.md | ~$0.04-0.24 |
| AI Video (Veo 3.1) | generators/ai-video.md | ~$0.15-0.75/s |
| Avatar Video (HeyGen) | generators/avatar-video.md | ~$1/min |
| Canva Design | generators/canva-design.md | Free (Edu) |

### Step 4: Deploy

Read deployer.md and upload the generated asset to the target platform.

### Step 5: Log

For paid generators, append a line to `_assets/media-factory/cost-log.jsonl`.

## Cost Control

**Free generators** (SVG, Mermaid, Pexels, Illustration Library, Kokoro TTS): Run automatically.

**Paid generators** (Nano Banana, Veo, HeyGen): ALWAYS show estimated cost and ask for confirmation:
```
Ich würde ein [TOOL] [ASSET-TYPE] generieren:
  Prompt: "[PROMPT]"
  Geschätzte Kosten: ~$X.XX

Generieren? (j/n)
```

Read cost-log on startup: `cat _assets/media-factory/cost-log.jsonl | ...` to show month-to-date.

## Integration

Other skills can invoke Media Factory by including this instruction:
> "Read and follow claude-skills/media-factory/SKILL.md to generate [TYPE] for [TOPIC]."
