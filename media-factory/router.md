# Media Factory Router — Decision Matrix

## How to Use

Given a content request, match the **context** column to determine the best **medium** and **tool**.
If multiple tools could work, prefer the free option. If a paid option would be significantly better,
present both options to the user.

## Decision Matrix

| Context | Signals | Medium | Primary Tool | Fallback |
|---------|---------|--------|-------------|----------|
| Process, workflow, steps | "Ablauf", "Prozess", "Schritte", "wie funktioniert" | Flowchart | Mermaid | Claude SVG |
| Data, comparison, statistics | "Vergleich", "Daten", "Statistik", "Übersicht" | Infographic | Claude SVG | Mermaid pie/bar |
| Concept, abstract idea | "Konzept", "Erklärung", "Was ist" | Illustration | Illustration Library | Nano Banana |
| Atmosphere, real-world scene | "Foto", "Stimmung", "Beispiel" | Photo | Pexels | Nano Banana |
| Technical architecture | "Architektur", "System", "Komponenten" | Diagram | Mermaid | Claude SVG |
| Timeline, history | "Geschichte", "Timeline", "Entwicklung" | Timeline diagram | Mermaid (Gantt) | Claude SVG |
| Explainer, talking head | "Erklärvideo", "Avatar", "Moderator" | Avatar video | HeyGen | Kokoro TTS + image |
| Short visual clip | "Clip", "Animation", "kurzes Video" | AI video | Veo 3.1 | HeyGen |
| Read-aloud, voiceover | "Vorlesen", "Narration", "Audio" | Audio | Kokoro TTS | — |
| Podcast, dialogue | "Podcast", "Dialog", "Gespräch" | Two-voice audio | Kokoro TTS (2 voices) | — |
| Dictation exercise | "Diktat", "Hörverständnis" | Audio + text | Kokoro TTS | — |
| Certificate, social media | "Zertifikat", "Social Media", "Flyer" | Designed graphic | Canva | Claude SVG |
| Photorealistic, detailed | "fotorealistisch", "detailliert", "KI-Bild" | AI image | Nano Banana Pro | Nano Banana |

## Override Rules

- If the user explicitly names a tool → use that tool, skip the matrix
- If the context matches multiple rows → prefer the free option, mention the paid alternative
- If no row matches → ask the user what kind of output they want

## Project Detection

Detect the target project from context:
- Cannabis/Stecklinge/Anbau/Kultur → `cannabis-kultur`
- Moodle/Kurs/Sektion/SuS → `bswi`
- Lernmodul/Excel/Word/KI-Handel → `lernmodule`
- Blog/Webseite/Portfolio → `dirk-schulenburg`
- If unclear → ask
